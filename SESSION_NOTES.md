# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** Open. Session 4 delivered `README.md`. Next session picks from Open items below.
**Status:** Methodology PR #25/#27 remediation — **PART 1 COMPLETE & committed (`1e99b42`)**; **PART 2 DEFERRED** until PR #25/#27 merge upstream on `KJ5HST/main` (option b — see Item A). **Item B (README.md) COMPLETE** (Session 4).

### Open items — next session picks ONE (1-and-done)

**Item A — PART 2: re-vendor methodology v2.1 → current  [DECISION: option (b) DEFER; NOT actionable until upstream merge]**
- **Decision (corrected out-of-session 2026-06-08): option (b) — DEFER until PR #25/#27 merge upstream.** Supersedes Session 3's option (a). Reason: the option-(a) prerequisite (a local `integration/pr2527` branch) **never existed and was never built**, and PART 1 already secured the only at-risk data (the 2 learnings, now in `CLAUDE.md`), so deferring costs nothing. A full-tree re-vendor is cleanest done ONCE from a stable, merged canonical.
- **Trigger to make this actionable again:** PR #25 + PR #27 merge into `KJ5HST/main` (they are OPEN there as of 2026-06-08, filed from `rmsharp:fix/3c-learnings-destination` and `rmsharp:fix/claude-md-learnings-overflow` — they are NOT local PRs on the `rmsharp` fork, which is why `gh pr view 25/27` does not resolve here). Until that merge happens, do not pick this item up.
- **When unblocked:** sync `origin/main` from upstream, then re-vendor airqino from `origin/main` in one pass — the PR-25/27 wording (3C body, caption, `HOW_TO_USE.md` bullet) arrives for free, no hand-patching.
- **Procedure:** corrected brief PART 2 "Re-vendor procedure" steps 1–6 in `docs/planning/methodology-pr2527-remediation-airqino.md` (corrected `a5fdd12`). Overwrites `SESSION_RUNNER.md`, `SAFEGUARDS.md`, `methodology_dashboard.py`, and `docs/methodology/`. **Do NOT overwrite `SESSION_NOTES.md`.** The 2 airqino learnings are already safe in `CLAUDE.md` (PART 1), so the overwrite of SESSION_RUNNER.md is non-destructive.

**Item B — README.md  [✅ DONE — Session 4, commit pending close-out]**

~~Create `README.md` at the project root.~~ Delivered Session 4 at `/Users/rmsharp/Development/airqino/README.md`, written from a read of the actual implementation files (not just this spec). Original spec retained below for reference:
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

### Session 3 Handoff Evaluation (by Session 4)
- **Score: 9/10**
- **What helped:** The Item B (README) spec was effectively a ready-made checklist — project description, the data-path summary, install steps, API reference, hardware summary, and the exact key-file list all transferred almost verbatim into the README's section structure. Key files were given with line numbers. The gotcha that `docs/HARDWARE.html` is untracked-and-leave-it told me exactly what NOT to touch. The "Connecting a Live Data Source" block fed the README's data-source section directly. All 6 minimum handoff requirements were met.
- **What was missing:** Nothing material for this session's deliverable. Session 3 documented both open items thoroughly enough that picking Item B required zero discovery.
- **What was wrong:** Session 3's PART 2 recommendation (option a, re-vendor now) was superseded out-of-session by option b (DEFER) — the option-(a) prerequisite (`integration/pr2527` branch) never existed. To Session 3's credit, it explicitly flagged that exact blocker ("no integration branch; PRs #25/#27 don't resolve") and said to confirm before building, so the reversal was a refinement of a risk Session 3 already surfaced — not an inaccuracy it hid.
- **ROI:** Strongly positive. The README spec saved the bulk of the planning work; I spent my time reading implementation files for accuracy rather than figuring out what to write.

### What Session 4 Did
**Deliverable:** Root `README.md` (Item B) — **COMPLETE**
**Started / Closed:** 2026-06-08

