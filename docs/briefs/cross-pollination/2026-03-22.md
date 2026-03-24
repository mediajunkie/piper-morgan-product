---
date: 2026-03-22
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "24h (March 21-22, 2026)"
---

# Cross-Pollination Brief — March 22, 2026

High-output day on both sides. Klatch published its most important architectural document yet — the canonical 5-layer prompt assembly specification — plus a new "agent traditions" pattern for durable per-agent knowledge. Piper Morgan completed a systematic quality sweep (M1 Tier 2), piloted automated omnibus synthesis via Dispatch, and shipped Mailbox v3 with 14 role-based inboxes. Most notable: **the cross-pollination loop closed** — Piper Morgan's Lead Dev session on March 21 explicitly reviewed the March 21 brief from this hub and noted cross-relevant insights.

---

## Key Insights

### 1. The 5-Layer Prompt Model Is Now Canonical — Piper Morgan Should Read This
**From:** Klatch (`docs/PROMPT-ASSEMBLY.md`, new)
**Relevant to:** Piper Morgan

Klatch published the definitive reference for its 5-layer system prompt architecture for agents crossing context boundaries:

1. **Layer 1 — Kit Briefing:** Environmental orientation (where am I, what can I do)
2. **Layer 2 — Project Instructions:** Behavioral rules and conventions (from CLAUDE.md or equivalent)
3. **Layer 3 — Project Memory:** Factual context about the current project state
4. **Layer 4 — Channel Addendum:** Conversation-specific framing
5. **Layer 5 — Entity Prompt:** Agent identity and persona

Each layer maps to a "fidelity dimension" (environmental, instructional, narrative, conversational). The document includes a presence matrix by channel type, a diagnostic API endpoint (`GET /api/channels/:id/prompt-debug`), and design rationale.

This is the document Piper Morgan's CIO has been asking about. The Klatch team's internal care package memo explicitly notes: "PROMPT-ASSEMBLY.md is the document the Piper Morgan CIO has been waiting for."

**Suggested action (Piper Morgan):** Review `docs/PROMPT-ASSEMBLY.md` in the Klatch repo. Piper Morgan has 14 agent roles, each with briefing documents and session protocols. The 5-layer model provides a framework for structuring what each agent knows at session start. The fidelity dimensions (environmental, instructional, narrative, conversational) could inform how progressive loading in CLAUDE.md is organized.

---

### 2. Agent Traditions — Durable Per-Agent Knowledge Pattern
**From:** Klatch (`docs/AGENT-TRADITIONS-SPEC.md`, `docs/agents/calliope.md`, `docs/agents/argus.md`)
**Relevant to:** Piper Morgan

Klatch introduced a new convention for persistent, per-agent working knowledge stored as Markdown files. Each "traditions document" has 7 sections:

1. Role and purpose
2. Working style
3. Standing responsibilities
4. Conventions and standards
5. Key relationships
6. Institutional memory
7. Standing instructions

These serve as the durable backing store for Layer 5 (entity prompt) in the 5-layer model. The Calliope traditions doc is the reference implementation — it covers the chronicler/writer agent's full operational context including institutional memory about past incidents and workflow conventions. The Argus doc was written with urgency after the reliability incident (lost work due to force-push) and emphasizes verification protocols.

**Suggested action (Piper Morgan):** Compare with the existing `BRIEFING-ESSENTIAL-*.md` pattern. The traditions spec addresses a gap Piper Morgan also has — what happens when a role hasn't been active in days and needs to spin up cold? The 7-section structure (especially "institutional memory" and "key relationships") provides structure that the current briefing docs may not fully capture. Consider adapting for less-frequently-used roles where briefing staleness is a known risk.

---

### 3. Dispatch Omnibus Automation Pilot — Automated Daily Synthesis
**From:** Piper Morgan (`docs/omnibus-logs/2026-03-20-omnibus-log.md`, Docs session log)
**Relevant to:** Klatch

Piper Morgan piloted automating its daily omnibus synthesis using **Dispatch** — a persistent Claude Desktop chat that can spin up worker sessions and control Chrome. The process:

