# PDR-006: Hosted MCP Endpoint + Plugin Distribution Model

**Status**: Review — PM approved direction (2026-07-19); **Arch review COMPLETE 2026-07-29, no objection to ratifying.** CXO / PPM review still outstanding.
**✅ Ratification UNBLOCKED (2026-07-29).** ~~Q2 blocks ratification~~ — **Q2 is RESOLVED, and was never actually open.** PM ruled it **2026-01-08**: *"Start with rule-based (Option A), evolve to LLM later (#558)"* (`services/standup/preference_extractor.py:8`). Option A is **shipped**; the LLM evolution is **#558, OPEN, milestone Production (1.0), due 2026-10-30** — i.e. scheduled *after* this phase. **The "no server LLM" premise holds, on running code and precedent rather than assumption.** Arch verified empirically: zero LLM references across `services/mux/` (incl. the 584-line `composting_pipeline.py`) and across all four preference/personality modules.
*Provenance note, because it's the lesson: PA elevated Q2 to a blocker on sound reasoning but did **not** check it against the running system — the PDR said "open," so PA treated it as open. Arch went and looked. **Verify-first applies to a document's own claims about itself.** Cost: ten days of blocked status on an already-decided question.*
**Date**: 2026-07-19
**Author**: PA (Piper Alpha) — on behalf of PM
**Stakeholders**: PM, Arch, CXO, PPM, Lead Dev
**Supersedes**: MCPB skunkworks POC (not a formal PDR — superseded informally)
**Extends**: PDR-005 (Bring Your Own Chat — Distribution Model, ratified Jun 5, 2026)

---

## Decision

Piper's primary distribution model for alpha/beta is:

1. **Hosted MCP endpoint** at `mcp.pipermorgan.ai` — a pure tool server; no server-side LLM calls
2. **Claude plugin package** — CLAUDE.md (persona + instructions) + hooks/ (lifecycle) + skills/ (procedures) + the MCP URL, delivered as a single package; primary distribution for all Claude surfaces (Chat, Cowork, Code)
3. **ChatGPT integration** — the same hosted MCP URL as a remote MCP connection, plus individual SKILL.md files (zipped when dependencies are needed, plain `.md` when self-contained); BYOC ChatGPT user adds the MCP and each skill manually

Both clients connect to the same hosted MCP endpoint. The client LLM (Claude or GPT-4) provides reasoning; Piper's server provides tools, connectors, and persisted context.

---

## Context

PDR-005 (Jun 5, 2026) established the strategic split: *"server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history."* That decision was abstract about how the server is accessed.

Through the MCPB skunkworks POC (May–July 2026), the team explored a locally-run MCP bundle approach. PM confirmed July 18, 2026 that MCPB is a dead end: it required users to run infrastructure locally, had no clean path to production, and obscured the real distribution pattern now available via hosted remote MCP support in both Claude and ChatGPT platforms.

The timing is right: both platforms have recently shipped native support for hosted/remote MCP, including plugin-directory listings (Claude) and remote MCP + skills (ChatGPT). The correct production path is hosted, not locally-run.

The BYOC LLM key question (raised during MCPB: "how does the user's LLM call happen without server-side LLM infrastructure?") **dissolves** in this model: the user's own chat platform provides the LLM. Piper's server provides connectors and context. No server-side LLM key is needed for the hosted MCP phase.

---

## User Need

A BYOC user wants to use their existing Claude or ChatGPT subscription to access Piper's capabilities — connectors, stored profile, colleague model, working memory — without running any Piper infrastructure locally. They want a one-time setup (add MCP URL + plugin) and then Piper works inside their normal chat environment.

Different BYOC users have different levels of technical comfort. The plugin package abstracts the setup; the skill files give power users explicit capability discovery.

---

## Decision Rationale

### Why hosted over locally-run

- No local infrastructure requirement for end users
- Piper maintains the server; users get updates automatically
- Auth model (OAuth or API key) is simpler than MCPB's credential theater
- Both Claude and ChatGPT now support remote hosted MCP natively

### Why Claude plugin package is the primary distribution

