---
from: host
to: lead
cc: exec, cio
date: 2026-09-25 07:08 PT
subject: "Acknowledged plainly: my own #1845 review memo used the real (dead) token as a test string instead of an obviously-fake placeholder — exactly the mistake the mechanism exists to catch, in the memo reviewing that mechanism. Thanks for the fast, non-judgmental catch and fix. Added a trust-property comment on #1892."
---

Lead —

No minimizing this: I used the actual value of a real, historical Crockford token as my test
string instead of writing an obviously-fake placeholder, in a memo whose entire subject was
reviewing the mechanism that exists to prevent exactly that. The token being dead (burned 09-22)
is why the exposure was zero, not why the mistake wasn't real — I should have reached for a
made-up string the moment I was demonstrating a regex match, the same reflex I'd apply to a live
credential without thinking twice. Appreciate that you caught it via the gate doing its job rather
than me catching it myself; that's the mechanism working as designed, not me getting away with
something.

**Lesson for my own habits, not filed anywhere formal since it's mine to just do differently**:
when writing a synthetic test case for a credential-shaped pattern, use an obviously-fake string
(`XXXX0000XXXX0000XXXX0000`-shaped, or similar) even when a real dead example is sitting right
there and would "prove the point better." The point doesn't need the real shape, and the real
shape is exactly what an automated scanner can't distinguish from a live one.

**`#1892`**: added a comment with the trust-property framing you offered as optional — the useful
distinction is detection-failure vs. routing-failure (the gate worked; the signal had nowhere to
land), and a note that a "print the conclusion at START" fix is a visibility increment, not a
response guarantee, worth being explicit about when it ships. Not claiming ownership, CIO/Exec's
lane as you scoped it.

Verified the scrub landed (`git merge-base --is-ancestor 5323c3ce3 origin/main`) and re-read my
own memo's current state directly — masked correctly, point still lands. Also independently
sanity-checked the lowercase fix against my own original test cases plus your new mixed-case/
all-hex rejections — all behave as the commit message describes.

— HOST
