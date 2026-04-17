#!/usr/bin/env python3
"""
Update DuckDB history with current IP range crawl results.

- Tracks when each CIDR was first seen per provider
- Marks CIDRs as "retired" when removed from source
- Removes retired CIDRs after 4 weeks
- Injects still-within-window retired CIDRs back into JSON/CSV/TXT outputs
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import duckdb

RETIREMENT_WEEKS = 4


def count_ipv4_addresses(cidr_list: list[str]) -> int:
    """Calculate total number of IPv4 addresses in a list of CIDRs."""
    total = 0
    for cidr in cidr_list:
        if isinstance(cidr, str) and "." in cidr:
            try:
                network = ipaddress.IPv4Network(cidr, strict=False)
                total += network.num_addresses
            except (ValueError, ipaddress.AddressValueError):
                continue
    return total


def count_ipv6_64_subnets(cidr_list: list[str]) -> int:
    """
    Calculate total number of /64 subnets represented by IPv6 prefixes.
    A /64 is the standard IPv6 subnet size. Larger prefixes contain more /64s.
    Example: /32 contains 2^32 /64 subnets, /48 contains 2^16 /64 subnets.
    """
    total = 0
    for cidr in cidr_list:
        if isinstance(cidr, str) and ":" in cidr:
            try:
                network = ipaddress.IPv6Network(cidr, strict=False)
                if network.prefixlen <= 64:
                    # Number of /64s in this prefix: 2^(64 - prefixlen)
                    total += 2 ** (64 - network.prefixlen)
                else:
                    # Prefix is smaller than /64 (e.g., /128), count as 1
                    total += 1
            except (ValueError, ipaddress.AddressValueError):
                continue
    return total


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------


def open_db(db_path: Path) -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cidr_history (
            provider_id  VARCHAR NOT NULL,
            cidr         VARCHAR NOT NULL,
            first_seen   TIMESTAMPTZ NOT NULL,
            last_seen    TIMESTAMPTZ NOT NULL,
            retired_at   TIMESTAMPTZ,
            PRIMARY KEY (provider_id, cidr)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS provider_last_changed (
            provider_id       VARCHAR PRIMARY KEY,
            provider_name     VARCHAR NOT NULL,
            last_changed_at   TIMESTAMPTZ NOT NULL,
            last_crawled_at   TIMESTAMPTZ NOT NULL,
            ipv4_count        INTEGER NOT NULL DEFAULT 0,
            ipv6_count        INTEGER NOT NULL DEFAULT 0,
            retired_ipv4_count INTEGER NOT NULL DEFAULT 0,
            retired_ipv6_count INTEGER NOT NULL DEFAULT 0,
            ipv4_ip_count     INTEGER NOT NULL DEFAULT 0,
            ipv6_64_count     BIGINT NOT NULL DEFAULT 0,
            retired_ipv4_ip_count INTEGER NOT NULL DEFAULT 0,
            retired_ipv6_64_count BIGINT NOT NULL DEFAULT 0,
            method            VARCHAR,
            source            VARCHAR,
            ipv4_hash         VARCHAR,
            ipv6_hash         VARCHAR
        )
    """)

    # Migration: Add new columns for IP counts if they don't exist (pre-2025-04 schema)
    # Note: DuckDB doesn't support constraints in ALTER TABLE ADD COLUMN
    conn.execute("""
        ALTER TABLE provider_last_changed
        ADD COLUMN IF NOT EXISTS ipv4_ip_count INTEGER DEFAULT 0
    """)
    conn.execute("""
        ALTER TABLE provider_last_changed
        ADD COLUMN IF NOT EXISTS ipv6_64_count BIGINT DEFAULT 0
    """)
    conn.execute("""
        ALTER TABLE provider_last_changed
        ADD COLUMN IF NOT EXISTS retired_ipv4_ip_count INTEGER DEFAULT 0
    """)
    conn.execute("""
        ALTER TABLE provider_last_changed
        ADD COLUMN IF NOT EXISTS retired_ipv6_64_count BIGINT DEFAULT 0
    """)
    # Ensure NULL values are set to 0 for existing rows
    conn.execute("""
        UPDATE provider_last_changed
        SET ipv4_ip_count = 0 WHERE ipv4_ip_count IS NULL
    """)
    conn.execute("""
        UPDATE provider_last_changed
        SET ipv6_64_count = 0 WHERE ipv6_64_count IS NULL
    """)
    conn.execute("""
        UPDATE provider_last_changed
        SET retired_ipv4_ip_count = 0 WHERE retired_ipv4_ip_count IS NULL
    """)
    conn.execute("""
        UPDATE provider_last_changed
        SET retired_ipv6_64_count = 0 WHERE retired_ipv6_64_count IS NULL
    """)

    # Drop old column name if exists (from intermediate development versions)
    try:
        conn.execute("""
            ALTER TABLE provider_last_changed
            DROP COLUMN IF EXISTS retired_ipv6_ip_count
        """)
    except Exception:
        pass  # Column may not exist, that's fine

    return conn


