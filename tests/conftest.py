"""Shared fixtures. See docs/planning/test-suite-plan.md §5, Phase 1."""

import pytest
import requests

import airqino_client
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


class FakeResponse:
    """The parts of requests.Response that airqino_client uses."""

    def __init__(self, json=None, text="", status_code=200):
        self._json = json
        self.text = text
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error", response=self)


class FakeRequests:
    """Stands in for the requests module inside airqino_client: records calls, answers from a script.

    A token request (form data with a grant_type) takes the next queued grant or refusal.
    Any other request gets the current answer. Each call is recorded as a dict of the method,
    the URL and the keyword arguments exactly as passed.
    """

    HTTPError = requests.HTTPError  # so code that catches the real class still behaves the same

    def __init__(self):
        self.calls = []
        self._token_replies = []
        self._answer = FakeResponse(json={})

    def grant(self, access_token, expires_in=300, refresh_token="refresh-1"):
        """Queue a token reply. expires_in=None leaves the field out."""
        body = {"access_token": access_token, "refresh_token": refresh_token}
        if expires_in is not None:
            body["expires_in"] = expires_in
        self._token_replies.append(FakeResponse(json=body))

    def refuse(self, status_code):
        """Queue a token reply that fails raise_for_status()."""
        self._token_replies.append(FakeResponse(json={}, status_code=status_code))

    def answer(self, json=None, text="", status_code=200):
        """Set the reply to every request that isn't for a token."""
        self._answer = FakeResponse(json=json, text=text, status_code=status_code)

    def get(self, url, **kwargs):
        return self._send("GET", url, kwargs)

    def post(self, url, **kwargs):
        return self._send("POST", url, kwargs)

    def _send(self, method, url, kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        if "grant_type" in (kwargs.get("data") or {}):
            return self._token_replies.pop(0)
        return self._answer


class FakeClock:
    """Stands in for the time module inside airqino_client, which only calls time.time()."""

    def __init__(self, now=1000.0):
        self.now = now

    def time(self):
        return self.now


@pytest.fixture
def fake_requests(monkeypatch):
    fake = FakeRequests()
    monkeypatch.setattr(airqino_client, "requests", fake)
    return fake


@pytest.fixture
def fake_clock(monkeypatch):
    """Patches airqino_client's own time name, never the global time.time, which pytest uses."""
    clock = FakeClock()
    monkeypatch.setattr(airqino_client, "time", clock)
    return clock
