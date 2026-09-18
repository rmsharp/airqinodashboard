"""The API branches of the routes, with a FakeClient installed as the app's client.

Phase 4 of docs/planning/test-suite-plan.md (T4.10-T4.15), plus get_api_client(), which
the plan's inventory (§3.1) assigns to this phase. FakeClient (conftest.py) answers for
the 7 AirQinoClient methods app.py calls and checks each call against the real method's
signature.

D5 and D2's hourly half are strict xfails (plan §4). The client fixture runs with
TESTING on, so D2's ValueError reaches the test instead of a 500.
"""

from datetime import datetime

import pytest

import app as app_module
from airqino_client import AirQinoClient

CREDS = {"AIRQINO_CLIENT_ID": "cid", "AIRQINO_CLIENT_SECRET": "secret",
         "AIRQINO_USERNAME": "user", "AIRQINO_PASSWORD": "pw"}
SESSION_INFO = [{"station": "S1", "lat": 43.7}, {"station": "S2", "lat": 43.8}]
SENSORS = {"co": "mg/m3"}
HOURLY_CSV = "timestamp;co;pm25\n2026-09-17 00:00;1.5;7\n2026-09-17 01:00;1.6;8\n"


class FrozenDatetime(datetime):
    """app.py's datetime, with utcnow() fixed at 2026-09-17 06:00."""

    @classmethod
    def utcnow(cls):
        return cls(2026, 9, 17, 6, 0)


@pytest.fixture
def configured(monkeypatch):
    monkeypatch.setenv("AIRQINO_STATION_NAME", "S1")
    monkeypatch.setenv("AIRQINO_PROJECT_NAME", "P1")


@pytest.fixture
def frozen(monkeypatch):
    monkeypatch.setattr(app_module, "datetime", FrozenDatetime)


# get_api_client() (app.py:26-37). It builds the client; no request is made.
def test_api_client_is_built_from_the_four_credentials_and_kept(monkeypatch):
    for var, value in CREDS.items():
        monkeypatch.setenv(var, value)
    api = app_module.get_api_client()
    assert isinstance(api, AirQinoClient)
    assert (api.client_id, api.client_secret, api.username, api.password) == ("cid", "secret", "user", "pw")
    assert app_module.get_api_client() is api


@pytest.mark.parametrize("missing", CREDS)
def test_any_missing_credential_means_no_api_client(monkeypatch, missing):
    for var, value in CREDS.items():
        if var != missing:
            monkeypatch.setenv(var, value)
    assert app_module.get_api_client() is None


# T4.10
def test_stations_needs_a_project(client, fake_client):
    resp = client.get("/api/stations")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "No project name specified"}
    assert fake_client.calls == []


@pytest.mark.parametrize("query, project", [("", "P1"), ("?project=P2", "P2")])
def test_stations_passes_the_data_through(client, fake_client, configured, query, project):
    fake_client.returns["get_stations"] = [{"name": "S1"}]
    resp = client.get("/api/stations" + query)
    assert resp.status_code == 200
    assert resp.get_json() == [{"name": "S1"}]
    assert fake_client.calls == [("get_stations", (project,), {})]


# T4.10-T4.14: each route turns a client exception into a 502 that carries its text.
@pytest.mark.parametrize("url", ["/api/stations", "/api/metadata", "/api/current",
                                 "/api/timeseries", "/api/hourly"])
def test_a_client_error_is_a_502_with_its_text(client, fake_client, configured, url):
    fake_client.error = RuntimeError("upstream said no")
    resp = client.get(url)
    assert resp.status_code == 502
    assert resp.get_json() == {"error": "upstream said no"}


# T4.12-T4.14
@pytest.mark.parametrize("url", ["/api/current", "/api/timeseries", "/api/hourly"])
def test_no_station_is_a_400(client, fake_client, url):
    resp = client.get(url)
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "No station name configured"}
    assert fake_client.calls == []


