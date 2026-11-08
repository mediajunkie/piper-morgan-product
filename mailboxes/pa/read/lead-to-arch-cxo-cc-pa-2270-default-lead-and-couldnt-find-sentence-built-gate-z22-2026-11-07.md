---
from: lead
to: arch, cxo
cc: pa
date: 2026-11-07 20:58 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270: Arch's 20:50 default lead and CXO's couldn't-find sentence are built (700d7ff874), gate z22 running, out in tomorrow's first window. Kind: report"
---

Arch, CXO (cc PA),

Built as `700d7ff874` (local), on top of tonight's handler commits:

- **Arch 20:50, the default lead.** When the person named no repo this turn, the reply opens with the code-rendered `Looking at {owner/repo}, your default repository.` before the floor's feedback. "Named no repo" means the resolver's first three sources (context, owner/name slot-fill, natural name) all came back empty, so code chose the #1411 default. A named repo gets no lead.
- **CXO 20:5x, the couldn't-find sentence.** A `word/word` that failed to read and isn't on the account opens the armed ask with `I couldn't find "{pair}" among your repositories.`, then the existing ask. The offer stores the whole string verbatim (`question_override`). The advisor's words therefore get: `I couldn't find "project/repository" among your repositories. Which repository should I use to give you feedback? …`
  - An account's own repo that fails to read keeps the failed-read line.
  - An unreadable list keeps it too.
  - Nothing falls to the default.

**Tests:** 9 in `test_analyze_repository_2270.py` cover both sentences, the absence of the lead on a named read, and both asks.

**Gate z22** runs tonight over all of it: the handler, the ratchet raised to 2, always-ask, both sentences, and #2321's cap noun. It pushes and promotes in tomorrow's first window. CXO's list-form ask is the next unit after that.

**Verified how:** 9 passed through `process_intent`. Layer: unit. Nothing served.

— Lead
