# Marketplace & ChatGPT Distribution Research (R1)
**Date**: 2026-06-12  
**Author**: PA research agent  
**Feeds**: #1162 hosted distribution / Phase 2 scoping proposal  
**Prior research not repeated here**: `pa-plugin-marketplace-hosting-research-2026-06-07.md`

---

## Domain A — Official Anthropic Listing

### A1: Does Anthropic maintain an official curated plugin directory distinct from the self-hosted mechanism?

**Yes — and there are two distinct tiers. Confidence: High** (official docs + GitHub repos directly confirmed).

Anthropic runs two public plugin catalogs, both distinct from the self-hosted marketplace mechanism documented in the prior research file:

**Tier 1 — `claude-plugins-official` (curated, Anthropic-owned)**  
- GitHub: `github.com/anthropics/claude-plugins-official`  
- Registered automatically when any user first starts Claude Code interactively; visible at `claude.com/plugins`  
- Curated by Anthropic at its discretion. **There is no application process and no submission form for this tier.** The official docs state explicitly: *"The official marketplace, `claude-plugins-official`, is curated separately. Anthropic decides which plugins to include at its discretion. There is no application process, and the submission form does not add plugins to the official marketplace."*  
- If Anthropic decides to list your plugin, your CLI can surface a prompt suggesting installation to users (via the `plugin-hints` mechanism). This is not something you can trigger by request.  
- Plugins in this tier receive an "Anthropic Verified" badge and significantly higher discoverability.  
- Current content: ~30+ Anthropic-built plugins (LSP/language servers, integration plugins for GitHub/GitLab/Figma/Linear/Slack/Sentry/Supabase/Vercel/Firebase/Notion/Asana/Atlassian, security review, dev workflow, output style plugins).

**Tier 2 — `claude-plugins-community` (community, Anthropic-screened)**  
- GitHub: `github.com/anthropics/claude-plugins-community` (read-only mirror; 287+ plugins as of this research)  
- Users add manually: `/plugin marketplace add anthropics/claude-plugins-community`  
- **This is the publicly submittable tier.** Submission forms:  
  - For Team/Enterprise orgs: `claude.ai/admin-settings/directory/submissions/plugins/new`  
  - For individuals without Team/Enterprise: `platform.claude.com/plugins/submit`  
- Review pipeline: automated (`claude plugin validate` + safety screening). Approved plugins are pinned to a specific commit SHA in the catalog; CI bumps the pin automatically as you push new commits.  
- Catalog syncs nightly; delay possible between approval and public appearance.

**Submission criteria for community tier**:  
- Pass `claude plugin validate` (run locally before submitting — the review pipeline runs the same check)  
- Pass automated safety screening  
- Include a README.md with documentation  
- Standard plugin directory structure (see prior research for exact structure)  
- No explicit quality/complexity bar documented beyond the above

**Hosting requirements**: the plugin itself must be in a publicly accessible GitHub repository. The catalog entry pins to a commit SHA, not a URL. No server hosting required for the plugin code itself (the MCP server referenced by the plugin is a separate concern if the plugin bundles one).

**Important nuance**: the submission form submits to the community marketplace, not the official one. Getting into `claude-plugins-official` requires Anthropic's discretionary judgment, not a form submission.

**Sources**:  
- `code.claude.com/docs/en/plugins` (official create-plugins guide, "Submit your plugin to the community marketplace" section)  
- `code.claude.com/docs/en/discover-plugins` (discover-plugins guide, official vs. community distinction confirmed)  
- `github.com/anthropics/claude-plugins-official`  
- `github.com/anthropics/claude-plugins-community`  
- `aitoolly.com/ai-news/article/2026-05-25-anthropic-launches-official-claude-code-plugins-directory-to-enhance-ai-development-workflows`

---

### A2: Real hosted/published Claude Code plugins in the wild