def _hash(cidrs: list[str]) -> str:
    return hashlib.sha256(",".join(sorted(cidrs)).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Bulk history reconciliation (all providers in one transaction)
# ---------------------------------------------------------------------------


def _write_current_cidrs_csv(providers: list[dict]) -> str | None:
    """
    Write all (provider_id, cidr) pairs to a temp CSV file.
    Returns the file path, or None if there are no rows.
    DuckDB's native CSV reader is orders of magnitude faster than executemany
    or unnest parameter binding for large datasets.
    """
    rows_exist = any(p.get("ipv4") or p.get("ipv6") for p in providers)
    if not rows_exist:
        return None

    fd, path = tempfile.mkstemp(suffix=".csv", prefix="cidr_history_")
    with os.fdopen(fd, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["provider_id", "cidr"])
        for p in providers:
            pid = p["provider_id"]
            for cidr in p.get("ipv4", []):
                if isinstance(cidr, str):
                    writer.writerow([pid, cidr])
            for cidr in p.get("ipv6", []):
                if isinstance(cidr, str):
                    writer.writerow([pid, cidr])
    return path


def reconcile_all_providers(
    conn: duckdb.DuckDBPyConnection,
    providers: list[dict],  # list of {provider_id, ipv4, ipv6}
    now: datetime,
) -> dict[str, tuple[list[tuple[str, datetime]], list[tuple[str, datetime]]]]:
    """
    Reconcile all providers against cidr_history in a single transaction.
    Returns {provider_id: (retired_v4, retired_v6)}.
    """
    cutoff = now - timedelta(weeks=RETIREMENT_WEEKS)

    # Write all current CIDRs to a temp CSV then bulk-load via DuckDB's native reader.
    # This is orders of magnitude faster than executemany or unnest parameter binding
    # for large datasets (547K rows loads in ~1s vs 90s with Python-side serialization).
    tmp_csv = _write_current_cidrs_csv(providers)

    conn.execute("BEGIN")

    # Load current state into a temp table using DuckDB's fast CSV reader
    conn.execute("DROP TABLE IF EXISTS current_cidrs")
    if tmp_csv:
        conn.execute(
            f"CREATE TEMP TABLE current_cidrs AS SELECT * FROM read_csv('{tmp_csv}', "
            f"columns={{'provider_id': 'VARCHAR', 'cidr': 'VARCHAR'}})"
        )
        os.unlink(tmp_csv)
    else:
        conn.execute(
            "CREATE TEMP TABLE current_cidrs (provider_id VARCHAR NOT NULL, cidr VARCHAR NOT NULL)"
        )

    # 1. Insert truly new CIDRs (not seen before at all)
    conn.execute(f"""
        INSERT INTO cidr_history (provider_id, cidr, first_seen, last_seen, retired_at)
        SELECT c.provider_id, c.cidr, '{now.isoformat()}', '{now.isoformat()}', NULL
        FROM current_cidrs c
        LEFT JOIN cidr_history h ON h.provider_id = c.provider_id AND h.cidr = c.cidr
        WHERE h.cidr IS NULL
    """)

    # 2. Re-activate previously retired CIDRs that are back
    conn.execute(f"""
        UPDATE cidr_history SET last_seen = '{now.isoformat()}', retired_at = NULL
        WHERE retired_at IS NOT NULL
        AND (provider_id, cidr) IN (SELECT provider_id, cidr FROM current_cidrs)
    """)

    # 3. Update last_seen for continuing active CIDRs
    conn.execute(f"""
        UPDATE cidr_history SET last_seen = '{now.isoformat()}'
        WHERE retired_at IS NULL
        AND (provider_id, cidr) IN (SELECT provider_id, cidr FROM current_cidrs)
    """)

    # 4. Mark removed CIDRs as retired
    conn.execute(f"""
        UPDATE cidr_history SET retired_at = '{now.isoformat()}'
        WHERE retired_at IS NULL
        AND (provider_id, cidr) NOT IN (SELECT provider_id, cidr FROM current_cidrs)
    """)

    # 5. Purge CIDRs beyond the retention window
    conn.execute(f"""
        DELETE FROM cidr_history
        WHERE retired_at IS NOT NULL AND retired_at < '{cutoff.isoformat()}'
    """)

    conn.execute("COMMIT")

    # Fetch all still-valid retired CIDRs grouped by provider
    retired_rows = conn.execute("""
        SELECT provider_id, cidr, retired_at
        FROM cidr_history
        WHERE retired_at IS NOT NULL
        ORDER BY provider_id
    """).fetchall()

    result: dict[str, tuple[list, list]] = {}
    for pid, cidr, retired_at in retired_rows:
        if pid not in result:
            result[pid] = ([], [])
        if ":" in cidr:
            result[pid][1].append((cidr, retired_at))
        else:
            result[pid][0].append((cidr, retired_at))

    return result


# ---------------------------------------------------------------------------
# Provider metadata tracking
# ---------------------------------------------------------------------------


def update_all_provider_metadata(
    conn: duckdb.DuckDBPyConnection,
    providers: list[dict],
    retired_by_provider: dict,
    now: datetime,
) -> None:
    """Update provider_last_changed for all providers in one transaction."""
    conn.execute("BEGIN")

    for p in providers:
        pid = p["provider_id"]
        pname = p.get("provider", pid)
        v4 = p.get("ipv4", [])
        v6 = p.get("ipv6", [])
        method = p.get("method")
        raw_src = p.get("source", "")
        if isinstance(raw_src, list):
            source = raw_src[0] if raw_src else ""
        else:
            source = raw_src or ""

        new_v4_hash = _hash(v4)
        new_v6_hash = _hash(v6)
        retired = retired_by_provider.get(pid, ([], []))
        rv4, rv6 = len(retired[0]), len(retired[1])

        # Calculate IPv4 IP counts and IPv6 /64 counts
        ipv4_ip_count = count_ipv4_addresses(v4)
        ipv6_64_count = count_ipv6_64_subnets(v6)
        retired_ipv4_ip_count = count_ipv4_addresses([cidr for cidr, _ in retired[0]])
        retired_ipv6_64_count = count_ipv6_64_subnets([cidr for cidr, _ in retired[1]])

        row = conn.execute(
            "SELECT last_changed_at, ipv4_hash, ipv6_hash FROM provider_last_changed WHERE provider_id = ?",
            [pid],
        ).fetchone()

        if row:
            last_changed_at = row[0]
            if new_v4_hash != row[1] or new_v6_hash != row[2]:
                last_changed_at = now
            conn.execute(
                """
                UPDATE provider_last_changed SET
                    provider_name=?, last_changed_at=?, last_crawled_at=?,
                    ipv4_count=?, ipv6_count=?,
                    retired_ipv4_count=?, retired_ipv6_count=?,
                    ipv4_ip_count=?, ipv6_64_count=?,
                    retired_ipv4_ip_count=?, retired_ipv6_64_count=?,
                    method=?, source=?, ipv4_hash=?, ipv6_hash=?
                WHERE provider_id=?
                """,
                [
                    pname,
                    last_changed_at,
                    now,
                    len(v4),
                    len(v6),
                    rv4,
                    rv6,
                    ipv4_ip_count,
                    ipv6_64_count,
                    retired_ipv4_ip_count,
                    retired_ipv6_64_count,
                    method,
                    source,
                    new_v4_hash,
                    new_v6_hash,
                    pid,
                ],
            )
        else:
            conn.execute(
                """
                INSERT INTO provider_last_changed
                    (provider_id, provider_name, last_changed_at, last_crawled_at,
                     ipv4_count, ipv6_count, retired_ipv4_count, retired_ipv6_count,
                     ipv4_ip_count, ipv6_64_count, retired_ipv4_ip_count, retired_ipv6_64_count,
                     method, source, ipv4_hash, ipv6_hash)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                [
                    pid,
                    pname,
                    now,
                    now,
                    len(v4),
                    len(v6),
                    rv4,
                    rv6,
                    ipv4_ip_count,
                    ipv6_64_count,
                    retired_ipv4_ip_count,
                    retired_ipv6_64_count,
                    method,
                    source,
                    new_v4_hash,
                    new_v6_hash,
                ],
            )

    conn.execute("COMMIT")


# ---------------------------------------------------------------------------
# Output file patching
# ---------------------------------------------------------------------------


def patch_json(
    json_path: Path,
    retired_v4: list[tuple[str, datetime]],
    retired_v6: list[tuple[str, datetime]],
) -> None:
    with open(json_path) as f:
        data = json.load(f)

    active_v4 = set(data.get("ipv4", []))
    active_v6 = set(data.get("ipv6", []))

    det_v4: dict[str, dict] = {d["address"]: d for d in data.get("details_ipv4", [])}
    det_v6: dict[str, dict] = {d["address"]: d for d in data.get("details_ipv6", [])}

    changed = False
    for cidr, retired_at in retired_v4:
        if cidr not in active_v4:
            data.setdefault("ipv4", []).append(cidr)
            det_v4[cidr] = {"address": cidr, "retired_at": retired_at.isoformat()}
            changed = True

    for cidr, retired_at in retired_v6:
        if cidr not in active_v6:
            data.setdefault("ipv6", []).append(cidr)
            det_v6[cidr] = {"address": cidr, "retired_at": retired_at.isoformat()}
            changed = True

    if changed:
        if det_v4:
            data["details_ipv4"] = list(det_v4.values())
        if det_v6:
            data["details_ipv6"] = list(det_v6.values())
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")


def patch_csv(
    csv_path: Path,
    retired_v4: list[tuple[str, datetime]],
    retired_v6: list[tuple[str, datetime]],
) -> None:
    if not csv_path.exists():
        return

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or ["Type", "Address"]
        rows = list(reader)

    existing = {r["Address"] for r in rows}

    # Ensure RetiredAt column exists
    has_retired_col = "RetiredAt" in fieldnames
    if not has_retired_col:
        fieldnames = list(fieldnames) + ["RetiredAt"]

    new_rows = []
    for cidr, retired_at in retired_v4:
        if cidr not in existing:
            row = {"Type": "IPv4", "Address": cidr, "RetiredAt": retired_at.isoformat()}
            # Copy other fields from first row template if available
            if rows:
                for key in fieldnames:
                    if key not in row:
                        row[key] = rows[0].get(key, "")
            new_rows.append(row)
    for cidr, retired_at in retired_v6:
        if cidr not in existing:
            row = {"Type": "IPv6", "Address": cidr, "RetiredAt": retired_at.isoformat()}
            if rows:
                for key in fieldnames:
                    if key not in row:
                        row[key] = rows[0].get(key, "")
            new_rows.append(row)

    if not new_rows and has_retired_col:
        return

    updated = [{**r, "RetiredAt": r.get("RetiredAt", "")} for r in rows] + new_rows

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)


def patch_txt(
    txt_path: Path,
    retired_v4: list[tuple[str, datetime]],
    retired_v6: list[tuple[str, datetime]],
) -> None:
    if not txt_path.exists():
        return

    with open(txt_path) as f:
        existing = {
            line.strip() for line in f if line.strip() and not line.startswith("#")
        }

    to_add = [cidr for cidr, _ in retired_v4 + retired_v6 if cidr not in existing]
    if to_add:
        with open(txt_path, "a") as f:
            f.write("\n".join(to_add) + "\n")


# ---------------------------------------------------------------------------
# all-providers.* patching
# ---------------------------------------------------------------------------


def patch_all_providers(
    json_dir: Path,
    all_retired: dict[str, list[tuple[str, datetime]]],
) -> None:
    json_path = json_dir / "all-providers.json"
    csv_path = json_dir.parent / "csv" / "all-providers.csv"
    txt_path = json_dir.parent / "txt" / "all-providers.txt"

    # Flatten: cidr -> (earliest retired_at, [provider_ids])
    retired_map: dict[str, tuple[datetime, list[str]]] = {}
    for provider_id, entries in all_retired.items():
        for cidr, retired_at in entries:
            if cidr not in retired_map:
                retired_map[cidr] = (retired_at, [provider_id])
            else:
                existing_at, providers = retired_map[cidr]
                providers.append(provider_id)
                if retired_at < existing_at:
                    retired_map[cidr] = (retired_at, providers)

    if not retired_map:
        return

    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)

        active_set = set(data.get("ipv4", [])) | set(data.get("ipv6", []))
        ip_providers: dict = data.get("ip_providers", {})

        new_v4, new_v6 = [], []
        for cidr, (retired_at, providers) in retired_map.items():
            if cidr in active_set:
                continue
            (new_v6 if ":" in cidr else new_v4).append(cidr)
            ip_providers[cidr] = providers

        if new_v4 or new_v6:
            data["ipv4"] = data.get("ipv4", []) + new_v4
            data["ipv6"] = data.get("ipv6", []) + new_v6
            data["ip_providers"] = ip_providers
            data["retired_ipv4_count"] = len(new_v4) + data.get("retired_ipv4_count", 0)
            data["retired_ipv6_count"] = len(new_v6) + data.get("retired_ipv6_count", 0)
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")

    if csv_path.exists():
        rv4 = [(c, r) for c, (r, _) in retired_map.items() if ":" not in c]
        rv6 = [(c, r) for c, (r, _) in retired_map.items() if ":" in c]
        patch_csv(csv_path, rv4, rv6)

    if txt_path.exists():
        rv4 = [(c, r) for c, (r, _) in retired_map.items() if ":" not in c]
        rv6 = [(c, r) for c, (r, _) in retired_map.items() if ":" in c]
        patch_txt(txt_path, rv4, rv6)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="meta/history.duckdb")
    parser.add_argument("--json-dir", default="json")
    parser.add_argument("--misc-dir", default="misc")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(tz=timezone.utc)
    json_dir = Path(args.json_dir)
    misc_dir = Path(args.misc_dir)

    conn = open_db(db_path)

    # Load all provider data from disk
    providers: list[dict] = []
    provider_paths: dict[str, tuple[Path, Path, Path]] = {}  # pid -> (json, csv, txt)

    for search_dir in [json_dir, misc_dir]:
        if not search_dir.exists():
            continue
        for json_path in sorted(search_dir.glob("*.json")):
            if json_path.stem == "all-providers" or json_path.stem.endswith("-details"):
                continue
            with open(json_path) as f:
                data = json.load(f)
            providers.append(data)

            pid = data.get("provider_id", json_path.stem)
            if search_dir == json_dir:
                csv_path = json_dir.parent / "csv" / json_path.with_suffix(".csv").name
                txt_path = json_dir.parent / "txt" / json_path.with_suffix(".txt").name
            else:
                csv_path = search_dir / json_path.with_suffix(".csv").name
                txt_path = search_dir / json_path.with_suffix(".txt").name
            provider_paths[pid] = (json_path, csv_path, txt_path)

    total_cidrs = sum(
        len(p.get("ipv4", [])) + len(p.get("ipv6", [])) for p in providers
    )
    print(
        f"Processing {len(providers)} providers, {total_cidrs:,} total CIDRs...",
        flush=True,
    )

    # Single-transaction bulk reconciliation
    retired_by_provider = reconcile_all_providers(conn, providers, now)

    # Update provider metadata
    update_all_provider_metadata(conn, providers, retired_by_provider, now)

    conn.close()
    print(f"DB updated: {db_path}", flush=True)

    # Patch output files for providers with retired IPs
    all_retired_flat: dict[str, list[tuple[str, datetime]]] = {}
    for pid, (rv4, rv6) in retired_by_provider.items():
        if not rv4 and not rv6:
            continue
        json_path, csv_path, txt_path = provider_paths[pid]
        patch_json(json_path, rv4, rv6)
        patch_csv(csv_path, rv4, rv6)
        patch_txt(txt_path, rv4, rv6)
        all_retired_flat[pid] = rv4 + rv6
        print(f"  {pid}: {len(rv4)} retired IPv4, {len(rv6)} retired IPv6", flush=True)

    if all_retired_flat and json_dir.exists():
        patch_all_providers(json_dir, all_retired_flat)

    print("Done.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
