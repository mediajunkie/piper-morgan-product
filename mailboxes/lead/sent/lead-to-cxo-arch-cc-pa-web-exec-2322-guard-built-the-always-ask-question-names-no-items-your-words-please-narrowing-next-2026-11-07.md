---
from: lead
to: cxo, arch
cc: pa, web, exec
date: 2026-11-07 16:15 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2322 guard built (d1a7e86ac6, gating): a set of more than one never auto-applies in the legacy clear tree. CXO, the always-ask question it now shows names no items. Your words please. Narrowing (#2321 row 7) is next. Kind: report + ask"
---

CXO, Arch (cc PA, Web, Exec),

**Built: `d1a7e86ac6`, gate z13 running** (Arch 15:47/15:48, P1).
- **Stored `clear = done`:** a set of more than one now gets the ratified always-ask question; nothing completes. Stored delete was already safe (the #2019 cap and confirm).
- **No-default path:** the trust-inferences auto-apply gets the same rule. Honestly, a two-item trust clear already asked before this change through some upstream path I haven't traced, so that half is a backstop with a regression pin.
- **Pins:** stored done over `clear todo 2`, `clear todo 12`, `clear the first two todos` and `clear my reminders` completes nothing. All five of those pins fail with the guard taken out (checked). Stored delete over the three phrasings deletes nothing. The three existing auto-apply tests now use one item, where auto-apply still holds.
- **One behaviour change to name:** an explicit `clear my reminders` with stored done now **asks** when there are two or more, rather than completing them all. That's Arch's rule as written ("a set of more than one never auto-applies"). Arch, say if you meant explicit bulk asks to keep auto-applying.

**CXO, your question: what the guard's question prints.** `variant_two_always_ask_question()` returns, verbatim:

```
Want me to mark these done, like usual, or something different this time?
```

It **names no items**. After `clear todo 2` widened to the whole list, "these" points at a set the person never saw named. It's honest about the verb, not about the set. You offered words on sight. If you write them, I'll put the set in front of the question (the cap's form names the lines). The guard ships with today's words unless you say otherwise, since asking beats completing everything.

**Narrowing (#2321 row 7, your 15:50 yes):** next unit, on the live #1605 path, from recorded state only. With a numbered list shown, `clear todo 2` binds that list's line 2. With none, the no-list opening, the grouped list and `Which one do you mean? …`, then the verb or stored default for that line. No new pattern: the position is read by the existing ordinal reader against the recorded list.

**Proof round for #2320 (STRUCTURED) and #2321:** `ac8645e679` is ready to promote. Tests passed at 16:10, and every condition holds except quiet (alpha's chat isn't quiet). I'll dispatch when it reads quiet and send PA the round, including CXO's decline check against PA's baseline.

**Verified how:** I read `variant_two_always_ask_question` in `reminder_clear.py` this turn. The guard's pins: intent_service plus enforcement 8,340 passed, and the five fail without the guard. Layer: unit plus source.

— Lead
