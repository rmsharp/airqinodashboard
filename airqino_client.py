"""AirQino API client with OAuth2 authentication."""

import time
import requests


API_BASE = "https://airqino-api.magentalab.it"
TOKEN_URL = "https://airqino-auth.magentalab.it/realms/airqino/protocol/openid-connect/token"


class AirQinoClient:
    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self._token = None
        self._token_expiry = 0
        self._refresh_token = None

    def _get_token(self):
        now = time.time()
        if self._token and now < self._token_expiry - 30:
            return self._token

        # Try refresh token first
        if self._refresh_token:
            try:
                return self._do_refresh()
            except Exception:
                pass

        # Full auth
        resp = requests.post(TOKEN_URL, data={
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
            "scope": "openid",
        }, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 300)
        self._refresh_token = data.get("refresh_token")
        return self._token

    def _do_refresh(self):
        resp = requests.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self._refresh_token,
        }, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 300)
        self._refresh_token = data.get("refresh_token")
        return self._token

    def _headers(self):
        return {"Authorization": f"Bearer {self._get_token()}"}

    def _get(self, path, params=None):
        resp = requests.get(f"{API_BASE}{path}", headers=self._headers(),
                            params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # --- Station discovery ---

    def get_stations(self, project_name):
        """List all stations for a project."""
        return self._get(f"/getStations/{project_name}")

    def get_session_info(self, project_name):
        """Station metadata: sensor list, description, coordinates."""
        return self._get(f"/getSessionInfo/{project_name}")

    def get_sensors(self, station_name):
        """Sensor configuration for a station."""
        return self._get("/getSensors", params={"station_name": station_name})

    # --- Current readings ---

    def get_current_values(self, station_name):
        """Latest calibrated sensor values."""
        return self._get(f"/getCurrentValues/{station_name}")

    def get_last_values_raw(self, station_name):
        """Latest raw (uncalibrated) sensor values."""
        return self._get(f"/getLastValuesRaw/{station_name}")

    def get_last_station_data(self, station_name=None, project_name=None):
        """Last 12 hours of calibrated data."""
        params = {}
        if station_name:
            params["station_name"] = station_name
        if project_name:
            params["project_name"] = project_name
        return self._get("/getLastStationData", params=params)

    # --- Historical / time-series ---

    def get_range(self, station_name, date_from, date_to):
        """Raw data for a date range (max 30 days). Dates: YYYY-mm-dd."""
        return self._get(f"/getRange/{station_name}/{date_from}/{date_to}")

    def get_single_day(self, station_name, date):
        """Raw data for a single day. Date: YYYY-mm-dd."""
        return self._get(f"/getSingleDay/{station_name}/{date}")

    def get_hourly_avg(self, station_name, date_from, date_to, pivot=False):
        """Hourly averages. Returns CSV text. Dates: YYYY-mm-dd."""
        params = {"pivot": "true"} if pivot else {}
        resp = requests.get(
            f"{API_BASE}/getHourlyAvg/{station_name}/{date_from}/{date_to}",
            headers=self._headers(), params=params, timeout=30,
        )
        resp.raise_for_status()
        return resp.text

    def get_station_hourly_avg(self, station_id, start_date=None, end_date=None):
        """Calibrated hourly data (v3). station_id is numeric.
        Dates: YYYYmmdd-HHMM format."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._get(f"/v3/getStationHourlyAvg/{station_id}", params=params)

    # --- Reports ---

    def generate_report(self, station_names, sensor, start_date, end_date):
        """Daily avg/min/max for a sensor across stations.
        Dates: dd-mm-YYYY format."""
        resp = requests.post(f"{API_BASE}/generateReport",
                             headers=self._headers(),
                             json={
                                 "centraline": station_names,
                                 "grandezza": sensor,
                                 "start_date": start_date,
                                 "end_date": end_date,
                             }, timeout=30)
        resp.raise_for_status()
        return resp.json()
