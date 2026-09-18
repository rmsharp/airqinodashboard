# CLAUDE.md

## SESSION PROTOCOL — FOLLOW BEFORE DOING ANYTHING

**Read and follow `SESSION_RUNNER.md` step by step.** It is your operating procedure for every session. It tells you what to read, when to stop, and how to close out.

**Three rules you will be tempted to violate:**
1. **Orient first** — Read SAFEGUARDS.md -> SESSION_NOTES.md -> run `methodology_dashboard.py` -> git status -> report findings -> WAIT FOR THE USER TO SPEAK
2. **1 and done** — One deliverable per session. When it's complete, close out. Do not start the next thing.
3. **Auto-close** — When done: evaluate previous handoff, self-assess, document learnings, write handoff notes, commit, report, STOP.

`SESSION_RUNNER.md` documents known failure modes and their countermeasures. The protocol compensates for documented tendencies to skip orientation, skip close-out, and continue past the deliverable.

---

## Project-Specific Methodology Adaptations

*Additions and overrides to the base methodology at `SESSION_RUNNER.md` and `SAFEGUARDS.md` (synced from canonical, not project-owned). The base files govern unless explicitly overridden here. **Do not edit the synced files** — put customizations here.*

### Additional Phase 0 steps

(none)

### Additional task-to-workstream mappings

(none)

### Ledger (`CHANGELOG.md`) conventions

The rules are `docs/methodology/FRAMEWORK_APPARATUS.md` §The Action Ledger. This project adds two conventions:

- **Source tags.** `[BL-<id>]` names an item in *this* repo's `BACKLOG.md`. Work that comes from the methodology repo's backlog, such as a sync or BL-57's header migration, is tagged `[ad hoc]` and names the methodology item in its summary.
- **Legacy layout, left as written.** Session 6 migrated the header to `ledger-format: 2` (`5e4b483`) and dropped the old Keep-a-Changelog `## [Unreleased]` heading. So the 2026-09 entries sit under no month heading, and the first `## YYYY-MM` heading opens with the first 2026-10 entry. Don't add `## 2026-09` above them. The 2026-09-14 and 2026-09-15 entries have prose bodies instead of the detail bullets. They stay that way, because entries are never edited.

### Project-specific Learnings

<!-- This table is loaded every session and grows with no cap. When CLAUDE.md nears its
     size budget, extract these rows to a committed PROJECT_LEARNINGS.md at the project
     root and replace them with a one-line pointer (read on demand). See BOOTSTRAP.md Step 5. -->

| # | Learning | Source | When to Apply |
|---|----------|--------|---------------|
| 1 | Hardware assumptions from research papers may not match the actual device revision. Session 1 described "Arduino Mega + SIM900 GPRS" based on published literature; the actual REV6 board (2022) is a custom PCB with no USB port. Physical verification trumps literature-based assumptions for hardware projects. | Session 2 hardware investigation | When documentation references specific hardware components, verify against the physical device before writing connection instructions or buying parts. |
| 2 | Verify product availability before recommending a purchase. First adapter recommendation was out of stock, requiring a second round of research and a doc update. Check stock status as part of the recommendation, not after. | Session 2 adapter research | When recommending specific products for purchase. |
| 3 | A factual correction landed in one surface but not its duplicates. Session 2 fixed the "no USB / Arduino Mega" hardware claim in `serial_reader.py`, `.env.example`, and `docs/HARDWARE.md`, but the same stale "connect a USB cable to the Arduino Mega port" copy stayed in the UI (`templates/dashboard.html:54-55`) until Session 7. Doc fixes don't auto-propagate to user-facing strings. | Session 4 (found while writing README) | When correcting a factual/hardware claim, grep ALL surfaces for the old wording — templates, JS, docs, comments — not just the module that prompted the fix. |
| 4 | The harness's session-start git snapshot and `SESSION_NOTES.md`'s ACTIVE TASK both go stale here, because other actors commit to this repo between and during sessions. Session 4's Phase 0 snapshot missed an out-of-session edit. In Session 5, a methodology-repo session had switched the branch and committed `dfe26fd` after the snapshot was taken, and three June re-vendor commits had left the ACTIVE TASK wrong for three months. Methodology-repo sessions keep their notes in `~/Development/methodology`, not here (the session-notes boundary rule in `SESSION_RUNNER.md`). | Session 5 orientation | At every Phase 0, run `git status` and `git reflog -5` yourself instead of trusting the snapshot. For commits newer than the last airqino session, find their record with `git -C ~/Development/methodology log --all -S<sha>` before calling them ghost sessions. Search by hash: matching on commit subjects misattributed `66abe78` in Session 5. |
| 5 | The Flask UI can be runtime-verified without the device. With no data source configured (no `.env`, no uploaded CSV), `/` renders the setup banner. Start `python3 app.py` in the background, `curl` port 5001 and grep the HTML, then take a headless-Chrome screenshot (`--headless=new --screenshot=<png> --window-size=1200,700`). That checks a template change end to end. In Session 7, Chrome wrote the PNG within seconds but its process never exited, so run it in the background and stop it. | Session 7 banner fix | Any change to `templates/`, `static/` or a route's output. Check the rendered page, not only the source, then stop the server and Chrome and confirm port 5001 is free. |
| 6 | The session records cite commits by SHA. `CHANGELOG.md` entries, `HANDOFFS.md` receipts and the `git show <sha>:SESSION_NOTES.md` archive pointers all do. A squash or rebase merge rewrites those SHAs, and deleting the branch afterwards leaves every citation pointing at nothing. Session 8 merged PR #1 (`9099569`) and PR #2 (`8554078`) with merge commits for this reason. GitHub still allows all three methods (Session 8 open item 4 proposes turning squash and rebase off). | Session 8 branch housekeeping | Merging any PR or branch into `main`: use a merge commit (`gh pr merge --merge`) or a fast-forward, never `--squash` or `--rebase`. Before deleting a branch, confirm with `git merge-base --is-ancestor` that it and every SHA the ledger cites are in `main`. |

### Project-specific Failure Modes

(none — the base failure modes in `SESSION_RUNNER.md` apply.)
