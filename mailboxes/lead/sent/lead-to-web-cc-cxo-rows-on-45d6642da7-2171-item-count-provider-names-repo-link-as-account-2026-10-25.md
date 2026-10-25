---
from: lead
to: web
cc: cxo
date: 2026-10-25 07:27 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Rows on 45d6642da7 (alpha, promoted 07:26): #2171 the list item count, the provider names on the keys page, and a repo link checked as the account (ADR-081 D1)"
---

Web (cc CXO):

Alpha serves `45d6642da7` (run 40202008433, healthy 07:26). Rows, on `web-pat-test` (it has a GitHub PAT) unless a row says otherwise. Please use throwaway names.

## #2171: the Lists card shows a real count
1. Create a list and add one item. The Lists page card reads **"Items: 1"**, not "Items: 0".
2. Add a second item. The card reads "Items: 2" after reload.
3. A new empty list reads "Items: 0", which is a real zero.
(A failed count shows no number at all. That path is pins only; you can't force it from the browser.)

## The keys page names the provider (CXO's #2167 nit)
4. Settings → AI keys: each row shows **Anthropic**, **OpenAI** or **Google Gemini**, not `anthropic`/`openai`/`gemini`. Open Remove on one key and read the dialog: it says the same name ("…stays valid at Anthropic until you revoke it there"). **Press Cancel, never Remove.**

## ADR-081 D1: a repo link is checked as the account
5. In chat, on `web-pat-test`: create a throwaway project linked to a public repo the PAT can see ("add project zz adr081 with repo <owner>/<repo>"). The link succeeds, and there's no "couldn't verify this repo" note.
6. The same ask on `web-scn-a-1020` (no GitHub connection): the link succeeds with **no** "couldn't verify" note either. With no credential the repo isn't checked, and "not checked" must never read as "doesn't exist".
7. On `web-scn-a-1020`, Settings → Integrations → GitHub reads not connected.

Please report each row as pass, or fail with the reply quoted. CXO judges 4 and 6.

-- Lead
