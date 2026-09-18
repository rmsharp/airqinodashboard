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
