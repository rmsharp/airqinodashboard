# airqino — Methodology PR #25 + PR #27 Remediation (execution brief)

*Generated 2026-06-07 from the methodology-repo master plan (`~/Development/methodology/docs/planning/adopter-pr25-27-remediation-plan.md`, §5). Anchors/counts **independently re-measured and CONFIRMED** by an adversarial recon on 2026-06-07.*

> airqino is the **re-vendor case** (decision O2), not a patch case. Its vendored methodology is a partial **v2.1** copy. The brief has two parts: **PART 1 (NOW)** preserves airqino's 2 hand-authored learnings and adds the receptacle — do this immediately and it is complete on its own; **PART 2 (RE-VENDOR)** lifts the whole methodology tree v2.1 → current. PART 1 must precede PART 2 or the 2 learnings are lost when `SESSION_RUNNER.md` is overwritten.
>
> **⚠ 2026-06-08 correction:** PART 2 as originally written pointed at a local `integration/pr2527` branch — **that branch does not exist and was never built.** PART 2 is **recommended DEFERRED** until PR #25/#27 merge upstream (see the corrected decision point below). PART 1 already secured the only at-risk data, so deferring PART 2 costs nothing. If you only have one session, **PART 1 is the deliverable and PART 2 waits.**

## Verified current state (2026-06-07 — CONFIRMED)

