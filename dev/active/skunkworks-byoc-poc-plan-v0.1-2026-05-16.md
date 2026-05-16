# Skunkworks Project: BYOC Proof-of-Concept via Anthropic Plugin / MCP / Skills

**Plan version**: v0.1 (PA strawman for PM collaboration)
**Status**: DRAFT — PA writes; PM + PA finalize
**Owner**: PA (overseeing); subagent(s) execute; PM is copilot
**Started**: 2026-05-16

---

## Project framing

**This is a skunkworks**, not a production track. The goal is rapid experimentation and learning: build a PoC that helps us answer "*what shape does Piper-as-plugin/MCP/skills actually take?*" while the leadership BYOC exploration (Architect feasibility check + PDR-005 v0.3) answers the strategic / architectural question at higher altitude. Both tracks feed each other; neither answers the other alone.

Operating principles per PM 2026-05-16:

- **Doesn't need to ship.** Doesn't need to be production-compatible. Won't go into the canonical codebase unless we explicitly decide it should.
- **Build less.** When in doubt, less. We iterate before we even think we have a viable PoC.
- **Contained but not hidden.** Leadership read in via prototype sharing + may seek input during design.
- **Backseat to core duties.** PA's mailbox triage, cross-pollination routing, ad-hoc PM questions, and methodology routing stay primary. Skunkworks is top priority when attention is available, paused when it isn't.
- **Validation discipline.** PA validates subagent output before it reaches PM. "Subagent said X; I confirmed Y" is the contract.

---

## Step 0 — Setup (PA hands-on, before subagent dispatch)

### 0.1 Clone the Anthropic priors

Two repos to study, per PM:

- **`https://github.com/anthropics/claude-for-legal`** — the architectural prior PM named as the fork target. Clone destination: `/Users/xian/Development/claude-for-legal/` (PM convention for sibling-project clones).
- **`https://github.com/anthropics/knowledge-work-plugins/tree/a0fda662dd52f2704c43a57ea38ff7de647b013f/product-management`** — comparison study. Clone the full `knowledge-work-plugins` repo at that commit (`a0fda66`); the `product-management/` subtree is the relevant slice.

`[PM INPUT NEEDED 0.1]`: Confirm clone destinations. Do you want both at `/Users/xian/Development/`, or somewhere else? Do you want PA to do the clones, or would you prefer to clone yourself (so the credentials/access are clean on your side)?

### 0.2 Skunkworks workspace setup

A dedicated workspace for the PoC artifact, separate from the PM codebase but able to reference it:

- **Worktree**: `claude/skunkworks-byoc-poc` branch + sibling checkout at `../piper-morgan-product-skunkworks-byoc/` (per worktree-default directive). Or — given skunkworks doesn't need to live IN the PM repo at all — a separate top-level dir `/Users/xian/Development/piper-morgan-skunkworks-byoc/` with its own git repo.

`[PM INPUT NEEDED 0.2]`: Skunkworks workspace shape — branch + worktree in PM repo, or separate top-level dir? My lean is **separate top-level dir** because:
- (a) Skunkworks artifact shouldn't pollute PM repo's git history with experimental scaffolding
- (b) The PoC may eventually be its own repo (plugin distribution); starting separate makes that path easier
- (c) Read-only references to PM repo are fine cross-tree; no need to live inside it

### 0.3 Plan-tracking document