# T4.11
@pytest.mark.parametrize("station, entry", [
    pytest.param("S2", SESSION_INFO[1], id="matching-entry"),
    pytest.param("S9", SESSION_INFO[0], id="no-match-first-entry"),
])
def test_metadata_picks_the_station_entry_from_a_list(client, fake_client, configured, station, entry):
    fake_client.returns["get_session_info"] = SESSION_INFO
    fake_client.returns["get_sensors"] = SENSORS
    resp = client.get(f"/api/metadata?station={station}")
    assert resp.get_json() == {"session_info": entry, "sensors": SENSORS}
    assert fake_client.calls == [("get_session_info", ("P1",), {}), ("get_sensors", (station,), {})]


def test_metadata_passes_a_dict_through(client, fake_client, configured):
    fake_client.returns["get_session_info"] = {"station": "S1", "lat": 43.7}
    fake_client.returns["get_sensors"] = SENSORS
    assert client.get("/api/metadata").get_json() == {
        "session_info": {"station": "S1", "lat": 43.7}, "sensors": SENSORS}


def test_metadata_without_a_project_has_no_session_info(client, fake_client, monkeypatch):
    monkeypatch.setenv("AIRQINO_STATION_NAME", "S1")
    fake_client.returns["get_sensors"] = SENSORS
    assert client.get("/api/metadata").get_json() == {"sensors": SENSORS}
    assert fake_client.calls == [("get_sensors", ("S1",), {})]


def test_metadata_without_a_station_has_no_sensors(client, fake_client, monkeypatch):
    monkeypatch.setenv("AIRQINO_PROJECT_NAME", "P1")
    fake_client.returns["get_session_info"] = SESSION_INFO
    assert client.get("/api/metadata").get_json() == {"session_info": SESSION_INFO[0]}
    assert fake_client.calls == [("get_session_info", ("P1",), {})]


# T4.12
@pytest.mark.parametrize("query, station", [("", "S1"), ("?station=S2", "S2")])
def test_current_returns_the_api_values(client, fake_client, configured, query, station):
    fake_client.returns["get_current_values"] = {"co": 1.5}
    resp = client.get("/api/current" + query)
    assert resp.status_code == 200
    assert resp.get_json() == {"source": "api", "data": {"co": 1.5}}
    assert fake_client.calls == [("get_current_values", (station,), {})]


# README.md:36 documents serial → API → CSV, and the data routes follow it (app.py:144, :182).
@pytest.mark.parametrize("url", ["/api/current", "/api/timeseries"])
def test_serial_is_served_before_the_api(client, fake_client, idle_reader, configured, url):
    idle_reader.latest = {"co": 9.0}
    idle_reader.history.append({"co": 9.0})
    assert client.get(url).get_json()["source"] == "serial"
    assert fake_client.calls == []


# D6 (fixed, Session 18): active_source() checked the API before serial, so with both
# configured the badge said "API Connected" over serial readings. Now the badge and
# /api/status name the source the data routes serve, for every mix of sources. The API
# has all four credentials, so a D5 fix can't flip a case. The reader and client are
# installed only for their own source, so no case starts a thread or sends a request.
BADGES = {"serial": ">Serial<", "api": ">API Connected<", "csv": ">CSV Data<"}


@pytest.mark.parametrize("sources, served", [
    pytest.param(("serial", "api"), "serial", id="serial+api"),
    pytest.param(("serial", "csv"), "serial", id="serial+csv"),
    pytest.param(("api", "csv"), "api", id="api+csv"),
    pytest.param(("serial", "api", "csv"), "serial", id="all-three"),
])
def test_badge_source_is_the_source_the_routes_serve(client, configured, monkeypatch, request,
                                                     sources, served):
    if "serial" in sources:
        monkeypatch.setenv("SERIAL_PORT", "/dev/ttyUSB0")
        reader = request.getfixturevalue("idle_reader")
        reader.latest = {"co": 9.0}
        reader.history.append({"co": 9.0})
    if "api" in sources:
        for var, value in CREDS.items():
            monkeypatch.setenv(var, value)
        request.getfixturevalue("fake_client")
    if "csv" in sources:
        monkeypatch.setattr(app_module, "_csv_data", [{"timestamp": "2026-09-17T00:00:00", "co": 9.0}])
    assert app_module.active_source() == served
    assert BADGES[served] in client.get("/").get_data(as_text=True)
    assert client.get("/api/status").get_json()["source"] == served
    for url in ("/api/current", "/api/timeseries"):
        assert client.get(url).get_json()["source"] == served


