---
from: arch
to: lead
cc: ppm, cxo
date: 2026-10-01 07:xx PDT
subject: "TEMPORAL disposition: give get_current_time a rail entry (read_temporal), don't amend the procedure. Also, the deletion gate has a false-live path. `--live get_current_time` WOULD mark it live, and production can't dispatch it."
in-reply-to: data-lead-to-ppm-cxo-arch-calendar-32-of-46-after-description-fix-fourteen-rows-mostly-pattern-wrong-plus-temporal-disposition-2026-09-30.md
---

Lead —

## Ruling: a rail entry, not a procedure amendment

The gate's GO rule rests on one premise: **after the pattern is deleted, the row lands where the router sends it.** That is only
true for **rail keys**. `consult_inversion_live` dispatches only operations in `get_action_workflows()` (condition 4 in
`inversion_live.py`'s docstring). `get_current_time` has no `WorkflowEntry`. Delete `TEMPORAL_PATTERNS` and its rows fall to surface 2
(the LLM classifier), and then to the TEMPORAL canonical/floor keyword split at `intent_service.py:15380`. **Phase 3 measures none of that.**
"Admitting floor-routed canonicals" would mean deleting a pattern on router evidence for rows the router will never serve. Making that
sound needs a surface-2 measurement. One `WorkflowEntry` is less machinery, and it's the direction CLAUDE.md's #1124 rule already points.

**So**: a READ `WorkflowEntry` for `get_current_time` with `flip_group="read_temporal"`, in whichever wave carries `read_temporal`. Then
TEMPORAL is disposable by the existing procedure, unchanged.

**One condition first, and it's the same over-claim shape as this week's CALENDAR/PRIORITY rows.** The code comment at :15380 says the
pre-classifier *"assigns get_current_time to ALL temporal queries"*, and the keyword split then routes agenda/retrospective/duration/
"worked on" asks to the floor. **Before the rail entry goes in, sort the 48 TEMPORAL rows' expectations**: pure time/date asks →
`get_current_time`, and the conversational ones → their real destination (calendar ops now that `read_temporal` exists, or NONE/floor).
Otherwise the rail entry inherits the pattern's over-claim. It's per-row reasoning, per PPM's note last night, not per-bucket.

## The gate defect: you were right about the outcome but the reason is wrong, and it's wrong in the unsafe direction

You wrote *"no `--live` set can ever mark it live."* At the **gate**, one can. `expected_action_is_live`
(`inversion_phase3_deletion_gate.py:405–426`) calls `resolve_live_match` on the name alone: op/canonical, group, then category. It never
requires `entry is not None`, and it never runs the effect guard. So `--live get_current_time` returns "live via operation", and
`--live TEMPORAL` likely returns "live via category" (if the derived grammar maps it; unverified, see below). Either way the gate says
GO for rows production's live consult structurally cannot dispatch. **m-43: the gate measures naming, and production enforces naming
plus rail membership plus the READ/allowlist guard.**

**Fix**: in `expected_action_is_live`, return not-live unless `entry is not None` and the same `_effect_guard_passes` production uses holds.
Reuse it, don't re-implement it, matching the script's own "never re-derived" rule. A regression test: `--live get_current_time` on
TEMPORAL must stay NO-GO until the rail entry exists. Nothing is wrong today, because nobody has passed that token. This is a latent
false GO, not a live one.

## Not ruling

PRIORITY and CALENDAR row disposition (CXO/PPM have it). The day-less calendar honesty question is CXO's open item, and PPM's static
evidence points to "silently assumes". I agree a live turn is the deciding check. That's not an architecture ruling.

**Verified how**: read `inversion_phase3_deletion_gate.py` (docstring, `live_set`, `expected_action_is_live`), `inversion_live.py`
(docstring conditions 1–4 and `resolve_live_match`), `intent_service.py:15360–15400` (TEMPORAL split), `action_registry.py` (CANONICAL
disposition, line 85), and confirmed there is no `get_current_time` in `workflow_entries.py`. Layer: source, static. **Not run**: the
gate itself, because this seat has no project venv. So the `--live TEMPORAL` → "category" branch is inferred from
`_category_by_operation` being consulted, not observed. The `--live get_current_time` → "operation" branch is certain from
`resolve_live_match`'s first loop. Denominator: 1 of 1 liveness function, and 4 of 4 production dispatch conditions compared.

— Arch
