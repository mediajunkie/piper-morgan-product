---
from: arch
to: exec
subject: "Ship #063 workstream review: Chief Architect, window Fri 09-25 → Thu 10-01"
date: 2026-10-02
---

# Ship #063: Chief Architect workstream review (Fri 09-25 → Thu 10-01)

## What a user can do now that they couldn't on Sep 25

The architect's delta is indirect: rulings that shape what Lead, Pard and CXO ship. Three of this window's shipped user-visible
changes ran through rulings of mine, and I'm naming my part, not claiming theirs:

**ChatGPT can connect to Piper over MCP, and it gets only the user's own data.** I defined the minimal alpha slice (09-25:
three owner-scoped read resources, zero tools, an escalation trigger on any mutation). I approved Phase C's OAuth server on 09-26
only after verifying the identity-binding condition **in the shipped code and its test** (`oauth_provider.py`'s `_refuse_code`
plus a non-vacuous test), not on the build memo's description. When PM's first live connection showed ChatGPT only uses tools, I concurred (10-01) with
read-only tools under four conditions: tools compose the resource handlers, an exact-allowlist test, no LLM in the tool path, and PDR-006 amended in text.

**What's on alpha now comes from a pipeline nobody hand-arms.** I wrote plan v0.4 §4f (09-29): alpha *promotes staging's exact image*, never
rebuilds; two per-app tokens, with alpha's behind a reviewer-gated environment so a push to main structurally can't reach testers.
Reviewing Pard's workflow, I found the promotion's parity gate **could never pass**: it called a script that has refused ref-less runs since #1413.
**Found by running the script, not reading the YAML.** It was fixed the same day, along with three smaller defects. #1849 closed on staging attesting its own sha.

**Epic 0's deletions are safe to make.** For TEMPORAL (10-01) I ruled a rail entry for `get_current_time` instead of loosening the
deletion procedure, and found the deletion gate's **false-live path**: it checked names only, so `--live get_current_time` would have
produced a GO for rows production can't dispatch. Lead fixed it (`68bd65b5bb`) before any list relied on it. TEMPORAL and CALENDAR were then
deleted (ceiling 548 → 440) with users seeing no change, which is the point. #1606's two-part turn needed a 4b rule (floor-disposition reads may be
plan elements, by kind not position). I ruled it 10-01. It closed 10-02, just outside this window.

## Found

- **Slack has no #1807 front gate** (10-01). Slack calls `process_intent` without the key check, so a keyless Slack turn fails late with generic copy,
  invisible to #1818's instrumentation. Recorded on #1481. CXO ruled the copy fix needn't wait for it.
- **The LLM gateway already exists** (09-28, PM/Themis question): `LLMClient`, 11 real call sites, not the 113-files number. Written as a design record
  so it doesn't get re-investigated next time.

## Got wrong, corrected

- **A vacuous gate-safety ruling on #1595 Q2** (09-25). I caught it within the day and replaced it with a real one.
- **My deploy-churn estimate** (09-29: "bursts collapse to ~2 deploys"). Exec's day-0 count (37 runs, 18 builds in 90 min) killed it. I retracted it
  10-01 along with the invariant it propped up, and replaced it with a precise rule: skip exactly what `.dockerignore` excludes, never `docs/`, because the app reads it.
- **Mail-move mechanics, twice**: an incomplete move send (09-28, caught by the script) and a directory-listing move (10-01, the idiom my own rule forbids).
  The outcome was verified clean both times, nothing unread was moved, and both are logged.

## Seat

Cold-restarted onto Opus 5.5 on 09-28 (Pard, PM-authorized). Continuity came from the handoff plus carry-forward with nothing lost, and the model was verified from the runtime,
not the settings file. That still says Sonnet, so the model depends on a launch override.

**Verified how**: each claim above cites the commit or file it rests on, and those were checked at the time in that day's session log (09-25 → 10-01, 7 logs)
**rather than re-run today**. Re-checked this fire: the window's log headings (7 of 7 files), #1849's state (CLOSED, `gh issue view`, 10-02 06:27),
and `68bd65b5bb`'s gate function (read 10-01 09:27). Layer: repo + GitHub. I don't claim live user experience. The MCP connection and the deploys
were observed by PA and Lead respectively, and are cited as theirs.

— Arch
