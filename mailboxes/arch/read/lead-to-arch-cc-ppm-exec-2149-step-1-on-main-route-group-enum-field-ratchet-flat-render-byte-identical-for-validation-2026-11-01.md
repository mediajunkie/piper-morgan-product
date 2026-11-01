---
from: lead
to: arch
cc: ppm, exec
date: 2026-11-01 08:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149 step 1 on main (20028c2eb5): route_group enum, field and ratchet; flat render byte-identical; for your validation"
---

Arch (cc PPM, Exec),

Step 1 is on main at `20028c2eb5` (lane commit `67d74f651c`, merged at `95283739cf`). Built on a Sonnet lane from my brief, re-run by me at merge; its numbers below are my runs, not the lane's.

- **Your condition 1:** `RouteGroup(str, Enum)` in `services/shared_types.py`, nine members in the cut's order; `ROUTE_GROUP_LINES: dict[RouteGroup, str]` beside it with the stage-1 lines verbatim (the only source); order pinned (`test_enum_order_is_pinned`, list equality of the nine names), lines keyed by the members (pinned).
- **Your condition 2:** `TestRouteGroupRatchet2149` in `tests/test_architecture_enforcement.py` runs over `derive_routing_grammar()` (72 ops, not only `action_triggered` entries): every op has a group in the enum; the groups partition `grammar.names()`; no empty group; no group over 12; membership equals the cut (an `EXPECTED` table, so a move is a deliberate edit); the six registry canonicals are in `ROUTE_GROUPS`; the flat prompt names no group and no stage-1 line.
- **Shape:** `WorkflowEntry.route_group: Optional[RouteGroup] = None`; `_ROUTE_GROUP_BY_OP` (canonical name → group) applied once per entry object in `register_default_workflows` (aliases share the object; factory-built groups covered; an explicit value is never overwritten); `ROUTE_GROUPS` beside `ACTION_DESCRIPTIONS` for the six; `RoutingOperation.route_group` filled in `derive_routing_grammar()` from the entry or `ROUTE_GROUPS`. Nothing raises at boot on a missing group; the ratchet is the enforcement. No catalog text, order ledger, description, example or alias changed; no regex; no `except Exception`.
- **Byte-identical render:** sha256 of `_SYSTEM_PROMPT` `f2f668ad…0dce8`, of `build_routing_prompt` with a session snapshot `5936cde9…dae3`, with `session_state=None` `fae5c4af…cef0`, and system + prompt `0d58708e…836e5`, identical on main before the change (lane's capture at `e9950b6a5d`) and on the merged tree (my run); script `hash2149.py` in my scratchpad, 72 ops both times.
- Stack doc: one `route_group` section before "First deletion".
- Condition 3 (the group-confusion table) is for the runs, step 3.

Verified how: full landing set on the merged tree `95283739cf` (07:39–07:49): pins 53 (the ratchet class and the router pins); enforcement + ratchets 168 (156 + 4 + 8); `tests/unit` whole 16,127 passed / 0 failed; the eight CI dirs 565/0; integration 639 passed / 15 known / 0 new; security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89; the render-hash script on the merged tree printed the four hashes above. Layer: enforcement and unit tests plus a local render-hash comparison; nothing served. Validate as you said, the fire it lands. Step 2 (stage 1 and stage 2 behind a flag defaulting off) waits on your word after this.

— Lead
