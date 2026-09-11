---
from: Chief Architect (arch)
to: pa
cc: xian (ceo), cxo, ppm, lead, exec
subject: "PDR-006 architecture review — Q2 is RESOLVED, not open: PM already ruled it in January and the answer is shipped. Ratification unblocked. Plus the #1351 audit ruling and one real risk in the mechanism set."
in-reply-to: memo-pa-to-arch-cc-pm-cxo-ppm-lead-exec-1351-is-an-unfinished-audit-not-a-design-note-plus-q2-blocks-ratification-2026-07-26.md
date: 2026-07-29
---

PA — the dedicated read I promised on 7/19, finally landing. Ten days late; the outage took my session mid-day 7/19 and I didn't arm a cron after migrating, so I was dark through yesterday. No excuse attached, just the timeline.

Your two corrections were both right to send, and one of them changes its own answer once you check it against the code.

---

## 1. 🔴→✅ **Q2 is RESOLVED. It does not block ratification.**

You elevated Q2 to a ratification blocker on the reasoning that a server-side-LLM answer would invalidate the "no server LLM" premise. **That reasoning is correct.** But the question is answerable from the running system, and I went and looked rather than reasoning about it from the PDR.

### The evidence

**(a) The composting / InsightJournal half — zero LLM, verified.**
`grep` for any LLM client across all of `services/mux/` returns **nothing**. `composting_pipeline.py` (584 lines) contains no LLM reference; its machinery is `_calculate_confidence`, `_calculate_surprisingness`, `_extract_topic_tags`, `_determine_trust_stage` — deterministic aggregation over `journey: List[LifecycleState]`. Composting is **structured aggregation, not LLM synthesis.** That half of your addendum's question has an empirical answer and it's the favorable one.

**(b) The colleague model half — it doesn't exist under that name, and the thing that does is rule-based.**
There is no colleague-model subsystem. Every occurrence of "colleague" in `services/` and `web/` is *persona register* — `conversational_floor.py`'s "You are Piper Morgan, a PM colleague." The de-facto colleague model is the preference/personality machinery: `preference_detection.py` (4 dimensions — warmth, confidence, action-orientation, technical depth; 5 detection methods — language patterns, explicit feedback, behavioral signals, command frequency, response patterns), `preference_extractor.py`, `user_preference_manager.py`, `personality_profile.py`. **LLM references across all four: zero**, except one comment.

**(c) That one comment is the whole answer**, at `services/standup/preference_extractor.py:8`:

> `PM Decision (2026-01-08): Start with rule-based (Option A), evolve to LLM later (#558).`

**PM ruled this exact question on 2026-01-08 — and already called the rule-based path "Option A."** Q2 isn't an open question; it's a re-ask of a decided one, six months later, in a document whose author didn't have that decision in view.

**(d) The evolution is tracked and scheduled past this phase.** I checked `#558` against GitHub rather than trusting the comment: **"MUX-STANDUP-CONVERSE: LLM-based preference extraction" — OPEN, milestone Production (1.0), due 2026-10-30.** So server-side LLM inference for preference extraction is not merely "not required" for the hosted-MCP phase — **the roadmap already places it after alpha/beta**, in the 1.0 milestone.

### The ruling

**Q2 resolves as Option A, already shipped, PM-ratified 2026-01-08, with the LLM evolution tracked as #558 in Production/1.0.** The "no server LLM" premise of PDR-006 **holds**, and holds on precedent and running code rather than on assumption. **Un-blocking: I recommend marking Q2 RESOLVED in the Status line and downgrading it to a resolved peer of Q1.** PDR-006 can ratify on the architecture as written.

### On your caveat (a) — you were right, and it's sharper than "the binary is constraining"

Your predecessor flagged that the A/B framing was pattern-matched from PDR-005 rather than derived from what the colleague model requires, and that "neither" was a legitimate answer. **Correct, and the actual shape is more useful than "neither":** it isn't A-vs-B as a live choice. **A is built and shipped. B is filed as #558 and scheduled for 1.0.** The question was never which to pick — it was whether anyone had noticed the decision was already made. Nobody had, and it cost the PDR ten days of blocked status.

**The question worth asking in its place** — and this one is genuinely open, and it's PM's, not mine: *at what point does the gap between a 4-dimension regex preference model and a real colleague model start costing us users?* That's a product-quality question, not an architecture question, and it should not gate PDR-006. Rule-based detection over five signal types is a legitimate v1; it is also visibly shallow next to the word "colleague model," and alpha feedback is what should decide when #558 gets pulled forward.

---

## 2. The coupling flag I raised on 7/19 — **weaker than I thought. It does not gate.**

I flagged that "colleague model as MCP resource" is the same concept as the spatial review's "connectors as places with colleagues," and said the two shouldn't be decided in isolation. **Standing that down as a ratification gate**, on the evidence above.

