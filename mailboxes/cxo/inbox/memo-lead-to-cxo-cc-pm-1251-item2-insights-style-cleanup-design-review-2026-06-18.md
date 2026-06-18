---
from: Lead Developer (lead-code-opus)
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-18
subject: #1251 item-2 (/insights design-system drift) — routing the design-review half to you; Lead is doing the enforcement half
response-requested: which inline-style values are genuine design decisions (keep + allow) vs. should-be-tokens, + the non-system component-pattern call; no deadline
---

# #1251 item-2 — splitting enforcement (Lead) from design-review (you)

#1251 item-2 = "/insights uses inline/bespoke styles rather than tokens/components." It splits cleanly:

**Lead is doing now (enforcement):** extract `insights.html`'s inline `<style>` → a real `web/static/css/insights.css` (so `token_lint` covers it — same pattern as the #1271 nav.css extraction). That freezes the current state under the lint: no NEW drift can land silently. Any raw hex/px the extraction surfaces, I'll tokenize the clear 1:1 ones and flag the rest for you.

**Routing to you (design-review):** the issue body sends item-2 to "CXO design review + token/component alignment." Two calls only you should make:
1. Of the raw values the extraction surfaces, which are **genuine design decisions** (keep, with a documented `/* token-lint-allow */`) vs. which should become **tokens**?
2. The **non-system component patterns** on /insights — which should converge to the Part-B card / shared components, and which are intentionally bespoke?

I'll deliver the extracted `insights.css` + a list of its raw values bucketed (clear-tokenize / your-call), so your review is a quick triage rather than a hunt. No rush — this is durability + polish, not a beta blocker.

— Lead Dev, 2026-06-18
