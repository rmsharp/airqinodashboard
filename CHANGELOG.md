# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken** in this repository — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"* Every session records its actions here at close-out (`SESSION_RUNNER.md`
Phase 3F); Phase 0 reconciles it against `git log` and backfills anything a crashed or
out-of-band session missed. Taking an action — any commit, or any non-commit action — and
not recording it is failure mode #27. Old entries are archived, never deleted.

**The rules** — how to add an entry, source tags, size and archiving — are in
[§The Action Ledger](docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger), which `bin/sync`
keeps current. ledger-format: 2 — keep this marker; `bin/status` reads it.

---

<!-- Entries go below, newest on top. Delete the seed-sentinel line near the top when you add the first one. -->

### 2026-09-17 · [ad hoc] No-source contract and CSV-path tests — test-suite plan Phase 2, commit 2 of 3
- **Change:** adds `tests/test_csv_routes.py` with 19 passing tests (T2.1–T2.8) and 3 strict xfails (D2's timeseries half, D3, D4). The breakdown: T2.1 is a 6-route table; T2.2 has 2 tests; T2.3 covers 3 delimiters; T2.4, T2.5, T2.7 and T2.8 have one test each; T2.6 has 4. `.quality-gates.json` tightens `tests-passed` from 9 to 28, the measured count. **Change from the plan's text:** the plan's D2 and D3 assertions are `status_code < 500`, but the `client` fixture runs with `TESTING` on, so Flask raises the route's exception into the test instead of answering 500. Each xfail therefore names the exception it expects today (`raises=ValueError`, `AttributeError`, `AssertionError`), so any other kind of failure still reports as FAILED
- **Commit/PR:** this commit (ships this entry)
- **Session:** S11 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` both give `28 passed, 3 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0dc3acde972e · manifest 770382cd43d3`. Red-drives in the working tree, each restored (`app.py` shasum unchanged): `.lower()` removed at `app.py:261` fails T2.4; `data[:500]` fails the 500-row cap test; `_csv_data[0]` fails the last-row test; dropping the `;` branch fails T2.3's semicolon case; `utf-8-sig` (a D4 fix) gives `XPASS(strict)` and fails the suite; one test hidden from collection fails `tests-passed` (measured 27)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 11 claimed — test-suite Phase 2 begins (in progress)
- **Change:** the operator picked Phase 2 of `docs/planning/test-suite-plan.md` (the no-source contract and the CSV path) in the Phase 0 picker. Session claimed on branch `test/suite-phase2` (off `main` `fbacf96`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S11 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 10 closed out — test-suite Phase 1 complete; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 9 evaluation (8/10) and the self-assessment (8/10). Its open items are renumbered, with Phase 2 recommended next. "Session 7 Handoff Evaluation" and "What Session 8 Did" were archived (`git show 4da62a1:SESSION_NOTES.md`; FM #28; 300 → 334 lines, under the 400-line ceiling). `CLAUDE.md` gains learning #9: plant the hazard a guard test exists to catch. `docs/planning/test-suite-plan.md` gains an "As implemented (Session 10)" note under Phase 1's DONE list. The S10 `HANDOFFS.md` receipt is `status: complete`. A new finding went to open item 3: `context_budget.py` reports `SESSION_NOTES.md` as "instrument-failed", because `.context-budget.json` expects at least 2 `^## ` headings but the synced seed has 1
- **Commit/PR:** the close-out commit (ships this entry); session commits `02016aa`, `067455f`, `4da62a1`. Pushed to `origin/main` straight after it is made, on the operator's direction
- **Session:** S10 · **Verified:** `python3 -m pytest -q` gives `9 passed`; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f`; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `test/suite-phase1` deleted
- **Change:** on the operator's direction, the fully merged local branch `test/suite-phase1` (tip `4da62a1`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S10 · **Verified:** before deletion, `git merge-base --is-ancestor test/suite-phase1 main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Phase 1 branch landed — main fast-forwarded to `test/suite-phase1`; push follows the close-out
- **Change:** the operator chose "fast-forward main + push" in a picker before close-out (learning #8). Local `main` was fast-forwarded from `7256c91` to `4da62a1` with `git merge --ff-only`, so `02016aa`, `067455f` and `4da62a1` keep their SHAs (learning #6). `main` is pushed to `origin/main` straight after the close-out commit. That push carries `7256c91` (Session 9's amended close-out, never pushed until now), the three Session 10 commits and the close-out
- **Commit/PR:** the close-out commit (ships this entry); fast-forward to `4da62a1`; push to `origin/main`
- **Session:** S10 · **Verified:** after `git fetch`, `origin/main` = `5cc4ce9`, and `git merge-base --is-ancestor` confirmed that both it and `main` are ancestors of the branch. A scan of the lines added in `origin/main..test/suite-phase1` found no secrets, home paths or scratchpad paths, only variable names and prose about earlier scans. The planted test values are `planted-*` strings
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test wire-up — .gitignore, README "Running tests", two quality gates (plan Phase 1, commit 3 of 4)
- **Change:** `.gitignore` gains `.pytest_cache/`. pytest already writes a `.gitignore` inside that directory, so this line is a backup. `README.md` gains a "Running tests" subsection under Quick start: it says the suite is verified on Python 3.10 only, and adds a `tests/` row in Key files. `.quality-gates.json` declares its first two gates: `tests-exit` (max 0) and `tests-passed` (min 9, the measured count). Both use one `python3 -m pytest -q` command, so the ratchet runs pytest once. `.quality-gates-results.json` stays untracked (open item 2, the operator's call)
- **Commit/PR:** this commit (ships this entry)
- **Session:** S10 · **Verified:** `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f`; `--precommit` passes on the staged manifest. Red-drives, each restored: a failing test → `tests-exit` fails (measured 1); one test hidden from collection → `tests-passed` fails (measured 8)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test harness and the setup-banner guard — test-suite plan Phase 1, commit 2 of 4
- **Change:** adds `requirements-dev.txt` (`-r requirements.txt`, `pytest>=8`), `pytest.ini` (as in the plan) and `tests/conftest.py` (the plan's `isolated` autouse fixture and the `client` fixture). Also adds `tests/test_dashboard_page.py` with 9 tests: T1.1–T1.6 as planned, and T1.7 as two tests. **Two changes from the plan text:** (1) the module fixture `planted_leak` sets all 8 variables and fills the 3 module globals before `isolated` runs. A probe showed that with `autouse` off, all 9 tests still **passed** on this machine, because no `.env` exists, so the plan's red-drive only worked in the Session 9 spike, which had one. (2) A second T1.7 test scans `app.py` for `os.getenv` names, so a new variable has to join the isolation lists. The unused `import os` in the plan's conftest is left out
- **Commit/PR:** this commit (ships this entry)
- **Session:** S10 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` both `9 passed`. Red-drives in the working tree, each restored: pre-Session-7 banner (`e5f52e1^` template) → T1.1 fails; `autouse=False` → 6 fail, T1.7 included; `SERIAL_BAUD` dropped from `CONFIG_VARS` → T1.7 fails; a new `os.getenv` in `app.py` → the scan test fails. `git status` shows no modified tracked file
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 10 claimed — test-suite plan approved; Phase 1 begins (in progress)
- **Change:** the operator approved `docs/planning/test-suite-plan.md` as written and picked Phase 1 (the harness and the setup-banner guard) in the Phase 0 picker. The plan's Status line now records the approval. Session claimed on branch `test/suite-phase1` (off `main` `7256c91`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S10 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 close-out amended — follow-on git actions recorded, receipt brought to session end
- **Change:** the operator asked for a Phase 3 close-out at the end of each session. The first close-out (`f49da64`) predated three operator-directed actions (the fast-forward and push, the branch deletion, and a second push). `SESSION_NOTES.md` now records them, and its self-assessment drops from 8/10 to 7/10. The S9 `HANDOFFS.md` receipt is overwritten in place: it no longer calls the branch unpushed or says to land it first, and its `changelog_ref` names this entry. `CLAUDE.md` gains learning #8: close-out belongs at the end of the session, so run Phase 3 again after any follow-on work
- **Commit/PR:** the amended close-out commit (ships this entry); not pushed unless the operator asks
- **Session:** S9 · **Verified:** n/a — docs-only; `git diff 15b0a3f -- '*.py' templates static` is empty; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `docs/test-suite-plan` deleted
- **Change:** on the operator's direction, the fully merged local branch `docs/test-suite-plan` (tip `f49da64`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch. `SESSION_NOTES.md`'s ACTIVE TASK no longer says the branch exists
- **Commit/PR:** this commit (ships this entry); branch op, no commit of its own
- **Session:** S9 (operator-directed follow-on after close-out) · **Verified:** before deletion, `git merge-base --is-ancestor docs/test-suite-plan main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Plan branch landed — main fast-forwarded to `docs/test-suite-plan` and pushed to origin
- **Change:** on the operator's direction, local `main` was fast-forwarded from `15b0a3f` to `f49da64` (`git merge --ff-only`, so Session 9's SHAs `1177049`, `d813463` and `f49da64` are unchanged; learning #6). `SESSION_NOTES.md`'s ACTIVE TASK and open item 1 no longer call the branch unpushed. This commit is pushed to `origin/main` directly after it is made, together with the three Session 9 commits. The local branch `docs/test-suite-plan` is kept (fully merged; not pushed)
- **Commit/PR:** this commit (ships this entry); fast-forward to `f49da64`; push to `origin/main`
- **Session:** S9 (operator-directed follow-on after close-out) · **Verified:** before the fast-forward, `origin/main` = `main` = `15b0a3f` after `git fetch`, and `git merge-base --is-ancestor` confirmed it could fast-forward; a scan of the added lines found no secrets, home paths or scratchpad paths
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 closed out — test-suite plan written, approval pending
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 8 evaluation (9/10) and the self-assessment (8/10). Its open items are renumbered, with Phase 1 of the plan recommended next after approval. The Session 5–7 notes were archived (`git show 15b0a3f:SESSION_NOTES.md`; FM #28; 350 → 266 lines). `CLAUDE.md` gains learning #7: probe the code before a plan claims how it behaves, and re-grep citations after writing. The S9 `HANDOFFS.md` receipt is `status: complete`. The branch `docs/test-suite-plan` stays local and unpushed
- **Commit/PR:** the close-out commit (ships this entry); session commits `1177049`, `d813463`
- **Session:** S9 · **Verified:** n/a — docs-only; `git diff 15b0a3f -- '*.py' templates static` is empty; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test-suite plan written — `docs/planning/test-suite-plan.md` (open item 1)
- **Change:** a four-phase pytest plan, one session per phase: P1 harness + setup-banner guard, P2 no-source contract + CSV path, P3 serial (real pty), P4 API client + API routes. It has a grep-based inventory (§3), and each phase names its DONE criteria, verification commands, surface and session boundary. It records 7 defects (D1–D7) reproduced by scratch probes; each becomes a strict-xfail test and a later fix session. The operator chose pytest, strict xfail, monkeypatch fakes and Python-only scope in one four-question picker. No product code changed
- **Commit/PR:** the plan commit (ships this entry)
- **Session:** S9 · **Verified:** a scratchpad spike ran every mechanism the phases rely on: a planted `.env` leak and the fixture that neutralises it, `pytest.ini`, the pty round trip, fake-client injection and the two ratchet gates (5 passed, 2 xfailed; `quality_ratchet.py --run` 2/2). It drove 3 guards red. Every file:line citation was re-grepped after writing (6 corrected)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 claimed — plan a test suite (in progress)
- **Change:** session claimed on branch `docs/test-suite-plan` (off `main` `15b0a3f`); the operator picked open item 1 from the Phase 0 picker. The deliverable is `docs/planning/test-suite-plan.md`, a plan only
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S9 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 8 closed out — four-branch stack merged into main; main is the only branch
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 7 evaluation (9/10) and the self-assessment (9/10). Its open items are renumbered, with planning a test suite recommended next. "Session 4 Handoff Evaluation" and "What Session 5 Did" were archived (`git show a31fea6:SESSION_NOTES.md`; FM #28; 437 → 350 lines). `CLAUDE.md` gains learning #6: never squash or rebase, because the records cite SHAs. The S8 `HANDOFFS.md` receipt is `status: complete`. This commit is pushed to `origin/main` directly after it is made, on the operator's direction
- **Commit/PR:** the close-out commit (ships this entry); session commit `a31fea6`
- **Session:** S8 · **Verified:** n/a — docs-only; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Branch cleanup — local main fast-forwarded; the four stack branches deleted locally and the two pushed ones on GitHub
- **Change:** local `main` was fast-forwarded from `03510d3` to `8554078`. `chore/methodology-pr2527-remediation`, `chore/methodology-read-set-budgets`, `chore/methodology-bl57-p6` and `fix/usb-serial-banner` were deleted locally with `git branch -d`. `origin`'s `chore/methodology-pr2527-remediation` and `fix/usb-serial-banner` were deleted and pruned. `main` is now the only branch, local and remote
- **Commit/PR:** none (branch operations); on the operator's direction
- **Session:** S8 · **Verified:** before deletion, `git merge-base --is-ancestor` confirmed each branch tip and every SHA the ledger cites is in `main`; afterwards `git branch -vv` and `git ls-remote --heads origin` each list only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #2 merged into main with a merge commit
- **Change:** PR #2 (`fix/usb-serial-banner` → `main`) merged as `8554078` (parents `9099569`, `a31fea6`). Sessions 5–8's work is now on `main`: the read-set-budgets sync, BL-57 P6 and the setup-banner fix. A merge commit keeps every SHA the ledger cites
- **Commit/PR:** PR #2 · merge commit `8554078`
- **Session:** S8 · **Verified:** `gh pr view 2` reads MERGED; `git diff a31fea6 main` is empty, so `main`'s tree is byte-identical to the verified branch tip
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #2 opened — the rest of the stack, 11 commits dfe26fd..a31fea6
- **Change:** pushed `fix/usb-serial-banner` to `origin` and opened https://github.com/rmsharp/airqinodashboard/pull/2 against `main`. It carries the three local branches that were stacked on PR #1, plus the Session 8 claim. The body lists the commits by branch and says to merge with a merge commit, not squash or rebase
- **Commit/PR:** PR #2
- **Session:** S8 · **Verified:** GitHub reported 11 commits, head `a31fea6`, MERGEABLE. Beforehand, `git merge-tree` showed no conflicts, and a scan of the added lines found no secrets
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #1 merged into main with a merge commit
- **Change:** PR #1 (`chore/methodology-pr2527-remediation` → `main`, open since 2026-06-12) merged as `9099569` (parents `765036c`, `0c59e5e`). This publishes `03510d3`, the hardware guide that had sat on local `main`, 1 commit ahead of `origin/main`
- **Commit/PR:** PR #1 · merge commit `9099569`
- **Session:** S8 · **Verified:** `gh pr view 1` reads MERGED; `origin/main` is `9099569` with the expected parents
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 8 claimed — branch/PR housekeeping for the four-branch stack (in progress)
- **Change:** session claimed on branch `fix/usb-serial-banner` (tip of the stack, `3712164`); the operator picked open item 1 from the Phase 0 picker
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S8 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 7 closed out — setup-banner serial fix complete
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 6 evaluation (9/10) and the self-assessment (8/10). Its open items are renumbered, and branch/PR housekeeping is recommended next. "What Session 4 Did" was archived (`git show e947798:SESSION_NOTES.md`; FM #28). `CLAUDE.md` gains learning #5, a runtime-verification recipe for the Flask UI. The S7 `HANDOFFS.md` receipt is `status: complete`. Not pushed
- **Commit/PR:** the close-out commit (ships this entry); session commits `38920e3`, `e5f52e1`
- **Session:** S7 · **Verified:** n/a — docs-only; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Setup banner's serial option describes the REV6 USB-to-TTL adapter, not an Arduino Mega USB port
- **Change:** `templates/dashboard.html` option 2 is now "Serial Adapter". The text says the REV6 board has no USB port, tells the user to wire a 3.3V USB-to-TTL adapter to the TX and GND pins, and points to `docs/HARDWARE.md`. The old heading was "USB Serial" and the old text said "connect a USB cable to the Arduino Mega port". `CLAUDE.md` learning #3 is now in the past tense, because the stale copy it described is gone. Searching every tracked surface outside the methodology docs and session records finds the old wording only in that learning's quote
- **Commit/PR:** the fix commit (ships this entry)
- **Session:** S7 · **Verified:** app launched (`python3 app.py`, no data source set); `GET /` returns 200 with the new text and 0 matches for "Arduino" or "USB cable"; a headless-Chrome screenshot at 1200×700 shows the three banner cards laid out cleanly
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 7 claimed — fix the stale USB Serial setup-banner text (in progress)
- **Change:** session claimed on branch `fix/usb-serial-banner` (off `e947798`); the operator picked open item 1 from the Phase 0 picker
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S7 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 6 closed out — methodology BL-57 P6 for airqino complete; Sessions 1–3 notes archived
- **Change:** P6 is complete here, with BL-56 folded in: synced from fork `main`, `CHANGELOG.md` at `ledger-format: 2`, and ledger conventions recorded in `CLAUDE.md`. Every item on the plan's DONE list passed, with counts re-derived per commit. `SESSION_NOTES.md` carries the handoff, the Session 5 evaluation (9/10) and the self-assessment (8/10), and no longer holds the Session 1–3 history (`git show 1402ad4:SESSION_NOTES.md`; 330 → 294 lines). The S6 `HANDOFFS.md` receipt is `status: complete`. Not pushed
- **Commit/PR:** the close-out commit (ships this entry); session commits `2b0230a`, `28022fe`, `5e4b483`, `9f150a5`
- **Session:** S6 · **Verified:** n/a — docs-only; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] `CLAUDE.md` records this ledger's conventions — BL-57 P6 step 4
- **Change:** a new Adaptations subsection, *Ledger (`CHANGELOG.md`) conventions*. It points to §The Action Ledger, reserves `[BL-<id>]` for this repo's own `BACKLOG.md` (methodology-backlog work is `[ad hoc]`), and records the legacy layout: no month heading over the 2026-09 entries, and prose bodies on the 2026-09-14 and 2026-09-15 entries. The protocol block already matches the current `CLAUDE_TEMPLATE.md` and carries no ledger wording, so it is unchanged
- **Commit/PR:** the `CLAUDE.md` commit (ships this entry)
- **Session:** S6 · **Verified:** n/a — docs-only; cited section, hash and entry dates resolve; `CLAUDE.md` 4,988 B of a 34,000 B resident ceiling
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] `CHANGELOG.md` header migrated to the thin seed (`ledger-format: 2`) — BL-57 P6 step 3, BL-56 folded in
- **Change:** the Keep-a-Changelog header (lines 1–11 at `28022fe`, recorded at claim) is replaced by fork `main`'s `starter-kit/CHANGELOG.md` header (`ff02b5c`), less its seed-sentinel comment, since this ledger already holds entries. `## [Unreleased]` is dropped: entries group by month, not by release, and this ledger opens its first `## YYYY-MM` at the next new month (2026-10) instead of retrofitting one. Every entry below is byte-identical
- **Commit/PR:** the migration commit (ships this entry)
- **Session:** S6 · **Verified:** fork `main`'s `bin/status` reads `present`; the upstream marker (`Authoritative Action Ledger`) is present; only lines 1–11 lose content (§9.8); `### ` headings 4 → 5 and audit 4 → 5 in zsh and bash (the block held 0 of either)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Methodology synced from fork `main` (`ff02b5c`) — BL-57 P6 step 2
- **Change:** `bin/sync . --source=local` from fork `main` (`v3.7-848-gff02b5c`), after a dry run that exited 0 with no refusals: 12 tracked files updated, `quality_ratchet.py` created, `.quality-gates.json` seeded with no gates, the 5 existing seeds left as they are. Fork `main`'s `bin/status` now reads every tracked file `current`; `CHANGELOG.md` still reads *present (stale format)* until its header is migrated. Synced from `main`, not the branch the plan names, because BL-54 is fixed fork-side (`865119f`) and no longer refuses files. One commit of 14 synced files plus this ledger — one tool run, not split under the 5-file cap
- **Commit/PR:** the sync commit (ships this entry)
- **Session:** S6 · **Verified:** all 7 `.py` files parse; `app` imports (9 routes); `methodology_dashboard.py` v2.18.0 runs (health 54/100); `quality_ratchet.py --run` 0/0 gates; `methodology_trim.py --check` runs, trigger does not fire
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 6 claimed — methodology BL-57 P6: sync from fork `main` and migrate this ledger's header (in progress)
- **Change:** session claimed on branch `chore/methodology-bl57-p6` (off `1402ad4`); the header block to replace is recorded as lines 1–11 in `SESSION_NOTES.md` before any edit
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S6 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-15 · [ad hoc] Session 5 — orientation-only session closed out; no deliverable

Phase 0 ran in full (started 2026-09-14). Reconcile found no undocumented commits (this ledger's frontier was HEAD,
`dfe26fd`), and the four commits after Session 4 (`66abe78`, `28db357`, `0c59e5e`, `dfe26fd`) trace to methodology-repo
sessions, not ghost sessions. The operator then closed the session without assigning a task. Close-out refreshed the stale
`SESSION_NOTES.md` ACTIVE TASK, added `CLAUDE.md` learning #4, and wrote the first `HANDOFFS.md` receipt (S5; seed
sentinel removed). No application code changed; not pushed.

- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-14 · [ad hoc] Methodology synced to `read-set-budgets` (`598c459`), ahead of its upstream merge

Synced with `bin/sync --source=local` from a full clone of `KJ5HST/methodology`'s `read-set-budgets`
branch (`598c459`, `v3.7-12-g598c459`) — the content of its open PR #80, not yet a release. 10 files
updated, 8 added (`FRAMEWORK_LEARNINGS.md`, `docs/methodology/FRAMEWORK_APPARATUS.md`,
`methodology_trim.py`, `context_budget.py`, `BOOTSTRAP.md`, `CLAUDE_TEMPLATE.md`,
`CONTEXT_TEMPLATE.md`, `RECOMMENDED_SKILLS.md`) and 2 seeds created (`HANDOFFS.md`,
`.context-budget.json`); `bin/status` now reads every tracked file `current`. Branched from
`chore/methodology-pr2527-remediation` (open PR #1), the only branch whose files the sync accepted
without `--force`; not pushed. This file's own format predates the ledger format (`bin/status`:
*present (stale format)*) and was left as it is — `bin/sync` never rewrites a seed.

- **Model:** Claude Opus 5 (claude-opus-5)
