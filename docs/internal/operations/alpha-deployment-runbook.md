# Alpha Deployment Runbook

**Status**: STUB — deployment mechanism to `alpha.pipermorgan.ai` needs to be confirmed and documented by Lead Dev.
**Created**: June 19, 2026 (PA)
**Last Updated**: June 19, 2026

---

## What we know

- **Production branch** (`origin/production`) is the stable release surface. As of v0.8.8, it tracks the tagged release commit.
- **`alpha.pipermorgan.ai`** is the hosted alpha instance where testers access Piper Morgan without a local install.
- The deployment mechanism that connects a `production` branch push to a live update at `alpha.pipermorgan.ai` is **not yet documented** and may not be automated.

---

## What we need Lead Dev to confirm

1. **Where is it hosted?** (Fly.io, Railway, Render, EC2, other?)
2. **How is it triggered?** Does a push to `production` auto-deploy, or is there a manual `fly deploy` / equivalent step?
3. **What are the environment variables?** `ANTHROPIC_API_KEY`, `POSTGRES_*`, `JWT_SECRET_KEY`, etc. — where are these stored for the alpha instance?
4. **Database migrations**: does `alembic upgrade head` run automatically or manually at deploy time?
5. **Is there a health check URL?** Something like `https://alpha.pipermorgan.ai/health` we can hit post-deploy?

---

## Release → Deploy sequence (current best understanding)

Until the above is confirmed, the sequence for cutting a release to alpha is:

```bash
# 1. Tag and push release (done as part of release runbook)
git tag -a v0.8.X -m "Release v0.8.X — [description]"
git push origin main
git push origin v0.8.X
git push origin HEAD:production --force   # advance production branch

# 2. Create GitHub Release
gh release create v0.8.X --title "..." --notes-file docs/releases/RELEASE-NOTES-v0.8.X.md --latest

# 3. Deploy to alpha.pipermorgan.ai
# [MECHANISM UNKNOWN — see Lead Dev confirmation above]
# Likely one of:
#   fly deploy --config fly.toml          # if Fly.io
#   git push heroku production:main        # if Heroku
#   [automatic via CD trigger on production branch push]
```

---

## Beta deployment (`beta.pipermorgan.ai`)

Not yet set up. Will be needed before 0.9.0 / Beta release. Same unknowns apply — document alongside alpha once the mechanism is clear.

---

## See Also

- [Release Runbook](release-runbook.md) — full release process (pre-release checks, version bump, doc updates, git ops, GitHub release)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md) — quality gate before release
- [Release Notes v0.8.8](../../releases/RELEASE-NOTES-v0.8.8.md) — current production release
