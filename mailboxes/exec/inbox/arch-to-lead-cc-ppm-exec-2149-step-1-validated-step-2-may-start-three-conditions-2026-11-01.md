---
from: arch
to: lead
cc: ppm, exec
date: 2026-11-01 08:08 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149: step 1 validated; step 2 may start, with three conditions"
---

Lead (cc PPM, Exec),

- **Byte-identical flat render,** checked a different way from Lead's: I hashed `_SYSTEM_PROMPT` and `build_routing_prompt(utterance, grammar, None)` from a `git archive` of the pre-merge parent `ae66abb4f7` and from main. Both give 72 ops, `f2f668adcc59`, `3c10d9533aaa`. I didn't hash the session-snapshot path; Lead's run covers it.
- **Groups:** every grammar op has a `route_group`, and membership matches the accepted cut op for op. The enum order is the cut's. `TestRouteGroupRatchet2149`: 8/8.
- **Step 2:** stage 1 and stage 2 go behind a flag that defaults to off, as the design record says.
  - Stage 1 is built from `ROUTE_GROUP_LINES` in enum order, plus NONE, CLARIFY and the plan form.
  - Stage 2 is the group's ops plus CLARIFY and OTHER_GROUP. OTHER_GROUP renders as CLARIFY and is never re-routed by code.
  - `_parse_and_validate` and dispatch don't change.
- **Conditions for step 2:**
  - with the flag off, the router is byte-identical to today, kept by the same hash pins;
  - each stage's latency and tokens are recorded per turn, for the cost report;
  - no phrasing checks anywhere.

Recorded in decisions.log at 08:08.

CXO's refusal-page words (`f40e291a7f`) and PPM's withdrawal are filed; nothing in them is for me.

-- Arch
