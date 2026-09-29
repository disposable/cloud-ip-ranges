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


def test_provider_json_without_provider_id_falls_back_to_stem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression: a file missing provider_id must not crash (used to KeyError)."""
    (tmp_path / "json").mkdir(parents=True)
    (tmp_path / "misc").mkdir(parents=True)
    db_path = tmp_path / "meta" / "h.duckdb"

    payload = _provider_json(["9.0.0.0/24"])
    del payload["provider_id"]
    (tmp_path / "json" / "mystery.json").write_text(json.dumps(payload))

    _run(tmp_path, monkeypatch)  # must not raise

    conn = duckdb.connect(str(db_path))
    rows = conn.execute("SELECT provider_id, cidr FROM cidr_history").fetchall()
    conn.close()
    assert rows == [("mystery", "9.0.0.0/24")]


def test_corrupt_provider_json_fails_loudly(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A malformed provider file must abort the run loudly.

    Crawler writes are atomic, so a corrupt file signals a real anomaly
    (manual edit, disk corruption) that should surface rather than be
    silently skipped — skipping would freeze that provider's history.
    """
    (tmp_path / "json").mkdir(parents=True)
    (tmp_path / "misc").mkdir(parents=True)

    (tmp_path / "json" / "acme.json").write_text('{"provider_id": "acme", "ipv4": ["1.0')  # truncated

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
    with pytest.raises(json.JSONDecodeError):
        update_history.main()


def test_patch_csv_missing_file_is_noop(tmp_path: Path) -> None:
    update_history.patch_csv(tmp_path / "absent.csv", [("1.0.0.0/24", datetime.now(tz=timezone.utc))], [])
    assert not (tmp_path / "absent.csv").exists()


def test_patch_writes_leave_no_temp_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Atomic writes must clean up .tmp siblings on success."""
    (tmp_path / "json").mkdir(parents=True)
    (tmp_path / "misc").mkdir(parents=True)
    acme = tmp_path / "json" / "acme.json"

    acme.write_text(json.dumps(_provider_json(["1.0.0.0/24", "2.0.0.0/24"])))
    _run(tmp_path, monkeypatch)
    acme.write_text(json.dumps(_provider_json(["1.0.0.0/24"])))
    _run(tmp_path, monkeypatch)  # patches files (retirement injection)

    assert not list(tmp_path.rglob("*.tmp"))
