---
from: Janus (DinP)
to: CIO (Piper Morgan)
cc: Exec
date: 2026-11-18 08:26 PT
subject: xian asks: is Claude Platform linked billing a better alternative to BYOK for Piper?
---

CIO,

xian, from the summit this morning (Wed 11-18, ~08:2x PT), verbatim:

> "from today's news: https://claude.com/resources/articles/linked-billing-on-claude-platform - Piper Morgan's CIO should explore if this is a better alternative to BYOK given we aren't marking up token costs anyhow?"

What the article says (my read; please check it against the article and the linked docs, not this summary):
- Linked billing is in beta. A customer links their Claude Platform organization to a third-party platform, and the platform's Claude usage bills to that organization. No API key changes hands, so the platform has no customer keys to store, encrypt or rotate.
- The platform registers an app in Console and follows the linked billing docs. An Owner, Admin or Billing role on the customer's side approves the link.
- For each request, the platform chooses whether it pays or the customer pays.
- Customers can set monthly spend limits per platform, see spend per platform in Console, and unlink at any time.
- Requests run in the platform's organization, so the customer's organization settings (IP allowlists, encryption keys, data retention) don't apply. For alpha users who care where their data goes, that's worth weighing.
- The article mentions no platform fee or markup.

What xian is asking for is an exploration, not a decision: is this a better fit than BYOK for Piper's users, given that Piper doesn't mark up token costs? Please put your finding on Exec's board when it's ready. There's no deadline from him. Two things would help him decide: what changes for an alpha user's setup, and what the beta status means for relying on it.

Note: Console is at platform.claude.com now (console.anthropic.com redirects there).

Janus
