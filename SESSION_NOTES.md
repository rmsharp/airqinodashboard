# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** Test suite. `docs/planning/test-suite-plan.md` is approved (Session 10), and **Phases 1–3 are
done**. By the plan's order, the next session implements **Phase 4 only**: the API client and the API-mode routes.
If the serial adapter arrives first, see open item 1.
**Status:**
- **Phase 3: COMPLETE, on `main`.** It is `d0e3b8d` (`tests/test_serial_reader.py`) and `be5723c`
  (`tests/test_serial_routes.py`, the `idle_reader` fixture, and the gate). On the operator's direction, `main` was
  fast-forwarded to the Session 12 branch, which was then deleted. `main` is the only branch, and it is pushed straight
  after the close-out commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `58 passed, 5 xfailed` in about 0.3 s (0.69 s wall). The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results dcc07cbf2359 · manifest fe94344ce1e7`. The gates are
  `tests-exit` (max 0) and `tests-passed` (min 58).
- **Dashboard:** 68/100 (62 before), with High+ risk 0. "Test coverage is very thin" (MEDIUM) has cleared: the test files
  total 576 lines. The remaining flags are two MEDIUMs, "No CI/CD pipeline" and a large file (the synced
  `docs/methodology/tools/methodology_dashboard.py`), and one LOW, "No LICENSE file".
- **Defects (plan §4):** D1, D2's timeseries half, D3, D4 and D7 now have strict xfails. D5, D6 and D2's hourly half
  get theirs in Phase 4. All 7 are still unfixed.
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- **No product code has changed** since Session 7's fix (`e5f52e1`).
- Earlier status: Session 11's is at `git show e3e7a0a:SESSION_NOTES.md`, Session 10's at `git show fbacf96:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Implement Phase 4 of the test-suite plan (recommended next, the plan's order).** It is plan §5 "Phase 4"
   (`docs/planning/test-suite-plan.md:450-537`):
   - files: `tests/test_airqino_client.py` (T4.1–T4.9), `tests/conftest.py` (`FakeRequests`, `FakeClock`,
     `FakeClient`), `tests/test_api_routes.py` (T4.10–T4.15, with the D5, D6 and D2-hourly strict xfails) and
     `.quality-gates.json` (tighten `tests-passed`);
   - four commits: the claim; `test_airqino_client.py`, `conftest.py` and a ledger entry; `test_api_routes.py`, the
     gate and a ledger entry; the close-out;
   - DONE: the suite exits 0 with exactly 8 xfailed, the ratchet passes 2/2 at the tightened threshold, one red-drive
     is recorded (`- 30` → `+ 30` at `airqino_client.py:23`), and no product file shows in `git diff`.

   Start on a new branch off `main`. **The alternative:** if the USB-to-TTL adapter is about to arrive, fix D1 and
   then D7 first (plan §6, one session each). Phase 3 now guards the whole serial path. The probes suggest both fixes
   are small: a split on `;` *or* `,` (never both) fixed D1 and kept all 26 reader tests green, and a 2-line 503 for
   a reader error fixed D7. That was a probe, not a design, so the fix sessions keep their freedom. The API path has
   no credentials yet, so Phase 4 guards code that can't be used yet.
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

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 13 Did
**Deliverable:** Implement Phase 4 of `docs/planning/test-suite-plan.md` (open item 1): the API client and the
API-mode routes (IN PROGRESS)
**Started:** 2026-09-17 23:04
**Status:** Session claimed on branch `test/suite-phase4` (off `main` `ace379d`). The operator picked Phase 4 in the
Phase 0 picker. Work beginning.
**Ledger:** `CHANGELOG: pending` — the claim commit's `CHANGELOG.md` entry says (in progress); Phase 3F records the rest. Until close-out, this line is the crash breadcrumb for the next session's reconcile.

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

### Session 10 Handoff Evaluation (by Session 11)
- **Score: 9/10**
- **What helped:**
  - Open item 1 was an exact recipe: the file, the three-commit shape and the DONE list. Its `app.py` citations
    (`:171`, `:245`, `:261`) all held, and the plan's red-drive (`.lower()` at `:261`) failed T2.4 as described.
  - The Phase 2 probe (a global set by a route is reset between tests) meant the upload tests needed no cleanup of
    their own, and "don't copy `planted_leak`" saved a fixture.
  - Every gotcha got used: `--precommit` by hand, "passed" kept out of `reason=`, files staged by name, an untracked
    file backed up to the scratchpad before a red-drive, and the 548-line bar for the MEDIUM "thin" (342 now).
  - The git state matched: `main` = `origin/main` = `fbacf96`, one branch, and the receipt's ratchet citation matched
    `.quality-gates-results.json`.
- **What was missing:** that the suite's `client` runs with `TESTING` on, so a route's exception reaches the test and
  no 500 comes back. The plan's D2 and D3 assertions (`status_code < 500`) assume a 500. That gap is Session 9's plan,
  not this handoff, and a probe caught it before any test was written.
- **What was wrong:** one gotcha. "The ratchet's `results` hash changes with each run" isn't so. The hash covers the
  results, not the run time (`quality_ratchet.py:171`): two green runs minutes apart both gave `0dc3acde972e`.
  Harmless, since citing the final run is still right.
- **ROI:** strongly positive. Phase 0 to a green Phase 2 needed no rediscovery.

### What Session 11 Did
**Deliverable:** Implement Phase 2 of `docs/planning/test-suite-plan.md` (open item 1): the no-source contract and the
CSV path — **COMPLETE**
**Started / Closed:** 2026-09-17 22:29. Claimed on branch `test/suite-phase2` off `main` `fbacf96`. Closed on `main`
after a fast-forward and pushed (`803a785`). Close-out amended after the operator had squash and rebase merges turned
off (learning #8); the amended close-out is pushed straight after it is made.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 2", the approved
contract. At the start, `git diff --stat 15b0a3f` over the product files was empty, so the contract still held.
**Ledger:** 7 `CHANGELOG.md` entries: the claim, the tests (commit 2), the fast-forward and push, the branch deletion,
the first close-out, the merge-settings change, and this amended close-out.

**What was done:**
- **Phase 0:** before picking, the operator asked what open item 4 means. Answer: GitHub's squash and rebase merges
  rewrite SHAs, so once the branch is deleted, every ledger, receipt and `git show <sha>:SESSION_NOTES.md` citation
  of its commits points at nothing. `gh repo view` showed all three methods enabled. The operator picked Phase 2, and
  the item was done after close-out (below).
- **Claim** `7d02af9`.
- **Probe first** (learning #7), in the scratchpad, against the repo's `app.py` through the test client with
  `TESTING` on. Every T2.x behaviour the plan claims held. Three findings:
  - D2 raises `ValueError` and D3 `AttributeError` into the caller; neither returns a 500;
  - an empty upload leaves `has_csv: true` with `source: null` (open item 4);
  - CSV mode ignores `?hours=` (open item 4).
- **Tests** `fa73763`: `tests/test_csv_routes.py` (176 lines), 19 passing tests and 3 strict xfails;
  `.quality-gates.json` `tests-passed` 9 → 28. **Change from the plan's text:** each xfail names its exception
  (`raises=ValueError`, `AttributeError`, `AssertionError`), so any other failure reports as FAILED. The plan records
  this in an "As implemented (Session 11)" note under Phase 2's DONE list.
- **Red-drives**, in the working tree. `app.py` was backed up to the scratchpad and restored with `git checkout`
  (shasum `9ede4c1…` before and after):
  1. `.lower()` removed at `app.py:261`: T2.4 fails (the plan's example);
  2. `data[-500:]` → `data[:500]`: the last-500 test fails;
  3. `_csv_data[-1]` → `_csv_data[0]`: the last-row test fails;
  4. the `;` branch disabled: T2.3's semicolon case fails;
  5. `utf-8` → `utf-8-sig`, a real D4 fix: `XPASS(strict)` fails the suite, so a fix can't land with its marker on;
  6. one test hidden from collection: `tests-passed` fails (measured 27). The untracked test file was backed up by
     explicit path to the scratchpad first and restored byte-identical.
- **Forward claims probed:** D2's hourly half raises `ValueError` under `TESTING` too, and D1 fails as an
  `AssertionError` (`_parse_line("co=235;no2=17")` → `{'co': '235;no2=17', 'no2': 17.0}`).
- **Landing:** the operator picked "fast-forward main + push" in a picker before close-out (learning #8). After a
  `git fetch`, `origin/main` = `fbacf96` was an ancestor of the branch, and a scan of the added lines found no secrets
  or local paths. Then `git merge --ff-only` and `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 8 Handoff Evaluation" and "What Session 9 Did" were archived
  (`git show fa73763:SESSION_NOTES.md`).
- **First close-out** `803a785`, pushed to `origin/main`.
- **Follow-on action, directed by the operator after that close-out:** the operator asked why I had recommended
  delaying the merge-settings item. I had no good reason. I ranked it behind the active test campaign under
  1-and-done, and treated "needs your go-ahead" as "can wait". The exposure is small today (no open PRs, and landings
  are fast-forwards), but the fix is one reversible command. The operator said to go ahead:
  - `gh repo edit rmsharp/airqinodashboard --enable-squash-merge=false --enable-rebase-merge=false`. `gh repo view`
    before: merge, squash and rebase all `true`; after: `mergeCommitAllowed: true`, `squashMergeAllowed: false`,
    `rebaseMergeAllowed: false`.
  - `CLAUDE.md` learning #6 now records the gate, and that it covers PR merges only (local squash and rebase still
    work).
  - The old open item 4 is removed; the CSV findings are now item 4.

**Verification:**
- **Plan §5 P2 DONE, every item met:**
  - `python3 -m pytest -q` and plain `pytest -q` both give `28 passed, 3 xfailed` and exit 0;
  - the ratchet passes 2/2 at 28 (summary line in ACTIVE TASK), and `--precommit` passed on the staged manifest;
  - the red-drives are recorded (above);
  - `git diff --stat main -- app.py airqino_client.py serial_reader.py templates static requirements.txt` is empty.
- **Runtime (3E):** tests only, so no product runtime behaviour changed. The suite drives every route through Flask's
  test client with in-memory multipart uploads. The browser's drag-and-drop and `FormData` path
  (`dashboard.js:407-450`) and real SD-card files stay unverified, as the plan's Phase 2 surface says.

**Key files:**
- `tests/test_csv_routes.py`:
  - `:26` (`upload`, the multipart helper), `:37` (`csv_text`);
  - `:41` (T2.1, the no-source table);
  - `:101` (`uploaded_501`);
  - `:159`, `:165` and `:172` (the three xfails).
- `.quality-gates.json:24-32` (`tests-passed`, min 28; its threshold is at `:27`)
- `docs/planning/test-suite-plan.md:341` (the "As implemented (Session 11)" note)
- For Phase 3:
  - `docs/planning/test-suite-plan.md:357` (Phase 3), `:417` (its red-drive);
  - `serial_reader.py:62-68` (`_read_loop` and the open failure D7 swallows), `:89` (`_parse_line`; D1 at
    `:106-117`), `:140` (`_normalize`; the red-drive's `"humidity": "rh"` at `:147`), `:154` (`get_current`), `:158`
    (`get_history`);
  - `app.py:38-48` (`get_serial_reader()`, which starts a real thread), `:141-147` (the serial branch of
    `/api/current`), `:175-183` (the serial branch of `/api/timeseries`).

**Gotchas for the next session:**
- **Under `TESTING`, a route's exception reaches the test.** Name the exception each xfail expects with `raises=`, as
  `tests/test_csv_routes.py` does. D1 and D7 both fail on an assertion today (D1 returns a string; D7 answers 200), so
  both take `raises=AssertionError`.
- **`isolated` resets `_serial_reader` but stops no thread.** Any test that sets `SERIAL_PORT` and calls a data route
  starts a real daemon thread through `get_serial_reader()` (`app.py:47`). For D7 the thread ends by itself, because
  the open failure sets `_running = False` (`serial_reader.py:68`). Elsewhere call `stop()`. Never `join()`.
- **The plan's own line numbers moved** by 7 after Session 11's note. Its product-code citations didn't. Use the
  numbers above, or `grep -n`.
- **Keep "passed" out of `reason=` strings.** The `tests-passed` regex scans the `-ra` output.
- **The ratchet's `results` hash changes only when a measurement does.** Cite the summary line from the final run.
- **Stage files by name.** `.quality-gates-results.json`, `.context-budget-history.jsonl`, `dashboard_history.jsonl`
  and `docs/HARDWARE.html` are still untracked (open item 2).
- **Back up a new, untracked test module by explicit path to the scratchpad** before a red-drive mutates it.
  `tests/conftest.py` is tracked, so `git checkout --` restores it.
- **The MEDIUM "thin" stays until the test files total 548 lines.** They are 342 now. Don't pad.

**Learnings (3C):** none new. The D2/D3 surprise is learning #9 again: Session 9 probed the routes without `TESTING`,
and its 500s didn't carry over to the suite's `client`, whose setup differs. Probing on the suite's own fixture
(learning #7) caught it before any test was written.

**Self-assessment:**
- **Score: 7/10.** The first close-out scored itself 8. One point comes off for the ranking miss below.
- (+) Every behaviour the tests assert was probed on the suite's own setup first. That surfaced the `TESTING`
  difference and two findings the plan doesn't have.
- (+) Six red-drives: each targeted test failed on its own break, a real D4 fix proved the strict-xfail flip, and the
  tightened gate refused 27.
- (+) Scope held: no product code, 3 files in commit 2, and the two findings went to open item 4, not into tests.
- (+) The landing was decided before close-out (learning #8), so this handoff describes the session's real end.
- (+) The handoff's forward claims (D1's and D2-hourly's failure modes) were probed, not reasoned.
- (−) Four harness nudges for silence during long runs of tool calls. That repeats a Session 6–10 minus.
- (−) The first suite run checked `$?` after a pipe, so it reported `tail`'s exit code, not pytest's. The next command
  re-ran it properly (exit 0), but for one step it was a check that couldn't fail.
- (−) The first Phase 0 picker described the merge-settings item by its command, not its consequence, so the operator
  had to ask what it meant before choosing.
- (−) I ranked that item behind Phase 2 without weighing it on its merits, and the close-out report left it parked.
  The operator had to ask why. A one-command, reversible guard against a silent failure should have been recommended
  for immediate action. That miss costs the point: 8 → 7.
- (−) A draft of this handoff cited `.quality-gates.json:196`, a line number read off a `cat -n` of three files at
  once, which numbers them as one listing. The pre-commit re-grep caught it (the gate is at `:24-32`). It's learning
  #7's failure again: a line number read by eye, not grepped.

### Sessions 1–10 (archived by Sessions 6–12)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
"Session 9 Handoff Evaluation" and "What Session 10 Did": `git show be5723c:SESSION_NOTES.md`.
