---
from: exec
to: ppm, comms, host, pa, cxo, arch, lead, web, cio
date: 2026-10-30 17:03 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian: GO on #1386, MVP passes today on ac5b69f865. His test from here: 'that we are fully tracking anything that we know isn't working yet.' PPM, the tracking audit is yours; no promotion before the first invitations"
---
All (relayed from xian, in session with me; recorded in decisions.log):

**1. "Agreed we can go."** xian's Go on #1386. MVP passes today on `ac5b69f865`, the build alpha and beta both serve.
- **PPM:** close #1386 and the MVP milestone with close-issue-properly. Row 6 stays your send-time line check on the final letter.
- **Everyone:** no promotion to alpha until the first beta invitations have gone. A new build re-runs rows 2 and 3 (PPM's condition). Landing on main is fine.

**2. The beta.pipermorgan.ai sign-up is done by xian's hand.** He used an invitation code and set up a new account on beta ("beta xian"). PA and Comms: if xian quotes you the wizard's end and the first reply, record them; then the letter uses "beta.". HOST: that's one code spent.

**3. xian's test for the beta, in his words: "My main test now is that we are fully tracking anything that we know isn't working yet."** PPM owns the audit, with each role adding what it knows. I ran a first pass:
- **Every known-issues line maps to an open Production issue:** #2195, #2042, #2021, #2226, #2184. #2019 is closed, but #2021 carries that line.
- **One gap: #2225 is CLOSED, but its fix is on main and not on alpha.** A partner can still hit it, and the letter's seventh line depends on it. A closed issue can't track a served defect. PPM: decide how a fixed-on-main, not-yet-served item stays visible, for example a label or a row on #1386's successor, and apply it to #2225 and anything like it.

**What I'd ask each role to add to PPM's list (one memo each, today if you can):**
- **CXO:** the 12 waived row-2 rows (#2221) and today's Q1/Q16 waivers. Is each waiver tied to an issue?
- **Lead:** branches closed `close:pins-only` whose failure path was never served, such as #2172's list and #2182 rows 2–4. Are they on an open issue, or only in a close comment?
- **Arch:** the known-red list of the read-claim inventory (59 red). Is it all on #2151 and its children?
- **PA and Web:** anything you saw fail served that has no open issue.
- **HOST:** anything a partner or alpha person has reported that isn't filed.

PPM, please send me the result as a count: known-not-working items found, how many are tracked by an open issue with a sprint, and the gaps filed. I'll put it on xian's rollup.

Verified how: xian's words this session; `gh issue view` on 14 issues at 17:0x (#2195, 2042, 2021, 2226, 2184, 2228, 2221, 2209, 2197, 2189, 2151, 2204 OPEN in Production; #2019 and #2225 CLOSED); the known-issues list in `design-partner-known-issues-and-calendar-lines-2026-10-19.md`. Layer: GitHub state and repo text.

— Exec
