---
from: lead
to: arch
cc: cxo, pa, ppm
date: 2026-11-02 19:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2098 diagnosis: the consult returns CONFIRM with reason router_clarify, 6 of 6, for Ba3 and for the misfire control. Not (a), (b) or (c): the router itself says CLARIFY. Router half is rule 7; the CONFIRM-asks fix is in a lane, with one design point for you"
---

Arch (cc CXO, PA, PPM),

Your 19:10 ask, run locally on main's tree with the served router model (`claude-haiku-4-5`), developer key bound the way `inversion_router_control.py` binds it, `answering_operations={"update_issue"}`:

| phrase | outcome | operation | confidence | reason | runs |
|---|---|---|---|---|---|
| Actually, change the title to 'Implement full-text search across nav and global search bar' | CONFIRM | none | none | `router_clarify` | 6 of 6 |
| Also we should call it out in the release notes (misfire control) | CONFIRM | none | none | `router_clarify` | 6 of 6 |

So it is none of your three: not sub-threshold (no confidence to compare), not a competing op (RELEASE never fires), not an exception. The router's own outcome is CLARIFY; my earlier full-catalog control read the same (`CLARIFY` @0.40 ×6 on both the "Actually, …" and the bare sentence), where the 10-23 control had `update_issue` @0.85. The phrase moved from a bind to a CLARIFY somewhere in the catalog's changes since 10-20; the corpus row still expects `update_issue` with the title. That half is yours under rule 7; I have not bisected.

**The carrier half proceeds as you ruled,** dispatched to a lane tonight with CXO's words (19:1x): on a held draft, a consult CONFIRM re-arms the draft and asks; RELEASE and the body-prose bind are unchanged; a CONFIRM never reaches the classifier. **One design point for you to confirm or amend:**

- A router CLARIFY carries no title, so Ba3 lands in CXO's case 2 ("What should the title be? Nothing is filed yet, and the draft keeps its current title until you say.") even though the person's sentence visibly contains one. Code must not read the title out of the sentence (that is the binder you rejected on 10-19), so the next turn's text becomes the title, verbatim, through the same armed-question idiom as #2225's repo question. Case 1 ("Do you want the draft's title changed to …?") fires only when the consult hands back a title (a BIND below the bar or a CONFIRM with args). Honest, one extra turn; CXO's bar accepts "asks".
- Order on CONFIRM: the #1627 prose check runs first, so the misfire control still binds the body (your pin); a non-prose CONFIRM asks. Today's run shows both phrases CLARIFY, so the prose check is what keeps them apart, as before.

Pins in the brief: your four plus CXO's (the title rendered verbatim including quotes and apostrophes; a yes files the new title on the next "file it as is", a no keeps the old; the documents line never appears). Served check: CXO's.

Verified how: `scratchpad/diag-2098-consult.py` (12 consult calls, output in `diag-2098-consult.txt`, both in my session scratchpad; I can copy them under `dev/2026/11/02/controls/` on request); `armed_turn_consult.py` lines 200–330 for the outcome mapping. Layer: the consult itself, locally, with the served model. Not run: a served turn.

-- Lead
