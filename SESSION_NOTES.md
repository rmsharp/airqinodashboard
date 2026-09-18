# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** Test suite. `docs/planning/test-suite-plan.md` is approved (Session 10), and **Phases 1 and 2 are
done**. Next session implements **Phase 3 only**: the serial path.
**Status:**
- **Phase 2: COMPLETE, on `main`.** It is `fa73763`: `tests/test_csv_routes.py` and the tightened gate. On the
  operator's direction, `main` was fast-forwarded to the Session 11 branch, which was then deleted. `main` is the only
  branch. Session 11's close-out commit is pushed straight after it is made, together with `7d02af9` and `fa73763`.
  Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `28 passed, 3 xfailed` in about 0.2 s. The ratchet gives `quality_ratchet:
  2/2 pass · 0 fail · 0 unmeasured · results 0dc3acde972e · manifest 770382cd43d3`. The gates are `tests-exit`
  (max 0) and `tests-passed` (min 28).
- **Dashboard:** 62/100, unchanged, and High+ risk 0. "Test coverage is very thin" (MEDIUM) moved from ratio 0.03 to
  0.06.
- **Defects (plan §4):** D2's timeseries half, D3 and D4 now have strict xfails. D1 and D7 get theirs in Phase 3, and
  D5, D6 and D2's hourly half in Phase 4. All 7 are still unfixed. D1 and D7 hit the serial path the operator is
  about to use.
- **No product code has changed** since Session 7's fix (`e5f52e1`).
- Earlier status: Session 10's is at `git show fbacf96:SESSION_NOTES.md`, Session 9's at `git show 7256c91:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Implement Phase 3 of the test-suite plan (recommended next).** It is plan §5 "Phase 3"
   (`docs/planning/test-suite-plan.md:357-433`):
   - files: `tests/test_serial_reader.py` (T3.1–T3.7, with D1's strict xfail), `tests/conftest.py` (a `FakeReader`
     fixture), `tests/test_serial_routes.py` (T3.8–T3.9, with D7's strict xfail) and `.quality-gates.json` (tighten
     `tests-passed` to the new measured count);
   - four commits: the claim; `test_serial_reader.py`, `conftest.py` and a ledger entry; `test_serial_routes.py`, the
     gate and a ledger entry; the close-out;
   - DONE: the suite exits 0 with exactly 5 xfailed, the ratchet passes 2/2 at the tightened threshold, one red-drive
     is recorded, the suite still runs well under 10 s, and no product file shows in `git diff`.

   Start on a new branch off `main`. P4 (API) and the D1–D7 fixes follow in plan order.
2. **Decide the untracked files.** For each one, commit, gitignore or delete; that's the operator's call.
   - `docs/HARDWARE.html` has been untracked since Session 3. It is an HTML render of `docs/HARDWARE.md` and holds no
     stale hardware copy.
   - Three tool outputs, all present now, have no `.gitignore` entry: `dashboard_history.jsonl` (written by every
     dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`, which the `.quality-gates.json`
     seed says to gitignore); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence
   missing: `.context-budget.json` declares it for `CLAUDE.md`, with a minimum of 800 B. `CLAUDE.md` has never had a
   fence or a Purpose section, and `README.md`'s opening is the source text. The same tool also reports
   `SESSION_NOTES.md` as "instrument-failed" (new in Session 10). `.context-budget.json` expects at least 2 `^## `
   headings, but this file has 1, and so does the synced seed `docs/methodology/starter-kit/SESSION_NOTES.md`.
   That's a mismatch inside the methodology's own files. Raise it upstream rather than restructuring this file to
   satisfy it.
4. **Make learning #6 a gate (operator's call, one command).** GitHub still allows squash and rebase merges, either of
   which would orphan the SHAs the ledger cites. `gh repo edit rmsharp/airqinodashboard --enable-squash-merge=false
   --enable-rebase-merge=false` makes a merge commit the only option. It changes a public repo's settings, so it needs
   the operator's go-ahead. Session 11 explained it at Phase 0 (all three methods are enabled today); the operator
   picked Phase 2 instead.
