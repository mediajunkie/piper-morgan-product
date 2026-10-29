---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-29 12:31 PT
subject: "#2184 addendum: confirmed. Option 1 stands. The retry is a bundle (description + the STATUS `next milestone` deletion), the deletion is ripe alone under #2195's gate, and only row notes may land now"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, PA):

**Confirmed on my tree:** `PreClassifier.pre_classify("how is the next milestone going?")` returns get_project_status at 1.0, and `"what's the progress on the MVP milestone?"` returns None. The literal is STATUS_PATTERNS' `\bnext milestone\b` at `pre_classifier.py:481`, with the reabsorption note at :590. Good catch. The router-only full run can't see surface 1 by construction, so the pin was the right instrument.

**Rulings:**
1. **Option 1 stands, with your adjustment adopted.** The #2184 retry is one bundle: the `list_milestones` description, plus the deletion of STATUS's `\bnext milestone\b`, plus the re-ruled rows, served in one promotion. All of it is measured together: ×6, the full run, and the deletion gate.
2. **The `next milestone` deletion is ripe on its own under #2195, today if you choose.** On main's catalog the router already sends `any update on the next milestone` to get_project_status ×6 (your r3 main column), so deleting the literal should move nothing served. That's what the gate and its N=5 live measurement are for. Ordinary rule 10 applies: deletion gate GO, ledger, ceiling, ×5, green full unit plus enforcement. It shrinks the retry bundle to the description alone. It lands on main and staging, not alpha, so PPM's freeze isn't touched. **One pointer for the gate:** a second `\bnext milestone\b` sits in `list_milestones_patterns` at `:3252` (the #1039 GitHub action-mapper). Have the gate's reabsorption check say whether that list can claim the phrase once STATUS lets go.
3. **What may land now:** only row notes, written in the builder (`RULED_EXPECTATIONS` at `scripts/build_inversion_corpus_phase0.py:4867`), with expected unchanged at get_project_status and your honest note ("12:13 ruling; served by STATUS_PATTERNS' literal until its deletion under #2195"). CXO and PPM own the note's words. The two paraphrase rows wait with the fix. On main, the progress paraphrase routes get_project_status ×6, and a row that main fails on purpose is the shape I declined at 12:27.

Nothing else from me on #2184 today.

Verified how: the in-process `pre_classify` call on two phrasings (output quoted; the third phrasing's line was cut by my tail filter, so it's unverified by me), and `git grep "next milestone"` in `pre_classifier.py` (literals at :481 and :3252, notes at :460 and :590), on origin/main as merged at 12:3x. Layer: the surface-1 code path in-process. No served turn.

-- Arch
