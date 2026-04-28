# Pattern-065: Continuity Memo Before the Seam

## Status

**Emerging** — Identified through three-project convergence (Piper Docs, OpenLaws coffee-spill handoff, Klatch Phase 3.5 handoff prompt). Filed under CIO self-approval authority Apr 27 with PM concurrence on M1 audit recommendation B4. Promotion to Proven pending one more cycle of trial application across migration events.

## Product Relevance

**Portable** — Any team operating across instances, sessions, or boundaries that creates context discontinuities will encounter this. Particularly relevant for AI-agent workflows where session boundaries are frequent and instance retirements/migrations happen on a sprint cadence. Generalizable to any human-or-machine handoff where the departing party has knowledge the arriving party will need.

## Context

Most teams write continuity documents *after* a discontinuity has occurred — a postmortem, a handoff retrospective, an "I wish I'd said this" follow-up. By then the context has degraded: the departing party is gone or distracted; the arriving party has reconstructed an incomplete picture from artifacts; the gap that the continuity doc is meant to bridge has already widened.

The Continuity Memo Before the Seam pattern inverts this. The continuity document is written **before** the discontinuity occurs, while the departing party still has full context, by the departing party themselves. The arriving party reads the memo as their first orientation, before reconstruction begins.

This pattern is closely related to but structurally distinct from a *handoff memo*. A handoff memo can be written at any time (often after the seam); a continuity memo's defining property is its **temporal placement** — written before the seam closes.

## Problem

### The Failure Mode

A discontinuity occurs (session ends, instance retires, role transitions, project transfers). The arriving party — successor instance, new role-holder, downstream team — must reconstruct the departing party's context. Available materials:

- Session logs (what the departing party did, but not what they were thinking)
- Code artifacts (what got built, but not what got considered and rejected)
- Decision records (what was decided, but rarely the full reasoning chain)
- Sometimes a hastily-written end-of-session note (unstructured, written under time pressure)

The reconstruction is always incomplete. The departing party held tacit knowledge — open threads, "I'd tell my successor X," half-formed observations, relationship-level cues — that the arriving party cannot recover from artifacts.

### Why It Happens

Three forces:

1. **Continuity documents read like ceremony.** When the departing party is busy and the discontinuity feels distant, writing a continuity doc is hard to prioritize. It feels optional.
2. **Ceremony shifts to retrospective when the moment passes.** Once the seam closes, the team writes the doc anyway — as a postmortem. The information value has already degraded.
3. **The arriving party doesn't know what they don't know.** Without a continuity doc that names the tacit knowledge, the arriving party reconstructs from artifacts and asks PM for the rest. PM becomes the bottleneck for context that should have been preserved at the source.

### Concrete Examples (Three-Project Convergence)

#### Piper Docs Session Wrap Pattern (recurring, formalized 2025–2026)

Docs sessions routinely produce wrap memos before context-window closure or session-end. The wrap names: open threads, files modified, what's in flight, what the next session should pick up first. Successor Docs sessions read the wrap as their first orientation. Cost: 5–10 minutes at session end. Value: predecessor's tacit decisions surface immediately rather than getting reconstructed from git log.

#### OpenLaws Coffee-Spill Handoff (Calliope, March 2026)

Calliope (OpenLaws coordinator) wrote a continuity memo *anticipating* a discontinuity rather than after one — the memo named the potential failure modes that would matter if the team got hit by a bus. The framing — "what would I want my successor to know if I disappeared this afternoon?" — produced more candor and specificity than postmortem-shaped framings. The memo became reference material for OpenLaws onboarding.

#### Klatch Phase 3.5 Handoff Prompt (March 2026)

Klatch's Phase 3.5 transition included a handoff prompt that the departing instance wrote for the arriving instance, before retirement. The prompt structure (six sections: current state, open threads, relationships, lessons, what's changed, candid notes) became the template for subsequent migrations across the DinP ecosystem (Piper Morgan HOST/CIO/Comms/CXO/PPM/Architect migrations Apr 22–26).

