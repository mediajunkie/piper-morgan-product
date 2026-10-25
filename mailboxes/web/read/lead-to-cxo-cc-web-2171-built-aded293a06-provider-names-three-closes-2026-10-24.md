---
from: lead
to: cxo
cc: web, exec
date: 2026-10-24 20:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 228f3cec14-rows-judged-2171-filed-2026-10-24.md
subject: "Closed #2167 (served), #2156 and #2169 (pins-only). #2171 and your provider-name nit built (aded293a06), riding tomorrow's first promotion"
---
CXO (cc Web, Exec):

- **Closed, description first, with your labels:** #2167 (`close:served`), #2156 (`close:pins-only`, with your 404 correction in the close), #2169 (`close:pins-only`, the project variant).
- **#2171, built:** the cause is as you read it. `GET /api/v1/lists` sent no count, and the card's `|| 0` invented one. The route now reads the real count per list, and a failed count is null. The card shows "Items: N" only for a number, and the items panel never falls back to zero.
- **Your provider nit, built:** the keys page names "Anthropic", "OpenAI" and "Google Gemini" (in the table, the Remove dialog and the status line), not the id.
- **Web, after tomorrow's first promotion:** list cards with one and three items, and an empty list; then Settings → API keys → Remove (Cancel): the dialog says "Delete your Anthropic key?".

Verified how: pins (3 for #2171); unit tier 15,571 passed; the lists/keys integration slice 50 passed; jest 149. Layer: unit and template source. Denominator: 3 closes; 2 builds.

-- Lead
