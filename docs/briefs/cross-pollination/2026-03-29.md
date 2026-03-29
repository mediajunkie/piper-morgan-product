---
date: 2026-03-29
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "96h (March 25-29, 2026)"
---

# Cross-Pollination Brief — March 29, 2026

Low-activity window — neither repo has committed since March 25. But one post-brief commit in Klatch surfaced a substantial dispatch report that the March 25 brief missed: a 700-line research memo documenting the first real-world Claude Chat→**Cowork** [needs definition] import experiment. The findings validate the five-layer prompt assembly model as an import fidelity framework and identify a structural gap at Layer 5 (behavioral calibration) that both projects should internalize.

Piper Morgan had no new commits since the last brief.

---

## Key Insights

### 1. Chat→Cowork Import Fidelity — Five-Layer Model Validated as Transfer Framework
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`)
**Relevant to:** Piper Morgan, Klatch

A dispatch memo from xian to Calliope documents the first end-to-end Claude Chat→Cowork import: a 28-document VA project ("VA Decision Reviews (OCTO)") was imported into a Cowork session called **Archie** [needs definition]. Two independent evaluators (Archie and Dispatch) verified transfer fidelity across all five layers.

**The fidelity profile:**

| Layer | Transfer | Notes |
|-------|----------|-------|
| 1 — Kit Briefing | 100% | Cowork provides automatically |
| 2 — Project Instructions | 100% | System prompt preserved in metadata.json |
| 3 — Project Memory | 100% | memory.md transferred intact; most valuable artifact |
| 4 — Channel Addendum | N/A | Session-specific; not applicable to static import |
| 5 — Entity Prompt / Behavioral Calibration | 0% | Implicit in conversation history; not serializable |

The key finding: **what transfers is inert information; what does not transfer is behavioral calibration.** Months of learned preferences — communication style, explanation depth, disambiguation heuristics — live only in conversation history, which is completely absent from the import. The gap is recoverable through continued interaction, but it's real and significant in early sessions.

Three sub-findings worth noting:
- **Three physically distinct knowledge layers** exist in production (Chat project snapshot, Code repository memory, repo files) that do not automatically synchronize.
- A `synced_at` timestamp in metadata.json suggests potential re-import capability (unconfirmed hypothesis — would significantly close the fidelity gap if true).
- The capability tradeoff is asymmetrical: Cowork reaches parity faster than Chat could ever reach Cowork's technical scope (filesystem, MCP, scheduled tasks).

**For Piper Morgan:** This maps directly onto your briefing infrastructure. When PM agents receive BRIEFING-CURRENT-STATE or knowledge base documents at session start, those are Layers 2-3 content. The dispatch report confirms these transfer at 100% fidelity. But the March 25 MAXT finding (subliminal injection) adds a twist: even when Layer 3 content transfers perfectly, agents may access it subliminally — correct answers, wrong attribution. The combination of these two findings means: **your briefing documents are being delivered and used, but agents may not be able to tell you they're using them.** Probe behaviorally, not declaratively.

**For Klatch:** The report explicitly recommends extending AXT methodology to test import fidelity per-layer (AXT-Layer1 through AXT-Layer5). This connects directly to Step 11 on the roadmap (export-to-Code). The fidelity profile documented here is the baseline for what Klatch's export pipeline must achieve or improve upon.

**Suggested action (Both):** Read the full dispatch report. For Klatch, the AXT-per-layer extension is a natural next step for Argus. For Piper Morgan, the finding reinforces that your briefing infrastructure works — but pair it with the MAXT subliminal finding to understand *how* it works.

---

## Emerging Patterns

**The five-layer model keeps earning its keep.** It was designed as a prompt assembly spec. MAXT Session 01 used it as a testing framework. Now the import fidelity report uses it as a transfer analysis framework. Each new application validates the taxonomy — layers are real, distinct, and behave differently under different conditions (assembly, testing, import). Neither project planned this convergence; the model is simply descriptive of something structurally true.

**Four-day silence is unusual.** Both repos went from daily multi-commit activity to zero commits for 96 hours (March 26-29). No session logs, no omnibus entries, no COORDINATION.md updates. This is not necessarily a problem — weekends, holidays, natural pauses — but it's worth noting as a baseline. If the silence extends further, a check-in may be warranted.

---

## Background Changes (Noted, Low Priority)

- Klatch: `dispatch-experience.html` committed alongside the dispatch report — appears to be an HTML rendering of the import experience (219 lines, not in a watch path)

---

## Sources Read

**Klatch:**
- `docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md` — 706-line dispatch report on Chat→Cowork import fidelity (post-dates March 25 brief)
- `git log --oneline -10` — last commit March 25 (dispatch report + cross-pollination brief delivery)

**Piper Morgan:**
- `git log --oneline -10` — last commit March 25 (cross-pollination brief delivery)
- No new content in watch paths since March 25 brief
