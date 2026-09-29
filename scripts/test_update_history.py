"""End-to-end tests for the update_history retire/inject/purge lifecycle."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import duckdb
import pytest

import update_history


def _provider_json(cidrs: list[str], retired: list[str] | None = None) -> dict:
    d = {
        "provider_id": "acme",
        "provider": "Acme",
        "method": "published_list",
        "ipv4": cidrs,
        "ipv6": [],
        "source": ["https://example.com/ips"],
    }
    if retired:
        d["details_ipv4"] = [{"address": c, "retired_at": datetime.now(tz=timezone.utc).isoformat()} for c in retired]
    return d


def _run(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "update_history.py",
            "--db",
            str(tmp_path / "meta" / "h.duckdb"),
            "--json-dir",
            str(tmp_path / "json"),
            "--misc-dir",
            str(tmp_path / "misc"),
        ],
    )
    assert update_history.main() == 0


def _retired_rows(db_path: Path) -> dict[str, object]:
    conn = duckdb.connect(str(db_path))
    rows = conn.execute("SELECT cidr, retired_at FROM cidr_history ORDER BY cidr").fetchall()
    conn.close()
    return dict(rows)


def test_retire_inject_persist_prune_lifecycle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "json").mkdir(parents=True)
    (tmp_path / "misc").mkdir(parents=True)
    db_path = tmp_path / "meta" / "h.duckdb"
    acme = tmp_path / "json" / "acme.json"

    # Day 0: two published CIDRs
    acme.write_text(json.dumps(_provider_json(["1.0.0.0/24", "2.0.0.0/24"])))
    _run(tmp_path, monkeypatch)
    assert _retired_rows(db_path) == {"1.0.0.0/24": None, "2.0.0.0/24": None}

    # Provider drops 2.0.0.0/24 -> marked retired and re-injected with marker
    acme.write_text(json.dumps(_provider_json(["1.0.0.0/24"])))
    _run(tmp_path, monkeypatch)
    patched = json.loads(acme.read_text())
    assert "2.0.0.0/24" in patched["ipv4"]
    assert any(d.get("address") == "2.0.0.0/24" and d.get("retired_at") for d in patched["details_ipv4"])

    # Re-run on the patched file: the injected entry must NOT be reactivated
    _run(tmp_path, monkeypatch)
    assert _retired_rows(db_path)["2.0.0.0/24"] is not None

    # Age the row beyond the retention window -> purged from DB and pruned
    conn = duckdb.connect(str(db_path))
    conn.execute(
        "UPDATE cidr_history SET retired_at = ? WHERE cidr = '2.0.0.0/24'",
        [(datetime.now(tz=timezone.utc) - timedelta(weeks=update_history.RETIREMENT_WEEKS + 1)).isoformat()],
    )
    conn.close()
    _run(tmp_path, monkeypatch)

    assert "2.0.0.0/24" not in _retired_rows(db_path)
    final = json.loads(acme.read_text())
    assert "2.0.0.0/24" not in final["ipv4"]
    assert not final.get("details_ipv4")


def test_missing_output_files_do_not_crash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "json").mkdir(parents=True)
    (tmp_path / "misc").mkdir(parents=True)
    db_path = tmp_path / "meta" / "h.duckdb"
    acme = tmp_path / "json" / "acme.json"

    acme.write_text(json.dumps(_provider_json(["1.0.0.0/24"])))
    _run(tmp_path, monkeypatch)

    # Retire the CIDR in the DB, then delete the provider file entirely.
    acme.write_text(json.dumps(_provider_json([])))
    _run(tmp_path, monkeypatch)
    acme.unlink()

    _run(tmp_path, monkeypatch)  # must not raise
    assert _retired_rows(db_path)["1.0.0.0/24"] is not None
