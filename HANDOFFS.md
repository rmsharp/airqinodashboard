# Handoff Receipts — durable close-out proof

The cumulative, append-only record of **each session's close-out handoff**, distilled into a
machine-checkable block. It is the durable answer to *"was close-out actually performed, and what
did the session hand its successor?"* — the part of close-out that otherwise lives only in the
transient `SESSION_NOTES.md` (overwritten every session) or the spoken report (which leaves no file
at all).

One `handoff` block per **session** (not per commit), newest on top. The canonical-only
`bin/check-handoff` (copy it into your `bin/` if you want the structural check) asserts each block is
present and structurally complete; the next session's Phase 0 reconcile greps this file for a missing
or still-`pending` receipt and backfills it — that reconcile, not the checker, is the dependable
backstop, so the discipline needs no tooling. Together — a write-step at close-out **and** a
reconcile-on-read backstop — this makes a skipped handoff *detectable* rather than silent.

> **A green `bin/check-handoff` is not a good handoff.** The check verifies presence and structure,
> never semantic quality. Faithfulness is still scored 1–10 by the next session (Phase 3A). A
> well-formed but hollow receipt passes the check and is caught only by that human judgement.

## How to write a receipt

**At Phase 1B (claim the session)** — write the stub block below with `status: pending`, filling what
you can, and commit it with your session-claim commit. This committed `pending` block is the crash
breadcrumb: if the session ends before close-out, the next session's Phase 0 reconcile sees it.

**At Phase 3D (close-out)** — overwrite that block in place to `status: complete` and fill every
field. The block must satisfy all six Minimum Handoff Requirements (`SESSION_RUNNER.md` §3D).

