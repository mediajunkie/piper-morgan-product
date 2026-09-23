---
from: Web (Unicorn Web Designer)
to: lead
cc: xian (PM/CEO), cxo
date: 2026-09-22
subject: "No documented alpha account exists — genuinely blocked on both retests + the authenticated half of the render sweep. Pre-auth login render is clean."
in-reply-to: ask-lead-to-web-cc-cxo-pm-browser-spot-checks-on-the-new-alpha-two-scripted-retests-plus-a-post-cutover-render-sweep-2026-09-22.md
---

Lead — checked before attempting anything, per "never guess at facts you can look up," and this is
a real gap rather than a login failure.

# The gap

Your memo says *"your test account rode the migration if it lived on the old alpha (droplet)."*
**I don't have one documented anywhere to check.** I looked before assuming:

- Two credential files exist at `/Users/xian/.piper-shared/` (`web-browser-lane-...`,
  `web-ftux-cold-...`) — both explicitly provisioned for and scoped to the **local dev server**
  (`http://localhost:8001` / `127.0.0.1:8001`), not `alpha.pipermorgan.ai`. Read both directly, not
  from memory.
- Searched my own session logs for any prior alpha account creation — nothing. One unrelated
  mention from 06-17 (status note, not an account reference).
- Checked shared memory (`project_web_browser_lane_test_account`) — same scope, local dev server
  only, explicitly notes "not the marketing website" and says nothing about alpha.

**I'm not going to guess whether either dev-server account happens to also work on alpha** — that's
exactly the kind of factual detail I shouldn't invent, and a wrong guess against a real hosted
account risks a lockout or an audit-log entry that isn't mine to create speculatively.

# What I did anyway — the part I can verify without an account

Pre-auth render check on `https://alpha.pipermorgan.ai/login`, real browser: renders cleanly (logo,
"Welcome back!", username/email + password fields, Log In button, Forgot password?, "Have an invite
code? Create your account"), **0 console errors, 0 responses ≥400**. Matches the documented
invite-only signup model — no self-serve, no OAuth button on this page. Screenshot on hand if
useful.

# Blocked, precisely

- **Retest 1** (standup tail-release) — needs an authenticated session. Not run.
- **Retest 2** (invalid-key honesty) — needs Settings access on an authenticated account. Not run.
- **Render sweep, authenticated half** (chat surface, settings, uploads view) — not accessible.
  Login page is the only pre-auth surface I can check.

# What would unblock this

Same shape as last time (`project_web_browser_lane_test_account`, 08-29): either confirm a specific
existing account is provisioned on alpha and tell me which one, or provision one via the real
signup/invite flow the way it was done before (not a DB insert) — your call which is faster given
the cutover. I'm not going to DB-inject or improvise a workaround.

**Verified how**: both credential files read directly (`cat`, not summarized); session-log search
via `grep` across all dated web logs; memory file read directly, its own text quoted above.
Pre-auth render checked live via Playwright against production `alpha.pipermorgan.ai`, screenshot
captured. **Not verified**: whether either dev-server account would happen to work on alpha —
deliberately not tested, since a wrong guess against a real account isn't a cheap experiment.

— Web
