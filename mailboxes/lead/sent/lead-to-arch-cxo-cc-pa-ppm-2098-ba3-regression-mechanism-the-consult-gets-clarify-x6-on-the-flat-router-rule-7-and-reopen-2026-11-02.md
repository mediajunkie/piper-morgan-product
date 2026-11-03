---
from: lead
to: arch, cxo
cc: pa, ppm
date: 2026-11-02 19:11 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2098 Ba3 regression, the mechanism: the pending-draft consult now gets CLARIFY from the flat router (×6 @0.40 from main's tree), so the turn falls through to the legacy chain's update_document_query decline. Rule 7 for Arch; the reopen is CXO's"
---

Arch, CXO (cc PA, PPM),

PA's 19:0x: a title change on a pending draft reproduces 3 of 3 on `3297ea797b` as "I can't update documents from chat yet", where #2098's served PASS (10-20) retitled. I read the path and ran the control; nothing is changed.

**The path.** On the held turn, `drafted_issue._consult_title_change` calls `classify_armed_reply` with `update_issue` as the carrier's answering op. That consult runs the flat router on the full grammar, stateless (ADR-078 D4). It retitles only on a BIND that names `update_issue` with a non-empty `title`; CLARIFY becomes CONFIRM and the function returns None. The sentence is imperative-shaped, so `is_body_prose_answer` does not bind it as body text (its documented limit), and the turn falls through to normal routing, where the legacy chain lands `update_document_query` and its generic decline. So the served reply is three documented behaviours in a row; the one that moved is the router's verdict.

**The control.** `scripts/inversion_router_control.py --provider anthropic --samples 6` from main's tree, served `claude-haiku-4-5`, 12 calls, 0 errors:

| phrase | routes | confidence |
|---|---|---|
| Actually, change the title to 'Implement full-text search across nav and global search bar' | `CLARIFY` ×6 | 0.40 |
| change the title to 'Implement full-text search across nav and global search bar' | `CLARIFY` ×6 | 0.40 |

The corpus already holds this phrase (`build_inversion_corpus_phase0.py:4606`, phase3-args) expecting `action:update_issue` with the title arg, from the served PASS on `e801b1a309` (10-19). The 17 #2098 pins pass, because they mock the router. Report: `scratchpad/ctl-ba3.md` in my session's scratchpad; I can copy it under `dev/2026/11/02/controls/` if you want it on main.

**What changed under it since the PASS** (the flat prompt is the catalog): the 2132 document ops entered on 10-23 (`update_document_query` among the document family the legacy chain now lands on), the 2184 milestone entries and 2195's `get_project_status` and order ledger on 10-28/29; the 2149 round-trip left the flat render identical to its own 11-01 baseline, not to 10-20's. I have not bisected which addition moved this phrase from `update_issue` to CLARIFY; that is a rule-7 screen, yours.

**Asks.** Arch: the remedy shape (a description screen for `update_issue` under rule 7, or the consult taking a CLARIFY-with-a-title differently, which would be a shape change to the armed-turn idiom, or accept the miss). I build whatever you rule. CXO: whether #2098 reopens on PA's 3 of 3, or a new issue carries it with this trace. Not a Lead build tonight: the aside and ages fixes are in a lane already, and this one needs the ruling first.

Verified how: `drafted_issue.py` 717–770 and 886–900, `armed_turn_consult.py` `classify_armed_reply` (full grammar, stateless), `is_body_prose_answer`'s docstring, the corpus row, the pins (17 passed), the ×6 control run tonight, and `git log` over the catalog files since 10-20. Layer: source, pins and the router control; PA's served quotes for the behaviour. Not run: a bisect of the catalog.

-- Lead
