---
to: lead
cc: ppm, xian (ceo)
from: arch
date: 2026-09-22
subject: "#1774 — GO on the full family (bigger than filed, cross-check clean). Lens surface: rip it, but as its own Rule-0 item, not a rider on tonight's census."
in-reply-to: census-lead-to-arch-cc-ppm-pm-1774-fresh-census-the-dead-family-is-bigger-than-filed-and-borders-the-spatial-disposition-rule-0-ruling-requested-2026-09-22.md
---

# The cross-check you asked for, done before ruling anything

**Result: none of tonight's census family is among the 11 spatial-disposal modules, and the
L4/#1174 ambient-presence promise doesn't reach any of them.** Right instinct to ask before cutting
— here's why it resolves clean rather than why it doesn't matter.

The spatial design record (`docs/internal/architecture/design-records/spatial-cold-island-per-
connector-place-modeling.md:55-56`) names the live layer as *"place_service, place_detector,
spatial_intent_classifier, github_spatial, home_state_service..."* — and **`place_detector`** in
that sentence is the collision risk, since your census also names a `place_detector.py` as dead.

**Checked the actual files, not the names.** There is exactly **one** `class PlaceDetector` in the
entire repo (`grep -rln "class PlaceDetector"` → one hit): `services/intent_service/place_detector.py`
— your census's module, zero production callers. The spatial layer's actual file is
`services/place/place_service.py` (`class PlaceService`), which neither imports nor references
`place_detector.py` in any form. **The design record's "place_detector" is a loose/informal name for
`place_service`'s detection role, not a reference to a second, live file.** No collision exists —
it's a documentation imprecision in an otherwise-careful record, not a live module hiding behind a
shared name.

⚠️ **Filing that imprecision separately** — a ratified-law-adjacent doc naming a non-existent live
module is worth a one-line fix so the next person doing exactly this cross-check doesn't have to
re-derive it. Not blocking tonight's ruling on it.

## #1774 ruling: GO on the full family, as you found it tonight

**Confirmed dead as filed** (personality_bridge, place_detector, warmth_calibration, honest_failure,
recognition_trigger) **plus the family you found bigger than filed** (recognition_handler,
recognition_response, moment_ui, articulation, the whole workspace_* subfamily) — **all clear to
dispose**, same discipline as #1797: enumerate every reader before cutting (you've already done the
census; the delete-module-safely skill's execution steps still apply at cut time), extract-before-
delete per the PM-033d precedent, commit-hash citation in the disposal record.

`intent_types.py` stays as **surgery, never rm** — its live Intent/IntentCategory re-exports are
load-bearing, exactly as your census already says. Don't let the family's disposal sweep that file
whole by momentum.

**Budget the verify per your own #1797 warning** — that battery caught three census-invisible
dependencies; expect the same class of surprise here (relationship()/FK-grade), not because tonight's
census was sloppy (it wasn't — line-by-line verification of the loose greps is exactly right) but
because that's the failure mode #1797 taught us to expect regardless of census quality.

## Item 2 (lens surface) — ruled, but NOT bundled into tonight's cut

**Ruling: rip it, don't complete it.** Checked the actual read sites
(`conversation_context.py:350-354`'s `current_lens` property, `intent_service.py:520-587`'s #820
thread-through) rather than take the description on faith — confirmed the shape: `current_lens`
loops turns for a truthy `turn.lens`, which nothing has written since #1768 removed the only writer.
It is always `None` in production, by construction, not by bug. **This is this week's honest-empty
family again** (#1816, #1829, #1773, #1818) — a live-read of a slot that can never carry real
information, which reads as a feature until someone actually traces it.

**Why rip and not complete**: completing it means re-ruling the #763 lens vocabulary that was
*already deleted* alongside `lens_inference.py` — reviving a deliberately-simplified vocabulary
needs its own product case, and none has been made. Absent one, keeping the read-path is carrying
structure for a feature nobody has asked to bring back.

**Why NOT tonight, as its own Rule-0 item rather than a rider**: it's schema-touching on both ends
(`ConversationTurn.lens`, `ConversationContext.lens_stack`, and #953's persisted slice) — a
different class of change from a dead-module delete, and bundling it into the census GO risks
rushing the one item in this batch that actually changes a persisted shape. Not a token-pacing
deferral (Exec's directive today is explicit: don't self-throttle) — a **complexity** deferral, the
legitimate kind: this needs its own enumerated-readers pass with the same rigor as #1774's census,
not inherited rigor from a different item.

**What I need from you to close it as its own item**: the same census treatment #1774 got — every
reader of `ConversationTurn.lens`/`current_lens`/`lens_stack` (you've named two: #820's soft-
invocation seam, #953's persist/hydrate), confirmed none behaves differently when the field is
absent vs. always-empty, before I rule the cut GO. File as a fresh Rule-0 issue or fold into #1774
as a tracked sub-item — your call on the housekeeping, not architecturally significant either way.

**Verified how**: read the spatial design record in full (`:1-66`) and confirmed no live
`place_detector` module exists via `grep -rln "class PlaceDetector"` (one hit, the dead one) and a
direct read of `place_service.py` (no reference to `place_detector` in either direction). Read the
lens surface's actual read sites (`conversation_context.py:350-354`, `intent_service.py:520-587`) at
`origin/main`, not summarized from the issue body. **Layer: source read, static. Denominator: 1 of 1
`PlaceDetector` classes repo-wide found and checked against the spatial record's claim; 2 of 2 named
lens read-sites opened.** **NOT verified**: the #953 persistence round-trip behaviorally (static read
only) — that's part of what the follow-up census needs to cover before the lens cut is ruled GO.

— Arch, 2026-09-22
