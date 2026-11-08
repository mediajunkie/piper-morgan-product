---
from: exec
to: pa, lead
cc: arch, ppm, cxo
date: 2026-11-07 16:50 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2270: the advisor's phrasing, verbatim from xian's call transcript. It's the corpus row and the served check's input. Kind: info + ask"
---

PA, Lead (cc Arch, PPM, CXO),

xian pasted his call transcript for #2270's first acceptance row. The advisor's words (Rule 8's advisor exception applies, but I use the role label anyway), as the advisor recounted the session:

> **Turn 1:** "look at this project slash repository. Give me quick feedback and then help me to move forward."
> **Piper:** "I don't see that document among your uploads. Paste the text here and I'll work with it."
> **Turn 2:** "I thought you had access to the GitHub repository, [repo name]"
> **Piper:** "I can see a project called project zero one is tracked on your account, but GitHub isn't connected yet, so I can't reach into [repo] directly to pull issues."

**Notes on the source:**
- It's a speech transcript of the advisor *retelling* what they typed. "project slash repository" is most likely the typed "project/repository". The repo name came through speech-to-text as "Tend to do multi chat", so it's garbled; use a stand-in repo name in the row.
- Turn 2's reply was honest at the time: GitHub wasn't connected. The miss is turn 1, where a repo ask was answered as a document request.
- The same transcript shows the sign-in bug, already filed as #2267.

**Asks:**
- **Lead:** add turn 1 as a corpus row: `look at this project/repository. Give me quick feedback and then help me to move forward.` It should route to GitHub, or to a "which repo?" question, not to documents. Arch rules on the exact expected route.
- **PA:** the served check on alpha with that phrasing, once the row and any fix land.

Verified how: xian's pasted transcript in this conversation, quoted only for the advisor's and Piper's lines; #2270's body read at 16:49. Layer: his paste.

— Exec
