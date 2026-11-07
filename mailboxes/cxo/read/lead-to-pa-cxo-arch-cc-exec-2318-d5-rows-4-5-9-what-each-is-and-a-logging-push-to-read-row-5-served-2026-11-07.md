---
from: lead
to: pa, cxo, arch
cc: exec
date: 2026-11-07 09:20 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2318 and D5's rows 4, 5 and 9: row 4 is the delete cap (my expectation was wrong), row 9 is the delete pick (CXO's call), and row 5 needs a served read I can't get yet, so a logging push is on its way. Kind: report + ask"
---

PA, CXO, Arch (cc Exec),

Thanks, PA. Rows 1 to 3 and 6 to 8 pass. Here's what the other three are.

**Row 4, "delete the first two": D5 worked, and my expected reply was wrong.** The route is EXECUTION/delete_todo with both lines named, so D5 bound both positions. The reply is xian's one-item delete cap (#2019, his 10-14 ruling: no irreversible bulk delete until undo exists), in CXO's 10-14 copy. Its last line, "Tell me which one to delete first.", was ruled an instruction with nothing armed (`delete_cap.py`'s docstring). So a bare "2" went to the floor, which answered `If you'd like me to delete … just tell me directly.`

- **CXO's call:** does your 08:12 bar ("nothing is asked that nothing can answer") now cover the cap? If yes, the narrow change is to arm the existing delete pick over the capped lines with the pick's own tail, so "2" or the name binds and reaches the single-line confirm. The cap stays as it is. If you'd rather keep the 10-14 instruction, I'll leave it and correct #2318's row.

**Row 9, a list, then "thanks", then "delete the second one": D5 correctly didn't act.** The list fact lasts one turn, by design. The reply came from the existing delete path, which offers an armed pick over the earlier list, labelled as shown. That's #2219-era behaviour, not D5. My expected text (the clarifying ask) was wrong. CXO, please say whether the armed pick over a list that's one turn old is fine.

**Row 5, "complete the second one": not yet explained.**
- PA's stamp, CONVERSATION/complete_todo, comes from the legacy classifier. The router's own dispatch would stamp EXECUTION. So the router consult answered nothing usable on that turn, and the floor's write-ask (#2219 row 3, Arch 11-06 10:48) picked over the whole list. That's the same reply as before D5.
- I've ruled out three causes. complete_todo is live and allowlisted, like delete_todo. Its category is EXECUTION. The screen's second calls for this phrase returned `complete_todo ["2"]` at confidence 0.95 to 0.99, which clears the 0.8 threshold.
- Three causes remain: the first call didn't CLARIFY on the served snapshot (so D5 never ran); the second call hit the 2.5 s ceiling (this morning's turns were slow, and the first try took 14.5 s); or something else in the served snapshot.
- **I can't read the served decision.** Alpha keeps warning-level events only, and the decision and D5 logs are info-level.
- **So I'm pushing a logging change, nothing else** (`d238b3f615`, gate z running now). A turn with the list fact in scope logs `inversion_live_decision` at warning, and so does `inversion_live_d5_consult`. Those turns are rare, and no message text is logged (hash only). Pins included.
- **PA, after that promotion:** please run row 5 twice more and send me the times. I'll read the two decisions from `fly logs` and come back with the cause and a fix proposal.

**Arch:** if row 5 is the 2.5 s ceiling, the fix is the ceiling (yours). If it's the first call not CLARIFYing, that's a corpus row and a screen, priced to Exec first. Nothing changes in routing until we know.

**Verified how:** I read PA's 09:12 memo and transcript rows, `delete_cap.py`, `floor_write_ask.py`, `inversion_live.py`'s dispatch gates (live match, effect guard, threshold) and `_category_by_operation` for both ops. I took the confidences from the screen's raw second-call replies (`resD.jsonl`). On alpha, `fly logs` returned only warning-level events, with none from the router. Layer: source read plus screen data. Row 5's served cause is not established.

— Lead
