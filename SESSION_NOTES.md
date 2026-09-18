# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete. All four phases of `docs/planning/test-suite-plan.md` are on
`main`, and every defect in its §4 has a strict xfail. Next come the plan's fix sessions (§6), one defect per
session, with D1 and then D7 first (open item 1).
**Status:**
- **Phase 4: COMPLETE, on `main`.** It is `0e5ed0d` (`tests/test_airqino_client.py`, `FakeRequests`, `FakeClock`)
  and `5084680` (`tests/test_api_routes.py`, `FakeClient`, the gate). On the operator's direction, `main` was
  fast-forwarded to the Session 13 branch, which was then deleted. `main` is the only branch, and it is pushed straight
  after the close-out commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `116 passed, 8 xfailed` in about 0.35 s (0.75 s wall). The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 263dc2f189c8 · manifest 970ed02cfdc1`. The gates are
  `tests-exit` (max 0) and `tests-passed` (min 116).
- **Dashboard:** 68/100, unchanged, with High+ risk 0. The flags are unchanged too: two MEDIUMs ("No CI/CD pipeline",
  and a large file, the synced `docs/methodology/tools/methodology_dashboard.py`) and one LOW ("No LICENSE file").
  The test files total 1,091 lines.
- **Defects (plan §4):** all 7 have strict xfails, 8 tests in all (D2 has two). All 7 are still unfixed.
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- **No product code has changed** since Session 7's fix (`e5f52e1`).
- Earlier status: Session 12's is at `git show ace379d:SESSION_NOTES.md`, Session 11's at `git show e3e7a0a:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D1 (recommended next), then D7: the plan's fix sessions (§6), one defect per session.** The plan's order is
   D1 and D7 first, because the serial path is the next to be used, then D3 and D4, then D6, D5 and D2. Each session,
   on a new branch off `main`:
   - removes the defect's `xfail` marker and watches its test fail on the unfixed code;
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by 1 (by 2 for D2, which has two tests);
   - runs learning #5's runtime check for D1, D3, D4 and D7, which are user-visible;
   - red-drives the fix against the whole suite (learning #11).

   Where each one is:
   - **D1:** `serial_reader.py:106-117`; its xfail is `tests/test_serial_reader.py:157` (marker `:154`). A Session 12
     probe fixed it by splitting on `;` *or* `,`, never both, and kept all 26 reader tests green.
   - **D7:** `serial_reader.py:64-69` and `app.py:141-147`; its xfail is `tests/test_serial_routes.py:54` (marker
     `:51`). A 2-line 503 for a reader error fixed it in a probe. Open item 4's third finding bears on its design.
   - **D2:** `app.py:171` and `:220`; its xfails are `tests/test_csv_routes.py:160` and `tests/test_api_routes.py:213`.
   - **D3, D4:** `tests/test_csv_routes.py:167`, `:174`.
   - **D5:** `app.py:53`; its xfail is `tests/test_api_routes.py:194`. **A real D5 fix also fails Phase 1's T1.5**
     (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`. That session must set all four
     credentials in T1.5 as well.
   - **D6:** `app.py:53-58`; its xfail is `tests/test_api_routes.py:205`.

   The probe fixes were probes, not designs, so each fix session keeps its freedom.
2. **Decide the untracked files.** For each one, commit, gitignore or delete; that's the operator's call.
   - `docs/HARDWARE.html` has been untracked since Session 3. It is an HTML render of `docs/HARDWARE.md` and holds no
     stale hardware copy.
   - Three tool outputs, all present now, have no `.gitignore` entry: `dashboard_history.jsonl` (written by every
     dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`, which the `.quality-gates.json`
     seed says to gitignore); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence
   missing: `.context-budget.json` declares it for `CLAUDE.md`, with a minimum of 800 B. `CLAUDE.md` has never had a
   fence or a Purpose section, and `README.md`'s opening is the source text. The same tool also reports
   `SESSION_NOTES.md` as "instrument-failed". `.context-budget.json` expects at least 2 `^## ` headings, but this
   file has 1, and so does the synced seed `docs/methodology/starter-kit/SESSION_NOTES.md`. That's a mismatch inside
   the methodology's own files. Raise it upstream rather than restructuring this file to satisfy it.
4. **Decide three findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:87` checks
     `_csv_data is not None`, but `active_source()` (`:57`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode **and in serial mode** (the serial half is new in Session 12). CSV returns the
     last 500 rows (`app.py:203-208`), and serial returns `get_history(limit=500)` (`:177`), whatever the range. So
     the chart's 6h–30d buttons (`templates/dashboard.html:86-91`) change nothing outside API mode.
   - In D7's state, `/api/timeseries` answers 200 with `data: []` (Session 12 probe). A D7 fix that only changes
     `/api/current` leaves the chart silent about the port error.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. This session's 21 red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:160`), which is 30
   days apart. `README.md:108` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### Session 12 Handoff Evaluation (by Session 13)
