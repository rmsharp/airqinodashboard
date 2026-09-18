"""The AirQino API client: what it sends, and the token lifecycle.

Phase 4 of docs/planning/test-suite-plan.md (T4.1-T4.9). FakeRequests and FakeClock
(conftest.py) replace the requests and time modules inside airqino_client, so these tests
pin every URL, parameter, header and timeout with no network. They can't show that the
real API accepts any of it: there are no credentials yet (plan §5, Phase 4 surface).
"""

import pytest
import requests

from airqino_client import AirQinoClient

# Written out here, not read from airqino_client, so a change to either constant fails a test.
API_BASE = "https://airqino-api.magentalab.it"
TOKEN_URL = "https://airqino-auth.magentalab.it/realms/airqino/protocol/openid-connect/token"

CREDS = ("cid", "secret", "user", "pw")
AUTH = {"Authorization": "Bearer tok-1"}


@pytest.fixture
def api(fake_requests, fake_clock):
    """A client whose first token request, at t=1000, is granted tok-1 for 300 s."""
    fake_requests.grant("tok-1")
    return AirQinoClient(*CREDS)


def grants(fake_requests):
    """The grant_type of each token request, in order."""
    return [c["data"]["grant_type"] for c in fake_requests.calls if c["url"] == TOKEN_URL]


# T4.1
def test_first_request_gets_a_password_grant_then_sends_the_bearer_token(api, fake_requests):
    api.get_stations("P1")
    assert fake_requests.calls == [
        {"method": "POST", "url": TOKEN_URL, "timeout": 15, "data": {
            "grant_type": "password", "client_id": "cid", "client_secret": "secret",
            "username": "user", "password": "pw", "scope": "openid"}},
        {"method": "GET", "url": f"{API_BASE}/getStations/P1", "headers": AUTH, "params": None,
         "timeout": 30},
    ]


# T4.2: the token is reused while now < expiry - 30 (airqino_client.py:23).
def test_token_is_reused_until_30_s_before_expiry(api, fake_requests, fake_clock):
    api.get_stations("P1")
    fake_clock.now = 1269.9
    api.get_stations("P1")
    assert grants(fake_requests) == ["password"]
    assert fake_requests.calls[-1]["headers"] == AUTH


# T4.3
def test_within_30_s_of_expiry_the_refresh_grant_is_used(api, fake_requests, fake_clock):
    api.get_stations("P1")
    fake_requests.grant("tok-2")
    fake_clock.now = 1270.0
    api.get_stations("P1")
    refresh, get = fake_requests.calls[-2:]
    assert refresh == {"method": "POST", "url": TOKEN_URL, "timeout": 15, "data": {
        "grant_type": "refresh_token", "client_id": "cid", "client_secret": "secret",
        "refresh_token": "refresh-1"}}
    assert get["headers"] == {"Authorization": "Bearer tok-2"}


# T4.4
def test_a_failed_refresh_falls_back_to_the_password_grant(api, fake_requests, fake_clock):
    api.get_stations("P1")
    fake_requests.refuse(400)
    fake_requests.grant("tok-3")
    fake_clock.now = 1270.0
    api.get_stations("P1")
    assert grants(fake_requests) == ["password", "refresh_token", "password"]
    assert fake_requests.calls[-1]["headers"] == {"Authorization": "Bearer tok-3"}


# T4.5
def test_a_token_without_expires_in_lasts_300_s(fake_requests, fake_clock):
    fake_requests.grant("tok-1", expires_in=None)
    fake_requests.grant("tok-2")
    api = AirQinoClient(*CREDS)
    api.get_stations("P1")
    fake_clock.now = 1269.9
    api.get_stations("P1")
    assert grants(fake_requests) == ["password"]
    fake_clock.now = 1270.0
    api.get_stations("P1")
    assert grants(fake_requests) == ["password", "refresh_token"]


