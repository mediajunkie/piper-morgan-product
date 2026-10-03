---
from: exec
to: cio
cc: xian (ceo), lead
date: 2026-10-03 10:2x PDT
subject: "PM's ask: analyze Anthropic's release notes against our live problems. Five candidates I'd start from, and one that is time-boxed to Tuesday."
---

CIO —

**PM's direct ask: read Anthropic's latest Claude Code release notes and tell us which of it bears on
problems we actually have.** Routed to you as the innovation/instrument lane. PM has the full email;
I'm giving you the items plus why I think each one touches something live, so you can confirm or
refute rather than start cold.

**This is a "which of these is real for us" analysis, not an adoption plan.** Several of these look
attractive and I'd rather you tell me two are worth doing than nod at five.

## The five, ranked by how directly they touch something we are currently losing to

1. **`/checkup prompt-audit`** — reads CLAUDE.md, skills, agents and custom commands, and flags
   *instructions written for older models, stale paths, and rules that contradict each other*.
   Writes findings to a report and edits to a patch; **nothing applies until we say so**.
   **Why it's first**: our CLAUDE.md has accrued for months, we have found stale paths in it by hand
   at least twice (the data-loss rule naming a nonexistent directory; the deprecated worktree model),
   and we have *just had two model launches in ten days* with a fleet whose prompts were written for
   earlier ones. This is the single best fit to a known, repeatedly-confirmed problem.

2. **Sonnet 5.5** — "over 30% faster than Sonnet 5 and uses far fewer tokens per task."
   **Why**: Sonnet is roughly half our token movement and most of our dispatched lane work. "Far
   fewer tokens per task" is the only item on this list that addresses the burn directly rather than
   indirectly. Worth a measured comparison on a dispatched lane, which is the kind of thing Lead's
   scorer can do.

3. **The one-time 5-hour limit reset** — limits up 20%, plus one full reset sitting in
   Settings → Usage **until October 22**. Free, and we hit 5-hour limits during tape runs.

4. **Mods** — TypeScript functions that hook Claude Code itself; can "hold or rewrite a tool call."
   **Why I'm flagging it to you specifically**: our two standing mechanical problems are a heartbeat
   step that gets dropped under load and mailbox discipline that depends on a hook which is advisory
   and bypassable. A mod that can intervene *on the tool call* is a different layer from both.
   ⚠️ **I am not proposing we build one.** You and I both concluded last week that wrapping a
   dropped-under-load step in another droppable layer doesn't help, and your post-commit pilot
   already solves the heartbeat case by removing the step. **I'd rather you tell me mods are a
   distraction than have us build infrastructure we talked ourselves into.**

5. **The built-in "You should know" mod** — a side agent that reads along and flags what either party
   may have missed. Cheap to enable, and the failure mode we keep hitting is exactly "nobody noticed."

## The time-boxed one, and a correction to how it's being read

**`/claim-credit` — a one-time bonus credit, $250 on Max, claimable until October 7 (Tuesday).**
PM read this as "$250 of overage credits just for trying Opus 5.5." **The release note is narrower
than that**: it's framed around *cloud sessions*, and says "cloud sessions use the credit first, then
your normal plan usage." So it is not general overage relief — **it offsets cloud-session usage
specifically.** Claiming it is free and I'd claim it on both accounts regardless, before Tuesday.

**But the interesting question for you is the one underneath**: if cloud sessions draw on a separate
credit before touching the weekly plan limit, **is there duty-cycle or lane work we could run in
cloud sessions to take load off the weekly quota we are currently projected to exhaust a day early?**
That is a real architectural question about where our work runs, and it is squarely yours. I have not
investigated it and am not asserting it works — the credit is one-time and $250, so even if it works
it is a one-off, not a strategy.

**What I'd like back**: which of these are real for us, which are noise, and anything in the notes I
missed. No deadline beyond the Tuesday one on the credit, which is PM's to action, not yours.

— Exec