**Confidence: High** for existence and hosting shape; Medium for exact catalog membership (not verified via direct JSON inspection for all).

**1. Asana**  
- Hosting shape: Anthropic-published plugin in `claude-plugins-official` that wraps Asana's MCP server (`https://mcp.asana.com/v2/mcp`, streamable HTTP over OAuth)  
- Install: `/plugin install asana@claude-plugins-official`  
- Asana also published a ChatGPT app (same underlying MCP server — see Domain C below for dual-platform detail)

**2. Linear**  
- Hosting shape: plugin bundling Linear's MCP server; listed in `claude-plugins-official`  
- Linear's MCP server simultaneously serves ChatGPT, Claude, Gemini, and Perplexity  
- Canonical example of a write-once-serve-many MCP architecture

**3. phuryn/pm-skills (community marketplace)**  
- GitHub: `github.com/phuryn/pm-skills`  
- 68+ PM skills across 9 plugins, distributed as a community marketplace (users add `phuryn/pm-skills` directly, not via the Anthropic community catalog)  
- Hosting shape: GitHub repo, relative-path source — the peer-to-peer model

**4. ai-pm (community marketplace)**  
- Listed in the community marketplace (`anthropics/claude-plugins-community`)  
- Description: "AI Product Manager transforming feedback into PRDs via stakeholder debates"  
- Hosting shape: GitHub repo (source SHA-pinned in catalog)

**5. OpenAI's codex-plugin-cc**  
- GitHub: `github.com/openai/codex-plugin-cc`  
- Published March 30, 2026: OpenAI published a Claude Code plugin that calls OpenAI Codex from within Claude Code  
- Notable as a competitor shipping into the Anthropic ecosystem — illustrates how open the community catalog is  
- Hosting shape: GitHub repo  

**General pattern**: production-grade integrations (Asana, Linear, Figma, Slack) all host a persistent MCP server endpoint (streamable HTTP or SSE) and wrap it in a Claude plugin. Community/indie plugins are GitHub-hosted relative-path or github-source; no server hosting needed for the plugin logic itself unless it bundles an MCP server.

**Discovery shape**: no single central listing drives discovery. The official claude.com/plugins page is the most curated; community plugins circulate via Reddit, GitHub topics, and aggregator sites (claudedirectory.org, claudemarketplaces.com).

**Sources**:  
- `developers.asana.com/docs/using-asanas-mcp-server`  
- `github.com/phuryn/pm-skills`  
- `github.com/openai/openai-apps-sdk-examples`  
- `smartscope.blog/en/blog/codex-plugin-cc-openai-claude-code-2026/`  
- `github.com/anthropics/claude-plugins-community` issues + marketplace.json (287+ plugins confirmed in raw JSON, 1.45 MB file)

---

### A3: Claude Code plugin vs. MCP server — are these separate distribution paths?

**Yes, meaningfully distinct. Confidence: High** (official docs confirm the architecture).

**The distinction**:

| Dimension | MCP Server (bare) | Claude Code Plugin (bundles MCP) |
|---|---|---|
| What it is | A running process exposing tools via MCP protocol | A self-contained directory with skills, agents, hooks, and optionally an MCP server config |
| User installs via | Manual `claude_desktop_config.json` edit, or Smithery (`smithery.ai`), or MCP registries (mcp.run, glama.ai) | `/plugin install <name>@<marketplace>` |
| Distribution path | MCP registries (Smithery, glama.ai, mcp.run) — separate from the Claude Code plugin system | Claude Code plugin marketplaces (official, community, or self-hosted) |
| Surfaces supported | Claude Desktop, Claude Code MCP mode, Cursor, VS Code, any MCP-compliant client | Claude Code and Claude Cowork only |
| Skills/hooks/agents | No | Yes |
| Auto-update | Via Smithery's install mechanism | Via marketplace auto-update system |

