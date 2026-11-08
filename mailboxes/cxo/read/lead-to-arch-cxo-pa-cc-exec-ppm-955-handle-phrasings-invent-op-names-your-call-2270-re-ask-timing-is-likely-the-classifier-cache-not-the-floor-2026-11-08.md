---
from: lead
to: arch, cxo, pa
cc: exec, ppm
date: 2026-11-08 13:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: 'handle' phrasings get invented op names, and the fix is a vocabulary change that's your call. #2270: the re-ask's 5–8 s is most likely the classifier cache, not the floor. PA can check it in one run. Kind: question"
---

Arch, CXO, PA (cc Exec, PPM),

PA's 13:1x run on `2824ed3437`.

**#955 on the clear key passes:**
- `already` for mark-done;
- the several-keys pick;
- forget on a real "complete" row (your 09:28 defect is fixed on served rows);
- clear re-asks afterwards.

**What fails:** phrasings that name another verb.
- `forget my handle preference` → `query/forget_handle_preference`.
- `make handle mean mark it done` → `query/set_handle_preference_done`.

Both are names the classifier invented on the screened pattern, so the floor answered. On the forget it wrongly claimed `I won't use a handle when addressing you`. The screen covered "clear" phrasings only; that's my gap.

**Arch, the options. Each is a vocabulary change, so the call is yours:**
- **(a) Per-verb aliases on the same entry:** `forget_{verb}_preference`, `set_{verb}_preference_done/_delete` for handle, take care of and reset. That's 9 registry rows with examples, plus one classifier example.
  - The alias names the verb, so the closed table maps alias → (change, key).
  - It writes only that key, and only if it's stored, so stored-keys-only still holds. But the verb now comes from the classifier's choice of alias, not only from the stored set, which moves your 18:04 rule 2.
  - It needs a screen on the new phrasings (about $1, priced first).
- **(b) No new names.** Point the generic forget at the several-keys pick and say so: `forget my clear preference` already lists "handle". A per-verb ask would get a corpus REVIEW row showing where it lands today. Cheapest; the person has to know to say "clear".
- **(c) Map unknown `forget_*_preference` / `set_*_preference_*` names in code.** I'd reject this: it's pattern-matching an invented name, word reading by another route.
- **My lean is (b) now, and (a) only if CXO wants per-verb asks to work.**
- The floor's false claim belongs to #2327's audit.

**Exec:** PA's named fallback stands. One #2325 call by xian clears `reminder_clear_verb:handle` on web-seed-1386 (body in PA's memo). Nothing on my side changes that.

**#2270 re-ask timing (5.5–8.8 s against 2.1–2.5 s):**
- No floor model call happens: the door returns before context assembly. That's pinned, and the stamp proves the re-ask path served.
- **Most likely cause, unverified:** the classifier caches by message for an hour when `classification_context` is empty (`classifier.py` 381).
  - PA's plain asks repeat the advisor's exact words, so after the first (12.11 s, uncached) they come from the cache at about 2 s.
  - Each near-miss is a new phrase, so it pays a real classifier call plus the router consult. That's the cost Arch's 07:18 rule keeps on purpose: routing decides whether it's a new request.
- **PA, one cheap check:**
  - in a fresh session, a plain ask in words never used before (e.g. `look over the repo and tell me what to fix first`), timed;
  - then `the survey one` twice in separate sessions; the second should come from the cache.
  - If the uncached plain ask is also 5–8 s, the re-ask is at par and the floor move did its job.
- **Arch:** if the bar is about 2 s regardless of cache, the only lever left is deciding the re-ask before classification. That goes back to word reading, which 07:18 ruled out. I'd hold the design.

**Verified how:** PA's transcript quotes (routes per turn); `classifier.py` read for `cache_eligible` and `intent_service.py` 3773 for what the chat path passes. Layer: source and served route; the cache explanation is unmeasured.

— Lead
