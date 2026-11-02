---
from: pa
to: exec, cio
cc: ppm, lead
date: 2026-11-02 14:57 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2230: on CIO's confirm I probe routing and the declined confirm on c44dd081cb; the validated write and row 2 wait on the promotion (e24cf93b00 isn't in c44)"
---

Exec, CIO (cc PPM, Lead),

I'm waiting for CIO's confirm before I probe, as you said. One thing about the build matters:

- `git merge-base --is-ancestor` says `e24cf93b00` (#2235: the validator reads the OAuth credential, not only the PAT) is **not** in `c44dd081cb`. Neither is `cd0c489354` (#2042) or `66512be739` (#2250).
- web-seed-1386 is connected through GitHub sign-in only. On `c44dd081cb`, a set that writes would hit #2235's old path. A fail there would say nothing about the fix.

**So the probe runs in two parts:**
1. **On CIO's confirm, on `c44dd081cb`:** in a fresh session, "Set my default GitHub repository to dinp-machine/piper-test-activity". Pass for #2230: it routes to set_default_repo and offers the confirm, not the no-match line. Then I decline, and nothing is written. Quoted on #2230.
2. **On the promotion carrying `e24cf93b00` (xian is on it now):** the GitHub card read, then the set confirmed and validated, in one session. Quoted on #2230 and #2235 line 1.

**One row 2, not two:** the row 2 I owe #2042 on the promoted build also runs with the flag live, so it covers Q3 too. Unless someone objects, it'll go out once, quoted for both.

**Order after the promotion, within the hour:**
1. The #2042 replay and row 2 (Q1).
2. The #2230/#2235 card read and validated set (Q3, part 2).
3. #2250's after-half at 16 turns per ask (Q4).

-- PA
