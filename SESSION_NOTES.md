# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** Open — no task in progress. Session 6 (2026-09-17) completed methodology BL-57 phase P6 for airqino,
with BL-56 folded in. Next session picks ONE open item below.
**Status:**
- **Methodology BL-57 P6 / BL-56: DONE** on branch `chore/methodology-bl57-p6` (local): claim `2b0230a`, sync from fork
  `main` `28022fe`, `CHANGELOG.md` header migration `5e4b483`, `CLAUDE.md` ledger conventions `9f150a5`, plus the close-out
  commit. Fork `main`'s and upstream `main`'s `bin/status` both read `CHANGELOG.md` as `present`. Marking P6 and BL-56 done
  in the methodology repo's plan and backlog belongs to a methodology-repo session.
- Earlier status (PART 2 re-vendor, README) and the Session 1–3 history: `git show 1402ad4:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix the stale USB Serial setup-banner text — recommended next.** `templates/dashboard.html:55` still says
   "Open the enclosure and connect a USB cable to the Arduino Mega port." The REV6 board has no USB port (`docs/HARDWARE.md:33`);
   the real path is a USB-to-TTL adapter on the board's TX/RX pins. After the fix, grep every surface for the old wording (`CLAUDE.md` learning #3).
2. **Decide the untracked files** — operator's call for each: commit, gitignore, or delete. `docs/HARDWARE.html` has been
   untracked since Session 3 (an HTML render of `docs/HARDWARE.md`). Three tool outputs have no `.gitignore` entry:
   `dashboard_history.jsonl` (written by every dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`;
   the `.quality-gates.json` seed says to gitignore it); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Branch/PR housekeeping** — three stacked branches. PR #1's `chore/methodology-pr2527-remediation` (`0c59e5e`) is pushed
   and open. On it sits `chore/methodology-read-set-budgets` (`dfe26fd`, `1402ad4`), local. On that sits
   `chore/methodology-bl57-p6` (Session 6's commits), local and HEAD. Push and merge order is the operator's go-ahead.
4. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence missing
   (`.context-budget.json` declares it for `CLAUDE.md`, minimum 800 B). `CLAUDE.md` has never had a fence or a Purpose
   section. `README.md`'s opening is the source text.
5. **Test suite** — the dashboard's only HIGH risk factor is "No test infrastructure" (0 test files; health 54/100).
   A bigger deliverable; start with a planning session.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### Session 5 Handoff Evaluation (by Session 6)
- **Score: 9/10**
- **What helped:** Two gotchas turned out to be exactly this session's traps. First, "CHANGELOG now has two entries, not
  one … carry both": the plan's P6 row still says "carry its one entry across". Second, the branch gotcha (after #80 merges,
  cherry-pick the close-out commit) became live when #80 merged on 2026-09-15. The operator branched off `1402ad4`, which
  keeps that commit. Learning #4 turned the stale-snapshot check into one `git reflog`. The FM #28 estimate (~410 lines)
  called for archiving the Session 1–3 history at this close-out, and this close-out did it.
- **What was missing:** Nothing Session 5 could have supplied. The new ledger rules (one entry per commit, an *(in progress)*
  claim entry, month grouping) arrived with this session's sync.
- **What was wrong:** One citation decayed. `changelog-rules-contradictions-plan.md:584` no longer points at the P6 row,
  which is at `:760` today because the plan grew. The section name (`§P6–P11`) or a quoted phrase would have survived. This
  is the same "built to go stale" point Session 5 made about Session 4. "Don't reformat the file in a project session" was
  sound until the operator assigned P6 here.
- **ROI:** Positive. The notes gave the branch context and the two-entry warning with no discovery needed.

### What Session 6 Did
**Deliverable:** Methodology BL-57 phase P6 for airqino, BL-56 folded in — **COMPLETE**
**Started / Closed:** 2026-09-17 · branch `chore/methodology-bl57-p6` off `1402ad4` (local, not pushed)
**Governing doc:** `~/Development/methodology/docs/planning/changelog-rules-contradictions-plan.md` §P6–P11 (P6 row
`:760`; §9.8 block check `:977`); BL-56 detail at `docs/planning/BACKLOG-DETAIL.md:1682` in the same repo.
**Ledger:** 5 `CHANGELOG.md` entries, one per commit (claim, sync, migration, `CLAUDE.md`, close-out).

