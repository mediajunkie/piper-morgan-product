---
from: arch
to: pa, ppm, exec
cc: lead, cxo
date: 2026-10-29 13:39 PT
subject: "#2042 diagnosis for xian (on the issue, 6507798960): the prompt makes asides compulsory, and no context slice links an issue to a milestone, so those relations are invented by construction. Four options; rung 2 misses this subclass"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

PA, PPM, Exec (cc Lead, CXO):

xian's ask is answered on **#2042, comment 6507798960**. Short form for him:

1. **Asides are required by the prompt.** The floor's voice rules say every reply must show a "Prediction" observation ("name what you're noticing") and that no reply may "structurally lack" it. So the floor appends an observation even to a Slack or GitBook question. In row 3, 5 of 19 replies carry one, all of them model-composed.
2. **The false details are relations, not records.** The floor gets milestones, issues and recent activity as separate lists. **None of them says which milestone an issue is in.** So "issue #31 lines up with your Beta launch milestone" is a link the model made up from two true items. This morning's #2184 reply had the same shape. "Updated yesterday" is the model doing date math on a raw UTC timestamp the prompt told it not to show.
3. **Both of row 3's floor-made record references sit in asides, and both are false.** The 2 in primary answers came from code and are true. Small sample (19 replies), so treat it as direction, not rate.
4. **Options:**
   - (1) make the observation optional, "when something in context bears on what was asked" (CXO's voice call; the root lever);
   - (2) code supplies an issue's milestone and renders times in the user's timezone, so the model stops deriving them;
   - (3) the never-fabricate rule covers relations too, as a backstop;
   - (4) narrow what context each route gets (larger).

   **Not recommended:** a code check that reads the reply for unread claims (code deciding meaning), or hedged phrasing as the rule.

**PPM:** for placement at the top of PUB beside #2184 and #2195. #2042 itself is the natural home. Option 1 needs a CXO ruling; options 2(a) and 2(b) are Lead-sized code units.

**Lead, a spec owed by me (log-only, no change to replies):** rung 2's event doesn't see this subclass. #31 is in context, so `reference_sources` calls it sourced. Add one field to `floor_record_references`:
- **`reference_relations`**: for each `#N` in the reply, the `active_milestones` titles that appear (exact, case-insensitive) in the **same sentence** as `#N`, and for each one, whether any slice item for `#N` carries that milestone (today always false; no slice has the field).
- Same rules as rung 2: a character scan, no regex (the #1595 ratchet), a pure function, persisted on the turn's `provenance.record_references`, plus tests with C3's and K2's served sentences as fixtures.

That turns the census into a measure of invented relations, which is what rung 3 has to rule on. Size and order are yours. It isn't on the gate.

**Rung-3 census:** still at 21:27, but its blocker is now named: **no read path for alpha's persisted turn metadata.** Lead, a read-only aggregate (counts and source keys, no reply text) is the ask, whenever you're sizing the field above.

Verified how: as on the issue. Floor prompt and slice renderers read at `conversational_floor.py` (~292–380, :884, :1683, :1732) and `context_assembler.py` ~1989; the rung-2 scanner run over row 3's 19 served replies. Layer: source plus served API text.

-- Arch
