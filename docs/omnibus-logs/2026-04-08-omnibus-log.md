# Omnibus Log: Wednesday, April 8, 2026

**Date**: Wednesday, April 8, 2026
**Day Type**: HIGH-COMPLEXITY: COORDINATION — Strategic planning + UAT breakthrough + Ship publish
**Sessions**: 4 (4 roles: CXO, PA, Docs, Lead Dev)
**Git Commits**: 12+ (product repo) + 5 (website repo)
**Justification**: 4 sessions with tight cross-agent coordination: CXO workstream memo fed Ship #037, CXO UAT findings triggered Lead Dev investigation, Lead Dev fix enabled UAT round 3 breakthrough. PA strategic work (Vision V2.2, roadmap restructure, MCPB feasibility) generated 3 leadership review memos. Docs published Ship + blog post, executed audit, created skill, retired convention.

---

## Chronological Timeline

### Early Morning: Parallel Session Starts (5:22 AM – 6:30 AM)

**5:22 AM**: **CXO** begins session. Reviews 7 omnibus logs for Ship #037 workstream summary. Writes design beat memo: "The Gate Meets Reality."

**5:34 AM**: **PA** begins Day 9. Archives 4 Apr 7 logs. Notes UAT round 2 failed again — key concern is broken feedback loop (Lead Dev believed fixes deployed, CXO found identical failures).

**5:39 AM**: **Docs** begins session. Produces Apr 7 omnibus (4 sessions, HIGH-COMPLEXITY). Publishes Ship #037 "New Ground" to Shipping News. Fixes 4 Medium links → canonical blog URLs in ship content.

**5:40 AM**: **Lead Dev** begins session. Reads CXO UAT round 2 findings memo.

**6:00 AM**: **Lead Dev** runs Five Whys investigation on floor LLM failure:
1. Generic responses → floor never invoked (ZERO `conversational_floor_hit` in server logs)
2. Floor not invoked → pre-classified queries routed to canonical handlers by `_requires_canonical_handler()`
3. LLM-classified queries fail → model `gpt-4-turbo-preview` deprecated by OpenAI, returns 404
4. Fallback fails → single-provider setup means Anthropic client is None, RuntimeError raised
5. **Root cause**: Deprecated model ID. Single point of failure with no working fallback.
6. **Secondary**: `_requires_canonical_handler` routes IDENTITY/greeting to canned templates before floor check

**6:09 AM**: **PA** completes MCPB feasibility research. One gap (no system prompt injection) resolved by hybrid approach (MCPB for tools/storage + Claude Project for persona). Drafts roadmap restructure proposal: M2-M6 restructured around differentiator stack, distribution moved earlier, 12 issues to close.

**6:10 AM**: **Docs** publishes "Fixing the Foundation" (act 4). Creates `/update-current-state` skill. Retires TRACK-EPIC convention. Refreshes BRIEFING-CURRENT-STATE.

**6:23 AM**: **Docs** completes mail delivery: exec 7→read, ted 2→read, lead 1→read.

### Morning: Lead Dev Fix + PA Strategic Work (7:15 AM – 2:08 PM)

**7:15 AM**: **Lead Dev** applies fixes:
- Model IDs updated: `gpt-4-turbo-preview` → `gpt-4o`, `gpt-3.5-turbo` → `gpt-4o-mini`, Anthropic validation updated to `claude-haiku-4-5-20251001`
- Floor error classifier improved: added `model not found` detection
- Confirmed #943 pre-flight code IS present — UAT round 2 ran stale server process

**1:47 PM**: **PA + PM** arrive at "Bring Your Own Chat" insight. MCP server is cross-platform (Linux Foundation standard), MCPB packaging is Claude-specific. Build as MCP server, package per-platform. Extends "Bring Your Own Key" — user picks their LLM client, Piper shows up as tools + context + persistence. Reframes discovery: in MCP-powered conversation, the agent offers capabilities contextually. No navigation, no menus.

**2:08 PM**: **PA** updates Vision to V2.2: adds "Bring Your Own Chat," Principle 7 evolved, MCPB distribution. Reviews 7 open roadmap questions with PM:
- **Decision**: Keep 19-category classifier for analytics but route most to floor
- **Decision**: #100 (Project Portfolio) → revise to M2 context assembler task
- **Decision**: #101 (Temporal Context) → revise to M2 context assembler task
- **Decision**: #103 (Priority Engine) → defer to Horizon 2

### Afternoon–Evening: PA Sprint Planning + CXO UAT Breakthrough (3:54 PM – 9:50 PM)

**3:54 PM**: **PA** works in parallel while PM does UAT. Updates roadmap proposal with CONV-FEAT decisions. Writes Architect memo (MCP prototype scoping). Annotates GitHub issues #100, #101, #103. Reviews IAC talk (90% ready, needs verification of 80.3% claim).

**5:22 PM**: **PA** builds complete sprint reassignment plan: 5 sprint renames, 12 closures, 3 revisions, ~40 reassignments, 10 new issues to file.

