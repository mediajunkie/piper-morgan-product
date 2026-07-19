# Design Record — Multi-Agent Coordination (PM-033d era)

**Status**: code deleted 2026-07-18 (#1436 Tier-3 Family 2, Arch-ruled); thinking preserved here.
**What it was**: a 2025-era orchestration subsystem (`services/orchestration/`) that never reached
production wiring (its API package was broken at import; zero live callers at deletion).

## The ideas worth keeping
1. **Typed agents by strength** — `AgentType.{CODE, CURSOR, COORDINATOR}`: route work by what an
   agent is *good at* (infrastructure/backend vs testing/UI/polish vs pure coordination), not
   round-robin. The cohort's current role system (Lead/Arch/PPM/CXO/…) is this idea, matured.
2. **Complexity-driven decomposition** — `TaskComplexity.{SIMPLE(<30min, 1 agent), …}` gating
   whether a task decomposes at all and how parallel it goes. Today's equivalent: the
   quality-banking / drain-it-all boundary and census-style parallel fan-out.
3. **Chain-of-Draft** — a 2-draft compare-and-learn loop (draft → systematic comparison →
   quality-delta learning) for coordination outputs. Ancestor of judge-panel / adversarial-verify
   patterns the cohort now uses via subagents.
4. **Excellence-Flywheel enforcement in the coordinator** — methodology compliance as a
   coordinator responsibility, not per-agent vigilance. Survives as CLAUDE.md + skills + ratchets.

## Why it was deleted rather than finished
The live cohort implements every idea above through different, working machinery (roles + duty
cycles + Task-tool subagents + skills + CI ratchets). The subsystem's remaining value was the
record of intent — this page. `api/orchestration/__init__.py` imported a class that never
existed (`MultiAgentAPI`), so nothing could ever have loaded it; the island's only inbound edge
was a lazy chain-of-draft import in `query_learning_loop`, now an honest removed-feature reply.

*Extracted per Arch's Family-2 ruling ("if there's real thinking, park a design record").*
