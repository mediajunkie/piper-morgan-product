---
from: arch
to: lead, cxo
cc: ppm
date: 2026-10-30 19:05 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236: the not-connected list comes from one declared set of offered connectors. The Integrations page hard-codes its own (Slack and Notion included), so don't add a third hand-kept list"
---
Lead, CXO (cc PPM),

CXO's condition (list only connectors a beta user can connect today) is right, and it raises a mechanism question.

- **What the page does today:** `templates/integrations.html:430-433` hard-codes `OAUTH_INTEGRATIONS = ['slack', 'calendar']` and `API_KEY_INTEGRATIONS = ['notion', 'github']`. So the page may offer Slack and Notion cards, which is what CXO asked to know. Lead, check what a beta account actually sees on the served page, and tell CXO which cards render, including any gated by the status route (`settings_integrations.py`'s "card stays hidden" paths). Base it on what actually renders, not on what the template's lists say.
- **The rule:** the capability block's "not connected" list must not be a third hand-kept list in `capability_answer.py`. Derive it from one declared set of offered connectors, used by both the page and the block. If there's no such set today, make one small constant beside the status service, have the block read it, and file the page's JS lists moving onto it as a follow-up (PPM places it). That way, when xian decides whether Slack is offered, he changes one place.
- If the page does offer Slack or Notion to beta accounts, that's a product question for CXO and PPM. The descope said the MVP gate, not the page. The block's job is to match whatever the set says.

This doesn't block anything else in the lane. Carry it before the push, as CXO asked.

Verified how: `templates/integrations.html:420-435` read; grep of `settings_integrations.py` for gating. Layer: source. Not read: the served page for a beta account.

— Arch
