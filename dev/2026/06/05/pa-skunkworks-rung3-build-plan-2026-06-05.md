# Rung 3 build plan — `consult-piper` (host enriches Piper at the floor)

**Author**: PA · **Date**: 2026-06-05 · **Tracking**: #1145 · **Design spine**: `pa-skunkworks-rung3-design-spine-2026-06-05.md`
**This doc is the resume-point**: if interrupted mid-build, restart from "Build steps" + check what's committed in skunkworks.

## Goal

A NEW skill, `consult-piper` (probe name, held loosely), that demonstrates **composed-on-primitive**
layering: when Piper floors for lack of context, the host gathers the declared gap (GitHub first),
re-asks Piper enriched, and synthesizes with **visible, correctable provenance**. Honesty as ground,
LLM latitude as finish.

## Locked decisions (from the design conversation)

- **New skill**, not an extension of `ask-piper` (which stays bare-passthrough per its rung-2 fence).
- **Composed-on-primitive**: `consult-piper` orchestrates around the SAME `ask_piper` MCP tool. Shared
  primitive = the tool (skills can't call skills in Claude Code).
- **Stage 1 = prototype-by-inference**: host reads Piper's prose floor, infers the gap, gathers it.
  Stage 2 (later) = structured "needed-but-lacked" signal from Piper (#1151 on that critical path).
- **GitHub first** (Piper's DNA + #1155: floor declares it lacks projects/sprint/todos despite
  `github_connected:true`). Calendar is the natural next source, not now.
- **Visible + correctable inference**: the skill SHOWS its interpretation of the gap and invites
  correction before/around gathering — never silently guesses Piper's need.

## The skill's behavioral contract (the honest spine)

1. **Ask Piper first** (via `ask_piper`) — get Piper's own answer + whether it floored.
2. **If Piper floored** (detect: the `ask_piper` OK response whose prose declares missing context — e.g.
   "I don't have your projects/sprint/todos"):
   a. **State the interpretation, visibly**: "Piper floored — it said it's missing your current projects
      and priorities. I'm reading that as: pull your open GitHub issues. (Correct me if that's not it.)"
   b. **Gather exactly that** — use the host's GitHub MCP (or `gh` if no MCP) to pull open issues /
      a priority slice. Targeted to the declared gap, not a fishing trip.
   c. **Re-ask Piper, enriched** — call `ask_piper` again with the original question + the gathered
      context folded into the message ("Here's my current open work: [issues]. Given that, what should I
      focus on today?").
   d. **Synthesize with provenance** — present Piper's enriched answer, clearly marking what came from
      Piper vs. what the host gathered. No laundering host data as Piper's reasoning.
3. **If Piper did NOT floor** — just relay (same as ask-piper); no gathering needed.
4. **No-silent-failure throughout** — honor ask_piper's failure tags (SERVER-DOWN / PIPER-INTERNAL-ERROR
   / etc.); if GitHub gather fails, say so and still relay Piper's un-enriched answer.

## Build steps (Gall's Law — smallest working version)

**File**: `piper-morgan-skunkworks/byoc/poc/dinp/piper-morgan/skills/consult-piper/SKILL.md`
(mirrors the `ask-piper` / `cold-start-interview` skill-dir convention; one new SKILL.md, no manifest or
MCP-server changes — same minimal-diff discipline as rung 2.)

1. Frontmatter (match conventions): `name: consult-piper`, description naming it the "fuller working
   session — gathers missing context when Piper floors" vs. ask-piper's quick relay.
2. Body = the behavioral contract above, written as agent instructions (not code).
3. **Gather mechanism for v1**: prefer the host's GitHub MCP if present; fall back to `gh issue list`
   (the host has shell). Keep it to "open issues, newest/priority slice" — don't over-pull.
4. Scope guard in the skill: GitHub-only for now (Calendar/etc. later); inference-stage (no structured
   signal yet); provenance always visible.

## Acceptance test (rung-3 gate, PM-at-keyboard)

Fresh `claude --plugin-dir …` session, Piper running local:
1. `/consult-piper` appears under `(piper-morgan)` alongside ask-piper + cold-start. ✓
2. Invoke it with "what should I focus on today?" → it asks Piper → detects the floor → **shows its gap
   interpretation** → gathers GitHub issues → re-asks Piper enriched → Piper now gives a *grounded*
   answer (names actual issues), with provenance visible. ✓
3. The honesty check: the output makes clear what Piper reasoned vs. what the host gathered (not
   laundered). ✓
4. Failure paths: GitHub gather fails → skill says so + still relays Piper's un-enriched answer (no
   fabrication). ✓

If all pass: **rung 3 gated PASS** — the host-enriches-at-the-floor payoff loop works, honestly.

## Watch-items / notes
- Floor-detection heuristic: reuse the phrasing markers from ask_piper's PIPER-INTERNAL-ERROR logic
  pattern, but for "missing-context" floor prose ("I don't have", "I'd need to understand", "what
  projects"). Imperfect; that imperfection is *why* Stage 2 (structured signal) exists.
- This prototype is also the live workaround-demo for #1155 (floor doesn't consume connected GitHub).
- Keep ask-piper untouched — consult-piper is additive.
