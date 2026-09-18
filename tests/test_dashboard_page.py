"""GET / — the setup banner, the source badge and the header.

Phase 1 of docs/planning/test-suite-plan.md (T1.1-T1.7). T1.1 guards Session 7's
banner fix (e5f52e1): the REV6 board has no USB port, so the page must not tell
the user to plug a cable into an Arduino Mega.
"""

import html
import os
import re
from pathlib import Path

import pytest

import app as app_module

# The per-request variables app.py reads, listed here rather than imported from
# conftest, so that T1.7 still checks all of them if conftest's list shrinks.
ISOLATED_VARS = (
    "AIRQINO_CLIENT_ID", "AIRQINO_CLIENT_SECRET", "AIRQINO_USERNAME", "AIRQINO_PASSWORD",
    "AIRQINO_STATION_NAME", "AIRQINO_PROJECT_NAME", "SERIAL_PORT", "SERIAL_BAUD",
)
IMPORT_TIME_VARS = ("FLASK_SECRET_KEY",)
MODULE_GLOBALS = ("_api_client", "_serial_reader", "_csv_data")

BANNER_HEADING = "Connect Your AirQino"


@pytest.fixture(autouse=True, scope="module")
def planted_leak():
    """Plant the worst case a stray .env could cause: every variable set, every global filled.

    Module scope runs before conftest's function-scoped `isolated` fixture, which
    must undo all of it for every test here. Without this, a broken `isolated`
    passes on any machine that has no .env. The originals come back at module end.
    """
    with pytest.MonkeyPatch.context() as mp:
        for var in ISOLATED_VARS:
            mp.setenv(var, f"planted-{var.lower()}")
        for name in MODULE_GLOBALS:
            mp.setattr(app_module, name, f"planted-{name}")
        yield


def get_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    return resp.get_data(as_text=True)


def visible_text(page):
    """The page with entities decoded and whitespace collapsed, for phrases that span template lines."""
    return re.sub(r"\s+", " ", html.unescape(page))


# T1.1
def test_no_source_shows_rev6_setup_banner(client):
    page = get_page(client)
    assert BANNER_HEADING in page
    assert "Serial Adapter" in page
    assert "docs/HARDWARE.md" in page
    # The stale hardware copy (Session 7's surface grep, minus "usb port":
    # the correct banner says "The REV6 board has no USB port").
    lowered = page.lower()
    for stale in ("arduino", "mega", "usb cable", "usb serial", "usb-b"):
        assert stale not in lowered, f"stale hardware wording on the page: {stale!r}"


# T1.2
def test_no_source_badge_and_placeholder(client):
    page = get_page(client)
    # Match the badge markup: the bare phrase also appears in an HTML comment.
    assert ">No Data Source<" in page
    assert "Configure a data source to see readings" in page


# T1.3
def test_csv_source_hides_banner(client, monkeypatch):
    monkeypatch.setattr(app_module, "_csv_data", [{"timestamp": "2026-09-17T00:00:00", "pm25": 7.0}])
    page = get_page(client)
    assert BANNER_HEADING not in page
    assert ">CSV Data<" in page
    assert "Import CSV Data" in page


# T1.4
def test_serial_source_hides_banner(client, monkeypatch):
    monkeypatch.setenv("SERIAL_PORT", "/dev/tty.not-a-real-port")
    page = get_page(client)
    assert BANNER_HEADING not in page
    assert ">Serial<" in page
    # dashboard() reads the environment only; it must not start a reader thread.
    assert app_module._serial_reader is None


# T1.5
def test_api_source_badge_and_project_row(client, monkeypatch):
    monkeypatch.setenv("AIRQINO_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AIRQINO_PROJECT_NAME", "TestProject")
    page = get_page(client)
    assert BANNER_HEADING not in page
    assert ">API Connected<" in page
    assert '<span class="key">Project</span><span class="val">TestProject</span>' in page


# T1.6
def test_header_shows_station_and_project(client, monkeypatch):
    monkeypatch.setenv("AIRQINO_STATION_NAME", "TestStation")
    monkeypatch.setenv("AIRQINO_PROJECT_NAME", "TestProject")
    text = visible_text(get_page(client))
    assert "Station: TestStation · Project: TestProject" in text
    assert "Device S/N: AIRO 6153" not in text


def test_header_falls_back_to_device_serial(client):
    text = visible_text(get_page(client))
    assert "Device S/N: AIRO 6153" in text
    assert "Station:" not in text


# T1.7 — guard the guard
def test_isolation_fixture_undoes_the_planted_leak():
    leaked = [var for var in ISOLATED_VARS if var in os.environ]
    assert leaked == [], f"the isolated fixture let these through: {leaked}"
    stale = [name for name in MODULE_GLOBALS if getattr(app_module, name) is not None]
    assert stale == [], f"the isolated fixture did not reset: {stale}"


def test_isolation_covers_every_variable_app_reads():
    # A new os.getenv() in app.py has to join the isolation lists, or a .env leaks it into tests.
    source = Path(app_module.__file__).read_text()
    read_by_app = set(re.findall(r"""os\.getenv\(\s*["']([A-Z0-9_]+)["']""", source))
    uncovered = read_by_app - set(ISOLATED_VARS) - set(IMPORT_TIME_VARS)
    assert uncovered == set(), (
        f"app.py reads {sorted(uncovered)}; add them to CONFIG_VARS in tests/conftest.py "
        "and to ISOLATED_VARS here"
    )
    assert read_by_app >= set(ISOLATED_VARS), "the variable scan found fewer reads than expected"
