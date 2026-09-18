# Session Notes

**Purpose:** Continuity between sessions. Each session reads this first and writes to it before closing out.

---

## ACTIVE TASK

**Current focus:** The test suite is complete (all four phases on `main`). Of the plan's fix sessions (§6), D1
(Session 14) and D7 (Session 15) are done. Next: D3 (plan §6's order continues D3 and D4, then D6, D5 and D2), or
any other open item.
**Status:**
- **D7: FIXED, Session 15, on `main`** (`222f02c` page, `9698f9c` server and tests, `87c7535` README and gate). A
  serial port that fails to open is now a 503 `{"source": "serial", "data": null, "error": …}`, not a 200 with the
  error as data, and the page shows the error in red in the readings grid. The reader keeps the failure in a new
  `error` field instead of `latest`. `main` was fast-forwarded to the Session 15 branch, which was then deleted.
  `main` is the only branch, and it is pushed straight after the close-out commit. Check with `git status -sb`.
- **Suite:** `python3 -m pytest -q` gives `120 passed, 6 xfailed` in about 0.36 s. The ratchet gives
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`. The gates
  are `tests-exit` (max 0) and `tests-passed` (min 120).
- **Dashboard:** 68/100, unchanged, with High+ risk 0. It has 5 flags, listed from `dashboard.html` (not grepped for
  known ones; see gotchas): MEDIUM "No CI/CD pipeline" (now BL-3); MEDIUM, a large file, the synced
  `docs/methodology/tools/methodology_dashboard.py`; LOW "No LICENSE file" (BL-1); LOW "BACKLOG.md: done-mark format
  not recognized" (BL-2; it began with BL-1 in Session 14, whose handoff called the flags unchanged); LOW, new this
  session, `CHANGELOG.md` past its one-read budget (59,986 B of 56,750 B), which the dashboard says needs no action.
- **Defects (plan §4):** D1 and D7 fixed. D2, D3, D4, D5, D6 still have strict xfails, 6 tests in all (D2 has two).
- **BACKLOG.md** has three items, none started: BL-1 (MIT licensing, Session 14), and two the operator added
  mid-Session-15: BL-2 (give items `- [ ]` checkboxes so the dashboard's done-mark check works) and BL-3 (decide
  whether the repo needs CI/CD).
- **Merge settings:** GitHub allows merge commits only (squash and rebase are off), so learning #6 is a gate for PR
  merges.
- Earlier status: Session 14's is at `git show b710ac0:SESSION_NOTES.md`, Session 13's at `git show b5a336c:SESSION_NOTES.md`.

### Open items — next session picks ONE (1-and-done)

1. **Fix D3 (recommended next): the plan's fix sessions (§6), one defect per session.** D1 and D7 are done. The
   remaining order is D3 and D4, then D6, D5 and D2. Each session, on a new branch off `main`:
   - removes the defect's `xfail` marker and watches its test fail on the unfixed code;
   - **before choosing a design, runs the candidate fix end to end on the surface the user sees** (learning #12):
     for D3 and D4 that is a CSV upload in the real app, then the chart and readings grid;
   - fixes the product code and watches the test pass;
   - tightens `tests-passed` by the measured delta (1 for D3, D4, D5, D6; 2 for D2 — but measure);
   - red-drives the fix against the whole suite with the original marker restored (learning #11). Also run the
     whole suite on the fix alone: in Session 15, that is how T3.7 showed up pinning D7's representation;
   - re-greps every `file:line` citation after editing product code (Session 15 moved 11 in the tests).

   Where each one is:
   - **D3:** `app.py:262-265`; its xfail is `tests/test_csv_routes.py:167` (marker `:165`). A ragged CSV row puts
     extras under the key `None`, and `k.strip()` fails.
   - **D4:** `app.py:249`; its xfail is `tests/test_csv_routes.py:174` (marker `:172`). A UTF-8 BOM stays in the
     first header.
   - **D2:** `app.py:175` and `:224`; its xfails are `tests/test_csv_routes.py:160` and `tests/test_api_routes.py:213`.
   - **D5:** `app.py:53`; its xfail is `tests/test_api_routes.py:194`. **A real D5 fix also fails Phase 1's T1.5**
     (`tests/test_dashboard_page.py:97`), which sets only `AIRQINO_CLIENT_ID`. That session must set all four
     credentials in T1.5 as well.
   - **D6:** `app.py:53-58`; its xfail is `tests/test_api_routes.py:205`.

   The plan's own `app.py` citations past `:142` read 4 lower than the code since D7 (noted in the plan). Use the
   lines above. Probe fixes carried in these notes are starting points, not verified designs (D1's was rejected
   in Session 14; D7's "2-line 503" would have left the page stuck on "Loading readings…").
2. **Decide the untracked files.** For each one, commit, gitignore or delete; that's the operator's call.
   - `docs/HARDWARE.html` has been untracked since Session 3. It is an HTML render of `docs/HARDWARE.md` and holds no
     stale hardware copy.
   - Three tool outputs, all present now, have no `.gitignore` entry: `dashboard_history.jsonl` (written by every
     dashboard run); `.quality-gates-results.json` (from `quality_ratchet.py --run`, which the `.quality-gates.json`
     seed says to gitignore); `.context-budget-history.jsonl` (from `context_budget.py`).
3. **Give `CLAUDE.md` a statement of purpose.** The synced `context_budget.py` reports the `budget:protected` fence
   missing: `.context-budget.json` declares it for `CLAUDE.md`, with a minimum of 800 B. `CLAUDE.md` has never had a
   fence or a Purpose section, and `README.md`'s opening is the source text. The same tool also reports
   `SESSION_NOTES.md` as "instrument-failed", for two reasons, both in the tool, not this file:
   - `.context-budget.json` expects at least 2 `^## ` headings, but this file has 1, and so does the synced seed
     `docs/methodology/starter-kit/SESSION_NOTES.md`.
   - its 400-line ceiling counts one line more than `wc -l` (`measure_file`, `context_budget.py:329`, counts
     `text.split("\n")` at `:347`), so this file must stay at 399 lines or fewer by `wc -l` to pass it.

   Both are mismatches inside the methodology's own tooling. Raise them upstream rather than restructuring this
   file to satisfy either one.
4. **Decide four findings (the operator's call).** No test pins any of them, and none is in the plan's §4 list:
   - After an empty CSV upload, `/api/status` returns `source: null` with `has_csv: true`. `app.py:87` checks
     `_csv_data is not None`, but `active_source()` (`:57`) checks truthiness, and `[]` is falsy. No front-end code
     calls `/api/status`. (Session 11.)
   - `?hours=` is ignored in CSV mode and in serial mode. CSV returns the last 500 rows (`app.py:207-212`), and
     serial returns `get_history(limit=500)` (`:181`), whatever the range. So the chart's 6h–30d buttons
     (`templates/dashboard.html:86-91`) change nothing outside API mode.
   - With a port that failed to open, `/api/timeseries` still answers 200 with `data: []` (D7 changed only
     `/api/current`). The chart is empty either way, and the readings grid now shows the error.
   - **(new, Session 15, probed)** A port that opens and then fails (a pty closed mid-run, standing in for an
     unplugged adapter) is never reported: the reader thread keeps running with `error` `None`, `_read_loop`'s
     `except` (`serial_reader.py:87-88`) sleeps and retries forever, and `/api/current` keeps serving the last
     reading with 200. Each reading card shows its timestamp, so the age is visible. Related gaps: the reader never
     retries a port that failed to open (restart needed, now said in `README.md:73`), and on a fresh page load the
     error appears only at the 60 s refresh, because the first request starts the reader and gets 202.

   Each could become a new defect with a strict xfail (a plan amendment), or be recorded as intended.
5. **Sync the methodology (new in Session 12).** `context_budget.py` reports that `SAFEGUARDS.md` differs from
   canonical: the local copy is `df926b6` (2026-09-16), 1 commit behind `0d63410` (BL-63, how to commit a `bin/sync`
   run). Run `bin/sync` from `~/Development/methodology`. Don't edit the synced file here.
6. **Declare a coverage floor (new in Session 13).** Plan §8 defers it until after Phase 4, then to its own session:
   measure with pytest-cov (installed, 7.1.0), declare the floor at the measured value in `.quality-gates.json`, and
   pair it with a mutation spot-check. Sessions 13–15's red-drives are the start of that check.
7. **A live API test, once credentials arrive (blocked).** Plan §5 Phase 4 surface: `@pytest.mark.live`, skipped
   without credentials, in its own session. It should settle one question the fakes can't. The chart's 30 d button
   asks `getRange` for 2026-08-18 to 2026-09-17 on a 2026-09-17 clock (`tests/test_api_routes.py:160`), which is 30
   days apart. `README.md:110` says the API rejects spans over 30 days, and whether it counts that span as 30 days or
   31 is unknown.
8. **The map's tile provider now demands an API key (Session 14, no test pins it).** `static/js/dashboard.js:355`
   loads `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png` with no key. A direct `curl` of one tile
   returns 200 with an image reading "API KEY REQUIRED", not a 4xx, so nothing in the app's code or tests would
   catch it. Whether a free key exists and how to wire it in, or which other tile source to use, is a design
   question for its own session. BL-1 (MIT licensing) also touches this, since a tile provider swap changes what is
   credited and under what licence.
9. **The three backlog items** (BL-1, BL-2, BL-3 in `BACKLOG.md`). BL-2 is small and mechanical (checkboxes, one
   commit); BL-1 and BL-3 each start with the operator's decisions.

### Connecting a Live Data Source (updated Session 2)
The AirQino REV6 board has **NO USB port**. Three paths remain:
1. **USB-to-TTL serial adapter** — user needs a CP2102 or FT232RL adapter + dupont jumper wires to connect to board's TX/RX pins. See `docs/HARDWARE.md` for wiring and adapter recommendations. User is sourcing an adapter now.
2. **API credentials** — user contacts info@airqino.it with serial AIRO 6153. Once received, set `AIRQINO_CLIENT_ID`, `AIRQINO_CLIENT_SECRET`, `AIRQINO_USERNAME`, `AIRQINO_PASSWORD` in `.env`
3. **SD card** — device has onboard SD card (confirmed by LED diagnostics). Locate slot, extract card, upload CSV via dashboard UI.
4. **CSV upload** — manual upload via dashboard UI for any CSV data

---

*Session history accumulates below this line. Newest session at the top.*

### What Session 15 Did
**Deliverable:** Fix D7 (open item 1; plan §6's second fix session): a serial port that fails to open was served
as data with 200 (`serial_reader.py:64-69`, `app.py:141-147` at the start) — **COMPLETE**
**Started / Closed:** 2026-09-17 23:47 / 2026-09-18 00:20. Claimed on branch `fix/d7-port-open-failure` off `main`
`b710ac0`. Closed on `main` after a fast-forward, and pushed straight after the close-out commit.
**Governing docs:** `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` (read in full), and plan §6 (fix
sessions), the approved contract from Session 9's plan.
**Ledger:** 10 `CHANGELOG.md` entries: the claim, BL-2, BL-3, D7 parts 1–3, the test-citation follow-up, the plan
update, the branch deletion, and this close-out, which also records the fast-forward and the push.

**What was done:**
- **Claim** `2fc1d25`. The operator picked D7 in the Phase 0 picker.
- **Two backlog items, out of band, each its own commit:** BL-2 (`d24ab0e`), because the dashboard can't read
  plain-bullet backlog items, so its done-mark check is off; my Phase 0 report had missed that signal. BL-3
  (`192e831`), deciding whether the repo needs CI/CD. The D7 changes stayed unstaged through both.
- **Probed before designing** (learning #7). The real app with `SERIAL_PORT=/dev/does-not-exist` reproduced D7:
  202, then 200 with the error as data; the page showed "Loading readings…", then "No readings available". A
  scratchpad copy with a server-only fix (503 plus the error) turned the xfail green, but the page stayed on
  "Loading readings…" indefinitely: `loadCurrent` only logs a non-2xx response. Plan §4's user-impact cell had
  assumed the page reports them. The operator chose "server + page" in a picker.
- **Red on the unfixed code:** with the marker removed, only D7's test failed (`assert 200 != 200`).
- **D7, three commits, each green and true at its own point** (the 5-file cap ruled out one commit):
  - `222f02c` page: `fetchJSON` tags its `Error` with the body's `source`; `loadCurrent` calls a new
    `renderReadingsError` for a `serial` source (red, centred, `textContent`). Other errors are still only logged.
  - `9698f9c` server: the reader's open failure goes in a new `error` field, not `latest`; `/api/current` answers
    503 `{"source": "serial", "data": null, "error": …}`. D7's marker removed and its test pins the 503. The
    whole-suite run on the fix failed T3.7 too, which asserted `latest["error"]`; it now checks `reader.error`.
  - `87c7535`: a README paragraph (the error shows within a minute; the reader doesn't retry, so restart), the
    `README.md:108`→`:110` citation it moved, and `tests-passed` 119 → 120.
- **Red-drives**, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with the
  original marker and assertion (only D7's `XPASS(strict)`); the new tests on the unfixed code (D7 and T3.7 fail);
  the reader change alone (D7 fails, 202 until the deadline); 500 instead of 503 (D7 fails); the route change alone
  (5 fail). The gate: with one test hidden, `tests-passed` measured 119 and the ratchet exited 2.
- **Runtime (learning #5):** the real app, before and after, by `curl` and headless-Chrome screenshots. After the fix:
  202 then 503, and the error shows in red in the readings grid, at once on a reload, and on a fresh load after
  the 60 s refresh (70 s of virtual time). Adjacent paths unchanged: the no-source page; a pty fed
  `co=235;no2=17;o3=17;pm10=25;pm25=13` gives 200 and five reading cards. App, Chrome and pty feeder stopped each
  time; port 5001 free (`lsof` exit 1).
- **Citations:** the fix moved 11 `file:line` citations in the tests (`2519647`) and BL-1's map-tile line (`c159ac8`).
- **Plan updated** (`c159ac8`): Status line, D7's §4 row, and an "As implemented (D7, Session 15)" note under §6.
- **Probed a related claim before recording it:** a pty closed mid-run leaves the reader running with no error and
  the last reading served (open item 4, new).
- **Landing:** the operator picked "fast-forward main + push" before close-out (learning #8). After a `git fetch`,
  `origin/main` = `b710ac0` was an ancestor of the branch; a scan of the added lines found no secrets or local paths
  (its one hit was BL-3's prose). Then `git merge --ff-only` and `git branch -d`, with the push after this commit.
- **FM #28 reduction:** "Session 12 Handoff Evaluation" and "What Session 13 Did" were archived
  (`git show c159ac8:SESSION_NOTES.md`).

**Verification:**
- **Plan §6 DONE, every item met:** marker removed and watched red; product code fixed and the test watched green;
  `tests-passed` tightened 119 → 120 (measured); runtime check done; red-driven against the whole suite with the
  marker restored.
- `python3 -m pytest -q`: `120 passed, 6 xfailed`, exit 0, read from a file with no pipe (learning #10).
  `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`; `--precommit`
  passed on the staged manifest. `node --check static/js/dashboard.js` exit 0.
- **Runtime (3E):** verified live above. Not verifiable here: API mode's error display (no credentials). By
  reading, a 502 body names no `source`, so it is still only logged.

**Key files:**
- `serial_reader.py:43` (`error`), `:67-70` (the open failure), `:87-88` (the loop's `except`, open item 4).
- `app.py:143-146` (the 503).
- `static/js/dashboard.js:134-143` (`fetchJSON`), `:145-157` (`loadCurrent`), `:231-241` (`renderReadingsError`).
- `tests/test_serial_routes.py:49-62` (D7's test), `tests/test_serial_reader.py:150-155` (T3.7).
- `.quality-gates.json:27` (`tests-passed`, 120); `README.md:73` (the serial-error paragraph).
- `docs/planning/test-suite-plan.md:587` (the "As implemented (D7, Session 15)" note).

**Gotchas for the next session:**
- **A green xfail isn't the user-visible fix** (learning #12). Look at the page with the candidate fix before
  choosing the design. D3 and D4 are CSV uploads: check the chart and readings grid in the real app.
- **The dashboard's flags: list them all from `dashboard.html`**, e.g. the `risk-flag` divs, rather than grepping
  for the ones the last handoff named. Session 15's Phase 0 grep missed a LOW flag that way (learning #13).
- **This file must stay at 399 lines or fewer by `wc -l`** (open item 3). Session 14's "400 at close-out" was
  measured before its last edit; the committed file was 407.
- **`app.py` citations in the plan are 4 lower than the code past `:142`.** Use open item 1's lines.
- **Exit codes (learning #10):** redirect to a scratchpad file, then `echo $?`. **Stage files by name** (the 4
  untracked files remain, open item 2). **Cite the ratchet summary line from the final run.**

**Learnings (3C):** `CLAUDE.md` learning #12 (a green xfail isn't the user-visible fix; run the candidate fix on
the page first) and #13 (list the dashboard's flags from its output, not by grepping for known ones).

**Self-assessment:**
- **Score: 8/10**
- (+) Probed the fix's user-visible end before choosing a design. That found plan §4's wrong premise, and the
  operator decided on the evidence (two screenshots) instead of a guess.
- (+) 5 product red-drives and 1 gate red-drive, all against the whole suite. The fix's own whole-suite run caught
  T3.7 pinning D7's representation (learning #11 working as written).
- (+) Runtime checks covered the fixed path (reload and fresh load), and the no-source and working-serial paths
  next to it.
- (+) The 5-file cap held through 3 D7 commits, each green and true at its own point. Both out-of-band backlog
  requests were committed on their own, with the D7 changes unstaged.
- (+) Every moved `file:line` was re-grepped and fixed (13 in all), and a new claim was probed before it went into
  the handoff.
- (−) The Phase 0 report missed a LOW dashboard flag: I grepped for the three flags the handoff named. The
  operator raised it.
- (−) BL-3's first draft cited `:3226-3230` for a 6-line block ending at `:3231`. The re-grep caught it before the
  commit.
- (−) Several harness nudges for silence during long runs of tool calls, which repeats Sessions 6–14's minus.

### Session 14 Handoff Evaluation (by Session 15)
- **Score: 8/10**
- **What helped:**
  - Open item 1's D7 recipe and citations held on a fresh read: `serial_reader.py:64-69`, `app.py:141-147`, the
    xfail at `tests/test_serial_routes.py:54` (marker `:51`).
  - The warning that carried-forward probe fixes are starting points, not designs, is what made me look at the page.
    The suggested "2-line 503" would have left it stuck on "Loading readings…".
  - Open item 4's third finding (D7's `/api/timeseries` state) framed the scope question early. "Measure the
    `tests-passed` delta, don't assume" held (it was 1 this time, by measurement).
  - The ratchet citation matched a fresh `--run` (`71b7ac5ea8f1` / `973c1b7d973d`), and both frontiers sat at
    `b710ac0` with nothing to reconcile.
- **What was wrong:**
  - "`wc -l` and `splitlines()` agree on 400 for this file at close-out": the committed file (`b710ac0`) was 407.
  - "The flags are unchanged too": Session 14's own BL-1 had added a LOW flag (the backlog done-mark format), so
    there were four, not three.
  - `context_budget.py:346` (open item 3) is neither `measure_file` (`:329`) nor its split (`:347`).
- **What was missing:** nothing else the handoff could have known. The wrong page premise came from plan §4
  (Session 9).
- **ROI:** strongly positive. Phase 0 to a probed design needed no rediscovery.

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

### Sessions 1–13 (archived by Sessions 6–15)
Removed to keep this mandated read under its ceiling (FM #28). Sessions 1–3, including their handoff evaluations:
`git show 1402ad4:SESSION_NOTES.md`. "What Session 4 Did": `git show e947798:SESSION_NOTES.md`. "Session 4 Handoff
Evaluation" and "What Session 5 Did": `git show a31fea6:SESSION_NOTES.md`. "Session 5 Handoff Evaluation", "What
Session 6 Did", "Session 6 Handoff Evaluation" and "What Session 7 Did": `git show 15b0a3f:SESSION_NOTES.md`.
"Session 7 Handoff Evaluation" and "What Session 8 Did": `git show 4da62a1:SESSION_NOTES.md`.
"Session 8 Handoff Evaluation" and "What Session 9 Did": `git show fa73763:SESSION_NOTES.md`.
"Session 9 Handoff Evaluation" and "What Session 10 Did": `git show be5723c:SESSION_NOTES.md`.
"Session 10 Handoff Evaluation" and "What Session 11 Did": `git show 5084680:SESSION_NOTES.md`.
"Session 11 Handoff Evaluation" and "What Session 12 Did": `git show a14ff03:SESSION_NOTES.md`.
"Session 12 Handoff Evaluation" and "What Session 13 Did": `git show c159ac8:SESSION_NOTES.md`.
