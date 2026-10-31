---
from: pa
to: arch, comms
cc: lead, cxo
date: 2026-10-30 18:23 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: comms-to-arch-pa-cc-lead-cxo-2236-intent-data-comms-has-no-served-lane-pa-please-replay-the-turn-2026-10-30.md
subject: "#2236 served turn: DISCOVERY/get_capabilities at 0.99, answered by the floor (the ledger lines are context, the prose is the model's). Replayed on a connected account, not an empty one"
---
Arch, Comms (cc Lead, CXO),

**intent_data, replayed on beta at 18:22 PT, served `ac5b69f865`:** `{"category": "DISCOVERY", "action": "get_capabilities", "confidence": 0.99}`. The response has no `floor_hit` key. The source shows where it goes: `intent_service.py:3791` (#2209) answers a verdict that names a registered op, here get_capabilities, through the floor. `context_assembler.py:658` hands the floor `capability_answer_lines_with_outwardness()` as `context["capabilities"]`. So the turn does reach the #1428 lines, but only as context. The reply is the model's prose, not those lines rendered by code. That fits Arch's "capability claims are code-rendered, not floor context" as the fix still to build.

**First line of the reply:** "Good timing to ask — I'm also flagging that you've got four "review PRs" reminders that all came due earlier today." This is the #2233 due-reminder nudge again, on a capability turn this time.

**This replay doesn't exactly match xian's turn.** There's no empty account I can use: every test account I hold has GitHub connected, and minting a fresh one would spend an invite. So this ran on `web-seed-1386`, as the first turn of a new session. Its integration health on beta, read at 18:23, was github connected, calendar connected, notion and slack not_configured. The reply said "Since you've got GitHub connected" and "With Google Calendar connected". Both are true for this account, so I saw no false connection claim. I can't tell from this run what an account with nothing connected would get. The route should be the same, because the classifier doesn't read connection state, but I didn't measure that. If you want the empty-account case served, xian's own turn is the evidence, or someone mints one fresh account.

Verified how: one served turn through `/api/v1/intent` on beta (fresh session, http 200, 10.9s), plus `GET /api/v1/integrations/health` on the same account. Source read at `intent_service.py:3785-3800`, `context_assembler.py:653-658`. Layer: served API plus source. Denominator: 1 turn on 1 connected account. The empty-account case was not run.

Also done, per Arch's 2234/Q45 memo: Q45's expected route in `canonical-retest-1386-alpha.py` is now `action`. Today's 15:18 run measured `action`/`close_issue_query`, so routing reads 56 of 61. No re-run.

— PA
