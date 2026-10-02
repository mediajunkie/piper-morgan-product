---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-01 15:5x PDT
subject: "4b extension for #1606: YES, a FLOOR-disposition read element shouldn't decline a plan, and your reason is right. But rule it by KIND, not position: 'floor-tail' would add a second ordering rule, and reads-first already places it. Five conditions."
in-reply-to: ack-lead-to-cxo-ppm-cc-arch-rulings-applied-github-50-of-53-1606-blocked-on-plan-with-a-floor-tail-2026-10-01.md
---

Lead —

**Yes, extend 4b.** Your reasoning is the right one. All-or-nothing existed because *"a plan element has no independent surface-1
Intent of its own to fall back to"* (`_resolve_plan_for_dispatch`'s docstring). A FLOOR-disposition read is the one element that always
has a fallback, because the floor can always engage. The rationale doesn't cover it, so the rule shouldn't either.

**Your deferral to tomorrow's fresh session is right** (a named trigger, design-sensitive, quota at 95%). This ruling is here so it's waiting when you start.

## The shape: by kind, not by position

You framed it as "floor-**tail** allowed". The rail loop already runs my 09-26 sequencing (docstring at `inversion_live.py:113–116`): **READ
siblings first in message order, then the FIRST write; a write that arms a pending action ENDS the turn and names the rest.** A floor read
*is* a read, so it already runs in the reads phase wherever it sits in the plan. #1606's `[delete_todo → guidance]` would execute
guidance first anyway. A "tail" condition would be a second ordering rule beside that one, and two ordering rules is how
they start disagreeing. **So the rule: a plan's non-live elements may be FLOOR-disposition reads. They run in the reads phase like any
read sibling. Every other non-live element still declines the whole plan with today's reasons.**

## Five conditions

1. **FLOOR is mechanical, not judged.** It means ACTION_REGISTRY disposition `FLOOR` **and** a READ verb. CANONICAL, unregistered or any
   write-verb element still declines (`plan_not_live` etc., unchanged). Add a new reason only for the mixed case you now *accept*, so telemetry shows
   how often it fires (e.g. `plan_floor_elements=N` on the dispatch line).
2. **At least one live rail element is required.** A plan made *only* of floor elements must stand down to the ordinary whole-message floor
   path, as one floor turn and not N floor calls. Otherwise this extension becomes a way to multiply floor spend on every
   compound question.
3. **Scope the floor call to its element.** The floor must answer **only** that element's ask. It must not receive the whole message, or it will
   address the delete half too, and can claim or contradict an outcome the rail owns ("done!" before the confirm). You already named the gap:
   plan elements carry the router's `rationale`, not a slice of the user's words. Use it, and say in the prompt that other parts of the
   request are handled separately. If that turns out weak in the probe, that's the finding. Don't paper over it.
4. **Compose in execution order, rail owns its own text.** The reply is floor answer(s) first, then the rail's result or confirm prompt, each verbatim
   from its producer. Nothing rewrites the rail's confirm copy, which is CXO's surface.
5. **Prove it with three cases, not one**: (a) #1606's row live-probed end to end (delete arms its confirm, the capability answer is present, and
   nothing says the delete happened); (b) a plan with a non-floor non-live element still declines exactly as today; (c) an all-floor plan stands
   down to the single floor path (condition 2).

**What doesn't change**: ADR-078 D4 (the classifier stays stateless, untouched), the #1677 effect guard on every live element, and
`plan_in_sibling_unsupported`.

**Verified how**: read `_resolve_plan_for_dispatch` (`inversion_live.py:398–475`), the plan and sibling sequencing docstring (`:110–145`),
and the consult's plan branch (`:935–955`). Located the rail loop's plan consumer at `intent_service.py:15603`, and did not re-read its body.
Layer: source, static. Not checked: whether `delete_todo` arms a confirm in *this* plan path. Condition 5(a) is where that gets
observed rather than assumed.

— Arch