**What was done:**
- **Bookkeeping first (per user):** (1) committed the out-of-session correction to `docs/planning/methodology-pr2527-remediation-airqino.md` on its own as `a5fdd12` (PART 2 reclassified to DEFER — the `integration/pr2527` branch never existed); (2) verified the claim before committing — Phase 0 `git status` showed a clean tree, so I re-ran `git status` and confirmed the file was genuinely modified out-of-session. (3) Reclassified Item A (PART 2 re-vendor) in this file from **BLOCKED → DEFERRED** so it stops surfacing as actionable.
- **Deliverable:** Wrote `README.md` from a direct read of `app.py`, `airqino_client.py`, `serial_reader.py`, `.env.example`, `requirements.txt`, `static/js/dashboard.js`, `templates/dashboard.html`, and `docs/HARDWARE.md` — not from the handoff description. Covers: project background (abandoned PN 800506 / S/N AIRO 6153 device), quick start, all three data sources (CSV/SD, cloud API, serial), feature list, full API endpoint + Flask route tables, hardware summary, key-file map, and a config-variable reference.
- **Left `docs/HARDWARE.html` untouched** (per user — separate decision).

**Verification:**
- `app.py` confirms port **5001**, host `0.0.0.0`, env var names, and route list → README matches.
- API base/token URLs, endpoint paths, and the 30-day/CSV/401-empty quirks taken verbatim from `airqino_client.py`.
- Sensor units and chart ranges (6h/12h/24h/3d/7d/30d) taken from `static/js/dashboard.js` and `templates/dashboard.html`.

**Commits:**
- `a5fdd12` — docs: correct airqino PART 2 — defer re-vendor until PR #25/#27 merge (no integration branch)
- (close-out commit for README + SESSION_NOTES + CLAUDE.md follows this note)

**Key files:**
- `README.md` — NEW, the deliverable
- `CLAUDE.md:34` — added project learning #3 (factual corrections must be grepped across ALL surfaces)
- `docs/planning/methodology-pr2527-remediation-airqino.md` — corrected (committed `a5fdd12`)

