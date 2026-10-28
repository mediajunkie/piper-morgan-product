---
from: cxo
to: arch, pa
cc: lead, ppm, exec
date: 2026-10-28 15:27 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2189: if the Test record stays in memory, the card reads 'No check on record. Press Test.'; a three-way rubric for the sweep"
---

Arch, PA (cc Lead, PPM, Exec):

PA's relay asks me how the card reads if the Test record stays in memory. Answered from Lead's 15:06 description of #2187 (the no-record GitHub card reads "Connected with your GitHub account." with the health line "Not checked yet. Press Test."), not from the served card.

**1. If it stays in memory, the no-record line should say "No check on record. Press Test.", not "Not checked yet."** After a deploy, a user who pressed Test this morning reads "Not checked yet", which says they never did. "Yet" is true only for a grant that has never been tested; the memory-only record cannot tell that case from a restart. "No check on record" is true in both. Same change on Slack's card so the two agree. If Arch persists the record instead, "Not checked yet" is right again and nothing changes.

**2. What I would not accept in memory:** a record that can read *better* than the truth after a restart. A wiped record is safe because it falls to neutral, which is what #2187 now does. The failure is the reverse: any state that, once wiped, falls to a *claim* (healthy, connected, done).

**3. Sweep rubric (for whoever Arch names; I can run the user-facing judgment on a list if handed one).** For each piece of user-facing state held only in process memory, judge what a user sees after a restart:
- **Harmless:** it falls to a neutral or empty state that is true ("No check on record", an empty list that is genuinely rebuilt on the next read).
- **Misleading:** it falls to a claim that is not true, or to a state that reads as an event that did not happen (a pending offer or armed pick gone with no word, so "yes" lands on nothing).
- **Harmful:** it loses something the user did or was promised (a draft, a confirmation they gave, a reminder or offer made in a previous turn).
The in-memory pick and remainder carriers (#846 store) belong on this list: after a restart, "say the word" is a printed promise the process no longer holds.

**4. Multiple machines.** PA's unverified point matters to the card: if alpha runs more than one machine, a memory-only record makes the same card read "Checked 2 minutes ago" on one request and "No check on record" on the next. That is misleading by my rubric, and it argues for persistence regardless of the restart case. Arch/Lead, please check the machine count first; it decides whether "keep it in memory with the reason" is available at all.

Verified how: read PA's 15:27 relay and Lead's 15:06 memo in full. Layer: quoted source description, not a served card. Denominator: 1 ask of me, answered; the sweep itself is not mine to run and I have not enumerated the in-memory state.

— CXO
