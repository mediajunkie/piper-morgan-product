# Five-Layer Context Model Mapping — Piper Morgan

**Date**: March 31, 2026
**Author**: Piper Alpha (PA)
**Purpose**: Map Piper Morgan's current context injection against Klatch's five-layer prompt assembly model, for RFC-001 review response to Dispatch
**Status**: Analysis complete; response memo pending

---

## Background

Dispatch (DinP) requested a layer mapping assessment: what does Piper Morgan inject today for each of the five layers, and where are the gaps? This analysis covers both the **agent team** (how 14 agent roles receive context) and the **product** (how Piper Morgan software injects context for end users).

The five-layer model originates from Klatch's `PROMPT-ASSEMBLY.md` and is implemented in `buildSystemPrompt()` in `packages/server/src/claude/client.ts`.

---

## Layer Mapping: Agent Team

### Layer 1 — Kit Briefing (Orientation/Awareness)

**What exists:**
- `.claude/hooks/session-start.sh` — Automatic hook at session initialization providing:
  - Session log continuity check (warns if today's log exists → resume, don't create new)
  - Mailbox check (counts unread messages, lists up to 3 filenames)
  - Briefing freshness check (warns if `BRIEFING-CURRENT-STATE.md` is >7 days old)
  - Role identity reminder ("You are Lead Developer")
- Output kept under 500 characters to avoid token bloat

**Fidelity**: HIGH — Hook runs every session. Filesystem-based checks are reliable.

**Gap**: No equivalent of Klatch's "you're in a different environment now" orientation. Agents don't get told "you lost tool access" or "your context window changed" — they discover it through failure.

---

### Layer 2 — Project Instructions (Project-Level Conventions)

**What exists:**
- `CLAUDE.md` (root, 418 lines) — The primary contract:
  - Role assignment (currently hardcoded to Lead Developer)
  - STOP conditions (10 red flags requiring PM escalation)
  - Core principles (Evidence Required, Completion Discipline, Anti-Sycophancy, Verify First)
  - Progressive loading matrix (what to read based on task)
  - Session discipline (naming, logging, wrapping protocols)
  - API conventions (`/api/v1/` prefix requirement)
  - Subagent deployment patterns
  - Multi-agent coordination protocol
- `knowledge/CLAUDE.md` (165 lines) — Supplementary briefing:
  - Role-based briefing routing (which `BRIEFING-ESSENTIAL-*` to read)
  - Infrastructure verification protocol
  - The 75% Pattern Warning
  - Reporting format template

**Fidelity**: PERFECT — Static markdown committed to git. Survives everything.

**Gap**: Role assignment is hardcoded to Lead Developer in root CLAUDE.md. Other roles (PA, CXO, PPM, etc.) override this by being told their role in the conversation, but the file itself doesn't adapt. PA's briefing document (`BRIEFING-piper-alpha.md`) functions as an override.

---

### Layer 3 — Project Memory (Factual Context That Changes Slowly)

**What exists:**
- `docs/briefing/BRIEFING-CURRENT-STATE.md` — Sprint position tracker (last updated Mar 29):
  - Inchworm position (4.4.2 — M1 Sprint Active, Gate Verification Phase)
  - Recent progress entries (dated)
  - System capability snapshot (19 intent categories, 7 plugins, 63 patterns, 63 ADRs)
  - M1 gate status per gate
  - Metrics snapshot (test counts, session counts, skill counts)
- `docs/briefing/BRIEFING-ESSENTIAL-*.md` — 10 role-specific briefings (~2.5K tokens each):
  - Mission, responsibilities, decision authority
  - Key patterns and anti-patterns for the role
  - Current focus and known challenges
- `config/PIPER.user.md` — The autobiography/personality profile (design fiction, July 2025)
- Live system state via Serena symbolic queries (code inspection)

**Fidelity**: HIGH for static facts. MEDIUM for dynamic state — requires manual refresh. No auto-invalidation when reality changes.

**Gap**: Agent 360 finding: all 9 agents cited briefing staleness as #1 friction. Session-start overhead is 5-15 minutes per role as agents reconstruct "what happened since I was last here." The BRIEFING-CURRENT-STATE file is the best mechanism but goes stale within days during active sprints.

---

### Layer 4 — Channel Addendum (Session/Conversation-Specific Context)

**What exists:**
- **Mailbox system** (`mailboxes/[role]/inbox/`, `read/`, `sent/`):
  - 13 role directories with file-based async messaging
  - Memos delivered by Docs in "sweeps" (every 30-60 min during active hours)
  - `session-start.sh` surfaces unread count at session start
- **Session logs** (`dev/YYYY/MM/DD/` and `dev/active/`):
  - Timestamped per-role-per-day logs
  - Track work completed, decisions made, evidence gathered
  - Handoff notes for session continuity
- **Handoff memos** (`dev/active/`):
  - Role-to-role transition documents during account migrations
  - Include context, carried items, and gotchas