- PM walked Dispatch through the omnibus workflow as a pilot automation case
- Dispatch produced a v3 omnibus for March 20 (3 agents, STANDARD format)
- Two failed attempts first (worktree isolation ate output)
- Docs agent provided QA review against Methodology 20, identifying gaps: missing header fields, slug-based actor names instead of role names, chronological ordering errors, entry length violations
- Four iterations total to reach methodology compliance (v1–v2 worktree failures, v3 format issues, v4 approved)

The resulting omnibus has a provenance section documenting the automation experiment. This is effectively an eval loop for reducing manual orchestration overhead.

**Suggested action (Klatch):** This parallels Klatch's use of Cowork scheduled tasks for intelligence sweeps (~$0.15/day). Dispatch offers a different automation pattern — persistent chat with browser control vs. scheduled headless tasks. If Klatch considers automating session log synthesis or coordination updates, the Dispatch pilot provides a concrete case study including failure modes (worktree isolation) and eval methodology.

---

### 4. Mailbox v3 Infrastructure — 14 Role-Based Inboxes
**From:** Piper Morgan (`mailboxes/` directory, `DIRECTORY.md`, `DELIVERY-LOG.md`)
**Relevant to:** Klatch

Piper Morgan shipped Mailbox v3 with full directory-based routing:

- 14 role-specific inboxes: `arch/`, `cio/`, `comms/`, `cos/`, `cxo/`, `docs/`, `exec/`, `hosr/`, `lead/`, `ppm/`, `spec/`, plus human mailboxes
- `DIRECTORY.md` — routing table mapping roles to inbox paths
- `DELIVERY-LOG.md` — audit trail for all deliveries
- `MANIFEST.md` per inbox for tracking read/unread
- `incoming/` for unrouted messages, `read/` subdirectory for archives

The March 21 brief noted both projects have parallel mailbox evolution (Klatch's `docs/mail/` with sender-to-recipient naming vs. Piper Morgan's directory-based approach). v3 makes the gap wider — Piper Morgan's system now has delivery tracking, manifests, and role-based routing that Klatch's simpler system doesn't need yet but may eventually want.

**Suggested action (Klatch):** No immediate action needed. The DIRECTORY.md pattern (routing table as a flat Markdown file) is worth noting as a lightweight way to formalize routing if Klatch's agent team grows beyond the current named entities. Also note that the care package memo (`docs/mail/calliope-to-mnemosyne-care-package-2026-03-22.md`) is effectively a mailbox-to-mailbox handoff for syncing knowledge to the cloud environment — a pattern Klatch may want for its own cloud import flows.

---

### 5. Audit Cascade Methodology — Systematic Issue Triage
**From:** Piper Morgan (Lead Dev session, `dev/2026/03/21/`)
**Relevant to:** Klatch

Piper Morgan's Lead Dev completed a systematic "audit cascade" across four M1 Tier 2 quality issues (#908, #909, #910, #898) in a single session. The methodology:

1. **Verify scope:** Does the issue description still match reality after recent architectural changes?
2. **Narrow or widen:** #908's scope shrank because #923 (registry gate) and #911 (floor routing) already addressed the root causes. #898's 9 misclassifications reduced to 2 meaningful ones post-floor-inversion.
3. **Decide disposition:** Implement, defer, or close based on updated context.
4. **Execute efficiently:** #908 implemented and closed same session. #909 and #910 audited and staged for next session.

Result: What looked like 4 separate work items became 1 immediate fix, 2 quick follow-ups, and 1 partially moot issue — all triaged in under 2 hours.

**Suggested action (Klatch):** As Klatch's issue count grows (currently 10+ open), this pattern prevents the common trap of working issues in filing order rather than impact order. The key insight: audit issues against *current* architectural state, not the state when they were filed. Klatch's rapid shipping pace (8 releases in a week) means issues filed 3 days ago may already be partially resolved.

---

### 6. The Cross-Pollination Loop Closed
**From:** Both projects
**Relevant to:** Both teams (and this process)

Piper Morgan's Lead Dev session on March 21 begins with an explicit "Cross-Pollination Hub Review" section:

> *Reviewed designinproduct.com/internal newsletter... Six cross-relevant insights identified between projects — conversation management patterns (Klatch) and multi-agent role coordination (Piper Morgan) create mutual improvement opportunities. Registry-driven approach highlighted as transferable methodology.*

