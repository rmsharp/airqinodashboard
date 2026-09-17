# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

When completing work, remove the item from `BACKLOG.md` and add an entry here.

## [Unreleased]

<!-- Add entries here as work is completed. Group by month when the list grows. -->

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