# T4.13: 12 hours or less asks for the last 12 h. More asks for a date range from the clock.
@pytest.mark.parametrize("query, call", [
    pytest.param("?hours=12", ("get_last_station_data", (), {"station_name": "S1"}), id="12h"),
    pytest.param("?hours=13", ("get_range", ("S1", "2026-09-16", "2026-09-17"), {}), id="13h"),
    pytest.param("", ("get_range", ("S1", "2026-09-16", "2026-09-17"), {}), id="default-24h"),
    pytest.param("?hours=48", ("get_range", ("S1", "2026-09-15", "2026-09-17"), {}), id="48h"),
    # The chart's widest button (templates/dashboard.html:91), at getRange's 30-day cap (README.md:110).
    pytest.param("?hours=720", ("get_range", ("S1", "2026-08-18", "2026-09-17"), {}), id="30d"),
])
def test_timeseries_hours_picks_the_client_call(client, fake_client, configured, frozen, query, call):
    fake_client.returns[call[0]] = [{"co": 1.5}]
    resp = client.get("/api/timeseries" + query)
    assert resp.get_json() == {"source": "api", "data": [{"co": 1.5}]}
    assert fake_client.calls == [call]


# T4.14. The values stay strings: unlike the CSV upload, nothing converts them.
@pytest.mark.parametrize("query, date_from", [("", "2026-09-10"), ("?days=3", "2026-09-14")])
def test_hourly_parses_the_semicolon_csv(client, fake_client, configured, frozen, query, date_from):
    fake_client.returns["get_hourly_avg"] = HOURLY_CSV
    resp = client.get("/api/hourly" + query)
    assert resp.get_json() == {"source": "api", "data": [
        {"timestamp": "2026-09-17 00:00", "co": "1.5", "pm25": "7"},
        {"timestamp": "2026-09-17 01:00", "co": "1.6", "pm25": "8"},
    ]}
    assert fake_client.calls == [("get_hourly_avg", ("S1", date_from, "2026-09-17"), {"pivot": True})]


# T4.15. All four credentials are set: with only AIRQINO_CLIENT_ID this would pin D5.
def test_status_in_api_mode(client, configured, monkeypatch):
    for var, value in CREDS.items():
        monkeypatch.setenv(var, value)
    assert client.get("/api/status").get_json() == {
        "source": "api", "station_name": "S1", "project_name": "P1", "serial_port": "", "has_csv": False}


# Known defects (plan §4). Keep the word for a green test out of these reasons:
# -ra prints them into the output the tests-passed gate's regex scans.
@pytest.mark.xfail(raises=AssertionError,
                   reason="D5: active_source() says api when only AIRQINO_CLIENT_ID is set, "
                          "but get_api_client() needs all four credentials (app.py:58, :34)")
def test_one_credential_is_not_an_api_connection(client, monkeypatch):
    monkeypatch.setenv("AIRQINO_CLIENT_ID", "cid")
    assert "API Connected" not in client.get("/").get_data(as_text=True)


@pytest.mark.xfail(raises=ValueError, reason="D2: int() on ?days= with no validation (app.py:227)")
def test_hourly_bad_days_is_a_client_error(client, fake_client, configured):
    assert client.get("/api/hourly?days=abc").status_code < 500
