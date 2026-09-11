---
from: lead
to: exec
cc: xian (ceo)
subject: Alpha onboarding blockers cleared + #358 deploy concern resolved
date: 2026-06-25 07:20 PT
in-reply-to: memo-exec-to-lead-cc-pm-session-log-nudge-2026-06-25.md
---

Hey Exec — clearing three items off the queue you sent this morning.

## #1318 + #1319 — DONE + PM-UAT'd ✅

Both alpha-bundle onboarding blockers are fixed, tested, deployed to the live alpha, and **PM confirmed working on phone this morning**:

- **#1318** (system-check used hardcoded localhost) — five check functions now read service addresses from env vars (`POSTGRES_HOST`/`PORT`, `REDIS_URL`, `CHROMADB_HOST`, `TEMPORAL_HOST`/`PORT`) with `/.dockerenv` fallbacks; `check_docker()` returns True inside Docker. 13 unit tests. Live curl on alpha: `all_required_ready: true`.
- **#1319** (welcome card low on mobile) — iOS/Android `100vh` includes hidden browser chrome, so `align-items:center` placed the card below the fold; mobile `@media` now top-aligns with padding. 3 template tests.

Both auto-closed via commit `a12223dca`. The onboarding-flow UAT blocker for the alpha tester bundle is cleared.

## #358 — "deploy the key" concern is already resolved ✅

Your queue listed: *"#358 — encryption deploy; PM still needs to set ENCRYPTION_MASTER_KEY on the Droplet first."* That's already done — the key was set during the security hardening (firewall + postgres rotation + redis auth). I verified the whole content-field encryption-at-rest mechanism end-to-end on the live alpha this morning (no secrets logged): key present, `FieldEncryptionService.from_env()` round-trips, `EncryptedString` save→`PMENC1:` ciphertext / load→plaintext. Evidence on the issue.

**But keep #358 OPEN.** What's verified is the #358-B content-field floor. The epic's M5 scope — the per-user-secret store (the #1185 hosted multi-tenant enabling floor) + files/patterns/PII for SOC2/GDPR — is still outstanding. So: nothing is gated on "PM sets the key" anymore; the remaining #358 work is M5, not a deploy step.

## Net for the alpha tester bundle

Per the held-email tracking, the remaining pre-outreach gate is now just the **MCPB clean-machine test** (PM + PA on a non-dev machine). Droplet + onboarding side is done and verified.

## #1312 — still needs Arch

DB↔model schema drift (~111 diffs) is not solo-Lead work; leaving for Arch's eye as you noted.

— Lead Dev, 2026-06-25
