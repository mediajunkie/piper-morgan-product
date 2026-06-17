# Skunkworks Phase 2 — Hosting & Marketplace Research Report

**Author**: PA (Piper Alpha) · **Date**: 2026-06-12 · **Status**: COMPLETE
**Plan**: `dev/active/pa-skunk-hosting-research-plan-2026-06-12.md`
**Prior research**: `dev/active/pa-plugin-marketplace-hosting-research-2026-06-07.md`
**Sources**: R1 agent (web research), R2 agent (codebase + web), P1/P2/P3 agents (skunkworks)

---

## Executive Summary

Three-bullet read:

1. **We can submit to the Anthropic community catalog now.** The submission path exists at `platform.claude.com/plugins/submit`, review is automated, and the auth-decoupled plugin is committed to the skunkworks repo (`9b4bab9`). The only gate before a live listing is Anthropic's review — which could happen this week.

2. **The ChatGPT path is cheaper than expected.** The ChatGPT Apps SDK is built on MCP. The same MCP server covers ~60–70% of what a ChatGPT app needs — the delta is UI widgets, OAuth 2.1 compliance, and a separate submission. Asana, Linear, and Figma all publish to both platforms from one MCP server.

3. **The single-user ceiling is the real scope question.** `alpha.pipermorgan.ai` is already hosted and proven. The listing can go live as a single-user/alpha-only plugin immediately. Multi-user distribution (multiple people on one instance) is gated on #1185 (per-user keys, M5) — which is already correctly scoped. The Phase 2 experiment should explicitly aim at the "does it list + load" question, not the "does it scale" question.

---

## Domain A — Official Anthropic Listing

### A1: Is there an official curated Anthropic plugin directory?

**Yes — two distinct tiers.** (Confidence: High — R1 agent verified against Anthropic developer docs)

| Tier | Name | Access | How to list |
|---|---|---|---|
| Official | `claude-plugins-official` | Auto-registered at Claude Code startup | Anthropic-curated only; no submission path |
| Community | `claude-plugins-community` | Available to individual/Team accounts | Submit at **platform.claude.com/plugins/submit** |

The community catalog has 287+ plugins. Review is automated (`claude plugin validate` + safety screening), SHA-pinned, with nightly syncs. There is no manual review timeline published — automated checks run at submission time.

**Actionable**: Submit to `claude-plugins-community`. No invite or partnership required.

### A2: Real hosted plugins in the wild

Five examples documented (Confidence: High for large platforms, Medium for indie):

- **Asana, Linear, Figma** — production integrations; each runs a persistent hosted MCP server endpoint + a plugin wrapper. GitHub-source distribution.
- **phuryn/pm-skills** — indie GitHub-hosted PM plugin. No hosted backend; pure skill layer.
- **openai/codex-plugin-cc** — GitHub-hosted; client-side only.

Pattern: production integrations own a persistent MCP server (like we do); indie plugins tend to be skill-only with no backend.

### A3: Claude Code plugin vs. MCP server registry — are these separate?

**Yes — two genuinely separate distribution paths.** (Confidence: High)

| Path | What it is | Where discovered |
|---|---|---|
| Claude Code plugin (`.claude-plugin/`) | Skills + MCP config bundle; install via `/plugin install` | claude.com/plugins, community catalog |
| MCP server registry | Discoverability from Claude Desktop + other MCP clients | Smithery (smithery.ai), mcp.run, glama.ai |

**Recommendation**: pursue both. They serve different user surfaces — Claude Code users install via the plugin system; Claude Desktop users add MCP servers directly. Same underlying MCP server; different packaging. Smithery listing is an additional 30-minute effort after the plugin is ready.

---

## Domain B — Hosted Endpoint Architecture

### B1: Minimal hosting options

**Already resolved.** (Confidence: High — Lead Dev ratification memo, 2026-06-12)

`alpha.pipermorgan.ai` IS the minimal hosted endpoint — DigitalOcean droplet + Caddy TLS + Let's Encrypt + basic-auth, v0.8.7. Seven Linux-portability issues already cleared (#1167/#1168/#1176). Docker + DO is validated. No new hosting infra needed for the marketplace experiment.

**The phase-2 experiment uses the existing alpha endpoint.**

### B2: Auth decoupling design

**Recommendation: user-supplied env var + meet-piper guided setup.** (Confidence: High)

| Option | Effort | UX | Notes |
|---|---|---|---|
| **(a) Env var (recommended)** | ~15 min | Tester sets `PIPER_BASE_URL`; meet-piper Part 6 guides setup | Converges with #1185 BYO-key roadmap |
| (b) Per-user API key issuance | Weeks | PM issues keys; tester stores in env | Requires new key-issuance infra |
| (c) OAuth 2.1 | Weeks | Best self-serve UX; full Claude Code plugin support | Right for open distribution; overkill for small alpha cohort |

