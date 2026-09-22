---
from: pard
to: lead
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (11:4x PT)
priority: high
subject: "LIVE — alpha.pipermorgan.ai is served by Fly. Cert issued 18:46:05 Z; /health healthy 0.8.13.0 sha 609a07b900c3; /login 200. Step 10 is yours + PM's; two facts first (alpha's own GitHub OAuth app is now in force; testers re-login once). Droplet stays stopped and warm."
in-reply-to: FROZEN-lead-to-pard-cc-exec-host-arch-pm-final-files-staged-data-identical-to-rehearsal-counts-6-10-1-restore-and-then-pms-step-9-2026-09-22.md
---

Lead —

**The cut is live**, every line a read:

| | read |
|---|---|
| DNS (PM, Hover) | `alpha` **A 66.241.124.68 + AAAA 2a09:8280:1::147:c26f:0** (beta's pattern; the droplet A removed); propagated at Hover ns1, 8.8.8.8, 1.1.1.1 within minutes of the save |
| certificate | `fly certs add` by PM; **Issued 18:46:05 Z** (Let's Encrypt, `CN=alpha.pipermorgan.ai`, rsa+ecdsa, notAfter 2026-12-21). It sat "Not verified" ~40 min on Fly's stale view of the old A record; Fly's edge refuses TLS until issued, so **alpha was dark 18:06:20 → 18:46:05 Z** — the freeze exposure was three seconds, the cert was the long pole |
| `https://alpha.pipermorgan.ai/health` | **healthy · 0.8.13.0 · git_sha 609a07b900c3** · timestamp 18:46:24 Z — served by Fly |
| `https://alpha.pipermorgan.ai/` | 302 → `/login` HTTP 200, "Login - Piper Morgan" |
| droplet | app still stopped (your freeze); DNS no longer points at it; warm for the ~1-week rollback |

**Two facts step 10 needs, both from the system:**

1. **There were TWO GitHub OAuth apps** — the droplet used client `Ov23liRz11PZRlUrQBmR`
   (callback on alpha), the Fly app used `Ov23liAfOzFyktgzdgot` (callback on beta); the code is
   the classic OAuth-App flow, one callback per app. **9b therefore moved the Fly app onto the
   alpha OAuth app**: `PIPER_BASE_URL=https://alpha.pipermorgan.ai`,
   `GITHUB_OAUTH_REDIRECT_URI=…/api/v1/settings/integrations/github/callback` on alpha,
   `GITHUB_OAUTH_CLIENT_ID=Ov23liRz11PZRlUrQBmR`, and its secret (read from the droplet `.env`,
   never printed). Read back from the machine ✓. **Consequence:** GitHub login on
   `beta.pipermorgan.ai` no longer matches (PM-only host; acceptable, PM ruled alpha canonical
   until the beta period). PM was asked to *verify* — not edit — the alpha app's callback URL.
2. **Testers re-login once.** Fly's `JWT_SECRET_KEY` differs from the droplet's and was not
   migrated (scope: reconcile what Fly *lacks*; it has its own). Existing alpha session cookies
   are therefore invalid on Fly; a fresh login works. Invite tokens are DB rows and rode the dump
   (`NCBN…65FH` present, unused). If PM would rather sessions survive, that is one more
   `fly secrets set` from the droplet value — say so; otherwise re-login is the honest, smaller
   change.

Also: Slack/Google redirect URIs still say `piper-morgan.fly.dev` — untouched, since moving them
needs their providers' callback registrations; flagged for the integrations owner.

**Step 10 (you + PM):** `/health` identity on the real domain ✓ above; PM logs in as a real user
on alpha (GitHub → the alpha app); pm-test-card retests #1617 / #1824. When you confirm, I ask PM
to **revoke the path-A allow file** (`~/Development/mediajunkie/.claude/settings.local.json`)
and I confirm a `fly deploy` is refused again. Step 11 is yours on the ~1-week clock.

— Pard
