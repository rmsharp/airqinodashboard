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
