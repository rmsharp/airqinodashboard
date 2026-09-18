"""The no-source contract and the CSV upload path.

Phase 2 of docs/planning/test-suite-plan.md (T2.1-T2.8). With no source configured,
every JSON route must say so with a 4xx/5xx body, not crash. The CSV upload is the
path README.md calls the fastest way to see data.

D2 (timeseries half), D3 and D4 are strict xfails (plan §4). A fix makes its test
XPASS, which fails the suite until the marker comes off (plan §6). The client
fixture runs with TESTING on, so Flask raises a route's exception into the test
instead of answering 500; each marker names the exception it expects today.
"""

import io

import pytest

import app as app_module

BANNER_HEADING = "Connect Your AirQino"
NO_SOURCE = {"error": "No data source configured"}
NO_API = {"error": "API not configured"}

SMALL_CSV = "timestamp,pm25\n2026-09-17T00:00,7\n2026-09-17T01:00,8\n"


def upload(client, content, filename="data.csv"):
    """POST a file under the field name the dashboard's FormData uses (dashboard.js:432)."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return client.post(
        "/api/upload_csv",
        data={"file": (io.BytesIO(content), filename)},
        content_type="multipart/form-data",
    )


def csv_text(rows, delimiter=","):
    return "".join(delimiter.join(row) + "\n" for row in rows)


# T2.1
@pytest.mark.parametrize("route, status, body", [
    ("/api/status", 200, {"source": None, "has_csv": False,
                          "station_name": "", "project_name": "", "serial_port": ""}),
    ("/api/current", 503, NO_SOURCE),
    ("/api/timeseries", 503, NO_SOURCE),
    ("/api/stations", 503, NO_API),
    ("/api/metadata", 503, NO_API),
    ("/api/hourly", 503, NO_API),
])
def test_no_source_contract(client, route, status, body):
    resp = client.get(route)
    assert resp.status_code == status
    assert resp.get_json() == body


# T2.2
def test_upload_without_file_part_is_400(client):
    resp = client.post("/api/upload_csv", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "No file provided"}


def test_upload_with_empty_filename_is_400(client):
    # What a browser sends when the file input has nothing selected.
    resp = upload(client, SMALL_CSV, filename="")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "No file selected"}
    assert app_module._csv_data is None


# T2.3
@pytest.mark.parametrize("delimiter", [";", "\t", ","], ids=["semicolon", "tab", "comma"])
def test_upload_detects_delimiter(client, delimiter):
    text = csv_text([
        ("timestamp", "pm25", "no2"),
        ("2026-09-17T00:00", "7", "17"),
        ("2026-09-17T01:00", "8", "18"),
    ], delimiter)
    resp = upload(client, text)
    assert resp.status_code == 200
    assert resp.get_json() == {"rows": 2, "columns": ["timestamp", "pm25", "no2"]}


# T2.4
def test_upload_coerces_values_and_normalizes_headers(client):
    resp = upload(client, " Timestamp , PM25 ,Site\n2026-09-17T00:00, 7.5 ,  Rome  \n")
    assert resp.get_json()["columns"] == ["timestamp", "pm25", "site"]
    [row] = app_module._csv_data
    assert row == {"timestamp": "2026-09-17T00:00", "pm25": 7.5, "site": "Rome"}
    assert type(row["pm25"]) is float


# T2.5 — characterization: current behaviour, not necessarily intended (plan §4).
def test_upload_short_row_stores_none(client):
    upload(client, "timestamp,pm25,no2\n2026-09-17T00:00,7\n")
    assert app_module._csv_data == [{"timestamp": "2026-09-17T00:00", "pm25": 7.0, "no2": None}]


# T2.6
@pytest.fixture
def uploaded_501(client):
    """Upload 501 rows, one more than /api/timeseries returns; give back the rows as stored."""
    stamps = [f"2026-09-17T{i // 60:02d}:{i % 60:02d}" for i in range(501)]
    resp = upload(client, csv_text([("timestamp", "pm25")] + [(s, str(i)) for i, s in enumerate(stamps)]))
    assert resp.get_json()["rows"] == 501
    return [{"timestamp": s, "pm25": float(i)} for i, s in enumerate(stamps)]


def test_upload_makes_csv_the_active_source(client):
    upload(client, SMALL_CSV)
    status = client.get("/api/status").get_json()
    assert status["source"] == "csv"
    assert status["has_csv"] is True
    page = client.get("/").get_data(as_text=True)
    assert ">CSV Data<" in page
    assert BANNER_HEADING not in page


def test_current_returns_last_uploaded_row(client, uploaded_501):
    resp = client.get("/api/current")
    assert resp.status_code == 200
    assert resp.get_json() == {"source": "csv", "data": uploaded_501[-1]}


def test_timeseries_returns_the_last_500_rows(client, uploaded_501):
    body = client.get("/api/timeseries").get_json()
    assert body["source"] == "csv"
    assert len(body["data"]) == 500
    assert body["data"] == uploaded_501[-500:]


def test_timeseries_sensor_filter_keeps_rows_with_that_key(client):
    upload(client, SMALL_CSV)
    # Unlike the serial branch (app.py:178-182), CSV rows come back whole, not reshaped.
    assert len(client.get("/api/timeseries?sensor=pm25").get_json()["data"]) == 2
    assert client.get("/api/timeseries?sensor=no2").get_json() == {"source": "csv", "data": []}


# T2.7 — characterization: current behaviour, not necessarily intended (plan §4).
def test_empty_upload_replaces_data_and_clears_source(client):
    upload(client, SMALL_CSV)
    resp = upload(client, b"")
    assert resp.status_code == 200
    assert resp.get_json() == {"rows": 0, "columns": []}
    assert client.get("/api/status").get_json()["source"] is None
    assert client.get("/api/current").status_code == 503


# T2.8
def test_invalid_utf8_is_replaced_not_rejected(client):
    resp = upload(client, b"timestamp,site\n2026-09-17T00:00,caf\xe9\n")
    assert resp.status_code == 200
    assert app_module._csv_data == [{"timestamp": "2026-09-17T00:00", "site": "caf�"}]


# Known defects (plan §4). Keep the word for a green test out of these reasons:
# -ra prints them into the output the tests-passed gate's regex scans.
@pytest.mark.xfail(raises=ValueError, reason="D2: int() on ?hours= with no validation (app.py:171)")
def test_timeseries_bad_hours_is_a_client_error(client):
    resp = client.get("/api/timeseries?hours=abc")
    assert resp.status_code < 500


@pytest.mark.xfail(raises=AttributeError,
                   reason="D3: extra fields land under the key None, and k.strip() fails on it (app.py:258-261)")
def test_ragged_row_is_not_a_server_error(client):
    resp = upload(client, "a,b\n1,2,3\n")
    assert resp.status_code < 500


@pytest.mark.xfail(raises=AssertionError,
                   reason="D4: decoded as utf-8, not utf-8-sig, so a BOM stays in the first header (app.py:245)")
def test_bom_is_not_part_of_the_first_header(client):
    resp = upload(client, "﻿timestamp,pm25\n2026-09-17T00:00,7\n")
    assert resp.get_json()["columns"][0] == "timestamp"
