---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-05-08
subject: #304 Notion Phase -1 investigation complete — verdict "close to ready"; sub-epic placement recommendation included
priority: normal
response-requested: PA — sub-epic placement ratification with PM (M2f or M2-discovered recommended)
artifact: dev/2026/05/08/304-phase-minus-1-notion-investigation.md
---

# Phase -1 done; #304 ready for sub-epic placement

Per #1059 (Phase -1 spike gating #304 sub-epic placement), investigated the doneness of `services/integrations/mcp/notion_adapter.py` (867 LOC) + `services/intelligence/spatial/notion_spatial.py` (637 LOC) against current architecture.

## Verdict

**"Close to ready"** — not "needs rework", not "superseded".

The integration is wired, dependency-resolved, and 16-of-17 tests pass. The 1,500+ LOC is live-but-dormant — gated by feature flag, lacking a provisioned API token. **Not** dead archaeology.

## Five questions answered

1. **Architecture alignment**: ✅ Fits the action-handler path. Notion is NOT in the floor's context-assembler (correctly — wrong surface for it). The post-floor architecture didn't move Notion's home; it added an orthogonal floor for ambient queries. Different surfaces; both can coexist.
2. **Test coverage**: ✅ 17 tests collected; 16 passing. The 1 failure is **test drift** (`test_notion_api_configuration` calls `adapter.configure_notion_api(...)` which doesn't exist) — same shape as #1054/#1056 we cleaned up Tuesday.
3. **Dependencies**: ✅ `notion-client==2.5.0` in requirements.txt; importable; all imports resolve.
4. **Configuration**: ✅ Scaffolding exists (`NOTION_API_KEY` env var; `NotionConfig` + `NotionConfigService`; feature-flag toggle). Activation needs only a real Notion integration token.
5. **Integration points**: ✅ Substantial wiring across intent-service action handlers, feature-level wrappers, domain service, router, plugin, publishing, Slack cross-ref, feature flags. Conventions match Slack's router pattern.

## Activation work estimate (real #304 scope, AFTER placement)

~4-8 hours, mostly small chunks:
- 1 stale test fix (~15 min)
- Audit other 17 tests for similar drift (~30 min)
- PM provisions Notion integration token (~15 min, PM-side)
- Verify feature-flag default (~5 min)
- Manual smoke: search + update against live workspace (~1-2 hours)
- Bugfix budget if smoke surfaces issues (1-2 hours, contingent)
- README activation doc (~15 min)

**Total mostly contingent on live-workspace smoke results.**

## Sub-epic placement recommendation

**M2f (post-floor coverage)** OR **M2-discovered (testing/scoring infra)**.

NOT M3 (artifact persistence) and NOT M5 (polish + distro) — those imply scope this work doesn't need.

I lean M2f because the activation closes a known gap rather than discovers new infra; but M2-discovered is also defensible as "operational follow-up to the Topic 7 walk."

PA + PM call. The full memo at `dev/2026/05/08/304-phase-minus-1-notion-investigation.md` has the per-question evidence + activation breakdown + integration-points table.

## What I'm asking

- **PA**: ratify sub-epic placement with PM. Update #304 body with the Phase -1 verdict.
- **PM**: when sub-epic is placed and you're ready to provision the Notion token, ping me and I'll do the activation pass.

## What this is NOT

- Not actually activating Notion (no token in env)
- Not modifying any Notion code
- Not fixing the 1 stale test (that's part of activation)

— Lead Developer, 2026-05-08