# T4.6: the 11 endpoint methods, as README.md's API reference lists them.
ENDPOINTS = [
    pytest.param("get_stations", ("P1",), {}, "GET", "/getStations/P1", None,
                 id="get_stations"),
    pytest.param("get_session_info", ("P1",), {}, "GET", "/getSessionInfo/P1", None,
                 id="get_session_info"),
    pytest.param("get_sensors", ("S1",), {}, "GET", "/getSensors", {"station_name": "S1"},
                 id="get_sensors"),
    pytest.param("get_current_values", ("S1",), {}, "GET", "/getCurrentValues/S1", None,
                 id="get_current_values"),
    pytest.param("get_last_values_raw", ("S1",), {}, "GET", "/getLastValuesRaw/S1", None,
                 id="get_last_values_raw"),
    pytest.param("get_last_station_data", (), {"station_name": "S1", "project_name": "P1"},
                 "GET", "/getLastStationData", {"station_name": "S1", "project_name": "P1"},
                 id="get_last_station_data"),
    pytest.param("get_last_station_data", (), {}, "GET", "/getLastStationData", {},
                 id="get_last_station_data-no-args"),
    pytest.param("get_range", ("S1", "2026-09-01", "2026-09-17"), {},
                 "GET", "/getRange/S1/2026-09-01/2026-09-17", None, id="get_range"),
    pytest.param("get_single_day", ("S1", "2026-09-17"), {},
                 "GET", "/getSingleDay/S1/2026-09-17", None, id="get_single_day"),
    pytest.param("get_hourly_avg", ("S1", "2026-09-10", "2026-09-17"), {},
                 "GET", "/getHourlyAvg/S1/2026-09-10/2026-09-17", {}, id="get_hourly_avg"),
    pytest.param("get_station_hourly_avg", (42,),
                 {"start_date": "20260910-0000", "end_date": "20260917-0000"},
                 "GET", "/v3/getStationHourlyAvg/42",
                 {"start_date": "20260910-0000", "end_date": "20260917-0000"},
                 id="get_station_hourly_avg"),
    pytest.param("get_station_hourly_avg", (42,), {}, "GET", "/v3/getStationHourlyAvg/42", {},
                 id="get_station_hourly_avg-no-dates"),
    pytest.param("generate_report", (["S1", "S2"], "pm25", "10-09-2026", "17-09-2026"), {},
                 "POST", "/generateReport", None, id="generate_report"),
]


@pytest.mark.parametrize("name, args, kwargs, method, path, params", ENDPOINTS)
def test_endpoint_url_and_params(api, fake_requests, name, args, kwargs, method, path, params):
    getattr(api, name)(*args, **kwargs)
    call = fake_requests.calls[-1]
    assert (call["method"], call["url"], call.get("params")) == (method, API_BASE + path, params)
    assert (call["headers"], call["timeout"]) == (AUTH, 30)


# T4.7
@pytest.mark.parametrize("pivot, params", [(False, {}), (True, {"pivot": "true"})])
def test_hourly_avg_returns_the_csv_text(api, fake_requests, pivot, params):
    fake_requests.answer(json={"not": "this"}, text="timestamp;co\n2026-09-17 00:00;1.5\n")
    result = api.get_hourly_avg("S1", "2026-09-10", "2026-09-17", pivot=pivot)
    assert result == "timestamp;co\n2026-09-17 00:00;1.5\n"
    assert fake_requests.calls[-1]["params"] == params


# T4.8
def test_generate_report_posts_a_json_body(api, fake_requests):
    fake_requests.answer(json=[{"day": "10-09-2026", "avg": 7.5}])
    result = api.generate_report(["S1", "S2"], "pm25", "10-09-2026", "17-09-2026")
    assert result == [{"day": "10-09-2026", "avg": 7.5}]
    assert fake_requests.calls[-1] == {
        "method": "POST", "url": f"{API_BASE}/generateReport", "headers": AUTH, "timeout": 30,
        "json": {"centraline": ["S1", "S2"], "grandezza": "pm25",
                 "start_date": "10-09-2026", "end_date": "17-09-2026"}}


# T4.9: nothing between raise_for_status() and the caller catches an HTTP error.
@pytest.mark.parametrize("call", [
    pytest.param(lambda api: api.get_stations("P1"), id="_get"),
    pytest.param(lambda api: api.get_hourly_avg("S1", "2026-09-10", "2026-09-17"), id="get_hourly_avg"),
    pytest.param(lambda api: api.generate_report(["S1"], "pm25", "10-09-2026", "17-09-2026"),
                 id="generate_report"),
])
def test_an_http_error_reaches_the_caller(api, fake_requests, call):
    fake_requests.answer(status_code=500)
    with pytest.raises(requests.HTTPError):
        call(api)


def test_a_refused_password_grant_reaches_the_caller(fake_requests, fake_clock):
    fake_requests.refuse(401)
    with pytest.raises(requests.HTTPError):
        AirQinoClient(*CREDS).get_stations("P1")
    assert [c["method"] for c in fake_requests.calls] == ["POST"]  # no request went out without a token