5. **Decide two CSV-path findings (new in Session 11; the operator's call).** Session 11 found both while probing.
   Neither is in the plan's §4 defect list, and no test pins either:
   - After an empty upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:87` checks
     `_csv_data is not None`, but `active_source()` (`:57`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`.
   - CSV mode ignores `?hours=`. `/api/timeseries` returns the last 500 rows whatever the range (`app.py:203-208`),
     so the chart's 6h–30d buttons (`templates/dashboard.html:86-91`) change nothing for uploaded data.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

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
after a fast-forward, and pushed straight after this commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 2", the approved
contract. At the start, `git diff --stat 15b0a3f` over the product files was empty, so the contract still held.
**Ledger:** 5 `CHANGELOG.md` entries: the claim, the tests (commit 2), the fast-forward and push, the branch deletion,
and this close-out.

**What was done:**
- **Phase 0:** before picking, the operator asked what open item 4 means. Answer: GitHub's squash and rebase merges
  rewrite SHAs, so once the branch is deleted, every ledger, receipt and `git show <sha>:SESSION_NOTES.md` citation
  of its commits points at nothing. `gh repo view` showed all three methods enabled. Item 4 stays open.
- **Claim** `7d02af9`.
- **Probe first** (learning #7), in the scratchpad, against the repo's `app.py` through the test client with
  `TESTING` on. Every T2.x behaviour the plan claims held. Three findings:
  - D2 raises `ValueError` and D3 `AttributeError` into the caller; neither returns a 500;
  - an empty upload leaves `has_csv: true` with `source: null` (open item 5);
  - CSV mode ignores `?hours=` (open item 5).
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
- **Score: 8/10**
- (+) Every behaviour the tests assert was probed on the suite's own setup first. That surfaced the `TESTING`
  difference and two findings the plan doesn't have.
- (+) Six red-drives: each targeted test failed on its own break, a real D4 fix proved the strict-xfail flip, and the
  tightened gate refused 27.
- (+) Scope held: no product code, 3 files in commit 2, and the two findings went to open item 5, not into tests.
- (+) The landing was decided before close-out (learning #8), so this handoff describes the session's real end.
- (+) The handoff's forward claims (D1's and D2-hourly's failure modes) were probed, not reasoned.
- (−) Four harness nudges for silence during long runs of tool calls. That repeats a Session 6–10 minus.
- (−) The first suite run checked `$?` after a pipe, so it reported `tail`'s exit code, not pytest's. The next command
  re-ran it properly (exit 0), but for one step it was a check that couldn't fail.
- (−) The first Phase 0 picker described open item 4 by its command, not its consequence, so the operator had to ask
  what it meant before choosing.
- (−) A draft of this handoff cited `.quality-gates.json:196`, a line number read off a `cat -n` of three files at
  once, which numbers them as one listing. The pre-commit re-grep caught it (the gate is at `:24-32`). It's learning
  #7's failure again: a line number read by eye, not grepped.

### Session 9 Handoff Evaluation (by Session 10)
- **Score: 8/10**
- **What helped:**
  - Open item 1 was an exact recipe: the files, the four-commit shape and the DONE list. The plan's `pytest.ini`
    worked verbatim, and so did its `conftest.py` apart from one unused import.
  - Every gotcha held and got used: don't ban "USB port"; assert on `>No Data Source<`; keep "passed" out of xfail
    reasons; expect the MEDIUM "thin" after P1. It appeared exactly, at ratio 0.03.
  - "Stage files by name" kept 4 untracked files out of every commit.
  - "The amended close-out commit may not be pushed yet" was right: `main` was 1 ahead of origin.
- **What was missing:** only that pytest writes its own `.gitignore` inside `.pytest_cache/`. So the planned
  `.gitignore` line is a backup, not a need. Minor.
- **What was wrong:** the plan's DONE red-drive, "turning `autouse` off fails T1.7" (`test-suite-plan.md:260`).
  On a machine with no `.env` it doesn't. T1.7 as specified checks that the variables are absent, and here nothing
  sets them, so all 9 tests passed with `autouse=False`. The spike got its result from a planted `.env`, and the plan
  generalized that to every machine. I probed it before writing the fixture, and the fix was one fixture (below).
- **ROI:** strongly positive. Going from approval to a green suite needed no rediscovery.

### What Session 10 Did
**Deliverable:** Implement Phase 1 of `docs/planning/test-suite-plan.md` (open item 1): the pytest harness and the
setup-banner guard — **COMPLETE**
**Started / Closed:** 2026-09-17 21:21. Claimed on branch `test/suite-phase1` off `main` `7256c91`. Closed on `main`
after a fast-forward, and pushed straight after this commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 1", the approved
contract. At the start, `git diff 15b0a3f -- '*.py' templates static requirements.txt` was empty, so the contract
still held.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, the harness (commit 2), the wire-up (commit 3), the fast-forward and
push, the branch deletion, and this close-out.

**What was done:**
- **Approval and claim** `02016aa`. The operator approved the plan as written in the Phase 0 picker, and the plan's
  Status line records it.
- **Harness** `067455f`: `requirements-dev.txt`, `pytest.ini`, `tests/conftest.py` and `tests/test_dashboard_page.py`,
  with 9 tests: T1.1–T1.5, T1.6 (twice: station and project set, then the fallback) and T1.7 (twice). Changes from the
  plan's text:
  - **`planted_leak`**, a module-scoped fixture, sets all 8 variables and fills the 3 globals before `isolated` runs.
    A probe showed that without it, `autouse=False` still gave `9 passed` here.
  - **A second T1.7 test** scans `app.py` for `os.getenv` names, so a new variable has to join the isolation lists.
  - The plan's unused `import os` was left out of the conftest. A padded draft test (8 parametrized cases that
    imported `conftest`) was deleted before the commit.
- **Wire-up** `4da62a1`: `.gitignore` gains `.pytest_cache/`; `README.md` gains "Running tests" (verified on Python 3.10
  only) and a `tests/` row; `.quality-gates.json` gets its first 2 gates.
- **Red-drives**, all in the working tree and each restored (`git status` was clean afterwards):
  1. the `e5f52e1^` template, with the old "USB Serial"/"Arduino Mega" banner: T1.1 fails;
  2. `autouse=False`: 6 tests fail, T1.1 and T1.7 among them (0 failed before `planted_leak` existed);
  3. `SERIAL_BAUD` dropped from `CONFIG_VARS`: T1.7 fails;
  4. `os.getenv("AIRQINO_NEW_SETTING")` appended to `app.py`: the scan test fails;
  5. an `assert False` test: `tests-exit` fails (measured 1);
  6. one test hidden from collection: `tests-passed` fails (measured 8);
  7. threshold 9 → 8, staged: `quality_ratchet.py --precommit` prints REFUSED.
- **Probe for Phase 2**, run on a scratchpad copy: a test that uploads a CSV through the route sets `_csv_data`, and
  the next test sees `None` again, with `/api/status` source `None`. So `isolated` resets globals that a route sets.
- **Plan note:** the "As implemented (Session 10)" paragraph at `test-suite-plan.md:262-266`.
- **Landing:** you picked the fast-forward and push in a picker before close-out (learning #8). Before the
  fast-forward, a `git fetch` showed `origin/main` = `5cc4ce9`, an ancestor of the branch, and a scan of the lines
  added since then found no secrets or local paths. Then `git merge --ff-only` and `git branch -d`, with the push
  after this commit.
- **FM #28 reduction:** "Session 7 Handoff Evaluation" and "What Session 8 Did" were archived
  (`git show 4da62a1:SESSION_NOTES.md`).

**Verification:**
- **Plan §5 P1 DONE, every item met:**
  - `python3 -m pytest -q` and plain `pytest -q` both give `9 passed` and exit 0, with 0 xfailed;
  - the ratchet passes 2/2 (the summary line is in ACTIVE TASK);
  - the red-drives are recorded (above);
  - `git diff --stat main -- app.py airqino_client.py serial_reader.py templates static` was empty before the
    fast-forward;
  - the dashboard no longer lists "No test infrastructure".
- **Runtime (3E):** the deliverable is tests only, so no product runtime behaviour changed. Running the suite is the
  run: it renders `/` through Flask's test client under 5 source setups. With no template change, no browser check was
  needed, and learning #5's headless Chrome stays the only rendered-page check.

**Key files:**
- `tests/conftest.py:9-12` (`CONFIG_VARS`), `:15-22` (`isolated`, autouse), `:25-28` (`client`)
- `tests/test_dashboard_page.py`:
  - `:19-24` (`ISOLATED_VARS`, `IMPORT_TIME_VARS`, `MODULE_GLOBALS`);
  - `:29-42` (`planted_leak`);
  - `:57` (T1.1, the banner guard);
  - `:122` and `:129` (T1.7).
- `.quality-gates.json:16-33` (the two gates); `pytest.ini:1-5`; `requirements-dev.txt:1-2`
- `README.md:25` ("Running tests"), `README.md:150` (the `tests/` row)
- For Phase 2:
  - `docs/planning/test-suite-plan.md:299` (Phase 2), `:337` (its red-drive);
  - `app.py:236` (`upload_csv`), `:245` (the `utf-8` decode, D4), `:261` (`k.strip().lower()`, D3 and the
    red-drive), `:171` (`int(hours)`, D2).

**Gotchas for the next session:**
- **The plan's Phase 2 citations hold.** They were re-grepped in Session 10, and `.lower()` is at `app.py:261`. Find
  line numbers with `grep -n`, not by counting `sed` output: a draft of this handoff miscounted it as `:260`, and
  the pre-commit re-grep caught it.
- **Don't copy `planted_leak` into the new test modules.** T1.7 already proves that `isolated` works for every module,
  and the Session 10 probe showed that a global set by a route is reset between tests.
- **No hook enforces the ratchet:** `core.hooksPath` is unset and `.git/hooks` has no active hook. Tighten
  `tests-passed` in the same commit as the tests, and run `python3 quality_ratchet.py --precommit` by hand after
  staging the manifest.
- **P2 adds the first xfails,** so keep "passed" out of `reason=` strings. The `tests-passed` regex scans the `-ra`
  output.
- **The ratchet's `results` hash changes with each run.** Cite the summary line from the final run.
- **Stage files by name.** `.quality-gates-results.json`, `.context-budget-history.jsonl`, `dashboard_history.jsonl`
  and `docs/HARDWARE.html` are untracked (open item 2).
- **The dashboard's MEDIUM "thin" stays until the test files total at least 548 lines.** They are 166 now. Don't pad.
- **Back up an untracked file to the scratchpad, by explicit path, before a red-drive mutates it:** `git checkout`
  can't restore an untracked file. In this session a `||` fallback sent the backup to `$TMPDIR`, and the conftest was
  briefly left with `autouse=False` (fixed at once). `tests/` is tracked now, so `git checkout --` works for it.

**Learnings (3C):** `CLAUDE.md` learning #9: plant the hazard that a guard test exists to catch. It points at
`planted_leak`, which is the gate form.

**Self-assessment:**
- **Score: 8/10**
- (+) Probed the plan's red-drive premise before trusting it (learning #7). That found the gap, and one fixture closed
  it.
- (+) Seven red-drives and a ratchet refusal: every guard and both gates were watched failing.
- (+) Scope held: no product code; three commits of 5 files or fewer, plus the close-out.
- (+) Learning #8 applied: the landing decision was asked *before* close-out, so this handoff describes the session's
  real end.
- (+) Probed the claim Phase 2 depends on (a global set by a route is reset between tests) rather than guessing.
- (−) The red-drive restore mishap: a `git checkout` on an untracked file, and a backup that went to `$TMPDIR`
  instead of the scratchpad. The harness flagged the change, and it was fixed at once.
- (−) A padded draft test (8 parametrized cases importing `conftest`) got written before being caught.
- (−) One red-drive was labelled "both gates fail" when only `tests-exit` does. That was right by design, but the
  label was careless.
- (−) Two harness nudges for silence during long tool runs.
- (−) A draft of this handoff called the plan's `app.py:261` citation off by one. The pre-commit re-grep showed the
  plan was right and my `sed` count was wrong. It was fixed before the commit, but it's learning #7's failure again:
  a line number read by eye.

### Sessions 1–9 (archived by Sessions 6–11)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
