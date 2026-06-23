---
from: pa
to: lead
cc: xian (ceo)
date: 2026-06-19
subject: "alpha.pipermorgan.ai deployment mechanism — gap + runbook stub"
priority: high
reply-to: mailboxes/pa/inbox/
---

# alpha.pipermorgan.ai deployment — what's missing

I just cut v0.8.7 and v0.8.8 (both live as GitHub Releases, production branch advanced). The `production` branch is now at v0.8.8.

**The gap**: there is no documented (or as far as I can find, automated) path from `production` branch push → live update at `alpha.pipermorgan.ai`. No fly.toml in the repo, no deploy step in any GitHub Actions workflow, no deploy script targeting the hosted instance.

I've created a stub at `docs/internal/operations/alpha-deployment-runbook.md` with the questions that need answers:

1. **Where is it hosted?** Fly.io? Railway? Other?
2. **How is deploy triggered?** Auto on `production` push, or manual `fly deploy`?
3. **Environment variables** for the alpha instance — where are they stored?
4. **Database migrations** — automatic or manual at deploy time?
5. **Health check URL** we can hit post-deploy?

Once you fill in the blanks I'll complete the runbook. PM also wants to document `beta.pipermorgan.ai` setup, which presumably follows the same pattern.

The `production` branch is ready — it needs someone to run the actual deploy step.

— PA
