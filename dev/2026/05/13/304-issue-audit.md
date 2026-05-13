# #304 CONV-INFR-NOTN: Activate Existing Notion Integration — Phase 0 audit

**Issue**: [#304](https://github.com/mediajunkie/piper-morgan-product/issues/304) — Activate Existing Notion Integration
**Predecessor**: [#1059](https://github.com/mediajunkie/piper-morgan-product/issues/1059) Phase -1 spike CLOSED 2026-05-08 with "close to ready" verdict
**Branch**: `claude/1059-notion-activation` (worktree `piper-morgan-product-1059`)
**Date**: 2026-05-13

---

## Pattern-067 check (5 days post-#1059)

May 8 Phase -1 memo (`dev/2026/05/08/304-phase-minus-1-notion-investigation.md`) said: "Notion is wired, dependency-resolved, ~94% tested-passing; 4-8 hours of work, mostly contingent on real-workspace smoke." Re-verified today against current main:

| May 8 finding | Today (May 13) | Match |
|---|---|---|
| `services/integrations/mcp/notion_adapter.py` 867 LOC | 867 LOC | ✅ |
| `services/intelligence/spatial/notion_spatial.py` 637 LOC | 637 LOC | ✅ |
| `should_use_spatial_notion()` default True | Default True (`USE_SPATIAL_NOTION`) | ✅ |
| Action-handler routing path (not floor context) | Unchanged | ✅ |

**One material drift since May 8** (Pattern-067-shaped):

- May 8 memo: "17 tests, 16 pass, 1 fail (`test_notion_api_configuration` references removed `configure_notion_api`)"
- Today: across `test_notion_integration.py` + `test_notion_spatial_integration.py` + `test_notion_adapter.py`, I see **17 pass / 9 fail / 1 skipped**
- All 9 failures are the same shape: `AttributeError: 'NotionMCPAdapter' object has no attribute 'configure_notion_api'`. May 8 only sampled one test file; the broader sweep shows the same drift hits 9 tests in `test_notion_spatial_integration.py` (verified: `grep -c configure_notion_api tests/features/test_notion_spatial_integration.py` = 9)

**Conclusion**: NEGATIVE on the architecture side — May 8's verdict holds. POSITIVE for test-drift estimate — fix-scope is ~10 tests, not ~1.

---

## What activation needs (May 8 memo, validated today)

| Task | Estimate | Owner |
|---|---|---|
| Provision Notion integration token (Notion admin UI) | 15 min | PM |
| Add token to `.env` + keychain (mirroring Anthropic pattern) | 5 min | PM |
| Verify `should_use_spatial_notion()` default is sensible | 5 min | Lead Dev (✅ verified: True) |
| Fix `configure_notion_api` test drift across ~10 sites | 45-60 min | Lead Dev |
| Audit other notion tests for similar drift | 30 min | Lead Dev |
| Manual smoke: `search_documents` against live workspace | 30-60 min | PM or Lead Dev |
| Manual smoke: `update_document` against live workspace | 30-60 min | PM or Lead Dev |
| Bugfix budget if smoke surfaces issues | 1-2 hr (contingent) | Lead Dev |
| Update `services/integrations/notion/README.md` for the activation | 15 min | Lead Dev |

**Total**: ~5-8 hours (up from 4-8 in May 8's estimate, due to the broader test-drift surface). Mostly bounded once the token lands.

---

## Open design questions (Q1–Q7)

### Q1 — Token + workspace provisioning

PM needs to:
- Create a Notion integration at https://www.notion.so/my-integrations
- Decide whether the integration scope is read-only (search/list) or read+write (search + update_document)
- Share the integration with the target workspace pages/databases
- Provide the `secret_*` or `ntn_*` token to Lead Dev via:
  - **(a) `.env` write** — easiest; matches the existing `NOTION_API_KEY` env var pattern
  - **(b) Keychain entry** — matches Anthropic key pattern; survives worktree-isolation (per yesterday's #1070 finding, this is the more durable path)

**Recommendation**: **(b) keychain**, with a keychain entry `notion` so the same `KeychainService().get_api_key("notion")` pattern works as `anthropic` does. Requires verifying `config/notion_config.py:NotionConfig` falls back to keychain when env is empty — small adapter change (~10 lines, mirrors the #1070 fallback I added to `canonical-retest-run8.py`).

### Q2 — Test-fix scope

- **(a) Minimum**: fix only the 9 `configure_notion_api` failures so the suite is green
- **(b) Full audit**: walk all 27 notion-related tests for any other stale-API references; rewrite if found
- **(c) Beyond**: also add coverage for the `search_documents` / `update_document` happy paths if missing

**Recommendation**: **(b) full audit** — same pattern that caught the #1063 stale-test-cluster. May 8 only sampled, so a deliberate sweep is the safe move. Adds ~30 min to the estimate.

### Q3 — Smoke methodology + workspace

Two roles in smoke:
- **(a) Lead Dev runs smoke** with PM-provided token against PM's workspace — fast feedback loop, PM watches
- **(b) PM runs smoke themselves** after Lead Dev ships the test fixes + README — slower, but PM gets hands-on verification

**Recommendation**: **(a) Lead Dev runs initial smoke** (search-only first), then PM verifies `update_document` themselves since writes touch their workspace state. Hybrid keeps the Lead Dev feedback loop tight while PM owns the write verification.

### Q4 — Bugfix budget cap + ship gate

If live-workspace smoke surfaces real bugs, two stances:
- **(a) Fix-or-ship-partial**: ship `search_documents` as alpha-ready even if `update_document` needs more work
- **(b) Hold until clean**: ship both or neither — no partial activation

**Recommendation**: **(a) fix-or-ship-partial**. Search is the read-only, low-risk path; update is the higher-risk write. Shipping search first gates risk while still moving the alpha story forward. May 8 framed the work this way implicitly.

### Q5 — Sub-epic placement

May 8 memo: "M2f or M2-discovered". M2f is now closed (4 sub-epics shipped May 9-12); M2-discovered is the testing-infra parking lot. Neither perfectly fits an activation task.

- **(a) M2f reopened as M2f-F** for the activation
- **(b) M2-discovered** (with the understanding that "discovered" is now broadening from testing-infra to "integration activation that was always in alpha scope")
- **(c) Standalone milestone** under "MVP" without a sub-epic tag
- **(d) M3** if PM wants to defer post-alpha

**Recommendation**: **(c) standalone under MVP** since this is a single bounded ship, not part of a structured sub-epic walk. Tag the issue with `priority: medium` (alpha-scope per PM ratification, but not blocking the current week's work).

### Q6 — Scope of first ship: search-only vs. full

- **(I) Minimum**: search_documents only (read path; no write risk; gates the credential plumbing + test cleanup)
- **(II) Full**: search + update_document (matches #304's body; full activation)
- **(III) Full + auxiliary**: II + slack-cross-reference verification (`slack_integration_router.py` cross-references Notion config per May 8 inventory)

**Recommendation**: **(I) search-only first ship**, then **(II)** as a follow-up if PM has bandwidth same-session. Splits the risk; matches yesterday's "split related issues" memory rule.

### Q7 — Feature flag posture for alpha

`USE_SPATIAL_NOTION` defaults True. `ALLOW_LEGACY_NOTION` defaults TBD. Three stances:
- **(a) Keep both flags as-is** — spatial primary, legacy fallback
- **(b) Lock to spatial only** — set `ALLOW_LEGACY_NOTION=False`, delete legacy fallback codepath (M2g-style cleanup)
- **(c) Lock to legacy only** — disable spatial, use legacy plugin (defensive if spatial smoke surfaces issues)

**Recommendation**: **(a) keep both flags**, run smoke against spatial path. If smoke fails on spatial but legacy works, that's useful data — and the fallback is the alpha safety net. Cleanup to (b) is M2g concern, not this ship.

---

## Suggested gameplan shape (pending PM Q1–Q7 disposition)

Conditional on PM picking recommended answers:

- **Phase 1** (~10 min): keychain fallback in `config/notion_config.py:NotionConfig` (mirroring yesterday's #1070 `canonical-retest-run8.py` pattern — try env, fall back to `KeychainService().get_api_key("notion")`)
- **Phase 2** (~45-60 min): fix the 9 `configure_notion_api` test failures + sweep all 27 notion tests for other drift
- **Phase 3** (PM blocked): PM provisions Notion integration token + stores in keychain
- **Phase 4** (~30 min): Lead Dev runs `search_documents` smoke against PM's workspace, captures evidence
- **Phase 5** (PM action, ~30 min): PM verifies `update_document` smoke themselves
- **Phase 6** (~1-2 hr, contingent): bugfixes if smoke surfaces issues
- **Phase 7** (~15 min): update `services/integrations/notion/README.md` with activation evidence + token-provisioning steps for future users
- **Phase 8** (~10 min): merge + close #304

**Realistic total**: ~5-8 hours including PM-blocked steps. The Lead-Dev-only chunks are ~2-3 hours.

---

## Risks

1. **Token provisioning bottleneck**: Phase 3 + Phase 5 require PM time. If PM is heads-down on other work, the activation stalls. Mitigation: Lead Dev ships Phase 1-2 as a pre-activation foundation (clean tests + keychain fallback) so PM's later 15 min unblocks everything else.
2. **Spatial path bugs**: the 9 stale tests suggest there's been API drift on `NotionMCPAdapter` that the test-fix surfaces; if the production callers (e.g. `notion_queries.py`) have similar drift, smoke may fail in unexpected ways. Mitigation: include a callsite audit in Phase 2.
3. **Live-workspace state risk**: `update_document` smoke writes to PM's actual Notion workspace. If we hit an undocumented permission, the write may corrupt data. Mitigation: PM owns write smoke per Q3=(a); Lead Dev sticks to read.
4. **Pre-floor code drift over 9 months**: the integration was last actively developed Aug 2025. The Notion API itself may have evolved (deprecations, new pagination conventions). Mitigation: smoke surfaces this; bugfix budget covers it.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #304 (and predecessor #1059) |
| Pattern-067 check | ✅ NEGATIVE on architecture; POSITIVE on test-drift surface (broader than May 8 noted) |
| Body-vs-reality | ✅ May 8 memo validated against current main; one delta surfaced |
| Existing infra mapped | ✅ adapter / spatial / router / config / feature-flag / 8 production callsites |
| Live-data verification | ⏸ deferred (requires PM-provisioned token; Phase 0 spike intentionally read-only) |
| Scope questions | ✅ Q1–Q7 |
| Risk assessment | ✅ provisioning bottleneck + spatial-path drift + live-workspace write risk + 9-month code-drift |
| Recommended path | ✅ 8 phases ~5-8 hr (mostly contingent on PM availability) |

---

## STOP — awaiting PM disposition on Q1–Q7

Most have clear recs. **Most consequential**:
- **Q1 (provisioning path)** — keychain vs env determines Phase 1's shape
- **Q3 (smoke split)** — determines wall-clock-time / PM-availability balance
- **Q6 (search-only first vs. full)** — determines whether this is one ship or two

— Lead Developer