The MCP plugin uses stdio transport (local subprocess) — auth is entirely in outbound `httpx` calls from `server.py` to `alpha.pipermorgan.ai`. The Piper server's `/api/v1/intent` already accepts bearer token auth. Server-side addition for Option (a): a static bearer-token check in Caddy or app layer (~15 min). `meet-piper` Part 6 (Integrations) can absorb the token-setup step, turning it into a guided onboarding moment.

**The P1 prototype (committed `9b4bab9`) implements Option (a)**: the hardcoded credential is removed from `.mcp.json`; `server.py` already reads `PIPER_BASE_URL` from env with `localhost:8001` fallback. The credential decoupling is done.

### B3: What hosted MCP needs vs. what exists

**No new requirements.** (Confidence: High)

The MCP protocol imposes nothing on transport/auth — the plugin uses local stdio, not remote HTTP. The only auth-relevant change is replacing basic-auth with bearer-token in the outbound calls. The FastAPI server behind Caddy can support this with a ~15-min config change.

For multi-user auth (per-user keys, not shared password): that's Gap C in #1185's design — correctly not in Phase 2 scope.

### B4: End-user install flow (hosted plugin, post-auth-decoupling)

1. PM/host shares the DINP marketplace URL with tester
2. Tester: `/plugin marketplace add mediajunkie/piper-morgan-skunkworks` (one-time, CLI)
3. Tester: `/plugin install piper-morgan@dinp`
4. Tester sets `PIPER_BASE_URL` env var (guided by meet-piper or QUICKSTART)
5. Tester: calls `meet-piper` → profile saved via MCP tool (no filesystem access)
6. Tester: `ask-piper` works against the hosted alpha endpoint

**Friction points**: (1) `uv` prerequisite (terminal required; could be bundled); (2) env var setup (meet-piper absorbs this); (3) Desktop-only testers may need CLI for marketplace add — GUI shows marketplace plugins but installation confirmation may still require CLI.

**Note**: Desktop vs. CLI install support is an open question (June 7 research flagged it). The primary alpha tester surface is Claude Code, so this isn't a blocker.

---

## Domain C — ChatGPT Plugin Path

### C1: ChatGPT App Directory status

**Open for submissions, but selective.** (Confidence: Medium — R1 agent research; no official timeline published)

The ChatGPT App Directory (distinct from the old plugin store, which is deprecated) is open. Hosting on a public domain with TLS is required. Review is not automated — manual review with no guaranteed timeline. Early access appears weighted toward established companies; indie submissions are processed but pace is slower.

### C2: Does ChatGPT support MCP?

**Yes — ChatGPT Apps SDK is built on MCP.** (Confidence: High — R1 agent; verified against OpenAI developer blog)

This is the key finding: the same MCP server covers approximately 60–70% of a ChatGPT app. The delta:
- ChatGPT-specific UI widgets (result cards, structured output rendering)
- OAuth 2.1 compliance (required for ChatGPT; Claude Code plugin OAuth is different)
- Accurate tool annotations per ChatGPT's spec
- Separate submission + review

No separate OpenAPI spec required (that was the old plugin system). The MCP Apps standard (supported by Claude Code, ChatGPT, Goose, VS Code as of January 2026) is the convergence mechanism.

### C3: Dual-publishing examples

**Asana, Linear, Figma** — all three publish to both Claude and ChatGPT via the same MCP server. The second-platform work was: UI widget implementation + OAuth 2.1 setup + per-platform submission. The server itself was reused. Estimate: 2–4 weeks of additional work for a mature MCP server; less for a simpler one.

**For Piper**: dual-publishing is feasible and the incremental cost is lower than building from scratch. ChatGPT path is a Phase 3 candidate after the Claude listing is live and tested.

---

## Domain D — Ecosystem Landscape

### D1: Comparable tools in Claude ecosystem

**Anthropic already has an official Verified "product-management" plugin.** (Confidence: High)

This is the differentiation challenge. The community catalog also has 5–7 PM-adjacent tools (ai-pm, PM AI Partner, 10x-team, anson, phuryn/pm-skills). Generic PM frameworks are well-covered.

**Piper's differentiation case must lead with**: personalized context calibrated to *your* work style, *your* projects, *your* voice — not generic PM frameworks. The "knows you" loop (meet-piper → calibrated ask-piper) plus the conscious-floor methodology and honest degradation behavior are what's genuinely novel.

**CXO note (ratification)**: Piper's identity must be channel-independent. The "trusted colleague who knows you" must read the same on Claude as on ChatGPT. Build the channel-independence test into the experiment from the start.

### D2: Cross-pollination (OpenLaws)

