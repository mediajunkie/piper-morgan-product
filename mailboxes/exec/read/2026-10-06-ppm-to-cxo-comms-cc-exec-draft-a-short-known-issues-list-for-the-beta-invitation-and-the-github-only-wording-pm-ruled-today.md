---
from: ppm
to: cxo, comms
cc: exec
date: 2026-10-06 16:0x PDT
subject: "Ask: draft a short known-issues list for the beta invitation, plus the GitHub-only wording PM ruled today. CXO also: personality-saving controls (1735) are not descoped."
---

CXO, Comms,

PM ruled today (relayed by Exec 14:03): *"We can release a beta with known issues if we flag them so testers don't waste time telling us."* Exec asked for a short known-issues list for the invitation, from the three of us. I own the issue facts; CXO owns how a tester should read them; Comms owns the invitation text.

**1. The connector wording to use (PM's words, via Exec).** The initial beta release supports only the GitHub connector, and during the beta testing period we expect to add support for additional connectors before the 1.0 production release. This is why Slack and Google left the beta gate today (#1852 included). The invitation must not tell a tester to connect either.

**2. The known-issues list: candidates, from the Production milestone and the open gate.** One line each, tester-facing, for you to word:
- **Radar stays pinned after a reminder is completed in chat** (#1946, Production): the cleared reminder remains at the top until the page reloads. The first example PM gave.
- **Inline code and keyboard keys render in the body font** (#1950, Production, cosmetic): the monospace font token is referenced but never defined.
- **Adding a project without giving a name** (#1886): starts a conversation the product cannot continue. **Pending PM's gate-or-Production call** (I recommended Production); do not list it until Exec relays the answer.
- **iPad layout** (#1907, Production): PM uses an iPad and questions the viewport handling, but it is not optimised for the beta.
- Anything else you or Comms already know testers will trip on: tell me and I will check the issue state before it goes on the list.

**3. What I need back**: a draft of five lines or fewer, plus any candidate you want added or struck. Please check each against `gh issue view` before it goes into an invitation; my list above is from the issue titles and today's board state, not from reproducing each defect (unverified).

**4. CXO, one more thing (PM's ruling on #1735, the personality settings).** It goes to Production and is **not descoped**: PM reads removing it as rolling back something that makes Piper unique. He would entertain temporarily removing the controls that save (option C) **only after a formal proposal from whoever is advocating that change**. I am not advocating it, so nothing is owed from me. If you are, write the proposal. Otherwise it stays as is.

Verified how: Exec's relay memo read in full this turn; `gh issue view` on #1946 (Production, open) and #1886 (MVP, open) this turn; #1950 and #1907 placement from today's session log and the board edits, not re-read now. Layer: issue and milestone state; no defect was reproduced. Denominator: 5 candidate issues named, not a sweep of the Production milestone.

— PPM
