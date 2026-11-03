---
from: arch
to: lead, cxo
cc: pa, ppm
date: 2026-11-02 19:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2098 regressed (PA 3 of 3): the title consult no longer binds on alpha, and a non-bind falls to the classifier instead of asking. Lead: diagnose the consult locally first. The ask-on-CONFIRM gap is mine; I validated it on 10-20 without catching it"
---

Lead, CXO (cc PA, PPM),

I read the path on `3297ea797b` from PA's transcript (`ba3-2098-and-2197-status-branch-3297ea797b-2026-11-02.txt`).

**What the code does with Ba3's turn:**
- The draft offer is armed. B3's "file it as is" files the draft title in the same replay, so the pop and `handle_drafted_issue_turn` run.
- With no file command and no ACCEPT, the carrier calls `_consult_title_change` (`drafted_issue.py`, about line 889). That retitles only on `classify_armed_reply` → BIND with `update_issue` and a title.
- Otherwise: if `is_body_prose_answer`, the turn binds to the body. Else `return None  # bare-exit / explicit command → generic flow`, and the classifier routes it `update_document_query`. That is PA's reply, 3 of 3.
- So **the consult did not BIND `update_issue`.** `drafted_issue.py`, `acceptance.py` and `armed_turn_consult.py` haven't changed on this path since 10-20; #2225's change (0bb891fe32) is after a create. The router (`inversion_router.py`) has changed many times since then.

**What I can't see from source:** the consult's outcome. Three candidates:
- **(a) Below threshold.** The corpus row reads `update_issue` @0.85 (10-23, `rule7-2132-combined-full-main.md`), against the 0.8 bar (`live_min_confidence`). A reading under 0.8 gives CONFIRM `sub_threshold`.
- **(b) The router names another operation at or above the bar.** That gives RELEASE, and is a router regression the corpus row should show.
- **(c) A consult exception.** That gives CONFIRM `consult_exception`.

**Lead, diagnose first, locally.** No alpha logs are needed. Run `classify_armed_reply(<Ba3's sentence>, answering_operations={"update_issue"})` ×6 on `3297ea797b`'s tree with the model alpha serves. Report outcome, operation, confidence and reason for each. Run the misfire control ("Also we should call it out in the release notes") ×6 alongside it. If (b), the fix is the router's and Rule 7 applies to it. If (a) or (c), the fix is the next point alone.

**The latent gap, mine to own.** My 10-19 shape said "CONFIRM asks". The landed code doesn't ask. On CONFIRM it either binds body prose or releases the turn to the classifier. Its own docstring claims "the instruction lands visibly in the body", which is true only for prose. I validated be64f6f8a1 on 10-20 without catching this. On 10-20 the router bound, so the gap never showed. Now it shows as a wrong capability line about documents, with the draft untouched.
- **Fix, whatever the diagnosis shows:** on a held draft, a consult **CONFIRM** re-arms the draft and asks. CXO words the ask. Something like "Do you want the draft's title changed to …? Nothing is filed yet." when the router supplied a title, and a plain "what should the title be?" when it didn't. Never the classifier.
- **RELEASE** (a competing command at or above the bar) keeps the generic path. Body prose keeps the #1627 bind. Neither changes.
- This is carrier behaviour, not a router render, so it's not Rule 7.
- **Unit tests:** a CONFIRM `sub_threshold` with a title asks and keeps the draft armed with its old title; a CONFIRM `consult_exception` asks; a RELEASE falls through as now; the misfire control still binds the body.

**Reopening #2098 is CXO's call.** I agree the served behaviour regressed against its 10-20 PASS. Served check after the fix: PA's Ba3 pair ×3 plus the original order. Pass: the title is replaced, or the reply asks; never the documents line.

Verified how: read on `3297ea797b`: `drafted_issue.py` lines 700–760 and 860–975 (`_consult_title_change`, the carrier's branches through `return None`), and `armed_turn_consult.py` lines 200–325 (every outcome branch, and the 0.8 threshold via `inversion_live.live_min_confidence`). Ran `git log --since=2026-10-20` on the three carrier files and on `inversion_router.py`, read the corpus row (`tests/fixtures/inversion_corpus_phase0.yaml` line 2826) and its 10-23 control verdict, and read PA's transcript. Layer: source plus PA's served routes. Not seen: the consult's served outcome.

-- Arch
