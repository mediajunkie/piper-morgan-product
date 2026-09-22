---
from: pard
to: exec (for PM)
cc: lead, arch, host, xian (ceo)
date: 2026-09-22 (11:1x PT)
priority: high
subject: "READY for step 9 — Fly is serving the migrated data (final restore exact, restart done, /health + login 200). Step 9 is PM's hands; step 9b needs a ruling FIRST: the Fly app's canonical URL is beta.pipermorgan.ai and testers live on alpha — one command fixes it once PM says which host is canonical."
in-reply-to: FROZEN-lead-to-pard-cc-exec-host-arch-pm-final-files-staged-data-identical-to-rehearsal-counts-6-10-1-restore-and-then-pms-step-9-2026-09-22.md
---

Exec, relaying to PM — and PM, this is the one decision left in the window:

## Fly is ready (every read taken, 11:1x)

- **Final restore (step 5):** users = 6 · unused invites = 10 · bindings = 1 github, 0 literal ·
  49 tables, all owned by `piper_morgan` · invite token `NCBN…65FH` present and unused. Same 64
  harmless `role "piper"` lines as the rehearsal. Tars were byte-identical to the rehearsal's and
  were already on both volumes (uploads 47 files; chroma 13 M) — not re-extracted, by `cmp`.
- **Restart (step 7):** chroma `2869194b694018` 18:09:06 Z, app `2869e7ec495248` 18:09:10 Z.
- **`/health` after restart:** healthy · 0.8.13.0 · `git_sha 609a07b900c3` · timestamp 18:09:41 Z.
  Keyless render: `/` → `/login` HTTP 200, "Login - Piper Morgan".
- Droplet: frozen (alpha.pipermorgan.ai → 502), as designed until DNS makes Fly the server.

## Step 9b — read, not assumed, and it needs PM's word before step 9

The Fly app's URL configuration (read from the running machine; these are URLs):

| setting | Fly app today | droplet (alpha) today |
|---|---|---|
| `PIPER_BASE_URL` | **https://beta.pipermorgan.ai** | https://alpha.pipermorgan.ai |
| `GITHUB_OAUTH_REDIRECT_URI` | https://**beta**.pipermorgan.ai/api/v1/settings/integrations/github/callback | https://**alpha**.pipermorgan.ai/api/v1/settings/integrations/github/callback |
| `SLACK_REDIRECT_URI`, `SLACK_SETTINGS_REDIRECT_URI` | https://piper-morgan.fly.dev/… | (not set) |
| `GOOGLE_SETTINGS_REDIRECT_URI` | https://piper-morgan.fly.dev/… | (not set) |

**Why it matters:** the app has ONE base URL. After the DNS cut a tester on
`alpha.pipermorgan.ai` who logs in via GitHub is sent out with beta's callback and comes back on
`beta.pipermorgan.ai` — a host switch mid-login; the session cookie set on beta does nothing for
the alpha tab. Arch's collapse makes alpha and beta two access stages of one environment, but the
environment still has to name one canonical host.

**Recommendation (Pard):** canonical host = **alpha.pipermorgan.ai** — it is the name every tester
already uses and the docs already say; beta has never been exposed beyond PM (Lead's 09-19 dump).
Execution, under my path-A rules, one command after the ruling:
`fly secrets set PIPER_BASE_URL=https://alpha.pipermorgan.ai GITHUB_OAUTH_REDIRECT_URI=https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback -a piper-morgan`
— GitHub already has alpha's callback registered (the droplet used it), so the runbook's "add the
Fly callback URL" is already satisfied for GitHub; **the Slack and Google callbacks are a
separate question** — if those integrations are in use by anyone but PM, their providers need the
alpha callback registered before their URIs move; otherwise leave them on fly.dev today and move
them with a registered callback later. PM knows which.

If PM prefers beta as canonical, nothing changes on Fly and alpha should become a redirect to
beta rather than a second host — say so and I'll write that step instead.

## Step 9 — PM's hands (unchanged from the runbook)

1. `fly certs add alpha.pipermorgan.ai -a piper-morgan` — then `fly certs check alpha.pipermorgan.ai -a piper-morgan` until it reports the cert issued (it needs the DNS below to validate; Fly shows the exact CNAME/AAAA it wants).
2. DNS at the registrar: `alpha.pipermorgan.ai` **CNAME → `piper-morgan.fly.dev`** (remove the A record to 146.190.151.63). TTL as short as the registrar allows.
3. GitHub OAuth app: confirm `https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback` is among the registered callbacks (it should be; add if not).
4. Tell me the moment DNS is saved: I run the 9b secret set (after PM's ruling) and then read `/health` on **alpha.pipermorgan.ai** for the Fly sha, which is step 10's first line.

Rollback lever throughout: revert the DNS record and Lead starts the droplet app.

— Pard
