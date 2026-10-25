---
from: ppm
to: exec
cc: cxo, lead, comms, arch
date: 2026-10-24 1747 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "For xian (a decision only he makes: an admission): #2167 as Gate class 3, the key dialog's 'we destroy our copy immediately'. Also #2166 placed (known-issues line proposed), #1325 closed per ADR-081, #2168 rubric filed, the PDR-001 beta check on the checklist"
---

Exec (cc CXO, Lead, Comms, Arch):

**1. For xian: admit #2167 to MVP as Gate class 3 (honesty), a must-close. I recommend yes.**
- **The problem:** the API key Remove dialog says "we destroy our copy immediately". It's served on alpha `89b8c3d8b6`, as CXO quoted from Web's rows. Encrypted backups keep the key for up to about five days, and the invitation's key line says exactly that.
- **Why it matters:** a partner reads this dialog at the moment they delete their key, and it contradicts the Terms they were just given.
- **Cost:** one string. CXO's replacement words are in the body, plus Lead's check of the insights Start-fresh dialog ("permanently deletes" next to "We keep it for a while").
- **Close condition (CXO):** the new dialog quoted served on alpha.
- **Gate:** if admitted, 3 -> 4 open, 1 must-close.
- **Meanwhile:** it sits on Production, H.
- **Class:** it's Class 3, not 1 or 2, so my "no Class 1 or 2 open" line stays true either way.

**2. #2166 (Share broken end to end):**
- **Placed:** Production, E. It isn't a gate item, because the dialog shows an error toast on failure and never claims a share happened (`todos.html` ~L653-659).
- **Known-issues line, yes. Comms, a proposed sentence:** "Sharing a to-do, list or project with another person doesn't work yet; you'll see an error if you try." Lead adds the share-Remove confirm with the fix, per your 17:42.

**3. Arch's ADR-081 asks:**
- **#2163** already was the F5 tracking issue (filed 17:3x). It now carries the ADR link and each of the six issues' fate under D1 to D7.
- **#1325 closed** as superseded by D5.

**4. CXO's asks:**
- **#2168 filed** (PUB): ratify the plugin surface rubric v0.1 and run it per increment. Linked from each of #1701 to #1707 as their precondition.
- **The PDR-001 beta check** is linked on #1538 and is a row in `beta-formalities-checklist.md`, set to run in each beta wave. I set no precondition on invitations; timing the waves is xian's.

**5. Rule 8, an old mention, for you:** #1538's body names an outside alpha tester by first name and initial ("Source: …"). I haven't edited it. Removing old mentions is xian's call.

Verified how:
- `gh issue view` on #2166 and #2167 (Production);
- `gh issue view 1325` (CLOSED NOT_PLANNED);
- #2168 created (Production, Sprint PUB) and its comments on #1701 to #1707 posted (7 of 7);
- the `todos.html` share handler read;
- the checklist diff read.

Layer: GitHub state and source. #2167's served quote is CXO's reading of Web's row, which I haven't verified.

— PPM
