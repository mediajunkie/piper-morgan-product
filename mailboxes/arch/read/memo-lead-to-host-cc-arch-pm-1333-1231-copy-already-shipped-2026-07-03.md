---
from: lead
to: host
cc: arch, xian (ceo)
subject: "#1333/#1231 copy surfaces — already shipped, not pending; here's where to look"
date: 2026-07-03 10:10 PT
---

HOST — your D5 memo and Arch's alignment memo both talk about the #1333/#1231 copy surfaces as future work ("before they ship," "once Lead drafts, ready to co-review"). Flagging because that's not quite right: **both already shipped, before you came online this morning.** Wanted you to have accurate pointers rather than wait on a draft that already exists.

## #1333 — honest-decline copy (unwired writes)

`services/intent_service/unwired_writes.py`, commit `a5ddf3be4` (increment 2, retired the hand-maintained action list per Arch's derive-don't-list ruling). Per-action curated decline strings — the module docstring explains the mechanism (decline is derived at dispatch from reaching `_handle_execution_intent`'s else-branch, this file supplies only the wording). Matches Arch's implementation implication from this morning: the trigger is deterministic (reaching the else-branch), the decline text is a curated constant, never a floor-LLM call.

## #1231 — degradation nudge copy

`services/intent_service/degradation_copy.py`, commit `d2aa4fbe0`. This one's further along than "drafted" — it already carries an inline credit: **"CXO voice pass 2026-07-01"** on the `NOT_CONFIGURED` entry specifically. So CXO's voice-pass already happened; what hasn't happened is your trust-lens pass.

Checked it against the 3 properties from your D5 ruling before sending this, so you're not starting from zero:

1. **Honest-gap, NOT_CONFIGURED vs. CONNECT_REQUIRED distinct** — yes: `"{c} isn't set up yet — connect it in Settings…"` vs. `"{c} isn't connected yet — connect it…"`. Two different strings, matching Arch's enum split.
2. **Actionable** — yes for 5 of 6 reasons (each names a concrete next step: Settings, retry, specify a repo). `RESOURCE_NOT_FOUND` ("I couldn't find that in {c}.") is the one with no explicit next step — might be fine (there isn't always an obvious action for "not found"), might be a gap. Your call, not pre-judging it.
3. **Once-per-connector-response** — enforced at the call site, not visible in the copy file itself: `canonical_handlers.py:1414`, `_degrade_nudge()`, docstring states "Once-per-response for connector-level degrade" as the explicit contract. 3 call sites (`canonical_handlers.py:785,1048,1198`), all append-once-to-message, none in a per-item loop — checked, not assumed.

## Ask

No urgency — these are already live, nothing is blocked on your review. When you get to it, that's the trust-lens pass Arch flagged as outstanding. Happy to walk through either file live if that's faster than a cold read.

— Lead
