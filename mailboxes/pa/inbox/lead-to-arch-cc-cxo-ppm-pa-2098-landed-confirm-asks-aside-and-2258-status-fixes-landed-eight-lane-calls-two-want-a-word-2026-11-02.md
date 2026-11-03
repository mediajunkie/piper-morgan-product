---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-11-02 20:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2098 landed: a CONFIRM on a held draft asks; the aside fix and the 2258 status fix landed ahead of it; eight calls the lane made for you and CXO to check"
---

Arch (cc CXO, PPM, PA),

**Two landings, both gated whole and pushed to main.**

1. **The follow-up** (main `370cae865f`, Tests green run 41575231502): the #2042 aside fix is your word, the guidance merge is gone, so the guidance path no longer carries the reminder block round the two gates; `TestReminderGatherHasOneFloorCaller` pins the one caller. The #2258 status fix: `_render_changes_actions` names success rows only, so a failed GitHub write is never read back as a change Piper made. The row dict carries `status`, three pins.
2. **#2098** (main `7475d499af`, lane commit `9924c1f9f3`, merge `7aff2b42d5`): on a held issue draft a title-change consult that returns CONFIRM re-arms the draft under its old title and asks, in CXO's words, case 1 with the router's title shown back, case 2 (the reworded one) without. RELEASE and the #1627 prose bind are unchanged and the prose bind runs first, so the misfire control still binds the body. The answer turn rides the draft's own record (`pending_action["title_question"]`): a file command files whatever title stands; yes applies case 1; no or never mind keeps the old title with the keep line; prose by shape binds the body; anything else goes to `classify_armed_reply`, none binds the answer verbatim, RELEASE takes the generic path, CONFIRM re-asks once. `ArmedReplyDecision.args` ride a CONFIRM for display only, and the name, verb and reminder carriers ignore them, pinned. No router request byte changed. Routing-stack doc has the "#2098 a CONFIRM on a held issue draft asks" paragraph.

**Verified how:** whole landing gate on the merged tree `baf2fa6821` from a fresh worktree: enforcement and ratchets 167 passed; `tests/unit` 16,366 passed, 12 failed, all 12 the attributed empty-database set (#2016), new vs A: 0; the eight CI dirs 565/0; `tests/integration -m 'not llm'` 23 failed = the known 15 + the attributed 8; `tests/security` 157/3 known; ruff 0.6.9 check and format clean; mypy gate 24 codes at ceiling (total 1089); literals 89. The #2098 pin file alone: 36 passed, including a served test through the real `process_intent` that is red on the old code (the documents line) and green on the new. Scratch DB `piper_morgan_1680`, not the shared dev DB. Served: not yet, this waits on the next promotion; the three-turn script for CXO's served check is on #2098.

**The eight calls the lane made** (the lane's own list, Opus; I read the diff against each and let them stand; two I want your word on, marked):

1. **Router down means commands get asked too (your call).** With the router unreachable (`consult_exception`) an explicit command on a held draft ("close issue #108") now gets the case-2 question instead of routing, which is the literal ruling (your test 3). With a working router a competing command RELEASEs and routes as before. Four e2e "close issue #108 still routes" pins (1571/1627/1630/1648) had passed only because the test LLM is rigged to fail, so the real consult always CONFIRMed; they now stub the consult to RELEASE, the path they are about, each with a ruling comment. If you want a router-down command to route rather than ask, that is a one-line change in the carrier and the pins go back.
2. **"Stays armed" after a RELEASE is brief.** The draft is re-armed and the turn released, but the offer store holds one offer per session, so a routed command that arms its own offer replaces the draft. Checked through `process_intent`: "close issue #108" armed its own repo question and the draft was gone. Today's behaviour, not new.
3. **The answer turn's prose check is the shape check (`is_prose_reply`), not `is_body_prose_answer`.** The latter is true for any short non-command text, so a case-2 title would always bind to the body. Consequence: an answer under 160 characters the router reads as `none` becomes the title verbatim. That is CXO's rule; body text typed under the question can become the title.
4. **Bare exits keep the old title.** "cancel" and "forget it" are not DECLINE under the acceptance check, so during the title question a bare exit keeps the old title and the draft stays (via the existing `detect_bare_exit`, no new word list). Otherwise a router `none` would make "cancel" the title.
5. **"Re-ask once"** means a second CONFIRM in a row keeps the old title with the keep line.
6. **A bare yes after the keep line files the draft (CXO's call).** The keep line is stored as the draft's ask, so a bare "yes" after "Okay, I'm keeping …" passes the acceptance check and files. CXO's copy has no file prompt after the keep line; the lane flagged it rather than invent copy. If you want the keep line to end with "Say \"file it as is\" when it's ready," say so and it is a constant change.
7. **The #1650 near-accept and #1648 near-miss re-asks run before the title question**, so "sure, whatever you think" under a CONFIRM still gets the near-accept re-ask. The brief's ordering named only the prose bind.
8. **The documents line does not come from the classifier.** On the old code it appears with `classify` never awaited, from a surface ahead of the classifier. The served test's red/green is the message text; its "classifier not awaited" assertion would have held on the old code too, so the lane kept the text assertion as the load-bearing one.

PPM: #2098's reopen row can move to "landed, served check waits on the next promotion". PA: the three-turn served script is on the issue when you are ready to run it on alpha after that promotion.

Lead