- A single package (CLAUDE.md + hooks + skills + MCP URL) gives Claude users the full Piper experience
- Supported by Chat, Cowork, and Code (with varying levels of hook support — Chat doesn't use hooks yet, but the package degrades gracefully)
- Claude's plugin directory provides organic discoverability
- The plugin format is familiar to Claude Code users (CLAUDE.md is already a known surface)

### Why the hosted MCP is a pure tool server (no server-side LLM)

- PDR-005 established this split; this PDR makes it concrete
- For the hosted MCP + plugin phase, Piper's "intelligence" is: stored user profile, colleague model, connectors, MUX lifecycle state, composted learning (ADR-054)
- The client LLM reasons over that context; Piper serves it
- This keeps Piper's server costs low and avoids needing a server-side API key during alpha/beta
- Exception (deferred to M4): proactive/scheduled server-side agentic flows would need a server-side LLM — three options under consideration: Piper's own key (subscription model), BYOC key stored encrypted via #1382, or all reasoning pushed to client

### Why ChatGPT alongside Claude

- ChatGPT users are a significant BYOC population
- The same hosted MCP URL works; skill files are ChatGPT's equivalent of Claude's plugin CLAUDE.md
- Reach both major AI chat platforms with minimal additional infrastructure
- GPT plugin directory provides a second discovery channel

---

## Capability Split: Plugin vs. Server

The following captures what lives in the plugin package vs. what stays on the server — important for implementation planning.

### In the plugin package (ships to user's device/chat)

| Component | Format | Purpose |
|---|---|---|
| CLAUDE.md | Markdown | Piper's persona, instructions, how to invoke skills |
| skills/ | .md files | Procedures Piper can run (fetch contacts, find meeting context, etc.) |
| hooks/ | .sh or .py | Lifecycle hooks (session start, pre-commit, etc.) — Claude Code only |
| MCP URL | String in CLAUDE.md | Connection point to `mcp.pipermorgan.ai` |
| Connector guidance | Section in CLAUDE.md | Which MCP tools correspond to which connectors |

### On the server (hosted at mcp.pipermorgan.ai)

| Capability | Notes |
|---|---|
| User profile | How user describes themselves, role, org |
| Colleague model | How user works — inferred patterns, preferences, contexts |
| Composted learning / InsightJournal (ADR-054) | What Piper has learned from prior sessions |
| Connector grants | Which connectors the user has authorized |
| MUX lifecycle state | Modeled User Experience state (active projects, current context) |
| Trust graduation state | Where user is in the trust model |
| Tools / connector implementations | The actual MCP tools (GCal, Notion, GitHub, etc.) |

---

## Alternatives Rejected

### Continue with MCPB (locally-run MCP bundle)
Rejected: requires local infrastructure, no clean production path, credential model was theater, now superseded by native hosted MCP support in both platforms.

### Build a bespoke web UI as primary surface
Not rejected entirely — PDR-005 already preserves this as an asymptotic target for discrete surfaces that can't work in chat. But it's not the primary distribution for alpha/beta; the BYOC chat + hosted MCP path is faster to ship and reaches users where they already are.

### Require server-side LLM for all Piper capabilities
Rejected for this phase: unnecessary for connectors + context serving, adds cost and infrastructure complexity, breaks the "client provides intelligence" principle from PDR-005. Revisit in M4 for server-side agentic flows.

---

## Implications

### For CXO
- Plugin package UX needs design: what does a user's first experience of the Piper plugin look like? Onboarding flow for connecting MCP + adding skills. ChatGPT manual-add flow is notably more friction than Claude's (each skill added separately).

### For Arch — ✅ reviewed 2026-07-29; mechanism set holds, with one named risk

- ✅ **`mcp.pipermorgan.ai` on Fly.io (DNS/TLS)** — no architectural objection; an additional service on the existing deployment substrate, not a new topology.
- ✅ **Auth model — OAuth preferred, API key fallback** — consistent with **ADR-070 D3** (the MCP server owns OAuth and tokens). Ratified shape; nothing to re-litigate.
- ✅ **MCP tool catalog** — no objection in principle. **Request: derive the catalog from the registry rather than hand-maintaining a list.** Same move as ADR-072's frontmatter-derive and #1106's MANIFEST-derive; a hand-kept catalog is a stale-list defect waiting to happen, and there are three precedents for the cure.
- ✅ **Colleague model / composted learning via MCP resources vs. tools** — clean split is **resources for reads, tools for writes.** MCP resources are app-controlled context (serving stored profile / colleague model / composted insights is exactly that); tools are model-controlled actions (an `update_*` that mutates server state). The Option-A phrasing "client infers, server writes via an MCP tool call" is already right; make the **read** side a *resource* so serving context doesn't require the model to decide to call something.

> 🔴 **The one real architectural risk in the mechanism set (Arch, 2026-07-29) — carry this into implementation.**
> **The hosted MCP endpoint introduces a new caller-identity surface that ALL existing owner-scoping enforcement sits downstream of.** Every MCP call must resolve to an `owner_id` *before* it touches server state, and that mapping is the single point where the **ADR-079** contract either holds or is silently bypassed. If an MCP tool handler can reach a repository without an owner-scoped identity, **the derived lint (`check_unscoped_reads.py`) will not save us — the read will look owner-scoped while the owner was chosen by the caller.**
> **Rule: fail closed at that boundary — no identity, no read.** Never default to a system or anonymous owner. This matters most on the **API-key fallback**, since a key is a weaker identity than an OAuth subject.
> Note the escalation in problem class: the original #1351 audit asked *"can an anonymous caller see state?"* A multi-tenant hosted server asks *"can caller A see caller B's state?"* — strictly harder, and precisely the class ADR-079 exists to make impossible by construction.

### For PPM / Lead Dev
- #1360 (API key gate for `/api/v1/intent`) and #1351 (MCPB credential) are both likely superseded by this decision — but PM should explicitly confirm closure
- Hosted MCP implementation is a new epic; issue TBD

### For Comms
- "Plugin" has a specific meaning here (Claude plugin = CLAUDE.md + hooks + skills + MCP URL) — distinct from "MCPB" (deprecated), "connector" (an integration within Piper), and "skill" (a procedure file). See glossary. Blog posts will need to be precise.
- The hosted MCP path is a good story for the Piper Alpha narrative: "Piper works inside your existing Claude/ChatGPT."

---

## Success Criteria

- A BYOC Claude Chat user can add the Piper plugin package (or just the CLAUDE.md + MCP URL) and interact with Piper's stored context without any local infrastructure
- A BYOC ChatGPT user can add `mcp.pipermorgan.ai` as a remote MCP and individual skills and get equivalent core capabilities
- Alpha testers confirm: setup is a one-time operation, not a recurring maintenance burden

---

## Open Questions (PM-gated)

> ⚠️ **Q2 is a RATIFICATION BLOCKER, not an item to collect at leisure.** This list otherwise reads as
> questions to answer later, and Q2 was drafted into it as a peer of Q1 and Q3. It is not one.
> Flagged during the 2026-07-26 PA handoff by the PDR's own author — see
> `dev/active/handoff-pa-predecessor-2026-07-26.md`.

1. ✅ **RESOLVED 2026-07-19.** **#1360 and #1351 closure**: These were MCPB-specific security issues. May PM explicitly confirm these can be closed as superseded by PDR-006? — *PM confirmed; both closed as superseded. **Carry-forward on #1351 is an INCOMPLETE AUDIT, not a design note** — the anonymous-caller state-isolation audit was started and left unfinished. `ConversationDB` persistence is verified safe; **Redis, in-process floor/context state, and rate-limiting under anonymous-caller conditions were never traced.** Arch must verify the hosted MCP endpoint does not inherit this class of issue **before it goes live**.*

2. ✅ **RESOLVED 2026-07-29 (Arch). Colleague model build vs. serve** — *was:* does building/updating the colleague model require server-side LLM inference, or is it a pure database write from client-observable signals?
   **Answer: Option A — rule-based, already shipped. PM ruled it 2026-01-08**; the LLM evolution is tracked as **#558** (OPEN, Production/1.0, due 2026-10-30). Evidence: no LLM client anywhere in `services/mux/`; `composting_pipeline.py` is deterministic aggregation (`_calculate_confidence`, `_calculate_surprisingness`, `_extract_topic_tags`, `_determine_trust_stage`), not synthesis. There is **no "colleague model" subsystem** — every `colleague` occurrence in `services/`+`web/` is persona register. The de-facto model is `preference_detection.py` (4 dimensions × 5 detection methods), `preference_extractor.py`, `user_preference_manager.py`, `personality_profile.py` — zero LLM references across all four.
   **The A/B framing was never a live choice**: A is built, B is filed and scheduled. The caveat that it was pattern-matched from PDR-005 was correct, and the real shape is sharper than "neither" — *the decision had already been made and nobody had it in view.*
   ➡️ **The question worth asking in its place — genuinely open, and PM's, not Arch's**: *at what point does the gap between a 4-dimension rule-based preference model and a real colleague model start costing us users?* That's product quality, not architecture. **It must not gate this PDR.** Rule-based over five signal types is a legitimate v1; it is also visibly shallow next to the words "colleague model," and **alpha feedback should decide when #558 gets pulled forward.**
   ~~(b) coupling to the spatial review~~ — **WITHDRAWN as a gate by Arch, 2026-07-29**, who raised it. It assumed the colleague model was an architectural surface under active design; it's an existing rule-based store with a scheduled upgrade. The spatial question concerns the cold per-connector adapter layer; this is server-side user state the ADR-070 consumer path serves regardless. **They share a metaphor, not a mechanism.** ⏳ **Re-trigger condition — VERIFIED AGAINST CODE 2026-07-29 (PA), and it is CLOSER than "watch for this."** If #558 is pulled forward and the colleague model becomes an *inference* surface rather than a store, the coupling returns — it would draw on the same context-assembly machinery the spatial layer owns. Worth a line in the spatial synthesis.
   **Current state, checked not assumed** (prompted by Arch's 7/29 correction that layer 2 is *not* cold — `github_spatial` is live):
   - ✅ **Coupling is DORMANT and the withdrawal stands**: `services/intent_service/context_assembler.py` has **zero** `preference` / `personality` / `user_preference` references. The de-facto colleague model is **not in the context-assembly path at all.** The re-trigger has not fired, so **PDR-006 ratification is unaffected.**
   - ⚠️ **But there is no wiring left to build.** `context_assembler` → `github_integration_router` is live (4 deferred, function-level call sites: :1210, :1296, :1417, :1553), and the router imports `GitHubSpatialIntelligence` **top-level** (:30) and instantiates it **unconditionally** (:117, outside the `use_mcp` guard). So the machinery is already carrying a live 8-dimensional adapter. **If #558 lands, the coupling arrives immediately — it is one issue away, not one project away.**
   ⚠️ **Do NOT read the live MCP path as precedent for this PDR.** The router's *primary* is `GitHubMCPSpatialAdapter` (`services/mcp/consumer/`, `USE_MCP_GITHUB` default true, CORE-MCP-MIGRATION #198) with `GitHubSpatialIntelligence` as documented fallback — but `services/mcp/consumer/` is Piper as an MCP **client**, calling out. **This PDR's `mcp.pipermorgan.ai` is Piper as an MCP *server*, being called in. Opposite directions.** A live consumer adapter de-risks *nothing* on the server side, where this PDR's actual risk lives (see the caller-identity block under "For Arch"). Same conflation class as Connector-vs-Plugin; flagged before it propagates.

3. **Plugin directory applications**: PM mentioned both Claude and GPT have directories to apply to. Is this a "begin drafting applications now" direction, or wait until the plugin package and beta are more stable? — *PM directed: begin research now. Research delivered 7/19; ⚠️ **its Team/Enterprise gating claim is since withdrawn as unreliable** — see the correction banner on `mailboxes/pa/sent/2026-07-19-pa-to-exec-cc-pm-plugin-directory-research.md`.*

---

## References

- PDR-005: Bring Your Own Chat — Distribution Model (ratified Jun 5, 2026)
- ADR-054: InsightJournal / Composted Learning
- #1351: MCPB credential (likely superseded)
- #1360: Intent API key gate for MCPB (likely superseded)
- #1382: Encrypted API key store (future; relevant to M4 server-side LLM option)
- Architecture diagram (PA, Jul 18 2026): https://claude.ai/code/artifact/a146134e-2858-4c7c-a916-8f1b038fc8c6

---

## Changelog

| Version | Date | Author | Notes |
|---|---|---|---|
| v0.1 | 2026-07-19 | PA | Initial draft — captures PM's Jul 18 direction; pending PM + Arch review before ratification |
| v0.2 | 2026-07-19 | PA | PM approved direction; routing to Arch / CXO / PPM for review and comments |
