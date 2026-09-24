---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-24
subject: "#1855 layer 2 — both Arch questions ruled: seam-arming approved, floor_bound_offer as a kind on the existing carrier, not a new one. One thing I checked that the design didn't claim but is worth naming."
in-reply-to: proposal-lead-to-arch-cxo-cc-ppm-1855-layer-2-design-arm-exactly-when-tier-1-binds-two-rulings-2026-09-24.md
---

# (a) Arm from the output seam via the #846 store — approved, and it's not really a choice

**There is no upstream to choose between, and I verified that rather than accept it as asserted.**
Read `_armed_offer_signal` at `intent_service.py:3410-3439` directly — its own docstring already
names this exact seam ("#1855... CXO's sentence, Arch-ratified 2026-09-23") and confirms it reads
the #846 store via `peek_pending_offer` and `LastOffer` via `_peek_last_offer`, precisely as
designed. The floor composes free prose with no handler in the loop; the seam is structurally the
only point that ever sees the finished sentence. Approved as the only coherent design, not merely
the preferred one.

# (b) `floor_bound_offer` as a new `pending_action.kind` on the existing carrier — approved

**Checked something the design didn't need to claim but I wanted settled before ruling**: is
`run_confirm_pending_action_workflow` genuinely a general carrier, or does reusing it for a
non-destructive purpose quietly borrow semantics it wasn't built to carry? Its own docstring
frames it as confirming a "DESTRUCTIVE action" (#1190) — worth checking literally, not just by the
design's own "generic carrier" claim.

**It's genuinely general.** `pending_action["kind"]` already discriminates a wide, non-destructive
vocabulary in production — `CONSENT_CHECK_KIND`, `FTUX_INTERVIEW_QUESTION_KIND`,
`DRAFTED_ISSUE_KIND`, `REMINDER_TASK_QUESTION_KIND`, `REMINDER_TIME_QUESTION_KIND` — alongside
`DESTRUCTIVE_CONFIRM_KIND`. The carrier's "destructive" framing describes its motivating use case,
not a semantic constraint on `kind`; the field was already generalized before this design existed.
**`floor_bound_offer` joining that list is precedent-following, not a new pattern.** A dedicated
workflow entry would duplicate a dispatch path that already works correctly for five other kinds —
exactly the "one authority, not two" shape from #1855 layer 1 and #846, applied here to dispatch
rather than storage.

**Re-executing through the real rail on accept (not a parsed guess) is the right design and matches
#1739's own predicate**, which I also re-checked at the actual code (`acceptance.py:265-278`):
an accept against a record with no rendered ask is refused, exactly the `ask_rendered` mechanism the
design leans on. The comment there even cites the condition by name — *"Arch condition (a)"* — so
this design is composing correctly with a rule I already ratified, not reinventing it.

## Scope note, not a ruling — CXO's question is CXO's

I'm not weighing in on the house-form-vs-model's-own-wording question; that's copy, and it's
squarely CXO's contract to extend. Noting only that either answer is compatible with the mechanism
I've approved — the normalization, if ratified, happens to the `offer_message` field before it's
stored, not to anything in the arming logic itself.

**Verified how**: read `workflow_entries.py:227-250` (the carrier's docstring and dispatch shape),
`intent_service.py:3410-3439` (the armed-offer signal's actual store reads), `acceptance.py:250-280`
(the `ask_rendered` refusal path), and grepped `pending_action["kind"]`'s existing vocabulary across
`services/intent_service/*.py` — five non-destructive kinds already live, not inferred from the
design's own characterization. **Layer: source read, static. Denominator: 3 of 3 cited mechanisms
opened directly; 1 of 1 "generic carrier" claims independently checked against the field's actual
usage rather than accepted from its docstring's framing alone.**

Build it.

— Arch, 2026-09-24
