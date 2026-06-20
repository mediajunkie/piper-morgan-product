# Alpha Deployment Runbook

**Status**: STUB — deploy sequence on the Droplet needs to be confirmed and documented by Lead Dev.
**Created**: June 19, 2026 (PA)
**Last Updated**: June 19, 2026

---

## What we know

- **Production branch** (`origin/production`) is the stable release surface. As of v0.8.8, it tracks the tagged release commit.
- **`alpha.pipermorgan.ai`** is the hosted alpha instance where testers access Piper Morgan without a local install.
- **Hosting**: DigitalOcean Droplet (PM-owned). SSH credentials and droplet access are with PM (xian).
- The deploy sequence on the droplet (git pull, alembic, restart) is not yet documented.

---

## What we need Lead Dev to confirm and document

1. **SSH / access**: how Lead Dev (and future agents) SSHs in — key, IP, user.
2. **Deploy sequence on the droplet**: `git pull origin production`, `pip install`, `alembic upgrade head`, server restart command (systemd? screen? nohup?).
3. **Environment variables**: are they in a `.env` file on the droplet, or set via droplet console? What vars are needed (`ANTHROPIC_API_KEY`, `POSTGRES_*`, `JWT_SECRET_KEY`, etc.)?
4. **Database**: is Postgres running on the droplet itself, or external (managed DB)?
5. **Process management**: how is `main.py` kept running — systemd service, screen session, supervisor?
6. **Health check URL**: `https://alpha.pipermorgan.ai/health` (or equivalent) to verify deploy succeeded.
7. **Domain / reverse proxy**: how does `alpha.pipermorgan.ai` resolve to the droplet — nginx? Caddy? Direct port 8001?

---

## Release → Deploy sequence (current best understanding)

Steps 1–2 are done as part of the release runbook. Step 3 is the gap.

```bash
# 1. Tag and push release (complete — done for v0.8.8)
git tag -a v0.8.X -m "Release v0.8.X — [description]"
git push origin main && git push origin v0.8.X
git push origin HEAD:production --force

# 2. Create GitHub Release (complete — done for v0.8.8)
gh release create v0.8.X --title "..." --notes-file docs/releases/RELEASE-NOTES-v0.8.X.md --latest

# 3. Deploy to Droplet — SEQUENCE TO BE CONFIRMED BY LEAD DEV
# ssh <user>@<droplet-ip>
# cd /path/to/piper-morgan-product
# git pull origin production
# source venv/bin/activate
# pip install -r requirements.txt        # if deps changed
# alembic upgrade head                   # if migrations pending
# [restart server process]
```

---

## Beta deployment (`beta.pipermorgan.ai`)

Not yet set up. Will be needed before 0.9.0 / Beta release. Same unknowns apply — document alongside alpha once the mechanism is clear.

---

## See Also

- [Release Runbook](release-runbook.md) — full release process (pre-release checks, version bump, doc updates, git ops, GitHub release)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md) — quality gate before release
- [Release Notes v0.8.8](../../releases/RELEASE-NOTES-v0.8.8.md) — current production release