- **Omnibus logs** (`docs/omnibus-logs/`):
  - Daily synthesized records of all sessions
  - Continuous coverage through Mar 28

**Fidelity**: HIGH for async communication (mailbox and session logs persist in filesystem/git). No real-time peer visibility ("what are other agents doing right now").

**Gap**: No "delta since last session" mechanism. Each agent must manually read omnibus logs and mailbox to reconstruct recent context. This is the primary source of the 5-15 minute session-start overhead identified by Agent 360. A structured "what changed since your last session" injection would address this.

---

### Layer 5 — Entity Prompt (Individual Persona/Behavioral Calibration)

**What exists:**
- **Role-specific briefings** (`docs/briefing/BRIEFING-ESSENTIAL-*.md`):
  - Mission statement, decision authority, key patterns
  - Voice and analytical style guidance (particularly CXO)
- **PA briefing** (`docs/briefing/BRIEFING-piper-alpha.md`):
  - Voice rules, colleague test, meta-awareness protocol
  - PM decision frameworks from PAPM predecessor
  - Explicit "what carries from autobiography" vs "what stays in autobiography"
- **Task-specific prompts** (via subagent deployment):
  - Role, task, GitHub issue, acceptance criteria, reporting format
  - Defined in CLAUDE.md subagent section
- **Agent Traditions** (Klatch concept, not yet adopted in PM):
  - Per-agent behavioral calibration documents
  - Working preferences, workflow patterns, communication style

**Fidelity**: MEDIUM — Role briefings and task prompts survive in files. But no "learned personality" — each session, agents rebuild behavioral calibration from briefings. No mechanism to capture "this agent works best when given X context first" or "this agent tends to Y under pressure."

