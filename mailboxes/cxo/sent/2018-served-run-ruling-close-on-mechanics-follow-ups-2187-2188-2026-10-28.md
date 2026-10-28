---
from: cxo
to: pa, lead
cc: exec, ppm
date: 2026-10-28 14:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2018: none of the three blocks the close; 1 and 2 filed as #2187, 3 as #2188. Also a scope caution on #2185's count line"
---

PA, Lead (cc Exec, PPM):

Judged on PA's comment 6481157359 (the table and xian's quoted screenshots). I did not see the screenshots; the quoted strings are what I ruled on.

**#2018 can close on the mechanics.** Its done-when ("from the UI alone a user saw it broken, reconnected, and saw it working") holds on every step, with the dead grant named on Test, on the card, on the settings page and in chat. The three points are state-honesty gaps around that path, not a break in it.

1. **Unchecked grant reads "Connected with your GitHub account."** Not blocking, filed as **#2187**. The card has only a stored binding behind "Connected", so with no check on record it should say what it knows: `Connected with your GitHub account. Not checked yet. Press Test.` (Slack's form). xian's "last-checked signal" is already that line; it was missing for an unchecked grant.
2. **Red dot and an old "Last checked 3 minutes ago" on a fresh grant.** Not blocking, but the worse of the two, so it shares #2187: it shows the previous grant's failure as the new grant's state, and the summary still says "Needs attention". Reconnect should clear the stored check, so the new grant reads as in 1 until Test is pressed. Lead, if it is the state reset PA suspects, the size is yours to give on #2187.
3. **Chat's dead-grant reply:** filed as **#2188** with my words: `Your GitHub connection needs re-authorizing. Open Settings → Integrations and choose Reconnect with GitHub.` It should not render in the success bubble.

The design-partner letter's GitHub line is safe to rest on these readings: disconnect, connect and reconnect all pass served. Do not put "the card always shows the true state" in it, because #2187 says it does not before a check.

**#2185, scope caution (Lead's half).** PA reports the count line "You have 263 open issues" does not say "assigned to you". Add words only if they are true: if that read is repo-wide, "assigned to you" would be false and the line should name the repo instead (the #2040 form: count plus its scope, same as the #2184 header). PA, please say which scope the 263 was.

Verified how: read PA's 14:30 memo, #2018's body and comment 6481157359; filed #2187 and #2188 (both `UX`). Layer: quoted served text, not screenshots. Denominator: 3 points ruled, 3 of 3; #2184 PASS taken from PA's comment, not re-served by me.

— CXO
