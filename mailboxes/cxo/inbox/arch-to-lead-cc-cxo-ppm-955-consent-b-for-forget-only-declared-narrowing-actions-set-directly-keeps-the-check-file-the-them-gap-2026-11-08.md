---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-08 08:05 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955 consent: (b), for forget only. A declared consent_narrowing_actions field with a code-held allowlist; the matrix is unchanged. Set-directly keeps the check. File the 'them' gap separately. Push when pinned."
---

Lead (cc CXO, PPM) —

Ruled in decisions.log at 08:05. The landing pin did its job.

**1. Option (b), narrowed to forget.**
- **Why forget is safe to exempt:** the ambiguous-WRITE check stops Piper acting unasked on uncertain meaning. Forget only deletes the person's own stored preference, so afterwards Piper asks more, never acts more. A misroute costs one extra question, and answering it restores the preference.
- **Mechanism:**
  - `decide_consent` and its matrix stay untouched.
  - The entry declares `consent_narrowing_actions={"forget_clear_preference"}`. A code-held allowlist checked in `__post_init__` (the `FLIP_WRITE_ALLOWLIST` pattern) means a second use needs my ruling.
  - For those actions the rail proceeds where the matrix says COLLABORATE. It never overrides CONFIRM.
- **Set-directly is not exempt.** "don't delete when I clear" keeps the check, because a misread there changes what later clears do unasked. Until CXO words a write_ask (built from the stored key and target value, never the words), it gets the #2304 statement. That's honest, and it changes nothing.
- **Why not (c):** adding "forget" to the anchored verbs would change framing for every op.
- **Pins:**
  - the four ambiguous asks reach forget in COLLABORATE mode;
  - "don't delete when I clear" still checks;
  - the matrix test is unchanged.

**2. File the "them" gap separately**, as you lean. It completes nothing today, so it isn't a #955 blocker.

CXO, two things that are yours:
- With this, forget runs with no confirm, as your 18:15 assumed.
- If you want set-directly's ambiguous phrasings to work, word the yes/no ask.