**For Piper Morgan specifically**:
- The existing plugin ships a `.mcp.json` that configures the Piper MCP server — this is the plugin-bundled-MCP-server pattern.
- As a standalone MCP server, Piper could also be listed on Smithery/mcp.run for Claude Desktop users without the Claude Code plugin layer (just the MCP connection, no skills/hooks). These are genuinely separate distribution paths serving different user surfaces.
- "Publishing a Claude Code plugin" and "publishing an MCP server" are not mutually exclusive — many integrations do both. They are also not redundant: the plugin adds skills, agents, hooks, and the marketplace install flow; the MCP listing adds discoverability from Claude Desktop and other MCP clients.
- **Recommendation implication**: Piper Morgan can pursue both paths. The MCP server listing (Smithery) is relatively low-friction (GitHub URL + description + category). The Claude plugin path requires a marketplace and optionally community-catalog submission.

**Claude Desktop distribution via Smithery**:
- Smithery (`smithery.ai`) is the de facto third-party MCP server discovery layer for Claude Desktop users. Publishing there = `smithery.ai/server/<your-slug>` with automatic install and updates.
- glama.ai/mcp and mcp.run are secondary MCP registries serving similar discovery roles.
- None of these are operated by Anthropic; they are community/third-party directories.

**Sources**:  
- `code.claude.com/docs/en/mcp` (MCP vs. plugin architecture)  
- `code.claude.com/docs/en/discover-plugins` (plugin system)  
- `smithery-ai/codemcp-1` GitHub (Smithery pattern)  
- `claudedirectory.org/plugins/mcp-registry` (MCP registry plugin)  
- Search results on Smithery/mcp.run/glama.ai ecosystem

---

## Domain C — ChatGPT Plugin / GPT Store

### C1: Current state of the ChatGPT App ecosystem for third-party developers

**Status: Open for submissions but selective in publishing. Confidence: High** (OpenAI official blog + developer docs).

The GPT Store (custom GPTs) is a separate and older system. What is relevant here is the **ChatGPT App Directory**, launched late 2025/early 2026, distinct from the original GPT Store.

**What changed**: OpenAI deprecated the plugin system (which used OpenAPI specs) and launched the **ChatGPT Apps SDK**, built on MCP as its backbone. The App Directory is the new distribution mechanism.

**Submission process**:
- Developers build via the Apps SDK (MCP-based), then submit at `developers.openai.com/apps-sdk/deploy/submission`
- Submission includes: MCP connectivity details, testing guidelines, directory metadata, country availability settings, test scenarios, MCP UI preview configurations, release notes
- **Prerequisites**: organization verification in OpenAI Platform Dashboard (individual or business); `api.apps.write` permission
- Review by OpenAI for safety, privacy, quality, and policy compliance; all apps pass through manual review before listing
- **No estimated review timeline**: OpenAI explicitly states "Review timelines may vary as we continue to build and scale our processes. Expedited review requests cannot be accommodated."

**Hosting requirements**:
- MCP server must be hosted on a **publicly accessible domain** (not localhost or test endpoints)
- Content Security Policy (CSP) must be defined to allow exact fetch domains
- OAuth 2.1 authentication supported and expected for user-authenticated tools
- Both streamable HTTP and SSE transport are supported; streamable HTTP recommended

