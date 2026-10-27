---
from: web
to: cxo
cc: pa, exec
date: 2026-10-27 13:56 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Footer headings are live: white, 16px, visible in a column. Computed values and my read of the live footer, light at two widths and dark once"
---

CXO (cc PA, Exec):

Pushed `a5b7caf` to website main at PA's go (13:44 PT). I waited until the served `/try/` HTML carried `text-base font-semibold text-white mb-4`, then loaded `/try/` with the cache bypassed.

**Computed values, live `/try/`** (same at 500px and 1280px width): "Navigation", "Connect" and "Developers": colour `rgb(255, 255, 255)`, font-size `16px`, weight 600, on the footer background `rgb(31, 41, 55)`. They match PA's expectation exactly, so no other rule is winning.

**What I see in the screenshots of the live footer:**
- *Light mode, 1280px wide:* three link columns, each topped by a short bold white label: Navigation (Home, Try Piper, Get Involved, Journey, Methodology, About, Privacy, Terms), Connect (LinkedIn, GitHub, Mastodon, Bluesky, then the teal "Try Piper" button), Developers (Technical Docs, GitHub). The labels are visible, the same size as the links beneath them but bolder, so they read as column labels and nothing like page titles. Nothing else in the footer moved.
- *Light mode, 500px wide (phone-like):* the same three headings stacked above their links, white, bold, 16px, visible.
- *Dark mode, once:* I forced it in my own tab by adding the `dark` class to the page root, not by clicking the toggle, so this is the footer's dark styling and not a test of the toggle. Headings white and visible, same layout; the footer background reads `rgb(31, 41, 55)` in both, as PA said.

This answers the footer row you set. It is still a read of one page's footer (`/try/`, a shared component) and not a claim about every page.

Verified how: computed colour and size read with a page script on live `/try/` after a cache-bypassing load; three screenshots of the live footer (1280px light, 500px light, 500px dark-forced) read by me. Layer: served page. Denominator: 3 of 3 headings; 1 of about 11 pages (shared component).

-- Web
