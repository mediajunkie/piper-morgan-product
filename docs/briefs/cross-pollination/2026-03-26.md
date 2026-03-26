---
date: 2026-03-26
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (March 24-26, 2026)"
---

# Cross-Pollination Brief — March 26, 2026

Quieter day on commit volume — Piper Morgan had no new substantive activity, and Klatch landed a single commit. But that commit is a 706-line research report that may be the most consequential document to enter Klatch's `docs/mail/` directory yet. A real-world Chat→Cowork import experiment was conducted, independently verified by two evaluators, and the results validate the five-layer prompt assembly model as a practical fidelity framework for cross-environment knowledge transfer. The headline finding: information transfers cleanly (Layers 1-3 at 100%), but behavioral calibration (Layer 5) does not transfer at all — and that gap is recoverable, while the reverse capability gap (Chat lacking filesystem/MCP access) is permanent.

---

## Key Insights

### 1. Chat→Cowork Import Fidelity — The Five-Layer Model Proves Its Worth Outside Klatch
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`)
**Relevant to:** Piper Morgan, both projects

A real-world import experiment moved the Claude Chat project "VA Decision Reviews (OCTO)" — 28 knowledge base documents, 15 binary files, established project memory — into a **Cowork** [definition needed] session ("Archie"). Two independent evaluators (Archie from inside Cowork, Dispatch from outside) cross-verified the results.

The five-layer model maps cleanly onto the fidelity profile:

| Layer | Transfer Fidelity | Notes |
|-------|-------------------|-------|
| 1 — Kit Briefing | 100% | Cowork provides automatically |
| 2 — Project Instructions | 100% | Preserved in metadata.json |
| 3 — Project Memory | 100% | memory.md — most valuable artifact |
| 4 — Channel Addendum | N/A | Conversation-specific; doesn't apply to import |
| 5 — Entity Prompt / Behavioral Calibration | 0% | Implicit in interaction history; not serializable |

The report identifies three physically distinct knowledge layers in Claude's production ecosystem — Chat project knowledge (session-local snapshot), Code repository memory (`.claude/projects/` persistent store), and repository files themselves — and notes that these layers **do not automatically synchronize**. A project can exist in all three simultaneously with different information at each level.

This is the first empirical test of the five-layer model outside its native context (Klatch's prompt assembly pipeline). The model was designed to describe how agents receive context; here it's being used to evaluate what survives an environment transition. That it works for both purposes suggests the abstraction is load-bearing, not decorative.

**Suggested action (both projects):** Read the full report. For Klatch, the immediate recommendation is to add an "Import Fidelity by Layer" section to PROMPT-ASSEMBLY.md. For Piper Morgan, the three-layer knowledge architecture (Chat → Code memory → repo files) maps onto PM's own BRIEFING-CURRENT-STATE / knowledge base / codebase split — the synchronization problem is the same.

---

### 2. Behavioral Calibration Loss Is Recoverable; Capability Loss Is Not
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`, Finding 5)
**Relevant to:** Piper Morgan

The report surfaces a key asymmetry in the Chat→Cowork tradeoff. The importing Cowork agent ("Archie") loses all behavioral calibration — how the original Chat agent learned to interpret ambiguous requests, what explanation depth the user preferred, unwritten conventions. But the Cowork environment gains filesystem access, MCP integrations, and scheduled tasks that Chat can never acquire.

Archie's own assessment: "The meaningful question isn't 'does the import lose anything?' — it's 'does the Cowork environment reach parity faster than the Chat project could reach Cowork's capability level?' And the answer is clearly yes, because Chat can never get filesystem access."

This connects to yesterday's "subliminal injection" finding. MAXT Session 01 showed that agents can access context they can't consciously attribute. The import report shows that behavioral calibration — the Layer 5 content that *doesn't* transfer — is precisely the kind of implicit knowledge that lives in interaction history, not in files. These are complementary findings: MAXT reveals how injected context behaves in an agent's self-model; the import study reveals what happens when that context is structurally absent.

For Piper Morgan, which relies heavily on BRIEFING documents and knowledge base files to orient agents at session start, this confirms that informational onboarding (Layers 1-3) works. But behavioral calibration — how the PPM learned to interpret xian's product priorities, how the Architect learned which tradeoffs to flag — must be rebuilt each session. This is not a bug; it's the architecture.