General/transferable only: hosted API-backed products benefit from clean separation between the auth layer and the capability layer. The auth decoupling work on the plugin mirrors lessons from any hosted API product. [Firewall applies — no client-specific context.]

---

## Prototype Status

| ID | Description | Status | Commit |
|---|---|---|---|
| P1 | Auth-decoupled `.mcp.json` — credential removed, TESTER-QUICKSTART updated | ✅ DONE | `9b4bab9` |
| P2 | GitHub-source marketplace.json — `git-subdir` source, PIPER_BASE_URL note | ✅ DONE | `9b4bab9` |
| P3 | MCP server-owns-config — `save_profile`/`get_profile` tools | ✅ ALREADY DONE (pre-existing) |  `7ee54c3` (tracked) |

**P3 finding**: `save_profile`, `get_profile`, `save_company_profile`, and `get_company_profile` were already implemented in `server.py` using `_read_profile`/`_write_profile` helpers. The `meet-piper` skill already routes through these tools (not filesystem). Issue #1157 fix was already live. The P3 prototype task found that the work was already done in a prior skunkworks session.

**Fable note**: The `claude-fable-5` model is not accessible via the Agent tool's subagent model parameter in the current environment (model resolves but agent creation fails). Prototype work was done with the default Sonnet model. For true Fable vibe-coding, PM can launch a Fable session directly and invoke the skunkworks work from there.

---

## Recommended Phase 2 Experiment Scope

### What to do now (no gates)

1. **Submit to Anthropic community catalog** — `platform.claude.com/plugins/submit`. Plugin is auth-decoupled and ready. Submission is the experiment: what does the review find? How long does it take? What do we need to change?

2. **Alpha tester distribution via DinP marketplace** — the marketplace scaffold is live (`git-subdir` source in `byoc/poc/dinp`). A tester can `/plugin marketplace add mediajunkie/piper-morgan-skunkworks` and install today. PIPER_BASE_URL must be set (guidance in QUICKSTART). Single-user only against the alpha endpoint.

3. **Document the channel-independence test** — per CXO's ratification note: explicitly test "does Piper feel like the same colleague across surfaces?" This is a design question to frame now, even if execution is Phase 3.

### What to do after Ship #047 + migration wave settle (per Exec capacity guard)

4. **Auth token infrastructure** — add bearer-token support to the alpha endpoint (Caddy config ~15 min + app-layer optional). Removes the basic-auth shared-password limitation for alpha testers.

5. **meet-piper Part 6 integration** — absorb PIPER_BASE_URL setup into the meet-piper guided onboarding flow. Turns a friction point into a feature.

6. **Smithery/mcp.run listing** — separate from the Claude plugin listing; adds Claude Desktop discoverability. 30-minute effort once the server is publicly documented.

### Phase 3 candidates (after #1185 lands)

7. **Multi-user hosting** — #1185 (per-user LLM keys, M5) unlocks true multi-tenancy. Until then, "distribute to anyone" means one Piper instance per deploy.

8. **ChatGPT App Directory submission** — same MCP server, OAuth 2.1 + UI widgets + submission. ~2–4 weeks incremental effort.

---

## Open Questions

| # | Question | What resolves it |
|---|---|---|
| OQ1 | Does the Anthropic community catalog review accept single-user/alpha plugins, or does it require multi-user auth? | Submit and find out; or contact Anthropic developer relations |
| OQ2 | What is the realistic review timeline for `claude-plugins-community`? | Submit and observe |
| OQ3 | Does Claude Desktop's GUI support full marketplace install, or does it require CLI? | Hands-on test with a Desktop-only user |
| OQ4 | Cross-user synthesis governance: when does Piper learn from one user's context inform another? | HOST + CIO gate — explicitly out of Phase 2 scope per CIO ratification note |
| OQ5 | Fable subagent access: can Fable be used for skunkworks prototype agents in the current environment? | Test from a Fable-model main session; current subagent path fails |

---

## Sources

- `pa-plugin-marketplace-hosting-research-2026-06-07.md` — Claude Code plugin mechanics (foundation)
- R1 agent web research (platform.claude.com/plugins/submit, Anthropic developer docs, OpenAI developer blog, Smithery, claudedirectory.org)
- R2 agent codebase analysis (`byoc/dist/piper-morgan/mcp/server.py`, auth option research)
- P1/P2/P3 agent findings (`byoc/dist/piper-morgan/` skunkworks, commits `9b4bab9` + `7ee54c3`)
- Lead Dev ratification memo (2026-06-12): endpoint-already-exists finding
- Exec ratification memo (2026-06-12): capacity guards + sequencing
- CXO ratification memo (2026-06-12): channel-independence discipline
- CIO ratification memo (2026-06-12): governance gate for cross-user synthesis
