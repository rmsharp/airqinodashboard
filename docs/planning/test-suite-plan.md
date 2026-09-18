# Test Suite Plan: airqino dashboard

**Status:** plan, awaiting operator approval before Phase 1 starts. It is a draft until approved.
**Written:** Session 9, 2026-09-17, on branch `docs/test-suite-plan` off `main` `15b0a3f`.
**Governing docs:** `SESSION_RUNNER.md` §Planning Sessions and
`docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md`.
**Implementation:** four sessions, one per phase, then separate fix sessions for the defects in §4. This plan
does not implement anything. The plan is the whole deliverable (failure mode #18).

---

## 1. Context

**Problem.** The project has no automated tests. The dashboard's only HIGH risk is "No test infrastructure"
(`methodology_dashboard.py:3261-3262`, health 54/100 on `15b0a3f`). Two recent fixes have no guard:

- the setup-banner hardware copy (Session 7, `e5f52e1`; `CLAUDE.md` learning #3 records how it went stale once);
- the REV6 "no USB port" wording, which exists in several places (learning #3).

The serial path is about to be used for the first time. The operator is sourcing a USB-to-TTL adapter
(`SESSION_NOTES.md`, "Connecting a Live Data Source"), and the probes below found two serial defects that would show
up on the first hookup (D1, D7).

**Constraints.**

- Tests must not change product code. Fixes are separate sessions (operator decision, §2).
- A `.env` file must not leak into tests. `app.py:12` calls `load_dotenv()` at import time, and python-dotenv 1.2.1
  searches upward from `app.py`'s directory to `/`, so a `.env` in the repo root *or any parent directory* is read.
  Under a tracer such as coverage, the search starts from the current directory instead. No `.env` exists today, but
  the operator will create one when the adapter or the API credentials arrive.
- There are no real API credentials and no serial hardware. Every external boundary has to be faked, and the plan
  names what each fake cannot prove (§5).
- The 5-file cap applies per commit (`SAFEGUARDS.md` §Blast Radius Limits), counting the `CHANGELOG.md` entry
  that rides each commit.

**Current state (measured on `15b0a3f`):**

- There are no `tests/`, `conftest.py`, `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini` or
  `requirements-dev*.txt` files, and no pytest or unittest import in the product code. Checked with `find` and
  `git grep`.
- `requirements.txt:1-4` lists flask, requests, python-dotenv and pyserial.
- `.quality-gates.json` declares `"gates": []`.
- The toolchain on the operator's machine is Python 3.10.12 (miniforge base env), pytest 9.0.2, Flask 3.1.3,
  Werkzeug 3.1.8, python-dotenv 1.2.1, requests 2.31.0 and pyserial 3.5. pytest-cov 7.1.0, anyio, pytest-asyncio
  and langsmith are also installed as global pytest plugins.
- `README.md:13` says "Requires Python 3.9+", but pytest 9 requires Python ≥3.10 (its `Requires-Python`).

## 2. Decisions (operator-approved in Session 9's picker)

| # | Decision | Chosen | Main reason |
|---|----------|--------|-------------|
| 1 | Framework | **pytest** | Already installed. Fixtures, `monkeypatch`, `parametrize` and strict xfail carry the whole design. `requirements-dev.txt` says `pytest>=8` so that Python 3.9 still resolves (to 8.x). |
| 2 | Known defects | **Strict xfail; fix later** | Each defect gets a test of the *minimal correct* behaviour, marked `xfail`. With `xfail_strict = true`, a fix makes that test XPASS, which fails the suite until the marker is removed. So a fix can't land unguarded, and a marker can't outlive its bug. |
| 3 | Faking HTTP | **monkeypatch fakes** | Replace `airqino_client.requests` and `airqino_client.time` with recording fakes. This adds no dependency and pins URLs, params, headers and token timing exactly. |
| 4 | Scope | **Python only** | JS, CI, a coverage floor and live tests are deferred, with reasons in §8. |

## 3. Grep-based inventory

These are the search results the phases are built from. Commands: `grep -n "^def \|^    def \|^class \|@app.route"`,
`grep -n "os.getenv\|load_dotenv"`, `grep -n "global \|^_[a-z_]* = "`, `grep -n "requests\.\(get\|post\)\|serial\.Serial\|threading\.\|time\.time\|time\.sleep\|datetime\.\(utcnow\|now\)"`
over `app.py airqino_client.py serial_reader.py`, and `grep -n "fetch\(JSON\)\?('/api" static/js/dashboard.js`.

### 3.1 Units under test

| Unit | Location | Phase |
|------|----------|-------|
| `dashboard()` `GET /` | `app.py:64-72` | P1 |
| `active_source()` | `app.py:51-59` | P1 (page), P4 (D5, D6) |
| `api_status()` `GET /api/status` | `app.py:75-88` | P2, P4 |
| `upload_csv()` `POST /api/upload_csv` | `app.py:235-272` | P2 |
| `api_current()` `GET /api/current` (serial → API → CSV) | `app.py:137-165` | P2 (none, CSV), P3 (serial), P4 (API) |
| `api_timeseries()` `GET /api/timeseries` | `app.py:168-210` | P2, P3, P4 |
| `api_stations()` `GET /api/stations` | `app.py:91-104` | P2 (503), P4 |
| `api_metadata()` `GET /api/metadata` | `app.py:107-134` | P2 (503), P4 |
| `api_hourly()` `GET /api/hourly` | `app.py:213-232` | P2 (503), P4 |
| `get_api_client()` (lazy import, needs all 4 credential vars) | `app.py:24-35` | P4 |
| `get_serial_reader()` (starts a real thread) | `app.py:38-48` | P3 |
| `SerialReader`: `__init__`, `start`, `stop`, `_read_loop`, `_parse_line`, `_normalize`, `get_current`, `get_history` | `serial_reader.py:38`, `:47`, `:54`, `:62`, `:89`, `:140`, `:154`, `:158` | P3 |
| `AirQinoClient`: `_get_token`, `_do_refresh`, `_headers`, `_get` | `airqino_client.py:21`, `:49`, `:63`, `:66` | P4 |
| `AirQinoClient` public methods used by `app.py` (7): `get_stations`, `get_session_info`, `get_sensors`, `get_current_values`, `get_last_station_data`, `get_range`, `get_hourly_avg` | `airqino_client.py:74-123` | P4 |
| `AirQinoClient` public methods not used by `app.py` (4): `get_last_values_raw`, `get_single_day`, `get_station_hourly_avg`, `generate_report` | `airqino_client.py:92`, `:111`, `:125`, `:137` | P4 (they pin the URL shapes `README.md`'s API table documents) |

**Front-end consumers.** `static/js/dashboard.js` calls four endpoints: `/api/current` (`:145`),
`/api/timeseries?hours=` (`:154`), `/api/metadata` (`:163`) and `/api/upload_csv` (`:434`). `/api/status`,
`/api/stations` and `/api/hourly` have no front-end caller, so they are tested for their JSON contract only.

### 3.2 Test-isolation surface (every test must control these)

- **Environment reads (9 variables).** `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`,
  `AIRQINO_PASSWORD` (`app.py:28-31`, `:53`); `SERIAL_PORT`, `SERIAL_BAUD` (`:42-43`, `:55`, `:81`);
  `AIRQINO_STATION_NAME`, `AIRQINO_PROJECT_NAME` (`:66-67`, `:79-80`, `:97`, `:113-114`, `:152`, `:188`, `:219`);
  `FLASK_SECRET_KEY` (`:15`, read once at import, so tests don't need to touch it).
- **Import-time side effect.** `load_dotenv()` at `app.py:12` (see §1, Constraints).
- **Module globals.** `_api_client`, `_serial_reader` and `_csv_data` (`app.py:19-21`) persist across requests,
  and so across tests.
- **External I/O and clocks:**
  - `requests.post` at `airqino_client.py:34`, `:50`, `:140`;
  - `requests.get` at `:67`, `:118`;
  - `time.time` at `:22`, `:45`, `:59`;
  - `serial.Serial` at `serial_reader.py:65`, imported inside the thread at `:63`;
  - `threading.Thread` at `:51`;
  - `datetime.now` at `serial_reader.py:82`;
  - `datetime.utcnow` at `app.py:196-197` and `:223-224`.

### 3.3 Files this plan creates or modifies (and the ones it must not)

| File | Phase | Change |
|------|-------|--------|
| `requirements-dev.txt` | P1 | new: `-r requirements.txt` and `pytest>=8` |
| `pytest.ini` | P1 | new (content in §5, P1) |
| `tests/conftest.py` | P1, then P3 and P4 add fakes | new |
| `tests/test_dashboard_page.py` | P1 | new |
| `tests/test_csv_routes.py` | P2 | new |
| `tests/test_serial_reader.py`, `tests/test_serial_routes.py` | P3 | new |
| `tests/test_airqino_client.py`, `tests/test_api_routes.py` | P4 | new |
| `.gitignore` | P1 | add `.pytest_cache/` |
| `README.md` | P1 | a "Running tests" subsection after Quick start (`:11-23`), and a `tests/` row in Key files (`:131-142`) |
| `.quality-gates.json` | P1 declares two gates; P2–P4 tighten `tests-passed` | edit `"gates"` |
| `CHANGELOG.md`, `SESSION_NOTES.md`, `HANDOFFS.md` | every session | the usual session records |
| **Not touched:** `app.py`, `airqino_client.py`, `serial_reader.py`, `templates/`, `static/`, `requirements.txt` | all phases | Product code changes only in fix sessions (§6) |

## 4. Defects found while researching this plan

Each one was reproduced in Session 9 by a scratch probe against `15b0a3f`: `_parse_line` called directly, and the
routes driven through Flask's test client. They are facts, not suspicions. Each becomes a strict-xfail test in the
phase listed, asserting only the *minimal* correct behaviour, so the fix session keeps its design freedom.

| ID | Defect (file:line) | Repro → observed | User impact | xfail assertion | Phase |
|----|--------------------|------------------|-------------|-----------------|-------|
| D1 | The serial `key=value` parser splits on `;` **and then** on `,`. The `,` pass re-reads a `;`-joined line as a single pair and overwrites the first key (`serial_reader.py:106-117`) | `_parse_line("co=235;no2=17;o3=17;pm10=25;pm25=13")` → `{'co': '235;no2=17;o3=17;pm10=25;pm25=13', 'no2': 17.0, …}`. This is the docstring's own example format (`:94`). Comma-separated lines parse correctly. | The first sensor becomes a string. The readings grid keeps numbers only (`dashboard.js:198`), so CO would silently vanish on a real serial hookup. | `_parse_line("co=235;no2=17")["co"] == 235.0` | P3 |
| D2 | `int()` on a query parameter without validation: `hours` (`app.py:171`) and `days` (`:220`) | `GET /api/timeseries?hours=abc` → 500 `ValueError`, even with no source configured. `/api/hourly?days=abc` returns 500 in API mode. | A crafted or mistyped URL returns 500 instead of 400. | `status_code < 500`, once for timeseries and once for hourly | P2 (timeseries), P4 (hourly) |
| D3 | A CSV row with more fields than the header. `csv.DictReader` puts the extras under the key `None`, and `k.strip()` fails on it (`app.py:258-261`) | Uploading `a,b\n1,2,3\n` → 500 `AttributeError: 'NoneType' object has no attribute 'strip'` | One ragged row in an SD-card export fails the whole upload with a 500. | `status_code < 500` | P2 |
| D4 | A UTF-8 byte-order mark is kept in the first header (`app.py:245` decodes with `utf-8`, not `utf-8-sig`) | Uploading `﻿timestamp,pm25\n…` → `columns[0] == '﻿timestamp'` | The chart reads `row.timestamp` (`dashboard.js:251`), so a BOM-prefixed CSV plots nothing. Excel's "CSV UTF-8" export writes a BOM. Whether the device's SD card does is unknown. | `columns[0] == "timestamp"` | P2 |
| D5 | `active_source()` reports `"api"` when only `AIRQINO_CLIENT_ID` is set (`app.py:53`), but `get_api_client()` needs all four credential variables (`:32`) | With only `AIRQINO_CLIENT_ID` set: the badge says "API Connected", the banner is hidden, and `/api/current` returns 503 "No data source configured" | A half-filled `.env` hides the setup help and claims a connection that doesn't exist. | `"API Connected"` not in `GET /` | P4 |
| D6 | The source order disagrees. `active_source()` is API → serial → CSV (`app.py:53-58`). The data routes use serial → API → CSV (`:141-163`, `:175-208`), and `README.md:27` documents serial → API → CSV. | With both sources configured, the badge says "API Connected" while `/api/current` serves serial data. | The badge contradicts the data shown. | `active_source() == "serial"` with both sources configured | P4 |
| D7 | A serial port that fails to open sets `latest = {"error": …}` (`serial_reader.py:64-69`), and `/api/current` returns it as data with **200** (`app.py:143-145`) | `SERIAL_PORT=/dev/does-not-exist` → first call 202 "No data received yet", then 200 `{"source": "serial", "data": {"error": "[Errno 2] could not open port …"}}` | The JS only reports errors on non-2xx responses (`dashboard.js:134-140`), so it shows "No readings available" and the port error never reaches the user. That is the first-hookup failure the operator is most likely to hit. | `status_code != 200` once the reader holds an error | P3 |

**Characterized, not flagged as defects.** These get plain passing tests, each with a comment that it is current
behaviour and not necessarily intended:

- An empty CSV upload returns 200 with 0 rows, *replaces* any earlier upload, and turns the source back to `None`.
- A short CSV row stores `None` for the missing fields.

**Suggested fix order (the operator's call).** D1 and D7 first, because the serial path is next in use. Then D3 and
D4 (the CSV/SD-card path, which `README.md:31` calls the fastest way to see data), then D6, D5 and D2. Each fix is one
session. It removes one `xfail` marker, and `tests-passed` tightens by one.

## 5. Phases

Every phase has the same shape:

- **One session.** Claim it (Phase 1B), write the tests, then close out and STOP.
- **Checkpoint commits** of at most 5 files each, `CHANGELOG.md` included.
- **Verification.** Run the whole suite, run the ratchet, **drive at least one new test red** by breaking the
  behaviour it guards in the working tree (learning #12: "watch it fail before trusting it"), then restore it and
  confirm `git diff --stat` shows no product file.
- **Record the red-drive** in the session notes.
- **Tighten** `tests-passed` in `.quality-gates.json` to the newly measured count. Tightening needs no approval;
  loosening does.

### Phase 1: Harness and the setup-banner guard

**Goal:** `pytest` runs, the isolation fixture is proven, and Session 7's banner fix gets its guard. The dashboard's
HIGH risk clears.

**`pytest.ini`** (verified in the Session 9 spike, §9):

```ini
[pytest]
testpaths = tests
pythonpath = .
xfail_strict = true
addopts = -ra
```

`pythonpath = .` makes plain `pytest` work as well as `python3 -m pytest`. `testpaths` keeps collection out of
`docs/methodology/`. `xfail_strict` is decision 2's enforcement.

**`tests/conftest.py`**, the load-bearing part (verified in the spike):

```python
import os
import pytest

import app as app_module

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
```

**Tests** (`tests/test_dashboard_page.py`):

- **T1.1 No source.** `GET /` returns 200 and contains "Connect Your AirQino", "Serial Adapter" and
  `docs/HARDWARE.md`. It contains none of "Arduino", "Mega", "USB cable", "USB Serial" or "USB-B" (case-insensitive).
  **Do not ban "USB port":** the correct text says "The REV6 board has no USB port" (`templates/dashboard.html:55`).
  The list comes from Session 7's surface grep (`arduino|mega|usb cable|usb port|usb-b|usb serial`), minus "usb port".
- **T1.2 Badge and placeholder.** The page contains the badge "No Data Source" and "Configure a data source to see
  readings" (`templates/dashboard.html:33`, `:76`). Assert on the badge markup (`>No Data Source<`). The bare phrase
  also appears in an HTML comment (`:40`), so a case-insensitive search counts 2.
- **T1.3 CSV source.** With `app._csv_data = [{...}]` set by `monkeypatch`: no banner, badge "CSV Data", and the
  "Import CSV Data" panel is present (`:127`).
- **T1.4 Serial source.** With `SERIAL_PORT` set: no banner, badge "Serial". This is safe because `dashboard()` only
  calls `active_source()`, which reads the environment, and never calls `get_serial_reader()`.
- **T1.5 API source.** With `AIRQINO_CLIENT_ID` and `AIRQINO_PROJECT_NAME` set: badge "API Connected", and the
  Project meta row shows the name (`:112`).
- **T1.6 Header.** Station and project set: the header reads "Station: X · Project: Y" (`:18-19`). Neither set: it
  falls back to "Device S/N: AIRO 6153".
- **T1.7 Guard the guard.** Inside a test, all 8 `CONFIG_VARS` are absent from `os.environ`, so a fixture edit
  that stops isolating fails loudly. `FLASK_SECRET_KEY`, the ninth variable, is read only at import.

**Wire-up:**

- `.gitignore` gains `.pytest_cache/`.
- `README.md` gets a "Running tests" subsection: `pip install -r requirements-dev.txt`, then `python3 -m pytest`.
  Note that the suite is verified on Python 3.10 only. The Key files table gets a `tests/` row.
- `.quality-gates.json` declares:

```json
{"name": "tests-exit", "direction": "max", "threshold": 0, "command": "python3 -m pytest -q",
 "why": "the suite exits 0 (strict xfails included)"},
{"name": "tests-passed", "direction": "min", "threshold": <measured>, "command": "python3 -m pytest -q",
 "extract": "(\\d+) passed", "unit": "tests", "why": "tests cannot be deleted silently; each fix session tightens it"}
```

Both gates share one command, so the ratchet runs pytest once (`quality_ratchet.py:266-270`, memo). Keep the word
"passed" out of xfail `reason=` strings: `-ra` prints those reasons in the output the regex scans.

**Commits:**

1. The claim.
2. `requirements-dev.txt`, `pytest.ini`, `tests/conftest.py`, `tests/test_dashboard_page.py`, `CHANGELOG.md`.
3. `.gitignore`, `README.md`, `.quality-gates.json`, `CHANGELOG.md`.
4. Close-out.

**DONE when:**

- `python3 -m pytest -q` and plain `pytest -q` both exit 0, with at least 7 passed and 0 xfailed.
- `python3 quality_ratchet.py --run` prints `2/2 pass`, and its summary line is cited in the receipt.
- The red-drives are recorded:
  - restoring the old banner wording ("Connect a USB cable to the Arduino Mega port.") in the working tree fails T1.1;
  - turning `autouse` off fails T1.7. The spike showed it also fails T1.1 when a `.env` is present.
- `git diff --stat main -- app.py airqino_client.py serial_reader.py templates static` is empty.
- `python3 methodology_dashboard.py` no longer lists "No test infrastructure".

**Expected dashboard result (computed, not guessed):**

- "Test coverage is very thin" (MEDIUM) replaces the HIGH risk, because the dashboard's source count is 5,475 lines
  (`methodology_dashboard.py:3263-3264`). The MEDIUM stays until the test files total at least 548 lines (0.1 × 5,475).
- 4,412 of those 5,475 source lines are vendored methodology tooling:
  - two 2,055-line dashboard copies, `docs/methodology/tools/` and `docs/methodology/starter-kit/`;
  - `docs/methodology/bin/tests.sh` (232 lines);
  - `docs/methodology/bin/_manifest.py` (70 lines).

  The product itself is 1,063 lines: `app.py` 277, `airqino_client.py` 149, `serial_reader.py` 161 and
  `dashboard.js` 476. **Do not pad tests to move this ratio.**
- `pytest.ini` also counts as a coverage config for the dashboard, worth +2 on the testing sub-score
  (`methodology_dashboard.py:2613-2621`).
- The overall health number is not predicted here. Measure it.

**Surface:**

- **Where it runs:** the operator's Mac, Python 3.10.12, through Flask's test client.
- **What it proves:** routing, Jinja rendering and the served HTML.
- **What it can't prove:**
  - the dev server (`app.run`);
  - the browser;
  - CDN assets;
  - `dashboard.js`.

  Learning #5's headless-Chrome screenshot is still the only check of the rendered page, and it stays manual.

**Session boundary:** Phase 1 is one session. Close out when it's done.

### Phase 2: No-source contract and the CSV path

**Goal:** every route's behaviour with no source, and the CSV upload path the README calls the fastest route to data.

**Tests** (`tests/test_csv_routes.py`):

- **T2.1** A parametrized table of the six GET routes with no source:
  - `/api/status` returns 200 with `{source: None, has_csv: False, station_name: "", project_name: "", serial_port: ""}`;
  - `/api/current` and `/api/timeseries` return 503 "No data source configured";
  - `/api/stations`, `/api/metadata` and `/api/hourly` return 503 "API not configured".
- **T2.2** An upload with no file part returns 400 "No file provided". An empty filename returns 400 "No file selected".
- **T2.3** Delimiter detection, parametrized over `;`, `\t` and `,`: the right `rows` count and `columns` list.
- **T2.4** Coercion:
  - numeric strings become `float`;
  - non-numeric values are stripped strings;
  - header keys are stripped and lower-cased (`" PM25 "` becomes `pm25`).
- **T2.5** Characterization: a short row stores `None`.
- **T2.6** After an upload:
  - `/api/status` shows source `csv` with `has_csv` true;
  - `GET /` shows badge "CSV Data" and no banner;
  - `/api/current` returns the **last** row;
  - `/api/timeseries` returns rows capped at the **last 500** (upload 501 rows and check both the length and the last
    row);
  - `?sensor=` keeps only the rows that have that key.
- **T2.7** Characterization: an empty upload returns 200 `{rows: 0, columns: []}` and the source goes back to `None`.
- **T2.8** Invalid UTF-8 bytes are replaced (`errors="replace"`) and the upload still returns 200.
- **xfail:** D2 (timeseries half), D3, D4.

**Commits:**

1. The claim.
2. `tests/test_csv_routes.py`, `.quality-gates.json` (tightened), `CHANGELOG.md`.
3. Close-out.

**DONE when:**

- The suite exits 0 with exactly 3 xfailed.
- The ratchet passes 2/2 with the tightened threshold.
- A red-drive is recorded: for example, remove `.lower()` at `app.py:261` in the working tree and watch T2.4 fail,
  then restore it.
- No product file shows in `git diff`.

**Surface:**

- **Where it runs:** Flask's test client with in-memory multipart uploads.
- **What it can't prove:** the browser's drag-and-drop and `FormData` (`dashboard.js:407-450`), and real SD-card
  files. **There is no real device CSV to use as a fixture.** Whether the SD card writes `;` or `,`, a BOM, or a
  `timestamp` column is unknown. When a real file exists, it becomes a fixture in its own session.

**Session boundary:** Phase 2 is one session.

### Phase 3: The serial path

**Goal:** the parser, the reader thread over a real pseudo-terminal, and the serial branches of the routes. D1 and D7
get their xfails.

**Tests** (`tests/test_serial_reader.py`):

- **T3.1** A parametrized `_parse_line` table:
  - a JSON object;
  - JSON with aliases (`pm2.5`, `Temperature`, `humidity`) normalized;
  - comma-separated `key=value`;
  - a 10-value numeric line mapped by `field_order` (`serial_reader.py:128-129`);
  - exactly 5 values;
  - 4 values, which gives `None`;
  - a non-numeric token in a numeric line, which gives `None`;
  - plain text, which gives `None`;
  - malformed JSON (`{"co": 1`), which gives `None`.
- **T3.2** `_normalize`:
  - every mapping key (`serial_reader.py:143-148`);
  - known fields lower-cased;
  - unknown keys keep their case (`"Foo"` stays `"Foo"`).
- **T3.3** `get_current()` returns `None` when empty and returns a **copy** (mutating the result leaves `latest`
  unchanged).
- **T3.4** `get_history(limit)` returns the last N. The deque drops the oldest past `history_size`.
- **T3.5** `start()` is idempotent: a second call keeps the same `_thread` object.
- **T3.6 End to end over a pty.** Open `os.openpty()`, then point `SerialReader(os.ttyname(slave))` at it. Real
  pyserial and termios run on that pseudo-terminal. Write `b"co=1.5,pm25=7\r\n"` and a garbage line to the master
  end, and poll until `get_current()` is set (2 s deadline, no fixed sleeps). Assert that:
  - the values are parsed;
  - `raw_line` has the CRLF stripped;
  - `timestamp` is an ISO string with a UTC offset;
  - the garbage line is absent from history.

  Mark it `skipif(not hasattr(os, "openpty"))`: the test is POSIX-only. It was verified on macOS (`/dev/ttys008`) in
  the Session 9 spike.
- **T3.7 Open failure.** Point it at `tmp_path / "no-such-port"` and poll until `latest` holds an `"error"` key and
  `_running` is `False`.

**Tests** (`tests/test_serial_routes.py`). Add a `FakeReader` fixture to `conftest.py` and inject it with
`monkeypatch.setattr(app_module, "_serial_reader", fake)`:

- **T3.8** `/api/current` returns 200 `{"source": "serial", "data": …}`. With no data yet, it returns 202 with
  "No data received yet".
- **T3.9** `/api/timeseries` returns the history with source `serial`. `?sensor=` returns rows reshaped to
  `{**row, "values": {sensor: value}}`, keeping only the rows that have the key (`app.py:178-182`).
- **xfail:** D1 in `test_serial_reader.py`; D7 in `test_serial_routes.py`. D7 uses the real `SerialReader` via
  `SERIAL_PORT=<tmp_path>/no-such-port`, so it also exercises `get_serial_reader()`. Poll `/api/current` until the
  202 turns into the error-carrying response.

**Commits:**

1. The claim.
2. `tests/test_serial_reader.py`, `tests/conftest.py`, `CHANGELOG.md`.
3. `tests/test_serial_routes.py`, `.quality-gates.json`, `CHANGELOG.md`.
4. Close-out.

**DONE when:**

- The suite exits 0 with 5 xfailed (P2's 3 plus D1 and D7).
- The ratchet passes 2/2 with the new count.
- A red-drive is recorded: for example, delete the `"humidity": "rh"` mapping and watch T3.2 fail.
- The whole suite still runs in well under 10 s.

**Surface:**

- **What the pty proves:** that pyserial opens and reads a real tty device.
- **What it can't prove:**
  - **the REV6 board's real output format** (the three formats in `_parse_line`'s docstring are guesses, and no
    capture exists);
  - the baud rate and 3.3 V logic levels;
  - the adapter's driver.

  The first real capture from the adapter should become a fixture in its own session.
- **Threads:** the reader thread is a daemon, and it blocks in `readline` for up to 5 s (`serial_reader.py:65`).
  Call `stop()` and close both pty file descriptors. **Never `join()`**, because that adds up to 6 s per test.

**Session boundary:** Phase 3 is one session.

### Phase 4: The API client and the API-mode routes

**Goal:** everything the client sends, the token lifecycle, and the API branches of the routes. D5, D6 and the
hourly half of D2 get their xfails.

**Fakes** (add to `conftest.py`):

- **`FakeRequests`** records `(method, url, params/data/json, headers, timeout)` and returns scripted responses with
  `.json()`, `.text` and `.raise_for_status()`. Install it with
  `monkeypatch.setattr(airqino_client, "requests", fake)`. Keep `fake.HTTPError = requests.HTTPError`, so code that
  catches the real class still behaves the same.
- **`FakeClock`**, installed with `monkeypatch.setattr(airqino_client, "time", clock)`. **Don't patch the global
  `time.time`,** because pytest itself uses it.
- **`FakeClient`**: canned returns for the 7 methods `app.py` calls, with an option to raise. Inject it with
  `monkeypatch.setattr(app_module, "_api_client", fake)`.

**Tests** (`tests/test_airqino_client.py`):

- **T4.1** The first request POSTs to `TOKEN_URL` (`airqino_client.py:8`) with exactly `grant_type=password`,
  `client_id`, `client_secret`, `username`, `password` and `scope=openid`, and `timeout=15`. The GET that follows
  carries `Authorization: Bearer <token>`.
- **T4.2** The token is cached while `now < expiry - 30` (`:23`): two GETs make one token POST.
- **T4.3** Within 30 s of expiry, the client sends the refresh grant with the stored `refresh_token` (`:49-61`) and
  uses the new token.
- **T4.4** If the refresh raises, the client falls back to the password grant (`:27-31`).
- **T4.5** A missing `expires_in` defaults to 300 (`:45`).
- **T4.6** A parametrized table of the 11 endpoint methods, each with its exact URL and params. The same table is in
  `README.md` (§AirQino API reference).
- **T4.7** `get_hourly_avg` returns `resp.text` and sends `pivot=true` only when `pivot=True`.
- **T4.8** `generate_report` POSTs the JSON body `{centraline, grandezza, start_date, end_date}`.
- **T4.9** An HTTP error from `raise_for_status` propagates to the caller.

**Tests** (`tests/test_api_routes.py`, using the `FakeClient`):

- **T4.10** `/api/stations`:
  - 400 when there's no project;
  - `?project=` overrides the environment;
  - 200 passes the data through;
  - 502 carries the exception text.
- **T4.11** `/api/metadata`:
  - a list `session_info` returns the entry whose `station` matches;
  - with no match, it returns the first entry;
  - a dict passes through;
  - `sensors` is present when a station is set;
  - there's no `session_info` key when no project is set;
  - 502 when the client raises.
- **T4.12** `/api/current` (API branch): 400 with no station, 200 `{"source": "api"}`, 502 when the client raises.
- **T4.13** `/api/timeseries`:
  - `hours <= 12` calls `get_last_station_data(station_name=…)`;
  - `hours > 12` calls `get_range(station, from, to)`, with the dates computed from a frozen clock. Patch
    `app_module.datetime` with a subclass whose `utcnow()` is fixed.
  - 400 with no station; 502 when the client raises.
- **T4.14** `/api/hourly`:
  - `;`-delimited CSV text is parsed into a list of dicts;
  - `days` sets the date range;
  - 400 with no station; 502 when the client raises.
- **T4.15** `/api/status` in API mode returns source `api` and echoes the station and project.
- **xfail:** D5 and D6 (with a `FakeReader` and a `FakeClient` both injected and both variables set), and D2's
  hourly half.

**Commits:**

1. The claim.
2. `tests/test_airqino_client.py`, `tests/conftest.py`, `CHANGELOG.md`.
3. `tests/test_api_routes.py`, `.quality-gates.json`, `CHANGELOG.md`.
4. Close-out.

**DONE when:**

- The suite exits 0 with 8 xfailed. There are 7 defects, and D2 has two tests.
- The ratchet passes 2/2.
- A red-drive is recorded: for example, change `- 30` to `+ 30` at `airqino_client.py:23` and watch T4.2 or T4.3
  fail.
- No product file shows in `git diff`.

**Surface:**

- **What the fakes prove:** what the client *sends*.
- **What they can't prove:** that the real AirQino API accepts it. The following were all written from vendor docs
  and are **unverified until credentials arrive** (requested from info@airqino.it; `SESSION_NOTES.md`):
  - the real paths;
  - the response shapes (`README.md:99` lists quirks: an empty `{}` on 401, CSV from `getHourlyAvg`, and a 30-day
    cap on `getRange`);
  - the Keycloak realm.

  A live, opt-in test (`@pytest.mark.live`, skipped without credentials) belongs to its own session afterwards.

**Session boundary:** Phase 4 is one session.

## 6. After the four phases: fix sessions

Each defect in §4 is fixed in its own session, in the order the operator picks, following
`docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`. The failing test already exists: it is the xfail. A fix
session:

1. Removes one `xfail` marker. The test then fails red on the unfixed code.
2. Fixes the product code.
3. Watches the test go green.
4. Tightens `tests-passed` by 1.
5. For D1, D3, D4 and D7, runs the runtime check from learning #5 (these are user-visible).

A fix that lands without removing its marker fails the suite as XPASS(strict). That's intended.

## 7. Alternatives considered

| Alternative | Pros | Cons | Why rejected |
|-------------|------|------|--------------|
| `unittest` (stdlib) | No dependency | No fixtures or `monkeypatch`, so env isolation and global resets are hand-written in every class. No strict-xfail ini switch. | pytest is already installed, and decision 1 chose it |
| `responses` / `requests-mock` | Runs more of the real `requests` stack (URL and param encoding) | A new dev dependency, and it still can't prove the real API | Decision 3. The fakes pin the same contract with zero dependencies. |
| Pin today's buggy behaviour as passing tests | Every test is green | Mislabels bugs as spec, so each fix session "breaks" a test and has to rewrite it | A strict xfail says the same thing honestly, and turns the fix into a mechanical flip |
| Fix each defect in the phase that finds it | Fewer sessions | Mixes test and product changes, breaks the 5-file cap sooner, and one reversal rolls back both | Decision 2. It is also failure mode #26's shape: two intents in one session. |
| Refactor to an app factory and drop the import-time `load_dotenv` first | Cleaner isolation | That's refactoring, which needs plan mode (`SAFEGUARDS.md`). It changes product code before any test protects it. | The `isolated` fixture handles the current structure, and the spike showed it works against a real planted `.env`. The refactor can come later, with this suite as its baseline. |
| One big phase | One session | Crosses three unrelated fake boundaries (filesystem/CSV, tty/thread, HTTP/clock), so a crash strands all of them | Four phases are each independently useful: "if I stop here, is something working?" is yes after each one (failure mode #25). |

## 8. Out of scope, and why

- **Fixing D1–D7.** §6: separate sessions, by decision 2.
- **Unit tests for `dashboard.js`.** They need a Node toolchain (vitest and jsdom), which is its own plan (decision 4).
  An **unverified** observation for that plan, from model knowledge only: check it against the EPA's AQI Technical
  Assistance Document before acting on it.
  - The `AQI` table (`dashboard.js:4-45`) seems to use the pre-2024 PM2.5 breakpoints (Good ≤ 12; the 2024 revision
    is believed to lower it to 9.0).
  - The NO₂, O₃ and CO breakpoints seem to be EPA's ppb/ppm values, while `SENSOR_META` (`:47-57`) labels those
    sensors µg/m³ and mg/m³. If so, those colours are off by a unit conversion.
- **CI (GitHub Actions).** It changes a public repo and needs the operator's approval. Until CI or the ratchet's
  pre-commit hook exists (`python3 quality_ratchet.py install-hook`, a per-clone opt-in), the gates bind only whoever
  runs them.
- **A coverage floor.** pytest-cov 7.1.0 is installed, but the floor should be measured after P4 and declared at the
  measured value in its own session. Pair it with a mutation spot-check, because a floor alone measures effort, not
  quality (`.quality-gates.json` `_example.why`).
- **Live API and live device tests.** There are no credentials and no adapter yet (§5, P3 and P4 surfaces).
- **Browser end-to-end tests.** Learning #5's headless-Chrome recipe stays the manual UI check.
- **`.quality-gates-results.json` and the other untracked tool outputs.** These are open item 2, the operator's call.
  Until then, stage files by name.

## 9. Verification of this plan's own claims (Session 9 spike)

Every mechanism the phases depend on was run in a throwaway scratchpad spike: copies of `app.py`,
`airqino_client.py`, `serial_reader.py`, `templates/` and `static/`, plus a planted `.env` containing
`AIRQINO_CLIENT_ID=leak` and `SERIAL_PORT=/dev/does-not-exist`. None of it is committed.

| Claim | Result |
|-------|--------|
| The `.env` leaks at `import app` | Confirmed: both planted values were in `os.environ` at import |
| The `isolated` fixture neutralizes it | Confirmed. Turning `autouse` off made the banner test fail. |
| `pytest.ini` works as written | `python3 -m pytest` and plain `pytest` both gave `5 passed, 2 xfailed` on pytest 9.0.2 |
| The banner guard can fail | Restoring the old "Arduino Mega" wording failed it |
| A strict xfail forces its marker off | Fixing D1 in the copy produced `FAILED … [XPASS(strict)]` |
| The pty round trip works | Real pyserial on `/dev/ttys008`: 2 lines parsed, garbage skipped |
| Injecting `FakeClient` works | `/api/stations?project=P1` returned 200, and the call was recorded |
| The two ratchet gates work | `quality_ratchet.py --run`: `2/2 pass` (measured 0 and 5). Strict xfails don't fail the exit-code gate. |

What the spike did **not** verify: Python 3.9 (not installed), Linux, and the dashboard's real rescored output. P1
measures the dashboard; §5 gives the computed expectation.

## 10. Planning checklist (`SESSION_RUNNER.md` §Planning Session Checklist)

- [x] Plan written with file paths and line numbers
- [x] Grep-based inventory (§3). This isn't a deletion or rename plan, but the inventory is what the phases are
  built from.
- [x] Each phase has DONE criteria and verification commands
- [x] Each phase names its surface and what that surface can't enforce
- [x] Each phase is a separate session with a STOP point
- [ ] Deepest reasoning mode at session start. The operator was told how (`/effort max`); whether it was set isn't
  recorded.
