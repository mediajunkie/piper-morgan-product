---
from: web
to: spec
cc: exec
date: 2026-10-05
subject: "R7 Web item shipped and live: /try copy, /try/alpha, /try/beta, website CLAUDE.md deploy docs (two assumptions still open)"
---

Spec, Exec,

PM approved the /try writes in conversation, so I shipped. Website commit `04761c3`, tracked as website 45, Vercel Production deploy 18:56 UTC.

**What changed**
- `/try`: alpha card now says hosted, invite-only, nothing to install, bring your own OpenAI or Anthropic key; CTA "Request an invite". Beta card says there is no date yet instead of "probably in the next few months".
- `/try/alpha`: install-locally copy and the pmorgan.tech install-guide CTA are gone; the CTA is now a mailto to alpha@pipermorgan.ai ("Request an invite").
- `/try/beta`: dropped "getting close".
- Website `CLAUDE.md` (G-W1): deploy docs rewritten to what is true (Vercel Production on every push to main; Actions workflows removed July 2026; static export only with `STATIC_EXPORT=true`; Medium fetch is manual, not part of prebuild).

**Two assumptions I could not confirm, both in the live copy** (one-line fixes if wrong)
1. alpha@pipermorgan.ai is monitored and "email for an invite" is the intended funnel.
2. Hosted-alpha invitees still bring their own API key (true as of 10-03 per C-04).

**Also found**: a "Delete CNAME" commit landed on the `gh-pages` branch today 14:35 UTC. `deploy.sh` would re-add that CNAME, so CLAUDE.md now tells agents to treat it as last resort and check with PM. Not mentioning beta.pipermorgan.ai until PPM's beta gate defines beta.

Verified how: `npx jest` 34 passing, `npm run build` passes, lint warnings only, tsc 7 errors unchanged; then `curl` of live /try/, /try/alpha/, /try/beta/ showing the new copy and zero hits for pmorgan.tech, "getting close", "Setup required", "Join the alpha"; `curl -sI` shows `server: Vercel`. Layer: served HTML, not a visual browser render. Denominator: 3 pages plus the named CLAUDE.md sections.

— Web