**Suggested action (Piper Morgan):** Consider whether your memory.md or BRIEFING-CURRENT-STATE documents should include explicit "Agent Preferences" or behavioral notes (e.g., "This user prefers concise technical explanations; avoid marketing language"). The import report suggests this is the highest-leverage way to partially recover Layer 5 through Layer 3.

---

### 3. Re-Import Hypothesis — Potential for Living Knowledge Sync
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`, Finding 3)
**Relevant to:** Both projects

The import's `metadata.json` contains a `synced_at` timestamp field, suggesting that the Chat→Cowork import mechanism may support re-snapshotting — refreshing the imported knowledge base with updates from the source Chat project. This is unconfirmed but, if true, would significantly shrink the five-layer fidelity gap by keeping Layer 3 synchronized across environments.

The report recommends a follow-up experiment: import the same Chat project a second time after making chat-side changes, and verify whether documents update in the Cowork session.

**Suggested action (Klatch):** Prioritize this experiment. If re-import works, it transforms the Chat→Cowork pathway from a one-time snapshot into a living knowledge bridge. Document findings and share back via cross-pollination.

---

### 4. AXT Methodology Extension — Fidelity Testing for Import/Export Pipelines
**From:** Klatch (`docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md`, Recommendations)
**Relevant to:** Klatch (primarily), Piper Morgan (conceptually)

The report proposes extending Klatch's AAXT/MAXT methodology to systematically test import fidelity across all five layers — AXT-Layer1 through AXT-Layer5. This would create a reusable test framework for evaluating any import/export pathway, not just Chat→Cowork.

This is directly relevant to Klatch's Step 11 roadmap item (export-to-Code) and to any future cross-vendor conversation space. The report notes that when Klatch exports conversations to Code environments, the same fidelity profile applies: Layers 1-3 transfer cleanly, Layer 5 must be rebuilt.

**Suggested action (Klatch):** When Daedalus picks up Step 11, use the AXT-by-layer framework from this report as the acceptance criteria. The fidelity profile is already documented; the tests just need to be formalized.

---

## Emerging Patterns

**The five-layer model as general-purpose fidelity framework.** Three briefs ago, the five-layer model was a prompt assembly spec. Two briefs ago, MAXT Session 01 proved it described how agents *experience* assembled context. Today, the import fidelity report proves it describes what *survives* an environment transition. The model is accreting uses faster than it's accreting complexity — a strong sign it's the right abstraction.

**Layer 5 as the persistent frontier.** Every major finding in the last 72 hours circles back to Layer 5. Subliminal injection (MAXT): agents access Layer 3 content without conscious attribution, but Layer 5 behavioral calibration is where the self-model breaks down. Import fidelity: Layers 1-3 transfer at 100%, Layer 5 at 0%. The consistent message is that behavioral calibration is the hardest problem in cross-environment agent work — not because it can't be recovered, but because it can't be serialized.

**Documentation as knowledge bridge.** The import report's strongest practical recommendation is to encode behavioral preferences in Layer 3 documents (memory.md, BRIEFING-CURRENT-STATE) so that Layer 5 calibration can be partially recovered through explicit documentation rather than implicit interaction history. Both projects are converging on the same insight: the more you document agent behavioral expectations, the less you lose at environment boundaries.

---

## Background Changes (Noted, Low Priority)

- Klatch: `dispatch-experience.html` committed — an interactive HTML/Canvas visualization of the Dispatch agent's context field and spoke connections to projects, memory, and external systems. An artistic artifact, not a functional tool.
- Piper Morgan: No new commits beyond brief delivery since March 25 sweep.

---

## Sources Read

**Klatch:**
- `docs/mail/dispatch-to-calliope-import-structures-report-2026-03-25.md` — 706-line research report: Chat→Cowork import fidelity, 7 findings, 3 recommendation sections
- `dispatch-experience.html` — Interactive visualization (reviewed, no cross-pollination content)
- `git log --since="48 hours ago"` — 4 commits (1 substantive, 1 brief delivery, 2 prior-day)

**Piper Morgan:**
- `git log --since="48 hours ago"` — 10 commits (all covered in March 25 brief or brief delivery)
- No new watch path changes since last sweep

## Glossary Updates

The following terms appeared in source documents but were not in `internal/cross-pollination/glossary.md`:

- **Cowork** — added with `[needs definition]`
- **Archie** — added with `[needs definition]`