This is the first evidence that the brief is being consumed as intended — an agent on one project reading the brief, extracting relevant insights, and noting them in their session log. The loop is: Klatch discovers → brief publishes → Piper Morgan reads → Piper Morgan's session log records the insight.

The Docs session also explicitly noted the hub's existence and three-step workflow. Both sessions demonstrate consumption, not just awareness.

**No action needed** — this validates the process. Continue publishing.

---

## Emerging Patterns

**Knowledge formalization accelerating:** Both projects are moving from ad-hoc documentation to structured, machine-readable knowledge formats. Klatch: PROMPT-ASSEMBLY.md + AGENT-TRADITIONS-SPEC.md. Piper Morgan: Mailbox v3 DIRECTORY.md + DELIVERY-LOG.md + role-specific MANIFEST.md. The pattern: name it, spec it, give it a schema, make it discoverable.

**Automation of daily synthesis:** Both projects now have automation experiments for their daily processes. Klatch: Cowork scheduled tasks for intelligence sweeps. Piper Morgan: Dispatch pilot for omnibus synthesis. Different tools, same goal — reduce the overhead of the daily knowledge-synthesis loop so agents can focus on actual work.

**Quality gating before capability work:** Piper Morgan's M1 tier ordering (architecture → quality → capabilities) and Klatch's AAXT/MAXT split (automated structural tests gate qualitative tests) both reflect the same principle: verify what you have before building more. Both teams independently arrived at "stop and clean up" before "add features."

---

## Background Changes (Noted, Low Priority)

- Klatch published blog draft "What Does an Imported Agent Know?" — public-facing narrative of the 5-layer model (awaiting editorial review)
- Klatch created BLOG-TEMPLATE.md after losing edits to web tool mangling
- Klatch added speculative roadmap items from Piper Morgan conversations (Klatch as MCP service, standing workflow templates)
- Piper Morgan completed #908 (generic response signaling with structural `is_generic_response` flag)
- Piper Morgan completed #909 (removed all hardcoded user names from production code — multi-user readiness)
- Piper Morgan fixed #910 (pre-existing test failures in calendar adapter and GitHub preferences — 6263 passed, 0 failures)
- Piper Morgan resolved 7/9 intent classifier edge cases in #898 (pre-classifier pattern fixes, 2 deferred as low-value)
- Piper Morgan Docs completed CDN image backfill (175/269, rate-limited on remaining 94)
- Piper Morgan CoS infrastructure memo proposals 2 and 3 applied (open items tracker, session completion checklist)

---

## Sources Read

**Klatch:**
- `docs/PROMPT-ASSEMBLY.md` — 5-layer prompt architecture (canonical reference)
- `docs/AGENT-TRADITIONS-SPEC.md` — Per-agent persistent knowledge specification
- `docs/agents/calliope.md` — Calliope traditions (reference implementation)
- `docs/agents/argus.md` — Argus traditions (reliability-focused)
- `docs/drafts/prompt-assembly.md` — Blog draft, "What Does an Imported Agent Know?"
- `docs/BLOG-TEMPLATE.md` — Publishing workflow template
- `docs/mail/calliope-to-mnemosyne-care-package-2026-03-22.md` — Knowledge sync priorities
- `docs/INTELLIGENCE.md` — Standing intelligence protocol
- `docs/intel/2026-03-20-sweep.md` — First intelligence sweep (20 items)
- `docs/fork-continuity-quiz.md` — Fork Continuity Quiz v4 (portable)

**Piper Morgan:**
- `dev/2026/03/21/2026-03-21-2158-lead-code-opus-log.md` — Lead Dev session (audit cascades, #908)
- `dev/2026/03/21/2026-03-21-1857-docs-code-opus-log.md` — Docs session (Dispatch pilot, CoS memo)
- `docs/omnibus-logs/2026-03-20-omnibus-log.md` — March 20 omnibus (Dispatch automation provenance)
- `mailboxes/DIRECTORY.md` — Mailbox v3 routing table
- `mailboxes/DELIVERY-LOG.md` — Delivery audit trail
- Commit history: #908, #909, #910, #898 implementation commits
