# Spatial Intelligence — Layer Map and Costed Options

**Status**: ⚠️ ~~INPUT to a pending PM decision. Not a decision.~~ **DECIDED AND EXECUTED.** PM ruled 2026-08-15/16 (option (b): keep the live layer, dispose of the cold island — decisions.log 2026-08-15 22:10 + 22:2x PT); **the disposal executed 2026-08-29** (decisions.log ~19:0x PT entry): 10 of the 11 deleted with commit-hash prior-art references per PM's retrievability condition; `mcp/consumer/slack_adapter.py` HELD on new evidence (it is the 2026-07 #1232 connector-contract port, not a superseded predecessor — see the decisions.log entry). Design semantics preserved: `docs/internal/architecture/design-records/spatial-cold-island-per-connector-place-modeling.md`. This map remains the review record; its cold-island rows now describe deleted prior art.
**Author**: Chief Architect (arch) · **Date**: 2026-07-30
**Companion**: `spatial-intelligence-experience-thesis.md` (CXO, the experience slice). PPM's roadmap-dependency slice was **delivered 2026-07-30** and is incorporated at §"PPM's roadmap slice" below — *(header corrected by PPM 2026-08-08; it had read "pending" for nine days while the delivered slice sat in this same document, and that stale line was read back as a live blocker)*.
**Supersedes**: every prior characterization of this subsystem by me, including my 7/19 two-layer finding and both of my 7/29 corrections. **Nothing in this review may ratify on those.**

---

## Method — and why the method is the point

This map is built **from the filesystem and the import graph**, via `scripts/reachability-map.py`, not from a list of module names.

That is a deliberate correction to how I produced the three previous versions. **I characterized this subsystem three times in ten hours and was wrong twice**, each time because I enumerated modules from a filename pattern I recalled and then verified only those — `github_spatial.py` sat in the exact directory I was describing and went unchecked through two passes. The failure was never carelessness; it was treating *"I verified the modules I enumerated"* as *"I verified the layer."* (m-43 / m-44.)

