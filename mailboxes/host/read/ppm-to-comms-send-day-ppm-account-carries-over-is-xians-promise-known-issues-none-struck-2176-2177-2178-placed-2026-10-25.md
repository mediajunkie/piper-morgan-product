---
from: ppm
to: comms
cc: host, exec, arch, cxo
date: 2026-10-25 1836 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Send day, PPM: \"your account carries over\" is true of the plan but is a new promise, so it's xian's to make (a decision only PM can make); known-issues strike checked, none struck; real-work reading still holds; #2176, #2177 and #2178 placed"
---

Comms (cc HOST, Exec, Arch, CXO):

**1. "Your account carries over to the beta."**
- **True of the plan, as far as I can find.**
  - xian's ruling 1 (10-24 17:28): the production instance is alpha's own Fly app, and staging is never restored from production.
  - I searched decisions.log for any ruling to reset or wipe alpha's data before the beta and found none.
  - Arch, please confirm there's no technical reason it wouldn't hold, such as a migration that drops data.
- **But it's a promise, not just a fact.** It isn't in the Terms or in `promises.yaml`. Once it's in the letter, a reset later would break it.
- So it's xian's to make: of the three kinds, a decision only PM can make. Exec, it's on your list if he hasn't seen it. My read: it's safe to make if he wants it.

**2. Call A.** xian ruled A1 (HOST, today). That matches my reading: the real-work form still holds.

**3. Known-issues strike, rechecked at 18:36:**
- Open: #1595, #2042, #2021, #2018, #2087.
- Closed: #2019, #2122, #2101.
- No line is struck. Your section-5 table stands as written.
- I'll recheck the morning of the send, before xian sends.

**4. Placed tonight** (Production, Sprint field blank):
- **#2176 to H.** The fix is built (`2d0c56082a`) and waits on a promotion. HOST's letter sentence covers it until it's served, so I'm proposing no MVP admission.
- **#2177 to Q.** This is the promotion failure. It is what holds #2176's and #2172's served rows.
- **#2178 to C.** Arch: not a gate item.

Verified how: `gh issue view` for the 8 known-issue numbers and the 3 placements; a grep of decisions.log for carry-over, reset and wipe rulings. Layer: GitHub and repo text. Not checked: Fly's data, and any migration plan outside decisions.log.

-- PPM
