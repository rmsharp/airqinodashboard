"""The serial branches of /api/current and /api/timeseries.

Phase 3 of docs/planning/test-suite-plan.md (T3.8-T3.9). The idle_reader fixture
(conftest.py) installs a real SerialReader that was never started, so these tests run
the reader's own get_current/get_history and start no thread.

D7 is a strict xfail (plan §4). It goes through get_serial_reader() (app.py:38-48),
which starts a real thread; the failed open ends that thread by itself
(serial_reader.py:66-69).
"""

import time

import pytest

ROWS = [
    {"co": 1.0, "timestamp": "2026-09-17T00:00:00+00:00"},
    {"pm25": 7.0, "timestamp": "2026-09-17T00:03:00+00:00"},
]


# T3.8
def test_current_returns_the_latest_reading(client, idle_reader):
    idle_reader.latest = dict(ROWS[0])
    resp = client.get("/api/current")
    assert resp.status_code == 200
    assert resp.get_json() == {"source": "serial", "data": ROWS[0]}


def test_current_before_any_reading_is_202(client, idle_reader):
    resp = client.get("/api/current")
    assert resp.status_code == 202
    assert resp.get_json() == {"source": "serial", "data": None, "error": "No data received yet"}


# T3.9
def test_timeseries_returns_the_history(client, idle_reader):
    idle_reader.history.extend(ROWS)
    assert client.get("/api/timeseries").get_json() == {"source": "serial", "data": ROWS}


def test_timeseries_sensor_filter_reshapes_rows_with_that_key(client, idle_reader):
    idle_reader.history.extend(ROWS)
    # Unlike the CSV branch, each kept row gains a "values" dict (app.py:178-182).
    assert client.get("/api/timeseries?sensor=co").get_json() == {
        "source": "serial", "data": [{**ROWS[0], "values": {"co": 1.0}}]}


# Known defect (plan §4). Keep the word for a green test out of the reason:
# -ra prints it into the output the tests-passed gate's regex scans.
@pytest.mark.xfail(raises=AssertionError,
                   reason="D7: a port that fails to open is served as data with 200 "
                          "(serial_reader.py:64-69, app.py:143-145)")
def test_port_open_failure_is_not_a_200(client, monkeypatch, tmp_path):
    monkeypatch.setenv("SERIAL_PORT", str(tmp_path / "no-such-port"))
    deadline = time.monotonic() + 2
    resp = client.get("/api/current")
    while resp.status_code == 202 and time.monotonic() < deadline:
        time.sleep(0.01)
        resp = client.get("/api/current")
    if resp.status_code == 202:
        pytest.fail("the reader never reported its open failure")  # FAILED, never XFAIL
    assert resp.status_code != 200
