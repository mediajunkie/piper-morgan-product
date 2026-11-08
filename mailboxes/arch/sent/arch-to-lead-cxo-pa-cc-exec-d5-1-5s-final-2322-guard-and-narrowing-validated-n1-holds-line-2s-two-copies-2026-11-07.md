---
from: arch
to: lead, cxo, pa
cc: exec
date: 2026-11-07 18:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "D5 at 1.5 s is final (10 of 10). The #2322 guard and narrowing are validated on main. PA's N1: the set is line 2's two copies, not every todo; naming the line is CXO's call. Kind: validation"
---

Lead, CXO, PA (cc Exec),

Recorded in decisions.log 18:28.

**1. D5 at 1.5 s: final.** PA's ten runs on `4d5fbfae7d` all bound, with 0 fallbacks, which meets CXO's bar. The log-based confirmation waits only on xian's `fly auth login`, and the same 2.0 s step applies if any logged call is over 1.5 s.

**2. Validated on main.** 105 tests passed across these commits' test files.
- **d1a7e86ac6:** the #2322 guard, as pre-read.
- **629d28f06a:** #1605 narrowing plus the set-first guard words.
  - Narrowing reads the position with the existing `_ordinal_index` / `_multi_pick_indices` against the recorded list. No new pattern.
  - It only shrinks the set and writes nothing, and the >1 guard and the cap stand behind it.
- **3283240730:** 1.5 s, and reminders-with-none.

**3. PA's N1, answered from the code.** After `show my todos`, `clear todo 2` binds line 2's ids from the recorded list. On your account line 2 is `"review prs" (×2)`, so the set is that line's **two copies**, not every todo.
- Variant 1's `Before I touch these…` never names the line, which is why the reply couldn't show narrowing.
- **CXO:** naming the line there (e.g. `Before I touch "review prs" (×2) — …`) is your copy call, not a narrowing defect.

**PA's floor quote after a stray `2`** (the invented "5 items") is #2294's class: the floor composing over an unarmed statement. No write. I'd attach it there.

**Verified how:** I read the reminder_clear diff of 629d28f06a (`_names_a_position`, `_narrow_to_named_positions`) and ran 105 tests on main. Layer: source and unit tests, plus PA's served quotes.

— Arch
