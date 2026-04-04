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
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import duckdb

RETIREMENT_WEEKS = 4
RIPESTAT_ASN_RE = re.compile(r"resource=(AS\d+)", re.IGNORECASE)


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
            method            VARCHAR,
            source            VARCHAR,
            ipv4_hash         VARCHAR,
            ipv6_hash         VARCHAR
        )
    """)
    return conn


def _hash(cidrs: list[str]) -> str:
    return hashlib.sha256(",".join(sorted(cidrs)).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Per-provider history logic
# ---------------------------------------------------------------------------

def process_history(
    conn: duckdb.DuckDBPyConnection,
    provider_id: str,
    current_ipv4: list[str],
    current_ipv6: list[str],
    now: datetime,
) -> tuple[list[tuple[str, datetime]], list[tuple[str, datetime]]]:
    """
    Reconcile current CIDRs against DB state.
    Returns (retired_ipv4, retired_ipv6) — lists of (cidr, retired_at) tuples
    that are still within the retention window and should appear in output.
    """
    cutoff = now - timedelta(weeks=RETIREMENT_WEEKS)
    current = set(current_ipv4) | set(current_ipv6)

    rows = conn.execute(
        "SELECT cidr FROM cidr_history WHERE provider_id = ? AND retired_at IS NULL",
        [provider_id],
    ).fetchall()
    active_in_db = {r[0] for r in rows}

    new_cidrs = current - active_in_db
    removed_cidrs = active_in_db - current
    continuing_cidrs = current & active_in_db

    # Batch insert new CIDRs
    if new_cidrs:
        conn.executemany(
            """
            INSERT INTO cidr_history (provider_id, cidr, first_seen, last_seen, retired_at)
            VALUES (?, ?, ?, ?, NULL)
            ON CONFLICT (provider_id, cidr) DO UPDATE SET last_seen = excluded.last_seen, retired_at = NULL
            """,
            [[provider_id, cidr, now, now] for cidr in new_cidrs],
        )

    # Batch update last_seen for continuing CIDRs using a temp VALUES table
    if continuing_cidrs:
        conn.execute(
            f"""
            UPDATE cidr_history SET last_seen = ?
            WHERE provider_id = ?
            AND cidr IN (SELECT unnest(?::VARCHAR[]))
            """,
            [now, provider_id, list(continuing_cidrs)],
        )

    # Batch mark removed CIDRs as retired
    if removed_cidrs:
        conn.execute(
            f"""
            UPDATE cidr_history SET retired_at = ?
            WHERE provider_id = ?
            AND cidr IN (SELECT unnest(?::VARCHAR[]))
            AND retired_at IS NULL
            """,
            [now, provider_id, list(removed_cidrs)],
        )

    # Purge CIDRs that exceeded the retention window
    conn.execute(
        "DELETE FROM cidr_history WHERE provider_id = ? AND retired_at IS NOT NULL AND retired_at < ?",
        [provider_id, cutoff],
    )

    # Fetch still-valid retired CIDRs
    retired_rows = conn.execute(
        "SELECT cidr, retired_at FROM cidr_history WHERE provider_id = ? AND retired_at IS NOT NULL",
        [provider_id],
    ).fetchall()

    retired_v4 = [(c, r) for c, r in retired_rows if ":" not in c]
    retired_v6 = [(c, r) for c, r in retired_rows if ":" in c]
    return retired_v4, retired_v6


def update_provider_metadata(
    conn: duckdb.DuckDBPyConnection,
    provider_id: str,
    provider_name: str,
    now: datetime,
    current_ipv4: list[str],
    current_ipv6: list[str],
    retired_v4: list,
    retired_v6: list,
    method: str | None,
    source: str | None,
) -> None:
    new_v4_hash = _hash(current_ipv4)
    new_v6_hash = _hash(current_ipv6)

    row = conn.execute(
        "SELECT last_changed_at, ipv4_hash, ipv6_hash FROM provider_last_changed WHERE provider_id = ?",
        [provider_id],
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
                method=?, source=?, ipv4_hash=?, ipv6_hash=?
            WHERE provider_id=?
            """,
            [
                provider_name, last_changed_at, now,
                len(current_ipv4), len(current_ipv6),
                len(retired_v4), len(retired_v6),
                method, source, new_v4_hash, new_v6_hash,
                provider_id,
            ],
        )
    else:
        conn.execute(
            """
            INSERT INTO provider_last_changed
                (provider_id, provider_name, last_changed_at, last_crawled_at,
                 ipv4_count, ipv6_count, retired_ipv4_count, retired_ipv6_count,
                 method, source, ipv4_hash, ipv6_hash)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            [
                provider_id, provider_name, now, now,
                len(current_ipv4), len(current_ipv6),
                len(retired_v4), len(retired_v6),
                method, source, new_v4_hash, new_v6_hash,
            ],
        )


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

    # Build details maps (address → detail dict)
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
        rows = list(reader)

    existing = {r["Address"] for r in rows}

    new_rows = []
    for cidr, retired_at in retired_v4:
        if cidr not in existing:
            new_rows.append({"Type": "IPv4", "Address": cidr, "RetiredAt": retired_at.isoformat()})
    for cidr, retired_at in retired_v6:
        if cidr not in existing:
            new_rows.append({"Type": "IPv6", "Address": cidr, "RetiredAt": retired_at.isoformat()})

    # Migrate existing rows to include RetiredAt column (empty for active)
    has_retired_col = rows and "RetiredAt" in rows[0]
    if not new_rows and has_retired_col:
        return

    updated = [{**r, "RetiredAt": r.get("RetiredAt", "")} for r in rows] + new_rows

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Type", "Address", "RetiredAt"])
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
        existing = {line.strip() for line in f if line.strip() and not line.startswith("#")}

    to_add = [cidr for cidr, _ in retired_v4 + retired_v6 if cidr not in existing]
    if to_add:
        with open(txt_path, "a") as f:
            f.write("\n".join(to_add) + "\n")


# ---------------------------------------------------------------------------
# all-providers.json/csv/txt patching
# ---------------------------------------------------------------------------

def patch_all_providers(
    json_dir: Path,
    all_retired: dict[str, list[tuple[str, datetime]]],  # provider_id -> [(cidr, retired_at)]
) -> None:
    """Inject retired CIDRs from all providers into the all-providers.* files."""
    json_path = json_dir / "all-providers.json"
    csv_path = json_dir.parent / "csv" / "all-providers.csv"
    txt_path = json_dir.parent / "txt" / "all-providers.txt"

    # Flatten: cidr -> (retired_at, [provider_ids])
    retired_map: dict[str, tuple[datetime, list[str]]] = {}
    for provider_id, entries in all_retired.items():
        for cidr, retired_at in entries:
            if cidr not in retired_map:
                retired_map[cidr] = (retired_at, [provider_id])
            else:
                existing_at, providers = retired_map[cidr]
                providers.append(provider_id)
                # Keep earliest retirement date
                if retired_at < existing_at:
                    retired_map[cidr] = (retired_at, providers)

    if not retired_map:
        return

    # Patch JSON
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)

        active_set = set(data.get("ipv4", [])) | set(data.get("ipv6", []))
        ip_providers: dict = data.get("ip_providers", {})

        retired_v4_new = []
        retired_v6_new = []
        for cidr, (retired_at, providers) in retired_map.items():
            if cidr in active_set:
                continue
            if ":" in cidr:
                retired_v6_new.append(cidr)
            else:
                retired_v4_new.append(cidr)
            ip_providers[cidr] = providers

        if retired_v4_new or retired_v6_new:
            data["ipv4"] = data.get("ipv4", []) + retired_v4_new
            data["ipv6"] = data.get("ipv6", []) + retired_v6_new
            data["ip_providers"] = ip_providers
            # Track how many retired IPs are present
            data["retired_ipv4_count"] = len(retired_v4_new) + data.get("retired_ipv4_count", 0)
            data["retired_ipv6_count"] = len(retired_v6_new) + data.get("retired_ipv6_count", 0)
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")

    # Patch CSV
    if csv_path.exists():
        retired_v4 = [(c, r) for c, (r, _) in retired_map.items() if ":" not in c]
        retired_v6 = [(c, r) for c, (r, _) in retired_map.items() if ":" in c]
        patch_csv(csv_path, retired_v4, retired_v6)

    # Patch TXT
    if txt_path.exists():
        retired_v4 = [(c, r) for c, (r, _) in retired_map.items() if ":" not in c]
        retired_v6 = [(c, r) for c, (r, _) in retired_map.items() if ":" in c]
        patch_txt(txt_path, retired_v4, retired_v6)


# ---------------------------------------------------------------------------
# Source display helpers
# ---------------------------------------------------------------------------

def format_source(sources: list[str]) -> str:
    """Return a compact source string suitable for DB storage."""
    if not sources:
        return ""
    return sources[0]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="meta/history.duckdb", help="Path to DuckDB file")
    parser.add_argument(
        "--json-dir", default="json", help="Directory containing provider JSON files"
    )
    parser.add_argument(
        "--misc-dir", default="misc", help="Directory containing misc provider JSON files"
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(tz=timezone.utc)

    conn = open_db(db_path)

    dirs_to_process = []
    json_dir = Path(args.json_dir)
    misc_dir = Path(args.misc_dir)
    if json_dir.exists():
        dirs_to_process.append(json_dir)
    if misc_dir.exists():
        dirs_to_process.append(misc_dir)

    # Map: provider_id -> (retired_v4, retired_v6) for all-providers update
    all_retired: dict[str, list[tuple[str, datetime]]] = {}

    for search_dir in dirs_to_process:
        for json_path in sorted(search_dir.glob("*.json")):
            if json_path.stem == "all-providers":
                continue

            with open(json_path) as f:
                data = json.load(f)

            provider_id = data.get("provider_id", json_path.stem)
            provider_name = data.get("provider", provider_id)
            method = data.get("method")
            sources = data.get("source", [])
            current_v4 = data.get("ipv4", [])
            current_v6 = data.get("ipv6", [])

            retired_v4, retired_v6 = process_history(
                conn, provider_id, current_v4, current_v6, now
            )
            update_provider_metadata(
                conn, provider_id, provider_name, now,
                current_v4, current_v6, retired_v4, retired_v6,
                method, format_source(sources),
            )

            if retired_v4 or retired_v6:
                all_retired[provider_id] = retired_v4 + retired_v6
                patch_json(json_path, retired_v4, retired_v6)

            # Determine sibling CSV/TXT paths
            if search_dir == json_dir:
                csv_path = json_dir.parent / "csv" / json_path.with_suffix(".csv").name
                txt_path = json_dir.parent / "txt" / json_path.with_suffix(".txt").name
            else:
                csv_path = search_dir / json_path.with_suffix(".csv").name
                txt_path = search_dir / json_path.with_suffix(".txt").name

            if retired_v4 or retired_v6:
                patch_csv(csv_path, retired_v4, retired_v6)
                patch_txt(txt_path, retired_v4, retired_v6)

            total_retired = len(retired_v4) + len(retired_v6)
            print(
                f"  {provider_id}: {len(current_v4)} IPv4, {len(current_v6)} IPv6"
                + (f", {total_retired} retired" if total_retired else ""),
                flush=True,
            )

    # Update all-providers aggregated files
    if all_retired and json_dir.exists():
        patch_all_providers(json_dir, all_retired)

    conn.close()
    print(f"History updated: {db_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
