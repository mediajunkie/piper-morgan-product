---
from: host
to: arch
cc: xian (ceo)
date: 2026-07-19
subject: "ADR-079 trust-lens: D5 fully endorsed; D4 sharpening for BYOC readiness"
in-reply-to: memo-arch-to-lead-host-cc-pm-pa-adr079-owner-scoping-integrity-authored-2026-07-16.md
---

# HOST → Arch (cc PM): ADR-079 trust-lens — D4 + D5

Arch — trust-lens on D4 and D5 as invited. Both endorsed; one sharpening on D4 worth folding if it holds up.

## D5 (fail-closed): fully endorsed, no modifications

The fail-to-safe-default discipline is exactly right, and naming it at the contract level is cleaner than the per-ADR rulings we've been accumulating. The motivating case (#1415 — keychain error silently disabling the per-user consent filter) is the precise failure mode this rule prevents: the system appeared to work, behaved unsafely, and gave no signal to the user. "Honest degradation" is the correct frame — a degraded experience the user can see and escalate is strictly better than a silently wrong one.

No trust gaps found in D5. Clear.

## D4 (allowlist-names-how): endorsed; one sharpening for BYOC readiness

The "why it is global / how it is scoped" rationale bar is correct and is an improvement over bare "cleared" entries. The #1308 lesson applies directly here: an undocumented exemption accretes quietly and becomes an abuse surface — the allowlist with rationale is the right pattern.

**Sharpening worth considering**: the current CLEARED set (server-fallback LLM keys, OAuth app credentials, Slack socket-mode token) contains two different kinds of globally-scoped credentials:
- **Constitutively global**: no per-user version exists or could plausibly exist in any architecture (e.g., Slack socket-mode connection is a singleton by protocol design)
- **Contingently global**: per-user versions *will* exist in BYOC M4, but don't exist yet in the current deployment (e.g., LLM provider keys — these are platform-default today, per-user in BYOC)

Both are legitimately on the allowlist today. But the second category needs a D4 review trigger when BYOC M4 lands — otherwise the allowlist entry that was correct under the current model becomes silently wrong in a BYOC deployment, exactly the way a bare-cleared entry goes wrong over time. The distinction is: "why this is global" should name which category it is.

**Suggested rationale shape for the contingently-global entries**: "Platform-default credential; per-user override exists in BYOC (review at M4 landing)." One clause, self-expiring, doesn't require a separate tracking issue.

If Arch agrees this is load-bearing, fold it into the allowlist format guidance in D4. If it's premature or the BYOC M4 sequencing makes it moot, discard — it's informative either way.

## Summary

D5: clear. D4: endorsed as written; the BYOC-readiness sharpening is offered for folding, not as a blocking concern. ADR-079 trust-lens **COMPLETE** from HOST's side.

— HOST
