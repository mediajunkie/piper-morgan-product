---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-05-27
subject: Methodology candidate — load-bearing line-count deltas need coverage-audit gate; surfaced by 8-month Slack-inbound silent disconnection (Pattern-073 Instance #15)
priority: standard — methodology-feeder
response-requested: CIO — disposition (file as candidate / absorb-into-existing-methodology / reject); no action gating
---

# Methodology candidate from today's #1129 discovery

Today's forensic finding (#1129 SLACK-INBOUND-STRUCTURAL) surfaced an 8-month silent disconnection that originated in **CORE-GREAT-2D** (commit `aad66d9d1`, 2025-10-01). That single commit:

- Deleted ~750 lines from `main.py` (1184 → 421)
- Removed the `SlackWebhookRouter` mount that had been live since PM-074 (2025-07-28)
- Was followed by GREAT-3B (2025-10-03) which introduced plugin-system replacement that was incomplete (only `/status` exposed, not `/webhooks/events`)
- No follow-up coverage audit caught the gap
- 8 months of cohort-wide asserted-behavior drift (multiple memos + blog posts + README all claiming "Phase 3 Complete ✅") followed

## Proposed methodology

**Working title**: *Coverage-audit gate for load-bearing line-count deltas in cross-cutting modules*

**The gap this addresses**: refactor commits with substantial line-count deltas in surface-shaped modules (entry points, route mounts, startup, plugin registries) are high-risk for silently removing wiring that downstream subsystems depend on. The risk is asymmetric — the wiring's absence doesn't fail loudly; subsystems that try to use the wiring just fail-silent (no inbound traffic, no error logged, no test catching the regression because tests covered the LOGIC not the WIRING).

**Proposed mechanism**:
- Trigger: any commit with >300 line-delta in entry-point / mount / startup / plugin-registry files (`main.py`, `web/app.py`, `services/*/startup.py`, `*/plugin.py`, `services/orchestration/workflow_factory.py`, etc.)
- Gate: same-PR or follow-up coverage audit listing each subsystem that DID have wiring before and verifying it has wiring (or explicit deprecation marker) after
- Heuristic for "load-bearing": cross-cutting subsystems with external integration points (Slack, Notion, GitHub, etc.) and the conversational floor's intent dispatch surfaces

## Possible parents in methodology corpus

This might absorb into existing methodologies rather than standing alone:
- **methodology-19 (Cleanup as Pattern)** — refactor-as-cleanup is the failure mode here
- **methodology-30 (Consumer-Trace Verification)** — coverage-audit is consumer-tracing in mirror image (don't trace the consumer; trace the producer's wiring)
- **Pattern-073 (Documentation-Asserted-Behavior Drift)** — this is a particularly load-bearing instance class; might warrant its own catalog entry rather than a fresh methodology

CIO judgment on shape — full methodology, pattern catalog instance, or extension to existing methodology?

## What this candidate IS

- A reflection on the cost of the 8-month silent disconnection we just discovered
- A specific proposed mechanism (line-delta threshold + wiring inventory) for catching this class of failure earlier
- Surfaced now while the discovery is fresh, not after we've moved on

## What this candidate is NOT

- Not blaming the CORE-GREAT-2D commit itself (the refactor was good work; the gap was the missing coverage audit)
- Not requesting CIO to drive immediate methodology work (file as candidate; absorb at v0.7+ or whatever cadence makes sense)
- Not blocking #1129 work — that proceeds on its own post-M2 schedule

## Cross-references

- #1129 SLACK-INBOUND-STRUCTURAL (today's discovery): https://github.com/mediajunkie/piper-morgan-product/issues/1129
- Forensic report: `dev/active/slack-inbound-forensics-2026-05-27.md`
- CORE-GREAT-2D commit `aad66d9d1` (2025-10-01)
- GREAT-3B commit `e12d62303` (2025-10-03)
- Pattern-073 catalog: `docs/internal/development/methodology-core/patterns/pattern-073-documentation-asserted-behavior-drift.md`

— Lead Developer, 2026-05-27 ~12:52 PM PDT
