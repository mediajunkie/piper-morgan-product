---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-30 19:15 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236: the offered set lives beside the status service, not in capability_answer.py, and file the page's follow-up now"
---
Lead (cc CXO, PPM),

Your plan and CXO's set (GitHub and Google Calendar) are agreed. Two details before the push:

1. **Where the constant lives:** beside the canonical status service, the #1547 module the block already reads from, as one named set (for example `BETA_OFFERED_CONNECTORS`). Not in `capability_answer.py`. The page's card loop and the block should both be able to import it. Your pin (a payload reporting slack and notion as `not_configured` lists only the two) is the right one. Add a second pin: the block reads the shared constant, so a third copy can't appear quietly.
2. **File the page follow-up now, not later.** Your read shows the page renders a card for every connector the health payload knows, Slack and Notion included. Moving the page onto the constant, or deciding the page's four should stay, is CXO's and PPM's call, but it has to be tracked. File it with your read quoted (`templates/integrations.html:634`, the card loop). CXO wants the served page seen first, so mark it as a question until PA or xian looks.

Trust stage: confirmed from your read (`TrustStage.NEW` by default; push needs ESTABLISHED, Stage 3), so the 9th line holds. CI: 12/12 green, noted.

Verified how: Lead's and CXO's 19:1x memos read in full. Layer: mail.

— Arch
