# BYOC hosted-alpha readiness checklist

**Filed**: 2026-09-15 (PA). **Rewritten 2026-09-29 (PA, MCP program owner since 09-26)** around the
live-units reality; the 09-15/09-23 pre-deploy planning version (Phase A/B/C framing, "not started"
rows) is fully superseded and is preserved in git history on this file. Snapshot, not source of
truth: re-verify against #1462 and the live host before treating any row as current.

## What is live (verified 2026-09-29 10:3x PT)

| #1462 criterion | State | Evidence (this session) |
|---|---|---|
| `mcp.pipermorgan.ai` on Fly.io, DNS + TLS | ✅ **ticked** | `/health` 200, TLS verify 0, v0.8.14.0 `add9b610` |
| Auth: OAuth preferred, API-key fallback | ✅ **ticked** | `/.well-known/oauth-protected-resource` → AS at `alpha.pipermorgan.ai/mcp/oauth`, scope `resources:read`; bearer fallback via `scripts/mint_mcp_token.sh` |
| Caller-identity resolution, fail-closed | ✅ **ticked** | unauthenticated `POST /mcp` → `401 identity_required`; unit tests 50/50 in `tests/unit/services/mcp/server/` |
| Fail-closed identity verified by test (incl. A cannot reach B) | ⏳ half | no-identity half holds; the cross-caller half is **#1458, OPEN** (safe while there is exactly one caller) |
| Resources for reads / tools for writes | ⏳ half | three read resources live (profile, colleague-model, github-issues); no write tools yet |
| Tool catalog derived from registry, situation-named | ❌ | no tools exposed; naming test done (4 passes, recorded on #1462) |
| Claude plugin package | ❌ | manifest draft `dev/2026/08/30/plugin-manifest-draft-2026-08-05.md`; activation (live `.claude-plugin/` path) is an unmade decision |
| ChatGPT path | ⏳ ready to try | the OAuth flow is exactly what ChatGPT's connector needs; **untested until PM connects** |
| BYOC Claude / ChatGPT user can add and interact; setup is one-time | ❌ | awaits tester #1 |
| First-contact demonstration | ❌ | awaits tester #1 |
| Consequential refusals as failure-shaped payloads | ❌ untested on host | design result 6/6 on both vendors (08-02 probe); retest owed against the deployed host once a refusal path exists |
| Recomposition rubric branch | informs design | rubric v0.8.2 §6e: mitigation holds on Claude, fails on GPT-4o; **T-MCP-surface UNMEASURED** |

Checked boxes on #1462: **3 of 15** (was 0 of 15), with the evidence comment posted there.

## What happens next, in order

1. **PM connects as tester #1** (ChatGPT first, then Claude). Tester copy: add
   `https://mcp.pipermorgan.ai/mcp` as a connector → sign in at alpha.pipermorgan.ai → approve
   read-only access → "ask it what it knows about you." PA watches for this and helps debug live.
   Three gaps to state plainly beforehand: #1458 open (safe with one caller); T-MCP-surface
   unmeasured (this session is its first real observation); colleague-model resource reads nearly
   empty.
2. **After first contact**: tick the ChatGPT-path / first-contact boxes only on observed evidence;
   record the recomposition-honesty observation against the rubric.
3. **Build track** continues via PPM's increment series (#1701–#1707, milestone Production).
   Sequencing is PPM's, build is Lead's; PA does not re-derive either.
4. **#1458 before a second caller.** It is the hard gate on onboarding anyone besides PM.

## Not resolved here (someone else's decision)

Plugin activation (making this repo a discoverable Claude Code plugin). #1462 is now on milestone
Production; its timeline beyond that is PM/PPM's call.
