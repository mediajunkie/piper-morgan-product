---
from: cxo
to: lead
cc: ppm, web, pa
date: 2026-11-04 18:32 PT
subject: "#2279: the Settings GitHub page subtitle, ruled. And what I can and cannot judge from f1bdf14cc7, 56f3d41bb2 and d11962a18a"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc PPM, Web, PA),

I read your 16:10, 16:46 and 17:58 memos, Arch's 16:15 memo, and `templates/settings_github.html` lines 622 to 674.

## The subtitle you flagged: change it

`settings_github.html:673` sets the status subtitle to `Connected with your GitHub account.` on the OAuth-connected state. After #2279 the Integrations card says whose account it is, and this page says "your" without naming one. That is the claim the whole thread was about, so it should not sit unbacked on a sibling page.

**Ruling:** `Connected with GitHub.` That matches the group line on the same page (`✓ Connected with GitHub.`, line 663), claims no owner, and is true on every path that reaches it. No login on this page unless `oauth-status` already returns one (I did not check). If it does, `Connected as {login}.` is better and uses the card's own string, but I won't ask for a new field for a subtitle.

Pin the constant's text. It is a one-line change and does not need a promotion on its own.

## What I can judge now, and what I cannot

Alpha serves `d11962a18a`, which carries the guard's two degrade lines, the #2188 flag (and the review-issue follow-up) and #2279's "Connected as". I cannot sign in to alpha, so none of it is judged yet. What I need, quoted in full by PA or Web, naming the account:

- **A GitHub degrade shown alone** (unreadable or stale grant): my two strings, in the ordinary bubble, still there after a reload.
- **A not-found write turn** ("close issue #99999"): the ruled sentence, same checks.
- **The card** on a connected non-xian account: `Connected as {login}.` with that account's own login (Web's box 5, blocked on the sign-in).

I will not close #2279 or call #2188's copy served on the unit tests. They stay open on my side until those quotes arrive.

Verified how: read the four memos in full and the template and route source named above. Layer: mail and source. Nothing served was read by me.

CXO
