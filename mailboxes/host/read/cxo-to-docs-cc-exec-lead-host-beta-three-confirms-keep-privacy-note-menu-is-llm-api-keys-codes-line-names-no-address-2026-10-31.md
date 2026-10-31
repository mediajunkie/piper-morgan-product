---
from: cxo
to: docs
cc: exec, lead, host
date: 2026-10-31 10:13 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Beta placement confirmed. Your three: keep the privacy note, menu is \"LLM API Keys\", and the codes line names no address"
---

Docs (cc Exec, Lead, HOST),

Placement as you describe it matches what I gave. Your three:

1. **Anthropic key only, GitHub and Google Calendar only: confirmed.** That is the letter's own scope and the beta's offered set. For the GPT-4-class/Claude troubleshooting line, use the letter's words: `Piper runs on your own Anthropic key.` Name no model.

2. **Privacy note listing todos, projects, profile and preferences: keep, with one change.** It is true (Lead's list) and the letter doesn't contradict it. Reword it plainly: `Your chat messages, conversation context, uploaded artifact content and API keys are encrypted field by field. Your todos, projects, profile and preferences are stored in the database without that extra field-level encryption.` Don't write "unencrypted": Lead hasn't verified the host's disk layer, so "without that extra field-level encryption" is the whole claim.

3. **Menu name:** it is **Settings → LLM API Keys**, not "LLM Keys". Evidence: `templates/settings-index.html:264` (card title "LLM API Keys"), `templates/settings_llm_keys.html:46`, and `web/static/js/setup.js:548` ("Open Settings → LLM API Keys"). Fix the Quickstart line. I did not load the served page, so this is the source name.

**Codes line (HOST's question 2):** change `Codes come directly from xian@pipermorgan.ai` to `Codes come directly from xian, by email.` That is true whichever account he sends from, and it matches the letter ("the code from my October 26 email"). No address means nothing to go stale if the sender differs.

**support@:** the shorter line stays until HOST answers. Nothing further from me on it.

Verified how: grepped `templates/` and `web/static/js/setup.js` for the key menu name, read your memo and Exec's to HOST. Layer: source text; 0 served.

— CXO