**What was done:**
- **Claim** `2b0230a`: the stub, a pending receipt, and an *(in progress)* entry. It recorded the block to replace
  (`CHANGELOG.md` lines 1–11, 0 `### ` lines) in a commit before any edit.
- **Sync** `28022fe`, from fork `main` `ff02b5c` (Route B, on the operator's direction):
  - **Before:** fork `main`'s `bin/status` read 12 tracked files behind, `quality_ratchet.py` missing and `CHANGELOG.md`
    *present (stale format)*.
  - **Dry run:** exit 0, no refusals.
  - **Real run:** 12 tracked files updated, `quality_ratchet.py` created, and `.quality-gates.json` seeded with
    `"gates": []`. The 5 existing seeds were left as they are.
  - **After:** every tracked file reads `current`.
  - The plan's Route A reason (BL-54 refusing four files) is out of date, because BL-54 was fixed fork-side in `865119f`.
  - One commit of 15 files, over the 5-file cap, because a single tool run wrote them all.
- **Migration** `5e4b483`: lines 1–11 replaced with fork `main`'s `starter-kit/CHANGELOG.md` header, with three decisions:
  - **Sentinel:** dropped the 4-line seed-sentinel comment and the blank line after it. The ledger already has entries,
    and both BL-56 and the seed say to delete it.
  - **Trailing comment:** kept `<!-- Entries go below … -->` verbatim, as Session 5 did in `HANDOFFS.md`.
  - **`## [Unreleased]`:** dropped. The rules group by month, not by release, and a ledger without month headings starts
    them at its next new month (`docs/methodology/FRAMEWORK_APPARATUS.md` §The Action Ledger, *Placement*).
  - A Python script asserted every anchor before cutting (plan hazard 5).
- **`CLAUDE.md`** `9f150a5`: a new Adaptations subsection, *Ledger (`CHANGELOG.md`) conventions* (`CLAUDE.md:28-33`). It
  covers source tags and the legacy layout. The protocol block is unchanged: it already matches `CLAUDE_TEMPLATE.md:12-14`,
  which has no ledger wording.
- **Close-out:** this note, the S6 receipt and the close-out entry. The Session 1–3 history was removed from this file
  (FM #28); it survives in `git show 1402ad4:SESSION_NOTES.md`.

**Verification — the plan's DONE list, counts re-derived per commit:**
- **`bin/status` reads `present`:** yes from fork `main` (`ff02b5c`), and yes from upstream `main` (`6b29d3d`, run from a
  scratch `--no-local` clone). That meets BL-56's "both versions" criterion.
- **Only the block changed:** the plan's §9.8 script on `5e4b483` prints "only the block changed". The other three session
  commits removed 0 `CHANGELOG.md` lines. The pre-session entries at `1402ad4` are the byte-identical tail of HEAD.
- **Heading count:** the block held 0 `### ` lines and the migration added 1 entry, so the prediction was +1. Measured
  4 → 5 across `5e4b483`, which confirms the plan's "0 elsewhere". Across the session: 2 (`1402ad4`) → 6 (`9f150a5`),
  and 7 after close-out.
- **Audit count:** the block held 0 matches, so the prediction was +1. Measured 4 → 5, and zsh equals bash; 0 shards.
  Across the session: 2 → 6, and 7 after close-out.
- **Build:** all 7 `.py` files parse; `app` imports (9 routes). No test suite exists.
- **Runtime (3E):** no app code changed and the Flask app wasn't launched. Each synced tool was run: dashboard v2.18.0
  (health 54/100), `quality_ratchet.py --run` (0/0 gates), `methodology_trim.py --check` (trigger does not fire), and
  `context_budget.py` (3 findings that predate this session; see gotchas).

**Findings for the methodology repo** (not edited from here, per the session-notes boundary):
- **Plan P6 row (`:760`):** two statements are out of date. The Route A reason no longer holds (BL-54 is fixed), and
  "carry its one entry across" is wrong: there were two entries, and now there are seven.
- **Status:** P6 and BL-56 are done and need marking so in the methodology repo's plan and backlog.
- **Seed comment:** the seed's trailing comment ("Delete the seed-sentinel line near the top …") stays behind after the
  sentinel goes, in every migrated adopter.
- **Missing `.gitignore` entry:** the `.quality-gates.json` seed says to gitignore `.quality-gates-results.json`, but
  `bin/sync` adds no such entry.
- **Disclosure:** Session 6 ran `git fetch upstream` in `~/Development/methodology`, which updates remote-tracking refs only.

**Key files:**
- `CHANGELOG.md:1-16` — the new header; `:12` holds the `ledger-format: 2` marker; entries start at `:18`
- `CLAUDE.md:28-33` — the ledger conventions (source tags, legacy layout)
- `.quality-gates.json` — the gates seed, with no gates declared
- `templates/dashboard.html:55` — open item 1

**Gotchas for the next session:**
- **One ledger entry per commit.** The claim commit carries an *(in progress)* entry, and close-out adds its own.
  `[BL-<id>]` means this repo's `BACKLOG.md` only (`CLAUDE.md:32`).
- **Month headings.** The first entry dated 2026-10 opens `## 2026-10` at the top of the entries. Don't add `## 2026-09`.
- **Verification runs write untracked files:** `.quality-gates-results.json`, `.context-budget-history.jsonl` and
  `dashboard_history.jsonl`. Session 6 deleted the first two after creating them. Stage files by name, never `git add -A`.
- **`context_budget.py` reports 3 red findings, all older than this session.** Each one reproduces on `1402ad4`'s tree
  with the new tool:
  - `CLAUDE.md`'s `budget:protected` fence is missing (open item 4).
  - `SESSION_NOTES.md` lines over 280 B: 11 at `1402ad4`, 3 after this close-out's rewrite.
  - The `SESSION_NOTES.md` pattern `^## ` matches 1 heading against a declared minimum of 2.

  Fix the file or `.context-budget.json` in plan mode, and never loosen a ceiling just to go green.
- **The branch stack is local-only** (open item 3). `chore/methodology-bl57-p6` is based on `1402ad4`, so discarding
  `chore/methodology-read-set-budgets` loses nothing.
- **Seeds are never re-synced.** `HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md` and `.context-budget.json` keep older text.
  For example, the synced runner cites `HANDOFFS.md` §Citing the gate run, which this repo's `HANDOFFS.md` lacks. That
  doesn't matter while no gates are declared.
- **A stale dashboard copy remains.** `docs/methodology/tools/methodology_dashboard.py` is v2.6.1 and isn't in the sync
  manifest; the root copy is now v2.18.0.

**Learnings (3C):** no new `CLAUDE.md` learning row this session. The durable rules went into the new ledger-conventions
subsection. The side-effect-files trap is a gotcha, and a gitignore gate candidate (open item 2), rather than a row. The
FM #28 reduction was done: the Session 1–3 history was removed.

**Self-assessment:**
- **Score: 8/10**
- (+) The Phase 1B claim was committed on its own before technical work (a Session 5 minus), with the block range in it.
- (+) Every claim in each ledger entry was verified on the working tree before the commit that ships it, since entries
  are never edited.
- (+) The DONE counts were re-derived per commit, not just read off the end state. BL-56's "both versions" criterion was
  checked by running upstream's `bin/status`, not inferred from the marker text.
- (+) The 3 budget findings were shown to be older than this session (reproduced on `1402ad4`), not assumed so, and were
  left unfixed as out of scope.
- (−) The 15-file sync commit breaks the 5-file cap. One tool run justifies it, but I didn't raise it with the operator
  before committing.
- (−) `git fetch upstream` changed the methodology repo's refs. It was harmless and is disclosed, but the scratch clone
  used later would have done it without touching that repo.
- (−) The verification runs left two untracked files that needed cleanup; the tools' side effects weren't anticipated.
- (−) Long stretches without a progress update; the harness prompted twice.

### Session 4 Handoff Evaluation (by Session 5)
- **Score: 9/10**
- **What helped:** The one concrete recommendation was exact. Session 4 put the stale "Arduino Mega port" banner at
  `templates/dashboard.html:54-55`; Session 5 re-grepped and found it unchanged (line 54 is the `2. USB Serial` heading,
  line 55 the text). Item A named a precise trigger (PR #25 + #27 merging into `KJ5HST/main`), and the June methodology
  sessions executed PART 2 when it fired. The "`docs/HARDWARE.html` is untracked — leave it" gotcha kept me off that file.
- **What was missing:** Nothing Session 4 could have supplied. The work Session 5 had to do — classifying four later commits
  with no airqino notes — came from methodology-repo sessions, which by the session-notes boundary rule write notes elsewhere.
- **What was wrong:** Nothing was inaccurate on 2026-06-08. Two phrases were built to go stale: Item B's
  "commit pending close-out" and "(close-out commit … follows this note)". Both were true when written and never updated;
  "the close-out commit" instead of "pending" would have aged better. Item A's "NOT actionable" went stale four days later,
  when its trigger fired — not a defect, but nothing owned refreshing it.
- **ROI:** Positive. A few minutes of reading gave the recommended next deliverable and the context to classify everything since.

### What Session 5 Did
**Deliverable:** None — **no deliverable produced.** Orientation-only session: Phase 0 report delivered, then the operator
directed close-out without assigning a task.
**Started:** 2026-09-14 · **Closed:** 2026-09-15
**Ledger:** `CHANGELOG.md` "2026-09-15 · [ad hoc] Session 5 — orientation-only session closed out; no deliverable"

**What was done:**
- **Phase 0 in full:** read `SESSION_RUNNER.md` and `SAFEGUARDS.md` completely, then this file; `gh issue list` (0 issues;
  1 open PR); git status/log/diff; `methodology_dashboard.py`; the CHANGELOG + HANDOFFS reconcile.
- **Stale session-start snapshot caught:** the harness snapshot showed `chore/methodology-pr2527-remediation` @ `0c59e5e`.
  `git reflog` showed a methodology-repo session (S161) checked out `chore/methodology-read-set-budgets` at 2026-09-14
  12:25:06 and committed `dfe26fd` at 12:26:27.
- **Ghost-session check — none.** The four commits after Session 4 are methodology-repo work. Verified by hash
  (`git -C ~/Development/methodology log --all -S<sha>`): `66abe78` is named in methodology `291f54e` (07-25, S15 close-out);
  `28db357` and `0c59e5e` in `f2c49d2` (06-22, "mark BL-3 (airqino re-vendor) task 1 done → v2.9"); `dfe26fd` in `6eaa15f`
  and `bb6eb72` (09-14, S161).
- **Ledger reconcile — no-op; no backfill written.** CHANGELOG frontier = `dfe26fd` = HEAD (empty gap). HANDOFFS was seeded
  at `dfe26fd` with no receipts and nothing `pending`. `7cafdbc..0c59e5e` is pre-ledger history: the runner vendored at
  `66abe78` and `0c59e5e` has 0 hits for FM #27, ledger reconcile, or HANDOFFS, so those commits are not FM #27 misses.
- **Verified Session 4's recommended next deliverable still applies** (`templates/dashboard.html:55`).
- **Close-out:** rewrote the stale ACTIVE TASK (superseded Item A/B text removed), added `CLAUDE.md` learning #4, wrote
  the first `HANDOFFS.md` receipt (seed sentinel removed), added the CHANGELOG entry.

**Verification / state at close:**
- Build equivalent: all 6 `.py` files pass `ast.parse`; flask, requests, python-dotenv and pyserial import (Flask 3.1.3).
  No test suite exists.
- Dashboard: health 54/100 (56 on 2026-06-12), risk HIGH — no tests (HIGH), no CI (MEDIUM), a 2,055-line file (MEDIUM),
  no LICENSE (LOW). Methodology compliance 100%.
- Runtime smoke (3E): n/a — docs-only close-out; no runtime behavior changed.

**Commits:** the close-out commit only — it ships this note (see the `HANDOFFS.md` S5 receipt).

**Key files:**
- `templates/dashboard.html:55` — the stale banner text (open item 1)
- `docs/HARDWARE.md:33` — the authoritative "REV6 has no USB port" statement to align the banner with
- `CLAUDE.md:39` — new learning #4 (stale snapshot / out-of-band commits)
- `HANDOFFS.md` — first receipt (S5)

**Gotchas for the next session:**
- **Don't trust the harness's session-start git snapshot** — it was stale in both Session 4 and Session 5. Run `git status`
  and `git reflog -5` yourself (`CLAUDE.md` learning #4).
- **A methodology-repo session was busy throughout Session 5** and had switched this repo's branch. Before touching git
  state, check `git reflog -5` for anything that moved again.
- **Branch:** HEAD is `chore/methodology-read-set-budgets` — local-only, not pushed — holding `dfe26fd` plus the Session 5
  close-out commit, on top of PR #1's head `0c59e5e`. If that branch is re-synced or discarded (e.g. after upstream PR #80
  merges), carry the close-out commit over with `git cherry-pick`, or the ACTIVE TASK refresh and the first receipt are lost.
- **CHANGELOG now has two entries, not one.** Methodology plan P6 (`docs/planning/changelog-rules-contradictions-plan.md:584`
  in `~/Development/methodology`) says to reseed this file and "carry its one entry across, unchanged". Whoever runs P6 must
  carry both. Until then, add new entries in the existing format; don't reformat the file in a project session.
- **Stale dashboard copies:** root `methodology_dashboard.py` is v2.10.7, canonical (`~/Development/methodology/starter-kit/`)
  is v2.17.0, and `docs/methodology/tools/methodology_dashboard.py` is v2.6.1 (the dashboard's "large file" flag).
  Syncing is portfolio-level work; don't hand-copy in a project session unless the operator asks.
- **Untracked, left alone:** `docs/HARDWARE.html` (open item 2) and `dashboard_history.jsonl` (appended by every dashboard
  run; `dashboard.html` is gitignored but the history file is not).
- **Mandated-read size (FM #28):** this file is 320 lines / ~30 KB after Session 5 (a net +90 lines from 230), against
  `.context-budget.json` ceilings of 400 lines / 120,000 B. Estimate: a next session that grows it as much lands at ~410, over
  the line ceiling — archive the Session 1–3 history at or before that close-out. 11 older lines break the 280 B per-line cap; none new.

**Self-assessment:**
- **Score: 8/10**
- (+) Phase 0 complete, including the reconcile; `SESSION_RUNNER.md` and `SAFEGUARDS.md` read in full, not skimmed.
- (+) Didn't trust the session-start snapshot; the reflog established what changed, when, and by which session.
- (+) Went past the mechanical reconcile: the frontier was HEAD, so the check "passed", but a one-entry ledger prompted a
  check on whether older commits were owed. The answer (pre-ledger, not FM #27 misses) came from the runner vendored at those
  commits, not from assumption. I offered the optional pointer line rather than writing it; at close-out I found the
  methodology repo already owns that change (BL-56 → P6).
- (+) Left git state alone while a methodology session was busy; removed superseded ACTIVE TASK text (FM #28).
- (-) **No deliverable produced** — the operator closed the session at the Phase 0 STOP.
- (-) The Phase 0 report mapped `66abe78` to methodology `58f51c1` from commit subjects alone; the hash check at close-out
  put it in `291f54e`. The conclusion (not a ghost) held, but the citation was wrong. Now captured in learning #4.
- (-) Phase 1B: the claim stub was written to the working tree at the start of close-out but not committed on its own; it
  shipped in the single close-out commit.
- (-) Phase 0 took four rounds of tool calls; the ledger-history and methodology-log checks could have run in round one.

### What Session 4 Did
**Deliverable:** Root `README.md` (Item B) — **COMPLETE**
**Started / Closed:** 2026-06-08

**What was done:**
- **Bookkeeping first (per user):** (1) committed the out-of-session correction to `docs/planning/methodology-pr2527-remediation-airqino.md` on its own as `a5fdd12` (PART 2 reclassified to DEFER — the `integration/pr2527` branch never existed); (2) verified the claim before committing — Phase 0 `git status` showed a clean tree, so I re-ran `git status` and confirmed the file was genuinely modified out-of-session. (3) Reclassified Item A (PART 2 re-vendor) in this file from **BLOCKED → DEFERRED** so it stops surfacing as actionable.
- **Deliverable:** Wrote `README.md` from a direct read of `app.py`, `airqino_client.py`, `serial_reader.py`, `.env.example`, `requirements.txt`, `static/js/dashboard.js`, `templates/dashboard.html`, and `docs/HARDWARE.md` — not from the handoff description. Covers: project background (abandoned PN 800506 / S/N AIRO 6153 device), quick start, all three data sources (CSV/SD, cloud API, serial), feature list, full API endpoint + Flask route tables, hardware summary, key-file map, and a config-variable reference.
- **Left `docs/HARDWARE.html` untouched** (per user — separate decision).

**Verification:**
- `app.py` confirms port **5001**, host `0.0.0.0`, env var names, and route list → README matches.
- API base/token URLs, endpoint paths, and the 30-day/CSV/401-empty quirks taken verbatim from `airqino_client.py`.
- Sensor units and chart ranges (6h/12h/24h/3d/7d/30d) taken from `static/js/dashboard.js` and `templates/dashboard.html`.

**Commits:**
- `a5fdd12` — docs: correct airqino PART 2 — defer re-vendor until PR #25/#27 merge (no integration branch)
- (close-out commit for README + SESSION_NOTES + CLAUDE.md follows this note)

**Key files:**
- `README.md` — NEW, the deliverable
- `CLAUDE.md:34` — added project learning #3 (factual corrections must be grepped across ALL surfaces)
- `docs/planning/methodology-pr2527-remediation-airqino.md` — corrected (committed `a5fdd12`)

**Gotchas for the next session:**
- **Stale UI copy (NOT fixed — deliberate scope hold):** `templates/dashboard.html:54-55` still tells the user to "connect a USB cable to the Arduino Mega port" — the pre-Session-2 hardware claim that Session 2 corrected everywhere else (`serial_reader.py`, `.env.example`, `docs/HARDWARE.md`). This is the setup-banner "USB Serial" option. A good, bounded next deliverable: fix that banner text to match the USB-to-TTL/REV6 reality. (Logged as CLAUDE.md project learning #3.)
- **PART 2 is DEFERRED, not actionable:** do not pick up Item A until PR #25/#27 merge into `KJ5HST/main`. See Item A for the trigger and the one-pass re-vendor procedure.
- `docs/HARDWARE.html` is still untracked and still undecided (track / ignore / delete?) — Session 4 left it alone per instruction, same as Session 3.
- Branch `chore/methodology-pr2527-remediation` is not merged to `main` or pushed. No push was requested.

**Self-assessment:**
- **Score: 9/10**
- (+) Verified the out-of-session edit before committing instead of trusting the description — caught that my own Phase 0 snapshot was stale and confirmed against a fresh `git status`.
- (+) Wrote the README from the actual code, so endpoint names, env vars, port, sensor units, and chart ranges are accurate rather than paraphrased from the handoff.
- (+) Held the line on scope: spotted the stale `dashboard.html` Arduino text but did NOT fix it (FM #8) — flagged it as a clean next-session deliverable and logged the root-cause learning instead.
- (+) Did the bookkeeping in the exact order requested, committed the correction as its own logical unit, and left `HARDWARE.html` untouched.
- (-) Did not boot the Flask app to confirm it serves (it's a blocking debug server); relied on reading `app.py`. The install/run steps are standard, but a runtime smoke test would have been stronger evidence.

**Previous session handoff evaluation:** See "Session 3 Handoff Evaluation (by Session 4)" above.

### Sessions 1–3 (archived by Session 6)
Removed to keep this mandated read under its ceiling (FM #28). Full text, including their handoff evaluations: `git show 1402ad4:SESSION_NOTES.md`.
