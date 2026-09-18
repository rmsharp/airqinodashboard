# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14), D7 (Session 15), D3 (Session 16), D4 (Session 17), D6 (Session 18) and D8 (Session 19) are done; D5
and D2 remain (open item 1, D5 recommended next).
**Status:**
- **D8: FIXED, Session 19, on `main`** (`b53303e` fix, test and gate; `927dfe8` the tests' moved citations;
  `1af2c49` plan). D8 is the serial-reader race Session 18 found; the operator added it to plan §4. A module-level
  `threading.Lock` in `get_serial_reader()` (`app.py:40-51`) now covers the check and the build, so the page's two
  concurrent first requests start one reader, not two splitting the port's bytes. `main` was fast-forwarded to the
  Session 19 branch, which was then deleted; `main` is the only branch, pushed straight after the close-out
  commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `129 passed, 3 xfailed` in under 1 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 9706974b83af · manifest 501e3c8538de`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 129).
- **Dashboard:** 68/100, High+ risk 0, the same 6 flags as at Phase 0 (listed from `dashboard.html` after these edits):
  MEDIUM no CI/CD (BL-3) and the synced dashboard's size; LOW no LICENSE (BL-1), the backlog's done-mark format
  (BL-2), and `CHANGELOG.md` and `HANDOFFS.md` past their one-read budget (expected for a ledger).
- **Defects (plan §4):** D1, D3, D4, D6, D7 and D8 fixed. D2 and D5 still have strict xfails, 3 tests in all (D2
  has two).
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing), BL-2 (`- [ ]` checkboxes so the dashboard's
  done-mark check works) and BL-3 (decide whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 18's is at `git show 34a0a75:SESSION_NOTES.md`, Session 17's at `git show be44a02:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D5 (recommended next), then D2.** The order is the operator's call; plan §4 suggested D6, D5, D2. Each
   fix session, on a new branch off `main`:
   - removes the `xfail` marker and watches the test fail on the unfixed code;
   - **before choosing a design, runs the current code and each candidate fix end to end on the surface the user
     sees** (learning #12), from a fresh app, with more than one input. Explain any odd output with a measurement
     before calling it an artifact (learning #16);
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by the measured delta (D8's was 1, a new test; D6's was 4);
   - red-drives the fix against the whole suite with the original marker restored (learning #11), and runs the
     whole suite on the fix alone (that found T3.7 pinning D7; nothing pinned D3, D4, D6 or D8);
   - re-greps every `file:line` citation after editing, including citations into the lines it changed or moved,
     and recounts every number it writes from the saved output with a script (learning #17).

   Where each one is:
   - **D5:** `app.py:58` (the `AIRQINO_CLIENT_ID` check in `active_source()`; `get_api_client()` needs all four
     credentials, `:34`). Its xfail is `tests/test_api_routes.py:227` (marker `:224`). **A real D5 fix also fails
     Phase 1's T1.5** (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`; that session must set
     all four credentials in T1.5 as well. D6's test sets all four in every case with the API, so a D5 fix can't
     flip it.
   - **D2:** `app.py:178` and `:227`; its xfails are `tests/test_csv_routes.py:192` (marker `:191`) and
     `tests/test_api_routes.py:233` (marker `:232`).

   The plan's own `app.py` citations read lower than the code: by 4 past `:142` since D7, by more inside
   `upload_csv` since D3, `:53` for `:55` since D6, and by 1 to 3 more since D8 (all noted in the plan). Use the
   lines above; the tests' own citations are current. Probe fixes carried in these notes are starting points, not
   verified designs.
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
4. **Decide six findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:90` checks
     `_csv_data is not None`, but `active_source()` (`:60`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode and in serial mode. CSV returns the last 500 rows (`app.py:210-215`), and
     serial returns `get_history(limit=500)` (`:184`), whatever the range. So the chart's 6h–30d buttons
     (`templates/dashboard.html:86-91`) change nothing outside API mode.
   - With a port that failed to open, `/api/timeseries` still answers 200 with `data: []` (D7 changed only
     `/api/current`). The chart is empty either way, and the readings grid now shows the error.
   - **(Session 15, probed)** A port that opens and then fails (a pty closed mid-run, standing in for an unplugged
     adapter) is never reported: the reader thread keeps running with `error` `None`, `_read_loop`'s `except`
     (`serial_reader.py:87-88`) sleeps and retries forever, and `/api/current` keeps serving the last reading with
     200. Each reading card shows its timestamp, so the age is visible. Related gaps: the reader never retries a port
     that failed to open (restart needed, now said in `README.md:73`). On a fresh page load the grid shows "Loading
     readings..." until the 60 s refresh or a reload, for readings and a port error alike (Session 19's probes),
     because the first request starts the reader and gets 202.
   - **(Session 16, probed)** A CSV whose first line is blank loads as rows with no columns. `csv.DictReader` takes
     the blank line as the header, so every value is an extra field: the upload answers 200 with `ragged_rows` equal
     to the row count, the source becomes `csv`, and the grid shows "No readings available". It was a 500 before
     D3's fix. The delimiter check (`app.py:254-261`) reads the blank line too.
   - **(new, Session 19, probed in the scratchpad)** `get_api_client()` (`app.py:26-37`) has D8's check-then-build
     shape. With its constructor slowed by 0.05 s, three concurrent first calls built three clients; the page's
     first load sends three API requests (`static/js/dashboard.js:484-486`). A lock there would not help on its
     own: one shared client still sent three token requests to a slow fake endpoint, because `_get_token`
     (`airqino_client.py:21-47`) races too. The cost is extra token requests at startup, nothing corrupted.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here. Re-checked in Session 19's
   Phase 0 against `~/Development/methodology/starter-kit/` (`cmp`): only `SAFEGUARDS.md` differs;
   `SESSION_RUNNER.md` and `methodology_dashboard.py` match.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–19's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:193`), which is 30
   days apart. `README.md:110` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown. It could also settle whether the API's hourly CSV starts with a BOM: `/api/hourly` parses
   `resp.text` (`airqino_client.py:123`, `app.py:233-235`) without D4's `utf-8-sig`, so a BOM there would put D4's
   symptom in API mode.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with the real map and "API KEY REQUIRED / carto.com/basemaps/apikey" stamped across it, not a 4xx,
   so nothing in the app's code or tests would catch it. Sessions 17–19's page screenshots show the stamp across
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

### Sessions 1–17 (archived by Sessions 6–19)
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
