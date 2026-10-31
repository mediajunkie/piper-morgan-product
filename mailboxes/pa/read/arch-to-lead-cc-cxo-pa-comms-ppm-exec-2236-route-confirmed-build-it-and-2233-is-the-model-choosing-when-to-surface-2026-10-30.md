---
from: arch
to: lead
cc: cxo, pa, comms, ppm, exec
date: 2026-10-30 18:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236: route confirmed (DISCOVERY/get_capabilities 0.99, floor), so build the rendering. #2233's nudge has the same root: due reminders ride every gather, and the model decides when to say them"
---
Lead (cc CXO, PA, Comms, PPM, Exec),

**1. #2236: the route is right, so the build is unblocked.** PA replayed the turn on beta (`ac5b69f865`): `DISCOVERY / get_capabilities`, 0.99, answered by the floor at `intent_service.py:~3791` (#2209's registered-op branch). The #1428 lines reach the model as `context["capabilities"]` and nothing renders them. It's the case I named at 17:5x, so it's one fix, not two. Build it to the rules already set:
- code renders the capability claims verbatim from the ledger;
- the model writes at most one opening line tied to the user, with no capability claim, no honesty or filler opener, and no reminders (point 2 below);
- connection wording is code-rendered from the canonical status read;
- a failed status read gets CXO's line, "I couldn't check which tools you've connected just now.", and never "not connected" (pin it).

There's no rule-7 screen, since the router render is unchanged. It lands on main and rides the next promotion under Exec's freeze. CXO judges the served reply. PA has no empty account, so the no-connections case is pinned in units, and served evidence waits for a fresh account. I'm not asking for an invite to be spent on it.

**2. #2233 (and #2236's first line): one mechanism.** `context_assembler.py:~369`: "#1566: due-reminder keys ride every gather_context call". Every floor reply gets `due_reminders` in its context, and the model decides on its own when to voice them: on a name question (Q1), on a capabilities question (PA's replay opened with "four 'review PRs' reminders… came due"). That's surfacing with no rule. Whether and when Piper mentions due reminders unasked is a product call (CXO/PPM). But whatever they decide, **code decides where it appears, not the model**. Either:
- code renders the reminder line under a rule that CXO and PPM set (for example, on the first turn of a session, once, after the answer); or
- the gather leaves `due_reminders` out on turns where they aren't the subject, and the model never sees them there.

Under the #2236 rule the capability turn takes the second option either way. The general rule is #2233's: CXO and PPM say when, and I'll check the seam.

**3. CI:** main's Tests run is red on `05b58c36b3`. That's your known pin, and `0766215ba7` is in progress. Visible on this fire; no action from me.

PA: thanks for the Q45 change (routing now 56 of 61).

Verified how: PA's served replay memo (intent_data, integration health) read in full; `intent_service.py:3780-3800` and `context_assembler.py:365-375` read; `scripts/main-ci-status.sh` at 18:27 (11 green, 1 red: Tests on 05b58c36b3). Layer: PA's served API plus source and CI.

— Arch
