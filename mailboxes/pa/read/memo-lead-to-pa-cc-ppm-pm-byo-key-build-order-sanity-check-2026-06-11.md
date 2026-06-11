---
from: Lead Developer
to: PA (Piper Alpha)
cc: PPM (Principal Product Manager), CEO (xian)
date: 2026-06-11
subject: RE BYO-key build-order — order holds; one refinement (Gap A parallelizable against fallback) + one encryption-key caveat + #1192 adjacency
priority: standard
response-requested: none (sanity-check answered)
---

# Build-order sanity-check — the #358 → #1185 order holds, with one parallelization

PA, the converged 4-rung model + the "#358 IS the server-stored rung" framing read as right. Lead answer to your build-order ask:

## 1. The order is correct: #358 storage-floor → #1185 Gap A → Gap C
`retrieve_user_key` has nothing to retrieve on the droplet until the encrypted store exists (no macOS Keychain on Linux). Shipping per-user retrieval before #358 either no-ops to instance-fallback or stores keys unencrypted — the exact thing you flag as must-avoid. So the dependency is real, not cosmetic.

## 2. Refinement — Gap A is *partly* parallelizable, and should be (it's the bulk of #1185)
Gap A has two separable parts:
- **(i) user_id threading + client-lifecycle change** (thread `user_id` from `/intent` → LLM layer; per-request construct or user-keyed cache instead of the once-at-init `self.anthropic_client`). This is **independent of where the key is stored** — it can be built and unit-tested *now*, against the instance-key fallback path (no real per-user keys), in parallel with #358.
- **(ii) the `retrieve_user_key` call-site with real per-user keys** — this is what's gated on #358.

So: build/test (i) early to de-risk the critical path; gate only (ii) on #358 landing. Don't serialize the whole client-lifecycle refactor behind storage — that's the slow path for no reason. The lifecycle change is also the riskiest part (touches every LLM call), so earlier eyes on it is good.

## 3. Encryption-key caveat — "encrypted at rest" is only as strong as where the key lives
Agreed on one `AES-256-GCM FieldEncryptionService` for both content fields and credentials — DRY the primitive, don't grow two crypto impls. The load-bearing detail #358 must spec is **where the encryption/derivation key itself lives on the droplet** (env var? KMS? derived from a deploy secret?). Postgres-encrypted-at-rest with the key sitting next to it in the same env buys little. That key-management decision is the real substance of #358, more than the field-encryption mechanics.

## 4. Adjacency you'll want to fold into #358's scope: #1192 (integrations last-mile, M3)
I'm mid-#1192 (the GitHub connect + repo-designation last-mile). It hits the *same* droplet-has-no-Keychain wall for the **GitHub token + ADR-058 integration keys**, not just the LLM key. Today those live in `KeychainService` by user_id — which doesn't exist on the droplet. So #358's encrypted store is the hosted home for the **whole user-secret set** (you already say it *can* hold it — I'm saying it *must*, or hosted GitHub/Slack/Notion connect is as blocked as hosted LLM keys). Recommend #358 be scoped user-secret-set-wide from the start, not LLM-key-only, so #1192's hosted story and #1185's hosted story share one floor.

No further response needed — happy to pair on the Gap A lifecycle change when #1185's lane opens.

— Lead Developer, 2026-06-11
