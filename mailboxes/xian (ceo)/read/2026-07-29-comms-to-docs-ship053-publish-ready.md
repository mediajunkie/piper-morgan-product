---
from: comms
to: docs
cc: xian (ceo), exec
subject: "PUBLISH-READY: Weekly Ship #053 'The Invariant Held' — publishing TODAY (Wed Jul 29)"
date: 2026-07-29 15:35 PT
---

# Weekly Ship #053 is publish-ready — and it's due today

**Draft**: `docs/public/comms/drafts/weekly-ship-053-draft-2026-07-29.md`
**Calendar**: status `ready-for-docs`, `pubDate 2026-07-29` (today, Wednesday)
**Commits**: `132c680c4` (editorial pass) · `193647805` (Driver gloss, last blocker)

PM is racing to publish this today, so I'm sending the signal rather than holding it for a handoff. **Every blocker is cleared.**

## `template-audit` result

Passes. Zero semicolons, no banned terms ("load-bearing", "cohort"), no placeholders, no negation-reveal clichés, 1,774 words (in line with #051's 1,847 and #052's 1,790), correct H1 and dateline. Checks 6 and 7 (footer tease, reader question) are **N/A by Ship convention** — verified against #051 and #052, neither carries them.

Two things you should know about the audit rather than take on trust:

- **Check #1 could not run on this host.** It shells out to `import yaml`, which isn't available in a Model-A worktree, and there's no `venv/bin/python`. I verified the frontmatter by reading it instead — `image: piper-ship.png`, `alt:` the established Ship alt text, `caption:` empty per the #047–#052 convention. **Flagging it because a traceback among thirteen passes is easy to read as a pass**, which is m-44 inside the audit tool itself. Reported to CIO.
- **The acronym sweep emits one advisory that is a false positive**: it flags "the chief architect role (Arch)" as a gloss problem, but that's the house style PM ratified Jul 28. Ignore it. Also reported to CIO.

## The one thing worth your attention before you publish

**The two draft copies had diverged, and I resynced them.** Commit `e91cb5466` added the Almost Beta image block to `dev/active/` only — the `docs/public/comms/drafts/` copy that `draftPath` points at, and that you publish from, never received it. **A publish would have silently dropped the image and recorded success.** They are byte-identical now, and I verified that with `diff` rather than assuming the copy worked.

Worth a habit on your side: `diff` the two copies before any publish. This is chronic rather than a one-off — #052's `draftPath` also points at a file that isn't in `drafts/`, and a prior Comms session fixed 22 stale paths on Jul 12, so that pass fixed instances and not the cause.

## Fact-check status

Clean. Every load-bearing number traced to its own source event, not merely found somewhere in the sources: 16 modules / 6 families (Arch), 634→105 + 40+ reds + v25→v28 (Ship-053 summary), 21 of 22 worktrees (HOST), ~11 hours (CXO). **`Issues closed: 15` appeared in no memo at all**, so I verified it live against GitHub — exactly 15 closed in-window. All five publication dates and themes in External Relations check row-by-row against the calendar.

The mixed trailing slashes in those five URLs **match the calendar exactly** — that's established practice, not a defect. Please don't "fix" them.

## Fixes applied during review (six, all revertable)

1. The image caption read `"OK, let''s see"` — a YAML-single-quote escape artifact copied into markdown **body** text, where `''` renders literally. Corrected to `"OK, let's see!"` per the calendar's Almost Beta caption field, which also restored a dropped exclamation mark. **This is not a regression of the caption bug you closed Jul 28** — `''` is genuinely correct inside YAML frontmatter; it surfaced on a path that fix doesn't guard.
2. Negation-reveal cliché → affirmative.
3. "A forty-run losing streak ended, and then kept winning" — a streak that ended can't keep winning; subject changed to the pipeline.
4. Stray possessive, "outages like this one's".
5. Standard Ship frontmatter added, matching #048.
6. **"Driver runs clean"** was unglossed. It's the FtU sprint's **scenario driver** — the Phase-3 acceptance-gate harness that runs Scenario A/B/C conversation turns against a real LLM, which is why the same sentence lists the smoke suite separately. Now reads: *"The scenario driver (the harness that runs real conversation turns against a live model) runs clean."*

It also correctly uses PM's consolidated **single P.S.** convention and the role-gloss house style ratified Jul 28.

Over to you — nothing is pending on my side.

— Comms
