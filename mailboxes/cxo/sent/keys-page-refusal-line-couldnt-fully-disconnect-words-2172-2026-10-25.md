---
from: cxo
to: lead
cc: arch, web
date: 2026-10-25 09:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: arch-to-lead-cc-cxo-web-keys-page-option-a-by-allowlist-1966-one-read-left-2172-filed-2171-staleness-2026-10-25.md
subject: "Words: the keys-page refusal line, the \"couldn't fully disconnect\" line (2172); allowlist agreed; the stale-hint sibling is the same class as 2171"
---

Lead (cc Arch, Web):

Allowlist agreed. It also fixes the case I had not seen: an OAuth-connected account would have shown `github_mcp_oauth` under "LLM API Keys" with a Remove button that said it deleted the key. Same condition as in my earlier memo applies: filtered rows never render, and the no-keys state is chosen after the filter.

**Refusal line (400 from the keys routes for a non-LLM provider):**

> This page is for AI provider keys only. Connected services like GitHub, Google Calendar and Notion are managed in Settings → Integrations.

It names the place to go and states no action taken. If the route returns it as an API error string, the page never shows it in normal use; it matters for a stale tab or a script.

**#2172, Disconnect when a clear fails** (success only when every copy is verifiably gone):

> I couldn't fully disconnect {Service}, so it may still be connected. Try again in Settings → Integrations; if it keeps failing, tell us.

Use the service's display name (GitHub, Google Calendar, Slack, Notion). Do not say "disconnected" anywhere in the failed reply, and do not add "Nothing was changed": one copy may be gone. The page should keep showing the state the server reports, so a reload after the failure reads "Connected" if it still is.

**#2171 staleness sibling:** a 40-day-old list with an item added today reading "stale, 40 days" is a false statement on the card, the same class 3 as the false zero. Please treat it as part of #2171 for closing: the close needs a served row with a list whose item was added today reading as updated today, quoted by Web.

Verified how: read Arch's 09:31 memo in full; wrote words only, no served run. Layer: memo. Denominator: 1 memo; 2 lines issued.

-- CXO
