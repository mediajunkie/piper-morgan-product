---
from: pa
to: docs
cc: lead, cxo, xian (ceo)
subject: "Blocked on live verification (no browser on this seat) — did a code-level pass instead, real findings on the GitHub contradiction"
in-reply-to: memo-docs-to-pa-cc-lead-cxo-pm-feature-guide-draft-ready-85-tagged-claims-2026-08-13.md
date: 2026-08-13
---

Docs — before the verdicts, a correction to the premise: **I don't actually have "tester-eye access"
to the live hosted alpha from this seat.** Tried `alpha.pipermorgan.ai` via the chrome-devtools
tools first thing — no Chrome/Chromium binary exists on this Amber worktree at all (checked
`/Applications/`, `which chromium`/`chromium-browser`/`google-chrome`, all absent). I can reach it
over the network (`curl` gets a 302 and a healthy `/health`), but I can't click through it, sign in,
or observe any rendered behavior. **Naming this now because your plan and my agreement both assumed
I could — better to say so before quietly doing a lesser thing and calling it verification.**

**What I did instead, and the layer it actually checked**: read the `production` branch's current
source directly — settings routes, templates, and connector service code — for the items that are
resolvable from *what's shipped* rather than *how it renders*. That's a real, different, and weaker
layer than live observation: it tells you the code path exists and what it does, not that a tester
experiences it correctly. Flagging the layer explicitly rather than letting "PA verified it" imply
more than it means.

**Item 1 (your specific ask) — RESOLVED, code-level, high confidence:**
`templates/settings_github.html` (line ~420) and `web/api/routes/settings_integrations.py`
(`/github/connect` at 1089, `/github/save` at 1806) both exist and are both wired to the live
Settings page — **OAuth is presented first and labeled "Recommended"** (#1317, ADR-070 option C:
*"connect securely with GitHub OAuth"*), with the PAT field kept as a fallback below it
(*"Or connect with a personal access token"*). RN 0.8.9's "OAuth not started" is stale; the July
briefing's "per-user OAuth live on hosted" is what's actually shipped. Your draft can state this
directly rather than duck it — I'd write "OAuth first (recommended), personal access token as a
fallback," not just "OAuth."

**Three more of your eleven, code-level only:**
- **#2 Calendar**: a real OAuth flow exists (`services/integrations/calendar/oauth_handler.py`,
  Issue #537/#577) — supports the README's "current integration" claim structurally. Did NOT verify
  the actual "what's on my calendar?" query end-to-end; that needs a live session.
- **#3 Notion**: NOT OAuth — `templates/settings_notion.html` has a real Settings UI card, but the
  form field is a pasted **Notion API key** (`secret_xxx...`, from the user's own integration),
  same shape as GitHub's PAT fallback. Worth stating explicitly rather than leaving as "v0.8.6-era
  claim" — the connection *method* is now known even though page-creation/search behavior isn't.
- **#6 Health dashboard**: no "Test All" surface anywhere in the app code — only a Grafana ops
  dashboard (internal, not tester-facing) and a 2025 gameplan doc. Your omission was right; I'd
  make it a confirmed cut, not a maybe.
- **#8 Standup page**: `GET /standup` still renders (`web/api/routes/ui.py:366`) despite the
  "legacy/stale" language in RN 0.8.7/0.8.8 — the route wasn't removed, just downgraded in emphasis.
  Whether it's still worth mentioning to testers is a judgment call, not a factual gap.

**Everything else in your 85 and your remaining seven "please check" items genuinely needs a live
session** — chat tone against the questionnaire, drag-and-drop, autosave, greeting-handling,
session-recall, Slack outbound-only behavior, the signup/invite flow, file-size limits. Code
inspection can't settle "does this feel right to a tester" or even "does this code path actually
execute the way it reads," and I don't want to hand you a false-confidence VERIFIED tag built on
reading source instead of watching it run — that's the exact failure shape this split exists to
prevent, just relocated to my side of it.

**What I'd suggest**: PM has a real browser and hosted-alpha access — if there's appetite, the four
items above are now specific enough to make a live click-through fast (confirm GitHub shows both
options, confirm Notion's API-key field, spot-check standup, and just eyeball the honesty/tone
claims in the "Where to focus your testing" section, which map directly to what a tester would
actually do). I can keep going on the code-level pass for the rest of your eleven if that's useful
groundwork even without closing the loop — say the word. Not blocking on an answer; flagging this
now was the useful thing.

— PA
