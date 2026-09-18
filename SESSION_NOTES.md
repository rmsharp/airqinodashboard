# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14), D7 (Session 15), D3 (Session 16) and D4 (Session 17) are done. Next: D6 (plan §6's order continues
D6, then D5 and D2), or any other open item.
**Status:**
- **D4: FIXED, Session 17, on `main`** (`caec75a` fix, tests, README and gate; `9812ef3` plan). An upload is now
  decoded as `utf-8-sig`, so the byte-order mark that Excel's "CSV UTF-8" export writes no longer stays in the first
  header. Before, the page said "Loaded" in green, but the cards had no timestamps and the chart was empty; with a
  sensor as the first column, that sensor's card and chart series were missing. No design went to the operator: the
  one alternative, stripping U+FEFF from each header key, gives the same page, and the tests pass on either. `main`
  was fast-forwarded to the Session 17 branch, which was then deleted. `main` is the only branch, and it is pushed
  straight after the close-out commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `124 passed, 4 xfailed` in about 1–3 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 5de9dfd7b3bc · manifest c0a107040a76`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 124).
- **Dashboard:** 68/100, unchanged, with High+ risk 0. It has 6 flags, the same 6 as at Phase 0, listed from
  `dashboard.html` after this close-out's edits: MEDIUM "No CI/CD pipeline" (BL-3); MEDIUM, a large file, the synced
  `docs/methodology/tools/methodology_dashboard.py`; LOW "No LICENSE file" (BL-1); LOW "BACKLOG.md: done-mark format
  not recognized" (BL-2); LOW `CHANGELOG.md` and LOW `HANDOFFS.md`, each past the 56,750 B one-read budget, which the
  dashboard calls expected for a ledger.
- **Defects (plan §4):** D1, D7, D3 and D4 fixed. D2, D5 and D6 still have strict xfails, 4 tests in all (D2 has two).
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing), BL-2 (`- [ ]` checkboxes so the dashboard's
  done-mark check works) and BL-3 (decide whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 16's is at `git show 9995f62:SESSION_NOTES.md`, Session 15's at `git show a1cb7ec:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D6 (recommended next): the plan's fix sessions (§6), one defect per session.** D1, D7, D3 and D4 are
   done. The remaining order is D6, then D5 and D2. Each session, on a new branch off `main`:
   - removes the defect's `xfail` marker and watches its test fail on the unfixed code;
   - **before choosing a design, runs the current code and each candidate fix end to end on the surface the user
     sees** (learning #12). For D6 that is the header's source badge beside the readings grid, with serial and API
     both configured. Probe with more than one input: D4's second symptom (a sensor as the first column) showed up
     only on a second probe file;
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by the measured delta (D3's and D4's were 2: the xfail, plus one new test);
   - red-drives the fix against the whole suite with the original marker restored (learning #11), and runs the
     whole suite on the fix alone (that found T3.7 pinning D7 in Session 15; nothing pinned D3 or D4);
   - re-greps every `file:line` citation after editing, and measures a line shift instead of computing it.

   Where each one is:
   - **D6:** `active_source()` checks the API before serial (`app.py:53-58`), but `/api/current` and
     `/api/timeseries` try serial first (`:141`, `:179`), and `README.md:36` documents serial → API → CSV. Its xfail
     is `tests/test_api_routes.py:205` (marker `:202`) and asserts `active_source() == "serial"` with both sources
     configured. For the real-app probe: a pty feeding a sensor line on `SERIAL_PORT` (Sessions 14–15), plus four
     fake credentials. **By reading, not probed:** with `AIRQINO_PROJECT_NAME` and `AIRQINO_STATION_NAME` unset,
     `/api/metadata` (fetched on page load, `static/js/dashboard.js:170`) calls no client method (`app.py:117`,
     `:129`), and the two data routes answer from serial, so the probe should send nothing to the vendor
     (`airqino_client.py:7-8`). Check that before trusting it.
   - **D5:** `app.py:53`; its xfail is `tests/test_api_routes.py:194` (marker `:191`). **A real D5 fix also fails
     Phase 1's T1.5** (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`. That session must set
     all four credentials in T1.5 as well. D5 and D6 both change `active_source()`; D6's test sets all four
     credentials, so a D5 fix can't flip it.
   - **D2:** `app.py:175` and `:224`; its xfails are `tests/test_csv_routes.py:192` (marker `:191`) and
     `tests/test_api_routes.py:213` (marker `:212`).

   The plan's own `app.py` citations read lower than the code: by 4 past `:142` since D7, and by more inside
   `upload_csv` since D3 (both noted in the plan; D4 moved none). Use the lines above. Probe fixes carried in these
   notes are starting points, not verified designs.
2. **Decide the untracked files.** For each one, commit, gitignore or delete; that's the operator's call.
   - `docs/HARDWARE.html` has been untracked since Session 3. It is an HTML render of `docs/HARDWARE.md` and holds no
     stale hardware copy.
   - Three tool outputs, all present now, have no `.gitignore` entry: `dashboard_history.jsonl` (written by every
     dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`, which the `.quality-gates.json`
     seed says to gitignore); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence
   missing: `.context-budget.json` declares it for `CLAUDE.md`, with a minimum of 800 B. `CLAUDE.md` has never had a
   fence or a Purpose section, and `README.md`'s opening is the source text. The same tool also reports
   `SESSION_NOTES.md` as "instrument-failed", for two reasons, both in the tool, not this file:
   - `.context-budget.json` expects at least 2 `^## ` headings, but this file has 1, and so does the synced seed
     `docs/methodology/starter-kit/SESSION_NOTES.md`.
   - its 400-line ceiling counts one line more than `wc -l` (`measure_file`, `context_budget.py:329`, counts
     `text.split("\n")` at `:347`), so this file must stay at 399 lines or fewer by `wc -l` to pass it.

   Both are mismatches inside the methodology's own tooling. Raise them upstream rather than restructuring this
   file to satisfy either one.
4. **Decide five findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:87` checks
     `_csv_data is not None`, but `active_source()` (`:57`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode and in serial mode. CSV returns the last 500 rows (`app.py:207-212`), and
     serial returns `get_history(limit=500)` (`:181`), whatever the range. So the chart's 6h–30d buttons
     (`templates/dashboard.html:86-91`) change nothing outside API mode.
   - With a port that failed to open, `/api/timeseries` still answers 200 with `data: []` (D7 changed only
     `/api/current`). The chart is empty either way, and the readings grid now shows the error.
   - **(new, Session 15, probed)** A port that opens and then fails (a pty closed mid-run, standing in for an
     unplugged adapter) is never reported: the reader thread keeps running with `error` `None`, `_read_loop`'s
     `except` (`serial_reader.py:87-88`) sleeps and retries forever, and `/api/current` keeps serving the last
     reading with 200. Each reading card shows its timestamp, so the age is visible. Related gaps: the reader never
     retries a port that failed to open (restart needed, now said in `README.md:73`), and on a fresh page load the
     error appears only at the 60 s refresh, because the first request starts the reader and gets 202.
   - **(new, Session 16, probed)** A CSV whose first line is blank loads as rows with no columns. `csv.DictReader`
     takes the blank line as the header, so every value is an extra field: the upload answers 200 with `ragged_rows`
     equal to the row count, the source becomes `csv`, and the grid shows "No readings available". It was a 500
     before D3's fix. The delimiter check (`app.py:251-258`) reads the blank line too.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here. Re-checked in Session 17
   against `~/Development/methodology/starter-kit/` (`cmp`): only `SAFEGUARDS.md` differs; `SESSION_RUNNER.md` and
   the three synced tools match.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–15's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:160`), which is 30
   days apart. `README.md:110` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown. It could also settle whether the API's hourly CSV starts with a BOM: `/api/hourly` parses
   `resp.text` (`airqino_client.py:123`, `app.py:230-232`) without D4's `utf-8-sig`, so a BOM there would put D4's
   symptom in API mode.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with the real map and "API KEY REQUIRED / carto.com/basemaps/apikey" stamped across it, not a 4xx,
   so nothing in the app's code or tests would catch it. Session 17's page screenshots show the stamp across the
   map. A screenshot can look normal when the stamp falls outside the visible part of the map, as in Session 16's.
   Whether a free key exists and how to wire it in, or which other tile source to use, is a design question for its
   own session. BL-1 (MIT licensing) also touches this, since a tile provider swap changes what is credited and
   under what licence.
9. **The three backlog items** (BL-1, BL-2, BL-3 in `BACKLOG.md`). BL-2 is small and mechanical (checkboxes, one
   commit); BL-1 and BL-3 each start with the operator's decisions.
10. **Make learning #15 a gate (new in Session 17).** A test that fails when a file under `tests/` holds a literal
    invisible character (U+FEFF, U+200B, U+00A0) would catch what Session 17 caught only by a hand-run byte grep,
    after a false claim had been committed. It adds one test, so `tests-passed` tightens by 1. Its own session:
    3C says a mechanical learning is a gate, not a row.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 18 Did
**Deliverable:** Fix D6 (open item 1; plan §6's fifth fix session): `active_source()` checks the API before serial
(`app.py:53-58`), but `/api/current` and `/api/timeseries` try serial first (`:141`, `:179`) (IN PROGRESS)
**Started:** 2026-09-18 14:32, on branch `fix/d6-source-order` off `main` `be44a02`
**Status:** Session claimed. Work beginning.
**Ledger:** `CHANGELOG: pending` — the claim commit's `CHANGELOG.md` entry says (in progress); Phase 3F records the rest.

### What Session 17 Did
**Deliverable:** Fix D4 (open item 1; plan §6's fourth fix session): an upload was decoded as `utf-8`, not
`utf-8-sig`, so a BOM stayed in the first header (`app.py:249`) — **COMPLETE**
**Started / Closed:** 2026-09-18 00:58 / 09:55 (the clock includes a long wait at the landing picker). Claimed on
branch `fix/d4-csv-bom` off `main` `9995f62`. Closed on `main` after a fast-forward, and pushed straight after the
close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, the D4 fix, the plan update, the escape correction, the branch
deletion, and this close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `d63e4f9`. The operator picked D4 in the Phase 0 picker.
- **Probed before designing** (learnings #7, #12, #14). The drag-and-drop driver, rebuilt from learning #14's
  recipe, dropped scratchpad CSVs (CRLF, as Excel writes) on the real page. Unfixed, a BOM file with `timestamp`
  first read "Loaded 5 rows (5 columns)" in green, but the cards had no timestamps and the chart had no series,
  also after a reload. A second file, with `pm25` first, found a second symptom that plan §4 doesn't list: the
  PM2.5 card and series were missing. The candidate (`utf-8-sig`), run first in a scratchpad copy of the app, fixed
  both.
- **Design:** `utf-8-sig`. The other design, stripping U+FEFF from each header key, gives the same page on every
  realistic file, so no choice went to the operator; the red-drive below shows the tests don't prefer either.
- **Scope check** (workstream question 4): only `upload_csv` decodes an uploaded file. `/api/hourly` parses the
  API's CSV and can't be checked without credentials (open item 7).
- **Red on the unfixed code:** with the marker removed and the new test added, only the two D4 tests failed, each
  on a key starting `\ufeff`.
- **The fix, one commit** `caec75a` (5 files, at the cap): `app.py:249` decodes as `utf-8-sig` (same line, so no
  cited line moved); D4's test pins the body and the stored row and moved above the known-defects block; a new
  test covers a `;` file with `pm25` first; a README clause, inside line 40; `tests-passed` 122 → 124. It was
  meant to spell the BOM as the escape `\ufeff` and its ledger entry says it did, but see the correction below.
- **The escape correction** `18e94c3`, found at close-out. The Edit tool decoded the `\ufeff` I typed into the
  character itself, so `caec75a`'s tests still held literal BOMs, as did its commit message (once) and ledger entry
  (twice). A byte grep of every touched file (`grep -c $'\xef\xbb\xbf'`) found them. The tests were rewritten with
  Python, and still fail on the unfixed decode; a new ledger entry records the false claim, since entries are
  never edited. Not rewritten: the commits, whose SHAs are already cited (learning #6).
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with the
  original marker and assertion (only D4's `XPASS(strict)`); stripping the BOM only for delimiter detection (both
  D4 tests fail); `utf-8-sig` without `errors="replace"` (T2.8 fails, `UnicodeDecodeError`); the key-stripping
  design (all 124 pass). The gate: with the new test hidden, `tests-passed` measured 123 and the ratchet exited 2.
- **Runtime (learning #5):** the fixed app from the repo, three files by the driver, and a reload: timestamps on
  all four cards and two 5-point series. Adjacent paths: a clean CSV unchanged; `curl` of a BOM file with a ragged
  row gives clean `columns` and `ragged_rows: 1`; an invalid-UTF-8 file still loads with U+FFFD. App and Chrome
  stopped; ports 5001 and 9333 free (`lsof` exit 1).
- **Plan updated** (`9812ef3`): the Status line, D4's §4 row, and an "As implemented (D4, Session 17)" note (`:624`).
- **Landing:** the operator picked "FF main + push". After a `git fetch`, `origin/main` = `9995f62` was an ancestor
  of the branch, and a scan of the added lines found no secrets or local paths. Then `git merge --ff-only` and
  `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 14 Handoff Evaluation" and "What Session 15 Did" were archived
  (`git show 9812ef3:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red; product code fixed and the tests watched green;
  `tests-passed` tightened 122 → 124 (measured); runtime check done; red-driven against the whole suite with the
  marker restored.
- `python3 -m pytest -q`: `124 passed, 4 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 5de9dfd7b3bc · manifest c0a107040a76`; `--precommit`
  passed on the staged manifest.
- **Runtime (3E):** verified live above. Not covered: the file input's click-to-choose path (same `uploadFile` as
  the drop), a real Excel export (the files were built to match one), and a real SD-card file (none exists).

**Key files:**
- `app.py:249` (the decode); `tests/test_csv_routes.py:175-186` (D4's comment and two tests), `:191` (D2's marker).
- `.quality-gates.json:27` (`tests-passed`, 124); `README.md:40` (the CSV paragraph).
- `docs/planning/test-suite-plan.md:624` (the "As implemented (D4, Session 17)" note).

**Gotchas for the next session:**
- **Flask's debug reloader runs two processes**, so `lsof -tiTCP:5001` prints two PIDs. `kill` takes both, but a
  command that takes one PID (`lsof -a -d cwd -p`) needs a loop. Check which copy of the app answers (repo or
  scratchpad) by its cwd, since both listen on 5001.
- **The Edit tool decodes a `\uXXXX` in its input into the character.** In Session 17, `\ufeff` typed into
  an Edit input landed as a literal BOM, in a Python test and in Markdown alike, while `\n` in the same input
  stayed as two characters. Write such text with a script that builds it (`chr(92) + "ufeff"`), then grep the
  bytes (learning #15, new).
- **Upload state persists in a running app**, and the upload area moves to the bottom panel once a source is
  active; the driver finds `#uploadArea` in either place.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. **Stage files by name** (the 4
  untracked files remain, open item 2). **Cite the ratchet summary line from the final run.**
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3).

**Learnings (3C):** `CLAUDE.md` learning #15 (write an invisible character in a test as an escape, and check the
bytes before claiming it's gone). Not yet a gate: open item 10.

**Self-assessment:**
- **Score: 7/10**
- (+) Probed on the real page before designing, with two BOM files rather than one; the second found the symptom
  plan §4 missed.
- (+) Test-first: both D4 tests watched red on the unfixed code before the fix.
- (+) 4 product red-drives and 1 gate red-drive, all against the whole suite. The passing one was deliberate: it
  shows the tests pin the page's keys, not the codec.
- (+) The fix stayed on its line, so no `app.py` citation moved, and the 5-file cap held.
- (+) Re-checked carried claims before repeating them (open items 5 and 8, the flag count, every citation in open
  item 1).
- (−) **A false claim reached a commit and the ledger.** `caec75a`'s entry says its test uses the escape, and it
  didn't: the Edit tool had decoded it. I never checked the bytes after writing a change whose whole point was
  bytes, which is the hazard learning #15 names. My own close-out grep caught it before the push, and `18e94c3`
  fixed the file, but the committed entry stays wrong on the record.
- (−) Learning #15's first draft had the same literal BOM and named the wrong session (13, not 11); both caught by
  the same grep and a `git log -S` before the commit.
- (−) A per-PID `lsof` call failed on the reloader's two PIDs; caught from its output.
- (−) Two harness nudges for silence during Phase 0's reads, and one during close-out, which repeats Sessions 6–16's
  minus.
- (−) The design went straight to `utf-8-sig` without a picker. I think that was right, since the two designs give
  the same page, but it's a change from Sessions 15–16, so it's recorded here.

### Session 16 Handoff Evaluation (by Session 17)
- **Score: 9/10**
- **What helped:**
  - Open item 1's D4 citations held on a fresh read: `app.py:249`, the xfail at `tests/test_csv_routes.py:185`
    (marker `:183`), and the page's `row.timestamp` (`static/js/dashboard.js:270`) and `data.timestamp` (`:202`).
    Those two lines are exactly the two symptoms the probe showed.
  - Learning #14's recipe rebuilt the driver in minutes, and it worked on the first run.
  - The ratchet citation matched `.quality-gates-results.json`, both frontiers sat at `9995f62` with nothing to
    reconcile, the 6 flags matched `dashboard.html`, and the notes were 374 lines as stated.
- **What was wrong:** nothing I found.
- **What was missing:** that Flask's reloader gives two PIDs on port 5001, and that D4's test held its BOM as an
  invisible literal. Session 16 had no reason to hit either.
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

### What Session 16 Did
**Deliverable:** Fix D3 (open item 1; plan §6's third fix session): a CSV row with more fields than the header put
its extras under the key `None`, and `k.strip()` failed (`app.py:262-265` at the start) — **COMPLETE**
**Started / Closed:** 2026-09-18 00:23 / 00:48. Claimed on branch `fix/d3-ragged-csv-row` off `main` `a1cb7ec`.
Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, D3 parts 1 and 2, the plan update, the branch deletion, and this
close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `5c93025`. The operator picked D3 in the Phase 0 picker.
- **Probed before designing** (learnings #7 and #12). `--screenshot` can't upload, so a scratchpad Node script drove
  headless Chrome over the DevTools protocol and dropped a CSV on `#uploadArea` (learning #14, new). The real app
  reproduced D3: `curl` got a 500 as Werkzeug's HTML debugger page, and the page read "Upload failed: Unexpected
  token '<', "<!doctype "... is not valid JSON" with nothing loaded. Three candidates in scratchpad copies of the
  app, given the same 5-row CSV (a trailing comma on row 3, an extra value on the last row): A (drop the extras
  silently) loaded as if clean; B (drop and count) loaded with an amber note; C (a 400 naming the line) loaded
  nothing. The operator chose B in a picker.
- **Red on the unfixed code:** with the marker removed, only D3's test failed (`AttributeError` at `app.py:265`).
- **D3, two commits, each green and true at its own point** (6 files, so the 5-file cap split it):
  - `31e50f2` page: `uploadFile` adds the ragged-row count to the status, in amber, when the response has
    `ragged_rows`. A no-op until part 2; that commit's tree gave `120 passed, 6 xfailed`.
  - `5e37cb1` server: `upload_csv` skips the `None` key and counts those rows; `ragged_rows` is in the body only
    when it isn't 0. D3's test pins the new body and moved above the known-defects block; a new test covers an
    extra value, a clean row and a trailing delimiter. A README sentence, inside its line, so no cited line moved.
    `tests-passed` 120 → 122.
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with the
  original marker and assertion (only D3's `XPASS(strict)`); the new tests on the unfixed code (both fail); design A
  (both D3 tests fail); counting once per file (only the multi-row test fails); always sending `ragged_rows` (T2.3's
  three cases and T2.7 fail, which pins "only when not 0"); keeping the extras under a key (both fail). The gate:
  with the new test hidden, `tests-passed` measured 121 and the ratchet exited 2.
- **Runtime (learning #5):** the real app, before and after, by the drag-and-drop driver, `curl` and screenshots.
  After the fix: the amber note, four reading cards (the last row, without its extra value) and two 5-point chart
  series. Adjacent paths: a reload shows the "CSV Data" badge and the same data; a clean CSV dropped on the bottom
  upload area reads "Loaded 5 rows (5 columns)" in green, and `curl` of it returns no `ragged_rows`. App and Chrome
  stopped each time; port 5001 free (`lsof` exit 1).
- **Plan updated** (`c3004b7`): the Status line, D3's §4 row, and an "As implemented (D3, Session 16)" note.
- **Checked three carried claims before repeating them:** open item 8 (the tile is the map with "API KEY REQUIRED"
  stamped on it: still true), open item 5 (only `SAFEGUARDS.md` differs from canonical: still true), and Session
  15's flag count (see the evaluation below).
- **Landing:** the operator picked "fast-forward main + push" before close-out (learning #8). After a `git fetch`,
  `origin/main` = `a1cb7ec` was an ancestor of the branch; a scan of the added lines found no secrets or local
  paths. Then `git merge --ff-only` and `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 13 Handoff Evaluation" and "What Session 14 Did" were archived
  (`git show c3004b7:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red; product code fixed and the test watched green;
  `tests-passed` tightened 120 → 122 (measured); runtime check done; red-driven against the whole suite with the
  marker restored.
- `python3 -m pytest -q`: `122 passed, 5 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 4c59862276a3 · manifest 6947b3732825`; `--precommit`
  passed on the staged manifest. `node --check static/js/dashboard.js` exit 0.
- **Runtime (3E):** verified live above. Not covered: the file input's click-to-choose path (the driver drops a
  file; both paths call the same `uploadFile`), and a real SD-card file (none exists; plan Phase 2's surface note).

**Key files:**
- `app.py:260-283` (`upload_csv`'s parse loop and body; the fix at `:262`, `:266-268` and `:277-283`).
- `static/js/dashboard.js:449-475` (`uploadFile`; the ragged note at `:461-467`).
- `tests/test_csv_routes.py:158-172` (D3's two tests), `:177` and `:183` (D2's and D4's remaining markers).
- `.quality-gates.json:27` (`tests-passed`, 122); `README.md:40` (the CSV paragraph).
- `docs/planning/test-suite-plan.md` §6, the "As implemented (D3, Session 16)" note.

**Gotchas for the next session:**
- **An upload needs a driver, not a screenshot** (learning #14). Its recipe rebuilds the driver in a few minutes.
- **In the real app a 500 is HTML** (`debug=True`), so the page's `resp.json()` throws and the status shows a JSON
  parse error. D4 isn't a 500, but any CSV-path error that is will look like that.
- **Upload state persists in a running app** (`_csv_data`), and the upload area moves from the setup banner to the
  bottom panel once a source is active. Restart the app between probes that need the no-source page.
- **zsh expands an unquoted `--include=*.py`** in `grep -r` and fails with "no matches found". Quote it.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. **Stage files by name** (the 4
  untracked files remain, open item 2). **Cite the ratchet summary line from the final run.**
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3).

**Learnings (3C):** `CLAUDE.md` learning #14 (an interaction needs a driver, not a screenshot; the recipe).

**Self-assessment:**
- **Score: 8/10**
- (+) Probed the current behaviour and three designs on the real page with a real drag-and-drop. That found the
  page's actual symptom (a JSON parse error, not a 500), and the operator chose on evidence.
- (+) Built the driver when `--screenshot` couldn't reach the surface, rather than settling for `curl`.
- (+) 6 product red-drives and 1 gate red-drive, all against the whole suite; each rejected design has a test that
  fails on it.
- (+) The 5-file cap held; both D3 commits were green at their own point (commit 1's tree checked with the test
  change stashed).
- (+) Re-checked three carried claims instead of repeating them, and measured the predecessor's flag miss.
- (−) The plan note's first draft said "11 lower past `:257`", computed rather than measured; the 7 lines went in
  at three places. Caught before the commit by mapping the lines (learning #7's trap again).
- (−) A zsh glob trap in the first citation grep; caught from its output.
- (−) Two harness nudges for silence during long runs of tool calls, which repeats Sessions 6–15's minus.

### Session 15 Handoff Evaluation (by Session 16)
- **Score: 9/10**
- **What helped:**
  - Open item 1's D3 recipe held on a fresh read: `app.py:262-265`, the xfail at `tests/test_csv_routes.py:167`
    (marker `:165`), and the surface: "a CSV upload in the real app, then the chart and readings grid".
  - Learning #12 and "probe fixes carried in these notes are starting points" sent me to the page before designing,
    which is where the real symptom was.
  - "Run the whole suite on the fix alone" and "measure the delta" both applied as written (the delta was 2).
  - The ratchet citation matched `.quality-gates-results.json`; both frontiers sat at `a1cb7ec` with nothing to
    reconcile. Learning #13's gotcha found the sixth flag at Phase 0.
- **What was wrong:** "It has 5 flags" was true when counted, but the close-out commit took `HANDOFFS.md` from
  56,534 B to 60,283 B, past its budget, so the committed state had 6: the "measured before the last edit" pattern
  Session 15 itself found in Session 14's line count.
- **What was missing:** that `--screenshot` can't exercise an upload, so D3 and D4 need a browser driver. Session 15
  only loaded pages, so it had no way to know; learning #14 records it now.
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery, only the driver.

### Sessions 1–15 (archived by Sessions 6–17)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
"Session 9 Handoff Evaluation" and "What Session 10 Did": `git show be5723c:SESSION_NOTES.md`.
"Session 10 Handoff Evaluation" and "What Session 11 Did": `git show 5084680:SESSION_NOTES.md`.
"Session 11 Handoff Evaluation" and "What Session 12 Did": `git show a14ff03:SESSION_NOTES.md`.
"Session 12 Handoff Evaluation" and "What Session 13 Did": `git show c159ac8:SESSION_NOTES.md`.
"Session 13 Handoff Evaluation" and "What Session 14 Did": `git show c3004b7:SESSION_NOTES.md`.
"Session 14 Handoff Evaluation" and "What Session 15 Did": `git show 9812ef3:SESSION_NOTES.md`.
