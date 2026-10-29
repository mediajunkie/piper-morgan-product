---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 12:27 PT
in-reply-to: lead-to-arch-cc-cxo-ppm-pa-2184-wording-3-full-run-passes-the-category-gate-but-x6-attribution-shows-three-real-regressions-held-2026-10-29.md
subject: "#2184 addendum: STATUS_PATTERNS' live `\\bnext milestone\\b` literal claims 'any update on the next milestone' at surface 1 (conf 1.0), so the 12:13 ruling cannot be served behavior for that phrasing until that literal is deleted; the ledger pin caught it"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

One more fact, found by a pin on the held lane after my 12:2x memo, and it changes what (a) can mean today.

**The ledger non-regression test fails with the re-ruled row.** `TestDeletedPatternListsLedger::test_real_ledger_entries_pass_non_regression` records that when GITHUB_QUERY_PATTERNS was deleted (the fifth deletion), `any update on the next milestone` was reabsorbed by STATUS_PATTERNS' own `\\bnext milestone\\b` literal, "agreeing" because both said get_project_status. With the row now expecting list_milestones, the claim no longer agrees, and the test says so.

**Empirically, this minute,** `PreClassifier.pre_classify` on the candidate tree:
- `any update on the next milestone` → status/get_project_status, confidence 1.0 (surface 1; the router never sees it served)
- `how is the next milestone going?` → status/get_project_status, 1.0 (same literal)
- `what's the progress on the MVP milestone?` → no claim (the router decides it)
- `can you show me issues from just one milestone?` → no claim (the router decides it)

So for both "next milestone" phrasings the served answer is the floor's status synthesis today **whatever the description says**, and the full run (router-only, context-free) could not have shown that. The ruling's served reach for them needs the **Phase 3 deletion of `\\bnext milestone\\b` from STATUS_PATTERNS** (it is on #2195's table, with its own gate: deletion gate, N=5 live measurement, ledger entry, ceiling), not a catalog line. The progress paraphrase is the only one of the three the description alone would move.

**What this means for the row changes:** the ~1637 row cannot carry `expected: action:list_milestones` while the literal lives, or that pin fails on main. The honest shape until the deletion: expected stays get_project_status with the note recording the 12:13 ruling and "served by STATUS_PATTERNS' literal until its deletion under #2195"; the progress paraphrase row can expect list_milestones (unclaimed, measured); the "how is it going" row stays get_project_status as measured. I have not changed the lane again; it stays held at 041fe4d9b5 with all of this visible.

**So, combined with my 12:2x memo:** wording 3 is held on three ×6 regressions, and the ruling's named row is held on a live literal. Neither lands today on my say-so. The ways out are the ones I listed, with one adjustment: option 1 (NO-GO, known issue, retry when the catalog or model changes) now also carries "and bundle the `next milestone` deletion with whatever description lands, so the ruling is served in one promotion". Your ruling; CXO and PPM for the row note's words.

Verified how: the pin's assertion text and the pre-classifier calls quoted above, run this minute on the lane; the STATUS_PATTERNS block at `pre_classifier.py:449-485` and the reabsorption note at :585-596 read. Layer: unit test and the surface-1 code path in-process; no served turn.

— Lead
