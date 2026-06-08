# AirQino Dashboard

A self-hosted web dashboard for viewing air-quality data from an **AirQino Air Aware Outdoor** environmental monitoring station. It renders live and historical readings — particulate matter, gases, temperature, and humidity — with EPA AQI color coding, interactive time-series charts, a location map, and device metadata.

## Background

This dashboard was built to recover data from a single abandoned AirQino Outdoor device (**PN 800506 / S/N AIRO 6153**) left over from a discontinued air-quality monitoring project. AirQino stations normally phone home over cellular to the vendor's cloud platform, but with the originating project shut down there is no portal access to the device's data. This app provides three independent ways to read the device — cloud API, direct serial, or CSV/SD-card upload — so the hardware stays useful even without the original project's infrastructure.

The device is a **REV6 (gen-2022) custom board by Quantit** — *not* a standard Arduino Mega, and it has **no USB port**. See [`docs/HARDWARE.md`](docs/HARDWARE.md) for the full hardware story before attempting a serial connection.

## Quick start

Requires Python 3.9+.

```bash
pip install -r requirements.txt
cp .env.example .env        # then edit .env to configure a data source
python3 app.py
```

Open <http://localhost:5001>.

The dashboard runs with no configuration — it just shows a "Connect Your AirQino" setup banner until you wire up one of the data sources below. The CSV upload path works immediately with no `.env` changes at all.

## Connecting a data source

Configuration lives in `.env` (copy from `.env.example`). The dashboard auto-detects which source is active in this priority order: **serial → API → CSV**.

### 1. CSV / SD-card upload (no setup)

The device logs to an onboard SD card. Extract the card (or export any AirQino CSV), then drag-and-drop the file onto the dashboard's upload area. The parser auto-detects comma, semicolon, or tab delimiters. No `.env` configuration needed — this is the fastest way to see data.

### 2. Cloud API (OAuth2)

Requires credentials from the vendor. Contact **info@airqino.it** (or **info@tea-group.it**) with serial number **AIRO 6153** and request:

- OAuth2 credentials: client ID, client secret, username, password
- Your station's `SMART###` name — the printed serial number does **not** map directly to the API station name

Then set in `.env`:

```ini
AIRQINO_CLIENT_ID=...
AIRQINO_CLIENT_SECRET=...
AIRQINO_USERNAME=...
AIRQINO_PASSWORD=...
AIRQINO_STATION_NAME=SMART###
AIRQINO_PROJECT_NAME=...
```

### 3. Direct serial (USB-to-TTL adapter)

The REV6 board has no USB port, so a direct connection needs a **USB-to-TTL serial adapter** (CP2102 or FT232RL, set to **3.3V logic**) wired to the board's TX/RX pins, plus female-to-female DuPont jumper wires. Wiring, adapter recommendations, and voltage warnings are in [`docs/HARDWARE.md`](docs/HARDWARE.md).

Once the adapter enumerates as a serial device:

```ini
SERIAL_PORT=/dev/tty.usbserial-XXXX   # macOS; /dev/ttyUSB0 on Linux
SERIAL_BAUD=9600
```

The serial reader runs in a background thread and parses the AirQino's output (semicolon-delimited, `key=value`, or JSON, depending on firmware).

## Dashboard features

- **Current readings** — one card per sensor, tinted by EPA AQI breakpoints (good → hazardous) for PM2.5, PM10, NO₂, O₃, and CO.
- **Time-series chart** — Chart.js line chart with selectable ranges: 6h, 12h, 24h, 3d, 7d, 30d.
- **Sensor toggles** — show/hide any sensor on the chart (PM2.5 and PM10 on by default).
- **Location map** — Leaflet map (CARTO dark tiles) that drops a marker from the station's GPS coordinates.
- **Device metadata** — part/serial number, model, manufacturer, station name, and sensor list.
- **CSV import** — drag-and-drop upload, always available.
- **Auto-refresh** — current readings poll every 60 seconds.

Tracked sensors and units: PM2.5 (µg/m³), PM10 (µg/m³), NO₂ (µg/m³), CO (mg/m³), O₃ (µg/m³), CO₂ (ppm), Temperature (°C), Humidity (%), VOC (µg/m³).

## AirQino API reference

The cloud client (`airqino_client.py`) authenticates via OAuth2 (Keycloak, password grant) and caches/refreshes the bearer token automatically.

