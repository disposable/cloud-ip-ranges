#!/usr/bin/env python3
"""
Generate and update README.md statistics from DuckDB history and provider JSON files.

Updates two sections between HTML comment markers:
  <!-- STATS_START --> ... <!-- STATS_END -->
  <!-- SOURCES_TABLE_START --> ... <!-- SOURCES_TABLE_END -->
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import duckdb

RIPESTAT_ASN_RE = re.compile(r"resource=(AS\d+)", re.IGNORECASE)

STATS_START = "<!-- STATS_START -->"
STATS_END = "<!-- STATS_END -->"
SOURCES_START = "<!-- SOURCES_TABLE_START -->"
SOURCES_END = "<!-- SOURCES_TABLE_END -->"


# ---------------------------------------------------------------------------
# Source / method display helpers
# ---------------------------------------------------------------------------

METHOD_LABELS = {
    "bgp_announced": None,  # further refined below
    "published_list": "Published List",
    "rdap_registry": "RDAP/ARIN Registry",
}


def method_label(method: str | None, sources: list[str]) -> str:
    if method == "bgp_announced":
        if any(s.startswith("RADB::") for s in sources):
            return "RADB AS-SET"
        return "ASN Prefix"
    return METHOD_LABELS.get(method or "", method or "")


def source_display(sources: list[str]) -> str:
    """
    Return a compact, human-readable source string for the README table.

    - RIPEStat URLs are collapsed to their ASN identifier (e.g. AS55293).
    - RADB AS-SET identifiers are kept as-is.
    - Regular URLs are rendered as markdown links with a shortened label.
    """
    parts: list[str] = []
    seen: set[str] = set()

    for s in sources:
        m = RIPESTAT_ASN_RE.search(s)
        if m:
            key = m.group(1)
            if key not in seen:
                parts.append(key)
                seen.add(key)
        elif s.startswith("RADB::"):
            if s not in seen:
                parts.append(s)
                seen.add(s)
        else:
            # Regular URL — render as a markdown link with a short label
            label = _url_label(s)
            link = f"[{label}]({s})"
            if link not in seen:
                parts.append(link)
                seen.add(link)

    return "<br>".join(parts)


def _url_label(url: str) -> str:
    """Return a short human-readable label for a URL."""
    url = re.sub(r"^https?://", "", url)
    # Strip common long path components
    url = re.sub(r"\?.*", "", url)  # query string
    url = re.sub(r"#.*", "", url)  # fragment
    url = url.rstrip("/")
    # Keep last 2 path segments at most
    parts = url.split("/")
    if len(parts) > 3:
        url = parts[0] + "/…/" + "/".join(parts[-1:])
    return url


# ---------------------------------------------------------------------------
# Stats generation
# ---------------------------------------------------------------------------


def generate_stats_block(conn: duckdb.DuckDBPyConnection, misc_dir: Path) -> str:
    rows = conn.execute("""
        SELECT
            provider_id,
            ipv4_count,
            ipv6_count,
            ipv4_ip_count,
            ipv6_64_count,
            retired_ipv4_count,
            retired_ipv6_count,
            retired_ipv4_ip_count,
            retired_ipv6_64_count,
            last_crawled_at
        FROM provider_last_changed
    """).fetchall()

    if not rows:
        return "_No statistics available yet — run after the first crawl._\n"

    total_providers = len(rows)
    total_v4 = total_v6 = total_v4_ips = total_v6_64s = 0
    retired_v4 = retired_v6 = retired_v4_ips = retired_v6_64s = 0
    cloud_providers = misc_providers = 0
    cloud_v4 = cloud_v6 = cloud_v4_ips = cloud_v6_64s = 0
    misc_v4 = misc_v6 = misc_v4_ips = misc_v6_64s = 0
    cloud_retired_v4 = cloud_retired_v6 = cloud_retired_v4_ips = cloud_retired_v6_64s = 0
    misc_retired_v4 = misc_retired_v6 = misc_retired_v4_ips = misc_retired_v6_64s = 0
    last_crawled = None

    for row in rows:
        (
            pid,
            v4,
            v6,
            v4_ips,
            v6_64s,
            rv4,
            rv6,
            rv4_ips,
            rv6_64s,
            lc,
        ) = row
        v4 = v4 or 0
        v6 = v6 or 0
        v4_ips = v4_ips or 0
        v6_64s = v6_64s or 0
        rv4 = rv4 or 0
        rv6 = rv6 or 0
        rv4_ips = rv4_ips or 0
        rv6_64s = rv6_64s or 0

        total_v4 += v4
        total_v6 += v6
        total_v4_ips += v4_ips
        total_v6_64s += v6_64s
        retired_v4 += rv4
        retired_v6 += rv6
        retired_v4_ips += rv4_ips
        retired_v6_64s += rv6_64s

        if lc and (last_crawled is None or lc > last_crawled):
            last_crawled = lc

        if (misc_dir / f"{pid}.json").exists():
            misc_providers += 1
            misc_v4 += v4
            misc_v6 += v6
            misc_v4_ips += v4_ips
            misc_v6_64s += v6_64s
            misc_retired_v4 += rv4
            misc_retired_v6 += rv6
            misc_retired_v4_ips += rv4_ips
            misc_retired_v6_64s += rv6_64s
        else:
            cloud_providers += 1
            cloud_v4 += v4
            cloud_v6 += v6
            cloud_v4_ips += v4_ips
            cloud_v6_64s += v6_64s
            cloud_retired_v4 += rv4
            cloud_retired_v6 += rv6
            cloud_retired_v4_ips += rv4_ips
            cloud_retired_v6_64s += rv6_64s

    last_crawled_str = (
        last_crawled.strftime("%Y-%m-%d %H:%M UTC") if last_crawled else "—"
    )

    lines = [
        "| Metric | Value |",
        "|--------|------:|",
        f"| Providers tracked | **{total_providers}** ({cloud_providers} cloud + {misc_providers} misc) |",
        f"| Active IPv4 addresses | **{total_v4_ips:,}** ({total_v4:,} subnets) |",
        f"| Active IPv6 /64 subnets | **{total_v6_64s:,}** ({total_v6:,} ranges) |",
        f"| Retired IPv4 (≤ 4 weeks) | {retired_v4_ips:,} addresses ({retired_v4:,} subnets) |",
        f"| Retired IPv6 (≤ 4 weeks) | {retired_v6_64s:,} /64s ({retired_v6:,} ranges) |",
        f"| Last crawled | {last_crawled_str} |",
    ]
    return "\n".join(lines) + "\n"


def _provider_table_row(
    pid: str,
    info: dict,
    provider_sources: dict[str, list[str]],
    misc_dir: Path,
) -> str:
    pname = info["provider_name"]
    changed_at = info["last_changed_at"]
    v4 = info["ipv4_count"]
    v6 = info["ipv6_count"]
    v4_ips = info["ipv4_ip_count"]
    v6_64s = info["ipv6_64_count"]
    rv4 = info["retired_ipv4"]
    rv6 = info["retired_ipv6"]
    rv4_ips = info["retired_ipv4_ips"]
    rv6_64s = info["retired_ipv6_64s"]
    method = info["method"]
    sources = provider_sources.get(pid, [info["source"]] if info["source"] else [])

    # Determine file locations (misc vs main)
    if (misc_dir / f"{pid}.json").exists():
        folder = "misc"
        csv_folder = "misc"
        txt_folder = "misc"
    else:
        folder = "json"
        csv_folder = "csv"
        txt_folder = "txt"

    json_link = f"[JSON]({folder}/{pid}.json)"
    txt_link = f"[TXT]({txt_folder}/{pid}.txt)"
    csv_link = f"[CSV]({csv_folder}/{pid}.csv)"

    changed_str = changed_at.strftime("%Y-%m-%d") if changed_at else "—"

    v4_str = (
        f"{v4_ips:,}"
        + (f" ({v4:,} subnets)" if v4 else "")
        + (f"<br>+{rv4_ips:,} retired" if rv4 else "")
    )
    v6_str = (
        f"{v6_64s:,}"
        + (f" ({v6:,} ranges)" if v6 else "")
        + (f"<br>+{rv6_64s:,} retired" if rv6 else "")
    )

    src_str = source_display(sources)
    method_str = method_label(method, sources)

    return f"| {pname} | {src_str} | {method_str} | {v4_str} | {v6_str} | {changed_str} | {json_link} | {txt_link} | {csv_link} |"


def generate_sources_table(
    conn: duckdb.DuckDBPyConnection,
    json_dir: Path,
    misc_dir: Path,
) -> str:
    rows_by_id: dict[str, dict] = {}

    # Load metadata from DuckDB
    db_rows = conn.execute("""
        SELECT provider_id, provider_name, last_changed_at,
               ipv4_count, ipv6_count, retired_ipv4_count, retired_ipv6_count,
               ipv4_ip_count, ipv6_64_count, retired_ipv4_ip_count, retired_ipv6_64_count,
               method, source
        FROM provider_last_changed
        ORDER BY provider_name COLLATE NOCASE
    """).fetchall()

    for (
        pid,
        pname,
        changed_at,
        v4,
        v6,
        rv4,
        rv6,
        v4_ips,
        v6_64s,
        rv4_ips,
        rv6_64s,
        method,
        source,
    ) in db_rows:
        rows_by_id[pid] = {
            "provider_name": pname,
            "last_changed_at": changed_at,
            "ipv4_count": v4 or 0,
            "ipv6_count": v6 or 0,
            "ipv4_ip_count": v4_ips or 0,
            "ipv6_64_count": v6_64s or 0,
            "retired_ipv4": rv4 or 0,
            "retired_ipv6": rv6 or 0,
            "retired_ipv4_ips": rv4_ips or 0,
            "retired_ipv6_64s": rv6_64s or 0,
            "method": method,
            "source": source,
        }

    # Enrich with full source list (for display) from JSON files
    provider_sources: dict[str, list[str]] = {}
    for search_dir in [json_dir, misc_dir]:
        if not search_dir.exists():
            continue
        for json_path in sorted(search_dir.glob("*.json")):
            if json_path.stem == "all-providers":
                continue
            try:
                with open(json_path) as f:
                    data = json.load(f)
                pid = data.get("provider_id", json_path.stem)
                src = data.get("source", [])
                # Normalize: some providers store source as a bare string
                provider_sources[pid] = [src] if isinstance(src, str) else src
            except Exception:
                pass

    # Split providers into cloud and misc
    normal_pids = [pid for pid in rows_by_id if not (misc_dir / f"{pid}.json").exists()]
    misc_pids = [pid for pid in rows_by_id if (misc_dir / f"{pid}.json").exists()]

    header = "| Provider | Source | Method | IPv4 IPs | IPv6 /64s | Last Changed | JSON | TXT | CSV |"
    separator = "|----------|--------|--------|---------:|----------:|--------------|------|-----|-----|"

    parts: list[str] = []

    if normal_pids:
        parts.append("### Cloud Providers")
        parts.append("")
        parts.append(header)
        parts.append(separator)
        for pid in normal_pids:
            parts.append(_provider_table_row(pid, rows_by_id[pid], provider_sources, misc_dir))
        parts.append("")

    if misc_pids:
        parts.append("### Misc Providers (ISP Traffic)")
        parts.append("")
        parts.append(header)
        parts.append(separator)
        for pid in misc_pids:
            parts.append(_provider_table_row(pid, rows_by_id[pid], provider_sources, misc_dir))
        parts.append("")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# README patching
# ---------------------------------------------------------------------------


def replace_section(
    content: str, start_marker: str, end_marker: str, new_body: str
) -> str:
    """Replace everything between start_marker and end_marker (inclusive) with new content."""
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{start_marker}\n{new_body}{end_marker}"
    if pattern.search(content):
        return pattern.sub(replacement, content)
    # Markers not found — return unchanged
    print(
        f"WARNING: markers '{start_marker}' / '{end_marker}' not found in README",
        file=sys.stderr,
    )
    return content


def update_readme(readme_path: Path, stats_block: str, sources_table: str) -> None:
    content = readme_path.read_text()
    content = replace_section(content, STATS_START, STATS_END, stats_block)
    content = replace_section(content, SOURCES_START, SOURCES_END, sources_table)
    readme_path.write_text(content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="meta/history.duckdb")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--json-dir", default="json")
    parser.add_argument("--misc-dir", default="misc")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: DuckDB file not found: {db_path}", file=sys.stderr)
        return 1

    conn = duckdb.connect(str(db_path), read_only=True)

    stats_block = generate_stats_block(conn, Path(args.misc_dir))
    sources_table = generate_sources_table(
        conn, Path(args.json_dir), Path(args.misc_dir)
    )
    conn.close()

    update_readme(Path(args.readme), stats_block, sources_table)
    print(f"README updated: {args.readme}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