- **Score: 9/10**
- **What helped:**
  - Open item 1 was an exact recipe: the files, the four-commit shape, the DONE list and the red-drive.
  - Every citation for Phase 4 held when read this session: `airqino_client.py:8`, `:21`, `:23`, `:30`, `:45`, `:49`,
    `:115`, `:137`; `app.py:51-59`, `:76`, `:92`, `:108`, `:214`, `:220`; plan `:450` and `:521`.
  - The gotchas got used and were right:
    - there is no `FakeReader`, so use `idle_reader`;
    - D6's assertion is on `active_source()`, which reads only the environment. That led straight to the check of
      how D5 and D6 interact;
    - learning #10 (no exit code was read after a pipe this session);
    - keep "passed" out of `reason=`, and stage by name;
    - back up the untracked test module by explicit path (used for the gate's red-drive).
  - The git state matched: `main` = `origin/main` = `ace379d`, and the receipt's ratchet citation matched the results
    file (`dcc07cbf2359`, reproduced at Phase 0).
- **What was missing:** nothing this handoff could have known. The two gaps were older. Phase 1's T1.5 pins D5, which
  only a real D5 fix run against the whole suite shows. The plan's `README.md` citations had moved 9 lines when Phase
  1 added a section. The handoff's "its product citations didn't move" was true, but README isn't product code, and
  I copied the plan's `README.md:27` into a test comment before re-grepping it.
- **What was wrong:** nothing I found.
- **ROI:** strongly positive. Phase 0 to a green Phase 4 needed no rediscovery.

### What Session 13 Did
**Deliverable:** Implement Phase 4 of `docs/planning/test-suite-plan.md` (open item 1): the API client and the
API-mode routes — **COMPLETE**
**Started / Closed:** 2026-09-17 23:04. Claimed on branch `test/suite-phase4` off `main` `ace379d`. Closed on `main`
after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 4", the approved
contract. At the start, `git diff --stat 15b0a3f` over the product files was empty, so the contract still held.
**Ledger:** 5 `CHANGELOG.md` entries: the claim, the client tests, the route tests, the branch deletion, and this
close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `5c52bf4`. The operator picked Phase 4 in the Phase 0 picker.
- **Probe first** (learning #7), in the scratchpad. The harness loaded the repo's own `tests/conftest.py` with
  `importlib`, so the routes ran on the suite's `isolated` and `client` fixtures (learning #9). 23 client probes and
  20 route probes were run against drafts of the three fakes. Every T4.x claim held, and D2-hourly, D5 and D6
  reproduced. Nothing surprised, apart from two notes:
  - the chart's 30 d button asks `getRange` for a span exactly 30 days apart (open item 7);
  - `/api/hourly` returns its values as strings. It has no front-end caller, so this is not an open item.
- **Client tests** `0e5ed0d`: `tests/test_airqino_client.py` (175 lines), 25 passing tests (T4.1–T4.9), plus
  `FakeResponse`, `FakeRequests` (`grant`, `refuse`, `answer`) and `FakeClock` in `tests/conftest.py`.
- **Route tests and gate** `5084680`: `tests/test_api_routes.py` (215 lines), 33 passing tests (T4.10–T4.15 and
  `get_api_client()`) and 3 strict xfails (D5, D6, D2-hourly). `FakeClient` and `fake_client` went into
  `tests/conftest.py`, and `tests-passed` was tightened from 58 to 116.
- **Changes from the plan's text,** recorded in its "As implemented (Session 13)" note:
  - `FakeClient` has only the 7 methods `app.py` calls, and binds each call to the real signature;
  - D6 uses `idle_reader` and all four credentials, and T4.15 sets all four too;
  - token requests are routed by `grant_type`, with the URL constants written out in the tests;
  - `get_api_client()` gets tests;
  - T1.5 pins D5 (below).
- **Red-drives**, in the working tree, each restored with `git checkout`, with the shasum the same before and after
  (`airqino_client.py` `8a7c798…`, `app.py` `9ede4c1…`):
  - `airqino_client.py` (10), each failing only its target. The plan's `- 30` → `+ 30` at `:23` failed T4.3, T4.4 and
    T4.5. The others: `"scope"` removed and the password timeout 15 → 30 (T4.1), the `expires_in` default → 600
    (T4.5), a re-raised refresh failure (T4.4), `pivot` never sent (T4.7), the `getSingleDay` path (its T4.6 row),
    `centraline` renamed (T4.8), `_get` without `raise_for_status()` (T4.9), and a refresh sending the access token (T4.3).
  - `app.py` (11), run against the whole suite:
    1. `hours <= 12` → `< 12`: the 12 h row;
    2. `?days=` ignored: the `days=3` row;
    3. the hourly delimiter `;` → `,`: both hourly rows;
    4. `info[0]` → `info[-1]`: the no-match and no-station metadata tests;
    5. `?project=` ignored: its stations row;
    6. the current route's 502 → 500: its 502 row;
    7. `get_range` called with 2 arguments: every range test, through `FakeClient`'s signature check;
    8. a real D5 fix: XPASS(strict), and T1.5 fails (below). At first, D6 flipped too;
    9. a real D6 fix: XPASS(strict) on D6 only;
    10. a real D2-hourly fix: XPASS(strict) on it only;
    11. `get_api_client()` needing only three credentials: the missing-password case.
  - **The D5 fix red-drive found two tests pinning D5.** My D6 test and T4.15 set only `AIRQINO_CLIENT_ID`. Both were
    changed to set all four credentials before the commit, and a re-run showed D5 and D6 each flipping only their
    own test. Phase 1's T1.5 (`tests/test_dashboard_page.py:97`) does the same. It's outside Phase 4's files, so it
    went into open item 1 for the D5 session (learning #11).
  - The gate: with one test hidden, `tests-passed` measured 115 and the ratchet exited 2. The untracked module was
    backed up by explicit path and restored byte-identical (`cmp`).
- **Landing:** the operator picked "fast-forward main + push" in a picker before close-out (learning #8). After a
  `git fetch`, `origin/main` = `ace379d` was an ancestor of the branch. A scan of the added lines found no secrets or
  local paths; its two hits were test names containing "password_grant". Then `git merge --ff-only` and `git branch
  -d`, with the push after this commit.
- **FM #28 reduction:** "Session 10 Handoff Evaluation" and "What Session 11 Did" were archived
  (`git show 5084680:SESSION_NOTES.md`).

**Verification:**
- **Plan §5 P4 DONE, every item met:**
  - `python3 -m pytest -q` and plain `pytest -q` both give `116 passed, 8 xfailed` and exit 0, read with a redirect
    and no pipe;
  - the ratchet passes 2/2 at 116 (the summary line is in ACTIVE TASK), and `--precommit` passed on the staged
    manifest;
  - the red-drives are recorded (above);
  - `git diff --stat HEAD -- app.py airqino_client.py serial_reader.py templates static requirements.txt` was empty
    before commit 3.
- **Runtime (3E):** tests only, so no product runtime behaviour changed. The real `AirQinoClient` and the real routes
  ran, with only `requests`, `time` and `utcnow` faked. **Not verified, and not verifiable yet:** that the real API
  accepts any request (no credentials), plus its response shapes, the Keycloak realm and the 30-day `getRange` cap
  (open item 7).

**Key files:**
- `tests/conftest.py`:
  - `:49` (`FakeResponse`), `:65` (`FakeRequests`; `grant` `:80`, `refuse` `:87`, `answer` `:91`), `:108`
    (`FakeClock`);
  - `:119` (`fake_requests`), `:126` (`fake_clock`);
  - `:133` (`FakeClient`; the signature binding is in `__getattr__`, `:149`), `:164` (`fake_client`).
- `tests/test_airqino_client.py`: `:23` (`api`), `:35` (T4.1), `:94` (the T4.6 table), `:163` (T4.9).
- `tests/test_api_routes.py`:
  - `:46` and `:56` (`get_api_client`), `:83` (the 502 table), `:146` (serial before the API), `:162` (T4.13);
  - `:194` (D5), `:205` (D6), `:213` (D2-hourly).
- `tests/test_dashboard_page.py:97` (T1.5, which pins D5).
- `.quality-gates.json:27` (`tests-passed`, 116).
- `docs/planning/test-suite-plan.md`: `:526` (the "As implemented (Session 13)" note), and §6 (the fix sessions).

**Gotchas for the next session:**
- **A fix session removes a marker, then red-drives the fix against the whole suite** (learning #11). For D5 that
  means T1.5 fails too; set all four credentials there.
- **D2 has two xfails** (`tests/test_csv_routes.py:160`, `tests/test_api_routes.py:213`), so its fix tightens
  `tests-passed` by 2, not 1.
- **Every test that sets all four credentials and calls a data route must install `fake_client`** (or
  `fake_requests`). Otherwise `get_api_client()` builds a real client, and the route sends a real request to
  magentalab.it. `test_status_in_api_mode` is safe without one, because `/api/status` never calls
  `get_api_client()`.
- **`FakeClient` refuses methods it doesn't list.** If a fix makes `app.py` call a new client method, add it to
  `FakeClient.METHODS` (`tests/conftest.py:133`). Until then the call fails, is caught, and shows as a 502.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`.
- **`git rev-parse --short` takes one revision.** Given two, it fails, and a following `&&` skips the next check.
- **Keep "passed" out of `reason=` strings,** and **stage files by name** (the 4 untracked files remain, open item 2).
- **The ratchet's `results` hash changes only when a measurement does.** Cite the summary line from the final run.

**Learnings (3C):** `CLAUDE.md` learning #11: a real-fix red-drive tests the other tests too. Configure state next to
a defect fully, and run the fix against the whole suite.

**Self-assessment:**
- **Score: 8/10**
- (+) Every asserted behaviour was probed first on the suite's own fixtures, 43 probes in all, before a test was
  written.
- (+) 21 red-drives on product code and 1 on the gate. The real D5, D6 and D2-hourly fixes proved each strict-xfail
  flip, and the `get_range` mutation proved `FakeClient`'s signature check.
- (+) The whole-suite D5 red-drive found three tests pinning a known defect: two of mine (fixed before the commit) and
  Phase 1's T1.5 (handed off, not edited, since it's outside the contract).
- (+) Scope held: no product code, commits of 3 and 4 files, and the landing decided before close-out (learning #8).
- (+) No exit code was read after a pipe (learning #10 held).
- (−) I wrote D6 and T4.15 with only `AIRQINO_CLIENT_ID` set, which pins D5, the very thing plan §7 rejects. Only
  the red-drive caught it.
- (−) A test comment cited `README.md:27`, copied from the plan without a re-grep (learning #7's failure). The first
  run's output check caught it before the commit.
- (−) A `git rev-parse --short` with two arguments failed and skipped the ancestor check behind it. The output gave it
  away, and it was re-run.
- (−) The first draft of a ledger entry used a nested list, unlike the ledger's one-line bullets. Fixed before the
  commit.
- (−) Four harness nudges for silence during long runs of tool calls, which repeats the Session 6–12 minus.

### Session 11 Handoff Evaluation (by Session 12)
- **Score: 9/10**
- **What helped:**
  - Open item 1 was an exact recipe: the files, the four-commit shape and the DONE list.
  - Every product citation held when read this session: `serial_reader.py:62-68`, `:89`, `:106-117`, `:140`, `:147`,
    `:154`, `:158` and `app.py:38-48`, `:141-147`, `:175-183`, plus plan `:357` and `:417`.
  - The gotchas got used and were right:
    - D1 and D7 both fail on an assertion (probed), so both take `raises=AssertionError`;
    - `isolated` stops no thread, and D7's thread ends by itself (`_running` was `False` within 13 ms);
    - never `join()`;
    - keep "passed" out of `reason=`;
    - stage files by name;
    - back up an untracked test module before a red-drive (used for the gate's).
  - "The hash changes only when a measurement does" held: `0dc3acde972e` reproduced at Phase 0.
  - The git state matched: `main` = `origin/main` = `e3e7a0a`, and the receipt's ratchet citation matched the results
    file.
- **What was missing:** the pipe exit-code trap. Session 11 recorded it only as a self-assessment minus, not as a
  gotcha, and I hit it twice: zsh left `PIPESTATUS` empty, and later `$?` after `| grep`. It's learning #10 now. The
  plan's T3.6 also doesn't say that pyserial flushes input on open. That gap is Session 9's plan, not this handoff,
  and a probe caught it.
- **What was wrong:** nothing I found. The "548-line bar" held: the MEDIUM "thin" cleared at 576 lines.
- **ROI:** strongly positive. Phase 0 to a green Phase 3 needed no rediscovery.

### What Session 12 Did
**Deliverable:** Implement Phase 3 of `docs/planning/test-suite-plan.md` (open item 1): the serial path — **COMPLETE**
**Started / Closed:** 2026-09-17 22:50 / 23:01. Claimed on branch `test/suite-phase3` off `main` `e3e7a0a`. Closed on
`main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 3", the approved
contract. At the start, `git diff --stat 15b0a3f` over the product files was empty, so the contract still held.
**Ledger:** 5 `CHANGELOG.md` entries: the claim, the reader tests, the route tests, the branch deletion, and this
close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `1c21529`. The operator picked Phase 3 in the Phase 0 picker.
- **Probe first** (learning #7), in the scratchpad against the repo's code, with the routes run on the suite's own
  `isolated` and `client` fixtures (learning #9). Every T3.x behaviour the plan claims held, and D1 and D7 reproduced.
  New facts:
  - pyserial flushes input when it opens the port, so a line written to the pty before the open is lost;
  - serial mode ignores `?hours=` too (open item 4);
  - in D7's state, `/api/timeseries` answers 200 with `data: []` (open item 4);
  - `get_history(0)` returns everything, because `items[-0:]` is the whole list. No caller passes 0, so it isn't an
    open item;
  - `pytest.fail` inside `xfail(raises=AssertionError)` reports FAILED, never XFAIL.
- **Reader tests** `d0e3b8d`: `tests/test_serial_reader.py` (158 lines), 26 passing tests and the D1 strict xfail.
- **Route tests and gate** `be5723c`: `tests/test_serial_routes.py` (63 lines), 4 passing tests and the D7 strict xfail;
  `idle_reader` in `tests/conftest.py`; `tests-passed` tightened from 28 to 58.
- **Changes from the plan's text**, recorded in its "As implemented (Session 12)" note:
  - `idle_reader` (a real `SerialReader`, never started) replaces the hand-written `FakeReader`, so no copy of
    `get_current` or `get_history` can drift. It also moved to commit 3, where it is first used;
  - T3.6 writes only after the port is open;
  - the D7 poll's timeout calls `pytest.fail`.
- **Red-drives**, in the working tree. The files were backed up to the scratchpad and restored with `git checkout`,
  with the shasum the same before and after (`serial_reader.py` `6f355ba…`, `app.py` `9ede4c1…`):
  - `serial_reader.py` (7), each failing only its target:
    1. `"humidity": "rh"` deleted (the plan's example): T3.2's humidity case and T3.1's json-aliases case fail;
    2. `start()`'s guard removed: T3.5;
    3. `.strip()` → `.rstrip("\n")`: T3.6 (`raw_line` keeps the `\r`);
    4. a naive `datetime.now()`: T3.6 (no UTC offset);
    5. a real D1 fix: XPASS(strict), with the other 26 green;
    6. `deque()` with no `maxlen`: T3.4's drop test;
    7. `_running` left `True` on an open failure: T3.7, after its 2 s deadline.
  - `app.py` (5):
    1. the no-data answer made 200: T3.8's 202 test;
    2. the `values` reshape removed: T3.9's filter test;
    3. a real D7 fix (503 on a reader error): XPASS(strict);
    4. `_serial_reader.start()` removed: D7 reports FAILED ("never reported"), not XFAIL;
    5. `limit=500` → `limit=1`: both T3.9 tests.
  - The gate: with one test hidden, `tests-passed` measured 57 and the ratchet exited 2. The untracked test module was
    backed up by explicit path first and restored byte-identical (`cmp`).
- **Landing:** the operator picked "fast-forward main + push" in a picker before close-out (learning #8). After a
  `git fetch`, `origin/main` = `e3e7a0a` was an ancestor of the branch. A scan of the added lines found no secrets or
  local paths; its one hit was the test id `non-numeric-token`. Then `git merge --ff-only` and `git branch -d`, with the
  push after this commit.
- **FM #28 reduction:** "Session 9 Handoff Evaluation" and "What Session 10 Did" were archived
  (`git show be5723c:SESSION_NOTES.md`).

**Verification:**
- **Plan §5 P3 DONE, every item met:**
  - `python3 -m pytest -q` and plain `pytest -q` both give `58 passed, 5 xfailed` and exit 0, captured with a
    redirect, not a pipe;
  - the ratchet passes 2/2 at 58 (the summary line is in ACTIVE TASK), and `--precommit` passed on the staged manifest;
  - the red-drives are recorded (above);
  - the suite runs in 0.27 s by pytest's count, 0.69 s wall;
  - `git diff --stat HEAD -- app.py airqino_client.py serial_reader.py templates static requirements.txt` was empty
    before commit 3.
- **Runtime (3E):** tests only, so no product runtime behaviour changed. T3.6 runs the real reader thread and real
  pyserial against a real tty device (`/dev/ttys008` in the probe). Four things stay unverified, as the plan's Phase 3
  surface says: the REV6 board's real output format, the baud rate, the 3.3 V logic levels and the adapter's driver.

**Key files:**
- `tests/test_serial_reader.py`:
  - `:21` (`unstarted`), `:26` (`poll`);
  - `:53` (T3.1), `:64` (T3.2), `:103` (T3.5);
  - `:115` (`pty_port`), `:124` (T3.6), `:145` (T3.7);
  - `:157` (the D1 xfail; its marker is at `:154`).
- `tests/test_serial_routes.py`: `:23` and `:30` (T3.8), `:37` and `:42` (T3.9), `:54` (the D7 xfail; marker at `:51`).
- `tests/conftest.py:33` (`idle_reader`); `.quality-gates.json:27` (`tests-passed`, 58).
- `docs/planning/test-suite-plan.md:420` (the "As implemented (Session 12)" note).
- For Phase 4:
  - the plan: `:450` (Phase 4), `:521` (its red-drive);
  - `airqino_client.py`: `:8` (`TOKEN_URL`), `:21` (`_get_token`), `:23` (the `- 30` expiry check), `:30` (the
    refresh fallback's `except`), `:45` (the `expires_in` default), `:49` (`_do_refresh`), `:115` (`get_hourly_avg`),
    `:137` (`generate_report`);
  - `app.py`: `:76` (`api_status`), `:92` (`api_stations`), `:108` (`api_metadata`), `:214` (`api_hourly`), `:220`
    (`int(days)`, D2's hourly half).
- For the D1 and D7 fixes: `serial_reader.py:106-117` and `app.py:141-147`.

**Gotchas for the next session:**
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. This shell is zsh, and `$?` after a
  pipe belongs to the pipe's last command.
- **Plan Phase 4 names a `FakeReader` for D6. There isn't one:** use `idle_reader` (`tests/conftest.py:33`). D6's
  assertion is on `active_source()`, which reads only environment variables (`app.py:51-59`).
- **`idle_reader` starts nothing.** A test that sets `SERIAL_PORT` and calls a data route still starts a real thread
  through `get_serial_reader()`. D7 does so on purpose, and its thread ends by itself. Elsewhere call `stop()`, and
  never `join()`.
- **pyserial flushes input on open.** For any pty test, or the first real capture from the adapter, write only after
  `reader._serial is not None`.
- **The plan's own line numbers moved by 15** after Session 12's note, so Phase 4 is at `:450`. Its product-code
  citations didn't move; `airqino_client.py:8`, `:23`, `:30`, `:45` and `:49` were spot-checked.
- **Keep "passed" out of `reason=` strings.** The `tests-passed` regex scans the `-ra` output.
- **The ratchet's `results` hash changes only when a measurement does.** Cite the summary line from the final run.
- **Stage files by name.** The 4 untracked files remain (open item 2).
- **Back up an untracked test module by explicit path** to the scratchpad before a red-drive mutates it.
- **The MEDIUM "thin" has cleared** (576 lines), so there's no line count to chase.

**Learnings (3C):** `CLAUDE.md` learning #10: read an exit code with no pipe in between. It is the Session 11 minus,
which came back because it was recorded as a minus and not as a rule.

**Self-assessment:**
- **Score: 8/10**
- (+) Every asserted behaviour was probed first, including the routes on the suite's own fixtures and `pytest.fail`
  inside a strict xfail. That found the flush-on-open fact before T3.6 was written.
- (+) 13 red-drives and one on the gate. Real D1 and D7 fixes proved the strict-xfail flips, and a reader that is
  never started proved the D7 timeout reports FAILED.
- (+) The plan's `FakeReader` became a real, unstarted reader, so the route tests run the real methods (the
  faithfulness gate). The change is recorded in the plan.
- (+) Scope held: no product code, commits of 2 and 4 files, and the landing decided before close-out (learning #8).
- (−) The pipe exit-code trap came back twice: an empty `PIPESTATUS`, then grep's `0` printed for a ratchet run that
  had exited 2. The output gave both away, and both were re-run properly, but it's Session 11's minus again.
- (−) Three harness nudges for silence during long runs of tool calls, which repeats the Session 6–11 minus.
- (−) A draft of open item 4 stated D7's `/api/timeseries` answer from reasoning. It was probed before the commit and
  held, but it was written before it was probed, against learning #7.

### Sessions 1–11 (archived by Sessions 6–13)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
"Session 9 Handoff Evaluation" and "What Session 10 Did": `git show be5723c:SESSION_NOTES.md`.
"Session 10 Handoff Evaluation" and "What Session 11 Did": `git show 5084680:SESSION_NOTES.md`.