PA maintains a skunkworks tracker at `dev/active/skunkworks-byoc-tracker.md` (in PM repo, for PA's coordination/log discipline). Daily status + subagent dispatch state + open questions + finding log. Mirrors the V1 Duty Cycle session-log discipline CIO is piloting.

---

## Step 1 — Subagent 1: Anthropic plugin architecture study

**Subagent kind**: research subagent (Explore-shape; read-only, returns findings to PA).
**Deliverable**: a 2-4 page memo: *"What Anthropic's plugin / MCP bundle / skills architecture actually is, with claude-for-legal + product-management as concrete instances."*
**Time**: estimate ~2-4 hours subagent time (single dispatch).
**Validation gate**: PA reads memo + cross-references against Anthropic public docs (via WebFetch) before sharing with PM.

Key questions for the subagent to answer:

- What ARE Anthropic plugins, MCP bundles, and skills, mechanically? How do they relate? What does each layer do?
- How does claude-for-legal organize its functionality across these layers? What lives in MCP server? What lives in skills? What lives in plugin manifest?
- How does the product-management plugin in knowledge-work-plugins differ in architecture? Same shape or different?
- What's the developer surface (config files, manifest formats, install/distribute flow)?
- What patterns translate to "PM-as-plugin" shape, what doesn't?

`[PM INPUT NEEDED 1.x]`: nothing right now; will surface if the subagent's findings raise questions.

---

## Step 2 — Subagent 2: PM codebase extraction analysis

**Subagent kind**: research subagent.
**Deliverable**: a 3-5 page memo: *"PM's distinctive value, organized by candidate plugin-layer destination."*
**Time**: estimate ~3-5 hours subagent time.
**Validation gate**: PA reads memo + spot-checks claims against PM codebase + reconciles with the BYOC scan (May 10) + Anthropic Dreams findings (May 12).

Subagent task:

- Identify PM's distinctive features (composting / Type 1 + Type 2 dreaming, object models per `objects-catalog.md`, ethics boundaries per ADR-061, trust graduation per PDR-004, Insight Journal, COMPOSTED-state experience, etc.)
- For each distinctive feature, propose a candidate layer mapping: skill / MCP tool / MCP resource / plugin manifest / PM API endpoint
- For each, note: confidence level, what would need to be extracted vs rebuilt, what's PM-internal-only (won't translate), what's load-bearing for PM's distinctive value vs commodity
- Identify the "what lives where" tensions that the PoC build pass would have to resolve

`[PM INPUT NEEDED 2.x]`: nothing right now; will surface if the subagent's findings raise questions.

---

## Step 3 — PA synthesis pass

PA reads both subagent memos + reconciles into a *"What the PoC should attempt to build"* memo. Probably 1-2 pages. Specifies:

