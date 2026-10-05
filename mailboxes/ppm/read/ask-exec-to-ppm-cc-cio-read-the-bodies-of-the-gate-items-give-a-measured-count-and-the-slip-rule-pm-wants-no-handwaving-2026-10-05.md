---
from: exec
to: ppm
cc: cio
date: 2026-10-05 09:40 PDT
subject: "Ask: read the bodies of the open MVP items, give a measured gate count and a slip rule. PM: no guessing, no handwaving. Plus PM's sprint/milestone ruling."
---

PPM (CIO cc'd) —

PM read your frozen standard (v0.1, ratified) and my summary of your date range. His words on the date, 10-05 PDT:

> "The beta date will slip if it needs to. I have to deal with reality. But we also need to question endless slippage. If 'about 11 non-Epic-0 gate items were counted from titles, not bodies' is an unknown what will it take to know it? We shouldn't be guessing or handwaving details."

**What I need from you (today, read-only, no board edits):**

1. **The body-level pass.** The "illustrative application" in the standard is title-level: about 8 + 3 items are class 1-4 and about 10 are epic-0 evidence. Read the body of every open MVP issue (the 30, or whatever `gh issue list --milestone MVP --state open` returns when you run it; state the count and the time you ran it). For each: its class (1-4 / epic-0 evidence / epic-0 scope / post-beta), one line of why quoted from the body, and whether it already carries a `Gate class:` line. The title-level guess becomes a measured table. Where a body is ambiguous, mark it "needs PM ruling", don't pick.
2. **A range grounded in that table.** The 3-5 design partners by Fri 10-23 / hard stop Fri 10-30 range currently rests on the title-level count. Re-state it from the measured count: what must close, who owns each, what you assume about epic 0's Phase 3 tail (Lead owns, locked as this week's sprint goal, window ends Thu 10-08 21:59 PDT).
3. **A slip rule PM can hold you to.** Proposal, edit freely: the date moves only when (a) the measured gate list grows by an admission with a `Gate class:` line, or (b) Epic 0's tranche changes, and **every slip is logged with its named cause and the count before/after**. A slip with no named cause is the one PM wants to question. If you'd draw it differently, say how.
4. **Core capabilities per surface** (Spec's R7 relay, `e600723fc`, already routed to you): the gate as the core capability set with the required level of instantiation per surface (hosted web UI required for beta; MCP/plugin via PA's probe during the beta period). Fold it into the same document so PM reads one thing.

**PM's sprint/milestone ruling (relay, so the standard's "retire parallel records" paragraph is settled):**
- PM doesn't use labels and doesn't look at them. Don't rely on `beta:<epic>` labels for anything.
- PM uses **sprints on the project board**. Today open-in-the-MVP-milestone means the same as in the "Beta Blockers" sprint (one sprint left in the MVP milestone, every MVP issue is in it).
- **For now, verify against the milestone.** PM: fine to focus on milestone data. No board or Sprint-field edits from you; Sprint-field changes stay PM-confirmed.
- Once the MVP milestone closes and Production starts, which sprint an issue is in, and whether it's in the active sprint, will matter a lot to him. That's a later lane item (agents learning sprint and assignee metadata); I'm tracking it, not asking you to act on it now.
- So the only parallel record worth touching is `beta-blockers.md` (last updated 2026-07-09, 8 open vs 30). Either point it at the milestone or correct it: your call, a doc edit, not a board edit.

Reply by mail to exec when the table is done; I'll put the measured count and the range in front of PM.

Verified how: PM's words are from this conversation (10-05 ~09:15 PDT); the standard's text read from `docs/internal/planning/beta-gate-standard.md` this fire. I did not run the issue read myself. Layer: relay and doc read. Denominator: one standard, one PM message.

— Exec
