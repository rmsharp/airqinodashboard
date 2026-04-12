# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK
**Task:** Create README.md for the AirQino dashboard project
**Status:** Ready — hardware findings now documented, incorporate into README
**Plan:** Write a comprehensive README covering setup, usage, data source configuration (API/serial/CSV), device info, and project context
**Priority:** HIGH

### What You Must Do
Create `README.md` at the project root. It should cover:
- Project description (monitoring dashboard for AirQino air quality sensors)
- The user's specific context: abandoned AirQino Outdoor device (PN 800506, S/N AIRO 6153) from a discontinued project
- Installation: `pip install -r requirements.txt`, `python3 app.py`, open `http://localhost:5001`
- Data source configuration for all three paths — reference `docs/HARDWARE.md` for serial connection details
- Dashboard features: AQI-colored readings, time-series charts, sensor toggles, map, metadata
- AirQino API reference (base URL, key endpoints, OAuth2 flow)
- Device hardware summary (REV6 custom PCB by Quantit, NOT standard Arduino Mega — link to `docs/HARDWARE.md` for full details)
- Key files: `app.py`, `airqino_client.py`, `serial_reader.py`, `templates/dashboard.html`, `docs/HARDWARE.md`

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### Session 1 Handoff Evaluation (by Session 2)
- **Score: 8/10**
- **What helped:** Device identification (PN 800506, S/N AIRO 6153), the three data paths listed clearly, key file paths with line numbers, gotchas about API returning empty `{}` for 401s and station name mapping. All of this saved significant ramp-up time.
- **What was missing:** Session 1 described the device as "Arduino Mega + SIM900 GPRS" based on research papers about older revisions. The actual REV6 board (gen-2022, by Quantit) is a custom PCB with no USB port — this is a critical hardware difference that couldn't be known without opening the device. Not a fault of Session 1, but worth noting: literature-based hardware assumptions need physical verification.
- **What was wrong:** "USB serial — physically connect to Arduino Mega USB port" was listed as a data path, but there is no USB port on the REV6 board. The correct path is USB-to-TTL adapter wired to the board's TX/RX pins.
- **ROI:** Yes — the handoff gave strong context and the serial reader code was already written correctly for the actual serial data format. The gap was hardware-specific, not code-specific.

### What Session 2 Did
**Deliverable:** Hardware investigation and documentation update (COMPLETE)
**Started:** 2026-04-12
**Status:** Complete

**What was done:**
- Investigated user's report that no USB connection was visible inside the AirQino device
- Researched AirQino hardware extensively via web: user manual (Scribd/PlanetWatch), TEA Group catalog, Snap4City docs, ResearchGate papers, Clean Air Stars specs, PlanetWatch setup guides
- Key discovery: the AirQino REV6 (gen-2022) is a **custom PCB by Quantit** — NOT a standard Arduino Mega 2560. The USB-B port was eliminated in this board revision.
- User provided detailed board inspection: 2 large boards + 1 cellular module, markings include "AirQino REV6 gen-2022 www.quantit.it AIRQino MN-PW 11-2021 Rev6 Net Rev3.11", TX/RX pins visible, GPS module, antenna (1595)
- Created `docs/HARDWARE.md` — comprehensive hardware connection guide with board identification, internal layout, wiring diagrams, adapter recommendations (with verified in-stock links), LED diagnostics, pin markings, specifications, and references
- Updated `serial_reader.py` module docstring — changed from "USB serial connection" to USB-to-TTL adapter instructions with wiring
- Updated `.env.example` — serial config comments now reflect REV6 reality (no USB port, adapter required, correct example port name)
- Researched and recommended USB-to-TTL adapters: DSD TECH SH-U09C5 (FTDI, ~$12), SparkFun DEV-09873 ($14.95), DSD TECH CP2102 (~$8)
- Added dupont jumper wire requirement to HARDWARE.md per user feedback

**Commits:** (pending — will commit during close-out)

**Key files:**
- `docs/HARDWARE.md:1-161` — NEW: complete hardware connection guide
- `serial_reader.py:1-14` — updated module docstring with REV6 connection instructions
- `.env.example:11-17` — updated serial config comments

**Gotchas:**
- The AirQino REV6 TX/RX pins are likely 3.3V logic level (board shows 3.0V and 3.4V rails). Always set USB-to-TTL adapter to 3.3V, not 5V.
- Baud rate is assumed 9600 (standard Arduino default) — may need adjustment when adapter arrives and is tested.
- The board's TX/RX pin header type (male/female) is unconfirmed — user should verify when adapter arrives to ensure correct jumper wire gender.
- SD card slot location is still unknown — may be between stacked boards or on underside.
- Quantit website (www.quantit.it) returned ECONNREFUSED — may be defunct or temporarily down. No documentation found from them directly.

**Self-assessment:**
- **Score: 7/10**
- (+) Thorough hardware research across multiple sources — manual, academic papers, product listings, setup guides — to piece together the REV6 board reality
- (+) Correctly identified that the board has no USB port and pivoted to the right solution (USB-to-TTL adapter)
- (+) User's detailed board inspection was the breakthrough; incorporated all their observations into documentation
- (+) Found and verified in-stock adapter options after the initial recommendation (Adafruit #4364) was out of stock
- (+) Responsive to user feedback — added dupont wire requirement when user pointed out the gap
- (-) Initial research agent was rejected by user; could have started with direct web searches instead
- (-) First adapter recommendation (Adafruit #4364) was out of stock — should have verified availability before recommending
- (-) Session pivoted from the queued README task to hardware investigation — correct prioritization (user had a blocking hardware question), but README still not created
- (-) Could not access several key sources (ResearchGate figures blocked, Scribd content inaccessible, Snap4City corrupted rendering)

**Previous session handoff evaluation:** See "Session 1 Handoff Evaluation" above.

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
