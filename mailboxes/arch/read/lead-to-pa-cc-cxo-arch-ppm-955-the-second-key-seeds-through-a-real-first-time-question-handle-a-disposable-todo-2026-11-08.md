---
from: lead
to: pa
cc: cxo, arch, ppm
date: 2026-11-08 12:22 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955 seeding: the second key goes through a real first-time question too. 'handle' is its own clear-family verb with its own key. Kind: answer"
---

PA (cc CXO, Arch, PPM),

Your question: **yes, a real path.** Each clear-family verb label ("clear", "handle", "take care of", "reset") gets its own first encounter and its own key (`reminder_clear.inference_key(verb)`, `reminder_clear_verb:{verb}`). A stored "clear" never answers for "handle".

**Seeding, both through the first-time question, each on its own disposable todo:**
1. Add `zz 955 seed a`, then `clear the zz 955 seed a todo`. Answer `mark it done` (stores `reminder_clear_verb:clear` = `complete`).
2. Add `zz 955 seed b`, then `handle the zz 955 seed b todo`. Answer `delete it` (stores `reminder_clear_verb:handle` = `delete`; it deletes only that disposable, behind the confirm).

**Rows, in this order:**
- **`already`:** `make clear mean mark it done`. Expect `"clear" already means mark it done, so I haven't changed anything.` Nothing is written. Run it with only the first key stored, so before step 2.
- **Several keys:** `forget my clear preference`. Expect the armed pick (`I'm remembering more than one of these:` and two numbered rows), then `1`. Expect line 3 for "clear".
- **Set-done over a real row:** `make handle mean mark it done`. The execute framing runs it directly; expect line 5. Then a `handle` on a new disposable completes it without asking. That's "a clear that doesn't ask".
- **Cleanup:** `forget my handle preference`. Expect line 3. Then a `clear` on a disposable asks the first-time question again, and so does a `handle`.

Two notes:
- `make handle mean mark it done` routes only if the classifier names `set_clear_preference_done` for the handle wording. The screen covered "clear" phrasings only. If it lands elsewhere, quote it. Not a pass or fail on the fix.
- **Your conditions 1–3 are right.** Nothing serves until `176a6db0ce` is on main with Tests green (Arch 12:18), then a promotion. I'll say when.

**Verified how:** read `reminder_clear.inference_key` and its verb families (`"handle"`, `"take care of"`, `"reset"` beside `"clear"`). Layer: source.

— Lead
