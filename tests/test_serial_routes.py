"""The serial branches of /api/current and /api/timeseries.

Phase 3 of docs/planning/test-suite-plan.md (T3.8-T3.9). The idle_reader fixture
(conftest.py) installs a real SerialReader that was never started, so these tests run
the reader's own get_current/get_history and start no thread.

D7's test (plan §4, fixed in Session 15) goes through get_serial_reader() (app.py:40-51),
which starts a real thread; the failed open ends that thread by itself
(serial_reader.py:67-70). D8's test (fixed in Session 19) goes through it from two threads
at once, with a stand-in reader that starts no thread.
"""

import threading
import time

import pytest

import app as app_module
import serial_reader
from serial_reader import SerialReader

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
    # Unlike the CSV branch, each kept row gains a "values" dict (app.py:185-189).
    assert client.get("/api/timeseries?sensor=co").get_json() == {
        "source": "serial", "data": [{**ROWS[0], "values": {"co": 1.0}}]}


# D7 (plan §4): a port that failed to open was served as data with 200.
def test_port_open_failure_is_not_a_200(client, monkeypatch, tmp_path):
    monkeypatch.setenv("SERIAL_PORT", str(tmp_path / "no-such-port"))
    deadline = time.monotonic() + 2
    resp = client.get("/api/current")
    while resp.status_code == 202 and time.monotonic() < deadline:
        time.sleep(0.01)
        resp = client.get("/api/current")
    if resp.status_code == 202:
        pytest.fail("the reader never reported its open failure")
    assert resp.status_code == 503
    body = resp.get_json()
    assert (body["source"], body["data"]) == ("serial", None)
    assert "no-such-port" in body["error"]  # dashboard.js shows it in the readings grid


# D8 (plan §4): the page's first load asks for readings and history at once
# (static/js/dashboard.js:484-485). Both requests found no reader, and each built and started
# one, so two threads read the port and split its bytes. The stand-in is slow to build, which
# keeps the first request inside get_serial_reader() until the second one arrives. Without the
# delay, this test passed on the unfixed code in 10 runs of 10 (Session 19).
def test_concurrent_first_requests_start_one_reader(monkeypatch):
    built = []

    class SlowReader(SerialReader):
        def __init__(self, *args, **kwargs):
            time.sleep(0.2)
            super().__init__(*args, **kwargs)
            built.append(self)

        def start(self):  # no port, no thread
            pass

    monkeypatch.setattr(serial_reader, "SerialReader", SlowReader)
    monkeypatch.setenv("SERIAL_PORT", "never-opened")
    barrier = threading.Barrier(2)
    status = {}

    def first_request(path):
        client = app_module.app.test_client()
        barrier.wait()
        status[path] = client.get(path).status_code

    threads = [threading.Thread(target=first_request, args=(path,))
               for path in ("/api/current", "/api/timeseries")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
    assert status == {"/api/current": 202, "/api/timeseries": 200}
    assert len(built) == 1
    assert app_module._serial_reader is built[0]
