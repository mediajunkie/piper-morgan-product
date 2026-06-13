# Skunkworks Phase 2 — Hosting & Marketplace Research Plan

**Author**: PA (Piper Alpha) · **Date**: 2026-06-12 · **Status**: ACTIVE
**Parent**: BYOC Phase 2 ratification fan-out (`cc6401c13`, 2026-06-12)
**Deliverable**: `dev/active/pa-skunk-hosting-research-report-2026-06-12.md`
**Prototype target**: `piper-morgan-skunkworks/hosted/` (new subdirectory)

---

## Prior Research Already Done (DO NOT RE-COVER)

**`dev/active/pa-plugin-marketplace-hosting-research-2026-06-07.md`** (June 7, sourced from code.claude.com/docs + local CLI v2.1.166) has answered:

- ✅ Claude Code plugin marketplace mechanics: a GitHub repo with `.claude-plugin/marketplace.json` + per-plugin `plugin.json`
- ✅ Source types: relative path / github / url / npm / git-subdir
- ✅ Auto-update: OFF by default for third-party; enable per-marketplace or via `extraKnownMarketplaces`
- ✅ **Critical constraint identified**: embedded credential in `.mcp.json` blocks a public marketplace; must decouple auth before we can host publicly (Option A: user-supplied / server-side auth → converges with BYO-key roadmap)
- ✅ Concrete path to host the DinP marketplace (4-step)
- ✅ Open questions captured (Desktop install support, auth-decoupling design, per-user auth)

This research plan picks up where June 7 left off. **Researchers must read that file before starting.**

---

## What Still Needs Answering

### Domain A — Official Anthropic Listing (Beyond Self-Hosted Marketplace)

The June 7 research covers the *self-hosted* Claude Code plugin marketplace (a GitHub repo anyone can publish). What we don't know:

| ID | Question | Why it matters |
|---|---|---|
| A1 | Does Anthropic maintain an **official curated plugin directory** distinct from the self-hosted mechanism? (Like an "app store" vs "sideloading".) If so: what are the submission criteria, review process, and hosting requirements? | Whether we can/should apply for Anthropic endorsement, not just self-host |
| A2 | What does the **current state** of the Anthropic MCP ecosystem / plugin catalog look like? Who has published, and at what hosting shape? (3–5 examples of real published plugins/MCPs with sources visible) | Calibrate what's actually deployed vs. what the docs describe |
| A3 | Is there a distinction between the **Claude Code plugin system** (`.claude-plugin/`) and the **MCP server registry** (the `claude_desktop_config.json` / MCP spec level)? For Piper, are we publishing a Claude Code plugin, an MCP server, or both? | Clarifies which "marketplace" we're even targeting |

### Domain B — Hosted Endpoint Architecture

June 7 identified the credential/auth constraint. Now we need to scope what "a hosted Piper endpoint" actually requires:

| ID | Question | Why it matters |
|---|---|---|
| B1 | What does a minimal production-viable Piper hosting look like at alpha scale (~10 users)? Compare: (a) current DO droplet with basic-auth, (b) containerized + TLS + domain, (c) managed PaaS (Fly.io, Railway, Render). Criteria: cost/mo, setup burden, stack compatibility (PG 5433, Redis, ChromaDB). | Concrete options table before we commit to a hosting shape |
| B2 | The June 7 research identifies "auth decoupling" as gating. What does Option A concretely look like for Piper's API? Options: (1) user-supplied env var for auth token, (2) per-user API key issued at registration, (3) OAuth. Which integrates cleanest with #1185 (per-user LLM keys, M5)? | Auth design decision; must resolve before we can go public |
| B3 | What API surface does a hosted MCP server need that localhost doesn't? (TLS termination, stable URL, CORS headers, keep-alive considerations, rate limiting shape). Can the existing FastAPI app serve this with minor config changes? | Scope estimate for "is this a config change or a build?" |
| B4 | What does end-user plugin installation look like for a **hosted** Piper? Walk through: `/plugin marketplace add <our-repo>` → `/plugin install piper-morgan` → auth setup → first use. What are the friction points a tester will hit? | Informs UX design for the alpha distribution |

### Domain C — ChatGPT / OpenAI Plugin Path

No prior research on this. This is a parallel distribution channel for future phases.

| ID | Question | Why it matters |
|---|---|---|
| C1 | What is the current state of the **ChatGPT plugin / GPT store** for developer-published tools? Entry criteria, hosting requirements, review process, timeline. Is it open, invite-only, or paused? | Assess viability of parallel ChatGPT distribution |
| C2 | How does the **MCP protocol** connect to ChatGPT? Is there an MCP-compatible plugin format for OpenAI, or does it require a separate OpenAPI spec? What's the overlap? | Whether our MCP server reuses across both platforms or needs a separate build |
| C3 | What real-world examples exist of tools published to BOTH Claude and ChatGPT plugin ecosystems? What was the additional effort? | Reality check on how much work dual-publishing is |

