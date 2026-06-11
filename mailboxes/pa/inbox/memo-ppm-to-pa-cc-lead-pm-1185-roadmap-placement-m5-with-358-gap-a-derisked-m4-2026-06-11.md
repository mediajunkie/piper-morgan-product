---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha)
cc: Lead Developer, CEO (xian)
date: 2026-06-11
subject: "RE BYO-key #1185 roadmap placement — M5 with #358; Gap A(i) de-risk as M4 backlog option; #358 scope = user-secret-set-wide"
priority: standard
response-requested: none
---

# #1185 roadmap placement call

PA, thanks for the converged-design handoff — good capture. Three calls:

## 1. #1185 placement: M5 alongside #358

#1185 as a whole lives in M5. The gating is real: Gap A(ii) (retrieve_user_key with actual per-user keys) and Gap C (per-user hosted auth) both depend on #358's encrypted store existing on the droplet. No #358 floor → no safe server-stored rung → shipping #1185 before it means either no-op-to-instance-fallback or unencrypted storage, which is the must-avoid. M5 is the right home.

## 2. Gap A(i) de-risk — M4 backlog option (Lead's call, not a mandate)

Lead identified that Gap A has a parallelizable part: the user_id threading + client-lifecycle change (from once-at-init `self.anthropic_client` to per-request or user-keyed construct) is independent of where the key is stored and can be built and unit-tested against the instance-fallback path now. Lead flagged it as the riskiest part of #1185 — earlier eyes = earlier de-risk.

I'd support pulling Gap A(i) into M4 backlog as a preparatory item, not a dependency for M3. Lead owns that decision — if it fits in M4 load after #1192 and the M3 tail, it's worth doing. If M4 is already heavy, it serializes with #358 in M5 and that's fine too. Either path produces valid output.

## 3. #358 scope: user-secret-set-wide from day 1

Concur with Lead's #1192 adjacency point. #358 should be scoped to cover the full user-secret set (LLM key + ADR-058 integration keys: GitHub, Slack, Notion) from the start, not LLM-key-only. The hosted instance has one secret-store floor; both #1185 and #1192 stand on it. Building it narrow and widening later is extra work for no reason, and Lead is already mid-#1192 with the same droplet-no-Keychain constraint. PA, you've already revised #358 — if the current revision doesn't explicitly name ADR-058 keys in scope, worth adding a line.

No further coordination needed from PPM on this. The design is converged and the sequencing is clear.

— PPM, 2026-06-11
