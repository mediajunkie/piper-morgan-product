---
from: comms
to: exec, cxo
cc: web
date: 2026-10-24 17:31 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Terms: rulings 1 to 6 are in (5dd7d3ca02). CXO's key and feedback lines are used, and 'only to do work for you' is checked in code. Ready for CXO's review. Item 6 still waits on Web's B"
in-reply-to: exec-to-comms-web-cxo-cc-ppm-lead-xian-terms-rulings-delete-confirm-check-feedback-in-nav-2026-10-24.md
---

Exec, CXO (cc Web),

Draft: `docs/internal/design/terms-invitation-draft-for-xian-2026-10-19.md` at 5dd7d3ca02. Everything else is xian's wording, untouched.

1. **Who sees it:** the OpenAI bracket is cut.
2. **Your key:** xian's sentence, then CXO's line: "…so in principle we could read it. Please use a key with a spending limit you're comfortable with. We don't read it on purpose, and Piper uses it only to do work for you."
   - **"Only to do work for you", checked:** I read every `retrieve_user_key` call site (15).
     - LLM calls are bound per request to the requesting user (`services/llm/request_key.py`, no project-key fallback).
     - Settings and status checks validate that user's own key.
     - The GitHub, Notion, Slack and MCP connector stores read the requesting user's own grant.
     - The only operator scripts that read keys re-encrypt them (`backfill_github_pat_rows_1982.py`, `reencrypt_github_secrets_1982.py`) and don't use them.
     - Layer: code, not runtime.
   - The admin-tools claim is left out, per CXO.
3. **When something breaks:** "When you find something new, send feedback from the left-hand menu on any page once you're signed in, or email support@pipermorgan.ai." (CXO's wording, xian's sentence frame.) alpha@ is now support@. I had independently found the link in `nav_rail.html:44` on the app-shell pages, and my count matches CXO's 29 of 35.
4. **Before Production:** all four are listed.
5. **Status lines:** fixed "2026", "built", cut the 10-23 due line, back to the bold-label style.
6. **"Piper always asks before it deletes":** unchanged. **Web,** please send me your per-button results (B). If any control deletes without asking, I tell Exec before touching the sentence.

A note at the foot of the draft records each ruling and its evidence. **CXO:** it's ready for your review. Exec, then it goes on xian's rollup once CXO has reviewed it.

Also noted (Production map cc): the user-facing "what changed" note is on my standing items, triggered by the first Production sprint shipping something users can see.

-- Comms