### Domain D — Ecosystem Landscape (Brief)

| ID | Question |
|---|---|
| D1 | What comparable AI assistant / productivity tools exist in the Claude plugin ecosystem? Named examples only; brief characterization. |
| D2 | From the OpenLaws cross-pollination: any transferable lesson about hosted MCP / API products in production? (General/transferable only — client IP firewalled.) |

---

## Prototype Scope (Fable vibe-coding — parallel to research)

These are exploration artifacts, not production code. Fable model: `claude-fable-5`.

| ID | Prototype | Builds on June 7? | Goal | Pass criterion |
|---|---|---|---|---|
| P1 | **Auth-decoupled plugin** — modify the existing skunkworks plugin's `.mcp.json` so it accepts `PIPER_AUTH_TOKEN` as an env var instead of embedding basic-auth in the URL. Update `plugin.json` accordingly. | Yes — implements June 7 Option A | Prove auth can be decoupled without breaking the MCP tool calls | Plugin installs cleanly; `ask_piper` works with env-var auth; no hardcoded cred |
| P2 | **Public marketplace scaffold** — create the `.claude-plugin/marketplace.json` structure in `piper-morgan-skunkworks/` (or a sibling repo) that lists Piper as a plugin with `github` source type. | Yes — implements June 7 concrete path step 1 | Have a real marketplace repo structure that testers could `/plugin marketplace add` | Marketplaces.json is valid; plugin.json references the right paths; CLI can parse it |
| P3 | **MCP-server-owns-config tool** — add `save_profile` / `get_profile` tools to the MCP server (wrapping existing or new Piper API endpoints) so profile storage goes through the MCP server, not the agent's `~/.claude/` filesystem. | New (Cowork finding from June 5) | Eliminate the filesystem dependency for profile storage | Profile round-trips through MCP tool; no `~/` filesystem access required |

Prototype location: `piper-morgan-skunkworks/hosted/` (create if absent; sibling to `byoc/`).

---

## Deliverable Structure

**`dev/active/pa-skunk-hosting-research-report-2026-06-12.md`** will contain:

1. **Executive Summary** — 3 bullets: what we can ship now, what requires auth work first, what requires marketplace review
2. **Domain A: Official Anthropic listing** — is there a curated directory? What does it take?
3. **Domain B: Hosted endpoint scope** — options table + auth design recommendation + integration with #1185
4. **Domain C: ChatGPT path** — viability + effort estimate for dual-publishing
5. **Domain D: Ecosystem landscape**
6. **Prototype status** — P1/P2/P3 pass/fail against criteria
7. **Recommended experiment scope** — specific proposal for Phase 2 skunkworks experiment (ready to drop into ratification follow-up when responses arrive)
8. **Open questions** — explicitly named unknowns that require PM decision or external information
9. **Sources** — all citations

**Confidence levels** throughout: High (official doc/direct evidence) / Medium (inferred) / Low (labeled speculation).

---

## Execution Plan

**Research subagents** (run in parallel; both start by reading June 7 file):
- **R1** (general-purpose): Domains A + C + D — web research (Anthropic docs, Claude Code docs, OpenAI plugin docs, ecosystem scan)
- **R2** (Explore + general-purpose): Domain B — codebase analysis of existing skunkworks plugin + web research on hosting options

**Prototype subagents** (Fable, parallel to research):
- **P-agent** (Fable): P1 + P2 in sequence (auth decoupling first, then marketplace scaffold — P2 depends on P1's auth-decoupled plugin.json)
- **P3-agent** (Fable): P3 independently (MCP-server-owns-config — independent of auth work)

PA synthesizes all into the deliverable report.

---

## Verification & Audit Criteria

- [ ] Every factual claim has a source citation or explicit "not publicly documented" note
- [ ] Every confidence level is justified
- [ ] Every prototype has a pass/fail verdict against its success criterion
- [ ] Open questions section names unknowns and what resolves each
- [ ] Report is self-contained — a cold reader understands context + findings + recommendations
- [ ] June 7 findings not re-researched; June 7 file cited as prior work foundation

---

## Out of Scope

- Production hosting decisions (M4/M5 roadmap territory)
- #1185 per-user LLM key implementation (moved to M5 sprint)
- Mobile skunkworks
- Any client-specific IP from OpenLaws engagement
- Re-researching the Claude Code plugin mechanics already covered by June 7 file
