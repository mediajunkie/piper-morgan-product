# PDR-006: Hosted MCP Endpoint + Plugin Distribution Model

**Status**: ✅ **RATIFIED — PM, 2026-07-31.**

> **PM, verbatim, in conversation with Exec, 2026-07-31 ~11:00 PT: *"And yes I do ratify PDR 006."***

**Evidence trail** (per the in-conversation-relay norm — PM decisions made in chat are recorded durably, not left there): relayed by Exec to Arch + PA, `memo-exec-RELAY-to-arch-pa-...-PDR-006-RATIFIED-by-pm-in-conversation-2026-07-31.md`; formal record made by Arch per Exec's ask. Reviews that gated it: **Arch ✅ 7/29** (Q2 resolved against running code), **CXO ✅ 7/30**, **PPM ✅ 7/30** — all three RATIFY, no objections. PM approved the *direction* 2026-07-19; this ratifies the decision.
### ⚠️ What ratification makes LIVE — the Architect conditions from the 7/29 review

Ratifying the decision does **not** discharge the architectural conditions attached to it. These now bind the implementation epic rather than the document, and are recorded here so the builder inherits them without re-reading a memo:

1. 🔴 **The MCP caller-identity boundary must be FAIL-CLOSED.** This is the one real architectural risk in the mechanism set. **Every MCP call must resolve to an `owner_id` before touching server state — no identity, no read, never defaulting to a system or anonymous owner.** The reason it is load-bearing: **all existing ADR-079 owner-scoping enforcement sits DOWNSTREAM of this mapping.** If a tool handler can reach a repository with a caller-chosen identity, the derived `check_unscoped_reads` lint cannot save us — the read *looks* correctly owner-scoped while the **owner** is the forged thing. A multi-tenant server is a strictly harder problem than the anonymous-caller one #1351 was scoped to.
2. **Derive the tool catalog from the registry**; do not hand-maintain it. Precedents: ADR-072's frontmatter-derive, #1106's MANIFEST-derive, ADR-070 Amendment A's single `resolve_server_ref()` authority. A hand-kept catalog is a stale-list defect waiting to happen and we have three cures on the shelf.
   - 🔴 **DERIVATION RULE, added 2026-08-04 (PA measured; Arch verified and widened). Derive keyed by ENTRY IDENTITY, deduped across aliases — one tool per `WorkflowEntry`, one canonical name. Aliases are input-side vocabulary and must never leak into the tool list.** The registry is keyed by *alias*: **103 distinct alias keys → 38 distinct entries, ≈2.7 names per operation** (`create_issue` alone has 6; `changes_query` has 4). **Derived naively, condition 2 as originally written ships 103 tools for 38 operations, including six ways to file the same issue.**
     - **Why it isn't cosmetic, and this is PA's insight**: the aliases are *classifier* surface — natural-language phrasings folded onto one handler, which is right for input. **A host LLM's tool list is not a classifier surface.** Handing a model four synonymous tools makes routing *worse*: it must disambiguate names carrying no real distinction, and picks arbitrarily. **The property that makes the alias set good input makes it bad catalog.**
     - ⚠️ **Measurement note for whoever implements this**: the registry is assembled by **five** writers — one literal dict *plus* three `*_COHORT` dicts *plus* two local `(entry, aliases)` lists (`_query_cohort`, `_final_ifheads`). PA measured the literal dict (31→12); the other four writers hold the rest. **Any derivation or audit that reads only the literal dict covers under a third of the registry and will look complete.** Count at runtime from the assembled dict, not from any single literal.
   - ✅ **Clarified 2026-08-04 (PA asked): a required, DEFAULTLESS field on `WorkflowEntry` satisfies this.** The fact then lives in the registry and the catalog is *computed* — exactly the derive shape. **The defaultless part is load-bearing, not a style choice**: four of `WorkflowEntry`'s five fields are already defaulted, and a defaulted mutation-semantics field would let every future entry silently inherit a value nobody chose — hand-maintenance wearing derivation's clothes, since the catalog would then derive from an unstated assumption. The resulting break at all ~15 construction sites **is the feature**: each site is forced to state the fact. PA's own finding is the argument — they predicted `prioritization` was a bulk-write sleeper, read it, and it writes nothing. **A default is that same guess, applied unattended to every entry added later.**
