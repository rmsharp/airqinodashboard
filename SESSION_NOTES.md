# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14), D7 (Session 15), D3 (Session 16), D4 (Session 17) and D6 (Session 18) are done; D5 and D2 remain.
Session 18's probe also found a serial-reader race that plan §4 doesn't list (open item 1, recommended next).
**Status:**
- **D6: FIXED, Session 18, on `main`** (`5056055` fix, test and gate; `91ea569` plan; `2943371` a D5 citation the
  fix moved). `active_source()` now checks `SERIAL_PORT` before `AIRQINO_CLIENT_ID`, the order the data routes use
  and `README.md:36` documents. Before, with both configured, the badge said "API Connected" over serial readings.
  It is the only design the xfail and README allow, so no picker. `main` was fast-forwarded to the Session 18
  branch, which was then deleted; `main` is the only branch, pushed straight after the close-out commit. Check with
  `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `128 passed, 3 xfailed` in under 1 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0002758d231d · manifest f7714b97d99b`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 128).
- **Dashboard:** 68/100, High+ risk 0, the same 6 flags as at Phase 0 (listed from `dashboard.html` after these edits):
  MEDIUM no CI/CD (BL-3) and the synced dashboard's size; LOW no LICENSE (BL-1), the backlog's done-mark format
  (BL-2), and `CHANGELOG.md` and `HANDOFFS.md` past their one-read budget (expected for a ledger).
