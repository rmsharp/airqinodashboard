"""Shared fixtures. See docs/planning/test-suite-plan.md §5, Phase 1."""

import pytest

import app as app_module
from serial_reader import SerialReader

# Every environment variable app.py reads per request. FLASK_SECRET_KEY is read
# once at import, so tests leave it alone.
CONFIG_VARS = (
    "AIRQINO_CLIENT_ID", "AIRQINO_CLIENT_SECRET", "AIRQINO_USERNAME", "AIRQINO_PASSWORD",
    "AIRQINO_STATION_NAME", "AIRQINO_PROJECT_NAME", "SERIAL_PORT", "SERIAL_BAUD",
)


@pytest.fixture(autouse=True)
def isolated(monkeypatch):
    """Undo whatever load_dotenv() put in os.environ at import, and reset module state."""
    for var in CONFIG_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(app_module, "_api_client", None)
    monkeypatch.setattr(app_module, "_serial_reader", None)
    monkeypatch.setattr(app_module, "_csv_data", None)


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


@pytest.fixture
def idle_reader(monkeypatch):
    """A real SerialReader, never started, installed as the app's reader: no port, no thread.

    get_serial_reader() returns an installed reader as it is (app.py:40-41). A test fills
    .latest and .history, and the routes read them through the reader's own methods.
    """
    reader = SerialReader("never-opened")
    monkeypatch.setattr(app_module, "_serial_reader", reader)
    return reader