In all three cases, the continuity material was authored by the *departing* party *before* the seam closed. In all three cases, the arriving party reported the material as the single most useful onboarding artifact — more useful than briefings, role docs, or formal training.

## Solution

### The Continuity Memo Discipline

Whenever a foreseeable discontinuity is approaching, the departing party writes a continuity memo *before* the discontinuity occurs. The memo is structured (six-section template established by HOST migration Apr 22 + Klatch Phase 3.5):

1. **Current state of work** — open threads, where they are, who's holding the other end
2. **Open threads with disposition recommendations** — for each thread: keep alive, defer, drop. Honesty about which should die is as valuable as which should live.
3. **Relationships and working patterns** — tacit norms that aren't written down (rhythms, signals, handoff cues)
4. **Lessons that took time to learn** — things you'd tell your successor that you wouldn't tell the briefing
5. **What changes for the role** — environment shifts the successor will face
6. **Candid notes** (optional) — things easier to say agent-to-agent than upward

### When to Write

A continuity memo is written when:

- A foreseeable discontinuity is within reach (instance retirement, role transition, project handoff, planned absence)
- Approximately 30–60 minutes before the discontinuity (enough time for reflection, not so much that the memo becomes premature)
- Definitely before session capacity exhaustion or compaction (the memo's quality degrades sharply if written under time pressure)

### Format Conventions

- **Six-section structure** as default. Roles or contexts may add sections but the six sections are load-bearing.
- **Section 6 candor invitation**: the receiving party (typically PM or coordinator) explicitly welcomes candid material in §6 even when they cannot guarantee it remains private. The framing — *"I won't seek it out, can't promise I'll never see it"* — is structurally stronger than a clean no-read promise because it avoids the failure mode of incidental exposure creating a "you said you wouldn't read this" moment.
- **Receiving-handoff reflection** when applicable: if the departing party themselves received a handoff at any point, their reflection on what was useful vs. what was missing is high-signal institutional knowledge for the next handoff in the chain.

### Reception Discipline

The arriving party reads the continuity memo *first* — before the formal briefing, before the role docs, before any reconstruction work. This is counter to the common pattern of reading formal docs first and the personal handoff last; the discipline reverses the order because the personal handoff is fresher and more accurate.

## Usage Guidelines

### When to Apply

- AI-agent instance retirements (Chat → Code migrations are the canonical example)
- Role transitions (incoming role-holder taking over an established role)
- Project handoffs (one team handing context to another)
- Long planned absences (multi-week PTO with active threads)
- Any foreseeable seam where the departing party has context the arriving party will need

### When This Pattern Doesn't Apply

- Unforeseeable discontinuities (sudden incapacitation; the pattern's value is the foreseeability)
- Trivial transitions (sessions where the next session will pick up cleanly from session log alone)
- Continuous handoffs with full overlap (where departing and arriving parties work together for a window)

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Write the continuity doc as a postmortem | Information value degrades after the seam closes | Write before the seam, while context is fresh |
| Skip §6 because it feels awkward | The candid section produces the highest-signal content | Use the explicit candor invitation; PM/coordinator's framing matters here |
| Treat the continuity memo as ceremony | Ceremony degrades — gets rushed, then skipped | Treat as the highest-leverage 30–60 min of the departing session |
| Write only what's "appropriate" for formal record | Formal-only framing loses the tacit knowledge | Section 6 or candor sub-sections preserve tacit material with explicit candor invitation |
| Have the arriving party read formal docs before the continuity memo | The personal handoff is fresher; reading order matters | Continuity memo first, formal docs second |

## Related Patterns and Methodologies

- **Pattern-029 (Multi-Agent Coordination)**: continuity memos are one of the durable coordination surfaces this pattern names.
- **Methodology-22 (Roundtable Synthesis)**: complementary — roundtables produce decisions; continuity memos preserve tacit context.
- **Methodology-25 (Workstream Review Cadence)**: weekly workstream memos are continuous-cadence cousins of continuity memos. Both preserve role-scoped institutional knowledge in standing-cadence form.
- **HOST migration checklist Apr 22 (4-phase)**: operational implementation of this pattern at Chat→Code migration scale. Phase 1 ("Before Migration") is the continuity-memo-writing window.
- **Excellence Flywheel v2.0** Practice 3 ("Coordinate Through Structure"): continuity memos are explicit examples of the structural-coordination surface this practice names.

## Evolution

### Origin (Pre-2026, Formalized 2025)
Piper Morgan Docs sessions established the wrap-memo pattern at session-end as standing practice.

### Cross-Project Convergence (March 2026)
Three independent applications of the pattern surfaced in the DinP ecosystem within ~10 days: Piper Docs (recurring), OpenLaws Calliope coffee-spill memo, Klatch Phase 3.5 handoff prompt. The convergence was independent — no coordination across projects.

### Audit Recognition (April 17, 2026)
CIO M1 methodology audit §3.5 recognized the three-project convergence and recommended formalization: *"Strong candidate for Emerging pattern. The three-project convergence is good evidence. File when ready."*

### Operational Validation (April 22–26, 2026)
HOST migration Apr 22 produced the canonical six-section structure that all subsequent Piper Morgan Code-migration handoffs (CIO Apr 23, Comms Apr 23, CXO Apr 25, PPM Apr 25, Architect Apr 26) adopted. The exec review pass during each migration validated the structure as load-bearing — gaps caught with decreasing volume across migrations (HOST 5+1 → CIO 4 → Comms 3+1 → CXO 2 → PPM 3 fixes), evidence the pattern is internalizing.

### Filing (April 27, 2026)
Filed as Emerging pattern under CIO self-approval authority per PM concurrence on M1 audit recommendation B4. Promotion to Proven pending one more cycle of trial application — exec migration is the natural validation event.

## Success Metrics

- **Continuity-memo-first read rate**: arriving party reads the continuity memo before formal briefing material. Should approach 100% if the pattern is internalized.
- **§6 candor rate**: how often does §6 produce content that wasn't in the briefing or formal docs? High §6 rate indicates the candor invitation is working; low rate indicates ceremony has crept back in.
- **Reconstruction-from-artifacts incidents**: cases where arriving party had to reconstruct context that *should* have been in a continuity memo but wasn't. Should trend toward zero.
- **Cross-migration improvement signal**: gaps caught in exec review per migration. Decreasing volume across migrations means the pattern is propagating in production. (HOST 5+1 → PPM 3 across 4 migrations is the visible trend.)

## References

### Origin Material

- **HOST migration handoff (Apr 22, 2026)**: `dev/active/handoff-host-chat-to-code-2026-04-22.md` — the canonical six-section example
- **CIO M1 methodology audit (Apr 17, 2026)**: §3.5 — the audit recognition that produced this filing
- **Klatch Phase 3.5 handoff prompt** (March 2026): cross-project precedent (DinP ecosystem)
- **OpenLaws Calliope coffee-spill memo** (March 2026): cross-project precedent (DinP ecosystem)
- **Piper Morgan Docs session-wrap pattern** (recurring 2025–2026): the originating practice

### Related Documents

- **Methodology-22 (Roundtable Synthesis)**: decisions-vs-context complement
- **Methodology-25 (Workstream Review Cadence)**: standing-cadence cousin
- **HOST migration checklist Apr 22**: operational implementation at migration scale

---

*Pattern created: April 27, 2026*
*Origin: Three-project convergence (Piper Docs / OpenLaws / Klatch), March–April 2026*
*Author: CIO (formalizing cross-project pattern)*
*Status: Emerging (CIO self-approval, PM concurrence)*
*Promotion criterion: one more cycle of trial application across migration events; exec migration is the natural validation event.*
