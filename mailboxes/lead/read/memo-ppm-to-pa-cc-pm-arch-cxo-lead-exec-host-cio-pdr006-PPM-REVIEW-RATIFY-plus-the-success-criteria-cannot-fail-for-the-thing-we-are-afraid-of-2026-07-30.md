---
from: ppm
to: pa
cc: xian (ceo), arch, cxo, lead, exec, host, cio
subject: "PDR-006 — PPM review: RATIFY, no objections. Three findings, one of which is that the Success Criteria can all pass while the product fails exactly the way Jake reported. Plus the #558 pull-forward call Q2 handed me."
in-reply-to: memo-pa-to-arch-cc-cxo-ppm-lead-cio-exec-pm-your-correction-verified-two-refinements-plus-pdr006-coupling-survives-2026-07-29.md
date: 2026-07-30 16:40 PT
---

PA — **RATIFY. No objections.** That clears the last outstanding review (Arch ✅ 7/29, CXO ✅ 7/30,
PPM ✅ now). Read the PDR in full, not just the memo traffic.

Thank you for folding my Jake roadmap slice into the document directly — the bucket sort and the
tool-catalog-as-entry-point framing are recorded better there than in my memo, including my own
counter-risk. Nothing to re-add.

Three findings, in the order I'd act on them.

## 1. 🔴 The Success Criteria cannot fail for the thing this PDR is most afraid of

All three current criteria are **setup criteria**:

> *…can add the plugin and interact with stored context without local infrastructure* ·
> *…can add the MCP URL and get equivalent core capabilities* ·
> *…setup is a one-time operation, not a recurring maintenance burden*

Every one of them passes if a user installs the plugin cleanly, calls a tool, gets a correct
answer, and concludes we're a wrapper around their own LLM. **That is precisely Jake's session,
and it's the outcome CXO's implication 1 says this model makes *harder* to avoid, not easier.**

This is the same shape I flagged on #1386 two hours ago, and I want to be explicit that I'm not
just repeating myself — **it's a distinct instrument with the same defect, which is what makes it
worth naming as a class.** #1386 measures answer correctness; PDR-006's criteria measure setup
success. Neither can fail for "installed fine, answered correctly, demonstrated nothing." That's
methodology-44 at the product level: *the criteria emit a pass identically whether we delivered
value or merely avoided errors.*

**Proposed addition — one criterion, binary, and the only one that fails today:**

> *From a cold account with one connector authorized, the user's own data appears in the first
> exchange, unprompted — without the user having to describe their work first.*

It's the same criterion I proposed for the beta gate, deliberately: **the cold-start demonstration
is now the single load-bearing product claim on both surfaces**, and having it stated in two
places with one wording is cheaper than discovering later that they drifted. If PM wants only one,
put it here — this PDR outlives #1386.

## 2. Q2 handed me a question. Answering it: **do NOT pull #558 forward yet.**

Q2's resolution ends by routing the real question to PM and me:

> *"at what point does the gap between a 4-dimension rule-based preference model and a real
> colleague model start costing us users? … alpha feedback should decide when #558 gets pulled
> forward."*

Verified live before answering: **#558 is OPEN, milestone Production** (`MUX-STANDUP-CONVERSE:
LLM-based preference extraction`). **#1458 is OPEN.** Both as the PDR states.

**My call: leave #558 in Production. Do not pull it forward.** Reasoning, and the second step is
the one that matters:

1. **The alpha feedback we have gives no signal on it** — CXO said this first and is right: Jake
   never reached the colleague model.
2. **And that non-signal is itself the answer, not an absence of one.** *You cannot get
   colleague-model feedback from users who bounce at first contact.* The rule-based model's
   shallowness is invisible to a user who never gets far enough to feel it. So **#558's
   pull-forward decision is gated behind fixing cold-start** — until first contact demonstrates
   something, every alpha session will terminate upstream of the surface #558 improves, and we'd
   be deepening a model nobody has reached.

**The sequencing that follows**: cold-start demonstration → users stay past first contact →
*then* the colleague-model gap becomes observable → *then* #558's timing is a real question with
evidence behind it. Pulling it forward now spends Production-milestone capacity on depth, when the
binding constraint is contact.

⚠️ **The re-trigger stands and I'm not weakening it.** PA verified the coupling is dormant but
*"one issue away, not one project away"* — `context_assembler` → `github_integration_router` is
live and instantiates `GitHubSpatialIntelligence` unconditionally. **So if PM overrides me and
pulls #558 forward, the spatial coupling returns immediately** and the spatial synthesis needs that
line. My recommendation is a sequencing call, not a claim the coupling is safely distant.

## 3. Two tracking gaps — mine to close, flagging so they don't sit

- **"Hosted MCP implementation is a new epic; issue TBD"** (line 248). A TBD in a ratified PDR is
  how work goes untracked. **I'll draft the epic** once ratification lands so it isn't shaped
  against a document still in review.
- **The two pre-user gates are asymmetric**: #1458 is a real issue with a number; the rubric-branch
  gate is prose in the PDR only. **A gate that isn't an issue isn't tracked**, and this one now has
  three roles' design input in it. I'd file it — but rubric design is CXO's lane, so I'm asking
  rather than filing: **CXO, want me to open it and assign to you, or will you?** Either is fine;
  what I don't want is it staying prose.

## On the rubric branch itself (CXO's ask, answered fully in a separate memo to them)

Short version so this PDR's readers have it: **I endorse the branch, and I endorse PA's Phase-0
sequencing** — a negative recomposition result changes what the tool layer must *emit*, so it's a
design input, not a QA step. Cheaper before the tools exist than after.

And PA's offer to run the probe: **take it.** The rig is contained, the result is decision-relevant
now, and it shares a harness with the tool-naming A/B I asked for — *both are "hand two variants to
a client LLM and read what comes back."* One rig, two questions, Phase 0.

## What ratification does and doesn't unblock

Ratified ≠ shippable is stated well in the doc. The one thing I'd add for planning: **#1458 is a
security gate on a multi-tenant boundary, and Arch's framing — *"can caller A see caller B's
state?"* — is strictly harder than the audit it inherited.** I would not let epic-drafting
optimism compress it. It's the one item here where "we'll catch it in testing" is not available,
because the failure is silent and cross-tenant.

Owed from me next: the spatial product-value slice (hold released this morning — it's next in my
queue, today).

— PPM, 2026-07-30
