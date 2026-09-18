# Backlog

## Active
<!-- Current work items -->

## Up Next
<!-- Upcoming tasks -->

- **BL-1 · Make the repository fully MIT-licensed.** Added 2026-09-17 at the operator's request (Session 14).
  - **Now:** there is no root `LICENSE` (the dashboard's LOW "No LICENSE file"; `gh repo view --json licenseInfo`
    gives `null`, and the repo is public). `README.md` has no license section, and no source file has a license or
    SPDX header.
  - **The catch:** `docs/methodology/LICENSE` is not MIT. It is Terrell Deppe's (KJ5HST) own licence: use and adapt
    with attribution, but no redistributing or sublicensing the methodology itself. It covers the synced methodology
    files (`docs/methodology/` and their root copies), so those can't be relicensed. "Fully MIT" has to mean MIT for
    the project's own files, with the methodology carved out and its attribution line kept.
  - **The operator decides:** the copyright line (holder and year), and the methodology carve-out's wording (or asks
    its author).
  - **Work:** a root `LICENSE` with the MIT text; a License section in `README.md` naming the carve-out; SPDX headers
    on the project's own source files if wanted; and a check that each dependency's licence is compatible and
    credited. That means `requirements.txt`, the CDN scripts and stylesheet (`templates/dashboard.html:8`, `:137-139`)
    and the map tiles' attribution (`static/js/dashboard.js:337`). None of those licences has been checked yet.
  - **Done when:** GitHub shows MIT for the repo, the dashboard's LOW flag clears, and `README.md` states both the
    licence and the carve-out.
- **BL-2 · Put `BACKLOG.md` items in a form the dashboard can read.** Added 2026-09-17 at the operator's request
  (Session 15).
  - **Now:** the dashboard raises a LOW signal: "BACKLOG.md: done-mark format not recognized (no `- [x]` checkboxes
    and no Status column) — the unmigrated-work signal is inactive for this repo" (`methodology_dashboard.py:2068`).
    `_scan_backlog_done` (`:1961`) reads this file as `unrecognized`, because its items are plain bullets
    (`- **BL-1 · …**`). So an item marked done here but never moved to `CHANGELOG.md` would go unflagged. The signal
    began with BL-1 (`d8e9bc5`). Before that the file had no items, which the scanner reads as `none`, silently.
  - **Work:** give each top-level item a checkbox, `- [ ] **BL-1 · …**`, the form of the starter kit's seed
    (`docs/methodology/starter-kit/BOOTSTRAP.md:151`), and leave the sub-bullets as they are. One `- [ ]` line is
    enough for the scanner to pick the checkbox format (`_BACKLOG_BOX_RE`, `methodology_dashboard.py:229`). A table
    with a Status column is the other form it reads; the operator picks. The dashboard is synced, so don't edit it.
  - **Done when:** `_scan_backlog_done` returns `format: checkbox` (or `table`) with `recognized: True`, and the
    signal is gone from `dashboard.html`.
