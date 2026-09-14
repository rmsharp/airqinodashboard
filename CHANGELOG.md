# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

When completing work, remove the item from `BACKLOG.md` and add an entry here.

## [Unreleased]

<!-- Add entries here as work is completed. Group by month when the list grows. -->

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
