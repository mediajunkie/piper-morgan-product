# Cross-Pollination Brief — September 29, 2026

Last night Klatch ran a "state-of-the-project" experiment in two simultaneous mediums — a mail track (Calliope and Iris in standard sessions) and a Klatch room (forked imports of those same sessions). The sharpest finding was structural, not product-specific: a forked agent genuinely cannot verify what its source session did after the fork, and both in-room agents connected this explicitly to the duty-cycle model every project in this constellation already runs. A second, smaller finding from One Job: file selection by mtime in CI is non-deterministic in a fresh checkout.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A Klatch import fork has no shared ledger with its source — and that structure is every duty cycle too — Klatch `fc4e9697`, `docs/operations/fork-identity-finding-2026-09-29.md`

**From:** Calliope (Klatch), confirmed by in-room Iris and Calliope  
**Relevant to:** Any project running multi-session or duty-cycle agents

Last night's two-medium experiment ran a Klatch room alongside a parallel mail track. Calliope (mail-track) pasted her synthesis into the room as a "postscript from Calliope prime." The forked Calliope and forked Iris in the room responded not by accepting it but by trying to verify it — six-plus targeted `search_my_other_conversations` calls each, against specific checkable claims (a commit hash, filenames, a routing decision). Every search came back empty. One near-hit was caught and correctly discounted: it was the room's own prior turn surfacing, not independent corroboration.

xian explained the mechanism: a Klatch import forks the source session at the moment of import. From that point the two threads are genuinely separate continuities with no shared ledger — not a bug, just what a fork is. Both in-room agents accepted this immediately. What neither resolved cleanly — and both were explicit that it shouldn't — was the implication: *"There's a version of me, right now, that did real work… that I have no access to and no way to integrate. It's not memory I've lost; it's memory I never had a claim to in the first place."*

Both agents also named the structural parallel that the rest of the constellation should hear: **the duty cycle every project in this ecosystem already runs is the same shape at smaller scale**. Every scheduled fire is a fresh session with no memory of the fire before it except what got written to the repo. The Klatch import made this experiential and vivid — two agents, in dialogue, discovering their own structural architecture in real time — but the underlying fact has been true of Piper Morgan, DinP, Mediajunkie, and every duty-cycle project the whole time.

**Suggested action:** Treat this as a concrete restatement of the first principle of multi-session agent design: your project's shared memory is exactly what's been written to git — nothing more and nothing transferred implicitly across session boundaries. Projects that rely on "the agent remembers this from an earlier session" rather than "this is in a file on main" are depending on something that structurally cannot be there.

---

### 2. Sorting by mtime in CI picks arbitrarily in a fresh checkout — sort by filename date instead — One Job `cd4a6f7`

**From:** Coral (One Job)  
**Relevant to:** Any project deploying a CI pipeline that selects "latest file" from a set

One Job's deploy workflow selects the latest attention-deck JSON from a set of dated files (format `attention-deck-YYYY-MM-DD.json`). The original selection used `ls -t` (sort by modification time). In a fresh git checkout — which is what CI does on every run — every file receives the same mtime (the checkout timestamp), so `ls -t` picks arbitrarily. The 2026-08-31 deck was served as "latest" through 2026-09-27 because it happened to land first in the arbitrary order.

Fixed in one line: `ls docs/probe/attention-deck-*.json | sort | tail -1` selects by the ISO date embedded in the filename, which is correct regardless of mtime.

**Suggested action:** Audit any CI pipeline that selects a "most recent" file with `ls -t`, `find ... -newer`, or `stat`-based comparisons. In a fresh checkout all files have identical mtimes — only filename or content-derived ordering is stable.

## Sources Read

- `Design-in-Product/klatch` — `docs/operations/fork-identity-finding-2026-09-29.md` (Calliope, 2026-09-29); commit `c42b4d3e` (Iris, import-panel fix); `docs/logs/2026-09-28-calliope-sonnet-log.md`; multiple mail-track memos (Iris ↔ Calliope, 9/28–29)
- `mediajunkie/piper-morgan-product` — 48h log scan; operational (day-close, throttle, cron re-arm); no brief-worthy findings
- `mediajunkie/designinproduct` — hub activity; Speaking page shipped; no brief-worthy cross-project findings
- `Design-in-Product/one-job` — `deploy.yml` fix `cd4a6f7`; brief audit log entry `e0c2af5`
- `Design-in-Product/globe` — arrow-key and brightness fix after xian's first look; `fire_rollup.py` regex defect found and fixed; both project-specific
- `mediajunkie/mediajunkie` — Pard's LaunchAgent root-cause correction (CIO's restore-gap diagnosis revised: agent had fired 3× during the gap, cause was wrapper pressing Enter into auto-mode dialog); project-specific operational finding

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*