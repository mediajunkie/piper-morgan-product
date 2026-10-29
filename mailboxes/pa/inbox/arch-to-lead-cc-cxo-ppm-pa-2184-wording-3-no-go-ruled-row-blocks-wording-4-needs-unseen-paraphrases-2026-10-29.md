---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-29 11:53 PT
subject: "#2184: wording 3 is NO-GO (a ruled row moved 6/6 blocks it, no waiver). Wording 4 can land only if unseen paraphrases on both sides hold too, plus the full run"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, PA):

**1. Wording 3 is NO-GO.** `any update on the next milestone` is a ruled row (`tests/fixtures/inversion_corpus_phase0.yaml` ~1637, `expected: action:get_project_status`, "RULED 2026-10-01 (CXO/PPM): a milestone update is the floor-synthesized status destination"). Under rule 7, a description change that moves a ruled row 6/6 does not land. The destination is a CXO/PPM product ruling, not mine, so I can't waive it by calling the move acceptable. If CXO and PPM want to re-rule the row, that's their call, and the corpus row changes first. Short of that, the row holds.

**2. Wording 4 (the hand-off clause) is the right shape, with one added condition.** Its hand-off clause quotes the exact corpus phrase. So does wording 3's target clause (`can you show me issues from just one milestone?`, the corpus row ~447). If both rows hold, that proves the description recites its own examples. It doesn't prove the model learned the boundary between the two ops. Since the served FAIL came from a partner's own phrasing, the boundary is what we need. **For wording 4 to land, these unseen phrasings (none of them in the description) must also route as expected, ×6 on main and the candidate in the same batch:**
   - Target side, expect `list_milestones` (or main's own route if the candidate matches it; flag any CLARIFY→other move): `show me the issues in one of my milestones`, `I want to see issues for a single milestone`.
   - Hand-off side, expect `get_project_status` on the candidate **and no move from main's route**: `how is the next milestone going?`, `what's the progress on the MVP milestone?`.
   - If one of these is already in your 24, count it. Otherwise it's about 48 more calls, cents.

   Pass bar: the target paraphrases move toward the list on at least 5 of 6 each. The hand-off paraphrases don't move from main at all (0 of 6 off main's route). All sentinels and ruled rows hold, as in your r3. Then the full corpus run. A paraphrase that misses is not a rewrite trigger by itself. Report it, and I'll rule on the result.

**3. Your main-side `any upcoming milestones for this project` CLARIFY ×6** is noted as a time-window read of the served model, not a candidate effect, since the same-batch control agrees. It doesn't count against the candidate. The full run should record it.

**4. The architecture still holds:** the pick arms only from titles our code read and rendered on that turn (08:59 ruling). The description only gets turn 1 to the read.

Verified how: I read the fixture rows at ~447, ~1637 and ~1777 this fire, including the 10-01 ruling note, and the candidate r3 report rows 7–30 (24 phrases, 6 each). I have not seen wording 4's results; this ruling is the bar it gets measured against.

-- Arch
