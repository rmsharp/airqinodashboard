# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK
**Task:** Create README.md for the AirQino dashboard project
**Status:** Ready
**Plan:** Write a comprehensive README covering setup, usage, data source configuration (API/serial/CSV), device info, and project context
**Priority:** HIGH

### What You Must Do
Create `README.md` at the project root. It should cover:
- Project description (monitoring dashboard for AirQino air quality sensors)
- The user's specific context: abandoned AirQino Outdoor device (PN 800506, S/N AIRO 6153) from a discontinued project
- Installation: `pip install -r requirements.txt`, `python3 app.py`, open `http://localhost:5001`
- Data source configuration for all three paths (API credentials in `.env`, USB serial, CSV/SD card upload)
- Dashboard features: AQI-colored readings, time-series charts, sensor toggles, map, metadata
- AirQino API reference (base URL, key endpoints, OAuth2 flow)
- Device hardware details (Arduino Mega, SIM900 GPRS, sensor list)
- Key files: `app.py`, `airqino_client.py`, `serial_reader.py`, `templates/dashboard.html`

Also still pending: help the user connect a live data source. Three paths:
1. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
2. **USB serial** — physically connect to Arduino Mega USB port, set `SERIAL_PORT` in `.env`
3. **CSV upload** — extract SD card or export data, upload via dashboard UI

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 1 Did
**Deliverable:** AirQino environmental monitoring dashboard (COMPLETE)
**Started:** 2026-04-11
**Status:** Dashboard fully built and tested with sample CSV data

**What was done:**
- Researched AirQino API thoroughly: all endpoints require OAuth2 via Keycloak (`airqino-api.magentalab.it`), confirmed with live 401 tests
- Identified device: PN 800506 = AirQino Air Aware Outdoor (TEA Group / CNR-IBE), Arduino Mega + SIM900 GPRS cellular, no WiFi/local web interface
- Built Flask web dashboard with three data source backends:
  - AirQino cloud API client with OAuth2 token management (`airqino_client.py`)
  - USB serial reader for direct device connection (`serial_reader.py`)
  - CSV file upload for SD card data
- Dashboard features: real-time readings with EPA AQI color coding, interactive Chart.js time series (6h/12h/24h/3d/7d/30d ranges), sensor toggle pills (PM2.5, PM10, NO₂, CO, O₃, CO₂, Temp, Humidity, VOC), Leaflet map with dark tile layer, device metadata panel, drag-and-drop CSV upload
- Tested all endpoints with sample CSV data — current values, time series, and upload all working

**Key files:**
- `app.py:1-170` — Flask app, all routes (`/`, `/api/status`, `/api/current`, `/api/timeseries`, `/api/hourly`, `/api/metadata`, `/api/stations`, `/api/upload_csv`)
- `airqino_client.py:1-120` — OAuth2 + all AirQino API endpoints (getStations, getCurrentValues, getRange, getHourlyAvg, getStationHourlyAvg, etc.)
- `serial_reader.py:1-120` — Threaded serial reader with multi-format line parser (JSON, key=value, semicolon-delimited)
- `templates/dashboard.html:1-130` — Main UI template, CDN imports for Chart.js, Leaflet, chartjs-adapter-date-fns
- `static/js/dashboard.js:1-310` — Client logic: AQI thresholds, chart rendering, sensor toggles, CSV upload, auto-refresh (60s polling)
- `static/css/dashboard.css:1-230` — Dark theme, AQI color classes, responsive grid
- `.env.example` — Configuration template with all env vars documented
- `requirements.txt` — flask, requests, python-dotenv, pyserial

**Gotchas:**
- AirQino API returns empty `{}` for all 401s (no helpful error message) — the client will raise on HTTP status
- Device uses SIM900 cellular (2G GPRS), NOT WiFi — no local web interface exists
- Serial number `AIRO 6153` does NOT map directly to the `SMART###` station name used in the API — must ask AirQino for the mapping
- `getHourlyAvg` returns CSV (not JSON), needs `?pivot=true` for a usable format
- `getRange` has a 30-day max limit per request
- The methodology_dashboard.py in the project root is from the scaffolding framework, NOT part of this app

**Self-assessment:**
- **Score: 7/10**
- (+) Thorough API research before building — discovered auth requirements, device hardware constraints, and all available endpoints
- (+) Dashboard works end-to-end with CSV upload flow
- (+) Clean dark UI with proper AQI color coding
- (-) Could not verify browser rendering of charts/map (no screenshot capability), only tested API responses via curl
- (-) The fundamental blocker (no API credentials) means the user can't use the primary data path yet

**Previous session handoff evaluation:** N/A — this is Session 1.
