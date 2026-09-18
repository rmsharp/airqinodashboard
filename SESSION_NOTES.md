# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`), and D1, the plan's first fix session,
is done. Next: D7 (plan §6's second, recommended next), or any other open item.
**Status:**
- **Phase 4: COMPLETE, on `main`.** Unchanged since Session 13: `0e5ed0d`, `5084680`.
- **D1: FIXED, Session 14, on `main` (`a14ff03`).** `serial_reader.py` `_parse_line` now splits a `key=value`
  line on `;` and `,` in one pass. Its xfail marker is removed; `tests/test_serial_reader.py` gained two rows.
  `main` was fast-forwarded to the Session 14 branch, which was then deleted. `main` is the only branch, and it
  is pushed straight after the close-out commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `119 passed, 7 xfailed` in about 0.35 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 71b7ac5ea8f1 · manifest 973c1b7d973d`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 119).
- **Dashboard:** 68/100, unchanged, with High+ risk 0. The flags are unchanged too: two MEDIUMs ("No CI/CD pipeline",
  and a large file, the synced `docs/methodology/tools/methodology_dashboard.py`) and one LOW ("No LICENSE file").
- **Defects (plan §4):** D1 fixed. D2, D3, D4, D5, D6, D7 still have strict xfails, 7 tests in all (D2 has two).
- **BACKLOG.md has its first item, BL-1** (added mid-Session-14 at the operator's request): make the repository
  fully MIT-licensed. It records that the vendored `docs/methodology/LICENSE` is not MIT and needs a carve-out,
  and two decisions that are the operator's. Not started.
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 13's is at `git show b5a336c:SESSION_NOTES.md`, Session 12's at `git show ace379d:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D7 (recommended next): the plan's fix sessions (§6), one defect per session.** D1 is done (Session 14).
   The plan's remaining order is D7, then D3 and D4, then D6, D5 and D2. Each session, on a new branch off `main`:
   - removes the defect's `xfail` marker and watches its test fail on the unfixed code;
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by 1 (by 2 for D2, which has two tests);
   - runs learning #5's runtime check for D3, D4 and D7, which are user-visible (D1's is done);
   - red-drives the fix against the whole suite (learning #11), with the original marker restored first, so a
     fix that doesn't need it doesn't silently pin it (Session 14's check).

   Where each one is:
   - **D7:** `serial_reader.py:64-69` and `app.py:141-147`; its xfail is `tests/test_serial_routes.py:54` (marker
     `:51`). A 2-line 503 for a reader error fixed it in a probe. Open item 4's third finding bears on its design.
   - **D2:** `app.py:171` and `:220`; its xfails are `tests/test_csv_routes.py:160` and `tests/test_api_routes.py:213`.
   - **D3, D4:** `tests/test_csv_routes.py:167`, `:174`.
   - **D5:** `app.py:53`; its xfail is `tests/test_api_routes.py:194`. **A real D5 fix also fails Phase 1's T1.5**
     (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`. That session must set all four
     credentials in T1.5 as well.
   - **D6:** `app.py:53-58`; its xfail is `tests/test_api_routes.py:205`.

   The probe fixes were probes, not designs, so each fix session keeps its freedom. **D1's own probe fix
   ("split on `;` or `,`, never both") was rejected in Session 14**: it regresses on a comma line with a
   trailing `;` (`"co=1.5,pm25=7;"` → `{"co": "1.5,pm25=7"}`). The other suggested fixes above haven't been
   probed against a similarly adversarial case; treat them as starting points, not verified designs.
2. **Decide the untracked files.** For each one, commit, gitignore or delete; that's the operator's call.
   - `docs/HARDWARE.html` has been untracked since Session 3. It is an HTML render of `docs/HARDWARE.md` and holds no
     stale hardware copy.
   - Three tool outputs, all present now, have no `.gitignore` entry: `dashboard_history.jsonl` (written by every
     dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`, which the `.quality-gates.json`
     seed says to gitignore); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence
   missing: `.context-budget.json` declares it for `CLAUDE.md`, with a minimum of 800 B. `CLAUDE.md` has never had a
   fence or a Purpose section, and `README.md`'s opening is the source text. The same tool also reports
   `SESSION_NOTES.md` as "instrument-failed", for two reasons now, both in the tool, not this file:
   - `.context-budget.json` expects at least 2 `^## ` headings, but this file has 1, and so does the synced seed
     `docs/methodology/starter-kit/SESSION_NOTES.md`. A mismatch inside the methodology's own files.
   - (new, Session 14) its 400-line ceiling fires one line early: `measure_file` (`context_budget.py:346`) counts
     `text.split("\n")`, which is 1 more than the file's real line count for any file ending in a newline (the
     normal case; `wc -l` and `splitlines()` agree on 400 for this file at close-out). Reproducible on any
     trailing-newline file, not particular to this one.

   Both are mismatches inside the methodology's own tooling. Raise them upstream rather than restructuring this
   file to satisfy either one.
4. **Decide three findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:87` checks
     `_csv_data is not None`, but `active_source()` (`:57`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode **and in serial mode** (the serial half is new in Session 12). CSV returns the
     last 500 rows (`app.py:203-208`), and serial returns `get_history(limit=500)` (`:177`), whatever the range. So
     the chart's 6h–30d buttons (`templates/dashboard.html:86-91`) change nothing outside API mode.
   - In D7's state, `/api/timeseries` answers 200 with `data: []` (Session 12 probe). A D7 fix that only changes
     `/api/current` leaves the chart silent about the port error.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. This session's 21 red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:160`), which is 30
   days apart. `README.md:108` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown.
8. **The map's tile provider now demands an API key (new in Session 14, no test pins it).** `static/js/dashboard.js:336`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with an image reading "API KEY REQUIRED" over the map, not a 4xx — so nothing in the app's own code
   or tests would catch this. It showed in both the before- and after-fix screenshots this session. CARTO's basemap
   tiles moved behind a key at some point after this URL was written; whether a free key is available and how to
   wire it in (`static/js/dashboard.js` attribution object, or a self-hosted/alternate tile source) is a design
   question for its own session, not a defect with a minimal fix. BL-1 (MIT licensing) also touches this file, since
   any tile provider swap changes what's being redistributed and under what license.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 15 Did
**Deliverable:** Fix D7 (open item 1; plan §6's second fix session): a serial port that fails to open is served
as data with 200 (`serial_reader.py:64-69`, `app.py:141-147`) (IN PROGRESS)
**Started:** 2026-09-17 23:47
**Status:** Session claimed on branch `fix/d7-port-open-failure` (off `main` `b710ac0`). The operator picked D7 in the
Phase 0 picker. Work beginning.
**Ledger:** `CHANGELOG: pending` — the claim commit's `CHANGELOG.md` entry says (in progress); Phase 3F records the rest. Until close-out, this line is the crash breadcrumb for the next session's reconcile.

### What Session 14 Did
**Deliverable:** Fix D1 (open item 1; plan §6's first fix session): a `;`-joined serial line is split on `,` too,
which overwrites its first key (`serial_reader.py:106-117`) — **COMPLETE**
**Started / Closed:** 2026-09-17 23:28 / 23:39. Claimed on branch `fix/d1-serial-delimiter` off `main` `b5a336c`.
Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §6 (fix sessions), the approved contract from Session 9's plan.
**Ledger:** 4 `CHANGELOG.md` entries: the claim, the BL-1 backlog addition, the fix, and this close-out, which
also records the fast-forward and the push. Also 1 note (mid-session model switch, below).

**A note on the acting model:** the harness switched from Claude Opus 5 (1M context) to Claude Sonnet 5 partway
through this session, after the fix was already committed. Everything through `a14ff03` (claim, BL-1, the fix)
is Opus 5's; the close-out onward — this write-up, the plan-doc note, the ledger, the landing — is Sonnet 5's.
Commit trailers reflect this split; they were not rewritten.

**What was done:**
- **Claim** `0db8f73`. The operator picked D1 in the Phase 0 picker.
- **Mid-session, out of band:** the operator asked to add a backlog item for full MIT compliance. `BACKLOG.md`
  gained its first item, BL-1 (`d8e9bc5`), recording the current state (no root `LICENSE`, GitHub license `null`),
  the catch (`docs/methodology/LICENSE` is a non-MIT attribution/no-redistribution license and needs a carve-out),
  and two decisions left to the operator. This was committed on its own, separate from the D1 diff.
- **Probed three parser designs before writing the fix** (learning #7), in the scratchpad, against 10 hand-picked
  lines including the docstring's own example, mixed separators, a trailing separator and a decimal comma:
  - the original two-pass code (confirmed the defect);
  - Session 12's suggested probe fix, one separator per line (`;` if present, else `,`) — **rejected**: it turns
    `"co=1.5,pm25=7;"` into `{"co": "1.5,pm25=7"}`, a new regression on a case the old code got right;
  - a single pass over both separators (`re.split(r"[;,]", line)`) — correct on every probed case, and no worse
    than the old code on the one it still can't handle (a decimal comma inside a value).
- **Fix** `a14ff03`: `serial_reader.py` `_parse_line` uses the single-pass split. D1's xfail marker removed;
  `tests/test_serial_reader.py` T3.1 gains two rows (the docstring's full example, and the trailing-`;` case that
  broke the rejected design). `.quality-gates.json` `tests-passed` tightened from 116 to 119 (not 117: one row
  is the repro, the second was added once the rejected design's regression was known). No other product code
  changed.
- **Red-drives**, in the working tree, each restored with `git checkout`, with the shasum the same before and
  after (`serial_reader.py`, `tests/test_serial_reader.py`):
  - the fix with D1's original marker restored, run against the whole suite: only D1 flips, `XPASS(strict)` —
    no other test pins D1 (learning #11, checked from the start this time, not after the fact);
  - the rejected one-separator design: fails only the new trailing-`;` row;
  - `;`-only splitting: fails the comma row, the trailing-`;` row and the pty test (T3.6);
  - the original two-pass code: fails the 3 target rows.
  - The gate: with one test (`trailing-separator`) hidden, `tests-passed` measured 118 and the ratchet exited 2.
- **Runtime (learning #5, D1 is user-visible):** a real `python3 app.py` process, a real `os.openpty()` pty fed
  `"co=235;no2=17;o3=17;pm10=25;pm25=13"` (the docstring's example) once a second, `/api/current` and
  `/api/timeseries?sensor=co` queried by `curl`, and a headless-Chrome screenshot of `/`, both before and after
  the fix. Before: `co` arrived as the string `"235;no2=17;o3=17;pm10=25;pm25=13"` and the readings grid had no
  CO card. After: `co` is `235.0`, the timeseries rows are numeric, and the CO card shows 235 mg/m³. The app and
  Chrome were stopped and port 5001 confirmed free (`lsof`, exit 1) each time.
- **Plan updated:** `docs/planning/test-suite-plan.md` — the Status line and D1's §4 row note the fix and its
  commit; an "As implemented (D1, Session 14)" note under §6 records the rejected design and the two-row count.
- **Landing:** the operator picked "fast-forward main + push" in a picker before close-out (learning #8). After
  a `git fetch`, `origin/main` = `b5a336c` was an ancestor of the branch. A scan of the added lines found no
  secrets or local paths. Then `git merge --ff-only` and `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 11 Handoff Evaluation" and "What Session 12 Did" were archived
  (`git show a14ff03:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red (1 test failed on the unfixed code, matching
  the xfail's own assertion); product code fixed and the test watched green; `tests-passed` tightened (116→119,
  more than the "by 1" default, recorded above); the D1/D3/D4/D7 runtime check ran; the fix was red-driven
  against the whole suite with the marker restored.
- `python3 -m pytest -q` gives `119 passed, 7 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 71b7ac5ea8f1 · manifest 973c1b7d973d`, and
  `--precommit` passed on the staged manifest.
- **Runtime (3E):** verified live above — not a build-only claim.

**Key files:**
- `serial_reader.py:105-115` (`_parse_line`'s key=value branch, the fix).
- `tests/test_serial_reader.py:42-46` (the two new T3.1 rows), `:157-159` (D1's test, marker removed).
- `.quality-gates.json:27` (`tests-passed`, 119).
- `docs/planning/test-suite-plan.md`: the Status line, the D1 row in §4's table, and the "As implemented (D1,
  Session 14)" note under §6.
- `BACKLOG.md` (BL-1, new).

**Gotchas for the next session:**
- **D1's suggested probe fix in earlier notes ("split on `;` or `,`, never both") is wrong** — it regresses on a
  trailing separator. Don't reuse it for anything else without probing first.
- **Red-drive with the original marker restored, not just the new tests removed**, and do it before the commit,
  not after (learning #11 — this session did it from the start; Session 13 found the gap after committing).
- **`tests-passed` doesn't always tighten by exactly 1.** This fix added 2 test rows for 1 defect, because the
  probing that found the rejected design's regression turned into a second pinned case. Measure, don't assume.
- **The CARTO map tiles need an API key now** (open item 8) — not a test gap, a live-service change. Neither
  screenshot this session showed real map tiles.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`.
- **Stage files by name** (the 4 untracked files remain, open item 2).
- **The ratchet's `results` hash changes only when a measurement does.** Cite the summary line from the final run.
- **The acting model switched mid-session** (Opus 5 → Sonnet 5, see above). If a future handoff evaluation finds
  a seam in quality or voice between the fix and the close-out, this is why.

**Learnings (3C):** none new. Learning #11 (red-drive against the whole suite) was applied correctly from the
start this session, unlike Session 13's after-the-fact catch — no new row needed, the existing one worked.

**Self-assessment:**
- **Score: 9/10**
- (+) Probed three designs, not one, before writing the fix. The rejected design was Session 12's own suggestion,
  carried in this file's open items — probing it instead of trusting it caught a real regression before it
  reached product code.
- (+) Red-drove with the original marker restored, against the whole suite, before the commit — learning #11
  applied proactively, not as a post-commit catch.
- (+) A gate red-drive confirmed the tightened threshold actually gates (118 fails, 119 passes).
- (+) Full runtime verification: a real process, a real pty, real HTTP calls and two screenshots, not just a
  passing test suite.
- (+) An out-of-band request (BL-1) was handled without touching the D1 diff: its own commit, its own ledger
  entry, no scope bleed.
- (+) Scope held: fix commit touched 4 files; commits were 3, 1 and (this one) several docs files; landing
  decided before close-out (learning #8); no exit code read after a pipe (learning #10).
- (+) Found and recorded a live finding outside the session's contract (the CARTO API-key wall) as a new open
  item rather than either fixing it (scope creep) or silently dropping it.
- (−) `tests-passed`'s "+1 per fix" assumption in the plan and in this file's own open items turned out not to
  hold for D1 (it needed +2). Not caught until the fix was already probed; worth flagging in the plan for the
  remaining fix sessions rather than assuming a fixed increment.
- (−) A mid-session model switch (noted above) is outside this session's control, but it does mean this report's
  own voice isn't uniform. Recorded rather than smoothed over.

### Session 13 Handoff Evaluation (by Session 14)
- **Score: 9/10**
- **What helped:**
  - Open item 1 was an exact recipe for D1: `serial_reader.py:106-117`, the xfail at
    `tests/test_serial_reader.py:157` (marker `:154`), and the fix-session steps (remove marker, fix, tighten by
    1, runtime-check, red-drive). Every citation held on a fresh read.
  - The ratchet citation matched a fresh `--run` exactly (`263dc2f189c8` / `970ed02cfdc1`), and the ledger and
    `HANDOFFS.md` frontiers both sat at the close-out commit with no gap to reconcile.
  - The three-findings list (open item 4) and the coverage-floor and live-API-test items (5–7) gave enough
    context to leave them alone without rediscovering their history.
- **What was missing:** the suggested D1 fix — "split on `;` or `,`, never both," attributed to a Session 12
  probe — wasn't re-verified before being carried into this handoff's recipe. It has a real regression (above).
  This wasn't Session 13's own probe, and Session 13 didn't claim it as verified beyond Session 12's own tests,
  but repeating it in the recipe without a caveat cost this session an extra probing round to catch. Worth a
  standing note: a probe fix carried forward from an earlier session's notes is not re-verified just by being
  repeated.
- **What was wrong:** nothing else found. The `tests-passed` 58→116 arithmetic, the file line counts, and every
  other `file:line` citation checked out.
- **ROI:** strongly positive. Phase 0 to a green fix needed one extra probing round (the rejected design), not a
  rediscovery of anything the handoff should have supplied.

### Session 12 Handoff Evaluation (by Session 13)
- **Score: 9/10**
- **What helped:**
  - Open item 1 was an exact recipe: the files, the four-commit shape, the DONE list and the red-drive.
  - Every citation for Phase 4 held when read this session: `airqino_client.py:8`, `:21`, `:23`, `:30`, `:45`, `:49`,
    `:115`, `:137`; `app.py:51-59`, `:76`, `:92`, `:108`, `:214`, `:220`; plan `:450` and `:521`.
  - The gotchas got used and were right:
    - there is no `FakeReader`, so use `idle_reader`;
    - D6's assertion is on `active_source()`, which reads only the environment. That led straight to the check of
      how D5 and D6 interact;
    - learning #10 (no exit code was read after a pipe this session);
    - keep "passed" out of `reason=`, and stage by name;
    - back up the untracked test module by explicit path (used for the gate's red-drive).
  - The git state matched: `main` = `origin/main` = `ace379d`, and the receipt's ratchet citation matched the results
    file (`dcc07cbf2359`, reproduced at Phase 0).
- **What was missing:** nothing this handoff could have known. The two gaps were older. Phase 1's T1.5 pins D5, which
  only a real D5 fix run against the whole suite shows. The plan's `README.md` citations had moved 9 lines when Phase
  1 added a section. The handoff's "its product citations didn't move" was true, but README isn't product code, and
  I copied the plan's `README.md:27` into a test comment before re-grepping it.
- **What was wrong:** nothing I found.
- **ROI:** strongly positive. Phase 0 to a green Phase 4 needed no rediscovery.

### What Session 13 Did
**Deliverable:** Implement Phase 4 of `docs/planning/test-suite-plan.md` (open item 1): the API client and the
API-mode routes — **COMPLETE**
**Started / Closed:** 2026-09-17 23:04. Claimed on branch `test/suite-phase4` off `main` `ace379d`. Closed on `main`
after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, and plan §5 "Phase 4", the approved
contract. At the start, `git diff --stat 15b0a3f` over the product files was empty, so the contract still held.
**Ledger:** 5 `CHANGELOG.md` entries: the claim, the client tests, the route tests, the branch deletion, and this
close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `5c52bf4`. The operator picked Phase 4 in the Phase 0 picker.
- **Probe first** (learning #7), in the scratchpad. The harness loaded the repo's own `tests/conftest.py` with
  `importlib`, so the routes ran on the suite's `isolated` and `client` fixtures (learning #9). 23 client probes and
  20 route probes were run against drafts of the three fakes. Every T4.x claim held, and D2-hourly, D5 and D6
  reproduced. Nothing surprised, apart from two notes:
  - the chart's 30 d button asks `getRange` for a span exactly 30 days apart (open item 7);
  - `/api/hourly` returns its values as strings. It has no front-end caller, so this is not an open item.
- **Client tests** `0e5ed0d`: `tests/test_airqino_client.py` (175 lines), 25 passing tests (T4.1–T4.9), plus
  `FakeResponse`, `FakeRequests` (`grant`, `refuse`, `answer`) and `FakeClock` in `tests/conftest.py`.
- **Route tests and gate** `5084680`: `tests/test_api_routes.py` (215 lines), 33 passing tests (T4.10–T4.15 and
  `get_api_client()`) and 3 strict xfails (D5, D6, D2-hourly). `FakeClient` and `fake_client` went into
  `tests/conftest.py`, and `tests-passed` was tightened from 58 to 116.
- **Changes from the plan's text,** recorded in its "As implemented (Session 13)" note:
  - `FakeClient` has only the 7 methods `app.py` calls, and binds each call to the real signature;
  - D6 uses `idle_reader` and all four credentials, and T4.15 sets all four too;
  - token requests are routed by `grant_type`, with the URL constants written out in the tests;
  - `get_api_client()` gets tests;
  - T1.5 pins D5 (below).
- **Red-drives**, in the working tree, each restored with `git checkout`, with the shasum the same before and after
  (`airqino_client.py` `8a7c798…`, `app.py` `9ede4c1…`):
  - `airqino_client.py` (10), each failing only its target. The plan's `- 30` → `+ 30` at `:23` failed T4.3, T4.4 and
    T4.5. The others: `"scope"` removed and the password timeout 15 → 30 (T4.1), the `expires_in` default → 600
    (T4.5), a re-raised refresh failure (T4.4), `pivot` never sent (T4.7), the `getSingleDay` path (its T4.6 row),
    `centraline` renamed (T4.8), `_get` without `raise_for_status()` (T4.9), and a refresh sending the access token (T4.3).
  - `app.py` (11), run against the whole suite:
    1. `hours <= 12` → `< 12`: the 12 h row;
    2. `?days=` ignored: the `days=3` row;
    3. the hourly delimiter `;` → `,`: both hourly rows;
    4. `info[0]` → `info[-1]`: the no-match and no-station metadata tests;
    5. `?project=` ignored: its stations row;
    6. the current route's 502 → 500: its 502 row;
    7. `get_range` called with 2 arguments: every range test, through `FakeClient`'s signature check;
    8. a real D5 fix: XPASS(strict), and T1.5 fails (below). At first, D6 flipped too;
    9. a real D6 fix: XPASS(strict) on D6 only;
    10. a real D2-hourly fix: XPASS(strict) on it only;
    11. `get_api_client()` needing only three credentials: the missing-password case.
  - **The D5 fix red-drive found two tests pinning D5.** My D6 test and T4.15 set only `AIRQINO_CLIENT_ID`. Both were
    changed to set all four credentials before the commit, and a re-run showed D5 and D6 each flipping only their
    own test. Phase 1's T1.5 (`tests/test_dashboard_page.py:97`) does the same. It's outside Phase 4's files, so it
    went into open item 1 for the D5 session (learning #11).
  - The gate: with one test hidden, `tests-passed` measured 115 and the ratchet exited 2. The untracked module was
    backed up by explicit path and restored byte-identical (`cmp`).
- **Landing:** the operator picked "fast-forward main + push" in a picker before close-out (learning #8). After a
  `git fetch`, `origin/main` = `ace379d` was an ancestor of the branch. A scan of the added lines found no secrets or
  local paths; its two hits were test names containing "password_grant". Then `git merge --ff-only` and `git branch
  -d`, with the push after this commit.
- **FM #28 reduction:** "Session 10 Handoff Evaluation" and "What Session 11 Did" were archived
  (`git show 5084680:SESSION_NOTES.md`).

**Verification:**
- **Plan §5 P4 DONE, every item met:**
  - `python3 -m pytest -q` and plain `pytest -q` both give `116 passed, 8 xfailed` and exit 0, read with a redirect
    and no pipe;
  - the ratchet passes 2/2 at 116 (the summary line is in ACTIVE TASK), and `--precommit` passed on the staged
    manifest;
  - the red-drives are recorded (above);
  - `git diff --stat HEAD -- app.py airqino_client.py serial_reader.py templates static requirements.txt` was empty
    before commit 3.
- **Runtime (3E):** tests only, so no product runtime behaviour changed. The real `AirQinoClient` and the real routes
  ran, with only `requests`, `time` and `utcnow` faked. **Not verified, and not verifiable yet:** that the real API
  accepts any request (no credentials), plus its response shapes, the Keycloak realm and the 30-day `getRange` cap
  (open item 7).

**Key files:**
- `tests/conftest.py`:
  - `:49` (`FakeResponse`), `:65` (`FakeRequests`; `grant` `:80`, `refuse` `:87`, `answer` `:91`), `:108`
    (`FakeClock`);
  - `:119` (`fake_requests`), `:126` (`fake_clock`);
  - `:133` (`FakeClient`; the signature binding is in `__getattr__`, `:149`), `:164` (`fake_client`).
- `tests/test_airqino_client.py`: `:23` (`api`), `:35` (T4.1), `:94` (the T4.6 table), `:163` (T4.9).
- `tests/test_api_routes.py`:
  - `:46` and `:56` (`get_api_client`), `:83` (the 502 table), `:146` (serial before the API), `:162` (T4.13);
  - `:194` (D5), `:205` (D6), `:213` (D2-hourly).
- `tests/test_dashboard_page.py:97` (T1.5, which pins D5).
- `.quality-gates.json:27` (`tests-passed`, 116).
- `docs/planning/test-suite-plan.md`: `:526` (the "As implemented (Session 13)" note), and §6 (the fix sessions).

**Gotchas for the next session:**
- **A fix session removes a marker, then red-drives the fix against the whole suite** (learning #11). For D5 that
  means T1.5 fails too; set all four credentials there.
- **D2 has two xfails** (`tests/test_csv_routes.py:160`, `tests/test_api_routes.py:213`), so its fix tightens
  `tests-passed` by 2, not 1.
- **Every test that sets all four credentials and calls a data route must install `fake_client`** (or
  `fake_requests`). Otherwise `get_api_client()` builds a real client, and the route sends a real request to
  magentalab.it. `test_status_in_api_mode` is safe without one, because `/api/status` never calls
  `get_api_client()`.
- **`FakeClient` refuses methods it doesn't list.** If a fix makes `app.py` call a new client method, add it to
  `FakeClient.METHODS` (`tests/conftest.py:133`). Until then the call fails, is caught, and shows as a 502.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`.
- **`git rev-parse --short` takes one revision.** Given two, it fails, and a following `&&` skips the next check.
- **Keep "passed" out of `reason=` strings,** and **stage files by name** (the 4 untracked files remain, open item 2).
- **The ratchet's `results` hash changes only when a measurement does.** Cite the summary line from the final run.

**Learnings (3C):** `CLAUDE.md` learning #11: a real-fix red-drive tests the other tests too. Configure state next to
a defect fully, and run the fix against the whole suite.

**Self-assessment:**
- **Score: 8/10**
- (+) Every asserted behaviour was probed first on the suite's own fixtures, 43 probes in all, before a test was
  written.
- (+) 21 red-drives on product code and 1 on the gate. The real D5, D6 and D2-hourly fixes proved each strict-xfail
  flip, and the `get_range` mutation proved `FakeClient`'s signature check.
- (+) The whole-suite D5 red-drive found three tests pinning a known defect: two of mine (fixed before the commit) and
  Phase 1's T1.5 (handed off, not edited, since it's outside the contract).
- (+) Scope held: no product code, commits of 3 and 4 files, and the landing decided before close-out (learning #8).
- (+) No exit code was read after a pipe (learning #10 held).
- (−) I wrote D6 and T4.15 with only `AIRQINO_CLIENT_ID` set, which pins D5, the very thing plan §7 rejects. Only
  the red-drive caught it.
- (−) A test comment cited `README.md:27`, copied from the plan without a re-grep (learning #7's failure). The first
  run's output check caught it before the commit.
- (−) A `git rev-parse --short` with two arguments failed and skipped the ancestor check behind it. The output gave it
  away, and it was re-run.
- (−) The first draft of a ledger entry used a nested list, unlike the ledger's one-line bullets. Fixed before the
  commit.
- (−) Four harness nudges for silence during long runs of tool calls, which repeats the Session 6–12 minus.

### Sessions 1–12 (archived by Sessions 6–14)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
"Session 9 Handoff Evaluation" and "What Session 10 Did": `git show be5723c:SESSION_NOTES.md`.
"Session 10 Handoff Evaluation" and "What Session 11 Did": `git show 5084680:SESSION_NOTES.md`.
"Session 11 Handoff Evaluation" and "What Session 12 Did": `git show a14ff03:SESSION_NOTES.md`.