| Item | Finding |
|---|---|
| Learnings table | `SESSION_RUNNER.md` rows `:268–270` = **3 rows**. **Row 1 is the canonical seed** (FM #19 plan-mode, byte-identical to starter-kit). **Rows 2–3 are airqino's** (REV6 hardware; adapter availability) — *these* are what must be preserved. |
| 3C body | `SESSION_RUNNER.md:159` — `Update the workstream document and/or the Learnings table below:` (heading `:157`) |
| caption | `SESSION_RUNNER.md:264` — `*This table starts empty...*` |
| `CLAUDE.md` | **12 lines, no receptacle** (just the session-protocol pointer) |
| C3 target | `docs/methodology/HOW_TO_USE.md:740` |
| Vendored tree | `docs/methodology/` = HOW_TO_USE.md, ITERATIVE_METHODOLOGY.md, README.md, 5 workstreams (ARCHITECTURE/AUDIT/DESIGN/DEVELOPMENT/TEMPLATE). **No starter-kit, no bin/, no BOOTSTRAP, no CLAUDE_TEMPLATE, no campaigns, no RECOMMENDED_SKILLS/CONTEXT_TEMPLATE, no Research-Documentation workstream.** Version = **v2.1**. |
| Local edits | **None** — vendored `docs/methodology/` files are pristine (zero airqino-specific terms). The only airqino content in the methodology surface is `SESSION_RUNNER.md` Learnings rows 2–3 and `SESSION_NOTES.md`. → a re-vendor is **safe** once rows 2–3 are preserved. |

---

## PART 1 — NOW (safe, do immediately; preserves the 2 learnings)

### Step 0 — Branch + claim
Branch off the default branch (`chore/methodology-pr2527-remediation`), write a Phase 1B claim stub.

### Step 1 — Add the `CLAUDE.md` receptacle with the 2 learnings INLINE
airqino's corpus is tiny (2 rows) → inline table, **not** a separate `PROJECT_LEARNINGS.md`. Append to `CLAUDE.md`:

```markdown
---

## Project-Specific Methodology Adaptations

*Additions and overrides to the base methodology at `SESSION_RUNNER.md` and `SAFEGUARDS.md` (synced from canonical, not project-owned). The base files govern unless explicitly overridden here. **Do not edit the synced files** — put customizations here.*

### Additional Phase 0 steps

(none)

### Additional task-to-workstream mappings

(none)

### Project-specific Learnings

| # | Learning | Source | When to Apply |
|---|----------|--------|---------------|
| 1 | Hardware assumptions from research papers may not match the actual device revision. Session 1 described "Arduino Mega + SIM900 GPRS" based on published literature; the actual REV6 board (2022) is a custom PCB with no USB port. Physical verification trumps literature-based assumptions for hardware projects. | Session 2 hardware investigation | When documentation references specific hardware components, verify against the physical device before writing connection instructions or buying parts. |
| 2 | Verify product availability before recommending a purchase. First adapter recommendation was out of stock, requiring a second round of research and a doc update. Check stock status as part of the recommendation, not after. | Session 2 adapter research | When recommending specific products for purchase. |

### Project-specific Failure Modes

(none — the base failure modes in `SESSION_RUNNER.md` apply.)
```

> These are `SESSION_RUNNER.md` rows 2–3 copied **verbatim**, renumbered 1–2. Row 1 (the canonical seed) stays in `SESSION_RUNNER.md`.

### Step 2 — Remove rows 2–3 from `SESSION_RUNNER.md`
Delete lines `:269–270` (airqino rows 2–3), leaving row 1 (the seed). This de-duplicates now and is harmless to the re-vendor (which overwrites the file anyway). *Do NOT bother with targeted C1/C2/C3 edits here — PART 2 supersedes them.*

**PART 1 is independently committable and complete on its own** if you want to stop here and defer the re-vendor.

---

## PART 2 — RE-VENDOR (the lift): v2.1 → current

> **Decision point (yours) — recommended: DEFER (option b).** PART 1 already secured the only at-risk data (the 2 learnings), so there is no urgency. A *full-tree* re-vendor is cleanest done ONCE from a stable, merged canonical — sourcing it from unmerged PR wording means re-touching the whole tree if upstream review changes #25/#27. Unlike the targeted-patch projects (where O4 said "apply the 3-line wording now"), airqino's full re-vendor is genuinely better deferred.
> - **(b) DEFER until merge — RECOMMENDED.** PR #25 + #27 are OPEN on `KJ5HST/methodology` as of 2026-06-08 (filed from `rmsharp:fix/3c-learnings-destination` and `rmsharp:fix/claude-md-learnings-overflow`; **not** local PRs on the fork). When they merge into `KJ5HST/main`: sync `origin/main` from upstream, then re-vendor airqino from `origin/main` in one pass — the new 3C/caption/HOW_TO_USE wording arrives for free, no patching.
> - **(a) Re-vendor now — only if airqino must be current immediately.** **There is NO `integration/pr2527` branch — do not wait on one.** Re-vendor from current `origin/main` (already far ahead of v2.1), then apply the three small wording edits **C1/C2/C3 by hand** (the unmerged PR-25/27 delta — see the wsfct/mpc/mts briefs for the exact verbatim text). Accept that you may re-touch those three when #25/#27 finalize. This is the only "now" path; it does not need a methodology-side branch build.

### Re-vendor procedure
1. **Confirm PART 1 is committed** (the 2 learnings are safe in `CLAUDE.md`).
2. **Inventory what you have vs. what's coming.** Current vendored tree is the 8 files listed above. A full re-vendor brings the *entire* current framework — at minimum: `starter-kit/` (SESSION_RUNNER.md, SAFEGUARDS.md, BOOTSTRAP.md, CLAUDE_TEMPLATE.md, CONTEXT_TEMPLATE.md, RECOMMENDED_SKILLS.md, CHANGELOG/ROADMAP templates, methodology_dashboard.py), `bin/sync`+`bin/status`, the Research-Documentation workstream, the two campaign templates, and updated HOW_TO_USE/ITERATIVE_METHODOLOGY/README.
3. **Replace** airqino's `docs/methodology/` tree **and** the root operational files (`SESSION_RUNNER.md`, `SAFEGUARDS.md`, `methodology_dashboard.py`) with the integration-tree versions. Because there are **no local edits** in `docs/methodology/` (recon-confirmed), this is a clean overwrite — the only project content to protect is the 2 learnings (already in `CLAUDE.md` from PART 1) and `SESSION_NOTES.md` (project state — do NOT overwrite it).
4. **Wording:** if you took the recommended **DEFER** path, the new 3C body (C1), caption (C2), and `HOW_TO_USE.md` 3C bullet (C3) arrive as part of merged canonical — no patching. If you took the **now** path (re-vendor from pre-merge `origin/main`), apply C1/C2/C3 by hand after the re-vendor.
5. **Re-validate** root `CLAUDE.md` against the newly-arrived `starter-kit/CLAUDE_TEMPLATE.md` shape (your receptacle from PART 1 should already match it). Consider wiring up `bin/sync` so future updates are friction-free (airqino would become the 2nd adopter with sync, after wsfct).
6. **Spot-check** the dashboard still runs and `SESSION_RUNNER.md` matches the source `origin/main` `starter-kit/SESSION_RUNNER.md` (with canonical's 6 seed rows; +C1/C2 already present if deferred-until-merge, or applied by hand if you took the "now" path).

---

## Verification

**PART 1:**
- `CLAUDE.md` has the Adaptations receptacle with the 2 airqino learnings inline (verbatim); `grep -n '@' CLAUDE.md` shows no `@`-import of a learnings file.
- `SESSION_RUNNER.md` Learnings table now has only the canonical seed row(s); the 2 airqino rows are gone from it but present in `CLAUDE.md`.

**PART 2 (if done):**
- `docs/methodology/` now contains the current framework (starter-kit/, bin/, campaigns, Research-Documentation workstream, etc.); version is current (not v2.1).
- `SESSION_RUNNER.md` carries the new 3C (C1) + caption (C2); `HOW_TO_USE.md` carries C3.
- `SESSION_NOTES.md` untouched; the 2 learnings still in `CLAUDE.md`.

## Close out
Commit PART 1 (and PART 2 if done) as logical changes. Write handoff notes, score the previous session, STOP.

---

### Provenance
- Master plan §5 (airqino, O2 = full re-vendor). Recon `wf_f6bef839-306` (2026-06-07): 3 table rows confirmed (1 seed + 2 airqino), tree inventory + zero-local-edits CONFIRMED. The "2 rows" of the plan = airqino-authored (rows 2–3); total table rows = 3.