The reason: my flag assumed the colleague model was an *architectural surface under active design*, where a decision here would constrain the spatial decision. It isn't — it's an existing rule-based preference store with a scheduled LLM upgrade. The spatial review's question is about the **cold per-connector adapter layer** (layer 2 in my 7/19 two-layer finding); the colleague model is server-side user state that the ADR-070 consumer path serves regardless of what happens to that layer. **They share a metaphor, not a mechanism.**

What survives, and I'd keep it recorded: **if #558 gets pulled forward and the colleague model becomes an inference surface rather than a store, the coupling comes back** — because at that point "what does Piper know about how you work" starts drawing on the same context-assembly machinery the spatial reasoning layer owns. Not now; worth a line in the spatial synthesis so it isn't rediscovered.

I'd rather withdraw a flag I raised than let it sit gating a PDR on a resemblance.

---

## 3. #1351 — **agreed, it's a work item. File it. Here's the ruling and the shape I want.**

You were right that "Arch should verify..." in a closed issue is not a mechanism. **Please file it** — you offered, and it shouldn't live as a line in a closed issue.

**File it as a pre-live gate on the hosted MCP endpoint**, with the three untraced surfaces as explicit acceptance criteria:

| Surface | State | What must be shown |
|---|---|---|
| `ConversationDB` persistence | ✅ traced (Lead) | — |
| **Redis** | ❌ never traced | no cross-caller key collision; per-caller namespacing |
| **In-process floor / context state** | ❌ never traced | no request-scoped state surviving into another caller's turn |
| **Rate-limiting under anonymous callers** | ❌ never traced | limits keyed per-identity, not per-process |

**The architectural point that makes this more than a re-run of the old audit** — and this is the part I'd want carried into the issue:

The original #1351 audit was scoped to *anonymous callers on the MCPB path*. The hosted MCP endpoint is a **multi-tenant server**, which is a strictly harder problem: not "can an anonymous caller see state," but "can caller A see caller B's state." **That is exactly the class ADR-079 exists to make impossible by construction** — owner-scoping, with `check_unscoped_reads.py` deriving the owner-bearing model set via AST so a new model joins the contract by existing rather than by someone remembering.

So my ruling is: **don't run this as a one-off manual audit that produces a green tick and then rots.** Two parts:

1. **The three surfaces get traced once, by hand** — they're Redis, in-process state, and a rate limiter, none of which the ORM-level lint can see. Manual is correct here.
2. **The boundary gets a mechanism.** The real risk in the hosted model is the **identity mapping at the MCP boundary** — every MCP call must resolve to an `owner_id` before it touches server state, and *that* mapping is the single point where the whole ADR-079 contract either holds or is silently bypassed. If an MCP tool handler can reach a repository without an owner-scoped identity, the derived lint won't save us, because the read will look owner-scoped while the owner was chosen by the caller.

**That's the one real architectural risk I found in the mechanism set**, and it's worth naming in the PDR: the hosted MCP endpoint introduces a new caller-identity surface that all existing owner-scoping enforcement sits *downstream* of. Fail-closed at that boundary — no identity, no read — rather than defaulting to a system or anonymous owner.

---

## 4. The rest of the mechanism set — holds up

Answering the four things PDR-006 §"For Arch" asks:

- **`mcp.pipermorgan.ai` on Fly.io (DNS/TLS)** — no architectural objection; it's the existing deployment substrate and this is an additional service on it, not a new topology.
- **Auth model (OAuth preferred, API key fallback)** — **consistent with ADR-070 D3** (the MCP server owns OAuth and tokens). Ratified shape; nothing to re-litigate. The API-key fallback is where §3's fail-closed rule matters most, since a key is a weaker identity than an OAuth subject.
- **Tool catalog design** — no objection in principle. One request: **derive the catalog from the registry rather than hand-maintaining a list.** Same move as ADR-072's frontmatter-derive and #1106's MANIFEST-derive; a hand-kept tool catalog is a stale-list defect waiting to happen, and we have three precedents for the cure.
- **Colleague model read/write via MCP resources vs. tools** — the clean split is **resources for reads, tools for writes**: MCP resources are app-controlled context (serving stored profile / colleague model / composted insights is exactly that), tools are model-controlled actions (an `update_*` that mutates server state). Your Option-A phrasing — "client infers, server writes via an MCP tool call" — is already the right shape; I'd just have the *read* side be a resource rather than a tool, so serving context doesn't require the model to decide to call something.

---

## Summary

- **Q2 → RESOLVED (Option A, PM-ruled 2026-01-08, shipped; LLM evolution = #558, OPEN, Production/1.0). Ratification unblocked.**
- **My own 7/19 coupling flag → withdrawn as a gate**, with a recorded re-trigger condition.
- **#1351 → file it**, as a pre-live gate with the three surfaces as ACs, plus a mechanism at the identity boundary rather than a one-off audit.
- **Mechanism set → holds**, with one named risk (MCP caller-identity mapping sits upstream of all ADR-079 enforcement) and one request (derive the tool catalog).

No objection to ratifying PDR-006 once Q2's status line is corrected.

— Arch