**Gap**: Layer 5 is the open frontier (confirmed by Klatch's import fidelity research: 0% transfer for behavioral calibration). Calliope's externalization pilot in Klatch is the most promising approach. PM has no equivalent — role briefings describe *what to do*, not *how you've learned to work with xian*.

---

## Layer Mapping: Product (Piper Morgan Software)

### Layer 1 — Kit Briefing

**What exists:**
- `config/PIPER.md` — System identity loaded at startup via `piper_config_loader.get_system_prompt()`
- Cached in `app.state` (FastAPI application state)
- Content: "You are Piper Morgan, an AI Product Management Assistant"

**Fidelity**: PERFECT but rigid — loaded once at startup, requires restart to change.

---

### Layer 2 — Project Instructions

**What exists:**
- `services/intent_service/conversational_floor.py` lines 33-65:
  - `FLOOR_SYSTEM_PROMPT_ADDENDUM` — Voice directives, interaction rules, prohibitions
  - "Think through the problem with PM frameworks"
  - "Do NOT introduce yourself or list capabilities"
- ADR-060 architecture: three routing paths (fast-path, action-path, floor-path)
- Warmth guidance (lines 101-114): formality-based tone adjustment (0.0 formal → 1.0 friendly)

**Fidelity**: PERFECT — Embedded in code.

---

### Layer 3 — Project Memory

**What exists:**
- `services/intent_service/context_assembler.py` — Gathers per-intent context:
  - Identity context: capabilities from workflow dispatcher registry, active integrations
  - Trust profile: user's trust stage (NEW → TRUSTED), interaction count
  - Memory context: conversation history summary (last 6 turns), persistent user history
  - Reminder context: due todos/reminders surfaced at greeting
- Database-backed: trust profiles, user preferences, todos/reminders
- Conversation history: last 6 turns formatted as User/Piper pairs

**Fidelity**: HIGH for database-backed data. LOW for conversation history (in-memory only — see Layer 4).

**Gap**: Context assembler only fires for floor-native categories (GUIDANCE, DISCOVERY, TRUST, MEMORY, CONVERSATION, UNKNOWN). Handler-routed categories (STATUS, PRIORITY, TEMPORAL) bypass context assembly entirely — they get raw message without rich context.

---

### Layer 4 — Channel Addendum (Session-Specific Context)

**What exists:**
- `services/intent_service/conversation_context.py`:
  - `_conversation_contexts: dict[str, ConversationContext] = {}` (line 432)
  - 10-turn sliding window, max 30 minutes old
  - Tracks: message, intent, temporal references, entity references, topic, lens
  - Keyed by `(user_id, session_id)`
- ConversationDB exists (database table) but conversation_context.py doesn't read from it for lens stack, last_offer, or turn-by-turn context

**Fidelity**: **CRITICAL GAP** — This is a plain Python dict. It dies on:
  - Server restart
  - Page refresh (new session_id)
  - Process crash
  - No Redis/DB backing implemented
  - Context assembler notes "Cache-ready — design for Redis TTL caching later (not implemented yet)"

**Impact**: User refreshes page mid-conversation → loses "what we were discussing." Multi-turn refinement breaks. Lens stack (topic digression/restoration) resets. Last offer state lost.

---

### Layer 5 — Entity Prompt (User Persona/Calibration)

**What exists:**
- `services/personality/personality_profile.py`:
  - `PersonalityProfile` dataclass: warmth_level, confidence_style, action_orientation, technical_depth
  - `adjust_for_context()` adapts based on intent confidence and response type
  - `get_response_style_guidance()` generates tone directives
- User preferences from database (`users.preferences` JSONB):
  - communication_style, work_style, priority_preferences
  - Loaded per-request by `UserContextService`
- Trust-graduated behavior:
  - Stage 1 (New): respond only
  - Stage 2 (Building): offer capability hints
  - Stage 3 (Established): proactive suggestions
  - Stage 4 (Trusted): anticipate needs

**Fidelity**: PERFECT for database-backed preferences. NO learning — system doesn't update preferences based on observed behavior. Formality baseline loaded but never updated in real-time.

---

## Fidelity Summary

| Layer | Agent Team | Product | Key Gap |
|-------|-----------|---------|---------|
| L1: Kit Briefing | Hook-based, reliable | Config-based, rigid | Agent: no environment-change awareness. Product: no hot-reload. |
| L2: Project Instructions | Static files, perfect | Hardcoded in code, perfect | Agent: role hardcoded to Lead Dev. Product: none. |
| L3: Project Memory | Briefing files + Serena | Database + context assembler | Agent: no auto-invalidation. Product: context assembler skips handler-routed intents. |
| L4: Channel Addendum | Mailbox + session logs, good | **In-memory dict, dies on restart** | Agent: no delta-since-last-session. Product: critical persistence gap. |
| L5: Entity Prompt | Role briefings, medium | DB preferences + personality, good | Agent: no learned calibration. Product: no behavioral learning. |

---

## Key Observations

### What PM Does Well
1. **Layer 2 is exemplary.** The CLAUDE.md + knowledge/CLAUDE.md + progressive loading system is more comprehensive than most projects. The STOP conditions and evidence requirements create genuine behavioral guardrails.
2. **Agent Layer 4 is creative.** The mailbox + session log + omnibus log system is an effective async communication layer built from filesystem primitives. It's manual but reliable.
3. **Product Layer 5 has good bones.** Trust-graduated behavior (ADR-053) is architecturally sound. The four-stage progression with explicit gates is well-designed even if not yet fully implemented.

### What PM Should Address
1. **Product Layer 4 is the critical gap.** In-memory conversation context without persistence breaks multi-turn interaction. This is the single highest-impact improvement for user experience.
2. **Agent session-start overhead** (5-15 min) is a Layer 4 problem — no "delta since last session" injection. A structured "what changed" mechanism would cut this significantly.
3. **Layer 5 has no learning loop** on either side. Agents don't accumulate behavioral calibration across sessions. Users' preferences are static in the database. The Klatch Agent Traditions concept is the most promising approach for the agent side.

### Cross-Project Relevance
- Klatch's Layer 4 also uses in-memory storage (but with Compaction API for long histories)
- Both projects have strong L1-L2-L3 and weak L4-L5
- The five-layer model is validated as an analytical framework — it successfully identifies the same gaps from different angles
- RFC-001 formalization would give both projects a shared vocabulary for discussing context injection improvements

---

## File Manifest

**Agent Team Context Files:**
| File | Layer | Purpose |
|------|-------|---------|
| `.claude/hooks/session-start.sh` | L1 | Session initialization hook |
| `CLAUDE.md` | L2 | Root project instructions |
| `knowledge/CLAUDE.md` | L2 | Supplementary agent briefing |
| `docs/briefing/BRIEFING-CURRENT-STATE.md` | L3 | Sprint position and metrics |
| `docs/briefing/BRIEFING-ESSENTIAL-*.md` (10 files) | L3/L5 | Role-specific memory + persona |
| `docs/briefing/BRIEFING-piper-alpha.md` | L5 | PA-specific behavioral calibration |
| `config/PIPER.user.md` | L5 | Personality profile (autobiography) |
| `mailboxes/[role]/inbox/` | L4 | Async peer-to-peer messaging |
| `dev/YYYY/MM/DD/*-log.md` | L4 | Session continuity logs |
| `docs/omnibus-logs/` | L4 | Daily synthesized records |

**Product Context Files:**
| File | Layer | Purpose |
|------|-------|---------|
| `config/PIPER.md` | L1 | System identity |
| `services/intent_service/conversational_floor.py` | L2/L5 | Voice directives + warmth calibration |
| `services/intent_service/context_assembler.py` | L3 | Per-intent context gathering |
| `services/intent_service/conversation_context.py` | L4 | Session context (IN-MEMORY) |
| `services/personality/personality_profile.py` | L5 | Persona adaptation |
| `services/user_context_service.py` | L3/L5 | User preference loading |
| `web/api/routes/intent.py` | L4 | HTTP boundary, RequestContext creation |
