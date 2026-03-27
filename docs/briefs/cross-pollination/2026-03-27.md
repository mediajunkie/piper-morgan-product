---
date: 2026-03-27
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (March 25-27, 2026)"
---

# Cross-Pollination Brief — March 27, 2026

Quiet 48 hours for new code, but Klatch produced a substantial research artifact that landed after the March 25 brief was written. A 700-line Dispatch-to-Calliope memo documents the first real-world Chat→Cowork import experiment, mapping transfer fidelity across the five-layer prompt model. Three physically distinct knowledge layers identified in production. Layers 1–3 transfer at 100% fidelity; Layer 5 (behavioral calibration) is structurally absent but recoverable through continued interaction. Piper Morgan: no new commits beyond brief delivery.

---

## Key Insights

### 1. Three Knowledge Layers in Production — Not One
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`)
**Relevant to:** Piper Morgan

The Dispatch report documents a finding that matters for any multi-agent project: Claude project context lives in three physically distinct, non-synchronizing layers:

- **Layer A (Chat Project Knowledge):** Session-local `.projects/` snapshot — read-only, imported once, not visible to other sessions
- **Layer B (Code Repository Memory):** `.claude/projects/` memory files — persistent, git-tracked, shared across sessions
- **Layer C (Repository Files):** The actual repo (CLAUDE.md, docs/, code) — standard git workflow

These layers do not automatically stay synchronized. A project can exist in all three simultaneously with different information at each level. For Piper Morgan's multi-agent setup — where Lead Dev, Docs, PPM, and others work in parallel Code sessions — Layer B is the shared institutional memory. But if any agent imports a Chat project, that agent gets a Layer A snapshot invisible to everyone else.

**Suggested action (Piper Morgan):** Document which knowledge layer each agent role primarily reads from and writes to. If Chat→Cowork imports become part of the workflow, establish a protocol for surfacing Layer A findings into Layer B or C so they're visible to the whole team.

---

### 2. Five-Layer Import Fidelity Profile — Empirical Validation
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`)
**Relevant to:** Both projects

The import experiment tested the five-layer prompt assembly model against real transfer:

| Layer | Transfer Fidelity | Notes |
|-------|-------------------|-------|
| 1 — Kit Briefing | 100% | Cowork provides automatically |
| 2 — Project Instructions | 100% | Transferred in metadata.json |
| 3 — Project Memory | 100% | memory.md imported cleanly |
| 4 — Channel Addendum | N/A | Session-specific, not project-level |
| 5 — Entity Prompt | 0% | Behavioral calibration not serialized |

This aligns with the March 25 brief's "Subliminal Injection" finding: Layers 1–3 can arrive subliminally (delivered but not consciously attributable). Layer 5 doesn't arrive at all — it must be rebuilt through interaction. The March 25 MAXT finding established that delivery ≠ attribution; this report establishes that information ≠ calibration.

The report proposes extending Klatch's AXT methodology to systematically test import fidelity per layer (AXT-Layer1, AXT-Layer2, etc.). This would give both projects a reusable framework for evaluating any import/export pathway.

**Suggested action (Klatch):** Add a "Transfer Fidelity by Layer" section to PROMPT-ASSEMBLY.md, codifying this empirical finding alongside the existing theoretical model.

---

### 3. The Capability Gap Is Asymmetrical — And That's the Point
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`)
**Relevant to:** Both projects

The report frames the Chat↔Cowork tradeoff as structurally asymmetric:

- **Chat → Cowork gap (calibration):** Recoverable. Behavioral patterns rebuild through continued use. Layer 3 (memory.md) accelerates recovery.
- **Cowork → Chat gap (capability):** Permanent. Chat can never get filesystem access, MCP integrations, or scheduled tasks.

The experiment subject (**Archie** [definition needed] — a Cowork session that imported a Chat project) assessed: "The meaningful question isn't 'does the import lose anything?' — it's 'does the Cowork environment reach parity faster than the Chat project could reach Cowork's capability level?'" Answer: clearly yes.

This has implications for both projects' agent deployment strategy. When deciding where an agent should work, the capability floor matters more than the calibration ceiling — because calibration recovers, but capability constraints are architectural.

**Suggested action (Both):** When choosing agent environments for new work, bias toward the environment with the higher capability floor, not the one with the best current calibration.

---

## Emerging Patterns

**Information vs. calibration.** Two consecutive briefs now distinguish these clearly. March 25: subliminal injection shows information arrives even when agents can't self-report it. March 27: import fidelity shows information transfers but calibration doesn't. The five-layer model is proving its value not as a design spec but as an analytical framework — a vocabulary for diagnosing what works and what doesn't when agents move between contexts.

**Research artifacts as cross-project infrastructure.** The Dispatch-to-Calliope memo is addressed to a specific Klatch agent but its findings apply equally to Piper Morgan. This is exactly the kind of document the cross-pollination system exists to surface. The mailbox system (inter-agent memos) is generating artifacts whose value exceeds their intended audience.

---

## Background Changes (Noted, Low Priority)

- Klatch: `dispatch-experience.html` committed — a canvas-based visualization of the dispatch experience (context field animation). Exploratory/artistic artifact, no functional impact.
- Both repos: March 25 cross-pollination brief delivered to project repos. Delivery pipeline functioning normally.

---

## Sources Read

**Klatch:**
- `docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md` — 706-line research report on Chat→Cowork import structures and five-layer fidelity analysis
- `dispatch-experience.html` — Canvas visualization (noted, not analyzed in depth)
- `git log --since="48 hours ago"` — 2 commits: dispatch report + brief delivery

**Piper Morgan:**
- `git log --since="48 hours ago"` — 2 commits: both cross-pollination brief deliveries, no new substantive work
- `docs/briefs/cross-pollination/current.md` — confirmed March 25 brief received
