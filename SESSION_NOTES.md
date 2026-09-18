# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** Test suite. `docs/planning/test-suite-plan.md` is approved (Session 10), and **Phase 1 is done**.
Next session implements **Phase 2 only**: the no-source contract and the CSV path.
**Status:**
- **Phase 1: COMPLETE, on `main`.** It is `067455f` (the harness and 9 tests) plus `4da62a1` (the wire-up and 2
  gates). On the operator's direction, `main` was fast-forwarded to the Session 10 branch, which was then deleted.
  `main` is the only branch. Session 10's close-out commit is pushed straight after it is made, together with
  `7256c91`, `02016aa`, `067455f` and `4da62a1`. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `9 passed`, 0 xfailed, in about 0.02 s. The ratchet gives `quality_ratchet:
  2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f`. The gates are `tests-exit`
  (max 0) and `tests-passed` (min 9).
- **Dashboard:** 54 → **62/100**, and High+ risk 1 → 0. "Test coverage is very thin (ratio: 0.03)" (MEDIUM) replaced
  the HIGH, as the plan computed.
- **7 defects (plan §4, D1–D7) are still unfixed.** Each gets its strict xfail in P2–P4, then a fix session of its
  own. D1 and D7 hit the serial path the operator is about to use.
- **No product code has changed** since Session 7's fix (`e5f52e1`).
- Earlier status: Session 9's is at `git show 7256c91:SESSION_NOTES.md`, Session 8's at `git show 15b0a3f:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Implement Phase 2 of the test-suite plan (recommended next).** It is plan §5 "Phase 2"
   (`docs/planning/test-suite-plan.md:299-348`):
   - files: `tests/test_csv_routes.py` (T2.1–T2.8, plus strict xfails for D2's timeseries half, D3 and D4) and
     `.quality-gates.json` (tighten `tests-passed` to the new measured count);
   - three commits: the claim; the tests, the gate and the ledger entry; the close-out;
   - DONE: the suite exits 0 with exactly 3 xfailed, the ratchet passes 2/2 at the tightened threshold, one red-drive
     is recorded, and no product file shows in `git diff`.

   Start on a new branch off `main`. P3 (serial), P4 (API) and the D1–D7 fixes follow in plan order.
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
   the operator's go-ahead.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 11 Did
**Deliverable:** Implement Phase 2 of `docs/planning/test-suite-plan.md` (open item 1): the no-source contract and the
CSV path (IN PROGRESS)
**Started:** 2026-09-17 22:29
**Status:** Session claimed on branch `test/suite-phase2` (off `main` `fbacf96`). The operator picked Phase 2 in the
Phase 0 picker. Work beginning.
**Ledger:** `CHANGELOG: pending` — the claim commit's `CHANGELOG.md` entry says (in progress); Phase 3F records the rest. Until close-out, this line is the crash breadcrumb for the next session's reconcile.

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

### Session 8 Handoff Evaluation (by Session 9)
- **Score: 9/10**
- **What helped:** Open item 1 gave everything a planning session starts from:
  - the three surfaces with sizes and line ranges (`app.py:64`–`:236`, `active_source()` at `:51`);
  - the missing pytest in `requirements.txt`;
  - the first test case (the banner with "Serial Adapter" present and "Arduino" absent), which became T1.1.

  The git state matched exactly (`main` = `origin/main` = `15b0a3f`, no PRs), as did the Issues-count prediction (0)
  and the health score (54/100). "Start from `main` and branch" and "stage files by name" set up the claim with no
  lookup.
- **What was missing:** Toolchain facts that the plan's first decisions rest on. pytest 9.0.2 and pytest-cov were
  already installed in the base env, and pytest 9 needs Python 3.10 while `README.md:13` says 3.9+. Each took one
  command to find, and none was Session 8's area of work.
- **What was wrong:** Nothing found. Every line range, line count and SHA matched.
- **ROI:** Strongly positive. Orientation to the task took one picker round.

### What Session 9 Did
**Deliverable:** Plan a test suite (open item 1): `docs/planning/test-suite-plan.md` — **COMPLETE** (the plan; approval
pending)
**Started / Closed:** 2026-09-17 20:25 · claimed on branch `docs/test-suite-plan` off `main` `15b0a3f`; closed on `main`
after the branch was fast-forwarded in, pushed and deleted
**Governing docs:** `SESSION_RUNNER.md` §Planning Sessions and
`docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md` (research, then the design document). One optional Phase 2B
picker settled the load-bearing decisions before writing.
**Ledger:** 6 `CHANGELOG.md` entries: the claim, the plan, the first close-out, the branch landing and push, the branch
deletion, and this amended close-out.

**What was done:**
- **Claim** `1177049`: the stub, a pending receipt and an *(in progress)* entry, committed before any research.
- **Research:**
  - Read all of `app.py`, `airqino_client.py`, `serial_reader.py`, `templates/dashboard.html` and
    `static/js/dashboard.js`.
  - Ran the grep inventory (plan §3): 8 routes, 3 helpers, 15 client methods, 8 `SerialReader` methods, 9 environment
    variables, 3 module globals and every I/O or clock call.
  - Found what the dashboard counts as source: 8 files and 5,475 lines, of which the product is 1,063.
- **Probes** (scratch runs, repo untouched) reproduced **7 defects** (plan §4):
  - D1 serial `;` `key=value` clobbers the first field;
  - D2 `hours`/`days=abc` returns 500;
  - D3 a ragged CSV row returns 500;
  - D4 a CSV BOM corrupts the first header;
  - D5 a partial set of API credentials shows "API Connected";
  - D6 the badge's source order and the routes' source order disagree;
  - D7 a serial open failure is swallowed as a 200.

  D2's hourly half and D6 were first reasoned from the code, then probed after the plan was written.
- **Operator decisions** (one four-question picker, the recommended option each time): pytest; strict xfail with fixes
  later; monkeypatch fakes; Python only.
- **Spike** (scratchpad, not committed): copies of the app beside a planted `.env`. Results:
  - the `.env` leak is real, and the `isolated` fixture neutralises it;
  - `pytest.ini` works with both `python3 -m pytest` and plain `pytest` (5 passed, 2 xfailed);
  - the pty round trip works with real pyserial on `/dev/ttys008`;
  - fake-client injection works;
  - the two ratchet gates pass 2/2;
  - 3 red-drives: the old banner wording, a fixed D1 as XPASS(strict), and the fixture turned off.
- **Plan** `d813463` (585 lines): decisions, inventory, defects, 4 phases (tests, commits, DONE, surface, boundary),
  fix-session protocol, alternatives, out-of-scope list, and the spike's evidence table.
- **Citation check:** every `file:line` was re-grepped after writing, and 6 were wrong. There were 4 in
  `dashboard.js`, 1 in `README.md` and 1 range in `methodology_dashboard.py`, all written from memory. They were fixed
  before the commit.
- **FM #28 reduction:** "Session 5/6 Handoff Evaluation" and "What Session 6/7 Did" were removed from this file
  (`git show 15b0a3f:SESSION_NOTES.md`).
- **First close-out** `f49da64`: the handoff, the receipt and learning #7.
- **Follow-on actions, directed by the operator after that close-out:**
  - **Landing and push** (`4973cf7`). `git fetch` first showed `origin/main` = `main` = `15b0a3f`, and
    `git merge-base --is-ancestor` confirmed a fast-forward was possible. A scan of the added lines found no secrets,
    home paths or scratchpad paths. `main` was then fast-forwarded to `f49da64` (SHAs unchanged, learning #6), the
    ledger entry committed, and `main` pushed.
  - **Branch deletion** (`5cc4ce9`). The branch was confirmed to be an ancestor of `main`, deleted with
    `git branch -d`, the deletion recorded in the ledger, and `main` pushed after a fresh `git fetch`. That push has
    no ledger entry of its own, because recording it would need a new commit, which would then need pushing too.
  - **Amended close-out** (this commit). The operator asked for a Phase 3 close-out at the end of each session. The
    first close-out ran before the follow-on actions, so this handoff, the receipt and the self-assessment are
    brought up to the session's real end. Learning #8 records it.

**Verification:**
- **Deliverable:** the plan satisfies `SESSION_RUNNER.md` §Planning Session Checklist (plan §10). One box stays
  unticked: whether the deepest reasoning mode was set isn't recorded.
- **Build:** all 7 root `.py` files compile, and `app` imports with 8 non-static routes (checked at Phase 0). No
  product file changed: `git diff 15b0a3f -- '*.py' templates static` is empty.
- **Runtime (3E):** n/a, since the deliverable is docs-only. The spike ran the app's own code in copies.

**Key files:**
- `docs/planning/test-suite-plan.md`:
  - `:161-290` — Phase 1, including the `pytest.ini` and `conftest.py` text;
  - `:122-146` — the defects table;
  - `:556-574` — the spike evidence.
- `app.py:12` (`load_dotenv()` at import), `app.py:19-21` (module globals), `app.py:51-59` (`active_source()`)
- `templates/dashboard.html:33` (badge), `:40` (the HTML comment that also says "no data source"), `:55` (banner
  text containing "no USB port")
- `.quality-gates.json` (`"gates": []`, the field Phase 1 fills); `quality_ratchet.py:266-298` (how gates are measured)
- `README.md:11-23` (Quick start, where "Running tests" goes), `README.md:131-142` (Key files)

**Gotchas for the next session:**
- **`load_dotenv()` walks up to `/`.** A `.env` in the repo *or any parent directory* leaks into tests at `import app`
  (python-dotenv 1.2.1 `find_dotenv`). The `isolated` fixture must stay `autouse`. Never set `SERIAL_PORT` in a test
  without injecting a fake reader or pointing it at a pty: `get_serial_reader()` starts a real thread, which the probe
  showed.
- **T1.1's banned-word list must not include "USB port":** the correct banner says "no USB port". "No Data Source"
  matches twice case-insensitively (the badge and the HTML comment at `:40`), so assert on `>No Data Source<`.
- **Keep the word "passed" out of xfail `reason=` strings.** The `tests-passed` gate's regex `(\d+) passed` scans
  output that `-ra` prints them into.
- **After Phase 1 the dashboard shows MEDIUM "Test coverage is very thin".** That's expected (plan §5, P1): it stays
  until the test files total 548 lines, because 4,412 of the 5,475 source lines are vendored methodology tooling.
  Don't pad tests.
- **Untracked files will pile up:** `.pytest_cache/` (gitignored in Phase 1 commit 3) and
  `.quality-gates-results.json` (open item 2). Stage files by name.
- **The base env loads global pytest plugins** (cov, anyio, asyncio, langsmith). They didn't interfere in the spike.
- **The spike lived in this session's scratchpad and is gone.** The plan carries the fixture text and the evidence.
- **The first close-out's ledger entry is out of date.** It says the branch "stays local and unpushed", but
  ledger entries are never edited. The three entries above it supersede it.

**Learnings (3C):**
- `CLAUDE.md` learning #7: probe the code paths a plan claims about before writing it, and re-grep every citation
  afterwards.
- `CLAUDE.md` learning #8: close-out belongs at the end of the session, not the end of the deliverable. If the operator
  directs more actions after it, run Phase 3 again before stopping.

**Self-assessment:**
- **Score: 7/10.** The first close-out scored itself 8. One point comes off for the stale close-out below, which the
  operator had to correct.
- (+) Research came before the design: every module was read, and the suspicions were probed into 7 reproduced
  defects with repro strings and `file:line`.
- (+) The load-bearing decisions were asked before writing (one picker), so there were no stakeholder corrections.
- (+) The plan's mechanics were measured in a spike, with 3 red-drives, rather than asserted. The post-Phase-1
  dashboard outcome was computed, not guessed (learning #13).
- (+) Scope held: no test or product code in the repo; the plan only.
- (−) 6 line citations were written from memory and were wrong. The post-write check caught them, but grepping while
  writing would have avoided them (FM #11).
- (−) One backup copy of the template went to `/tmp` instead of the scratchpad. It was deleted immediately.
- (−) The harness prompted for status three times, which repeats a Session 6–8 minus.
- (−) The plan runs 585 lines, and a Phase 1 executor needs about a third of it. The §-structure keeps it navigable.
- (+) The follow-on git work was checked before each outward step: a fetch, an ancestor check and a secret scan before
  the push; a merge check before the delete. Each action was recorded in the ledger.
- (−) **The close-out went stale.** I carried out three operator-directed actions after the first close-out without
  re-running Phase 3. That left the receipt saying the branch was unpushed and telling the next session to land it,
  and left no final report. The operator had to ask for the close-out.

### Sessions 1–8 (archived by Sessions 6–10)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
