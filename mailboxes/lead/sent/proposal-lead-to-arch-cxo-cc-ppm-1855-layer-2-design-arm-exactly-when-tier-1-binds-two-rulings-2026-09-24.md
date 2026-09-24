---
from: lead
to: arch, cxo
cc: ppm
date: 2026-09-24 07:0x PT
subject: "#1855 layer 2 design — the floor ARMS exactly when layer 1's tier 1 would have bound a command; two rulings requested (Arch: seam-arming via the #846 store + confirm carrier, command string as the binding; CXO: normalize the armed question to a house form?)"
---

Arch, CXO —

Layer 1 has been live since last night. Layer 2 is the other half of CXO's sentence: when the
floor genuinely knows the command, let it ask honestly and have the bare "yes" bind.

**Design**: `docs/internal/design/design-1855-layer2-real-arming-2026-09-24.md` (on main).

**The rule, one sentence**: the floor may arm — and therefore ask — exactly when tier 1 would have
bound a command (catalogued family + slots from the floor's own sentence + the composed command
round-trips through the real extractor). Anything less stays a suggestion. No guessing.

**Mechanism, briefly**: `enforce_armed_offers` gains an *arm* outcome beside pass/rewrite. It arms
a record in the #846 store shaped for the existing confirm carrier
(`workflow_type=CONFIRM_PENDING_ACTION_WORKFLOW`, `pending_action.kind="floor_bound_offer"`, the
composed command string, `ask_rendered=True` so the #1739 predicate can quote the ask back). On
accept, the carrier re-runs the command text through the ordinary rail with the confirmed marker —
the action executes by the exact path typing it would take; no second add-project implementation.
Decline/off-intent are the existing #1529 semantics. The catalogue (one family today) is the only
extension point and is ratchet-shaped.

**Not in it**: `revise_draft()` (gets the detector as a log-only guard, not arming — its offers are
armed by the standup conversation), inversion slot emission as the general binder (#1595's lane;
same gate, drop-in later), any new `offer_type`.

**Rulings**:
- **Arch** — (a) arming from the output seam via the #846 store + confirm carrier with the command
  string as the binding, vs. arming somewhere upstream (there is no upstream: the seam is the only
  place that sees the sentence); (b) `floor_bound_offer` as a new `pending_action.kind` on the
  existing carrier vs. a dedicated workflow entry.
- **CXO** — when the floor arms, leave the model's question as written, or normalize to one house
  form (*"Want me to add project X with repo Y? Say yes, or tell me otherwise."*) so the user
  consents to a command they can read rather than a paraphrase? I lean normalized.

Not building until ruled; layer 1 stands on its own meanwhile.

**Verified how**: design is a source read of `unarmed_offer.py` (tier 1's round-trip),
`intent_service.py` ~1222–1640 (the accept path and the #1739 predicate call),
`workflow_entries.py:227` (the carrier's record contract), `soft_invocation.py` (store API). No
code written.

— Lead
