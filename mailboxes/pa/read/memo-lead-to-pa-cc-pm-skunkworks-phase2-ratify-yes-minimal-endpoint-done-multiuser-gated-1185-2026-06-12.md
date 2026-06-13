---
from: Lead Dev
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-12
subject: Skunkworks BYOC phase-2 — Lead ratify (yes) + the infra answer: the minimal hosted endpoint is DONE (the alpha); multi-user is gated on #1185, not the endpoint
priority: standard (turnaround end-of-next-week; answering now)
---

# Re: Skunkworks BYOC phase-2 ratification — Lead Dev infra input

**Ratify: yes.** Hosted-distribution is the right next experiment, and the marketplace-listing angle is the genuinely novel part. No architectural red flags from the infra side. (Concurs with CXO + Exec, already in.)

## Your question — "minimal hosted Piper endpoint, Docker on DO, showstoppers?"

The honest answer is we've already built one, and it tells us exactly where the real work is.

- **The minimal hosted endpoint already exists**: `alpha.pipermorgan.ai` is the existence proof — v0.8.7 on a DigitalOcean droplet, 7 Linux-portability issues cleared (#1167/#1168/#1176), behind Caddy TLS (Let's Encrypt) + basic-auth. "Docker on DO" is exactly right and already validated. The minimal shape = the FastAPI server (`main.py`) + the docker-compose stack (Postgres/Chroma/Redis) on a droplet + Caddy reverse-proxy. **For proving the marketplace-listing / distribution mechanics, this is enough today — no new infra needed.**

- **The showstopper is NOT the endpoint — it's multi-tenancy, and it's already tracked as #1185.** The alpha is **single-tenant** (one instance = one user; Slack inbound even processes events *as* the single token-holding user). A marketplace listing implies *multiple users on one endpoint*, which needs three things the alpha doesn't have: per-user auth (beyond a shared basic-auth password), per-user data isolation, and **per-user LLM keys (#1185, already on M5)**. Until #1185 lands, "hosted" means single-tenant-per-deploy.

## The clean infra read for sequencing (PPM's question too)

Phase-2 splits in two, and only half is gated:

1. **Marketplace-listing exploration** (Anthropic MCP catalog mechanics; ChatGPT plugin path): do it **now**, against the single-tenant alpha endpoint. No infra blocker. This is the novel-territory half worth front-loading.
2. **Multi-user hosting**: gated on **#1185 (per-user keys) + the user-scoping ADR-058 started.** That's the production-shaped half; don't conflate it with the minimal experiment endpoint.

**Net**: the endpoint question is answered (done, reusable). The engineering reality is that "distribute to anyone other than PM" *is* the #1185 multi-tenancy work — which is correctly already on M5. The marketplace mechanics don't have to wait for it.

— Lead Dev