- **API base:** `https://airqino-api.magentalab.it`
- **Token endpoint:** `https://airqino-auth.magentalab.it/realms/airqino/protocol/openid-connect/token`

Key endpoints wrapped by the client:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `get_stations(project)` | `/getStations/{project}` | List stations in a project |
| `get_session_info(project)` | `/getSessionInfo/{project}` | Station metadata: sensors, description, coordinates |
| `get_sensors(station)` | `/getSensors` | Sensor configuration for a station |
| `get_current_values(station)` | `/getCurrentValues/{station}` | Latest calibrated values |
| `get_last_values_raw(station)` | `/getLastValuesRaw/{station}` | Latest raw (uncalibrated) values |
| `get_last_station_data(...)` | `/getLastStationData` | Last 12 hours of calibrated data |
| `get_range(station, from, to)` | `/getRange/{station}/{from}/{to}` | Raw data for a date range (**30-day max**), `YYYY-mm-dd` |
| `get_single_day(station, date)` | `/getSingleDay/{station}/{date}` | Raw data for one day |
| `get_hourly_avg(station, from, to)` | `/getHourlyAvg/{station}/{from}/{to}` | Hourly averages as **CSV** (use `pivot=true`) |
| `get_station_hourly_avg(id, ...)` | `/v3/getStationHourlyAvg/{id}` | Calibrated hourly data (v3); numeric station id, `YYYYmmdd-HHMM` dates |
| `generate_report(...)` | `/generateReport` | Daily avg/min/max for a sensor (POST) |

**Known quirks:** the API returns an empty `{}` body for 401s (no error message); `getHourlyAvg` returns CSV rather than JSON; `getRange` rejects spans over 30 days.

### Flask routes

`app.py` exposes the UI and a small JSON API consumed by the front end:

| Route | Description |
|-------|-------------|
| `GET /` | Dashboard page |
| `GET /api/status` | Active data source and station/config info |
| `GET /api/current` | Current readings (serial → API → CSV) |
| `GET /api/timeseries?hours=N` | Time-series data for the chart |
| `GET /api/hourly?days=N` | Hourly averages (API mode, parsed from CSV) |
| `GET /api/stations?project=...` | List stations (API mode) |
| `GET /api/metadata?station=...` | Station metadata (API mode) |
| `POST /api/upload_csv` | Upload a CSV/SD-card export |

## Device hardware summary

| Field | Value |
|-------|-------|
| Product | AirQino Air Aware Outdoor |
| Part number | TEA 800506 |
| Serial number | AIRO 6153 |
| Board | REV6 (gen-2022), custom PCB by **Quantit** — **not** an Arduino Mega, **no USB port** |
| Firmware | Net Rev3.11 |
| Maker | TEA Group (Signa, Florence, Italy) / CNR-IBE |
| Connectivity | Cellular (GPRS/3G/4G); SD card; TX/RX serial pins |
| Sensors | PM2.5, PM10, NO₂, O₃, CO, CO₂, temperature, humidity, VOC |

Full board identification, internal layout, wiring diagrams, adapter recommendations, LED diagnostics, and pin markings are in [`docs/HARDWARE.md`](docs/HARDWARE.md).

## Key files

| Path | Role |
|------|------|
| `app.py` | Flask app and JSON API routes |
| `airqino_client.py` | AirQino cloud API client with OAuth2 token management |
| `serial_reader.py` | Threaded serial reader and multi-format line parser |
| `templates/dashboard.html` | Dashboard UI template |
| `static/js/dashboard.js` | Front-end logic: AQI coloring, charts, toggles, map, upload |
| `static/css/dashboard.css` | Dark theme and AQI color classes |
| `docs/HARDWARE.md` | Hardware connection guide for the REV6 board |
| `.env.example` | Configuration template |

## Configuration reference

| Variable | Purpose |
|----------|---------|
| `AIRQINO_CLIENT_ID` / `AIRQINO_CLIENT_SECRET` | OAuth2 client credentials |
| `AIRQINO_USERNAME` / `AIRQINO_PASSWORD` | OAuth2 user credentials |
| `AIRQINO_STATION_NAME` | API station name (`SMART###`) |
| `AIRQINO_PROJECT_NAME` | API project name |
| `SERIAL_PORT` | Serial device path for the USB-to-TTL adapter |
| `SERIAL_BAUD` | Serial baud rate (default `9600`) |
| `FLASK_SECRET_KEY` | Flask session secret |