**Gotchas for the next session:**
- **Stale UI copy (NOT fixed — deliberate scope hold):** `templates/dashboard.html:54-55` still tells the user to "connect a USB cable to the Arduino Mega port" — the pre-Session-2 hardware claim that Session 2 corrected everywhere else (`serial_reader.py`, `.env.example`, `docs/HARDWARE.md`). This is the setup-banner "USB Serial" option. A good, bounded next deliverable: fix that banner text to match the USB-to-TTL/REV6 reality. (Logged as CLAUDE.md project learning #3.)
- **PART 2 is DEFERRED, not actionable:** do not pick up Item A until PR #25/#27 merge into `KJ5HST/main`. See Item A for the trigger and the one-pass re-vendor procedure.
- `docs/HARDWARE.html` is still untracked and still undecided (track / ignore / delete?) — Session 4 left it alone per instruction, same as Session 3.
- Branch `chore/methodology-pr2527-remediation` is not merged to `main` or pushed. No push was requested.

**Self-assessment:**
- **Score: 9/10**
- (+) Verified the out-of-session edit before committing instead of trusting the description — caught that my own Phase 0 snapshot was stale and confirmed against a fresh `git status`.
- (+) Wrote the README from the actual code, so endpoint names, env vars, port, sensor units, and chart ranges are accurate rather than paraphrased from the handoff.
- (+) Held the line on scope: spotted the stale `dashboard.html` Arduino text but did NOT fix it (FM #8) — flagged it as a clean next-session deliverable and logged the root-cause learning instead.
- (+) Did the bookkeeping in the exact order requested, committed the correction as its own logical unit, and left `HARDWARE.html` untouched.
- (-) Did not boot the Flask app to confirm it serves (it's a blocking debug server); relied on reading `app.py`. The install/run steps are standard, but a runtime smoke test would have been stronger evidence.

**Previous session handoff evaluation:** See "Session 3 Handoff Evaluation (by Session 4)" above.

### Session 2 Handoff Evaluation (by Session 3)
- **Score: 8/10**
- **What helped:** Session 2's handoff was thorough and well-structured — all 6 minimum requirements met (ACTIVE TASK, what-was-done with file paths, gotchas, self-assessment written to file). Critically for *this* session, it clearly documented the two airqino-specific learnings (REV6 hardware verification; adapter availability) both in prose and in the SESSION_RUNNER.md Learnings table. That made PART 1 (preserve those exact 2 learnings verbatim) trivial to execute and verify — I could confirm byte-for-byte what to move.
- **What was missing:** Nothing Session 2 could have provided. This session's task (methodology PR #25/#27 remediation) came from an external brief generated 2026-06-07, ~2 months after Session 2 (2026-04-12). The handoff's ACTIVE TASK pointed at README.md, which was correct at the time but got superseded by the user's redirect — not a handoff defect.
- **What was wrong:** Nothing inaccurate. The learnings text in SESSION_RUNNER.md matched the handoff exactly.
- **ROI:** Positive. The documented learnings were the literal payload of PART 1; having them already clean and table-formatted saved verification time. The general quality bar was high and worth reading in full.

### What Session 3 Did
**Deliverable:** Methodology PR #25/#27 remediation — PART 1 (CLAUDE.md receptacle + preserve 2 learnings inline) — **COMPLETE**
**Started:** 2026-06-07 · **Closed:** 2026-06-08
**Governing doc:** `docs/planning/methodology-pr2527-remediation-airqino.md`

**What was done:**
- Branched `chore/methodology-pr2527-remediation` off `main` (brief Step 0), wrote Phase 1B claim stub.
- **CLAUDE.md:** appended the "Project-Specific Methodology Adaptations" receptacle (verbatim from brief PART 1 Step 1), with airqino's 2 learnings inline (renumbered 1–2). Inline table chosen over a separate `PROJECT_LEARNINGS.md` because the corpus is tiny (2 rows), per the brief.
- **SESSION_RUNNER.md:** removed Learnings rows 2–3 (the airqino rows), keeping only row 1 (the canonical FM #19 plan-mode seed). De-duplicates now; harmless to PART 2 which overwrites the file.
- **Committed PART 1** as `1e99b42` (CLAUDE.md + SESSION_RUNNER.md + the governing brief, for traceability).
- **Made the PART 2 timing decision: option (a)** — see ACTIVE TASK Item A above for the full rationale, prerequisite, and caveat. PART 2 was NOT executed (1-and-done; it is a separate, prerequisite-blocked deliverable).

**Verification (all passed — brief PART 1 criteria):**
- `grep -n '@' CLAUDE.md` → no `@`-import (learnings are inline, not imported). ✓
- `SESSION_RUNNER.md` Learnings table → only the seed row remains (line 268); 0 matches for the airqino learnings text. ✓
- `CLAUDE.md` → both airqino learnings present verbatim (2 matches). ✓

**Commits:**
- `1e99b42` — chore: methodology PR #25/#27 remediation PART 1 — CLAUDE.md receptacle
- (close-out handoff commit follows this note)

**Key files:**
- `CLAUDE.md:14-38` — NEW receptacle ("Project-Specific Methodology Adaptations") with the 2 learnings inline
- `SESSION_RUNNER.md:268` — Learnings table, now seed row only
- `docs/planning/methodology-pr2527-remediation-airqino.md` — the governing brief (committed this session)

**Gotchas for the next session:**
- **PART 2 is decided (option a) but prerequisite-blocked:** `~/Development/methodology` has no `integration/pr2527` branch yet, and PRs #25/#27 don't resolve on the `rmsharp/methodology` remote. Resolve the PR location/state and build the integration branch BEFORE attempting the re-vendor. (Details: ACTIVE TASK Item A.)
- When PART 2 runs, it overwrites `SESSION_RUNNER.md`/`SAFEGUARDS.md`/`methodology_dashboard.py`/`docs/methodology/`. **The 2 learnings are already safe in `CLAUDE.md`** — that's the whole point of PART 1 preceding PART 2. Do NOT overwrite `SESSION_NOTES.md`.
- Untracked file `docs/HARDWARE.html` predates this session (left from prior hardware work) — I did NOT touch or commit it. Confirm with the user whether it should be tracked, ignored, or deleted.
- This branch (`chore/methodology-pr2527-remediation`) is not yet merged to `main` or pushed. User did not request a push.

**Self-assessment:**
- **Score: 9/10**
- (+) Followed the protocol end-to-end: oriented (read SAFEGUARDS/SESSION_RUNNER/brief in full), reported findings, claimed the session (stub), branched before touching files, executed exactly PART 1, verified against the brief's criteria, committed, closed out.
- (+) Held the "1-and-done" line: did PART 1 only, did NOT bleed into PART 2 (FM #18). Made the (a)/(b) decision as asked and teed PART 2 up cleanly rather than starting it.
- (+) Evidence-based PART 2 decision: actually inspected the methodology repo and PR state instead of just echoing the brief's default — surfaced the real prerequisite blocker (no integration branch; PRs unresolvable).
- (+) Kept the PART 1 commit a clean logical unit; left the unrelated untracked file alone (SAFEGUARDS blast-radius discipline).
- (-) Did not strictly "STOP and wait" after the Phase 0 report before acting — proceeded into PART 1 since the user's instruction was explicit and bounded. Justified, but a stricter reading of Phase 0 step 8 would pause first.

**Previous session handoff evaluation:** See "Session 2 Handoff Evaluation" above.

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