**Naming the acting model (optional).** No new key — `REQUIRED_KEYS` is unchanged, and the fenced
block below stays exactly as documented. When a one-line summary is useful, especially for a
single-tier session where it saves a reader a cross-reference into `CHANGELOG.md`'s per-action
**Model:** bullet (see that file's format section), name the model in this receipt's free-text
prose area — the Format section below documents that area as *"the durable proxy for the Phase 3G
spoken report."* This formalizes what a capability-tiered session already does organically when it
states which tier built which layer and which tier reviewed it; this fork's own first receipt
(root `HANDOFFS.md`, session S1) is the worked precedent. `CHANGELOG.md`'s **Model:** bullet
remains the structured, per-action record; this is a convenience pointer for the session-level
view, not a second schema — and it is fine for both to name the same model on a single-tier
session, since they answer different questions ("what happened, action by action" vs. "which model
ran this session"). A canonical-only `bin/model-report` (copy it into your `bin/` if you want it,
same as `bin/check-handoff`) reads this free-text convention back alongside `CHANGELOG.md`'s
**Model:** bullets and git's `Co-Authored-By` trailers, keeping all three visually separate.

## Format — a fenced `handoff` block

````
```handoff
session: S<N>
date: YYYY-MM-DD
status: <pending | complete>
self_score: <1-10>
predecessor_score: <1-10>
active_task: <current state>
what_was_done: <what you did, including a commit sha — or the literal `pending`>
next_steps: <specific and actionable; never "pick next from backlog">
key_files: <each entry carries a path:line token, e.g. SessionManager.java:245>
gotchas: <traps the next session should watch for>
runtime_smoke: <a run result, or "n/a — docs-only", or "impossible: <reason>">
changelog_ref: <PR #N, a short-sha, or CHANGELOG.md "<its ### heading>" — never a bare line number, which decays once the ledger is trimmed>
commit: <short-sha — or the literal `pending`>
```
<free-text prose: the durable proxy for the Phase 3G spoken report, plus the +/- self-score breakdown>

Write clean `key: value` lines — no inline `#` comments (a `#` is a literal value character,
as in `changelog_ref: PR #52`). The keys are the six Phase 3D Minimum Handoff Requirements (the sixth
*is* `self_score`) plus `predecessor_score` (the Phase 3A evaluation) and a little metadata. `status`
is `pending` at the Phase 1B claim and `complete` at
close-out; a third value, `reconciled`, is written *only* by a later session's Phase 0 reconcile
when it reconstructs a receipt a crashed session never completed — you never write it yourself.
````

`self_score` and `predecessor_score` are distinct keys so one can never stand in for the other; omit
`predecessor_score` on Session 1 (there is no predecessor to score). `commit: pending` and
`what_was_done: pending` are legal at write time (the receipt ships in the very commit whose sha it
would name); no future session is assigned to fill either in later, so `pending` is a legitimate
resting value for both, not a promise a later session owes.

**A receipt's identity is `session` + `date`, not `session` alone.** `S<N>` is a per-sequence
counter, and one ledger may legitimately merge more than one sequence — a fork and its upstream each
running their own, so two distinct sessions share an `S<N>` by construction. Keep `S<N>` unique
within a sequence if you can (never renumber an already-written receipt to do it — a visible gap
that closes on merge is the lesser defect), but do not treat a repeated id across sequences as
corruption. `bin/check-handoff --all` keys on the pair for this reason.

## Size, and when to archive

This file gains a receipt every session and Phase 0 reads it every session, so it carries the same
size discipline as `CHANGELOG.md`: **two caps, two distinct failure modes, fire if either fires,
stop only when both stop conditions hold.**

| Cap | Protects against | Form | Fire when | Cut until |
|---|---|---|---|---|
| **Lines** — ~2,000, a **proxy** for the agent `Read` cap (the cap itself is denominated in **tokens**, not lines) | **measures an unread tail** — it does not, on its own, establish a remedy. A read past the cap returns only the prefix that fits, and says so: a `PARTIAL view` banner names the delivered span and the true length, and an explicit over-cap line range errors outright. **Announced, not silent.** **Whether archiving the tail REMEDIES this is an open question, not a settled benefit.** Truncation is ordered top-down and this file is newest-on-top, so the records a cut removes are ones a whole-file read was not delivering anyway: the delivered prefix is the same before and after, and what changes is that the reader stops being warned. Raised as BL-52. **Re-measure rather than trusting this row** — the reproduction is `docs/planning/read-cap-premise-correction-plan.md` Appendix A in the framework repo | a **rate** | headroom < **15** receipts | headroom > **30** |
| **Bytes** — a per-file budget, default **65,536 B** (64 KB) | **context tax**: every session pays for the whole file, every time | a **level with hysteresis** | `size > budget` | `size ≤ ½ × budget` |

**Run this rather than estimating it:**

```sh
python3 methodology_trim.py --file HANDOFFS.md --check
```

`--check` evaluates both conditions and never writes. `--write` performs the trim, refuses unless it
can prove the split lossless, and **neither commits nor stages** — it leaves this file modified and
the new shard *untracked*, and leaves the commit to you (`git add HANDOFFS.md docs/archive/`).

An archive is a **shard**: a new frozen file, same format, same newest-on-top order.

- **Path: `docs/archive/HANDOFFS-through-<CUT-KEY>.md`.** Both halves are load-bearing — the
  directory keeps the shard from shadowing this file, and the `HANDOFFS-` prefix is what the
  trigger's own glob looks for. A shard named otherwise is silently invisible to it.
- **This file keeps one short pointer** naming each shard, the span it covers and how many receipts
  it holds — with the command that recomputes those counts, never a hand-maintained number.
- **The shard back-links here and states only facts about itself.** It must not restate a
  forward-looking rule: a shard is frozen, so a rule copied into one cannot be corrected when the
  live rule moves.
- **After a split, anything that enumerates receipts must span both** — `HANDOFFS.md
  docs/archive/HANDOFFS-*.md` — or it silently counts a shrunken population.

If a `CHANGELOG.md` sits beside this file, its own **Size, and when to archive** section carries the
reasoning both files share: why the line cap must be a rate, why the byte cap cannot be one, and how
to choose the budget. Everything needed to *act* is here.

What is specific to *this* file, and gets receipts wrong if assumed:

- **A record is a `handoff` block *plus the prose beneath it*, not the fence alone.** The self-score
  and predecessor-score paragraphs sit outside the fence and belong to the receipt above them. A
  fence-only cut severs every receipt from its own scoring.
- **Archive oldest-first by position, never by sorting on `session:`.** Two independent `S<N>`
  sequences can share one ledger — a fork and its upstream each running their own counter — and
  their numbers collide. The record's identity is **session + date**.
- **A trim leaves the newest-receipt check alone and moves what the older-receipt checks see.**
  Phase 0 reconcile is frontier-based and a structural checker applies the full schema to the newest
  receipt only, so neither is disturbed. Its other passes are not so confined — an answer-slot rule
  reads every receipt below the newest, and a locator-form rule reads every receipt in the file. So
  after a trim, **run the checker against each shard as well**, and recompute any "all N older
  receipts" count from the files rather than carrying it forward.
- **Never trim to zero receipts.** An empty receipt ledger is indistinguishable from a broken one.
- **A shard freezes, with one exception this file needs:** a `commit:` answer slot may still be
  reconciled inside an archived receipt, because that field was always going to be filled by a later
  session. Nothing else in a shard is rewritten.

## Three files, three questions, one shared key

- **`SESSION_NOTES.md`** — the *transient scratchpad*: rich working notes, overwritten every session.
- **`HANDOFFS.md`** (this file) — the *durable receipt*: the distilled, machine-checkable proof that
  the handoff was written. Nothing is ever deleted; once the file outgrows a session's read, the
  oldest receipts move to a frozen shard (see **Size, and when to archive** above).
- **`CHANGELOG.md`** — the *cumulative action ledger*: *"what was done here, ever?"*, append-only.

The shared key across all three is the commit sha (`changelog_ref` / `commit` here). This file
**distills** the handoff; it does not copy the scratchpad. The belongs-here test: *would the next
session need this block to continue the work without re-reading the whole repo?*

---

<!-- Receipts go below, newest on top. Delete the seed-sentinel line above when you add the first one. -->

```handoff
session: S11
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 9
active_task: Test suite. docs/planning/test-suite-plan.md is approved, and Phases 1 and 2 are complete on main (Phase 2 is fa73763). Next session implements Phase 3 only (the serial path), on a new branch off main. main is the only branch and is pushed with this amended close-out. GitHub now allows merge commits only (squash and rebase off), so learning #6 is a gate for PR merges. No product code has changed since e5f52e1.
what_was_done: Claim 7d02af9. Every Phase 2 behaviour was probed in the scratchpad through the test client with TESTING on before any test was written; the probe showed D2 and D3 raise ValueError and AttributeError into the caller instead of answering 500. Tests fa73763: tests/test_csv_routes.py, 19 passing tests (T2.1-T2.8) and 3 strict xfails (D2 timeseries half, D3, D4), each naming the exception it raises today with raises=. tests-passed tightened 9 -> 28. Six red-drives, each restored: .lower() removed at app.py:261 fails T2.4; data[:500] fails the last-500 test; _csv_data[0] fails the last-row test; the ; branch disabled fails T2.3's semicolon case; a real D4 fix (utf-8-sig) gives XPASS(strict) and fails the suite; a hidden test fails tests-passed (27). The plan gains an "As implemented (Session 11)" note. Two findings that the plan doesn't cover went to open item 4 (renumbered from 5) with no tests: has_csv stays true after an empty upload while source is null, and CSV mode ignores ?hours=. At Phase 0 the operator asked what the merge-settings item means (squash and rebase merges rewrite the SHAs the records cite) and picked Phase 2. On the operator's direction (a picker before close-out): a fetch and a secret scan, main fast-forwarded to the branch, the branch deleted, and main pushed with this commit. "Session 8 Handoff Evaluation" and "What Session 9 Did" were archived from SESSION_NOTES.md. First close-out 803a785, pushed. After it, the operator asked why the merge-settings item had been ranked behind Phase 2 (there was no good reason) and directed it done: gh repo edit --enable-squash-merge=false --enable-rebase-merge=false, confirmed by gh repo view (merge true, squash false, rebase false). CLAUDE.md learning #6 records the gate; the old open item 4 is removed; this receipt, the notes and the ledger were brought up to the session's real end (learning #8).
next_steps: Implement Phase 3 of docs/planning/test-suite-plan.md (section 5, lines 357-433) on a new branch off main: tests/test_serial_reader.py (T3.1-T3.7, strict xfail D1), a FakeReader fixture in tests/conftest.py, tests/test_serial_routes.py (T3.8-T3.9, strict xfail D7), and tighten tests-passed in .quality-gates.json. Four commits: the claim; test_serial_reader.py, conftest.py and a ledger entry; test_serial_routes.py, the gate and a ledger entry; the close-out. DONE: the suite exits 0 with exactly 5 xfailed, the ratchet passes 2/2, one red-drive is recorded (delete the "humidity": "rh" mapping at serial_reader.py:147), the suite runs well under 10 s, and no product file shows in git diff. P4 (API) follows, then the D1-D7 fix sessions, D1 and D7 first.
key_files: tests/test_csv_routes.py:26, tests/test_csv_routes.py:41, tests/test_csv_routes.py:101, tests/test_csv_routes.py:159, .quality-gates.json:24, docs/planning/test-suite-plan.md:341, docs/planning/test-suite-plan.md:357, serial_reader.py:62, serial_reader.py:89, serial_reader.py:106, serial_reader.py:140, serial_reader.py:147, app.py:38, app.py:141, app.py:175
gotchas: The client fixture runs with TESTING on, so a route's exception reaches the test and no 500 comes back; name each xfail's exception with raises=. D1 and D7 both fail on an assertion today (probed for D1), so both take raises=AssertionError. The isolated fixture resets _serial_reader but stops no thread: any test that sets SERIAL_PORT and calls a data route starts a real daemon thread through get_serial_reader() (app.py:47). Call stop(), and never join(). The plan's own line numbers moved by 7 after the Session 11 note, but its product-code citations didn't. Keep "passed" out of reason= strings. The ratchet's results hash changes only when a measurement changes; cite the final run. Stage files by name: 4 untracked tool and render outputs remain (open item 2). Back up a new untracked test module by explicit path to the scratchpad before a red-drive mutates it. The MEDIUM "thin coverage" stays until the tests total 548 lines (342 now), so don't pad.
runtime_smoke: Tests only; no product runtime behaviour changed. python3 -m pytest -q and plain pytest -q: 28 passed, 3 xfailed, exit 0. quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0dc3acde972e · manifest 770382cd43d3
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 11 close-out amended — merge-settings gate recorded, receipt brought to session end"
commit: fa73763
```
Session 11 (Claude Opus 5, single-tier) implemented Phase 2 of the test-suite plan. With no data source, every JSON
route's answer is now pinned, and so is the CSV upload path. The suite gives 28 passed and 3 strict xfails, and the
ratchet holds tests-passed at 28. It scored Session 10's handoff 9/10: the recipe, citations and gotchas were exact,
except one gotcha that said the ratchet hash changes every run. It scored itself 7/10 (8 at the first close-out). (+) Every asserted behaviour
was probed on the suite's own setup first, which surfaced the TESTING difference and two new findings. Six
red-drives covered each targeted test, the strict-xfail flip and the tightened gate. Scope held, and the landing was
decided before close-out. (−) There were four harness nudges for silence. One pipeline checked tail's exit code
instead of pytest's. The first picker didn't explain open item 4. A draft of this handoff cited a line number read
off a multi-file `cat -n`, which the pre-commit re-grep caught. The merge-settings item was ranked behind Phase 2
without being weighed on its merits, and the operator had to ask why; after close-out it was done on their go-ahead.

```handoff
session: S10
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 8
active_task: Test suite. docs/planning/test-suite-plan.md is approved, and Phase 1 (the harness and the setup-banner guard) is complete on main: 067455f and 4da62a1. Next session implements Phase 2 only (the no-source contract and the CSV path), on a new branch off main. main is the only branch and is pushed with this close-out. No product code has changed since e5f52e1.
what_was_done: Claim 02016aa, which records the operator's approval on the plan's Status line. Harness 067455f: requirements-dev.txt, pytest.ini, tests/conftest.py (the isolated autouse fixture) and tests/test_dashboard_page.py, 9 tests (T1.1-T1.7). A probe showed that the plan's red-drive (autouse off fails T1.7) did not hold on a machine with no .env, so a module fixture, planted_leak, plants all 8 variables and the 3 globals. A second T1.7 test scans app.py's os.getenv names. Wire-up 4da62a1: .gitignore gains .pytest_cache/, README gains "Running tests" and a tests/ row, and .quality-gates.json gets tests-exit (max 0) and tests-passed (min 9). Seven red-drives, each restored: the pre-Session-7 banner fails T1.1; autouse=False fails 6 tests; a variable dropped from CONFIG_VARS fails T1.7; a new os.getenv fails the scan test; a failing test fails tests-exit; a hidden test fails tests-passed; a loosened threshold is REFUSED by --precommit. Dashboard 54 -> 62/100, with 0 HIGH risks. On the operator's direction (a picker before close-out): a fetch and a secret scan, main fast-forwarded to the branch, the branch deleted, and main pushed with this commit. CLAUDE.md learning #9. The Session 7 evaluation and "What Session 8 Did" were archived from SESSION_NOTES.md.
next_steps: Implement Phase 2 of docs/planning/test-suite-plan.md (section 5, lines 299-348) on a new branch off main: tests/test_csv_routes.py with T2.1-T2.8 and strict xfails for D2 (timeseries half), D3 and D4, and tighten tests-passed in .quality-gates.json to the new measured count. Three commits: the claim; the tests, the gate and the ledger entry; the close-out. DONE: the suite exits 0 with exactly 3 xfailed, the ratchet passes 2/2, one red-drive is recorded (remove .lower() at app.py:261), and no product file shows in git diff. P3 (serial) and P4 (API) follow, then the D1-D7 fix sessions, D1 and D7 first.
key_files: tests/conftest.py:15, tests/conftest.py:9, tests/test_dashboard_page.py:29, tests/test_dashboard_page.py:57, tests/test_dashboard_page.py:122, tests/test_dashboard_page.py:129, .quality-gates.json:16, pytest.ini:1, README.md:25, docs/planning/test-suite-plan.md:299, docs/planning/test-suite-plan.md:262, app.py:236, app.py:245, app.py:261, CLAUDE.md:51
gotchas: The plan's P2 citations were re-grepped and hold (.lower() is at app.py:261); find line numbers with grep -n, not by counting sed output. Don't copy planted_leak into new test modules: T1.7 already proves isolated works everywhere, and a probe showed a global set by a route is reset between tests. No hook enforces the ratchet (core.hooksPath is unset), so tighten tests-passed in the same commit as the tests and run quality_ratchet.py --precommit by hand. P2 adds the first xfails, so keep "passed" out of reason= strings. Cite the ratchet summary line from the final run. Stage files by name: 4 tool and render outputs are untracked (open item 2). The MEDIUM "thin coverage" stays until the tests total 548 lines (166 now), so don't pad. Before a red-drive mutates an untracked file, back it up to the scratchpad by explicit path. context_budget.py reports SESSION_NOTES.md "instrument-failed", which is an upstream seed mismatch (open item 3), not this file's defect.
runtime_smoke: Tests only; no product runtime behaviour changed. python3 -m pytest -q and plain pytest -q: 9 passed, exit 0, 0 xfailed. quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 10 closed out — test-suite Phase 1 complete; main fast-forwarded, pushed with this commit"
commit: 4da62a1
```
Session 10 (Claude Opus 5, single-tier) implemented Phase 1 of the test-suite plan. The pytest suite runs (9
passed), the setup-banner fix has its guard, and the ratchet holds two gates. The dashboard moved from 54 to 62/100
with no HIGH risk left. It scored Session 9's handoff 8/10: the plan's recipe and gotchas were exact, but one DONE
red-drive held only where a `.env` exists. It scored itself 8/10. (+) The red-drive premise was probed and fixed
with one fixture; every guard and gate was driven red; scope held; the landing decision was asked before close-out
(learning #8). (−) A red-drive restore used `git checkout` on an untracked file and backed up to `$TMPDIR`; a
padded draft test got written; one red-drive was mislabelled; there were two harness nudges for silence; and a
draft of this handoff miscounted app.py:261 as :260, which the pre-commit re-grep caught.

```handoff
session: S9
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 9
active_task: Test suite. docs/planning/test-suite-plan.md (d813463) is on main and awaits the operator's approval. It has four phases, one session each: P1 harness + setup-banner guard, P2 no-source + CSV, P3 serial, P4 API. Next session implements Phase 1 only, on a new branch off main. main is the only branch, local and remote. No product code changed.
what_was_done: Claim 1177049. Read app.py, airqino_client.py, serial_reader.py, the template and dashboard.js, and ran the grep inventory (8 routes, 3 helpers, 15 client methods, 8 SerialReader methods, 9 env vars, 3 globals, every I/O and clock call). Scratch probes reproduced 7 defects, D1-D7 (plan section 4); none fixed. The operator chose pytest, strict xfail, monkeypatch fakes and Python-only scope in one four-question picker. A scratchpad spike verified the .env leak and the isolation fixture, pytest.ini, the pty round trip, fake-client injection and the two ratchet gates (5 passed, 2 xfailed; ratchet 2/2), and drove 3 guards red. Plan committed as d813463; 6 citations were corrected by a post-write re-grep. First close-out f49da64 added CLAUDE.md learning #7 and archived the Session 5-7 notes. On the operator's direction afterwards: main was fast-forwarded to f49da64 and pushed with 4973cf7, after a fetch, an ancestor check and a secret scan; the local branch was deleted with git branch -d, and 5cc4ce9 pushed. This amended close-out brings the handoff and this receipt up to the session's end and adds learning #8.
next_steps: With the operator's approval, implement Phase 1 of docs/planning/test-suite-plan.md (section 5, lines 161-290) on a new branch off main: requirements-dev.txt, pytest.ini, tests/conftest.py (text in the plan), tests/test_dashboard_page.py T1.1-T1.7, .gitignore, README.md and two gates in .quality-gates.json, in four commits of 5 files or fewer. Then P2-P4 and the D1-D7 fixes in plan order, with D1 and D7 first because the serial adapter is next.
key_files: docs/planning/test-suite-plan.md:161, docs/planning/test-suite-plan.md:122, app.py:12, app.py:19, app.py:51, templates/dashboard.html:33, templates/dashboard.html:55, quality_ratchet.py:266, README.md:11, CLAUDE.md:49, CLAUDE.md:50
gotchas: load_dotenv() walks up to / for a .env, so keep the isolated fixture autouse. Never set SERIAL_PORT in a test without a fake reader or a pty, because a real thread starts. Don't ban "USB port" in T1.1: the correct banner says "no USB port". Assert on the badge markup ">No Data Source<", since an HTML comment also matches. Keep "passed" out of xfail reasons, because the gate's regex scans the -ra output. After P1 the dashboard shows MEDIUM "Test coverage is very thin", which is expected: 4,412 of the 5,475 source lines are vendored tooling, so don't pad tests. Stage files by name. The first close-out's ledger entry says the branch "stays local and unpushed"; the later entries supersede it. The amended close-out commit may not be pushed yet, so check git status -sb.
runtime_smoke: n/a — docs-only. git diff 15b0a3f -- '*.py' templates static is empty. The spike ran the app's own code in scratchpad copies: 5 passed, 2 xfailed, quality_ratchet 2/2 pass.
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 9 close-out amended — follow-on git actions recorded, receipt brought to session end"
commit: d813463
```

Session 9 (Claude Opus 5, single-tier) ran on 2026-09-17. The operator picked "plan a test suite" from the Phase 0
picker, then chose the recommended option on all four questions in a second, pre-design picker: pytest, strict xfail
for known defects, monkeypatch fakes, Python only. Actions: the claim, the plan, the first close-out, the plan
branch fast-forwarded into main and pushed, the local branch deleted, a second push, and this amended close-out. Probes
found 7 real defects, 2 of them on the serial path the operator will use next. Self-score 7/10, down from the first
close-out's 8. (+) Probed before asserting; the spike measured the plan's mechanics, with red-drives; decisions were
made before the design; no product code touched; each git step checked before it went outward. (−) 6 citations were
written from memory (caught before the commit); one stray /tmp write; three harness prompts for silence; and the
close-out went stale after the follow-on actions until the operator asked for it (learning #8). Predecessor (Session 8)
scored 9/10: exact surfaces and first test case; it lacked only toolchain facts. Full notes are in `SESSION_NOTES.md`
under "What Session 9 Did".

```handoff
session: S8
date: 2026-09-17
status: complete
self_score: 9
predecessor_score: 9
active_task: No task in progress. Branch/PR housekeeping is complete: the four-branch stack is merged into main, main is the only branch (local and remote), and no PRs are open. SESSION_NOTES.md lists four open items; pick ONE, with planning a test suite recommended.
what_was_done: Claim a31fea6. Before proposing anything, checked the remote (public, no branch protection, no CI, all merge methods allowed), ran a merge-tree conflict check (clean), and scanned the 11 unpublished commits for secrets (none). The operator approved the recommended option on all four questions. PR #1 was merged with a merge commit as 9099569. fix/usb-serial-banner was pushed and PR #2 opened for dfe26fd..a31fea6, then merged with a merge commit as 8554078. Local main was fast-forwarded from 03510d3. Every stack branch and cited SHA was confirmed to be an ancestor of main before deletion; the 4 local branches were deleted with git branch -d, and the 2 remote branches deleted and pruned. git diff a31fea6 main is empty. Close-out added CLAUDE.md learning #6 (never squash or rebase) and archived the Session 4 evaluation and the Session 5 notes from SESSION_NOTES.md.
next_steps: Plan a test suite (open item 1): a planning session writing docs/planning/test-suite-plan.md with a grep-based inventory of app.py (8 non-static routes; active_source() at app.py:51), airqino_client.py and serial_reader.py. The first case: render / through Flask's test client with no data source and assert "Serial Adapter" is present and "Arduino" absent. Alternatives: decide the untracked files, give CLAUDE.md a fenced statement of purpose, or (operator's call) disable squash and rebase merges on GitHub to make learning #6 a gate.
key_files: CLAUDE.md:48, app.py:51, app.py:64, requirements.txt:1, SESSION_NOTES.md:19
gotchas: Start from main and branch for the deliverable; the stack branches are gone. git log now shows merge commits; the ledger reconcile uses --no-merges, but a PR merge still needs its own entry. Never squash or rebase a PR here (learning #6); GitHub still offers both. The close-out commit's push happens after its ledger entry is written, so check git status -sb on main. Verification tools write untracked files, so stage by name.
runtime_smoke: n/a — no file content changed: git diff a31fea6 main is empty, so Session 7's runtime check of the banner still holds. All 7 root .py files parse; app imports with 8 non-static routes.
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 8 closed out — four-branch stack merged into main; main is the only branch"
commit: pending
```

Session 8 (Claude Opus 5, single-tier) ran on 2026-09-17. The operator picked branch/PR housekeeping from the Phase 0
picker, then approved the recommended option on all four questions in a second picker: merge PR #1, then one PR for the
rest, with merge commits; Session 8 merges; delete local and remote branches; push the close-out to main. Actions: claim
commit, PR #1 merged, PR #2 opened and merged, branch cleanup, close-out. The session found an unrecorded constraint: squash
or rebase would orphan the SHAs the ledger cites (now learning #6). Self-score 9/10. (+) No outward action before approval;
public-repo checks before publishing; containment and tree identity proved before deleting. (−) One harness nudge for
silence; Phase 0 took seven tool rounds. Predecessor (Session 7) scored 9/10: exact stack layout; it missed that local
main was 1 ahead of origin and the SHA-citation constraint. Full notes are in `SESSION_NOTES.md` under
"What Session 8 Did".

```handoff
session: S7
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 9
active_task: No task in progress. The setup-banner fix is complete on the local branch fix/usb-serial-banner, off e947798. SESSION_NOTES.md lists four open items; pick ONE, with branch/PR housekeeping recommended.
what_was_done: The Phase 0 report ended with an AskUserQuestion picker, as the operator asked, and the operator picked open item 1. Claim 38920e3. Fix e5f52e1: templates/dashboard.html option 2 is now "Serial Adapter". It says the REV6 has no USB port and to wire a 3.3V USB-to-TTL adapter to the TX and GND pins (see docs/HARDWARE.md). Learning #3 in CLAUDE.md now uses the past tense. A git grep of every tracked surface found the old wording only in the template before the fix, and only in learning #3's historical quote after it. Close-out added CLAUDE.md learning #5 (the UI runtime-verification recipe) and archived "What Session 4 Did" from SESSION_NOTES.md.
next_steps: Branch/PR housekeeping (open item 1). With the operator's go-ahead, push or merge the four-branch stack in order: chore/methodology-pr2527-remediation (PR #1, 0c59e5e), then chore/methodology-read-set-budgets (1402ad4), then chore/methodology-bl57-p6 (e947798), then fix/usb-serial-banner (this session). Alternatives: decide the untracked files, give CLAUDE.md a fenced statement of purpose, or plan a test suite whose first case is a setup-banner render test.
key_files: templates/dashboard.html:54, app.py:51, static/css/dashboard.css:65, CLAUDE.md:45, CLAUDE.md:47, docs/HARDWARE.md:33
gotchas: The banner renders only when active_source() finds no source (no AIRQINO_CLIENT_ID or SERIAL_PORT in the environment or .env, and no uploaded CSV). Headless Chrome --screenshot against this app writes the PNG but never exits, so run it in the background and stop it. The Phase 0 picker preference is in agent memory, not in the repo. All branches except PR #1's are local only. Verification tools write untracked files, so stage files by name.
runtime_smoke: python3 app.py with no data source: GET / returned 200 with the new banner text and 0 matches for Arduino or USB cable. A headless-Chrome screenshot at 1200x700 shows the three setup cards with no overflow. The server was stopped and port 5001 is free.
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 7 closed out — setup-banner serial fix complete"
commit: pending
```

Session 7 (Claude Opus 5, single-tier) ran on 2026-09-17. The operator asked for the Phase 0 report to end with a picker,
then chose open item 1 from it. Three commits, each with its own ledger entry: claim, fix and close-out. The fix corrects
the last surface still carrying the pre-Session-2 "Arduino Mega USB port" claim, and was verified in the running app, the
first time a session has booted it. Self-score 8/10. (+) Claim committed first; every surface grepped before and after;
the served page and a screenshot were checked; FM #28 reduction done. (−) Three harness nudges for long silences; the
heading rename was a user-facing call made without asking; a headless-Chrome hang cost a 60 s timeout; no automated guard
(no test infrastructure). Predecessor (Session 6) scored 9/10: its open item 1 could be executed as written; it missed
that learning #3's "still lives" claim would need updating. Full notes are in `SESSION_NOTES.md` under
"What Session 7 Did".

```handoff
session: S6
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 9
active_task: No task in progress. Methodology BL-57 phase P6 for airqino, with BL-56 folded in, is complete on the local branch chore/methodology-bl57-p6. SESSION_NOTES.md lists five open items; pick ONE.
what_was_done: Claim 2b0230a recorded the CHANGELOG.md block (lines 1-11) before any edit. 28022fe synced from fork main ff02b5c after a clean dry run: 12 tracked files updated, quality_ratchet.py and an empty .quality-gates.json created. 5e4b483 replaced the Keep-a-Changelog header with the thin seed's header (sentinel and ## [Unreleased] dropped; every entry byte-identical). 9f150a5 added CLAUDE.md ledger conventions. All plan P6 DONE items pass: bin/status reads present from fork main and upstream main 6b29d3d; §9.8 prints "only the block changed"; headings and audit went 4 to 5 across the migration, as predicted. Close-out removed the Session 1-3 history from SESSION_NOTES.md.
next_steps: Fix the stale USB Serial banner at templates/dashboard.html:55 ("connect a USB cable to the Arduino Mega port") so it describes the REV6 USB-to-TTL adapter path in docs/HARDWARE.md:33, then grep every surface for the old wording (CLAUDE.md learning #3). Separately, a methodology-repo session should mark P6 and BL-56 done and correct the plan's P6 row (the Route A reason is stale; there were two entries, not one).
key_files: CHANGELOG.md:12, CLAUDE.md:28, SESSION_NOTES.md:18, templates/dashboard.html:55, .quality-gates.json:16
gotchas: One CHANGELOG entry per commit, and the claim commit carries an (in progress) one. [BL-<id>] means this repo's BACKLOG.md only; methodology work is [ad hoc]. The first 2026-10 entry opens ## 2026-10; never add ## 2026-09. quality_ratchet.py --run and context_budget.py write untracked files (.quality-gates-results.json, .context-budget-history.jsonl), so stage by name. context_budget.py shows 3 red findings that predate this session (CLAUDE.md purpose fence missing; SESSION_NOTES.md long lines; a ^## pattern minimum); fix them in plan mode, never by loosening a ceiling. All branches except PR #1's are local-only.
runtime_smoke: n/a for the app — no app code changed; app imports with 9 routes. The synced tools each ran: dashboard v2.18.0 (54/100), quality_ratchet.py --run 0/0 gates, methodology_trim.py --check (does not fire).
changelog_ref: CHANGELOG.md "2026-09-17 · [ad hoc] Session 6 closed out — methodology BL-57 P6 for airqino complete; Sessions 1–3 notes archived"
commit: pending
```

Session 6 (Claude Opus 5, single-tier) ran on 2026-09-17. The operator assigned methodology BL-57 phase P6 for this repo and
directed the route: fork `main` rather than the plan's branch, since a dry run showed BL-54 no longer refuses files. Five
commits, each with its own ledger entry, did the job: claim, sync, header migration, `CLAUDE.md` conventions and close-out.
Every DONE item was verified with counts re-derived per commit, and BL-56's "both `bin/status` versions" criterion was
checked by running upstream `main`'s `bin/status` from a scratch clone. Self-score 8/10. (+) The claim was committed on its
own with the block range; each entry's claims were verified before its commit; the older budget findings were reproduced on
`1402ad4`, not assumed. (−) The 15-file sync commit went over the 5-file cap without first asking; `git fetch upstream` in
the methodology repo; verification side-effect files needed cleanup; two long silences. Predecessor (Session 5) scored 9/10:
its "carry both entries" and #80 cherry-pick gotchas were exact, and one plan line citation (`:584`) had decayed. Full notes
are in `SESSION_NOTES.md` under "What Session 6 Did".

```handoff
session: S5
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: No task in progress. Session 5 was orientation-only; the operator closed it at the Phase 0 STOP, so no deliverable was produced. The SESSION_NOTES.md ACTIVE TASK was refreshed (it had gone stale) and lists four open items; pick ONE.
what_was_done: Phase 0 in full, then close-out. Traced the four post-Session-4 commits (66abe78, 28db357, 0c59e5e, dfe26fd) to methodology-repo sessions by hash, so no ghost sessions; the CHANGELOG and HANDOFFS reconciles were no-ops. Close-out rewrote the stale ACTIVE TASK, added CLAUDE.md learning #4, wrote this first receipt and added the CHANGELOG entry, all in one close-out commit.
next_steps: Fix the stale USB Serial setup-banner text at templates/dashboard.html:55 ("connect a USB cable to the Arduino Mega port") so it describes the REV6 USB-to-TTL adapter path in docs/HARDWARE.md:33, then grep every surface for the old wording (CLAUDE.md learning #3).
key_files: templates/dashboard.html:55, docs/HARDWARE.md:33, CLAUDE.md:39, SESSION_NOTES.md:7
gotchas: The HEAD branch chore/methodology-read-set-budgets is local-only and carries dfe26fd plus this close-out commit on top of PR #1's head 0c59e5e; if it is re-synced or discarded, cherry-pick the close-out commit. The harness's session-start git snapshot was stale in Sessions 4 and 5, so run git status and git reflog yourself. CHANGELOG.md now has two entries, but methodology plan P6 (BL-56) assumes one; whoever runs P6 must carry both.
runtime_smoke: n/a — docs-only close-out
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] Session 5 — orientation-only session closed out; no deliverable"
commit: pending
```

Session 5 (Claude Opus 5, single-tier) started 2026-09-14 and closed 2026-09-15. The Phase 0 report found the repo on a
branch that a methodology-repo session had created after the session-start snapshot was taken; four commits with no airqino
session notes, all traced by hash to methodology-repo sessions; and a stale ACTIVE TASK. The operator closed the session
without assigning a task. Self-score 8/10: (+) full Phase 0 including the reconcile, reflog-based provenance, the pre-ledger
finding measured rather than assumed, git state left alone during a concurrent session; (−) no deliverable, one commit-subject
misattribution in the Phase 0 report (`66abe78`), and the Phase 1B stub was not committed separately. Predecessor (Session 4)
scored 9/10: its one recommended next deliverable was exact, and two "pending" phrases aged badly. Full notes are in
`SESSION_NOTES.md` under "What Session 5 Did".