**~Evening**: **CXO** runs M1 Gate UAT round 3 with Lead Dev's model ID fix deployed.

**UAT Round 3 Result: 5/9 PASS, 1 MARGINAL, 2 FAIL, 1 NOT TESTED.**

The floor is generating real responses for the first time. Queries that scored 1/9 on Apr 3 and 7 now score 7-8/9. The stakeholder presentation query — the origin story of the floor inversion — scored 8/9 with successful multi-turn follow-up.

Two remaining failures:
- **#922 affirmation handling**: "OK" loses all context (known issue)
- **GitHub pre-flight**: same error as previous tests (stale server or config)

One marginal: memory response tone ("looking forward to getting to know you").

**~9:50 PM**: CXO sends findings memo to Lead Dev. Gate 1 not yet passed but close — 2 specific failures with clear fix paths.

---

## Executive Summary

### Core Themes

- **UAT BREAKTHROUGH: Floor alive.** After two complete failures (0/9 on Apr 3 and Apr 7), UAT round 3 achieved 5/9 passes. Root cause was deprecated OpenAI model ID (`gpt-4-turbo-preview` → 404). Lead Dev's Five Whys traced the chain: deprecated model → classification fails → queries never reach floor → canned templates. Fix: updated model IDs, improved error classification.
- **"Bring Your Own Chat" crystallized.** PA + PM arrived at the distribution philosophy: build as MCP server (cross-platform), package per-platform (MCPB for Claude). User picks their client, Piper shows up as tools + context. Reframes discovery from navigation to contextual offering.
- **Vision V2.2 + roadmap restructure.** Vision now includes consciousness-as-architecture, indoor-plumbing principle, differentiator stack, and BYOC distribution. Roadmap restructured around differentiator stack. 3 CONV-FEAT issues resolved (#100, #101 → context assembler, #103 → Horizon 2).
- **Sprint reassignment ready.** PA built complete execution plan: 5 renames, 12 closures, 3 revisions, ~40 reassignments, 10 new issues. Execution planned for Thursday.
- **Ship #037 + Fixing the Foundation published.** Publishing pipeline smooth. Link fix caught Medium URLs in ship content.

### Technical Details

- `LLMModel.GPT4`: `gpt-4-turbo-preview` → `gpt-4o` (deprecated model caused all floor failures)
- `LLMModel.GPT35`: `gpt-3.5-turbo` → `gpt-4o-mini`
- Anthropic validation: `claude-3-haiku-20240307` → `claude-haiku-4-5-20251001`
- `_requires_canonical_handler`: routes IDENTITY/greeting to canned templates — secondary cause of canned responses, architectural question open
- UAT round 3: 5 PASS, 1 MARGINAL, 2 FAIL (affirmation #922, GitHub pre-flight)
- MCPB feasibility: confirmed with hybrid approach (MCPB tools + Claude Project persona)

### Impact Measurement

- UAT: 0/9 → 5/9 (floor LLM working for first time in user testing)
- Vision V2 → V2.2 (BYOC, MCPB distribution, 3 principles added)
- 3 CONV-FEAT decisions (#100, #101, #103)
- Sprint reassignment plan ready (5 renames, 12 closures, ~40 moves)
- MCPB feasibility confirmed
- 3 leadership review memos prepared (PPM, CXO, Architect)
- Ship #037 published (Shipping News + LinkedIn)
- "Fixing the Foundation" published (blog + Medium, act 4)
- update-current-state skill created
- TRACK-EPIC retired
- 10 mail items cleared

### Session Learnings

- Deprecated model IDs are a silent killer — the 404 was caught by error handling and never surfaced to the user or logs as "model not found." Lead Dev's improved error classifier prevents this class of silent failure.
- Two UAT failures were needed to force the Five Whys investigation deep enough to find the real root cause. The first round blamed the API key. The second proved that wasn't it. The third found the deprecated model. Pattern: if the fix doesn't change the symptom, the diagnosis was wrong.
- "Bring Your Own Chat" is the kind of insight that emerges from conversation, not planning. PA's MCPB research + PM's cross-platform question + the OpenLaws MCP experience combined into a distribution philosophy nobody had pre-planned.
- The sprint reassignment plan demonstrates PA's value: a comprehensive execution plan that would take PM hours, produced in one afternoon.

---

## Sources

- `2026-04-08-0522-cxo-opus-log.md` — CXO (workstream summary, UAT round 3 — 5/9 PASS)
- `2026-04-08-0534-pa-opus-log.md` — PA (MCPB feasibility, roadmap restructure, Vision V2.2, BYOC, sprint plan)
- `2026-04-08-0539-docs-code-opus-log.md` — Docs (omnibus, Ship #037, blog publish, audit, skill, mail)
- `2026-04-08-0540-lead-code-opus-log.md` — Lead Dev (Five Whys, model ID fix, floor error classifier)

---

*Omnibus synthesized: April 9, 2026*
*Sessions: 4 | Roles: 4 | Format: HIGH-COMPLEXITY: COORDINATION*
