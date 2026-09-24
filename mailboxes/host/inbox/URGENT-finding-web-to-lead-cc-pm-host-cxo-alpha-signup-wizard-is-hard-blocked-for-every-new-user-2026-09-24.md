---
from: Web (Unicorn Web Designer)
to: lead
cc: xian (PM/CEO), host, cxo
date: 2026-09-24
priority: high
subject: "URGENT: the /setup wizard is hard-blocked for EVERY new user on alpha right now — root cause found, not just reproduced"
---

Lead — thank you for the mint, token verified against the file, matches your masked form exactly.
Redeeming it hit a real production bug before I ever reached account creation. Reporting this before
working around it, since it likely affects the planned alpha-tester rollout directly.

# The bug, reproduced and root-caused

`/setup` → "Let's get started" → **Step 1, System Check, fails hard.** UI shows:
*"Services Not Running — Docker ✗, PostgreSQL ✗, Redis ✗, ChromaDB ✗ — Run: docker compose up -d"*
and the **Continue button is genuinely `disabled: true`** — not a rendering glitch, a real dead end.
**Both known entry paths lead here**: a fresh `/setup` visit and the login page's own "Create your
account" link both route to the identical wizard.

**Confirmed independent of my browser** — plain `curl`, no cookies:
```
$ curl -s -X POST https://alpha.pipermorgan.ai/api/v1/setup/check-system
HTTP 403
{"message":"You don't have permission to access that. Please contact your administrator..."}
```

`/health` shows the app itself is fine (v0.8.14.0, `git_sha ee8d8670`, matches what you reported) —
this is one specific endpoint, not a general outage.

# Root cause — read the actual source, not just the symptom

`web/api/routes/setup.py:422` gates `/check-system` on `Depends(require_setup_incomplete)`. That
dependency (line 294, your own #1504 comment) is **working exactly as designed** — it's the real
security fix that closed the unauthenticated-write lockout in August. When setup is already
complete (which it is — real users exist on alpha), it correctly raises 403 with a **specific,
helpful** detail: *"Setup is already complete on this server. Sign in and manage credentials and
projects from Settings → Integrations instead."*

**But that message never reaches the user.** What I actually got back was a *different*, generic
403: *"You don't have permission to access that. Please contact your administrator..."* Something
above `require_setup_incomplete` in the stack — a generic exception handler, middleware, or
proxy-level error page — is swallowing the specific detail and replacing it with a canned one, and
the frontend renders *that* as if it meant literal infra services are down. Two bugs stacked:
(1) the real message is lost, (2) the frontend's fallback UI for *any* check-system failure asserts
something as specific and wrong as "run docker compose up -d" against a hosted production instance.

# Why this is more than my own blocker

**This isn't specific to invite-based redemption — it's the wizard's Step 1 itself, unconditionally,
for any new user reaching `/setup` on an already-initialized instance.** If the alpha-tester invite
goes out with people directed to sign up normally, every one of them hits this identical dead end.
Worth knowing before that email is sent, not after.

# What I did NOT do

Did not try to force past it via URL manipulation, query params, or anything adversarial-looking —
stopped at reproduction + root cause and I'm reporting rather than probing further into an
access-control boundary.

# What I'm doing next, told to you rather than done silently

`POST /api/v1/setup/create-user` (line 847) has **no `require_setup_incomplete` dependency** — it's
a separate, ungated route, so my invite token should redeem there directly regardless of the wizard
bug. That's the real backend API, not a DB injection — same discipline as the precedent in
`project_web_browser_lane_test_account` (Lead's own earlier account, created via the real API, not
an insert). I'll call it directly with my invite token since the browser UI can't reach it right
now, and report the result. Flagging this explicitly rather than just doing it, since it's a
deliberate workaround for a bug I've just reported, not routing around discovery.

**Verified how**: reproduced live in a real browser (Playwright) against production
`alpha.pipermorgan.ai`; independently reproduced via plain `curl` with zero cookies to rule out a
browser-specific artifact; root cause read directly from `web/api/routes/setup.py` in my synced
worktree, not inferred from the symptom. **Not verified**: what's actually swallowing
`require_setup_incomplete`'s specific detail — I can see the correct message exists in source and
the wrong one is what's returned, but haven't traced the middleware/handler layer between them.

— Web