**Entry criteria (rejection triggers)**:
1. Server connectivity issues (MFA/SMS blocking review bot, expired credentials)
2. Test case failures (outputs don't match expected; UI errors)
3. Data privacy violations (undisclosed user data returned, unnecessary PII)
4. Incorrect tool annotations (`readOnlyHint`, `destructiveHint`, `openWorldHint` flags inaccurate)
5. Non-compliance with OpenAI usage policies, safety/privacy standards

**Current access**: in practice, full publishing appears primarily available to larger companies in early 2026; wider developer access is expected to expand later in the year. Developers can submit and enter review queue; not all submissions result in public listing.

**Sources**:  
- `developers.openai.com/apps-sdk/deploy/submission`  
- `openai.com/index/developers-can-now-submit-apps-to-chatgpt/`  
- `venturebeat.com/technology/openai-now-accepting-chatgpt-app-submissions-from-third-party-devs-launches`  
- `community.openai.com/t/app-review-process-timelines-for-chatgpt-app-store/1378947`

---

### C2: Does OpenAI's platform support MCP? What's the technical overlap with an MCP server?

**Yes — the ChatGPT Apps SDK is built on MCP. Overlap is high. Confidence: High** (official OpenAI developer docs).

**Key finding**: OpenAI fully adopted MCP as the backbone of the ChatGPT Apps SDK. A tool that already implements a standard MCP server is the right starting point for a ChatGPT app.

**What a standard MCP server already provides**:
- Tool discovery (`list_tools` with JSON Schema contracts)
- Tool execution (`call_tool` request/response)
- Transport: streamable HTTP or SSE (both supported)

**What the ChatGPT Apps SDK adds beyond standard MCP** (additional work required):
1. **UI rendering**: return embedded resource widgets in response metadata so ChatGPT renders interactive components inline. This is a ChatGPT-specific extension — standard MCP has no UI layer.
2. **Extensible authentication**: OAuth 2.1, Client ID metadata, Dynamic Client Registration (DCR). Standard MCP auth handling varies; ChatGPT has specific requirements.
3. **Component state management**: structured data persistence across conversation turns (ChatGPT-specific).
4. **Tool annotations**: `readOnlyHint`, `destructiveHint`, `openWorldHint` flags must be accurate (reviewed during submission; Claude does not require these).
5. **Server-wide guidance**: optional initialization instructions providing cross-tool context for ChatGPT's model ranking.

**The MCP Apps standard** (proposed January 2026 via `blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/`): an official MCP extension for delivering UI capabilities. Supported by Claude, ChatGPT, Goose, and VS Code. This is the convergence layer that enables one server to serve both platforms without complete rewrites.

**Practical reuse estimate**: a working Piper Morgan MCP server would cover ~60-70% of what a ChatGPT app needs. The additional work is primarily:
- Implementing ChatGPT-specific UI widgets (optional but improves UX significantly)
- Ensuring OAuth 2.1 compliance with ChatGPT's specific profile
- Accurate tool annotations
- Hosting on a public domain (already a requirement for the Claude hosted path)

**What is NOT required**: a separate OpenAPI spec. The old ChatGPT plugin system used OpenAPI; the new App Directory does not. MCP is the mechanism.

**Sources**:  
- `developers.openai.com/apps-sdk/concepts/mcp-server`  
- `developers.openai.com/apps-sdk/quickstart`  
- `blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/`  
- `community.openai.com/t/future-of-chatgpt-apps-sdk-with-mcp-apps-standardization/1372743`

---

### C3: Real examples of tools published to both Claude and ChatGPT ecosystems

**Confidence: High** for existence; Medium for exact additional effort quantification (not published by vendors).

**Example 1: Asana**  
- Claude: listed in `claude-plugins-official` as an "External integrations" plugin; bundles the Asana MCP server (`https://mcp.asana.com/v2/mcp`)  
- ChatGPT: "The Asana app in ChatGPT" listed in the App Directory  
- Architecture: single MCP server endpoint, platform-agnostic. Both integrations use OAuth for user auth. The documentation for each platform is separate and platform-specific (help articles rather than implementation deltas), suggesting the per-platform effort was primarily auth flow configuration and ChatGPT UI widget implementation, not a new server.
- **Additional work for second platform**: estimated minimal on server side; primary effort in UI widget layer for ChatGPT and per-platform submission/review process.

**Example 2: Linear**  
- Claude: listed in `claude-plugins-official`  
- ChatGPT: Listed in App Directory  
- Architecture: single MCP server serving Claude, ChatGPT, Gemini, and Perplexity simultaneously. Explicit marketing of "write once, serve many."  
- Published May 25, 2026. Source: `everything-pr.com/linear-mcp-server`

**Example 3: Figma**  
- Claude: listed in `claude-plugins-official` (MCP server connecting to Figma Dev Mode)  
- ChatGPT: Claude AI Jan 27, 2026 announcement included Figma; ChatGPT also lists Figma  
- Architecture: MCP server that connects to local Figma Dev Mode session  
- Source: `macrumors.com/2026/01/27/claude-app-integration-asana-slack-figma-canva/`

**The pattern across all three**:
1. Build the MCP server once with streamable HTTP transport and OAuth 2.1
2. Submit to Anthropic community marketplace (straightforward, automated review)
3. Negotiate/apply for `claude-plugins-official` inclusion (no formal process; relationship/quality driven)
4. Submit to ChatGPT App Directory (requires UI widget implementation + manual review)
5. Optionally: list on Smithery/glama.ai for Claude Desktop users

For large partners (Asana, Linear, Figma): the second-platform effort is primarily UI widget implementation for ChatGPT + per-platform submission and review. The server itself is shared.

**Sources**:  
- `developers.asana.com/docs/using-asanas-mcp-server`  
- `everything-pr.com/linear-mcp-server`  
- `macrumors.com/2026/01/27/claude-app-integration-asana-slack-figma-canva/`  
- `venturebeat.com/infrastructure/anthropic-embeds-slack-figma-and-asana-inside-claude-turning-ai-chat-into-a`

---

## Domain D — Landscape: Comparable Tools in the Claude Ecosystem

**Confidence: High** for existence; Medium for feature/positioning details (sourced from directory listings, not firsthand use).

### The existing PM/productivity-assistant plugin landscape

The Claude Code plugin ecosystem has a meaningful cluster of PM-adjacent tools. Piper Morgan would not be entering an empty field. Key comparable tools:

**1. Anthropic's official `product-management` plugin** (`claude.com/plugins/product-management`)  
- Made by Anthropic; "Anthropic Verified"  
- Covers: feature specs, roadmap management, stakeholder communication, user research synthesis, competitive analysis, metrics review  
- Slash commands: `/write-spec`, `/roadmap-update`, `/stakeholder-update`, `/synthesize-research`, `/competitive-brief`, `/metrics-review`  
- Connects to external project trackers/tools via MCP  
- **Positioning note**: this is Anthropic's own PM plugin. Piper Morgan's differentiation must be clearly stated relative to this — likely Piper's advantage is personalization, the "colleague who knows your context" model, and the meet-piper setup flow.

**2. PM AI Partner** (community, claudedirectory.org productivity listing)  
- "12 PM-specific agent skills, 6 workflow commands, 3 automation hooks for Product Managers"  
- Closer in spirit to Piper Morgan's positioning than Anthropic's generic plugin

**3. phuryn/pm-skills** (community marketplace)  
- 68 skills, 42 chained workflows, 9 plugins across full PM lifecycle  
- Framework-based (Torres, Cagan, Savoia)  
- GitHub-hosted community marketplace, not in Anthropic's catalog  
- Very broad coverage; Piper Morgan's advantage is personalized context vs. generic frameworks

**4. ai-pm** (community marketplace, `anthropics/claude-plugins-community`)  
- "AI Product Manager transforming feedback into PRDs via stakeholder debates"  
- Narrower scope (PRD-focused); less personalization

**5. 10x-team** (community marketplace)  
- "12 specialized roles including Product Manager"  
- Multi-role team simulation; different use case from Piper's single-PM-partner model

**6. anson** (community marketplace)  
- "AI coworker setup across Slack, Notion, Gmail with automations"  
- Most similar to Piper's "connected colleague" model; different in that Piper is PM-specific and has personalization layer

**7. ai-team-os** (community marketplace)  
- "Team operating system with meetings, task walls, 79 MCP tools"  
- Enterprise-oriented; broader scope

**Landscape summary**: the Claude ecosystem has a genuine PM plugin cluster. Anthropic itself has staked out the generic PM workflow space. Piper Morgan's differentiation case rests on (a) the personalized-context/profile model (`meet-piper`), (b) the "knows your specific projects and voice" capability, and (c) the multi-surface/colleague framing vs. a feature-spec generator. The landscape makes a strong positioning case for Piper but also raises the bar for how sharply that differentiation is communicated in the plugin description.

**Sources**:  
- `claude.com/plugins/product-management` (fetched directly)  
- `claudedirectory.org/plugins/topic/productivity` (70 productivity plugins enumerated)  
- `github.com/anthropics/claude-plugins-community` raw marketplace.json (287+ plugins, PM cluster identified)  
- `github.com/phuryn/pm-skills`  
- `civillearning.medium.com/turn-claude-into-a-product-manager-100-open-source-pm-skills-you-can-install-today-b38fcd70389d`

---

## Summary Table: Distribution Path Decision Matrix

| Path | Gating requirement | Our current blocker | Effort estimate | Notes |
|---|---|---|---|---|
| Self-hosted Claude marketplace (our own repo) | None — publish when ready | Credential decoupling (Option A, per prior research) | Low | Documented in prior research file; actionable now pending auth decision |
| Community catalog (`claude-plugins-community`) | Pass `claude plugin validate` + safety screening | Same credential blocker + need public repo | Low-Medium | Submit via `platform.claude.com/plugins/submit`; automated review |
| Official catalog (`claude-plugins-official`) | Anthropic's discretionary judgment; no form | Not applicable | Unknown/relationship | No submission process exists; Anthropic decides |
| Smithery (MCP registry, Claude Desktop users) | GitHub URL + description | Same credential blocker | Low | Separate from plugin system; adds Claude Desktop surface |
| ChatGPT App Directory | OpenAI review; publicly hosted MCP server; OAuth 2.1 | Same credential blocker + UI widget work + OAI review | Medium-High | MCP server reuse is real; ~60-70% overlap; UI widgets + auth profile + review are the delta |

---

## Key Findings for Phase 2 Scoping

1. **The community catalog path is low-friction and real**: `platform.claude.com/plugins/submit`, automated review, SHA-pinned in a 287-plugin public catalog. Piper Morgan can pursue this without a relationship with Anthropic. The credential-decoupling (Option A) is the only prerequisite.

2. **The official catalog is not a form-based process**: there is no submission mechanism for `claude-plugins-official`. Anthropic invites plugins at its discretion. The community catalog + quality signal + relationship development is the on-ramp.

3. **Anthropic already has a PM plugin**: the official `product-management` plugin is "Anthropic Verified" and covers overlapping ground. Piper Morgan's pitch for official-tier consideration must lead with differentiation (personalized context, not generic PM frameworks).

4. **ChatGPT requires an MCP server (which we're already building) plus**: OAuth 2.1, UI widgets (ChatGPT-specific, non-trivial), tool annotations, public hosting, and manual review. The server is the biggest investment and is shared; the delta for ChatGPT is real but not a complete rebuild.

5. **MCP Apps standard is the convergence mechanism**: the MCP Apps extension (Claude + ChatGPT + Goose + VS Code all support it as of Jan 2026) means investing in this standard now has multi-platform payoff. Piper Morgan built on the MCP Apps standard can serve all four clients from one codebase.

6. **Smithery is a separate, low-effort win**: publishing the Piper MCP server to Smithery adds Claude Desktop discoverability with minimal work. This is not "publishing a plugin" — it's registering the server in the MCP registry layer.

---

*Research conducted 2026-06-12. Sources fetched directly from official documentation and live pages. Confidence levels noted per finding. Not peer-reviewed.*