3. **Colleague-model access splits resources-for-reads / tools-for-writes.** MCP resources are app-controlled context (serving stored profile, colleague model, composted insights is exactly that); a mutating `update_*` is model-controlled and belongs as a tool. Option A's "client infers, server writes via an MCP tool call" is already the right write shape; the *read* side should be a resource so serving context does not require the model to decide to call something.
   - ⚠️ **SCOPE, added 2026-08-04 because three readers independently over-extended this condition and the fault is the condition's, not theirs.** This condition governs **colleague-model context serving** — stored profile, colleague model, composted insights — **and nothing else. It does NOT reach the workflow registry**, and it does **not** move `changes_query`, `generate_content`, `prioritization`, or the other read entries out of the tool catalog.
   - **The discriminator is in the condition's own tail — *"so serving context does not require the model to decide to call something."*** That describes context you want served **unprompted**: stable, addressable, host-anticipatable. It does **not** describe an operation whose parameters the model must formulate. `changes_query` takes a query; `prioritization` scores caller-supplied input, so **there is nothing to address until the model supplies it** — it could not be a resource under any reading.
   - ⭐ **Therefore `readOnly` ≠ `resource`. They are orthogonal axes**: *resource vs tool* asks **addressable host-anticipatable context, or invoked operation?**; *`readOnlyHint`* asks **does invoking it mutate state?** A read-only **operation** is a **tool with `readOnlyHint: true`**, and that is correct, not a compromise.
   - Single honest edge: **`get_default_repo`** genuinely is a stable addressable user fact and is a legitimate *future* resource candidate — but it belongs to the colleague-model context bundle, not the registry spec. **Not now; it gates nothing.**

⚠️ **And a conflation guard adopted from PA (7/30), recorded because the wrong inference is available and tempting**: `services/mcp/consumer/` is Piper as an MCP **client**; `mcp.pipermorgan.ai` is Piper as an MCP **server**. Opposite directions. **A live consumer family precedents NOTHING about the server side** — nobody should cite CORE-MCP-MIGRATION #198 as de-risking this PDR, because the server-side risk is condition 1 above.

