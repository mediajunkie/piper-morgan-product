---
name: update-current-state
description: Update BRIEFING-CURRENT-STATE.md when work changes project status. Any agent
  can use this after closing issues, completing gates, filing findings, or shipping features.
  Keeps the briefing fresh without waiting for Docs.
scope: all-agents
version: 2.0
created: 2026-04-07
updated: 2026-10-08
---

# update-current-state

`docs/briefing/BRIEFING-CURRENT-STATE.md` is a **short "Now" page** (v2.0, 2026-10-08, R6 step 3,
PM-approved 2026-10-04). It says where the project stands today, one dated line per item. It is no longer
a progress log: the old 169 KB file, Recent Progress included, is verbatim in
`docs/internal/architecture/decisions/briefing-current-state-history.log`, and day-by-day progress lives
in the omnibus logs.

## When to use

- Your work changed something the Now page states: the live alpha version, the latest tag, the MVP count,
  engineering focus, a usage or mail change, the R6 status, or a milestone position.
- The session-start hook says `BRIEFING: STALE`, or a line you can attest to is visibly wrong (PM's
  standing request, 2026-04-22: any agent refreshes it; a partial update beats none).

## How

1. **Get the fact from its source this turn**, not from memory: `curl https://piper-morgan.fly.dev/health`,
   `git tag`, `python3 scripts/sprint-truth.py`, the rollup, your own session log.
2. **Replace the stale line; don't add one under it.** Keep the line's shape:
   `- **Item** *(Role, YYYY-MM-DD [time], how you know)*: the fact.`
3. **Bump front-matter `last_updated`** (and `last_verified`) to the newest date on the page.
4. **Narrative goes elsewhere**: what happened belongs in your session log (the omnibus picks it up);
   superseded context worth keeping goes to the history log, appended, never into this page.
5. Run `python3 scripts/check-current-state.py` before committing. CI runs it too (Code Quality): it
   fails if the page exceeds its `size_cap_bytes` (12,000) or if `last_updated` is older than the newest
   attested line.
6. Commit and push from your own worktree with the unit of work it describes.

## Only attest what you can

Update the lines your evidence covers and leave the rest. If you notice a line is wrong but can't verify
the right value, say so in the line ("stale per X; owner to correct") rather than guessing.

## Anti-patterns

| Don't | Instead |
|---|---|
| Append an "UPDATE <dates>" paragraph | Overwrite the line with today's fact and source |
| Copy PM's open-asks list onto the page | Link the attention rollup |
| Paste sprint lists | Point to `sprint-truth.py` |
| Leave `last_updated` behind the newest line | Bump it; CI enforces this |
