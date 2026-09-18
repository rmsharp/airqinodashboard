# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14), D7 (Session 15) and D3 (Session 16) are done. Next: D4 (plan §6's order continues D4, then D6, D5 and
D2), or any other open item.
**Status:**
- **D3: FIXED, Session 16, on `main`** (`31e50f2` page, `5e37cb1` server, tests, README and gate, `c3004b7` plan).
  A CSV row with more fields than the header now loads without its extra fields, instead of failing the whole
  upload with a 500. The response gains `ragged_rows` when any row had extras, and the page's upload status then
  says how many, in amber. The operator chose this design ("B") over dropping the extras silently ("A") or
  rejecting the file ("C"), after all three were probed on the real page. `main` was fast-forwarded to the Session
  16 branch, which was then deleted. `main` is the only branch, and it is pushed straight after the close-out
  commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `122 passed, 5 xfailed` in about 0.3 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 4c59862276a3 · manifest 6947b3732825`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 122).
- **Dashboard:** 68/100, unchanged, with High+ risk 0. It has 6 flags, listed from `dashboard.html` at close-out:
  MEDIUM "No CI/CD pipeline" (BL-3); MEDIUM, a large file, the synced `docs/methodology/tools/methodology_dashboard.py`;
  LOW "No LICENSE file" (BL-1); LOW "BACKLOG.md: done-mark format not recognized" (BL-2); LOW `CHANGELOG.md` and LOW
  `HANDOFFS.md`, each past the 56,750 B one-read budget, which the dashboard calls expected for a ledger. Session
  15's handoff listed 5: its own close-out commit took `HANDOFFS.md` from 56,534 B to 60,283 B after it counted.
  This close-out can't add a size flag, since both ledgers are already flagged.
- **Defects (plan §4):** D1, D7 and D3 fixed. D2, D4, D5, D6 still have strict xfails, 5 tests in all (D2 has two).
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing), BL-2 (`- [ ]` checkboxes so the dashboard's
  done-mark check works) and BL-3 (decide whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 15's is at `git show a1cb7ec:SESSION_NOTES.md`, Session 14's at `git show b710ac0:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D4 (recommended next): the plan's fix sessions (§6), one defect per session.** D1, D7 and D3 are done.
   The remaining order is D4, then D6, D5 and D2. Each session, on a new branch off `main`:
   - removes the defect's `xfail` marker and watches its test fail on the unfixed code;
   - **before choosing a design, runs the current code and each candidate fix end to end on the surface the user
     sees** (learning #12). For D4 that is a CSV upload through the page, then the upload status, readings grid and
     chart. `--screenshot` alone can't upload; learning #14 has the drag-and-drop driver Session 16 used;
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by the measured delta (D3's was 2: its xfail, plus a test for the chosen design);
   - red-drives the fix against the whole suite with the original marker restored (learning #11), and runs the
     whole suite on the fix alone (that found T3.7 pinning D7 in Session 15; nothing pinned D3);
   - re-greps every `file:line` citation after editing, and measures a line shift instead of computing it (Session
     16's first plan note got one wrong by arithmetic).

   Where each one is:
   - **D4:** `app.py:249` decodes as `utf-8`, not `utf-8-sig`; its xfail is `tests/test_csv_routes.py:185` (marker
     `:183`). A BOM stays in the first header, and the page reads `row.timestamp` for the chart
     (`static/js/dashboard.js:270`) and `data.timestamp` for the reading cards (`:202`).
   - **D2:** `app.py:175` and `:224`; its xfails are `tests/test_csv_routes.py:178` and `tests/test_api_routes.py:213`.
   - **D5:** `app.py:53`; its xfail is `tests/test_api_routes.py:194`. **A real D5 fix also fails Phase 1's T1.5**
     (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`. That session must set all four
     credentials in T1.5 as well.
   - **D6:** `app.py:53-58`; its xfail is `tests/test_api_routes.py:205`.

   The plan's own `app.py` citations read lower than the code: by 4 past `:142` since D7, and by more inside
   `upload_csv` since D3 (both noted in the plan). Use the lines above. Probe fixes carried in these notes are
   starting points, not verified designs.
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
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here. Re-checked in Session 16
   against `~/Development/methodology/starter-kit/`: only `SAFEGUARDS.md` differs; `SESSION_RUNNER.md` and the three
   synced tools match.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–15's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:160`), which is 30
   days apart. `README.md:110` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with the real map and "API KEY REQUIRED / carto.com/basemaps/apikey" stamped across it, not a 4xx,
   so nothing in the app's code or tests would catch it (re-checked in Session 16). A page screenshot can look
   normal when the stamp falls outside the visible part of the map, as in Session 16's. Whether a free key exists and how to wire it in, or which other tile source to use, is a design
   question for its own session. BL-1 (MIT licensing) also touches this, since a tile provider swap changes what is
   credited and under what licence.
9. **The three backlog items** (BL-1, BL-2, BL-3 in `BACKLOG.md`). BL-2 is small and mechanical (checkboxes, one
   commit); BL-1 and BL-3 each start with the operator's decisions.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

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

### What Session 15 Did
**Deliverable:** Fix D7 (open item 1; plan §6's second fix session): a serial port that fails to open was served
as data with 200 (`serial_reader.py:64-69`, `app.py:141-147` at the start) — **COMPLETE**
**Started / Closed:** 2026-09-17 23:47 / 2026-09-18 00:20. Claimed on branch `fix/d7-port-open-failure` off `main`
`b710ac0`. Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 10 `CHANGELOG.md` entries: the claim, BL-2, BL-3, D7 parts 1–3, the test-citation follow-up, the plan
update, the branch deletion, and this close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `2fc1d25`. The operator picked D7 in the Phase 0 picker.
- **Two backlog items, out of band, each its own commit:** BL-2 (`d24ab0e`), because the dashboard can't read
  plain-bullet backlog items, so its done-mark check is off; my Phase 0 report had missed that signal. BL-3
  (`192e831`), deciding whether the repo needs CI/CD. The D7 changes stayed unstaged through both.
- **Probed before designing** (learning #7). The real app with `SERIAL_PORT=/dev/does-not-exist` reproduced D7:
  202, then 200 with the error as data; the page showed "Loading readings…", then "No readings available". A
  scratchpad copy with a server-only fix (503 plus the error) turned the xfail green, but the page stayed on
  "Loading readings…" indefinitely: `loadCurrent` only logs a non-2xx response. Plan §4's user-impact cell had
  assumed the page reports them. The operator chose "server + page" in a picker.
- **Red on the unfixed code:** with the marker removed, only D7's test failed (`assert 200 != 200`).
- **D7, three commits, each green and true at its own point** (the 5-file cap ruled out one commit):
  - `222f02c` page: `fetchJSON` tags its `Error` with the body's `source`; `loadCurrent` calls a new
    `renderReadingsError` for a `serial` source (red, centred, `textContent`). Other errors are still only logged.
  - `9698f9c` server: the reader's open failure goes in a new `error` field, not `latest`; `/api/current` answers
    503 `{"source": "serial", "data": null, "error": …}`. D7's marker removed and its test pins the 503. The
    whole-suite run on the fix failed T3.7 too, which asserted `latest["error"]`; it now checks `reader.error`.
  - `87c7535`: a README paragraph (the error shows within a minute; the reader doesn't retry, so restart), the
    `README.md:108`→`:110` citation it moved, and `tests-passed` 119 → 120.
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with the
  original marker and assertion (only D7's `XPASS(strict)`); the new tests on the unfixed code (D7 and T3.7 fail);
  the reader change alone (D7 fails, 202 until the deadline); 500 instead of 503 (D7 fails); the route change alone
  (5 fail). The gate: with one test hidden, `tests-passed` measured 119 and the ratchet exited 2.
- **Runtime (learning #5):** the real app, before and after, by `curl` and headless-Chrome screenshots. After the fix:
  202 then 503, and the error shows in red in the readings grid, at once on a reload, and on a fresh load after
  the 60 s refresh (70 s of virtual time). Adjacent paths unchanged: the no-source page; a pty fed
  `co=235;no2=17;o3=17;pm10=25;pm25=13` gives 200 and five reading cards. App, Chrome and pty feeder stopped each
  time; port 5001 free (`lsof` exit 1).
- **Citations:** the fix moved 11 `file:line` citations in the tests (`2519647`) and BL-1's map-tile line (`c159ac8`).
- **Plan updated** (`c159ac8`): Status line, D7's §4 row, and an "As implemented (D7, Session 15)" note under §6.
- **Probed a related claim before recording it:** a pty closed mid-run leaves the reader running with no error and
  the last reading served (open item 4, new).
- **Landing:** the operator picked "fast-forward main + push" before close-out (learning #8). After a `git fetch`,
  `origin/main` = `b710ac0` was an ancestor of the branch; a scan of the added lines found no secrets or local paths
  (its one hit was BL-3's prose). Then `git merge --ff-only` and `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 12 Handoff Evaluation" and "What Session 13 Did" were archived
  (`git show c159ac8:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red; product code fixed and the test watched green;
  `tests-passed` tightened 119 → 120 (measured); runtime check done; red-driven against the whole suite with the
  marker restored.
- `python3 -m pytest -q`: `120 passed, 6 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`; `--precommit`
  passed on the staged manifest. `node --check static/js/dashboard.js` exit 0.
- **Runtime (3E):** verified live above. Not verifiable here: API mode's error display (no credentials). By
  reading, a 502 body names no `source`, so it is still only logged.

**Key files:**
- `serial_reader.py:43` (`error`), `:67-70` (the open failure), `:87-88` (the loop's `except`, open item 4).
- `app.py:143-146` (the 503).
- `static/js/dashboard.js:134-143` (`fetchJSON`), `:145-157` (`loadCurrent`), `:231-241` (`renderReadingsError`).
- `tests/test_serial_routes.py:49-62` (D7's test), `tests/test_serial_reader.py:150-155` (T3.7).
- `.quality-gates.json:27` (`tests-passed`, 120); `README.md:73` (the serial-error paragraph).
- `docs/planning/test-suite-plan.md:587` (the "As implemented (D7, Session 15)" note).

**Gotchas for the next session:**
- **A green xfail isn't the user-visible fix** (learning #12). Look at the page with the candidate fix before
  choosing the design. D3 and D4 are CSV uploads: check the chart and readings grid in the real app.
- **The dashboard's flags: list them all from `dashboard.html`**, e.g. the `risk-flag` divs, rather than grepping
  for the ones the last handoff named. Session 15's Phase 0 grep missed a LOW flag that way (learning #13).
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3). Session 14's "400 at close-out" was
  measured before its last edit; the committed file was 407.
- **`app.py` citations in the plan are 4 lower than the code past `:142`.** Use open item 1's lines.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. **Stage files by name** (the 4
  untracked files remain, open item 2). **Cite the ratchet summary line from the final run.**

**Learnings (3C):** `CLAUDE.md` learning #12 (a green xfail isn't the user-visible fix; run the candidate fix on
the page first) and #13 (list the dashboard's flags from its output, not by grepping for known ones).

**Self-assessment:**
- **Score: 8/10**
- (+) Probed the fix's user-visible end before choosing a design. That found plan §4's wrong premise, and the
  operator decided on the evidence (two screenshots) instead of a guess.
- (+) 5 product red-drives and 1 gate red-drive, all against the whole suite. The fix's own whole-suite run caught
  T3.7 pinning D7's representation (learning #11 working as written).
- (+) Runtime checks covered the fixed path (reload and fresh load), and the no-source and working-serial paths
  next to it.
- (+) The 5-file cap held through 3 D7 commits, each green and true at its own point. Both out-of-band backlog
  requests were committed on their own, with the D7 changes unstaged.
- (+) Every moved `file:line` was re-grepped and fixed (13 in all), and a new claim was probed before it went into
  the handoff.
- (−) The Phase 0 report missed a LOW dashboard flag: I grepped for the three flags the handoff named. The
  operator raised it.
- (−) BL-3's first draft cited `:3226-3230` for a 6-line block ending at `:3231`. The re-grep caught it before the
  commit.
- (−) Several harness nudges for silence during long runs of tool calls, which repeats Sessions 6–14's minus.

### Session 14 Handoff Evaluation (by Session 15)
- **Score: 8/10**
- **What helped:**
  - Open item 1's D7 recipe and citations held on a fresh read: `serial_reader.py:64-69`, `app.py:141-147`, the
    xfail at `tests/test_serial_routes.py:54` (marker `:51`).
  - The warning that carried-forward probe fixes are starting points, not designs, is what made me look at the page.
    The suggested "2-line 503" would have left it stuck on "Loading readings…".
  - Open item 4's third finding (D7's `/api/timeseries` state) framed the scope question early. "Measure the
    `tests-passed` delta, don't assume" held (it was 1 this time, by measurement).
  - The ratchet citation matched a fresh `--run` (`71b7ac5ea8f1` / `973c1b7d973d`), and both frontiers sat at
    `b710ac0` with nothing to reconcile.
- **What was wrong:**
  - "`wc -l` and `splitlines()` agree on 400 for this file at close-out": the committed file (`b710ac0`) was 407.
  - "The flags are unchanged too": Session 14's own BL-1 had added a LOW flag (the backlog done-mark format), so
    there were four, not three.
  - `context_budget.py:346` (open item 3) is neither `measure_file` (`:329`) nor its split (`:347`).
- **What was missing:** nothing else the handoff could have known. The wrong page premise came from plan §4
  (Session 9).
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

### Sessions 1–14 (archived by Sessions 6–16)
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
