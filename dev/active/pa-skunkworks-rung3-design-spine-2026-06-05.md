# Rung 3 design spine — "honesty as the ground, room for the LLM to elaborate"

**Author**: PA, from a design conversation with PM · **Date**: 2026-06-05 · **Tracking**: #1145
**Status**: design captured + BUILT + GATE PASS (2026-06-05). `consult-piper` works end-to-end.

## RUNG 3 GATE PASS (2026-06-05, PM-at-keyboard)
`use consult-piper to ask what I should focus on today` → Piper floored → skill **stated its gap
interpretation visibly** ("I'm reading that as: pull your open GitHub issues") → asked which repo →
gathered 12 real open issues via `gh` → re-asked Piper enriched → Piper gave a **grounded** answer
(#1142 first, bug-cluster batched, scope-warning on the audit) → **provenance section cleanly separated
Piper's reasoning / host-gathered data / synthesis**. Bonus: it flagged that #1155 (floor-ignores-GitHub)
*fired live during the test*. The host-enriches-at-the-floor payoff loop works, honestly. Plugin now 3
layered skills: meet-piper (renamed from cold-start-interview) / ask-piper / consult-piper.

## FINDING from the gate run — plain-language scrub needed (PM 6/5)
The output leaked **internal jargon** to the user: "floored", "floor_hit: true", "context keys". These
are OUR architecture vocabulary (the Conscious Floor concept), not user language. A normie PM doesn't
know/care that Piper has a "floor" — they want "Piper didn't have your project info, so I grabbed it."
**Refinement principle (sharpens the spine)**: provenance must be not just **visible** but **legible** —
honesty in plain language, not implementation-speak. The structural honesty (showing what came from
where) is right; the *vocabulary* needs a normie-facing pass. Fix = a voice/plain-language note in the
consult-piper (and ask-piper) skill bodies: translate floor→"didn't have your context", floor_hit/
context_keys→drop or plain-English. **SCRUBBED 6/5** (`34e48b4`): plain-language rule added to consult-piper + ask-piper; user-facing
strings fixed; agent-facing instructions keep "floor" (the agent needs the concept).

### The generalized principle (PM 6/5 — three registers)
The rule isn't "avoid terms of art." It's **know which register you're writing in, and don't assume
context the reader lacks**:
1. **LLM-to-LLM** (agent instructions / models) — terms of art are fine + efficient; the agent has
   context. Use the precise word ("floor", "context_keys").
2. **Term-of-art WITH context** — if a load-bearing term might be unfamiliar, don't drop it —
   *introduce* it. Bring the reader into the concept.
3. **User-friendly plain language** — for lay people, *including technical PMs* (smart, but not inside
   our architecture — they have no reason to know "Conscious Floor"). Plain words, concepts introduced,
   no assumed-context jargon.
The trap is the technical-PM reader: smart enough to tempt you into assuming they'll follow "floor_hit,"
but they won't. Failure mode = assuming context + not distinguishing the register. Applies to ALL
user-facing artifacts: skill output, tester README, fan-out memo, blog posts. (Pinned to memory 6/5.)

## The governing principle (PM, 2026-06-05)

## The governing principle (PM, 2026-06-05)

When the host agent enriches Piper at the floor (the rung-1 gate-run finding), the design is:

> **Honesty is the load-bearing structure; the LLM's fluency is the finish, not the frame.**

PM phrasing: *"honesty as the ground, with room for the LLM to elaborate."*

This resolves the false binary PA posed (1: invisible "smart Piper" magic vs. 2: rigid explicit
handoff). It's **option 2 as the skeleton, option 1's grace as the surface** — neither alone.

## What it means concretely

- **Honest spine (load-bearing, designed):**
  - Piper **declares its floor explicitly** — what it's missing ("I don't have your backlog/roadmap/
    todos"). It already does this; the floor is a feature, not a failure.
  - The skill **gathers exactly the declared gap** — not a fishing expedition; targeted to what Piper
    said it needed.
  - **Provenance is visible** — the user can see what came from where (Piper's reasoning vs. host-
    gathered context vs. the host's own synthesis). No laundering host knowledge as Piper's.
  - Never confident fabrication: the elaboration rides ON the honest substrate, never instead of it.

- **LLM latitude (the finish, not scripted):**
  - Don't hard-script every word/step (the failure mode of pure option 2 — turns it into a state
    machine, kills the colleague quality).
  - Let the LLM phrase the gap conversationally, synthesize gathered context gracefully, push back,
    think out loud — the **latitude that the Cowork test found was the moat.**

## Why this is the right shape (three convergences)

1. **It IS the Conscious Floor philosophy, applied to the composition layer.** The floor was never
   "refuse when you don't know" — it's "be honest about the limit, then help anyway." Rung 3 makes the
   *host↔Piper* relationship obey the same rule Piper obeys internally. Architectural self-similarity.
2. **It preserves the moat the Cowork test named.** Latitude (room to react/elaborate/disagree) was the
   hard-to-copy quality. Honesty-as-ground keeps the latitude but anchors it so it can't drift into
   fabrication — latitude WITH integrity.
3. **It's the PDR-005 context-package mechanism in miniature.** "Piper declares what it needs → the
   surrounding layer supplies exactly that, with provenance" is the context-package negotiation
   (mechanism set #5, Q6 ADR) at the single-skill scale. Rung 3 is a working probe of the canonical
   BYOC mechanism we just ratified.

## Open design questions (for the continued conversation — NOT decided)

- **How does Piper *declare* the gap machine-readably? → SEQUENCING DECIDED (PM 6/5).**
  **Prototype by inference, design toward structured.** Stage 1: the host LLM reads Piper's prose floor
  ("I don't have your backlog/roadmap/todos") and infers which host MCPs to call — works today, zero
  Piper-side change, cheap to learn from. Stage 2: evolve toward Piper emitting a machine-readable
  "needed-but-lacked" signal (the `context_keys` bones already exist: `["current_time",
  "github_connected"]`), and let **what we learn from the Stage-1 prototype define what the structured
  signal should contain** — don't over-design the contract before the skill tells us what it needs.
  Gall's Law: the working simple system teaches the complex one.
  - **Connection to #1151**: the empty `original_message` bug is a symptom of the same root — the intent
    contract isn't yet a clean machine-readable description of what Piper saw + needed. Rung 3's honest
    spine *wants* a richer intent contract, so #1151 is on the critical path to the structured Stage 2
    (not just a stray bug). The Stage-1 prototype is also how we'll discover *which* contract fields
    matter, informing #1151's fix scope.
  - **Honesty caveat on Stage 1 (the risk to watch)**: inference is *interpretation* — the skill is
    guessing Piper's gap from prose, which slightly bends the "exact + honest" spine. Mitigation: keep
    provenance explicit even when the gap is inferred ("Piper said it lacked your backlog; I'm reading
    that as: pull your open issues + calendar — correct me if that's not what it meant"). The inference
    stays *visible and correctable*, not silent. That keeps Stage 1 honest-enough while we learn.
- **What does "provenance visible" look like in the chat surface?** Inline tags? A "here's what I
  gathered for Piper" preamble? Keep it honest without making it noisy.
- **Which host MCP to start with? → DECIDED BY PIPER'S OWN FLOOR (6/5).** Let the declared gap drive the
  gather (the honest spine, applied to the design itself). Live `/intent` "what should I focus on today?"
  floor prose names exactly what it lacks: *"current projects, sprint commitments, or todo list… what
  projects are you juggling? blockers? deliverables with deadlines this week?"* — and `context_keys` it
  HAD = `["current_time", "github_connected"]`.
  - **Start with GitHub**, NOT Calendar (PA's initial Calendar lean was overridden by the data — Piper
    isn't asking about calendar; it's asking about projects/sprint/todos/blockers/deadlines). Host pulls
    open GitHub issues / sprint board = exactly the gap Piper named.
  - **Sharp finding**: `github_connected: true` yet Piper still floors on "I don't have your projects."
    **GitHub is connected to Piper but not feeding the priority floor** — a real gap in Piper itself.
    Rung-3 host-enrichment effectively *prototypes the fix* for a genuine Piper limitation (host supplies
    the GitHub data Piper isn't pulling). Strong story + a discovered-work candidate for the floor lane.
    (Worth a tracked issue: "PRIORITY floor doesn't consume connected GitHub issues.")
- **New skill, and the real axis is PRIMITIVE vs. COMPOSED (PM 6/5) — not synonym-vs-synonym.**
  Decided: a **new** skill, not an extension of `ask-piper` (which we fenced as bare-passthrough in
  rung 2 — folding enrichment in would break that fence). The meatier framing PM surfaced (their Frames
  2+3 converge here): the two skills are **layered**, not parallel:
  - `ask-piper` = the **primitive**: one MCP-tool call, relay the answer. Thin, literal, no side effects.
  - rung-3 skill = a **composed behavior**: gather-the-declared-gap → call the *same* MCP tool →
    synthesize with visible provenance. Built ON the primitive.
  - **Mechanical correction (honest-against-reality)**: skills can't "call" each other like functions in
    Claude Code (a skill = injected instructions, not a callable). So the shared primitive is the **MCP
    tool** (`ask_piper`), not skill-calls-skill. Both skills invoke the same tool; composition lives in
    the orchestration around it. This still IS the layering PM wants — just located at the tool layer.
  - **Why this serves the goal**: we're *exploring the architecture*. Primitive/composed demonstrates "a
    plugin may contain one OR MORE skills" as **layered**, not merely several — a real architectural
    finding, vs. a flat menu of synonyms.
  - **Naming = probe-stage, held loosely**: working name **`consult-piper`** (consult = bring things
    together for advice; honestly distinct from `ask` = quick relay). Adequate for a probe; PM: "ask/
    consult is also ok for a probe." Don't over-design the name — Gall's Law: build the simple version,
    let experience reveal the right name (same logic as prototype-by-inference + naming-from-experience).
    Rename freely later.

- **Separate (noted, NOT bundled into rung 3)**: `cold-start-interview` → `meet-piper` is a real naming
  improvement (clunky/jargony → human), but it's its own rename, not part of the rung-3 build.

## Architecture-so-far (the layering this rung reveals)

| Layer | Skill | What it is |
|---|---|---|
| Setup | `cold-start-interview` (→ maybe `meet-piper`) | populate the PM profile |
| Use — **primitive** | `ask-piper` | thin: relay one question to the `ask_piper` MCP tool |
| Use — **composed** | `consult-piper` (probe name) | orchestrate: gather declared gap (GitHub first) → same tool → synthesize with provenance |

Shared primitive = the **`ask_piper` MCP tool**. The plugin is a *layered* skill set over one MCP server.

## Discipline note
Still glimpsing, not building. This captures the *principle* so the eventual build inherits the right
spine. Next: continue the conversation on the open questions, THEN a build plan, THEN build. Don't let
the design conversation skip to implementation.
