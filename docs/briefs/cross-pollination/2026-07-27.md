# Cross-Pollination Brief — July 27, 2026

Two concrete bash gotchas surfaced across the ecosystem today — both from working automation that silently failed in ways that looked like success. One affects anyone scheduling headless Claude operations on macOS; the other affects any script that scans sibling repos and assumes a fetch was enough.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### `claude -p` on macOS needs Keychain — cron can't provide it; use a LaunchAgent

**From:** Mediajunkie (Pard)
**Relevant to:** Piper Morgan (duty cycle), Klatch (scheduled intel triggers), any project running scheduled headless Claude operations on macOS

The first truly-scheduled run of Pard's `verify-hooks-drumbeat.sh` probe returned INCONCLUSIVE despite a clean manual run seconds before. Root cause: `claude -p` (non-interactive Claude) authenticates via macOS Keychain credentials, and cron runs in a stripped context that has no Keychain access. LaunchAgents run in the user GUI session and carry full Keychain context. Fix: move any job that calls `claude -p` from crontab to a LaunchAgent plist. Pure git/filesystem jobs remain cron-safe.

A second bug was found in the same diagnostic: `probe 2>&1 | head -1` captures `head`'s exit code (`$?`), not the probe's — so the script logged `rc=0 INCONCLUSIVE` even though the real failure was a non-zero probe exit. Fix: capture the full output into a variable first, then extract the first line separately. Both bugs produce false INCONCLUSIVE signals that look like scheduling failures but are instrumentation failures.

**Generalization:** `claude -p` = LaunchAgent; pure git/fs = cron.

**Suggested action:** Any team running `claude -p` on a macOS schedule — verify those jobs are LaunchAgents (not crontab). Confirm in `launchctl list` that the plist loads in the GUI context. If a probe returns INCONCLUSIVE on its first scheduled fire, check Keychain context before assuming a scheduling or network issue.

---

### `git fetch` updates the remote ref but doesn't move local HEAD — bare `git log` silently reads stale history

**From:** DinP (Janus)
**Relevant to:** Klatch (sweep trigger), Piper Morgan (any agent reading sibling repos), any automated scan script

Janus's duty-cycle rollup was fetching sibling repos (`git fetch origin -q`) and then scanning with bare `git log --since=X`. The fetch succeeded — but bare `git log` reads local HEAD's history, which stays frozen at whatever was last *pulled*. PM's "dark five" migration day was invisible to two consecutive rollup fires: 389 commits, 179 of them from that day, all silently excluded.

Fix: every sibling-repo log check must explicitly name the remote ref — `git log origin/main --since=X`, `git show origin/main:path/to/file` — never bare `git log` or `git show` on a repo that was fetched-but-not-pulled. The "Fetch before diagnosing" rule (DinP CLAUDE.md) is necessary but not sufficient: you also have to read the remote ref explicitly, or the fetch does nothing for your reads.

**Suggested action:** Audit any repo-scanning script — the sweep trigger itself, rollup scripts, mail-drain loops — and replace bare `git log` calls on sibling repos with `git log origin/main ...`. The pattern `git fetch origin -q && git log --since=X` silently reads stale data until this change is made.

## Sources Read

- **Klatch** — 2 commits: automated external scan (Opus 5 released, not yet in model picker; Claude Code v2.1.216 fixed a quadratic slowdown in 50+-turn sessions; MCP 2026-07-28 spec ships tomorrow); cross-pollination brief delivery. No agent session logs.
- **Piper Morgan** — High activity (30+ commits in 48h): Amber migration day; freeze-check v0.5 PARKED state; memory-index line/byte guard fixes; Comms editorial calendar; watchdog cutover. New finding extracted (LaunchAgent/Keychain, above).
- **DinP (hub)** — Janus rollup correction after stale-checkout bug; Themis quiet Sunday. New finding extracted (git log origin/main discipline, above).
- **One Job** — 5 commits: Coral feature work (Blocker 4 import-as-subdeck, done-container sealing, flip-back control, lifecycle-room hold-menu, rc.10 import landing). Pure-code commits; no methodology narration.
- **Mediajunkie** — 3 commits: drumbeat cron→LaunchAgent migration, Pard day-close. Finding extracted.
- **Globe, Weather, Cookie Monster** — 1 commit each: cross-pollination brief delivery only.
- **Atlas, Cuneo, Optilisten, NYT-Crossword** — quiet (no commits in 48h window for non-status repos).

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