- The minimum PoC scope (smallest set of PM features expressed across plugin/MCP/skills that demonstrates the architectural fit question)
- The "good enough to learn from" threshold per feature
- Explicit OUT-of-scope list (so subagent 3 doesn't drift)
- The "PoC asks" — open architectural questions the build pass should surface

**Validation gate**: PM reviews + ratifies before subagent 3 dispatch. This is the **first formal PM gate**.

---

## Step 4 — Subagent 3 (or 3+N): PoC build pass(es)

**Subagent kind**: programmer subagent (likely a coding-agent subagent with its own session log per CLAUDE.md guidance).
**Deliverable**: working PoC artifact at the skunkworks workspace path.
**Time**: highly variable; expect to iterate. First pass probably 1-2 days of subagent time.
**Validation gate**: PA verifies the PoC actually runs + demonstrates the architectural fit question + cross-references against subagent 2's extraction analysis.

Build sub-passes likely:

- 4.a Skeleton plugin manifest + MCP server scaffold (fork from claude-for-legal)
- 4.b One PM-distinctive feature expressed end-to-end (skill + MCP + PM API stub) — proves the layering works
- 4.c Iterate: add a second feature, see how the layering generalizes
- 4.d Stop when we have learned enough to answer the question (per "build less")

Each sub-pass: subagent dispatches, ships, returns findings. PA validates. PM gate at each meaningful inflection (typically after 4.b and 4.c).

`[PM INPUT NEEDED 4.x]`: build-pass gates. Per "iterate before viable PoC," we'll have several gates here; first one is at 4.b.

---

## Step 5 — Leadership read-in

When PA + PM judge the PoC has produced enough signal to be useful, share with leadership:

- **Architect** (BYOC feasibility check lane) — PoC findings about "what lives where" inform their architectural commitments
- **PPM** (PDR-005 drafting lane) — PoC findings about decision-rule consequences inform PDR-005 v0.N
- **CXO** (experience review lane) — PoC findings about the user-facing surface inform their experience commitments
- **CIO** (methodology lane) — PoC findings about the build-less / iterate discipline may inform methodology
- **Comms** — when the project has produced learnings worth narrating, Comms lane

`[PM INPUT NEEDED 5.x]`: timing for leadership read-in. My lean: after we have at least one feature expressed end-to-end (Step 4.b complete). Earlier would be premature; later loses the parallel-track benefit.

---

## Coordination shape with Architect (parallel work)

Architect is doing BYOC feasibility check + PDR-005 architectural fill-in (AC-1 through AC-4). The skunkworks operates at a different altitude (operational PoC vs strategic commitments) but shares the question domain.

Proposed coordination:

- **Pre-Step 0**: PA sends Architect a brief heads-up memo: "PA running a parallel skunkworks PoC on BYOC layering question; coordination shape below." Not asking for review or approval — just visibility.
- **After Step 3 (PA synthesis)**: share the "what the PoC should attempt to build" memo with Architect. Invite flag-back if any of the proposed layer mappings conflict with their architectural commitments. Not gating.
- **After Step 4.b (first feature end-to-end)**: share PoC findings with Architect. By this point, real signal exists.

`[PM INPUT NEEDED — coordination]`: endorse this shape, or want lighter / heavier coordination with Architect?

---

## Validation gates (PA → PM)

Three formal PM gates:

1. **End of Step 3** (PA synthesis): PM ratifies PoC scope before subagent 3 dispatch
2. **End of Step 4.b** (first feature end-to-end): PM reviews PoC behavior; decision = continue iterating / pivot / stop
3. **End of project**: PM reviews final state; decision = leadership read-in / archive / extract findings

Plus continuous: PA surfaces to PM whenever a fork or substantive finding lands. Mirrors how we've been operating on Anthropic Dreams research and other multi-step work.

---

## Cadence + check-in shape

PA daily status update in the skunkworks tracker doc (visible to PM; not pushing per-day to PM directly). Surface to PM whenever:

- A formal gate is reached
- A subagent dispatch is about to start (PA flags the gate decision before dispatching)
- A substantive finding warrants discussion
- PA is uncertain whether to proceed and wants direction

Implicit: if PM hasn't heard from PA on skunkworks in a few days, assume PA is paused on it due to other duties (per "backseat to core duties"). PA picks back up when bandwidth opens.

---

## Worktree + branch discipline

Per worktree-default directive:

- **v0.1 plan drafting (this doc)**: on main, as a single substantive doc (defensible exception)
- **All subsequent skunkworks work**: in a dedicated worktree OR separate top-level dir (see [PM INPUT NEEDED 0.2])
- **PA session log + tracker doc**: in PM repo (where institutional memory lives)
- **PoC artifacts**: in skunkworks workspace, NOT in PM repo

---

## Risk + mitigation

| Risk | Mitigation |
|---|---|
| Scope creep ("PoC needs more polish") | PA enforces "build less" + cuts ruthlessly at each gate |
| Subagent produces low-quality output | PA validates before propagating; can re-dispatch with refined prompt |
| Skunkworks competes with core duties | Explicit "backseat" framing; PA pauses skunkworks when triage / xpoll / ad-hoc PM work demand attention |
| Findings conflict with leadership work | Parallel track is the design; conflicts surface during read-in (Step 5) and inform both lanes |
| PA over-promises on subagent supervision | Honest naming: this is new for me; expect "I'm not sure if this output is good enough" moments surfaced to PM |
| Anthropic plugin architecture changes mid-project | Pin to specific commits in clones; flag if Anthropic ships breaking changes during the project |

---

## Open questions for PM (consolidated)

Marked `[PM INPUT NEEDED X.y]` above:

- **0.1**: Clone destinations + whether PA or PM does the clones
- **0.2**: Skunkworks workspace shape — branch in PM repo, or separate top-level dir? (PA lean: separate)
- **5.x**: Leadership read-in timing (PA lean: after Step 4.b)
- **Coordination shape with Architect** (PA lean: light heads-up pre-Step-0; share synthesis post-Step-3; share PoC post-Step-4.b)

Plus general: anything in this plan shape that lands wrong before we finalize?

---

## What this plan is NOT

- Not a commitment to ship anything to the PM codebase
- Not a competing track to leadership's BYOC architectural work
- Not an attempt to be the canonical answer on "what lives where" — just to generate signal that helps the canonical work
- Not gated on Anthropic's plugin architecture being stable (we pin to a commit)
- Not a multi-month investment — this is meant to produce signal in days/weeks, not weeks/months

---

— PA, 2026-05-16, v0.1 strawman