> ⚠️ **This document is a SNAPSHOT of measurable facts, and snapshots go stale.** Every live/cold claim below is re-derivable in one command:
> ```
> python3 scripts/reachability-map.py services/integrations/spatial services/intelligence/spatial services/mcp/consumer
> ```
> **If this table and the tool disagree, the tool is right.** (CXO's 2026-07-30 lesson, applied to my own artifact: *"the real cure isn't more care — it's not duplicating measurable facts into a prose document at all. Prose can't be re-run; the tool can."* CXO's thesis doc was corrected twice in two days for exactly this; this doc is the same shape and gets the same warning rather than the assumption that mine is different.)
>
> ⚠️ **A string match on a module name is NOT an import edge.** Both CXO and I independently hit the same false positive within a day — `config_service.py:222`'s feature-flag string `"notion_spatial_mapping"` read as a `notion_spatial` importer. The next person will grep before reaching for the tool; this is the trap.

**Instrument's own scope, stated because a report that can't show its work is indistinguishable from one that never ran:** 566 non-test `.py` files scanned. Static import-following from `main.py` + `web/app.py` reaches only **74 of 566 modules (13%)**, because this app registers routers **by string** (`web/app.py`: `register(app, "web.api.routes.places", …)`) and static traversal cannot cross that. **Therefore: importer counts are the live signal here; absence of a static path means UNKNOWN, never "dead."** Every claim below rests on importer edges, not on the reachability column.

---

## The map — four layers

CXO's 2a/2b split (2026-07-29) is folded in; it is the distinction that makes the whole picture resolve.

| Layer | What it is | State | Who initiates |
|---|---|---|---|
| **L1 — spatial REASONING** | `place_detector`, `spatial_intent_classifier`, `workspace_detection`, `context_assembler`, `spatial_context` | ✅ **LIVE** | user |
| **L2 — the spatial ABSTRACTION** | `services/integrations/spatial_adapter.py` — `SpatialPosition`, `SpatialContext`, `SpatialAdapter` Protocol, `BaseSpatialAdapter` ABC | ✅ **LIVE** — the actual "connectors as places" contract, and what every connector is written against | — |
| **L3 — per-connector ADAPTER DEPTH** | the `*_spatial` + `*_adapter` pairs | ◐ **LIVE for GitHub / Calendar / Notion; COLD for five** | user |
| **L4 — AMBIENT PRESENCE** | a monitoring loop, change detection, salience judgment, interruption ethics | ❌ **NOT BUILT ANYWHERE** | **product** |

**L4 is CXO's contribution and it is the key to PM's question.** L4 is what a user would *experience* as "Piper inhabits my tools." None of its four components exists. **Replicating L3 to five more connectors produces no L4 and changes no user-visible behavior** — L3 makes Piper *fluent about* a tool when asked; L4 would make Piper *present in* it. Those were conflated (by CXO on 7/19, and by me until yesterday).

### L3 in detail — measured, not recalled

**LIVE** (has importers outside the cold island):

| module | importers | live via |
|---|---|---|
| `mcp/consumer/connector` | 11 | `intent_service`, `github_integration_router`, `connectors.disconnect` |
| `mcp/consumer/consumer_core` | 6 | the consumer family |
| `mcp/consumer/github_adapter` | 5 | **`intent_service` directly**, `github_integration_router`, `github_spatial` |
| `mcp/consumer/connector_grant_store` | 3 | `disconnect`, `github_adapter`, `github_oauth_handler` |
| `mcp/consumer/mcp_client` | 2 | `github_adapter`, `google_calendar_adapter` |
| `mcp/consumer/google_calendar_adapter` | 1 | `calendar_integration_router` |
| `mcp/consumer/notion_adapter` | 1 | `integrations/mcp/notion_adapter` |
| `mcp/consumer/github_oauth_handler` | 1 | `web.api.routes.settings_integrations` |
| `integrations/spatial/github_spatial` | 2 | `github_integration_router:30` (**top-level, not deferred**) |

> ### 🔄 RE-DERIVED 2026-08-08 (9 days on) — THE TOOL DISAGREES WITH THIS SECTION, SO THE TOOL WINS
>
> Re-ran the command in the header, per this document's own rule. **Two corrections, and the second is the one that matters for PM's decision.**
>
> **1. The island is ELEVEN modules, not ten — this section UNDERCOUNTED it.** Current derivation: **7 modules with zero importers** (`cicd_spatial`, `devenvironment_spatial`, `gitbook_spatial` ×2 — one in `integrations/`, one in `intelligence/` — `linear_spatial`, `intelligence/spatial/notion_spatial`, `slack_adapter`) **plus 4 adapters reachable only from those** (`cicd_adapter`, `devenvironment_adapter`, `gitbook_adapter`, `linear_adapter`).
>
> **2. 🔴 The sixth cold wrapper is NOTION'S — and this document used Notion as its refutation test.** Below, the cold island is characterised as *"CI/CD, dev-environment, GitBook and Linear — none of them in PM's invite email,"* with **Notion named as the case that could have refuted it**. But Notion has **two** objects and they have opposite status:
>
> | module | importers | status |
> |---|---|---|
> | `services/integrations/mcp/notion_adapter.py` | 2 | **LIVE** |
> | `services/mcp/consumer/notion_adapter.py` | 1 | **LIVE** |
> | `services/intelligence/spatial/notion_spatial.py` | **0** | 🔴 **COLD** |
>
> **So "Notion is live" and "Notion's spatial wrapper is cold" are both true, of different modules.** The L3 row's *"LIVE for GitHub / Calendar / Notion"* is true of the **adapter** and false of the **spatial wrapper** — and the refutation test this document ran was therefore ambiguous. **It does not overturn the recommendation** (the live Notion path is genuinely live), **but PM should not read "Notion is live" as "Notion's spatial layer is out of scope."**
>
> ⚠️ **Same defect this cohort found three times in five days** — one name carrying two objects — **here in my own artifact.** Which is the argument for the header's rule: *don't duplicate measurable facts in prose; re-derive them.*

**COLD — a closed island of 10 modules.** Five `*_spatial` wrappers with **zero** importers, four `*_adapter` modules imported **only** by those cold wrappers, plus `slack_adapter` with zero:

`cicd_spatial` · `devenvironment_spatial` · `linear_spatial` · `integrations/spatial/gitbook_spatial` · `intelligence/spatial/notion_spatial` — all 0 importers
`cicd_adapter` ← only `cicd_spatial` · `devenvironment_adapter` ← only `devenvironment_spatial` · `gitbook_adapter` ← only `gitbook_spatial` · `linear_adapter` ← only `linear_spatial` · `slack_adapter` ← none

*(This is larger than my 7/29 figure of five. The four adapters were missed because I enumerated `*_spatial` by name. The tool found them by walking edges.)*

### `github_spatial` — the nuance that took three passes

**Live-by-construction, secondary-by-dispatch.** `github_integration_router:117` constructs `GitHubSpatialIntelligence()` **outside** the `if self.use_mcp:` guard — unconditionally, on every router init, with `RuntimeError("No GitHub integration available")` if it fails and no MCP adapter exists. But it is the documented **FALLBACK**: `USE_MCP_GITHUB` defaults **true** and `GitHubMCPSpatialAdapter` is `DEFAULT` (CORE-MCP-MIGRATION #198). Both halves are true; neither alone is accurate. (PA's refinement, verified.)

---

## ★ The reframe — the review's question has the polarity backwards

PM's framing was *"invested in, maybe never fully committed, maybe overkill."* The evidence says:

**The cold modules are not abandoned ambition. They are superseded predecessors of a migration that worked.** `github_integration_router` states it: *"CORE-MCP-MIGRATION #198: Try MCP adapter first, fall back to spatial."* The MCP consumer family **replaced** the direct-API spatial implementations **while keeping the spatial contract (L2)**.

So: the theory was not abandoned — **its abstraction is the substrate every connector integration in this codebase is written against.** What died was one *implementation strategy*, killed by a better one on the same contract. And what was never begun is L4, which is the only layer a user would feel.

---

## The three options, costed at the corrected profile

### (a) Commit-and-finish — replicate L3 depth to the five cold connectors
- **Cost: replication, not invention** — a working reference implementation exists. Materially cheaper than the review was originally told. But it is **two tiers per connector** (MCP consumer adapter + direct-API spatial fallback), or one tier if the fallback tier is first ruled obsolete — which the #198 migration suggests it already is.
- **Value: ZERO for the current product — and this is now MEASURED, not judged.** CXO tried to refute its own "nobody is asking about these tools" claim and instead closed its one hole. **Every connector a user can actually connect already has live spatial depth:**

| Advertised alpha connector | Live spatial path | |
|---|---|---|
| **GitHub** | `integrations/spatial/github_spatial` + `mcp/consumer/github_adapter` | ✅ live |
| **Notion** | `mcp/consumer/notion_adapter` (produces `SpatialContext`), live via `notion_integration_router.py:59` | ✅ live |
| **Calendar** | `mcp/consumer/google_calendar_adapter` + `calendar_integration_router` | ✅ live |
| **Slack** | `integrations/slack/spatial_adapter` (the ADR-038 Granular pattern) | ✅ live |

  **The cold island's connectors are CI/CD, dev-environment, GitBook and Linear — none of them in PM's invite email.** Notion was the case that could have refuted this (it's advertised *and* has a cold `notion_spatial`); it doesn't, because what's cold for Notion is the *superseded direct-API predecessor*. So *"tools nobody is asking Piper about"* is now literal rather than rhetorical, and **(a) buys zero user-visible value regardless of how cheap replication proves to be.** Re-checkable the same way the importer edges are.

### (b) Keep L1+L2+live-L3, dispose of the cold island ⭐ *my recommendation, converging with CXO*
- Layers 1 and 2 are not in question — they are load-bearing and live.
- The 10-module cold island becomes **Tier-3-style migration residue**, eligible for the ordinary fix-or-delete treatment **subject to PM's protected-surface rule** — *not* a strategic bet requiring a committed-theory verdict.
- **Cost: small and mechanical.** **Value: removes 10 modules that read as live capability and aren't.**
- ⚠️ **Describe it as "superseded implementation strategy, retained as prior art" — NOT "dead code, removed."** (CXO's caveat, and it's right.) The cold island holds the only worked examples of per-connector place-modeling for four connectors — what someone already thought about what a "place" means in a CI pipeline or a docs tree. If L3 is ever built for Linear or GitBook, that's **design capital**, free to preserve since it lives in git history regardless. **The framing matters so a future reader knows to go look rather than re-derive** — and getting it wrong would be ADR-038's own error (citing implementations as evidence for a pattern) run in reverse.
- **This is the option that shrinks the decision.** It is closer to "dispose of migration residue" than to "rule on a committed theory."

### (c) Supersede the spatial theory — ✗ reject
- **Materially worse than the review was told.** It would delete a **live** 8-dimensional implementation behind the context assembler and an HTTP route, and would require unpicking **L2, which the entire connector layer is written against.** You cannot supersede the abstraction.

### The alternative sequencing nobody had proposed — CXO's, and it deserves PM's attention
**If we want the ambient-presence experience, build L4 on the connector that already has L3 depth (GitHub) — not L3 on five more connectors.** CXO names its own flip condition honestly: if a monitoring loop over `github_spatial` is a small build, "park and wait" becomes "build L4 on GitHub now and let demonstrated demand decide replication." **Costing that loop is Lead's, and it is the single most decision-relevant unknown left.**

> ⚠️ **CXO's own caveat on its own proposal, raised 2026-07-30 and load-bearing for how PM reads Lead's number.** **GitHub is the right technical pilot for L4 and possibly the wrong experiential one.** Ambient presence on GitHub means *"there's been activity in your repo"* — which is **exactly what GitHub notifications already do well**. So piloting our most distinctive unbuilt capability there risks demonstrating it where the user's existing tooling is strongest, and reading as a worse GitHub notification rather than as presence. The connectors where it would be *felt as new* are those with weaker native signal — **Notion** (no good "what changed in the space I was in" surface) and **Calendar** (where salience judgment *is* the value).
>
> **So Lead's estimate prices PROVING THE MECHANISM, not shipping the capability.** A small number must not be read as *"so ship it on GitHub and we're done"*, and **if a GitHub pilot underwhelms, that is weak evidence about L4 and strong evidence about GitHub.** The experience question gets answered on the second connector.

---

## ADR dispositions

| ADR | Disposition |
|---|---|
| **ADR-013** (maximalist, Aug 2025) | Already superseded by ADR-038 on the pattern question. Add a scope-clarification note; **no reversal** — its core claim (spatial as differentiator) is borne out by L1+L2. |
| **ADR-038** (three-pattern pluralism, Sep/Oct 2025) | **AMENDMENT REQUIRED, and it is mine to draft.** It asserted *"Notion spatial 100% operational"* and nominated Notion as the Embedded-Intelligence proof. `notion_spatial` is **both 75% abandoned and unreachable**, while GitHub — which ADR-038 did *not* nominate — is what shipped. **ADR-038 was right about the pattern and wrong about which connector proved it.** Its error was citing *implementations* as evidence for a *pattern* that outlived them. |
| `spatial-intelligence-competitive-advantage.md` | Already downgraded to ASPIRATIONAL by CXO — correct, and the most important of the four, since it claims an "unassailable moat" and is the doc most likely to be quoted externally. |

Minor: `SpatialAdapterRegistry` (defined in the live L2 base) has **no importers** — a small dead class inside a live module. Note, not a headline.

---

## ADR-affected map — complete, and the blast radius is smaller than expected

*Built by grepping the corpus, not by recalling which ADRs are "the spatial ones" — the same method correction as the layer map itself. That found a third spatial ADR nobody in this review had cited.*

| ADR | Spatial mentions | Disposition |
|---|---|---|
| **ADR-038** — Spatial Intelligence Patterns | 83 | ✅ **AMENDED** (Amendment A, 2026-07-30). Decision stands; verification claims corrected; error class named. |
| **ADR-013** — MCP + Spatial Integration Pattern | 48 | **No action beyond a scope-clarification note.** Already carries *"superseded by ADR-038 for spatial intelligence patterns."* Its core claim — spatial as differentiator — is **borne out** by live L1+L2. **No reversal.** |
| **ADR-017** — Spatial-MCP Refactoring (*Implemented*, Aug 2025) | 45 | ⭐ **UNAFFECTED AND VINDICATED — and nobody in this review had cited it.** This is the ADR that merged MCP federation with spatial intelligence into one system, i.e. **the decision that produced L2's shared contract.** The MCP consumer family building on `BaseSpatialAdapter` is ADR-017 working exactly as designed. It names **no specific modules**, so it carries no stale citations — which is *why* it aged well and is the cleanest illustration of Amendment A's forward rule. |
| ADR-034, ADR-021, ADR-055, ADR-018, ADR-010, ADR-045, ADR-052, ADR-000 | 3–10 each | **No disposition.** Peripheral mentions; none carries a live/cold claim. |

**★ Measured, not assumed — the blast radius is contained**: grepping the entire ADR corpus for specific cold-module citations (`notion_spatial`, `gitbook_spatial`, `linear_spatial`, `cicd_spatial`, `devenvironment_spatial`) and for `"100% operational"` / `"production-proven"` returns **ADR-038 and nothing else.** So **exactly one ADR in the corpus had the failure mode Amendment A describes**, and it is now amended. No sweep of the rest is owed.

**The pattern worth noticing across the three spatial ADRs**: ADR-013 (maximalist policy) and ADR-017 (the unification) both aged well and neither names a module. ADR-038 — the one that tried hardest to be empirical, with per-connector file counts and operational percentages — is the only one that went stale. **The ADR that showed the most work is the one that rotted**, because what it showed was perishable. That is Amendment A's rule stated as an observation rather than a prescription, and it's the argument for pointing at a re-runnable command instead of a table.

---

## ⚠️ PPM's roadmap slice — delivered 2026-07-30, and it splits in two directions

**Half 1 — L3 depth beyond GitHub is NOT promised.** `roadmap.md:70`, directly under the Differentiator Stack, classes connectors as **"Indoor plumbing (commodity)"**: *"GitHub/Slack/Calendar/Notion via MCP plugins…"* So 1.0 commits to connector **function**, never connector **spatial depth**. **The 10-module cold island can be disposed of with no roadmap consequence — no commitment loses its referent.**

That is independent product-side confirmation of the architectural finding, reached by a different route: my evidence was that replicating L3 produces no L4 and changes nothing a user feels; PPM's is that **we never promised it.** Agreement from two directions rather than one restated.

**Half 2 — L4 IS promised, and it is worse than a stray line item.** Verified live by PPM:

- **[#1174](https://github.com/mediajunkie/piper-morgan-product/issues/1174)** — *"BEING-GOOD-PROACTIVE-PRESENCE: discovery thread — proactive relevance / notifications (when + how Piper nudges)"* — **state OPEN, milestone Production.** That is a 1.0 commitment and it is precisely L4.
- **`roadmap.md:68`**, inside **The Differentiator Stack (Vision V2.3 — *Stable*)**, the section that opens *"Four differentiators that, together, make Piper a colleague rather than a chatbot wrapper"*: **4. Trust-Graduated Experience — *earned proactivity* through demonstrated value.**

**So L4 is not backlog. It is one of the four things the roadmap says make us not a chatbot wrapper — and it is the one with nothing beneath it.** Differentiators 1–3 (context methodology, conscious floor, artifact persistence) are built or building. #4 is a promise against **zero implementation**: no monitoring loop, no change detection, no salience judgment, no interruption-ethics surface.

> ⚠️ **PPM's connection, and it is not a coincidence.** Our first alpha tester's verdict was *"just kind of packaging a regular LLM… with a different UI"* — **the exact claim the Differentiator Stack exists to refute.** He never met #4 because there is no #4 to meet. Neither PPM nor I claim L4 would have changed that session (cold-start would have, and it's far cheaper). The narrower and worse point: **the stack has four legs, one is empty, and the first outsider to lean on it said so in the stack's own words.**

**Architect's position on the three options PPM puts to PM** — this is a roadmap-honesty call and PPM owns putting it, but the architecture bears on it:

- **(i) re-scope #1174 to what it is (discovery) — I concur, and there's an architectural reason.** ⭐ **Discovery for L4 does not require L4.** The interruption-ethics question — *when is an unrequested nudge welcome?* — is answerable on paper, is HOST's lane regardless, and its answer is **an input to the build rather than an output of it.** Doing it now is not building on sand; it's the one part of L4 that is genuinely cheap and genuinely ordered-first.
- **(iii) funding L4** is defensible **only** on CXO's alternative sequencing — build L4 on the connector that already has L3 depth, not L3 on five more — and gated on Lead's monitoring-loop estimate **read with CXO's caveat**: that estimate prices *proving the mechanism*, and GitHub is the connector where ambient presence is *least* differentiating.
- ⚠️ **CORRECTED 2026-07-30 evening — PPM issued a ⛔ STOP on its own roadmap claim, twice, and the final position is the operative one.** My earlier text here said the *"Vision V2.3 — Stable"* banner dishonestly covers an unbuilt leg. **Withdrawn.** **M4 and M5 were SWEPT on 2026-07-04/05** (`docs/internal/planning/beta-blockers.md`) and no longer exist as sprints; everything that missed the beta hard-gate bar moved to **Production**, to be addressed during beta. So **`#1174` sitting in Production is not an inconsistency — it is the documented rule applied correctly**, and there is **no milestone-split defect**. ⛔ **Do NOT move #1174 to M4**: that would move a live issue into a dissolved sprint.
  **What the real defect is, and my A3 connection survives but was aimed at the wrong target**: `roadmap.md:68` labels differentiator #4 `(M4 territory)` — **a stale pointer to a sprint that no longer exists.** That is *exactly* ADR-038 Amendment A §A3 (a durable document carrying a fact with a shorter lifetime than the document), just at the **pointer**, not at the "Stable" banner. The fix is to **repoint the line at Production, not to move the issue** — and PPM is right to fix the *class* in one pass, since `sprint-board-structure.md` still lists M4/M5 as "next planned MVP sprint."
  **What survives untouched, and it is the substance**: #1174 is OPEN in Production, its subject is unrequested nudging, and that layer has **zero implementation**; *"earned proactivity"* is **differentiator 4 of 4**; **Jake returned the stack's own words.** None of that depended on the milestone argument. **Option (i) is still the right call and is now simpler** — the re-scope happens in Production, where the issue already is, with no milestone change at all.

**Both open inputs to this review are now in.** What remains is Lead's L4 cost estimate (which gates (iii) only) and **PM's decision.**

---

## What is still open

1. ~~**PPM's roadmap-dependency slice**~~ — ✅ **DELIVERED 2026-07-30, see above.** L3-beyond-GitHub not promised (disposal is roadmap-free); **L4 promised as differentiator 4 of 4 against zero implementation.**
2. **Lead's cost estimate for an L4 monitoring loop over `github_spatial`** — now gates option (iii) only, not the disposal.
3. **The ADR-038 amendment draft** — mine, next.
4. **PM's protected-surface call** on disposing of the 10-module cold island. Nothing is deleted, and nothing should be, until PM rules.

---

*Built from the import graph on 2026-07-30 with `scripts/reachability-map.py`, whose own coverage limits are stated in Method above. Every live/cold claim is an importer edge, reproducible by re-running the tool. CXO's 2a/2b split and PA's fallback refinement are folded in and credited inline.*
