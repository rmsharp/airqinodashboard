"""Shared fixtures. See docs/planning/test-suite-plan.md §5, Phase 1."""

import pytest

import app as app_module

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