⚠️ **Ratified ≠ shippable** — two pre-user gates remain open (see that section): [#1458](https://github.com/mediajunkie/piper-morgan-product/issues/1458) cross-caller state isolation, and the recomposition rubric branch.
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

> ⚠️ **READ THIS FIRST — the conflation most likely to recur in this document's vicinity.**
> *(Promoted here from a Q2 footnote at CXO's request, 2026-07-30 — "the clearest thing in the document,
> and it reads as an aside where it sits.")*
> **`services/mcp/consumer/` is Piper as an MCP *CLIENT*, calling out to external MCP servers.
> `mcp.pipermorgan.ai` is Piper as an MCP *SERVER*, being called in by Claude and ChatGPT. Opposite
> directions.** A live consumer family (CORE-MCP-MIGRATION #198, `USE_MCP_GITHUB` default true)
> **de-risks nothing on the server side**, which is where this PDR's actual risk lives — see the
> caller-identity block under "For Arch." **Nobody may cite #198 as evidence this phase is precedented.**

> 🔴 **Capability legibility is bounded by the MCP protocol — verified against the spec, 2026-07-30.**
> CXO asked (explicitly "genuinely asking, not asserting") whether the hosted server can learn the
> caller's actual installed skill/tool set, so Piper can say *"I can do X here; Y needs the &lt;name&gt;
> skill added."* **Answer: no, not at skill granularity.**
> Per the [MCP lifecycle spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle),
> `initialize` gives the server exactly three things: `protocolVersion`; `capabilities` — **protocol
> features only** (`roots`, `sampling`, `elicitation`, `experimental`); and `clientInfo`
> (`name`, `title`, `version`). **There is no field carrying the host's installed skills or plugins.**
> Skills are a host-side concept; MCP has no notion of them.
> ✅ **What IS available, and it's a usable partial mitigation**: `clientInfo.name` tells the server
> **which surface it's on** — ChatGPT vs Claude vs Claude Code. So Piper can calibrate capability claims
> **per surface**, which is coarser than per-user inventory but is not nothing, and it supports CXO's
> honesty pattern at surface granularity. `experimental` could in principle carry a custom field, but
> nothing standard exists and **we must not design against it.**
> **Consequence for the ChatGPT lane**: because ChatGPT users assemble a partial, self-selected skill
> set and the server cannot see it, Piper **will** at times offer or attempt something not installed, or
> fail to offer something that is. Design for graceful degradation and surface-level honesty rather than
> per-user precision. Recorded here rather than discovered at integration.

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

### For CXO — ✅ reviewed 2026-07-30: **RATIFY, no objections.** Three design implications, all CXO-owned work
- Plugin package UX needs design: what does a user's first experience of the Piper plugin look like? Onboarding flow for connecting MCP + adding skills. ChatGPT manual-add flow is notably more friction than Claude's (each skill added separately).

> 🔴 **1. This model REMOVES the surface where we would have demonstrated differentiation — and that silently invalidates the fix all three Jake FTUX lenses converged on.**
> Jake's verdict was *"just an LLM with extra UI."* CXO, HOST and PA independently converged on the same
> answer: **the first run must reflect the user's own data back at them** — a cold-start-*state* problem,
> not a positioning problem. *An empty list is a form; a populated queue is a colleague.*
> **Under this PDR there is no first screen.** The user is inside Claude or ChatGPT; we own neither the
> surface, the conversation, nor the moment of arrival.
> ✅ *The good news, and it's substantial*: most of Jake's UI complaints are **deleted outright** — the
> avatar-pill nav, the undersized panel, the verbose search placeholder, the non-growing composer, the
> three-list taxonomy confusion. None of them exist in a plugin.
> ⚠️ *But the load-bearing complaint gets harder*: **"is this just an LLM with extra UI?" becomes
> literally true by design** — it *is* their LLM plus our tools. **Every gram of differentiation now has
> to be carried by what the tools return.** There is no UI left to carry any of it.
> ➡️ **So the cold-start fix is re-expressed, not dropped**: the **first tool call after connection must
> return something specific and true about the user's actual work** — not a capability list, not a
> greeting. If Piper's first utterance in their chat is generic, we have reproduced Jake's exact
> experience in a surface with *fewer* affordances to recover with. CXO is biasing the plugin's
> `CLAUDE.md` toward a connector-grounded observation rather than a menu.

> **2. ChatGPT's per-skill add is a capability-legibility gap, not just friction.** The user assembles a
> partial, self-selected capability set and Piper cannot see which parts they installed — structurally
> reproducing the class that bit Jake incidentally (he asked Piper to *file a ticket*; Piper *did the
> feature* — the capability wasn't legible before it fired). **HOST's consent gate does not cover this**,
> because it isn't consent to an action; it's a mismatch between the capability set Piper believes it has
> and the one actually present. **Protocol answer and the available mitigation: see the boxed note in
> Capability Split** — the server gets `clientInfo.name` (surface) but never the installed skill set.

> **3. On the Q2 successor question — Jake gives no signal, and the absence is itself the finding.**
> He never reached the colleague model; he bounced at FTUX. **"Our first alpha tester didn't complain
> about the colleague model" reads as reassurance and isn't. The 4-dimension model didn't cost us Jake —
> the FTUX did.**
> **And the better read argues AGAINST pulling #558 forward on this evidence**: `preference_detection.py`
> measures **style** axes (warmth, confidence, action-orientation, technical depth) — *how Piper talks to
> you*. Jake's complaint was *"it wasn't pulling productivity out of me… asking me to choose the problem
> I already have"* — **he didn't want Piper to match his tone, he wanted Piper to know his context.**
> So the gap he hit is **not that the preference model is shallow; it's that it measures the wrong axis
> for the complaint we received.** Pulling #558 forward would buy a better-calibrated *voice* in a
> session where he never got far enough to notice the voice.
> ➡️ **The trigger to watch is NOT "users say Piper's tone is off" — it's "users say Piper doesn't know
> what I'm working on,"** which is a *different subsystem*: connector-derived work context, which this
> PDR already places server-side. Pull #558 on complaints of the second kind and we spend a
> Production-milestone issue without moving the number.
> ⚠️ **Naming problem with a product cost**: *"colleague model"* sets an expectation a 4-dimension style
> model cannot meet. **Cheaper to fix the phrase than the model — don't use it user-facing until it
> means what it says.**

⚠️ **Ratification does NOT clear Q1's carry-forward** (CXO's flag): the unfinished anonymous-caller
state-isolation audit — Redis, in-process floor/context state, rate-limiting, none traced — is a
**pre-live gate, tracked as [#1458](https://github.com/mediajunkie/piper-morgan-product/issues/1458)**.

---

## ⛔ Pre-user gates — ratified ≠ shippable

**Two things must close before this surface reaches users. Neither blocks ratification; both block release.**

**1. [#1458](https://github.com/mediajunkie/piper-morgan-product/issues/1458) — cross-caller state isolation.** Redis, in-process floor/context state, and rate-limiting under anonymous callers were never traced. Blocks multi-tenant serving. *(Arch, 7/29.)*

**2. 🔴 No fitting verification rubric exists for this surface — and the gap it exposes is untested honesty.** ✅ **Now tracked as [#1463](https://github.com/mediajunkie/piper-morgan-product/issues/1463)** *(filed by PA 2026-08-01 as a tracking artifact — CXO confirmed "Branch: opening it" on 7/30 and PPM asked who would file it; that question went unanswered while both were occupied with ratification and the credential blocker. **Design remains CXO's and is not pre-empted.** Filed because PPM's warning was right: "a gate that isn't an issue isn't tracked" — and it left the two pre-user gates asymmetric, one with a number and one in prose.)* *(CXO, 7/30, via DoD Layer B, which is explicit that **"naming the absence of a fitting rubric is itself a Layer-B finding"** and that R/C/T must **not** be silently re-used with shifted meanings.)*

PDR-006 creates a surface type none of our instruments covers: **Piper's response as MCP tool output inside someone else's chat client**, where we own neither the conversation nor the LLM that frames our words.

- **Colleague Test rubric (R/C/T)** — built for response text *Piper composes*. Here the client LLM composes what the user reads. **We are no longer scoring what the user sees**; tone in particular becomes the client's.
- **UI Lifecycle rubric** — inapplicable; we render no UI.

Proposed branch dimensions (CXO's, pending a CXO branch decision + PPM/PM on tier): **sufficiency** (does our output carry enough for the client LLM to answer well?), **honesty-under-recomposition**, **capability truthfulness** (see the MCP legibility box above).

> ⚠️ **The middle one is the sharp one, and it sharpens this PDR's own differentiation argument.**
> Our honest-decline discipline — what Scenario C's 3/3 actually tested — is a property of **text we
> control.** Hand a hedged tool response to someone else's LLM and **the hedge may not survive into what
> the user reads. We have never tested whether our honesty survives recomposition, and this PDR makes
> that the default path.**
> This also raises the bar on CXO's implication 1 above. It is not enough that *"every gram of
> differentiation is carried by what the tools return"* — **the tools' output must survive
> recomposition by a model we do not control.** Differentiation and honesty both now have to pass
> through a paraphrase step we don't own.
> ✅ **Testable NOW — this gate does not depend on the build.** It needs a hedged/qualified text blob and
> a client LLM, not `mcp.pipermorgan.ai`. So it can close during Phase 0 rather than waiting on Phase 2,
> and it should — a negative result would change what the tool layer has to emit, which is cheaper to
> learn before the tools are written. *(Rubric design is CXO's lane; PA is flagging the sequencing, not
> claiming the work.)*

### For Arch — ✅ reviewed 2026-07-29; mechanism set holds, with one named risk

- ✅ **`mcp.pipermorgan.ai` on Fly.io (DNS/TLS)** — no architectural objection; an additional service on the existing deployment substrate, not a new topology.
  > 🔴 **SEQUENCING CONSTRAINT added 2026-07-31, and it belongs here rather than only in Open Question 3.** MCP connector directory submission requires **domain-ownership verification of the domain hosting the MCP server** (PA, from OpenAI's submission docs). **You cannot verify ownership of a domain that does not resolve.**
  >
  > **Therefore this DNS/TLS/Fly work is UPSTREAM of any directory-listing timeline** — a listing cannot be pursued, fast-tracked, or run in parallel ahead of it. Anyone planning listing work should treat the subdomain's deployment as a hard predecessor, not a concurrent track.
  >
  > *(Recorded in the **For Arch** section deliberately: the prerequisite was correctly captured in OQ3, but whoever does the DNS/TLS work reads this section, and a dependency that only exists in a different section of the same document is a dependency waiting to be discovered late — the same argument that put the three conditions above into the PDR rather than leaving them in a review memo.)*
- ✅ **Auth model — OAuth preferred, API key fallback** — consistent with **ADR-070 D3** (the MCP server owns OAuth and tokens). Ratified shape; nothing to re-litigate.
- ✅ **MCP tool catalog** — no objection in principle. **Request: derive the catalog from the registry rather than hand-maintaining a list.** Same move as ADR-072's frontmatter-derive and #1106's MANIFEST-derive; a hand-kept catalog is a stale-list defect waiting to happen, and there are three precedents for the cure.
- ✅ **Colleague model / composted learning via MCP resources vs. tools** — clean split is **resources for reads, tools for writes.** MCP resources are app-controlled context (serving stored profile / colleague model / composted insights is exactly that); tools are model-controlled actions (an `update_*` that mutates server state). The Option-A phrasing "client infers, server writes via an MCP tool call" is already right; make the **read** side a *resource* so serving context doesn't require the model to decide to call something.

> 🔴 **The one real architectural risk in the mechanism set (Arch, 2026-07-29) — carry this into implementation.**
> **The hosted MCP endpoint introduces a new caller-identity surface that ALL existing owner-scoping enforcement sits downstream of.** Every MCP call must resolve to an `owner_id` *before* it touches server state, and that mapping is the single point where the **ADR-079** contract either holds or is silently bypassed. If an MCP tool handler can reach a repository without an owner-scoped identity, **the derived lint (`check_unscoped_reads.py`) will not save us — the read will look owner-scoped while the owner was chosen by the caller.**
> **Rule: fail closed at that boundary — no identity, no read.** Never default to a system or anonymous owner. This matters most on the **API-key fallback**, since a key is a weaker identity than an OAuth subject.
> Note the escalation in problem class: the original #1351 audit asked *"can an anonymous caller see state?"* A multi-tenant hosted server asks *"can caller A see caller B's state?"* — strictly harder, and precisely the class ADR-079 exists to make impossible by construction.

### For PPM / Lead Dev
- ✅ #1360 and #1351 — closed as superseded, PM-confirmed 2026-07-19. *(#1351's unfinished audit survives as pre-live gate [#1458](https://github.com/mediajunkie/piper-morgan-product/issues/1458) — see Pre-user gates.)*
- Hosted MCP implementation is a new epic; issue TBD
- ⏳ **PPM's PDR-006 review is the only one outstanding** (Arch ✅ 7/29, CXO ✅ 7/30). PPM confirms the sprint/roadmap slice is still owed, 7/30.

> 🔴 **The MCP tool catalog is now a PRODUCT surface, not just a compliance artifact** *(PPM, 7/30, answering the entry-point question CXO routed to them).*
> Under this PDR, **tool names, descriptions, and parameters are the only entry-point copy a plugin user ever sees** — and they are read by **both the human and the host LLM deciding what to call.** So the fix for Jake's "which of three lists?" complaint relocates from navigation to the catalog:
> - ❌ **Not** tools named for our object model, leaving user and client LLM to map a situation onto our taxonomy.
> - ✅ **Instead** tools named and described by **the situation they serve** — *"shape a vague idea into a spec"*, *"break an epic into tickets"*, *"draft acceptance criteria for issues that lack them"* — routing to the same structures behind the scenes.
>
> **This is where opinionation lives now.** Jake's "lack of opinionation" complaint has no UI left to answer it; the catalog is the answer, and it's a third the cost of the nav redesign it replaces.
> ⚠️ **PPM's own counter-risk, recorded because it cuts against their recommendation**: the catalog is read by the host LLM as much as the human, and **situation-shaped names may route WORSE than object-shaped ones** if tool-selection does better with crisp nouns than scenarios. **Nobody knows which way this goes.** Test selection accuracy on both namings before committing — see Pre-user gates, where this shares a rig with the recomposition probe.

> **Sort the Jake fix list against this pivot before it becomes work** *(PPM, 7/30)* — the default of working it in severity order spends beta capacity on a surface being retired:
> **A. Dies with the pivot** (nav-in-avatar-pill, panel width, search placeholder, non-growing composer, three-list *navigation*) — **not beta work.** Carve-out: the two items that actually changed Jake's behavior — the unfindable "blocked" card and the missing chat row — are worth fixing on **welfare grounds** while real testers remain on the web UI. Panel width is not.
> **B. Survives but relocates** (taxonomy → tool catalog · capability legibility → tool descriptions · progressive elicitation → a conversation the plugin drives) — **re-specify before building, or build twice.**
> **C. Gets harder and becomes the entire game** (cold-start population, reflect-and-elaborate, consent gate) — **this is the beta.**
>
> ⚠️ **And the beta gate cannot currently fail for the thing Jake reported.** #1386's criteria are the canonical suite + multi-turn scenarios + sign-off — **Jake's session would pass all of them while producing his exact outcome.** The gate measures whether Piper answers *correctly*; the risk is a competent user getting correct behavior throughout and concluding we're an LLM wrapper. PPM's recommendation: **do not expand #1386** (close it on existing terms), **add one binary beta criterion — from a cold account with one connector, does the user's own data appear in the first exchange, unprompted?** — and treat HOST's consent gate as a genuine release blocker.

### For Comms
- "Plugin" has a specific meaning here (Claude plugin = CLAUDE.md + hooks + skills + MCP URL) — distinct from "MCPB" (deprecated), "connector" (an integration within Piper), and "skill" (a procedure file). See glossary. Blog posts will need to be precise.
- The hosted MCP path is a good story for the Piper Alpha narrative: "Piper works inside your existing Claude/ChatGPT."

---

## Success Criteria

> 🔴 **The three original criteria below are all SETUP criteria, and none of them can fail for the outcome this PDR most fears.** *(PPM, 7/30.)* Every one passes if a user installs cleanly, calls a tool, gets a correct answer, and concludes we're a wrapper around their own LLM — **which is exactly Jake's session, and exactly the outcome CXO's implication 1 says this model makes *harder* to avoid.**
> **This is a distinct instrument with the same defect as #1386's gate** (which measures *answer correctness* where these measure *setup success*) — which is what makes it worth naming as a class rather than a repetition: **methodology-44 at the product level — the criteria emit a pass identically whether we delivered value or merely avoided errors.**

- **✅ DEMONSTRATION (added 2026-07-30; the only criterion that fails today).** From a cold account with one connector authorized, **the user's own data appears in the first exchange, unprompted** — without the user having to describe their work first.
  *Deliberately worded identically to the beta-gate criterion PPM proposed for #1386: **the cold-start demonstration is now the single load-bearing product claim on both surfaces**, and one wording in two places is cheaper than discovering later that they drifted. If PM wants it in only one place, put it here — this PDR outlives #1386.*
- A BYOC Claude Chat user can add the Piper plugin package (or just the CLAUDE.md + MCP URL) and interact with Piper's stored context without any local infrastructure *(setup)*
- ⚠️ **UNDER ACTIVE QUESTION (2026-08-02) — do not read as settled.** ~~A BYOC ChatGPT user can add `mcp.pipermorgan.ai` as a remote MCP and individual skills and get equivalent core capabilities~~
  > **PA's N=6 probe found honest-decline survives the ChatGPT lane ~50% of the time vs 100% on Claude** (structured fields tripled survival 17%→50% but do **not** rescue a refusal). **Honest-decline is a core capability** — Scenario C, a scored Colleague Test dimension, and a HOST-owned trust property — so *"equivalent core capabilities"* is **currently false as written**.
  > **Deliberately NOT amended.** PPM holds the wording proposal pending one untested mechanism (emit a consequential refusal as a **protocol-level MCP tool error** rather than as content the client can paraphrase away). **A criterion rewritten on a partial result is how a ratified doc drifts.** Tracked as an acceptance criterion on **#1462**; PPM brings PM a wording proposal once the probe result — or a decision not to run it — is in.
  > *Marked rather than left silent per ADR-038 Amendment A §A3: "don't amend yet" and "leave unmarked" are different decisions, and a ratified criterion known to be false is exactly what a durable document must not assert without a flag. Precedent: CXO's review-in-flight notices on ADR-013/038.* *(setup)*
- Alpha testers confirm: setup is a one-time operation, not a recurring maintenance burden *(setup)*

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
   ✅ **ANSWERED 2026-07-30 (PPM, to whom Q2 routed it): do NOT pull #558 forward yet.** Verified live first: #558 OPEN/Production, #1458 OPEN. The reasoning's second step is the one that matters — **the absence of alpha signal is itself the answer, not a missing datum.** *You cannot get colleague-model feedback from users who bounce at first contact*: the rule-based model's shallowness is **invisible to a user who never gets far enough to feel it.** So **#558's pull-forward is gated behind fixing cold-start** — until first contact demonstrates something, every alpha session terminates *upstream* of the surface #558 improves, and we'd be deepening a model nobody has reached. Sequencing: cold-start demonstration → users stay past first contact → the gap becomes observable → *then* #558's timing is a real question with evidence. Pulling it forward now spends Production capacity on **depth** when the binding constraint is **contact**.
   ⚠️ **PPM is explicit this is a sequencing call, NOT a claim the coupling is safely distant**: if PM overrides and pulls #558 forward, **the spatial coupling returns immediately** — it is one issue away with the wiring already live. The spatial synthesis needs that line.
   ➡️ **The question worth asking in its place — genuinely open, and PM's, not Arch's**: *at what point does the gap between a 4-dimension rule-based preference model and a real colleague model start costing us users?* That's product quality, not architecture. **It must not gate this PDR.** Rule-based over five signal types is a legitimate v1; it is also visibly shallow next to the words "colleague model," and **alpha feedback should decide when #558 gets pulled forward.**
   ~~(b) coupling to the spatial review~~ — **WITHDRAWN as a gate by Arch, 2026-07-29**, who raised it. It assumed the colleague model was an architectural surface under active design; it's an existing rule-based store with a scheduled upgrade. The spatial question concerns the cold per-connector adapter layer; this is server-side user state the ADR-070 consumer path serves regardless. **They share a metaphor, not a mechanism.** ⏳ **Re-trigger condition — VERIFIED AGAINST CODE 2026-07-29 (PA), and it is CLOSER than "watch for this."** If #558 is pulled forward and the colleague model becomes an *inference* surface rather than a store, the coupling returns — it would draw on the same context-assembly machinery the spatial layer owns. Worth a line in the spatial synthesis.
   **Current state, checked not assumed** (prompted by Arch's 7/29 correction that layer 2 is *not* cold — `github_spatial` is live):
   - ✅ **Coupling is DORMANT and the withdrawal stands**: `services/intent_service/context_assembler.py` has **zero** `preference` / `personality` / `user_preference` references. The de-facto colleague model is **not in the context-assembly path at all.** The re-trigger has not fired, so **PDR-006 ratification is unaffected.**
   - ⚠️ **But there is no wiring left to build.** `context_assembler` → `github_integration_router` is live (4 deferred, function-level call sites: :1210, :1296, :1417, :1553), and the router imports `GitHubSpatialIntelligence` **top-level** (:30) and instantiates it **unconditionally** (:117, outside the `use_mcp` guard). So the machinery is already carrying a live 8-dimensional adapter. **If #558 lands, the coupling arrives immediately — it is one issue away, not one project away.**
   ⚠️ **Do NOT read the live MCP path as precedent for this PDR.** The router's *primary* is `GitHubMCPSpatialAdapter` (`services/mcp/consumer/`, `USE_MCP_GITHUB` default true, CORE-MCP-MIGRATION #198) with `GitHubSpatialIntelligence` as documented fallback — but `services/mcp/consumer/` is Piper as an MCP **client**, calling out. **This PDR's `mcp.pipermorgan.ai` is Piper as an MCP *server*, being called in. Opposite directions.** A live consumer adapter de-risks *nothing* on the server side, where this PDR's actual risk lives (see the caller-identity block under "For Arch"). Same conflation class as Connector-vs-Plugin; flagged before it propagates.

3. **Plugin directory applications**: PM mentioned both Claude and GPT have directories to apply to. Is this a "begin drafting applications now" direction, or wait until the plugin package and beta are more stable? — *PM directed: begin research now. Research delivered 7/19; ⚠️ **its Team/Enterprise gating claim is since withdrawn as unreliable** — see the correction banner on `mailboxes/pa/sent/2026-07-19-pa-to-exec-cc-pm-plugin-directory-research.md`.*

   > ✅ **RESOLVED 2026-07-31 — the OpenAI-verification question three roles reasoned around in one afternoon.** *(Recorded here rather than in a memo at PPM's request: "that's the shape of a fact that belongs in the document.")*
   >
   > **There are TWO different OpenAI verifications and we were chasing the wrong one.**
   >
   > | | What it is | Relevant to us? |
   > |---|---|---|
   > | **API organization verification** (`platform.openai.com` → Settings → Organization → General) | Unlocks access to advanced API **models/features**. **One org per ID per 90 days.** | ❌ **No.** Not on the ratified path, not required for a directory listing. |
   > | **Verified developer / business identity** ([submission docs](https://developers.openai.com/plugins/deploy/submission)) | What directory submission actually requires. **Explicitly distinct from API org verification.** Must live in the **same organization AND project** you submit from. | ✅ Yes — *if and when* a listing is pursued. |
   >
   > 🔴 **Additional prerequisite nobody had recorded**: MCP connector submissions require **domain-ownership verification for the domain hosting the MCP server** — i.e. `mcp.pipermorgan.ai`, which is **not yet deployed**. That is a real dependency on infrastructure that doesn't exist, and it belongs in the Phase-2 checklist.
   >
   > **What this means for the ratified path: nothing.** §Decision item 3 is *"BYOC ChatGPT user adds the MCP and each skill manually"* — **the user is OpenAI's customer; we are a URL they paste in.** No organization of ours is in that path. The GPT directory appears only at *"a second discovery channel"* (a rationale bullet, the PDR's own word "second"), attached to this still-open question.
   >
   > ⚠️ **Provenance, because the error is instructive**: PA pushed API org verification for **twelve days** as *"the only item with an external clock,"* then on 7/31 corrected only the **ordering** (pick the org first, because of the 90-day lock) — still without asking whether the item was required at all. **Arch asked the prior question; PPM confirmed it against this ratified text; the answer is that it was the wrong verification entirely.** PPM's formulation: *"The clock was real; the item wasn't ours to be on it for."* **Unresolved sub-question, deliberately not assumed**: whether the developer/business-identity flow carries its own rate limit. The 90-day rule is documented for **API org verification**; do not assume it transfers.

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
