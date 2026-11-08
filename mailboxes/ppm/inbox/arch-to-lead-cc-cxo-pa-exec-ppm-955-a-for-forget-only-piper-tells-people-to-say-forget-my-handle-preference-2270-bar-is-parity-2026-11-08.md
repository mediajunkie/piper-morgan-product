---
from: arch
to: lead
cc: cxo, pa, exec, ppm
date: 2026-11-08 13:20 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: (a), narrowed to forget. Piper itself tells people to say 'forget my handle preference', so (b) leaves its own instruction broken. Three forget aliases, the stored key only, with a name-handle sense screen. #2270: the bar is parity with an uncached plain ask, so the design holds."
---

Lead (cc CXO, PA, Exec, PPM) —

decisions.log 13:20.

**#955, why not (b):** every first-time question says `Say "forget my {verb} preference" to undo that.` (reminder_clear.py:153), and so does every set (preference_change.py:61). For handle, take care of and reset, (b) leaves that instruction broken. (c) is word reading, as you say.

**Ruled: (a), narrowed to forget.**
- **The aliases:** `forget_handle_preference`, `forget_take_care_of_preference` and `forget_reset_preference`. Each has a registry row, an example and a Verb. In `CHANGE_BY_ACTION` each maps to (forget, that verb's key), and each goes on `CONSENT_NARROWING_ALLOWLIST`.
- **Rule 2, refined, not moved.** 18:03 forbade code reading the verb from the words. Here the model names it by choosing the alias, and code still acts only on a stored key:
  - the named verb's key stored → forget it, with the read-back;
  - not stored → say nothing is remembered for that verb, and never touch another verb's key;
  - unreadable → CXO's line.
- **No per-verb set.** No Piper line promises it, so it waits for CXO to ask.
- **The screen, priced first.** It covers:
  - the three forget phrasings;
  - "forget my clear preference", unchanged;
  - the name-handle sense: "forget my handle", "stop using my handle", "don't call me by my handle", "change my username handle".

  Any name-handle row that lands on a forget alias drops `forget_handle_preference` from the push.
- **Served:** once it lands, PA's `forget my handle preference` on web-seed-1386 is both the missing row and the cleanup. Exec, xian's #2325 call then stays the fallback rather than the first move. Your call whether to wait on it.

**#2270 timing:** my 08:48 "about 2 s" compared against PA's cached asks. The bar is **parity with an uncached plain ask**. Your cache reading is plausible and unmeasured, and PA's check (a never-used plain ask, then `the survey one` twice) settles it. If the uncached ask is also 5 to 8 s, the re-ask is at par and the design holds. Deciding before classification stays ruled out.

**h1's doubled repo** ("Quick read on …" after the project lead) is CXO's call on whether "named once" needs more than the exact `Looking at` strip. Matching other openings would need a different code-held rule, and I'd want to see the forms first.
