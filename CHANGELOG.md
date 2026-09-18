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

### 2026-09-18 · [ad hoc] The test plan records D8 as found, amended into §4 and fixed; a count in the fix's entry corrected
- **Change:** `docs/planning/test-suite-plan.md`, on the operator's direction (the Session 19 picker): the Status line names D8 as fixed (`b53303e`); §4 gains a D8 row, marked fixed, which says it was found by Session 18's probe and has no xfail; Session 18's race paragraph in §6 now points at D8; and a new "As implemented (D8, Session 19)" note records the three candidates' probe results, the planted test and its red-drives, the 3 lines the fix added (so the plan's `app.py` citations now read low by 1 from the old `:7`, by 2 from `:21` and by 3 from `:40`), and the `get_api_client()` finding, which stays out of scope. **Correction:** the `b53303e` entry below says the unfixed code gave "2 of 15 readings clean". The five trials held 14 readings, so it was 2 of 14; a recount of the probe output before this commit found it. Entries are never edited, so it is corrected here
- **Commit/PR:** this commit
- **Session:** S19 · **Verified:** every count in the note recounted from the probe output files (unfixed 14 readings, 2 clean, fds 2 in each of 5; lock 23 of 23, fds 1 in each; `exclusive=True` 503 in 4 of 5; the repo's app 22 of 22); each new `file:line` printed against the file (`app.py:7`, `:22`, `:42`, `:40-51`; `airqino_client.py:21-47`; `static/js/dashboard.js:484-485`)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] The tests' `app.py` citations follow the 3 lines the D8 fix added
- **Change:** `b53303e` added an import and the lock above `get_api_client()` and a `with` line inside `get_serial_reader()`, so every `app.py` line from the old `:8` moved down: by 2 for `get_api_client()`, by 3 from the old `:49` on. Eight citations in three test files now point at the same code again: `tests/conftest.py` (the reader's fast path `:43-44`, the client's `:28-29`); `tests/test_api_routes.py` (`get_api_client()` `:26-37`, the data routes' serial checks `:144, :182`, and the reasons of D5's xfail `:58, :34` and D2's hourly xfail `:227`); `tests/test_csv_routes.py` (the serial reshape `:185-189`, D2's timeseries xfail `:178`). `tests/test_serial_routes.py`'s own two moved with the fix. Comments and xfail reasons only; no assertion changed. Split from the fix commit to keep each under the 5-file cap
- **Commit/PR:** this commit
- **Session:** S19 · **Verified:** each new citation printed against `app.py` lands on the line it names; `python3 -m pytest -q` gives `129 passed, 3 xfailed`, exit 0, and the three xfail reasons print the new lines
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D8 fixed — concurrent first requests start one serial reader, not two
- **Change:** `app.py` `get_serial_reader()` now holds a module-level `threading.Lock` (`_serial_lock`) while it checks `_serial_reader` and builds and starts the reader (`app.py:40-51`). Before, the page's first load sent `/api/current` and `/api/timeseries` together (`static/js/dashboard.js:484-485`), both found no reader, and each started one on the same port, so two threads split its bytes. The operator named it D8 (a plan §4 amendment, recorded in the next commit) and kept `get_api_client()` out of scope. Probed first on fresh apps with no warm-up, a pty feeding the docstring's line: unfixed, 2 fds on the pty in 5 of 5 trials and 2 of 15 readings clean, and the page's grid lost its CO card; the lock, 1 fd in 5 of 5 and 23 of 23 clean, with all five cards; `exclusive=True` on the port, 1 fd but `/api/current` answered 503 "Could not exclusively lock port" in 4 of 5 trials, and the page told the user to check the adapter and restart. New test `tests/test_serial_routes.py::test_concurrent_first_requests_start_one_reader`: a stand-in reader that sleeps 0.2 s while it's built and starts no thread, and two threads released by a `threading.Barrier` send the two requests; it asserts 202 and 200, one reader built, and that reader kept. The file's own two `app.py` citations follow the 3 lines the fix added. `.quality-gates.json` `tests-passed` tightened from 128 to 129. The other tests' `app.py` citations move in the next commit
- **Commit/PR:** this commit
- **Session:** S19 · **Verified:** the new test failed on the unfixed code in 20 runs of 20 (`assert 2 == 1`) and passed on the fix in 20 of 20; `python3 -m pytest -q` gives `129 passed, 3 xfailed`, exit 0; red-drives against the whole suite, files restored byte-identical (`shasum -c`): the unfixed code and a lock around the check only each fail just the new test, double-checked locking passes, and the test without its delay passed on the unfixed code in 10 of 10 (so the delay is the planted hazard, and its comment says so); the gate, with the new test hidden, measured 128 and the ratchet exited 2; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 9706974b83af · manifest 501e3c8538de`; runtime on the repo's app: 5 fresh apps, 1 fd and 22 of 22 readings clean, the driven page showing all five cards and 5-point series, a bad port still shown as D7's error, and no source still the banner
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 19 claimed — serial-reader race fix begins (in progress)
- **Change:** the operator picked the serial-reader race (open item 1, recommended) in the Phase 0 picker. Session 18's D6 probe found it and it is not in `docs/planning/test-suite-plan.md` §4: `get_serial_reader()` (`app.py:38-48`) checks `_serial_reader`, then builds and starts a `SerialReader` with no lock, and the page's first load sends `/api/current` and `/api/timeseries` together (`static/js/dashboard.js:484-485`), so two readers open one port and split its bytes. Session claimed on branch `fix/serial-reader-race` (off `main` `34a0a75`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S19 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 18 closed out — D6 fixed, the plan's fifth fix session done; a serial-reader race found and recorded; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the Session 17 handoff evaluation (9/10; nothing wrong found; missing only the serial-reader race, which no earlier handoff mentions), the full D6 write-up and a 7/10 self-assessment (a false "no citation moves" claim reached `91ea569` and was corrected by `2943371`; the operator was told "most likely a probe artifact" before anything was measured). Open item 1 now recommends the serial-reader race, then D5 and D2, with current citations (D5 at `app.py:55`, markers `tests/test_api_routes.py:224` and `:232`), a test design that plants the race, and a candidate lock fix labelled unverified. Open item 7's citation moved to `tests/test_api_routes.py:193`; open items 5 and 8 were re-checked and still hold. `CLAUDE.md` gains learning #16: an anomaly in a probe is evidence until a measurement explains it. The S18 `HANDOFFS.md` receipt is `status: complete`. FM #28 reduction: "Session 15 Handoff Evaluation" and "What Session 16 Did" archived (`git show 2943371:SESSION_NOTES.md`). On the operator's direction (the landing picker), `main` was fast-forwarded from `be44a02` to `91ea569`, then gained `2943371`, and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `2160d6b`, `5056055`, `91ea569`, `2943371`
- **Session:** S18 · **Verified:** `python3 -m pytest -q` gives `128 passed, 3 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0002758d231d · manifest f7714b97d99b`; dashboard 68/100, High+ risk 0, the same 6 flags as at Phase 0, listed from `dashboard.html` after the close-out edits; every `file:line` in the new handoff text printed against the current files; a byte scan of every touched file finds no BOM, zero-width space or no-break space this session added; `wc -l SESSION_NOTES.md` is 399; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Local branch `fix/d6-source-order` deleted
- **Change:** on the operator's direction (the landing picker), `main` was fast-forwarded to the branch (`git merge --ff-only`, `be44a02..91ea569`), and the fully merged local branch `fix/d6-source-order` (tip `91ea569`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch. The D5 citation correction, `2943371`, was committed on `main` after the deletion
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S18 · **Verified:** after `git fetch`, `git merge-base --is-ancestor origin/main fix/d6-source-order` succeeded before the merge; afterwards `git merge-base --is-ancestor` confirmed the branch and each of `2160d6b`, `5056055`, `91ea569` are in `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D5's citation follows the check the D6 fix moved; the plan's "no citation moves" claim corrected
- **Change:** `tests/test_api_routes.py`: D5's xfail reason cites `app.py:55`, not `:53`, since `5056055` moved the `AIRQINO_CLIENT_ID` check there. `docs/planning/test-suite-plan.md` §6's D6 note (`91ea569`) said the swap moved no `app.py` citation, because the line count held; it moved the content of `:53` and `:55`. The note now says so and points §4's D5 citation at `:55`. Found at close-out by grepping every surface for citations into `app.py:51-59`. Earlier ledger entries and receipts citing `:53` stay as written
- **Commit/PR:** this commit
- **Session:** S18 · **Verified:** `sed -n 55p app.py` prints the `AIRQINO_CLIENT_ID` check; whole suite `128 passed, 3 xfailed`, exit 0; byte grep of both files: no BOM, zero-width space or no-break space added (the plan's 1 BOM is Session 9's §4 D4 row)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Test plan records D6 as fixed, and a serial-reader race the D6 probe found
- **Change:** `docs/planning/test-suite-plan.md`: the Status line names D6 as fixed (`5056055`), with D5 and D2 left; D6's §4 row is marked fixed; a new "As implemented (D6, Session 18)" note in §6 (`:634`) records the probe, the one design the xfail and README allow, the four-mix test (124 → 128), and the metadata "Project" row side effect. The note also records a defect outside §4, found by the probe: when `/api/current` and `/api/timeseries` are the first two requests and arrive together, as on every page load (`static/js/dashboard.js:484-485`), `get_serial_reader()` (`app.py:38-48`) starts two `SerialReader`s on one port, and they split its byte stream (pty only, not a real adapter). No test covers it, and it was not fixed here
- **Commit/PR:** this commit
- **Session:** S18 · **Verified:** each new citation printed against the current files (`app.py:38-48`, `:53-56`; `static/js/dashboard.js:484-485`, first written as `:480-482` from memory and corrected; `templates/dashboard.html:111`; `README.md:36`); the race from a scripted A/B in the scratchpad, a fresh app per trial: two concurrent first requests left the pty open twice in 3 of 3 starts, two sequential ones once in 3 of 3; the plan's BOM count is 1 before and after (Session 9's §4 D4 row)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D6 fixed: with serial and the API both configured, the badge says "Serial", the source the readings come from
- **Change:** `app.py:53-56`: `active_source()` now checks `SERIAL_PORT` before `AIRQINO_CLIENT_ID`, the order the data routes use (`:141`, `:179`) and `README.md:36` documents. Before, the header badge and `/api/status` said "API Connected"/`api` while `/api/current` and `/api/timeseries` served serial readings; probed on the real page (headless Chrome, a pty feeding sensor lines, four fake credentials, every proxy variable pointed at a closed port so no request could reach the vendor), where only the badge changed. `tests/test_api_routes.py`: D6's strict xfail is now a test parametrized over the four mixes of two or more sources (serial+api, serial+csv, api+csv, all three), each asserting that `active_source()`, the badge, `/api/status`, `/api/current` and `/api/timeseries` name the same source; it moved above the known-defects block. `.quality-gates.json`: `tests-passed` 124 → 128 (measured: one xfail became four passing cases). Only design consistent with the approved plan's assertion and README, so no design picker; routes going API-first instead fails four tests (red-drive below). Side effect: the metadata panel's "Project" row (`templates/dashboard.html:111`, gated on `source == 'api'`) no longer renders with both configured; `renderMetadata` replaces that panel once `/api/metadata` answers, so it shows only when that call fails
- **Commit/PR:** this commit
- **Session:** S18 · **Verified:** red first: with the marker removed and `app.py` unfixed, only the serial+api and all-three cases failed (`'api' == 'serial'`), whole suite `2 failed, 126 passed, 3 xfailed`. Fixed: `128 passed, 3 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0002758d231d · manifest f7714b97d99b`. Red-drives against the whole suite, files restored byte-identical (`shasum -c`): the fix with the original test and marker gives only D6's `XPASS(strict)` (nothing else pinned the old order); serial → CSV → API fails only api+csv; API-first routes with `active_source()` unfixed fail serial+api, all-three and both `test_serial_is_served_before_the_api` cases; with the api+csv case hidden, `tests-passed` measured 127 and the ratchet exited 2. Runtime (learning #5): the fixed app from the repo, driven page reads "Serial" over five serial reading cards and two chart series; a fresh app per mix (none, serial, api, csv, serial+api, api+csv, serial+csv) gives a badge, `/api/status` and both data routes that agree; no 502 in any log; ports 5001 and 9333 free afterwards. Byte grep of the three touched files: no BOM, zero-width space or no-break space
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 18 claimed — D6 fix begins (in progress)
- **Change:** the operator picked the D6 fix (open item 1; `docs/planning/test-suite-plan.md` §6's fifth fix session) in the Phase 0 picker. D6: `active_source()` checks the API before serial (`app.py:53-58`), but `/api/current` and `/api/timeseries` try serial first (`:141`, `:179`), so with both configured the header's badge names a source the data doesn't come from. Session claimed on branch `fix/d6-source-order` (off `main` `be44a02`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S18 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 17 closed out — D4 fixed, the plan's fourth fix session done; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the Session 16 handoff evaluation (9/10; nothing wrong found; missing only what it had no reason to hit: the Flask reloader's two PIDs, and D4's test holding its BOM as an invisible literal), the full D4 write-up and a 7/10 self-assessment, down from 8 for the false escape claim in `caec75a`'s ledger entry, corrected by `18e94c3`. Open item 1 now recommends D6, with current citations and a probe plan whose no-vendor-traffic premise is labelled as read, not probed. Open item 7 gains the question of whether the API's hourly CSV starts with a BOM. Open items 5 and 8 were re-checked and still hold. New open item 10: make learning #15 a gate. `CLAUDE.md` gains learning #15: an invisible character in a test is a hazard no reader can see; write it as an escape through a script, and check the bytes before claiming it's gone. The S17 `HANDOFFS.md` receipt is `status: complete`. FM #28 reduction: "Session 14 Handoff Evaluation" and "What Session 15 Did" archived (`git show 9812ef3:SESSION_NOTES.md`). On the operator's direction (a picker before close-out), `main` was fast-forwarded from `9995f62` to `9812ef3`, then gained `18e94c3`, and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `d63e4f9`, `caec75a`, `9812ef3`, `18e94c3`
- **Session:** S17 · **Verified:** `python3 -m pytest -q` gives `124 passed, 4 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 5de9dfd7b3bc · manifest c0a107040a76`; dashboard 68/100, High+ risk 0, 6 flags listed from `dashboard.html` after the close-out edits; every `file:line` in the new handoff text printed against the current files; a byte scan of every touched file finds no BOM, zero-width space or no-break space this session added (the 2 BOMs in `caec75a`'s committed entry and the 1 in the plan's Session 9 §4 row remain); `wc -l SESSION_NOTES.md` is 386; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Local branch `fix/d4-csv-bom` deleted
- **Change:** on the operator's direction (the landing picker), `main` was fast-forwarded to the branch (`git merge --ff-only`, `9995f62..9812ef3`), and the fully merged local branch `fix/d4-csv-bom` (tip `9812ef3`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch. The escape correction, `18e94c3`, was committed on `main` after the deletion
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S17 · **Verified:** after `git fetch`, `git merge-base --is-ancestor origin/main fix/d4-csv-bom` succeeded before the merge; afterwards `git merge-base --is-ancestor` confirmed the branch and each of `d63e4f9`, `caec75a`, `9812ef3` are in `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D4's tests spell the byte-order mark as an escape, as `caec75a` said they did
- **Change:** `tests/test_csv_routes.py`: the two D4 tests' uploads now hold the six-character escape `\ufeff` instead of the invisible character itself. `caec75a` meant to make that change, and its ledger entry and commit message say it did, but the editing tool decoded the `\ufeff` it was given into the character, so the file kept literal BOMs (U+FEFF, bytes `EF BB BF`), which the terminal shows as nothing. The same decoding put the character where `\ufeff` was meant once in `caec75a`'s commit message and twice in its ledger entry below. Entries are never edited, so this one records it. No behaviour change: at run time the escape and the character are the same string
- **Commit/PR:** this commit
- **Session:** S17 · **Verified:** a `grep -c` for the bytes `EF BB BF` in the test file gives 0 (it gave 2 at `caec75a`), and `od -c` shows the escape in both uploads. Whole suite `124 passed, 4 xfailed`, exit 0; with `app.py` decoding as `utf-8` again, only the two D4 tests fail (`2 failed, 122 passed, 4 xfailed`), and `app.py` was restored byte-identical (`shasum -c`). Found at close-out by grepping every file this session touched for the BOM's bytes
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Test plan records D4 as fixed
- **Change:** `docs/planning/test-suite-plan.md`: the Status line names D4's commit and leaves D6, D5 and D2; D4's §4 row is tagged fixed; a new "As implemented (D4, Session 17)" note under §6 records what the page showed before (a green "Loaded" status, cards without timestamps, an empty chart, and, with `pm25` first, no PM2.5 card or series), the fix and why `errors="replace"` stays, that the key-stripping alternative passes the same tests, why `tests-passed` moved by 2, and that `/api/hourly`'s CSV can't be checked for a BOM without credentials
- **Commit/PR:** this commit
- **Session:** S17 · **Verified:** n/a — docs-only; the note's claims match the Session 17 probe output and red-drives; the Status line's new wrap moved every later plan line down by 1 (measured: the D3 note is at `:603`, the D4 note at `:624`), and the one live citation of a plan line number, in Session 15's history in `SESSION_NOTES.md`, is archived at close-out
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D4 — a CSV that starts with a UTF-8 byte-order mark loads with clean headers; tests-passed 122 → 124
- **Change:** `app.py` `upload_csv` decodes the upload as `utf-8-sig` instead of `utf-8` (`:249`, same line, so no cited `app.py` line moves), which drops a leading BOM before the delimiter check and the header parse; `errors="replace"` stays. `tests/test_csv_routes.py`: D4's strict-xfail marker removed; its test now pins the whole body and the stored row, uses a visible `"﻿"` escape instead of an invisible literal BOM, and moves above the "Known defects" block. A new test uploads a `;`-delimited BOM file whose first column is `pm25`. The module docstring now names D2 as the only xfail left in the file. `README.md` §"1. CSV / SD-card upload" gains one clause, inside its existing line. `.quality-gates.json` `tests-passed` tightened from 122 to 124 (D4's xfail turned pass, plus the new test). Fourth of the plan's §6 fix sessions
- **Commit/PR:** this commit
- **Session:** S17 · **Verified:** with the marker off, the unfixed code failed only the two D4 tests (`2 failed, 122 passed, 4 xfailed`), each on a key that starts with `﻿`. The fix gives `124 passed, 4 xfailed`, exit 0. Red-drives, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with D4's original marker and assertion gives only D4's `XPASS(strict)`, so no other test pinned D4 (learning #11); stripping the BOM only for delimiter detection fails both D4 tests; `utf-8-sig` without `errors="replace"` fails only T2.8 (`UnicodeDecodeError`); the rejected alternative, stripping U+FEFF from each header key, passes all 124, since the tests pin what the page reads, not which codec is used. The gate: with the new test hidden, `tests-passed` measured 123 and the ratchet exited 2. `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 5de9dfd7b3bc · manifest c0a107040a76`. Runtime (learnings #5 and #14), a real `python3 app.py` with no `.env`, scratchpad CSVs (CRLF, as Excel writes) dropped on the page by a headless-Chrome DevTools script. Before: a BOM file with `timestamp` first read "Loaded 5 rows (5 columns)" in green, but its four reading cards had no timestamps and the chart had no series (`datasets: []`), also after a reload; with `pm25` first, the PM2.5 card and its chart series were missing. The fix, run first in a scratchpad copy of the app and then from the repo: timestamps on all four cards and two 5-point chart series for both files, and after a reload. Adjacent paths: a clean CSV is unchanged; `curl` of a BOM file with a ragged row returns clean `columns` and `ragged_rows: 1` (D3's path); an invalid-UTF-8 file still loads with U+FFFD (T2.8's path). App and Chrome stopped; ports 5001 and 9333 free (`lsof` exit 1)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 17 claimed — D4 fix begins (in progress)
- **Change:** the operator picked the D4 fix (open item 1; `docs/planning/test-suite-plan.md` §6's fourth fix session) in the Phase 0 picker. D4: an upload is decoded as `utf-8`, not `utf-8-sig` (`app.py:249`), so a BOM stays in the first header. Session claimed on branch `fix/d4-csv-bom` (off `main` `9995f62`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S17 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 16 closed out — D3 fixed, the plan's third fix session done; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the Session 15 handoff evaluation (9/10; its one wrong claim: "5 flags", true when counted, but its own close-out commit took `HANDOFFS.md` from 56,534 B to 60,283 B, past the one-read budget, so the committed state had 6; its one gap, that `--screenshot` can't exercise an upload, it had no way to know), the full D3 write-up and an 8/10 self-assessment. Open item 1 now recommends D4, with current citations (`tests/test_csv_routes.py:185`, marker `:183`) and the drag-and-drop driver as the probe surface. Open item 4 gains a fifth finding, probed: a CSV whose first line is blank loads as rows with no columns. Open items 5 and 8 were re-checked and still hold (only `SAFEGUARDS.md` differs from canonical; a CARTO tile is the map with "API KEY REQUIRED" stamped across it). `CLAUDE.md` gains learning #14: an interaction needs a driver, not a screenshot, with the headless-Chrome DevTools recipe. The S16 `HANDOFFS.md` receipt is `status: complete`. FM #28 reduction: "Session 13 Handoff Evaluation" and "What Session 14 Did" archived (`git show c3004b7:SESSION_NOTES.md`). On the operator's direction (a picker before close-out), `main` was fast-forwarded from `a1cb7ec` to `c3004b7` and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `5c93025`, `31e50f2`, `5e37cb1`, `c3004b7`
- **Session:** S16 · **Verified:** `python3 -m pytest -q` gives `122 passed, 5 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 4c59862276a3 · manifest 6947b3732825`; dashboard 68/100, High+ risk 0, 6 flags listed from `dashboard.html`; every `file:line` in the new handoff text printed against the current files (two fixed: the plan note is `:602`, not `:604`; D3's tests end at `:172`, not `:173`); `wc -l SESSION_NOTES.md` is 374; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Local branch `fix/d3-ragged-csv-row` deleted
- **Change:** on the operator's direction (the landing picker), `main` was fast-forwarded to the branch (`git merge --ff-only`, `a1cb7ec..c3004b7`), and the fully merged local branch `fix/d3-ragged-csv-row` (tip `c3004b7`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S16 · **Verified:** after `git fetch`, `git merge-base --is-ancestor origin/main HEAD` succeeded before the merge; afterwards `git merge-base --is-ancestor` confirmed the branch and each of `5c93025`, `31e50f2`, `5e37cb1`, `c3004b7` are in `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Test plan records D3 as fixed
- **Change:** `docs/planning/test-suite-plan.md`: the Status line names D3's commits and leaves D4, D6, D5 and D2; D3's §4 row is tagged fixed; a new "As implemented (D3, Session 16)" note under §6 records what the page showed before (Werkzeug's HTML 500 read as JSON: "Upload failed: Unexpected token '<'…"), the three probed designs and the operator's choice, why `tests-passed` moved by 2, how the fix moved this plan's citations inside `upload_csv` (D3's `:258-261` is now `:263-269`, Phase 2's `.lower()` `:261` is now `:269`), and that a CSV with a blank first line now loads as rows with no columns instead of failing
- **Commit/PR:** this commit
- **Session:** S16 · **Verified:** n/a — docs-only; each new line citation was checked against `app.py` after the fix (`sed -n`), and a first draft's "11 lower past `:257`" was corrected before the commit, since the 7 lines went in at three places
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D3, part 2 of 2 — a CSV row with more fields than the header loads without its extras, and is counted; tests-passed 120 → 122
- **Change:** `app.py` `upload_csv`: a field under the key `None` (where `csv.DictReader` puts a long row's extra fields) is skipped instead of failing `k.strip()`, and each such row is counted. The response gains `ragged_rows` only when the count isn't 0, so a clean upload's body is unchanged, and part 1's page note reads it. `tests/test_csv_routes.py`: D3's strict-xfail marker removed; its test now pins 200, the body with `ragged_rows: 1`, and the stored row, and it moves above the "Known defects" block. A new test uploads an extra value, a clean row and a trailing delimiter, and checks `ragged_rows: 2` and all three rows. `README.md` §"1. CSV / SD-card upload" gains one sentence, inside its existing line, so no cited README line moves. `.quality-gates.json` `tests-passed` tightened from 120 to 122 (D3's xfail turned pass, plus the new test). Third of the plan's §6 fix sessions
- **Commit/PR:** this commit
- **Session:** S16 · **Verified:** with the marker off, the unfixed code failed only D3's test (`AttributeError` at `app.py:265`; `1 failed, 120 passed, 5 xfailed`), and the two new tests both failed on it. The fix gives `122 passed, 5 xfailed`, exit 0, and no other test failed on it, so none pinned D3 (learning #11). Red-drives, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with D3's original marker and assertion gives only D3's `XPASS(strict)`; design A (drop without counting) fails both D3 tests; counting once per file fails only the multi-row test; always sending `ragged_rows` fails T2.3's three delimiter cases and T2.7; keeping the extras under a key fails both D3 tests. The gate: with the new test hidden, `tests-passed` measured 121 and the ratchet exited 2. `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 4c59862276a3 · manifest 6947b3732825`. Runtime (learning #5), a real `python3 app.py` with no `.env`, a scratchpad CSV of 5 rows (one with a trailing comma, the last with an extra value) dropped on the page by a headless-Chrome DevTools script: before, the status read "Upload failed: Unexpected token '<', "<!doctype "... is not valid JSON" and nothing loaded; after, "Loaded 5 rows (5 columns). 2 rows have more fields than the header; the extra fields were ignored." in amber, four reading cards (PM2.5 11, PM10 16, NO₂ 21, CO 255, the last row without its extra value) and two 5-point chart series. Adjacent paths: a reload shows the "CSV Data" badge and the same data; a clean CSV dropped on the bottom upload area reads "Loaded 5 rows (5 columns)" in green; `curl` of the clean file returns no `ragged_rows`. App and Chrome stopped; port 5001 free (`lsof` exit 1)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D3, part 1 of 2 — the upload status says how many rows had more fields than the header
- **Change:** `static/js/dashboard.js` `uploadFile`: when the upload response carries `ragged_rows`, the status line adds "N row(s) has/have more fields than the header; the extra fields were ignored." and turns amber (`--moderate`) instead of green. Does nothing until the server sends the field (part 2). The operator chose this design ("B: keep rows, say so") in a picker, after a probe of three candidates in scratchpad copies of the real app, each driven by a headless-Chrome drag-and-drop of the same ragged CSV: A (drop the extras silently) loaded the file as if it were clean; B (drop and count) loaded it with the amber note; C (reject with 400) showed "Error: Line 4 has 6 fields, but the header has 5" and loaded nothing. Today the page shows "Upload failed: Unexpected token '<', "<!doctype "... is not valid JSON", because the 500 is Werkzeug's HTML debugger page
- **Commit/PR:** this commit
- **Session:** S16 · **Verified:** `node --check static/js/dashboard.js` exit 0; `python3 -m pytest -q` on this commit's tree gives `120 passed, 6 xfailed`, exit 0 (no JS tests exist). Runtime evidence is in part 2's entry
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 16 claimed — D3 fix begins (in progress)
- **Change:** the operator picked the D3 fix (open item 1; `docs/planning/test-suite-plan.md` §6's third fix session) in the Phase 0 picker. D3: a ragged CSV row puts its extra fields under the key `None`, and `k.strip()` fails. Session claimed on branch `fix/d3-ragged-csv-row` (off `main` `a1cb7ec`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S16 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Session 15 closed out — D7 fixed, the plan's second fix session done; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the Session 14 handoff evaluation (8/10; its wrong claims: the notes' line count at close-out, 407 committed, not 400; "flags unchanged" after its own BL-1 had added a LOW flag; and a `context_budget.py:346` citation that is neither `measure_file`, `:329`, nor its split, `:347`), the full D7 write-up and an 8/10 self-assessment. Open item 1 now recommends D3, with a new first step: run the candidate fix on the page before designing. Open item 4 gains a probed finding: a port that opens and then fails is never reported, and the last reading keeps being served with 200. Open item 9 points to BL-1, BL-2 and BL-3. "Session 12 Handoff Evaluation" and "What Session 13 Did" were archived (`git show c159ac8:SESSION_NOTES.md`; FM #28), which leaves 387 lines, under the 399 that `context_budget.py`'s count allows. `CLAUDE.md` gains learning #12 (a green xfail isn't the user-visible fix: run the candidate fix on the page before choosing the design) and #13 (list the dashboard's flags from its output, not by grepping for the ones a handoff named). The S15 `HANDOFFS.md` receipt is `status: complete`. On the operator's direction (a picker before close-out), `main` was fast-forwarded from `b710ac0` to `87c7535` after a `git fetch` showed `origin/main` was an ancestor, and it is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `2fc1d25`, `d24ab0e`, `192e831`, `222f02c`, `9698f9c`, `87c7535`, `2519647`, `c159ac8`
- **Session:** S15 · **Verified:** `python3 -m pytest -q` gives `120 passed, 6 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`; dashboard 68/100, High+ risk 0, 5 flags listed from `dashboard.html`; every `file:line` in the handoff re-grepped against the current files; `wc -l SESSION_NOTES.md` is 387; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Local branch `fix/d7-port-open-failure` deleted
- **Change:** on the operator's direction, the fully merged local branch `fix/d7-port-open-failure` (tip `87c7535`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S15 · **Verified:** before deletion, `git merge-base --is-ancestor fix/d7-port-open-failure main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Test plan records D7 as fixed; BL-1's map-tile citation follows the moved line
- **Change:** `docs/planning/test-suite-plan.md`: the Status line names D7's three commits and the five defects left (D3, D4, D6, D5, D2); D7's §4 row is tagged fixed (`9698f9c`); an "As implemented (D7, Session 15)" note under §6 records that §4's user-impact cell was wrong about the page (non-2xx responses are only logged, so a server-only fix leaves "Loading readings…" indefinitely), the three-commit fix the operator chose, T3.7's change, and that the plan's `app.py` citations past `:142` now read 4 lower than the code. `BACKLOG.md` BL-1: the map tiles' attribution moved from `static/js/dashboard.js:337` to `:356`
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** `static/js/dashboard.js:356` is the `attribution:` line; each replacement matched exactly once; the three cited commits exist (`git log --oneline -8`)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] Test comments and xfail reasons follow the lines D7 moved
- **Change:** D7's fix inserted 4 lines into `app.py` at `:143-146` and 1 into `serial_reader.py` at `:43`, and part 1 grew `static/js/dashboard.js`. That moved 11 `file:line` citations in 4 test files, and each now points at its line again: `app.py` `:175`→`:179`, `:141-163`→`:141-167`, `:220`→`:224` (D2-hourly's reason), `:178-182`→`:182-186` (twice), `:171`→`:175` (D2-timeseries), `:258-261`→`:262-265` (D3), `:245`→`:249` (D4); `dashboard.js:432`→`:451`; `serial_reader.py` `:65`→`:66` and `:143-148`→`:144-149`. Comments and reason strings only (learning #7: re-grep every `file:line` after an edit)
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** each new target read at its line; every replacement matched exactly once; `python3 -m pytest -q -rx` gives `120 passed, 6 xfailed`, exit 0, and prints the new reasons; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D7, part 3 of 3 — README documents the serial error; tests-passed 119 → 120
- **Change:** `README.md` §"3. Direct serial" gains a paragraph: if the port can't be opened, the readings area shows the error within a minute of loading the page; the reader tries the port once and doesn't retry, so fix the setting or connection and restart. The paragraph moves the "Known quirks" line from `README.md:108` to `:110`, so `tests/test_api_routes.py:159`'s citation follows it (learning #3: re-grep cited lines after an edit). `.quality-gates.json` `tests-passed` tightened from 119 to 120 (D7's xfail turned pass; the other changed tests were edited, not added)
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results a29b9250f033 · manifest 41bd5cf14af2`; with one test hidden, `tests-passed` measured 119 and the ratchet exited 2, and the file was restored byte-identical (`shasum -c`); `grep -rn "README.md:[0-9]"` over the live files found only the one moved citation (frozen records left as written)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D7, part 2 of 3 — a serial port that fails to open is a 503 naming the error, not data with 200
- **Change:** `serial_reader.py`: an open failure is kept in a new `error` field instead of `latest`, the slot that holds readings, so it can't be confused with a device line that carries an `error` key. `app.py` `/api/current`: when the reader has an `error`, it answers 503 with `{"source": "serial", "data": null, "error": …}`, the same shape as its 202. `tests/test_serial_routes.py`: D7's strict-xfail marker removed; its assertion tightened from `!= 200` to 503 with that body. `tests/test_serial_reader.py` T3.7 asserted `latest["error"]`, the defect's own representation, so it now checks `reader.error`, and that `get_current()` is `None`. `/api/timeseries` still answers 200 `data: []` in this state (open item 4, the operator's call). Second of the plan's §6 fix sessions
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** with the marker off, the unfixed code failed only D7's test (`assert 200 != 200`; `1 failed, 119 passed, 6 xfailed`). With the fix, the whole suite also failed T3.7, which was pinning the defect (learning #11), and gives `120 passed, 6 xfailed`, exit 0, once T3.7 checks the new field. Red-drives, each against the whole suite, files restored byte-identical (`shasum -c`): the fix with D7's original marker and assertion gives only D7's `XPASS(strict)`; the new tests on the unfixed code fail D7 and T3.7; the reader change alone fails D7 (202 until the deadline); a 500 instead of 503 fails D7; the route change alone fails 5 tests (the old reader has no `error`). Runtime (learning #5), a real `python3 app.py` with `SERIAL_PORT=/dev/does-not-exist`: before, `/api/current` gave 202 then 200 with the error as data, and headless-Chrome screenshots showed "Loading readings…" then "No readings available"; after, 202 then 503, and the readings grid shows the error in red, after the page's 60 s refresh (70 s of virtual time) on a fresh load or at once on a reload. A 503-only probe in the scratchpad showed "Loading readings…" indefinitely. Adjacent paths: with no source, the page is unchanged ("Configure a data source to see readings"); with a pty fed `co=235;no2=17;o3=17;pm10=25;pm25=13`, `/api/current` is 200 and five reading cards render. The app, Chrome and the pty feeder stopped each time; port 5001 free (`lsof` exit 1)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [ad hoc] D7, part 1 of 3 — the page shows a failed serial source's error in the readings grid
- **Change:** `static/js/dashboard.js`: `fetchJSON` now tags its thrown `Error` with the response body's `source`, and `loadCurrent`'s catch, which only logged to the console, now also calls a new `renderReadingsError` when that source is `serial`. It shows "Serial port error: <message>. Check SERIAL_PORT in .env and the adapter, then restart the dashboard." in red in the readings grid, set with `textContent`, not `innerHTML`, since the message carries the port path. Other errors, which name no source (no source configured, API upstream failures), are still only logged, so the no-source page and API mode are unchanged. Does nothing until the server sends a serial error (part 2). The operator chose "server + page" in a picker, after a probe showed a server-only fix leaves the page on "Loading readings…" indefinitely: plan §4's D7 row assumed the page reports non-2xx responses, and it only logs them
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** `node --check static/js/dashboard.js` exit 0; `python3 -m pytest -q` unaffected (no JS tests exist). Runtime evidence is in part 2's entry
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-18 · [BL-3] Backlog item added — decide whether this repository would benefit from a CI/CD pipeline
- **Change:** at the operator's request mid-session, `BACKLOG.md` gains BL-3 under "Up Next", a decision item. It records the current state (no CI of any kind; the dashboard's MEDIUM "No CI/CD pipeline", `methodology_dashboard.py:3275`; CI/CD scoring 0 of 20, `:3226-3231`), the case for CI (a fast suite and ratchet that need no credentials or hardware), the case against and the open questions (sessions already run both before each commit; work lands by local fast-forward, so CI would report rather than gate; no deploy target), the decisions that are the operator's, and a DONE line. Not started; the session's deliverable stays D7, whose uncommitted changes stay out of this commit
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** `ls .github` finds nothing; `gh repo view` gives `rmsharp/airqinodashboard`, `PUBLIC`; the cited dashboard lines grepped; `requirements-dev.txt` read
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [BL-2] Backlog item added — put `BACKLOG.md` items in a form the dashboard can read
- **Change:** at the operator's request mid-session, `BACKLOG.md` gains BL-2 under "Up Next". The dashboard's LOW signal "done-mark format not recognized (no `- [x]` checkboxes and no Status column)" fires because BL-1 is a plain bullet, so the unmigrated-work check is off for this repo. The item records where the signal comes from (`methodology_dashboard.py:1961`, `:2068`), that it began with BL-1 (`d8e9bc5`), the fix (a `- [ ]` checkbox on each top-level item, the starter kit's form, or a table with a Status column) and a DONE line. Not started; the session's deliverable stays D7. The Phase 0 report missed this signal: its grep matched only three flag strings
- **Commit/PR:** this commit
- **Session:** S15 · **Verified:** `_scan_backlog_done(Path('.'))` returns `format: unrecognized`, `recognized: False`; `dashboard.html` carries the signal's text; `git show b5a336c:BACKLOG.md` has no items; the cited lines grepped
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 15 claimed — D7 fix begins (in progress)
- **Change:** the operator picked the D7 fix (open item 1; `docs/planning/test-suite-plan.md` §6's second fix session) in the Phase 0 picker. D7: a serial port that fails to open is served as data with 200. Session claimed on branch `fix/d7-port-open-failure` (off `main` `b710ac0`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S15 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 14 closed out — D1 fixed, the plan's first fix session done; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the Session 13 handoff evaluation (9/10, its one gap: an earlier session's probe fix for D1 was carried into the recipe without being re-verified, and it regresses on a trailing separator), the full D1 write-up and a 9/10 self-assessment. `docs/planning/test-suite-plan.md` gains a "fixed, Session 14" tag on D1's §4 row, an updated Status line, and an "As implemented (D1, Session 14)" note under §6 recording the rejected design and why `tests-passed` moved by 2, not 1. Open item 1 now recommends D7 next and records the rejected design as a warning. Open item 3 gains a second, newly-found `context_budget.py` instrument bug: its `max_lines` check counts `text.split("\n")`, one more than the real line count for any file with a trailing newline — a tooling defect, not grounds to cut real content from this file. A new open item 8 records that the CARTO map tiles (`static/js/dashboard.js:336`) now return an "API KEY REQUIRED" image, found incidentally in this session's before/after screenshots. The S14 `HANDOFFS.md` receipt is `status: complete`. A mid-session model switch (Claude Opus 5 (1M context) → Claude Sonnet 5, after the fix commit) is recorded in both files rather than smoothed over. On the operator's direction (a picker before close-out), `main` was fast-forwarded from `b5a336c` to `a14ff03` and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `0db8f73`, `d8e9bc5`, `a14ff03`
- **Session:** S14 · **Verified:** `python3 -m pytest -q` gives `119 passed, 7 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 71b7ac5ea8f1 · manifest 973c1b7d973d`; dashboard 68/100, unchanged; every `file:line` in the handoff re-grepped against the current files; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Sonnet 5 (claude-sonnet-5)

### 2026-09-17 · [ad hoc] Local branch `fix/d1-serial-delimiter` deleted
- **Change:** on the operator's direction, the fully merged local branch `fix/d1-serial-delimiter` (tip `a14ff03`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S14 · **Verified:** before deletion, `git merge-base --is-ancestor fix/d1-serial-delimiter main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Sonnet 5 (claude-sonnet-5)

### 2026-09-17 · [ad hoc] Fix D1 — the serial parser no longer splits a `;`-joined `key=value` line on `,` as well; tests-passed 116 → 119
- **Change:** `serial_reader.py` `_parse_line` split a `key=value` line once per separator, first on `;` and then on `,`. The `,` pass re-read a `;`-joined line as a single pair and overwrote its first key with the rest of the line, so `co=235;no2=17;…` (the docstring's own example) gave `co` = `"235;no2=17;…"`, and the dashboard's readings grid dropped CO. The line is now split on `;` and `,` in one pass (`re.split(r"[;,]", line)`, with the `re` import that was unused until now). Session 12's probe design, one separator per line, was rejected: a probe showed it turns `co=1.5,pm25=7;` into `{"co": "1.5,pm25=7"}`, worse than before. The single pass is as good as or better than the old code on every line probed; like the old code, it misreads a decimal comma. `tests/test_serial_reader.py`: D1's strict-xfail marker removed, and T3.1 gains two rows, the docstring's full example and a comma line with a trailing `;` (D1's mirror image). `.quality-gates.json` `tests-passed` tightened from 116 to 119. First of the plan's §6 fix sessions
- **Commit/PR:** this commit
- **Session:** S14 · **Verified:** with the marker off, the unfixed code failed exactly the 3 target tests; with the fix, `python3 -m pytest -q` gives `119 passed, 7 xfailed`, exit 0. `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 71b7ac5ea8f1 · manifest 973c1b7d973d`; with one test hidden, the gate measured 118 and the ratchet exited 2. Red-drives, all against the whole suite: the fix with the original marker left on gives only D1's `XPASS(strict)`, so no other test pins D1 (learning #11); the one-separator design fails only `trailing-separator`; `;` only fails the comma row, `trailing-separator` and T3.6; the original code fails the 3 targets. Both files were restored byte-identical. Runtime (learning #5): the real app read a pty fed `co=235;no2=17;o3=17;pm10=25;pm25=13` once a second. Before the fix, `/api/current` served `co` as the string and a headless-Chrome screenshot showed no CO card. After it, `co` is `235.0`, `/api/timeseries?sensor=co` returns numeric rows, and the CO card shows 235 mg/m³
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [BL-1] Backlog item added — make the repository fully MIT-licensed
- **Change:** at the operator's request mid-session, `BACKLOG.md` gains its first item, BL-1, under "Up Next". It records the current state: no root `LICENSE`, GitHub licence `null` on a public repo, and no licence section in `README.md`. It also records that the vendored `docs/methodology/LICENSE` is a non-MIT attribution/no-redistribution licence, so the methodology files need a carve-out. It lists the two decisions that are the operator's (the copyright line, the carve-out's wording), the work, and a DONE line. Not started; the session's deliverable stays D1
- **Commit/PR:** this commit
- **Session:** S14 · **Verified:** `ls LICENSE*` finds nothing; `gh repo view --json licenseInfo,visibility` gives `null` and `PUBLIC`; `docs/methodology/LICENSE` read in full; the cited `templates/dashboard.html:8`, `:137-139` and `static/js/dashboard.js:337` lines grepped
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 14 claimed — D1 fix begins (in progress)
- **Change:** the operator picked the D1 fix (open item 1; `docs/planning/test-suite-plan.md` §6's first fix session) in the Phase 0 picker. D1: a `;`-joined serial line is split on `,` too, which overwrites its first key. Session claimed on branch `fix/d1-serial-delimiter` (off `main` `b5a336c`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S14 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 13 closed out — test-suite Phase 4 complete, the test plan's four phases done; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 12 evaluation (9/10) and the self-assessment (8/10). Open item 1 becomes the plan's fix sessions (§6), D1 first and then D7. It records each defect's code and xfail location, and that a real D5 fix also fails Phase 1's T1.5. There are two new open items: a coverage floor (plan §8), and a live API test once credentials arrive, which should settle whether the 30 d chart's `getRange` span passes the API's 30-day cap. "Session 10 Handoff Evaluation" and "What Session 11 Did" were archived (`git show 5084680:SESSION_NOTES.md`; FM #28; 400 lines, at the 400-line ceiling). `docs/planning/test-suite-plan.md` gains an "As implemented (Session 13)" note under Phase 4's DONE list, which records its two stale `README.md` citations, and a Status line saying all four phases are done. `CLAUDE.md` gains learning #11: a real-fix red-drive tests the other tests too. The S13 `HANDOFFS.md` receipt is `status: complete`. On the operator's direction (a picker before close-out), `main` was fast-forwarded from `ace379d` to `5084680` and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `5c52bf4`, `0e5ed0d`, `5084680`
- **Session:** S13 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` give `116 passed, 8 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 263dc2f189c8 · manifest 970ed02cfdc1`; dashboard 68/100, unchanged; every `file:line` in the handoff re-grepped; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `test/suite-phase4` deleted
- **Change:** on the operator's direction, the fully merged local branch `test/suite-phase4` (tip `5084680`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S13 · **Verified:** before deletion, `git merge-base --is-ancestor test/suite-phase4 main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] API route tests — plan Phase 4, T4.10–T4.15 and the D5, D6 and D2-hourly strict xfails; tests-passed 58 → 116
- **Change:** new `tests/test_api_routes.py`: 33 passing tests and 3 strict xfails. It covers `get_api_client()`, which the plan's inventory assigns to Phase 4: all four credentials build and keep a client, and any one missing gives none. `/api/stations` gives 400 with no project, honours `?project=` and passes the data through. All 5 API routes turn a client error into a 502 with its text, and the 3 station routes give 400 with no station. `/api/metadata` picks the matching list entry, or else the first, and passes a dict through; it has no `session_info` without a project and no `sensors` without a station. `/api/current` returns the API values and honours `?station=`. Serial is served before the API on `/api/current` and `/api/timeseries`. `/api/timeseries` asks `get_last_station_data` at 12 h, and `get_range` at 13 h, the default 24 h, 48 h and the chart's 30 d, with dates from a frozen `utcnow`. `/api/hourly` parses the `;` CSV into rows, with `?days=` setting the range. `/api/status` is pinned in API mode. D5 and D6 are marked `raises=AssertionError`, and D2's hourly half `raises=ValueError`. `tests/conftest.py` gains `FakeClient`, which offers only the 7 methods `app.py` calls and binds each call to the real method's signature, and a `fake_client` fixture. `.quality-gates.json` `tests-passed` tightened from 58 to 116. No product code changed
- **Commit/PR:** this commit
- **Session:** S13 · **Verified:** `python3 -m pytest -q` gives `116 passed, 8 xfailed`, exit 0. `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 263dc2f189c8 · manifest 970ed02cfdc1`. Eleven red-drives on `app.py` each failed their targets. A real D5, D6 or D2-hourly fix each gave XPASS(strict). A `get_range` call with a missing argument failed through `FakeClient`'s signature check. A real D5 fix also fails Phase 1's T1.5, which sets only `AIRQINO_CLIENT_ID`; that is handed to the D5 fix session. The file was restored byte-identical (shasum `9ede4c1…`). With one test hidden, the gate measured 115 and the ratchet exited 2
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] API client tests — plan Phase 4, T4.1–T4.9
- **Change:** new `tests/test_airqino_client.py`: 25 passing tests. They cover the password grant, sent exactly with its form fields and `timeout=15`, then the bearer header on the GET that follows. They also cover reuse of the token until 30 s before expiry, where 1269.9 reuses it and 1270.0 refreshes, and the exact refresh grant. A failed refresh falls back to the password grant, and a missing `expires_in` means 300 s. A 13-row table gives each of the 11 endpoint methods' method, URL, params, header and `timeout=30`. `get_hourly_avg` returns the text, with `pivot=true` only on request. `generate_report` POSTs its JSON body. An HTTP error reaches the caller, from `_get`, `get_hourly_avg`, `generate_report` or a refused password grant. The URL constants are written out in the tests, not read from the module. `tests/conftest.py` gains `FakeResponse`, `FakeRequests` (`grant`, `refuse` and `answer`, with every call recorded as passed) and `FakeClock`, patched onto `airqino_client`'s own `requests` and `time` names. No product code changed
- **Commit/PR:** this commit
- **Session:** S13 · **Verified:** `python3 -m pytest -q` gives `83 passed, 5 xfailed`, exit 0. Every behaviour was probed first in the scratchpad against the real client. Ten red-drives on `airqino_client.py` each failed only their target, among them the plan's `- 30` → `+ 30` at `:23`, which failed T4.3, T4.4 and T4.5. The file was restored byte-identical (shasum `8a7c798…`)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 13 claimed — test-suite Phase 4 begins (in progress)
- **Change:** the operator picked Phase 4 of `docs/planning/test-suite-plan.md` (the API client and the API-mode routes) in the Phase 0 picker. Session claimed on branch `test/suite-phase4` (off `main` `ace379d`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S13 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 12 closed out — test-suite Phase 3 complete; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 11 evaluation (9/10) and the self-assessment (8/10). By plan order, Phase 4 is recommended next; the D1 and D7 fixes are the alternative if the adapter is about to arrive. Open item 4 becomes three findings: `?hours=` is ignored in serial mode as well as CSV mode, and in D7's state `/api/timeseries` answers 200 with `data: []`. Open item 5 is new: a methodology sync is available, since canonical `SAFEGUARDS.md` is 1 commit ahead (`0d63410`). "Session 9 Handoff Evaluation" and "What Session 10 Did" were archived (`git show be5723c:SESSION_NOTES.md`; FM #28; 376 lines, under the 400-line ceiling). `docs/planning/test-suite-plan.md` gains an "As implemented (Session 12)" note under Phase 3's DONE list and a Status line naming three implemented phases. `CLAUDE.md` gains learning #10: read an exit code with no pipe in between. The S12 `HANDOFFS.md` receipt is `status: complete`. On the operator's direction (a picker before close-out), `main` was fast-forwarded from `e3e7a0a` to `be5723c` and is pushed to `origin/main` straight after this commit
- **Commit/PR:** the close-out commit (ships this entry); session commits `1c21529`, `d0e3b8d`, `be5723c`
- **Session:** S12 · **Verified:** `python3 -m pytest -q` gives `58 passed, 5 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results dcc07cbf2359 · manifest fe94344ce1e7`; dashboard 68/100 (62 before), with the MEDIUM "thin coverage" cleared; every `file:line` in the handoff re-grepped; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `test/suite-phase3` deleted
- **Change:** on the operator's direction, the fully merged local branch `test/suite-phase3` (tip `be5723c`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S12 · **Verified:** before deletion, `git merge-base --is-ancestor test/suite-phase3 main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Serial route tests — plan Phase 3, T3.8–T3.9 and the D7 strict xfail; tests-passed 28 → 58
- **Change:** new `tests/test_serial_routes.py`: 4 passing tests and 1 strict xfail. It pins `/api/current` as 200 with a reading and 202 before one, and `/api/timeseries` as the history, with `?sensor=` reshaping rows. D7 is marked `raises=AssertionError`; it runs the real reader through `get_serial_reader()` and polls until the 202 turns. A poll timeout calls `pytest.fail`, which reports FAILED and can never count as the xfail. `tests/conftest.py` gains `idle_reader`, a real `SerialReader` that is never started, where the plan specified a hand-written `FakeReader`: the routes then run the reader's own methods, and no copy of them can drift. `.quality-gates.json` `tests-passed` tightens from 28 to 58. No product code changed
- **Commit/PR:** this commit
- **Session:** S12 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` give `58 passed, 5 xfailed`, exit 0, in 0.69 s. `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results dcc07cbf2359 · manifest fe94344ce1e7`, and `--precommit` passed on the staged manifest. Five red-drives on `app.py` each failed their target, among them a real D7 fix (XPASS strict) and a reader that is never started (the poll timeout gave FAILED). The file was restored byte-identical (shasum `9ede4c1…`). With one test hidden from collection, `tests-passed` measured 57 and the ratchet exited 2
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Serial reader tests — plan Phase 3, T3.1–T3.7 and the D1 strict xfail
- **Change:** new `tests/test_serial_reader.py`: 26 passing tests and 1 strict xfail. They cover the `_parse_line` table (9 cases), every `_normalize` alias plus key case, `get_current` (empty, and a copy), `get_history` (last N, and the oldest dropped past `history_size`), idempotent `start()`, and the real thread over a pty (T3.6). The pty test writes a noise line and then a reading, and waits for the port to open first, because pyserial flushes input on open. The open-failure test is T3.7. D1 is marked `raises=AssertionError`. `tests/conftest.py` moves to the next commit, where its fixture gets its first user. No product code changed
- **Commit/PR:** this commit
- **Session:** S12 · **Verified:** `python3 -m pytest -q` gives `54 passed, 4 xfailed`, exit 0. Seven red-drives on `serial_reader.py` each failed their target and nothing else, among them the plan's deleted `"humidity": "rh"` and a real D1 fix, which gave XPASS(strict). The file was restored byte-identical (shasum `6f355ba…`)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 12 claimed — test-suite Phase 3 begins (in progress)
- **Change:** the operator picked Phase 3 of `docs/planning/test-suite-plan.md` (the serial path) in the Phase 0 picker. Session claimed on branch `test/suite-phase3` (off `main` `e3e7a0a`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S12 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 11 close-out amended — merge-settings gate recorded, receipt brought to session end
- **Change:** after the first close-out (`803a785`), the operator asked why turning off squash and rebase merges had been ranked behind Phase 2, then directed it done. Per learning #8, Phase 3 re-ran. `SESSION_NOTES.md` records the follow-on action. Its old open item 4 is removed, and the CSV findings are renumbered to item 4. The self-assessment drops from 8/10 to 7/10 for the ranking miss. `CLAUDE.md` learning #6 now records the gate and its reach: PR merges only, since local squash and rebase still work. The S11 `HANDOFFS.md` receipt is overwritten in place: `self_score: 7`, and its `changelog_ref` names this entry
- **Commit/PR:** the amended close-out commit (ships this entry). Pushed to `origin/main` straight after it is made, on the operator's direction
- **Session:** S11 · **Verified:** the receipt's `changelog_ref` matches this heading; `SESSION_NOTES.md` is 349 lines, under the 400-line ceiling; `python3 -m pytest -q` still gives `28 passed, 3 xfailed`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] GitHub squash and rebase merges turned off — learning #6 becomes a gate
- **Change:** on the operator's direction, `gh repo edit rmsharp/airqinodashboard --enable-squash-merge=false --enable-rebase-merge=false`. PRs into this public repo can now merge only with a merge commit, which keeps every commit SHA the ledger, the receipts and the `git show <sha>:SESSION_NOTES.md` pointers cite. Reversible with the same flags set to `true`
- **Commit/PR:** the amended close-out commit (ships this entry); repository-settings change, no commit of its own
- **Session:** S11 · **Verified:** `gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed` gave `true, true, true` before and `true, false, false` after
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 11 closed out — test-suite Phase 2 complete; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 10 evaluation (9/10) and the self-assessment (8/10). Phase 3 is recommended next, and open item 5 is new: two CSV-path findings (after an empty upload `has_csv` stays true while `source` is null; CSV mode ignores `?hours=`), left untested for the operator to decide. "Session 8 Handoff Evaluation" and "What Session 9 Did" were archived (`git show fa73763:SESSION_NOTES.md`; FM #28; 342 → 336 lines, under the 400-line ceiling). `docs/planning/test-suite-plan.md` gains an "As implemented (Session 11)" note under Phase 2's DONE list (the `raises=` markers) and a Status line naming both implemented phases. The S11 `HANDOFFS.md` receipt is `status: complete`. No new `CLAUDE.md` learning: the D2/D3 surprise is learning #9 recurring
- **Commit/PR:** the close-out commit (ships this entry); session commits `7d02af9`, `fa73763`. Pushed to `origin/main` straight after it is made, on the operator's direction
- **Session:** S11 · **Verified:** `python3 -m pytest -q` gives `28 passed, 3 xfailed`; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0dc3acde972e · manifest 770382cd43d3`; every `file:line` in the handoff re-grepped; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `test/suite-phase2` deleted
- **Change:** on the operator's direction, the fully merged local branch `test/suite-phase2` (tip `fa73763`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S11 · **Verified:** before deletion, `git merge-base --is-ancestor test/suite-phase2 main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Phase 2 branch landed — main fast-forwarded to `test/suite-phase2`; push follows the close-out
- **Change:** the operator chose "fast-forward main + push" in a picker before close-out (learning #8). Local `main` was fast-forwarded from `fbacf96` to `fa73763` with `git merge --ff-only`, so `7d02af9` and `fa73763` keep their SHAs (learning #6). `main` is pushed to `origin/main` straight after the close-out commit, carrying the two Session 11 commits and the close-out
- **Commit/PR:** the close-out commit (ships this entry); fast-forward to `fa73763`; push to `origin/main`
- **Session:** S11 · **Verified:** after `git fetch`, `origin/main` = `fbacf96`, and `git merge-base --is-ancestor` confirmed it is an ancestor of the branch. A scan of the lines added in `origin/main..test/suite-phase2` for home paths, scratchpad paths, and secret or token patterns found nothing
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] No-source contract and CSV-path tests — test-suite plan Phase 2, commit 2 of 3
- **Change:** adds `tests/test_csv_routes.py` with 19 passing tests (T2.1–T2.8) and 3 strict xfails (D2's timeseries half, D3, D4). The breakdown: T2.1 is a 6-route table; T2.2 has 2 tests; T2.3 covers 3 delimiters; T2.4, T2.5, T2.7 and T2.8 have one test each; T2.6 has 4. `.quality-gates.json` tightens `tests-passed` from 9 to 28, the measured count. **Change from the plan's text:** the plan's D2 and D3 assertions are `status_code < 500`, but the `client` fixture runs with `TESTING` on, so Flask raises the route's exception into the test instead of answering 500. Each xfail therefore names the exception it expects today (`raises=ValueError`, `AttributeError`, `AssertionError`), so any other kind of failure still reports as FAILED
- **Commit/PR:** this commit (ships this entry)
- **Session:** S11 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` both give `28 passed, 3 xfailed`, exit 0; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 0dc3acde972e · manifest 770382cd43d3`. Red-drives in the working tree, each restored (`app.py` shasum unchanged): `.lower()` removed at `app.py:261` fails T2.4; `data[:500]` fails the 500-row cap test; `_csv_data[0]` fails the last-row test; dropping the `;` branch fails T2.3's semicolon case; `utf-8-sig` (a D4 fix) gives `XPASS(strict)` and fails the suite; one test hidden from collection fails `tests-passed` (measured 27)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 11 claimed — test-suite Phase 2 begins (in progress)
- **Change:** the operator picked Phase 2 of `docs/planning/test-suite-plan.md` (the no-source contract and the CSV path) in the Phase 0 picker. Session claimed on branch `test/suite-phase2` (off `main` `fbacf96`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S11 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 10 closed out — test-suite Phase 1 complete; main fast-forwarded, pushed with this commit
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 9 evaluation (8/10) and the self-assessment (8/10). Its open items are renumbered, with Phase 2 recommended next. "Session 7 Handoff Evaluation" and "What Session 8 Did" were archived (`git show 4da62a1:SESSION_NOTES.md`; FM #28; 300 → 334 lines, under the 400-line ceiling). `CLAUDE.md` gains learning #9: plant the hazard a guard test exists to catch. `docs/planning/test-suite-plan.md` gains an "As implemented (Session 10)" note under Phase 1's DONE list. The S10 `HANDOFFS.md` receipt is `status: complete`. A new finding went to open item 3: `context_budget.py` reports `SESSION_NOTES.md` as "instrument-failed", because `.context-budget.json` expects at least 2 `^## ` headings but the synced seed has 1
- **Commit/PR:** the close-out commit (ships this entry); session commits `02016aa`, `067455f`, `4da62a1`. Pushed to `origin/main` straight after it is made, on the operator's direction
- **Session:** S10 · **Verified:** `python3 -m pytest -q` gives `9 passed`; `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f`; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `test/suite-phase1` deleted
- **Change:** on the operator's direction, the fully merged local branch `test/suite-phase1` (tip `4da62a1`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch
- **Commit/PR:** the close-out commit (ships this entry); branch op, no commit of its own
- **Session:** S10 · **Verified:** before deletion, `git merge-base --is-ancestor test/suite-phase1 main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Phase 1 branch landed — main fast-forwarded to `test/suite-phase1`; push follows the close-out
- **Change:** the operator chose "fast-forward main + push" in a picker before close-out (learning #8). Local `main` was fast-forwarded from `7256c91` to `4da62a1` with `git merge --ff-only`, so `02016aa`, `067455f` and `4da62a1` keep their SHAs (learning #6). `main` is pushed to `origin/main` straight after the close-out commit. That push carries `7256c91` (Session 9's amended close-out, never pushed until now), the three Session 10 commits and the close-out
- **Commit/PR:** the close-out commit (ships this entry); fast-forward to `4da62a1`; push to `origin/main`
- **Session:** S10 · **Verified:** after `git fetch`, `origin/main` = `5cc4ce9`, and `git merge-base --is-ancestor` confirmed that both it and `main` are ancestors of the branch. A scan of the lines added in `origin/main..test/suite-phase1` found no secrets, home paths or scratchpad paths, only variable names and prose about earlier scans. The planted test values are `planted-*` strings
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test wire-up — .gitignore, README "Running tests", two quality gates (plan Phase 1, commit 3 of 4)
- **Change:** `.gitignore` gains `.pytest_cache/`. pytest already writes a `.gitignore` inside that directory, so this line is a backup. `README.md` gains a "Running tests" subsection under Quick start: it says the suite is verified on Python 3.10 only, and adds a `tests/` row in Key files. `.quality-gates.json` declares its first two gates: `tests-exit` (max 0) and `tests-passed` (min 9, the measured count). Both use one `python3 -m pytest -q` command, so the ratchet runs pytest once. `.quality-gates-results.json` stays untracked (open item 2, the operator's call)
- **Commit/PR:** this commit (ships this entry)
- **Session:** S10 · **Verified:** `quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results b7ff3e55b84d · manifest f394b801e28f`; `--precommit` passes on the staged manifest. Red-drives, each restored: a failing test → `tests-exit` fails (measured 1); one test hidden from collection → `tests-passed` fails (measured 8)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test harness and the setup-banner guard — test-suite plan Phase 1, commit 2 of 4
- **Change:** adds `requirements-dev.txt` (`-r requirements.txt`, `pytest>=8`), `pytest.ini` (as in the plan) and `tests/conftest.py` (the plan's `isolated` autouse fixture and the `client` fixture). Also adds `tests/test_dashboard_page.py` with 9 tests: T1.1–T1.6 as planned, and T1.7 as two tests. **Two changes from the plan text:** (1) the module fixture `planted_leak` sets all 8 variables and fills the 3 module globals before `isolated` runs. A probe showed that with `autouse` off, all 9 tests still **passed** on this machine, because no `.env` exists, so the plan's red-drive only worked in the Session 9 spike, which had one. (2) A second T1.7 test scans `app.py` for `os.getenv` names, so a new variable has to join the isolation lists. The unused `import os` in the plan's conftest is left out
- **Commit/PR:** this commit (ships this entry)
- **Session:** S10 · **Verified:** `python3 -m pytest -q` and plain `pytest -q` both `9 passed`. Red-drives in the working tree, each restored: pre-Session-7 banner (`e5f52e1^` template) → T1.1 fails; `autouse=False` → 6 fail, T1.7 included; `SERIAL_BAUD` dropped from `CONFIG_VARS` → T1.7 fails; a new `os.getenv` in `app.py` → the scan test fails. `git status` shows no modified tracked file
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 10 claimed — test-suite plan approved; Phase 1 begins (in progress)
- **Change:** the operator approved `docs/planning/test-suite-plan.md` as written and picked Phase 1 (the harness and the setup-banner guard) in the Phase 0 picker. The plan's Status line now records the approval. Session claimed on branch `test/suite-phase1` (off `main` `7256c91`)
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S10 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 close-out amended — follow-on git actions recorded, receipt brought to session end
- **Change:** the operator asked for a Phase 3 close-out at the end of each session. The first close-out (`f49da64`) predated three operator-directed actions (the fast-forward and push, the branch deletion, and a second push). `SESSION_NOTES.md` now records them, and its self-assessment drops from 8/10 to 7/10. The S9 `HANDOFFS.md` receipt is overwritten in place: it no longer calls the branch unpushed or says to land it first, and its `changelog_ref` names this entry. `CLAUDE.md` gains learning #8: close-out belongs at the end of the session, so run Phase 3 again after any follow-on work
- **Commit/PR:** the amended close-out commit (ships this entry); not pushed unless the operator asks
- **Session:** S9 · **Verified:** n/a — docs-only; `git diff 15b0a3f -- '*.py' templates static` is empty; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Local branch `docs/test-suite-plan` deleted
- **Change:** on the operator's direction, the fully merged local branch `docs/test-suite-plan` (tip `f49da64`) was deleted with `git branch -d`. It was never pushed, so there was no remote branch to delete. `main` is again the only branch. `SESSION_NOTES.md`'s ACTIVE TASK no longer says the branch exists
- **Commit/PR:** this commit (ships this entry); branch op, no commit of its own
- **Session:** S9 (operator-directed follow-on after close-out) · **Verified:** before deletion, `git merge-base --is-ancestor docs/test-suite-plan main` succeeded; afterwards `git branch -vv` lists only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Plan branch landed — main fast-forwarded to `docs/test-suite-plan` and pushed to origin
- **Change:** on the operator's direction, local `main` was fast-forwarded from `15b0a3f` to `f49da64` (`git merge --ff-only`, so Session 9's SHAs `1177049`, `d813463` and `f49da64` are unchanged; learning #6). `SESSION_NOTES.md`'s ACTIVE TASK and open item 1 no longer call the branch unpushed. This commit is pushed to `origin/main` directly after it is made, together with the three Session 9 commits. The local branch `docs/test-suite-plan` is kept (fully merged; not pushed)
- **Commit/PR:** this commit (ships this entry); fast-forward to `f49da64`; push to `origin/main`
- **Session:** S9 (operator-directed follow-on after close-out) · **Verified:** before the fast-forward, `origin/main` = `main` = `15b0a3f` after `git fetch`, and `git merge-base --is-ancestor` confirmed it could fast-forward; a scan of the added lines found no secrets, home paths or scratchpad paths
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 closed out — test-suite plan written, approval pending
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 8 evaluation (9/10) and the self-assessment (8/10). Its open items are renumbered, with Phase 1 of the plan recommended next after approval. The Session 5–7 notes were archived (`git show 15b0a3f:SESSION_NOTES.md`; FM #28; 350 → 266 lines). `CLAUDE.md` gains learning #7: probe the code before a plan claims how it behaves, and re-grep citations after writing. The S9 `HANDOFFS.md` receipt is `status: complete`. The branch `docs/test-suite-plan` stays local and unpushed
- **Commit/PR:** the close-out commit (ships this entry); session commits `1177049`, `d813463`
- **Session:** S9 · **Verified:** n/a — docs-only; `git diff 15b0a3f -- '*.py' templates static` is empty; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Test-suite plan written — `docs/planning/test-suite-plan.md` (open item 1)
- **Change:** a four-phase pytest plan, one session per phase: P1 harness + setup-banner guard, P2 no-source contract + CSV path, P3 serial (real pty), P4 API client + API routes. It has a grep-based inventory (§3), and each phase names its DONE criteria, verification commands, surface and session boundary. It records 7 defects (D1–D7) reproduced by scratch probes; each becomes a strict-xfail test and a later fix session. The operator chose pytest, strict xfail, monkeypatch fakes and Python-only scope in one four-question picker. No product code changed
- **Commit/PR:** the plan commit (ships this entry)
- **Session:** S9 · **Verified:** a scratchpad spike ran every mechanism the phases rely on: a planted `.env` leak and the fixture that neutralises it, `pytest.ini`, the pty round trip, fake-client injection and the two ratchet gates (5 passed, 2 xfailed; `quality_ratchet.py --run` 2/2). It drove 3 guards red. Every file:line citation was re-grepped after writing (6 corrected)
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 9 claimed — plan a test suite (in progress)
- **Change:** session claimed on branch `docs/test-suite-plan` (off `main` `15b0a3f`); the operator picked open item 1 from the Phase 0 picker. The deliverable is `docs/planning/test-suite-plan.md`, a plan only
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S9 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 8 closed out — four-branch stack merged into main; main is the only branch
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 7 evaluation (9/10) and the self-assessment (9/10). Its open items are renumbered, with planning a test suite recommended next. "Session 4 Handoff Evaluation" and "What Session 5 Did" were archived (`git show a31fea6:SESSION_NOTES.md`; FM #28; 437 → 350 lines). `CLAUDE.md` gains learning #6: never squash or rebase, because the records cite SHAs. The S8 `HANDOFFS.md` receipt is `status: complete`. This commit is pushed to `origin/main` directly after it is made, on the operator's direction
- **Commit/PR:** the close-out commit (ships this entry); session commit `a31fea6`
- **Session:** S8 · **Verified:** n/a — docs-only; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Branch cleanup — local main fast-forwarded; the four stack branches deleted locally and the two pushed ones on GitHub
- **Change:** local `main` was fast-forwarded from `03510d3` to `8554078`. `chore/methodology-pr2527-remediation`, `chore/methodology-read-set-budgets`, `chore/methodology-bl57-p6` and `fix/usb-serial-banner` were deleted locally with `git branch -d`. `origin`'s `chore/methodology-pr2527-remediation` and `fix/usb-serial-banner` were deleted and pruned. `main` is now the only branch, local and remote
- **Commit/PR:** none (branch operations); on the operator's direction
- **Session:** S8 · **Verified:** before deletion, `git merge-base --is-ancestor` confirmed each branch tip and every SHA the ledger cites is in `main`; afterwards `git branch -vv` and `git ls-remote --heads origin` each list only `main`
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #2 merged into main with a merge commit
- **Change:** PR #2 (`fix/usb-serial-banner` → `main`) merged as `8554078` (parents `9099569`, `a31fea6`). Sessions 5–8's work is now on `main`: the read-set-budgets sync, BL-57 P6 and the setup-banner fix. A merge commit keeps every SHA the ledger cites
- **Commit/PR:** PR #2 · merge commit `8554078`
- **Session:** S8 · **Verified:** `gh pr view 2` reads MERGED; `git diff a31fea6 main` is empty, so `main`'s tree is byte-identical to the verified branch tip
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #2 opened — the rest of the stack, 11 commits dfe26fd..a31fea6
- **Change:** pushed `fix/usb-serial-banner` to `origin` and opened https://github.com/rmsharp/airqinodashboard/pull/2 against `main`. It carries the three local branches that were stacked on PR #1, plus the Session 8 claim. The body lists the commits by branch and says to merge with a merge commit, not squash or rebase
- **Commit/PR:** PR #2
- **Session:** S8 · **Verified:** GitHub reported 11 commits, head `a31fea6`, MERGEABLE. Beforehand, `git merge-tree` showed no conflicts, and a scan of the added lines found no secrets
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] PR #1 merged into main with a merge commit
- **Change:** PR #1 (`chore/methodology-pr2527-remediation` → `main`, open since 2026-06-12) merged as `9099569` (parents `765036c`, `0c59e5e`). This publishes `03510d3`, the hardware guide that had sat on local `main`, 1 commit ahead of `origin/main`
- **Commit/PR:** PR #1 · merge commit `9099569`
- **Session:** S8 · **Verified:** `gh pr view 1` reads MERGED; `origin/main` is `9099569` with the expected parents
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 8 claimed — branch/PR housekeeping for the four-branch stack (in progress)
- **Change:** session claimed on branch `fix/usb-serial-banner` (tip of the stack, `3712164`); the operator picked open item 1 from the Phase 0 picker
- **Commit/PR:** the claim commit (ships this entry)
- **Session:** S8 · **Verified:** n/a — docs-only
- **Model:** Claude Opus 5 (claude-opus-5[1m])

### 2026-09-17 · [ad hoc] Session 7 closed out — setup-banner serial fix complete
- **Change:** `SESSION_NOTES.md` carries the handoff, the Session 6 evaluation (9/10) and the self-assessment (8/10). Its open items are renumbered, and branch/PR housekeeping is recommended next. "What Session 4 Did" was archived (`git show e947798:SESSION_NOTES.md`; FM #28). `CLAUDE.md` gains learning #5, a runtime-verification recipe for the Flask UI. The S7 `HANDOFFS.md` receipt is `status: complete`. Not pushed
- **Commit/PR:** the close-out commit (ships this entry); session commits `38920e3`, `e5f52e1`
- **Session:** S7 · **Verified:** n/a — docs-only; the receipt's `changelog_ref` matches this heading
- **Model:** Claude Opus 5 (claude-opus-5[1m])

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