- **Defects (plan §4):** D1, D7, D3, D4 and D6 fixed. D2 and D5 still have strict xfails, 3 tests in all (D2 has
  two). The serial-reader race is not in §4 and has no test.
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing), BL-2 (`- [ ]` checkboxes so the dashboard's
  done-mark check works) and BL-3 (decide whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 17's is at `git show be44a02:SESSION_NOTES.md`, Session 16's at `git show 9995f62:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix the serial-reader race (recommended next), then D5 and D2.** The race comes first because the serial path
   is next in use (the operator is sourcing an adapter), the reason D1 and D7 went first. The order is the
   operator's call. Each fix session, on a new branch off `main`:
   - watches its test fail on the unfixed code (for D5 and D2, by removing the `xfail` marker; the race has no test
     yet, so the session writes it first);
   - **before choosing a design, runs the current code and each candidate fix end to end on the surface the user
     sees** (learning #12). Probe with more than one input, and explain any odd output with a measurement before
     calling it an artifact (learning #16);
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by the measured delta (D6's was 4: its one xfail became four cases);
   - red-drives the fix against the whole suite with the original marker restored (learning #11), and runs the
     whole suite on the fix alone (that found T3.7 pinning D7; nothing pinned D3, D4 or D6);
   - re-greps every `file:line` citation after editing, **including citations into the lines it changed**: D6's
     swap kept the line count but moved the `AIRQINO_CLIENT_ID` check from `:53` to `:55`.

   Where each one is:
   - **The serial-reader race (new, Session 18, probed; not in plan §4).** `get_serial_reader()` (`app.py:38-48`)
     checks `_serial_reader`, then builds and starts a reader, with no lock. The page's first load sends
     `/api/current` and `/api/timeseries` together (`static/js/dashboard.js:484-485`), and Flask's dev server is
     threaded, so each request starts a `SerialReader` on the same port. The global keeps one, and both threads read
     until the app stops, splitting the byte stream. In a scripted A/B (a fresh app per trial), `lsof` found the pty
     open twice after 3 of 3 concurrent first requests and once after 3 of 3 sequential ones; the readings read
     back were garbled (`no2` as `'1o37'`). Probed on a pty only. **By reading, not probed:** pyserial opens a POSIX
     port without an exclusive lock by default, so a real adapter would open twice the same way. The operator
     decides whether it becomes D8 (a plan amendment). The test must plant the race (learning #9), e.g. a stand-in
     `SerialReader` whose constructor sleeps, two threads released together by a `threading.Barrier`, and an
     assertion that one reader was built. A candidate fix, not verified: a module-level `threading.Lock` around the
     check and the build. `exclusive=True` on the port looks wrong: the second open would fail, set `error`, and the
     page would show a port error. Probe from a fresh app with no warm-up request (learning #16). `get_api_client()`
     (`app.py:24-35`) has the same check-then-set shape; by reading, two clients would each fetch a token. Unprobed.
   - **D5:** `app.py:55` (the check D6's fix moved from `:53`); its xfail is `tests/test_api_routes.py:227` (marker
     `:224`). **A real D5 fix also fails Phase 1's T1.5** (`tests/test_dashboard_page.py:97`), which sets only
     `AIRQINO_CLIENT_ID`; that session must set all four credentials in T1.5 as well. D6's test sets all four in
     every case with the API, so a D5 fix can't flip it.
   - **D2:** `app.py:175` and `:224`; its xfails are `tests/test_csv_routes.py:192` (marker `:191`) and
     `tests/test_api_routes.py:233` (marker `:232`).

   The plan's own `app.py` citations read lower than the code: by 4 past `:142` since D7, and by more inside
   `upload_csv` since D3, and its §4 D5 citation reads `:53` for `:55` since D6 (all noted in the plan). Use the
   lines above. Probe fixes carried in these notes are starting points, not verified designs.
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
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here. Re-checked in Session 18's
   Phase 0 against `~/Development/methodology/starter-kit/` (`cmp`): only `SAFEGUARDS.md` differs;
   `SESSION_RUNNER.md` and `methodology_dashboard.py` match.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–15's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:193`), which is 30
   days apart. `README.md:110` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown. It could also settle whether the API's hourly CSV starts with a BOM: `/api/hourly` parses
   `resp.text` (`airqino_client.py:123`, `app.py:230-232`) without D4's `utf-8-sig`, so a BOM there would put D4's
   symptom in API mode.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with the real map and "API KEY REQUIRED / carto.com/basemaps/apikey" stamped across it, not a 4xx,
   so nothing in the app's code or tests would catch it. Session 17's and 18's page screenshots show the stamp
   across the map. A screenshot can look normal when the stamp falls outside the visible part of the map, as in Session 16's.
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
**Deliverable:** Fix D6 (open item 1; plan §6's fifth fix session): `active_source()` checked the API before serial
(`app.py:53-58` at the start), but the data routes try serial first — **COMPLETE**
**Started / Closed:** 2026-09-18 14:32 / 15:50. Claimed on branch `fix/d6-source-order` off `main` `be44a02`. Closed
on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, the D6 fix, the plan update, the D5 citation correction, the branch
deletion, and this close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `2160d6b`. The operator picked D6 in the Phase 0 picker.
- **Probed before designing** (learnings #5, #12, #14). A pty fed the docstring's sensor line once a second, and the
  real app ran with `SERIAL_PORT` on it plus four fake credentials. Every proxy variable pointed at a closed port, so
  a vendor request would have failed as a 502; none did, so the handoff's by-reading premise held. The DevTools
  driver read the page: "API Connected" over five serial reading cards, and `/api/status` said `api`. The reorder,
  run first in a scratchpad copy of the app, changed only the badge, to "Serial".
- **Found a defect outside plan §4.** The first readings came back garbled. I first called that a probe artifact;
  `lsof` then showed the app holding the pty twice. A scripted A/B (a fresh app per trial) confirmed a race in
  `get_serial_reader()`: two fds after 3 of 3 concurrent first requests, one after 3 of 3 sequential ones. Recorded
  in the plan and open item 1, not fixed. The D6 probes warmed the reader with one request, so their readings were
  clean.
- **Design:** the reorder, the only one the xfail and `README.md:36` allow (routes going API-first fail four tests),
  so no picker.
- **Red on the unfixed code:** D6's xfail became a test over the four mixes of two or more sources. With `app.py`
  unfixed, only serial+api and all-three failed (`'api' == 'serial'`).
- **The fix, one commit** `5056055` (4 files): the swap at `app.py:53-56` and its docstring; the test, moved above
  the known-defects block; `tests-passed` 124 → 128; the ledger entry. `--precommit` wasn't run before the commit
  (no hook is installed), so I replayed it afterwards in a detached worktree at the parent: exit 0.
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with the
  original test and marker (only D6's `XPASS(strict)`, so nothing else pinned the old order); serial → CSV → API
  (only api+csv fails); API-first routes with `active_source()` unfixed (serial+api, all-three and both
  `test_serial_is_served_before_the_api` cases fail). The gate: with the api+csv case hidden, `tests-passed`
  measured 127 and the ratchet exited 2.
- **Runtime (learning #5):** the fixed app from the repo; the driven page read "Serial" over five cards and two
  chart series. Then a fresh app per mix (none, serial, api, csv, serial+api, api+csv, serial+csv): the badge,
  `/api/status` and both data routes agree in each, with no 502 in any log. App, Chrome and the pty feeder stopped;
  ports 5001 and 9333 free.
- **Plan updated** (`91ea569`): the Status line, D6's §4 row, and an "As implemented (D6, Session 18)" note (`:634`)
  that also records the race.
- **A false claim corrected** (`2943371`). The plan note said the swap moved no `app.py` citation, because the line
  count held. It moved the `AIRQINO_CLIENT_ID` check from `:53` to `:55`, which D5's xfail reason cites. Found at
  close-out by grepping every surface for citations into `app.py:51-59`.
- **Landing:** the operator picked "FF main + push". After a `git fetch`, `origin/main` = `be44a02` was an ancestor
  of the branch, and a scan of the added lines found no secrets or local paths. Then `git merge --ff-only` and
  `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 15 Handoff Evaluation" and "What Session 16 Did" archived
  (`git show 2943371:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red; product code fixed and the test watched green;
  `tests-passed` tightened 124 → 128 (measured); runtime check done; red-driven against the whole suite with the
  marker restored.
- `python3 -m pytest -q`: `128 passed, 3 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0002758d231d · manifest f7714b97d99b`.
- **Runtime (3E):** verified live above. Not covered: a real adapter and real API credentials (neither exists yet),
  so the API side of each mix answered 400 for want of a station name, not with data.

**Key files:**
- `app.py:51-59` (`active_source()`, the swap at `:53-56`); `app.py:38-48` (`get_serial_reader()`, the race).
- `tests/test_api_routes.py:152-183` (D6's comment, `BADGES` and the four-mix test), `:224` and `:232` (D5's and
  D2's markers).
- `.quality-gates.json:27` (`tests-passed`, 128); `static/js/dashboard.js:484-485` (the page's two concurrent loads).
- `docs/planning/test-suite-plan.md:634` (the "As implemented (D6, Session 18)" note, and the race).

**Gotchas for the next session:**
- **Warming the reader hides the race.** The D6 probes sent one `/api/current` before loading the page, so their
  readings stayed clean. A probe of the race must start a fresh app and load the page first (learning #16).
- **A swap keeps line numbers but moves content.** After a change, grep every surface for citations into the lines
  you changed, not only for shifted line numbers.
- **Flask's debug reloader runs two processes.** In a probe script, start the app with `start_new_session=True` and
  stop it with `os.killpg`; by hand, kill both PIDs from `lsof -tiTCP:5001`.
- **No git hooks are installed**, so run `python3 quality_ratchet.py --precommit` by hand, with the manifest staged,
  before the commit.
- **A proxy guard for fake credentials:** set `HTTPS_PROXY`, `HTTP_PROXY` and their lowercase forms to
  `http://127.0.0.1:9` for the app only. A vendor request then fails as a 502 in the app log, so none means none left.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. **Stage files by name** (the 4
  untracked files remain, open item 2). **Cite the ratchet summary line from the final run.**
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3).

**Learnings (3C):** `CLAUDE.md` learning #16 (an anomaly in a probe is evidence until a measurement explains it).

**Self-assessment:**
- **Score: 7/10**
- (+) Probed the page before and after in the real app, and turned the handoff's by-reading "no vendor traffic"
  premise into a measurement with the proxy guard.
- (+) Chased a garbled reading to its cause instead of working around it, and confirmed the race with a 3-and-3 A/B
  before writing it down. It is the most consequential serial-path finding since D7, and it stayed out of scope.
- (+) D6's test pins the source agreement for every mix, not one pair. 3 product red-drives and 1 gate red-drive,
  all against the whole suite, and each wrong design fails a named case.
- (+) Runtime check across all 7 source mixes, not only the defect's.
- (−) **A false claim reached a commit again.** `91ea569`'s note said no `app.py` citation moved: I had checked the
  line count, not the lines' content. The close-out grep caught it and `2943371` fixed it before the push, but it is
  Session 17's minus in a new form: a claim committed before checking the thing it is about.
- (−) Told the operator the garbled readings were "most likely" a probe artifact before measuring anything.
- (−) A citation computed from memory (`dashboard.js:480-482`, really `:484-485`), caught before the commit.
- (−) `--precommit` not run before the fix commit; replayed afterwards (exit 0).
- (−) Several harness nudges for silence during long runs of tool calls, which repeats Sessions 6–17's minus.

### Session 17 Handoff Evaluation (by Session 18)
- **Score: 9/10**
- **What helped:**
  - Open item 1's D6 citations held on a fresh read (`app.py:53-58`, `:141`, `:179`, `README.md:36`, the xfail at
    `tests/test_api_routes.py:205`, marker `:202`), and so did its probe recipe: a pty plus four fake credentials.
  - Labelling the no-vendor-traffic premise "by reading, not probed", with "check that before trusting it", led to
    the proxy guard, which made it a measurement. It held.
  - "D6's test sets all four credentials, so a D5 fix can't flip it" carried straight into the new test's design.
  - The reloader's two-PID gotcha kept a port from being left busy. The ratchet citation matched
    `.quality-gates-results.json`, both frontiers sat at `be44a02` with nothing to reconcile, the 6 flags matched
    `dashboard.html`, and the notes were 386 lines as stated.
- **What was wrong:** nothing I found.
- **What was missing:** that the page's first load starts two serial readers. No earlier handoff mentions it; the
  D6 probe found it only because it loaded a fresh app's page before any other request.
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

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

### Sessions 1–16 (archived by Sessions 6–18)
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
"Session 15 Handoff Evaluation" and "What Session 16 Did": `git show 2943371:SESSION_NOTES.md`.
