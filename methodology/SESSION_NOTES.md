# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14), D7 (15), D3 (16), D4 (17), D6 (18), D8 (19) and D5 (Session 20) are done; D2 is the last (open item 1,
recommended next).
**Status:**
- **D5: FIXED, Session 20, on `main`** (`0a3b488` fix, tests and gate; `f9fb312` the missing-credentials note;
  `06023d8` and `aadb299` the moved citations, the README and the gate; `0ba0bea` plan). `active_source()` now asks
  `get_api_client()` (`app.py:67`), so a `.env` with 1 to 3 of the four credentials is no API source: the page shows
  "No Data Source" and the setup banner, not "API Connected" over a grid stuck on "Loading readings...". The operator
  picked design C, so an amber note at the top of the page names the missing credentials, whatever the source
  (`missing_api_credentials()`, `app.py:57-60`; `templates/dashboard.html:40-46`). `main` was fast-forwarded to the
  Session 20 branch, which was then deleted; `main` is the only branch, pushed straight after the close-out commit.
  Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `144 passed, 2 xfailed` in under 1 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2993256f954d · manifest 0f1d28b61292`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 144).
- **Dashboard:** 68/100, High+ risk 0, the same 6 flags as at Phase 0 (listed from `dashboard.html` after these edits):
  MEDIUM no CI/CD (BL-3) and the synced dashboard's size; LOW no LICENSE (BL-1), the backlog's done-mark format
  (BL-2), and `CHANGELOG.md` and `HANDOFFS.md` past their one-read budget (expected for a ledger).
- **Defects (plan §4):** D1 and D3 to D8 fixed. D2 has the last two strict xfails.
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing), BL-2 (`- [ ]` checkboxes so the dashboard's
  done-mark check works) and BL-3 (decide whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 19's is at `git show da040da:SESSION_NOTES.md`, Session 18's at `git show 34a0a75:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D2 (recommended next), the last defect in plan §4.** The fix session, on a new branch off `main`:
   - removes the `xfail` markers and watches the tests fail on the unfixed code;
   - **before choosing a design, runs the current code and each candidate fix end to end on the surface the user
     sees** (learning #12), from a fresh app, with more than one input. Explain any odd output with a measurement
     before calling it an artifact (learning #16);
   - fixes the product code and watches the tests pass;
   - tightens `tests-passed` by the measured delta (D5's was 6, then 9 more for its note; D8's was 1);
   - red-drives the fix against the whole suite with the original markers restored (learning #11), and runs the
     whole suite on the fix alone (that found T3.7 pinning D7 and T1.5 pinning D5; nothing pinned D3, D4, D6 or D8);
   - re-greps every `file:line` citation after each commit that adds or moves lines, in every file it touched, and
     recounts every number it writes from the saved output with a script (learning #17).

   **D2:** `int()` on `?hours=` in `/api/timeseries` (`app.py:188`) and `?days=` in `/api/hourly` (`:237`). Its
   xfails are `tests/test_csv_routes.py:192` (marker `:191`) and `tests/test_api_routes.py:261` (marker `:260`). The
   timeseries parse runs before any source check, so `?hours=abc` gives a 500 even with no source; the hourly one
   is reached only with an API client. The page's range buttons send numbers only (`templates/dashboard.html:94-99`),
   so a bad value comes from a typed URL. The design question (a 400 naming the parameter, or the default value) is
   the operator's; by reading, not probed.

   The plan's own `app.py` citations read lower than the code: by 4 past `:142` since D7, by more inside
   `upload_csv` since D3, `:53` for `:55` since D6, by 1 to 3 more since D8, and by 9 or 10 more since D5's note
   (all noted in the plan). Use the lines above; the tests' own citations are current. Probe fixes carried in these
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
4. **Decide seven findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:100` checks
     `_csv_data is not None`, but `active_source()` (`:69`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode and in serial mode. CSV returns the last 500 rows (`app.py:220-225`), and
     serial returns `get_history(limit=500)` (`:194`), whatever the range. So the chart's 6h–30d buttons
     (`templates/dashboard.html:94-99`) change nothing outside API mode.
   - With a port that failed to open, `/api/timeseries` still answers 200 with `data: []` (D7 changed only
     `/api/current`). The chart is empty either way, and the readings grid now shows the error.
   - **(Session 15, probed)** A port that opens and then fails (a pty closed mid-run, standing in for an unplugged
     adapter) is never reported: the reader thread keeps running with `error` `None`, `_read_loop`'s `except`
     (`serial_reader.py:87-88`) sleeps and retries forever, and `/api/current` keeps serving the last reading with
     200. Each reading card shows its timestamp, so the age is visible. Related gaps: the reader never retries a port
     that failed to open (restart needed, now said in `README.md:75`). On a fresh page load the grid shows "Loading
     readings..." until the 60 s refresh or a reload, for readings and a port error alike (Session 19's probes),
     because the first request starts the reader and gets 202.
   - **(Session 16, probed)** A CSV whose first line is blank loads as rows with no columns. `csv.DictReader` takes
     the blank line as the header, so every value is an extra field: the upload answers 200 with `ragged_rows` equal
     to the row count, the source becomes `csv`, and the grid shows "No readings available". It was a 500 before
     D3's fix. The delimiter check (`app.py:264-271`) reads the blank line too.
   - **(Session 19, probed in the scratchpad)** `get_api_client()` (`app.py:26-37`) has D8's check-then-build
     shape. With its constructor slowed by 0.05 s, three concurrent first calls built three clients; the page's
     first load sends three API requests (`static/js/dashboard.js:484-486`). A lock there would not help on its
     own: one shared client still sent three token requests to a slow fake endpoint, because `_get_token`
     (`airqino_client.py:21-47`) races too. The cost is extra token requests at startup, nothing corrupted.
   - **(new, Session 20, probed with the vendor unreachable)** D7's shape on the API side. With all four credentials
     set and the token request failing, every data route answers 502, and the page says "API Connected" over
     "Loading readings..." indefinitely, because `loadCurrent` reports only the serial source's errors
     (`static/js/dashboard.js:152`). By reading, a wrong password takes the same path: `_get_token` raises on the
     refusal (`airqino_client.py:42`), and each route turns it into a 502. It may be the first thing the operator
     sees when credentials arrive, so it is worth deciding before item 7.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here. Re-checked in Session 20's
   Phase 0 against `~/Development/methodology/starter-kit/` (`cmp`): only `SAFEGUARDS.md` differs;
   `SESSION_RUNNER.md` and `methodology_dashboard.py` match.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–20's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:193`), which is 30
   days apart. `README.md:112` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown. It could also settle whether the API's hourly CSV starts with a BOM: `/api/hourly` parses
   `resp.text` (`airqino_client.py:123`, `app.py:243-245`) without D4's `utf-8-sig`, so a BOM there would put D4's
   symptom in API mode. It could also show whether a wrong password reaches the page as item 4's new finding
   says.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with the real map and "API KEY REQUIRED / carto.com/basemaps/apikey" stamped across it, not a 4xx,
   so nothing in the app's code or tests would catch it. Sessions 17–20's page screenshots show the stamp across
   the map. A screenshot can look normal when the stamp falls outside the visible part of the map, as in Session 16's.
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

### What Session 20 Did
**Deliverable:** Fix D5 (open item 1, recommended): `active_source()` reported `api` on `AIRQINO_CLIENT_ID` alone,
but `get_api_client()` needs all four credentials — **COMPLETE**, with the missing-credentials note the operator chose
**Started / Closed:** 2026-09-18 23:15 / 23:39 by the machine clock. Claimed on branch `fix/d5-one-credential` off
`main` `da040da`. Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 7 `CHANGELOG.md` entries: the claim, the fix, the note, the tests' citations, the README and gate, the
plan, and this close-out, which also records the fast-forward, the branch deletion and the push.

**What was done:**
- **Claim** `98d9530`. The operator picked D5 in the Phase 0 picker.
- **Probed before designing** (learnings #5, #12, #14): `probe/d5.py` starts a fresh app per mix of variables, reads
  four routes over HTTP, then headless Chrome reads the page; every proxy variable pointed at a closed port. 4 apps
  (unfixed; A, the four variables read in `active_source()`; B, `active_source()` calls `get_api_client()`; C, B
  plus a note) × 7 mixes = 28 runs. Unfixed, with `AIRQINO_CLIENT_ID` and a credential missing: "API Connected",
  no banner, grid stuck on "Loading readings...", every route 503. With a CSV too: "API Connected" over CSV
  readings, a second symptom §4 didn't list. A and B matched on every mix once memory addresses in the error
  strings were masked (unmasked, a script first said they differed). C matched B apart from the note.
- **The operator's call** (a picker with previews): C. B is the implementation, since the badge then can't disagree
  with the routes.
- **Test-first:** the marker removed, 1 failed. D5's test widened to five half-filled cases and a CSV case: 5 failed,
  1 passed (no `CLIENT_ID`, which passed before).
- **The fix** `0a3b488` (5 files): `app.py:58` at the time (now `:67`); the tests; T1.5 given all four credentials
  (it pinned D5, as the plan predicted); `tests-passed` 129 → 135.
- **The note** `f9fb312` (5 files): `API_CREDENTIALS` and `missing_api_credentials()`, the template's amber note,
  its CSS, and 9 page tests (7 red, 2 green before the note existed). It added 10 lines to `app.py` and 8 to the
  template.
- **Citations** `06023d8` (five `app.py` citations in three test files, +10) and, with the README sentence and
  `tests-passed` 135 → 144, `aadb299` (a test comment's `README.md:112` and `templates/dashboard.html:99`, and
  BL-1's CDN scripts, `:145-147`).
- **Plan** `0ba0bea`: the Status line, D5's row, and an "As implemented (D5, Session 20)" note
  (`docs/planning/test-suite-plan.md:683`), which also records open item 4's new API-side finding.
- **Red-drives**, each against the whole suite in a scratch worktree, files restored byte-identical (`shasum -c`):
  the fix with the original marker and T1.5 (only those two fail); the new tests on the unfixed code (5 fail);
  design A (passes); a two-of-four check (the no-`USERNAME` and no-`PASSWORD` cases fail); a note shown with no
  credentials (its `none` case fails); a note only inside the banner (the CSV and serial cases fail). The gate: with
  the CSV test hidden, `tests-passed` measured 134 and the ratchet exited 2.
- **Landing:** the operator picked "FF main + push". After a `git fetch`, `origin/main` = `da040da` was an ancestor
  of the branch, and a scan of the added lines found no secrets or local paths. Then `git merge --ff-only` and
  `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 17 Handoff Evaluation" and "What Session 18 Did" archived
  (`git show 0ba0bea:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE:** marker removed and watched red; product code fixed and the tests watched green; `tests-passed`
  tightened by the measured deltas (129 → 135 → 144); runtime check done; red-driven against the whole suite.
- `python3 -m pytest -q`: `144 passed, 2 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2993256f954d · manifest 0f1d28b61292`;
  `--precommit` exit 0 before each commit that staged the manifest.
- **Runtime (3E):** the repo's app, a fresh app for each of the 7 mixes, headless Chrome on each page: the page and
  the four routes matched the probed design C on every mix, and the only vendor 502s (12) came from the 2 all-four
  runs. Chrome and every app stopped; ports 5001 and 9333 free. Not covered: real credentials (none yet).

**Key files:**
- `app.py:54-60` (`API_CREDENTIALS`, `missing_api_credentials()`), `app.py:63-71` (`active_source()`, the fix at
  `:67`), `app.py:85` (the note's template variable).
- `templates/dashboard.html:40-46` (the note); `static/css/dashboard.css:75-80` (its style).
- `tests/test_api_routes.py:222-253` (D5's comment and tests); `tests/test_dashboard_page.py:96-104` (T1.5),
  `:122-160` (the note's tests); `.quality-gates.json:27` (`tests-passed`, 144).

**Gotchas for the next session:**
- **Session 20's probe is reusable:** `d5.py` (a fresh app per mix of variables, with the proxy guard and an optional
  CSV upload; reads four routes and the page) and `drive.mjs` (reads the badge, banner, grid, note and chart), in
  `/private/tmp/claude-501/-Users-rmsharp-Development-airqino/5e86b688-17db-4360-b388-e291eebd27aa/scratchpad/probe/`.
  Start Chrome yourself, in the background: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  --headless=new --remote-debugging-port=9333 --user-data-dir=<scratchpad>/chrome-profile about:blank`, and stop it
  with `pkill -f remote-debugging-port=9333`.
- **Added lines move citations in other files.** The note's template lines moved a test comment's
  `dashboard.html:91` and BL-1's `:137-139`; the README's moved `README.md:110`. I found both one commit late. After
  each commit that adds lines, grep every surface for citations into every file it touched, not only `app.py`.
- **Mask memory addresses before comparing probe output** (`0x…` in exception strings); otherwise identical runs
  compare unequal.
- **`active_source()` now calls `get_api_client()`,** so a test that installs `fake_client` makes it say `api` with
  no credentials set. Only D6's test combines them, and it sets all four.
- **The suite took about 4 s while headless Chrome ran** (the unchanged code measured 4.90 s the same way), and
  0.57 s otherwise. That's the machine, not a regression.
- **No git hooks are installed**, so run `python3 quality_ratchet.py --precommit` by hand, with the manifest staged.
  **Exit codes (learning #10):** redirect to a file, then `echo $?`. **Stage files by name** (the 4 untracked files
  remain, open item 2). **This file must stay at 399 lines or fewer by `wc -l`** (open item 3).

**Learnings (3C):** `CLAUDE.md` learning #18 (a summary of a choice made elsewhere should call the function that
makes it, not re-test its inputs).

**Self-assessment:**
- **Score: 8/10**
- (+) Three designs probed on the real page across 7 mixes before choosing, which found D5's CSV symptom and an
  API-side finding, and let the operator choose from screenshots.
- (+) Comparisons and counts came from scripts over the saved output, which caught the address artifact in the A/B
  comparison. Every number in a commit was printed from a file before that commit.
- (+) Test-first throughout; 6 product red-drives and 1 gate red-drive against the whole suite; T1.5's pin
  predicted and confirmed.
- (+) Every commit held to the 5-file cap, and every moved citation was printed against its line.
- (−) The template and README citation drift was caught one commit late, when the README citation turned out to
  share a line with a template one. The stale citations stood in `f9fb312` and `06023d8`.
- (−) The plan note's first draft overclaimed ("0 to 2 of the other three", when only 0 and 2 were probed) and cited
  the fix at `:58` after the note had moved it to `:67`. The print check caught both before the commit.
- (−) Two harness nudges for silence, which repeats Sessions 6–19's minus.

### Session 19 Handoff Evaluation (by Session 20)
- **Score: 9/10**
- **What helped:**
  - Every D5 and D2 citation held on a fresh read (`app.py:34`, `:58`, `:178`, `:227`; the markers; T1.5 at
    `tests/test_dashboard_page.py:97`).
  - "A real D5 fix also fails T1.5" was exactly right: the red-drive with the original tests failed D5's
    `XPASS(strict)` and T1.5, nothing else.
  - The probe recipe ("the badge, the setup banner and `/api/current` with one credential, then all four") and the
    probe scripts' path; `drive.mjs` was reused almost unchanged, and the proxy-guard gotcha carried over.
  - The ratchet citation matched `.quality-gates-results.json`, both frontiers sat at `da040da` with nothing to
    reconcile, the 6 flags matched `dashboard.html`, and the notes were 385 lines as stated.
- **What was wrong:** nothing I found.
- **What was missing:** that a half-filled `.env` plus a CSV would also mislabel the source (neither the handoff nor
  the plan mentions it), and how to start headless Chrome for `drive.mjs`, which expects it already running.
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

### What Session 19 Did
**Deliverable:** Fix the serial-reader race (open item 1, found by Session 18's D6 probe): `get_serial_reader()`
checked, then built and started a reader with no lock, so the page's two concurrent first requests each started a
`SerialReader` on one port — **COMPLETE**, as D8
**Started / Closed:** 2026-09-18 16:34 / 17:20. Claimed on branch `fix/serial-reader-race` off `main` `34a0a75`.
Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, the D8 fix, the tests' citations, the plan (with a correction to
the fix's entry), the branch deletion, and this close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `052cc5a`. The operator picked the race in the Phase 0 picker.
- **Probed before designing** (learnings #5, #12, #16), reusing Session 18's scripts from its scratchpad: a pty fed
  the docstring's line once a second, and each trial started a fresh app with no warm-up and sent the page's two
  first requests together. 5 trials per candidate: unfixed, 2 fds on the pty every time and 2 of 14 readings clean
  (3 sequential controls: 1 fd, all clean); a lock, 1 fd and 23 of 23 clean; `exclusive=True`, 1 fd but a 503
  "Could not exclusively lock port" in 4 of 5. On the driven page after a reload: unfixed lost its CO card; the
  lock showed all five; `exclusive=True` told the user to check the adapter and restart.
- **Probed the API side** before claiming anything about it: `get_api_client()` built 3 clients from 3 concurrent
  calls (constructor slowed), and one shared client still sent 3 token requests. So a lock there prevents nothing.
- **The operator's calls** (a picker): name it D8 in plan §4; keep `get_api_client()` out of scope (open item 4).
- **Test-first:** a stand-in reader that sleeps 0.2 s while built and starts no thread, two threads behind a
  `threading.Barrier`, one test client each. Unfixed: `assert 2 == 1`, 20 of 20 runs.
- **The fix, one commit** `b53303e` (4 files): `import threading`, `_serial_lock` (`app.py:22`) and a `with` around
  the check and the build (`:42-51`); the test; `tests-passed` 128 → 129; the ledger entry. 20 of 20 green.
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): unfixed and a lock
  around the check only (each fails just the new test); double-checked locking (passes); the test with its sleep
  removed, on the unfixed code (passed 10 of 10, so the delay is the planted hazard, and the test's comment now says
  so). The gate: with the test hidden, `tests-passed` measured 128 and the ratchet exited 2.
- **Citations** `927dfe8`: the 3 added lines moved every `app.py` line from the old `:7`; eight citations in three
  test files follow them (each printed against its line). Split from the fix to keep the 5-file cap.
- **Plan** `1af2c49`: Status line, a D8 row in §4, a pointer from Session 18's paragraph, and an "As implemented
  (D8, Session 19)" note (`docs/planning/test-suite-plan.md:659`).
- **A false count reached a commit.** `b53303e`'s ledger entry says "2 of 15 readings clean"; the five trials held
  14. A script recount before the plan commit found it; that commit's ledger entry carries the correction.
- **Landing:** the operator picked "FF main + push". After a `git fetch`, `origin/main` = `34a0a75` was an ancestor
  of the branch, and a scan of the added lines found no secrets or local paths. Then `git merge --ff-only` and
  `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 16 Handoff Evaluation" and "What Session 17 Did" archived
  (`git show 1af2c49:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, adapted to a defect with no xfail:** the test written first and watched red (20 of 20); product
  code fixed and the test watched green (20 of 20); `tests-passed` tightened 128 → 129 (measured); runtime check
  done; red-driven against the whole suite.
- `python3 -m pytest -q`: `129 passed, 3 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 9706974b83af · manifest 501e3c8538de`;
  `--precommit` passed on the staged manifest before `b53303e`.
- **Runtime (3E):** the repo's app, 5 fresh apps with concurrent first requests: 1 fd each, 22 of 22 readings
  clean; the driven page (fresh app, then a reload): all five cards, 5-point series, 1 fd. Adjacent paths: a bad
  port still shows D7's error in the grid; no source still gives 503s and the banner. Chrome, the app and the pty
  feeder stopped; ports 5001 and 9333 free. Not covered: a real adapter (none yet).

**Key files:**
- `app.py:22` (`_serial_lock`), `app.py:40-51` (`get_serial_reader()`, the `with` at `:42`).
- `tests/test_serial_routes.py:71-106` (D8's comment and test).
- `.quality-gates.json:27` (`tests-passed`, 129); `docs/planning/test-suite-plan.md:142` (D8's row), `:659` (note).

**Gotchas for the next session:**
- **Session 19's probe scripts are reusable:** `race.py` (fresh app per trial, concurrent or sequential, fd count
  and a clean/garbled count), `page.py` (fresh app, page load, reload, report), `drive.mjs`, and a non-blocking
  `pty_feed.py`, in `/private/tmp/claude-501/-Users-rmsharp-Development-airqino/eeef13f7-f1c6-4ce7-802c-40ea6a5b2cc7/scratchpad/probe/`.
  `race.py` and `page.py` take the app directory as their first argument, so they run on the repo or a copy.
- **A planted delay can be the whole test.** Red-drive the test with its plant removed on the unfixed code: D8's
  passed 10 of 10 without its sleep. Keep the plant, and say why beside it.
- **A reading that's garbled can still parse.** Unfixed, the grid showed plausible numbers and silently dropped
  CO; count clean rows against the exact line fed, not "looks fine".
- **The page's first load shows "Loading readings..."** until a reload or the 60 s refresh (open item 4), so a
  page probe has to reload to see readings.
- **No git hooks are installed**, so run `python3 quality_ratchet.py --precommit` by hand, with the manifest
  staged, before the commit. **Exit codes (learning #10):** redirect to a file, then `echo $?`. **Stage files by
  name** (the 4 untracked files remain, open item 2).
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3).

**Learnings (3C):** `CLAUDE.md` learning #17 (sum a probe's numbers with a script before the commit that states
them).

**Self-assessment:**
- **Score: 7/10**
- (+) Three candidates probed on the real app and the page before choosing, 5 trials each, which settled
  `exclusive=True` (the handoff's by-reading doubt) with evidence.
- (+) The API-side claim was probed before it was stated, and it gave the operator a clear scope decision.
- (+) Test-first, 20 of 20 red and green; the plant itself was red-driven and found load-bearing; 3 product
  red-drives, 1 plant red-drive and 1 gate red-drive, all against the whole suite.
- (+) Each commit held to the 5-file cap, and every moved citation was printed against its line.
- (−) **A false count reached a commit and the ledger again** (2 of 15 for 2 of 14), and I told the operator the
  same wrong number. It is the third session running in which a false claim reached a commit (Sessions 17 and
  18 before it). A recount before the next commit caught it, but after `b53303e`.
- (−) The plan note's first draft omitted that the API probe slowed the constructor, and cited `_get_token` as
  `:21-46` for `:21-47`; both caught before the commit.
- (−) A harness nudge for silence during the red-drives, which repeats Sessions 6–18's minus.

### Session 18 Handoff Evaluation (by Session 19)
- **Score: 9/10**
- **What helped:**
  - Open item 1's race recipe was right in every part: a stand-in whose constructor sleeps, a `threading.Barrier`,
    "assert one reader was built", a lock as the candidate, and "probe from a fresh app with no warm-up". The test
    followed it nearly word for word.
  - "`exclusive=True` looks wrong: the second open would fail, set `error`, and the page would show a port error"
    was labelled a reading, and the probe confirmed it exactly (4 of 5).
  - The `get_api_client()` note ("same shape; by reading, two clients would each fetch a token. Unprobed.") led
    straight to the probe that settled the scope question.
  - The ratchet citation matched `.quality-gates-results.json`, both frontiers sat at `34a0a75` with nothing to
    reconcile, the 6 flags matched `dashboard.html`, and the D5 and D2 citations held.
- **What was wrong:** nothing I found.
- **What was missing:** where Session 18's probe scripts were. They survived in its scratchpad and spared a
  rebuild, but I found them only by listing old scratchpad directories.
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

### Sessions 1–18 (archived by Sessions 6–20)
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
"Session 16 Handoff Evaluation" and "What Session 17 Did": `git show 1af2c49:SESSION_NOTES.md`.
"Session 17 Handoff Evaluation" and "What Session 18 Did": `git show 0ba0bea:SESSION_NOTES.md`.
