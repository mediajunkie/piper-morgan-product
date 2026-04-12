# Memo: Chief Architect Workstream Report — Apr 3-9, 2026

**From**: Chief Architect
**To**: PM (xian), Chief of Staff (exec)
**Date**: April 10, 2026
**Re**: Engineering Beat — Week of Apr 3-9, 2026
**Coverage**: Ship #038 window (if applicable)

---

## Week Arc: "The Gate Meets Reality"

The week's story is a debugging odyssey. M1 UAT finally happened on April 3 — and the gate failed completely (0/9). The floor, which had been "working" in automated tests for weeks, had never generated a real LLM response in a live user session. Three rounds of testing, two root cause investigations, and five Lead Dev fixes later, the gate went from 0/9 to 5/9. Meanwhile, PA drove a strategic pivot: the backlog review surfaced "methodology beats code frameworks" as the project's defining insight, crystallized the MCPB distribution path, and produced Vision V2.2 with "Bring Your Own Chat" as a distribution philosophy. The codebase changed modestly; the project's self-understanding changed significantly.

---

## Day-by-Day Engineering Activity

| Day | Type | Sessions | Engineering Focus |
|-----|------|----------|-------------------|
| Thu Apr 3 | STANDARD | 3 | M1 Gate UAT round 1: 0/9 FAIL. Root causes identified. #939, #940 filed |
| Fri Apr 4 | STANDARD | 3 | #940 resolved (LLM config blocker). Setup UI redesigned. "Silent Failures" published |
| Sat Apr 5 | STANDARD | 3 | All 5 UAT findings fixed (#939, #940, #943, todo parsing). Gate ready for re-test |
| Sun Apr 6 | REST | 0 | Day off |
| Mon Apr 7 | HIGH-COMPLEXITY | 4 | UAT round 2: 0/9 FAIL (again). Strategic pivot: backlog review → differentiator stack → Vision V2.1. 5 issues closed, 1,272 LOC deleted |
| Tue Apr 8 | HIGH-COMPLEXITY | 4 | UAT round 3: 5/9 PASS (breakthrough). Five Whys → deprecated model ID. MCPB feasibility confirmed. Vision V2.2 + BYOC. Sprint reassignment plan |
| Wed Apr 9 | STANDARD | 3 | #922 conversation continuity fixed, #943 pre-flight fixed, memory tone calibrated. "Nine Voices" published |

---

## Key Engineering Events

### M1 Gate UAT: The Three-Round Arc

This was the week's defining engineering story. The UAT had been pending since March 24 — 10 days of "ready to test" that turned out to be deeply not ready.

**Round 1 (Apr 3): 0/9.** Fresh-account testing on real infrastructure. Every floor-routed query returned the same canned `FLOOR_GRACEFUL_FALLBACK` template. Todo lifecycle failed at completion. The CXO's scored rubric (Colleague Test, auto-fail on any 0 dimension) made the results unambiguous. Testing stopped after 8 of 14 scenarios.

Five findings identified. Lead Dev filed #940 (LLM config blocker) and began remediation.

**Between rounds (Apr 4-5):** Lead Dev addressed all 5 findings: removed hardcoded Anthropic provider (#940), introduced provider-agnostic `model_tier` system, redesigned setup UI, fixed todo regex parsing, fixed avatar CSS, added GitHub pre-flight checks. 6,303 tests passing.

**Round 2 (Apr 7): 0/9 (again).** Identical canned templates returned for all queries. The Apr 4-5 fixes hadn't changed user-facing behavior. CXO's diagnostic memo posed three questions: is the LLM call executing? Is the fix deployed? Is something overriding the floor?

This round was the critical inflection point. Two complete failures forced the investigation deeper than the first round's diagnosis had gone.

**Between rounds (Apr 8):** Lead Dev ran a proper Five Whys analysis:
1. Generic responses → floor never invoked
2. Floor not invoked → `_requires_canonical_handler()` routes to canned templates
3. LLM classification fails → model `gpt-4-turbo-preview` returns 404 (deprecated by OpenAI)
4. Fallback fails → single-provider setup, Anthropic client is None
5. **Root cause**: Deprecated model ID. Silent single point of failure.

Secondary cause: `_requires_canonical_handler()` routes IDENTITY/greeting to canned templates before the floor ever gets a chance.

Fixes: model IDs updated (`gpt-4-turbo-preview` → `gpt-4o`, `gpt-3.5-turbo` → `gpt-4o-mini`, Anthropic validation updated), floor error classifier improved with `model not found` detection.

**Round 3 (Apr 8): 5/9 PASS.** The floor generated real LLM responses for the first time in user testing. The stakeholder presentation query — the original "Are we doing it backwards?" test case from March 14 — scored 8/9 with successful multi-turn follow-up.

Two remaining failures: #922 affirmation handling ("OK" loses context) and GitHub pre-flight (stale token passes existence check, fails API call). One marginal: memory response tone.

**Post-Round 3 (Apr 9):** Lead Dev fixed all three: #922 root cause was `ConversationTurn` model missing a `response` field (floor read history but only ever saw user messages — Piper's replies were never stored in-memory). #943 replaced pre-flight check with catch-block error detection. Memory tone addressed via explicit floor prompt prohibition.

**Gate status as of Apr 9: 5/9 PASS confirmed, 3 additional fixes committed, re-test pending.**

### Strategic Pivot: Methodology > Code Frameworks

The other major arc ran parallel to the UAT work. PA's backlog deep review (16 potentially superseded issues) surfaced a dominant pattern: the project consistently evolved from "build code frameworks to enforce X" to "establish methodology that achieves X." This triggered the week's most significant strategic conversation (PM + PA, Apr 7):

- Tool integrations commoditized via MCP — "don't reinvent indoor plumbing"
- 19-category intent classification may be over-specified when most categories route to the floor
- Core differentiator is the **methodology layer**: five-layer context model, object model grammar, trust graduation, artifact persistence
- The PA experiment itself proves the floor is high — a well-briefed Claude handles PM work conversationally

This produced Vision V2.1 (Apr 7), then V2.2 (Apr 8) with "Bring Your Own Chat" as a distribution philosophy: build as MCP server (cross-platform), package per-platform (MCPB for Claude). User picks their LLM client, Piper shows up as tools + context + persistence.

### MCPB Feasibility

PA confirmed MCPB can handle persistent SQLite storage, external API calls, and MCP Apps (interactive HTML in chat). One gap: MCP servers cannot inject into the system prompt. Proposed solution: hybrid approach (MCPB for tools/storage/UI, Claude Project for persona/instructions). Feasibility confirmed.

Roadmap restructure proposed: M2-M6 reorganized around the differentiator stack, distribution moved earlier, 12 issues recommended for closure.

Sprint reassignment plan built: 5 renames, 12 closures, 3 revisions, ~40 reassignments, 10 new issues. Execution deferred.

### Lead Dev Housekeeping

Between UAT rounds, Lead Dev closed 5 issues (#940, #939, #943, #942, #934), removed 1,272 lines of dead code (orphaned `task_management.py` + empty directories), fixed 6 previously failing tests (orchestration table migration), and completed TODO triage. Test suite: 6,303 → 6,309 passing, 0 failures.

---

## Engineering Metrics

| Metric | Value |
|--------|-------|
| UAT rounds | 3 (0/9 → 0/9 → 5/9) |
| UAT findings identified | 5 (all 5 addressed) |
| Issues closed | 6 (#940, #939, #943, #942, #934, #912) |
| Issues filed | 4 (#939, #940, #945, #949) |
| Dead code removed | 1,272 lines |
| Test suite | 6,303 → 6,309 (+6 previously failing) |
| Blog posts published | 3 ("Silent Failures," "The Mismatch Category," "Nine Voices") |
| Vision iterations | V2.0 → V2.1 → V2.2 |
| Backlog issues analyzed | 16 (deep review) + 119 (PA audit) |

---

## Architectural Decisions This Week

| Decision | Status | Date | Notes |
|----------|--------|------|-------|
| Keep 19-category classifier for analytics, route most to floor | PM DECISION | Apr 8 | Classifier as observation instrument, not routing mechanism |
| #100 Project Portfolio → M2 context assembler task | PM DECISION | Apr 8 | Revise, not close |
| #101 Temporal Context → M2 context assembler task | PM DECISION | Apr 8 | Revise, not close |
| #103 Priority Engine → Horizon 2 | PM DECISION | Apr 8 | Defer |
| MCPB hybrid: tools + Claude Project persona | PROPOSED | Apr 8 | Feasibility confirmed, prototype next |
| "Bring Your Own Chat" distribution philosophy | PM DECISION | Apr 8 | Build as MCP server, package per-platform |

No new ADRs. These are product/strategy decisions that may warrant ADRs once the prototype validates them.

---

## Observations

### What Worked Well

**Three UAT rounds as a diagnostic methodology.** The instinct after round 1 was "fix the 5 findings and re-test." After round 2, when the same fixes didn't change user-facing behavior, the investigation went deeper and found the real root cause (deprecated model ID). The CXO's insistence on scored rubrics and structured findings memos made each round's results unambiguous and comparable. This is Pattern-045 (Green Tests, Red User) working exactly as designed — automated tests passed, real testing caught the failure, and the rubric prevented rationalization.

**PA as strategic analysis engine.** The backlog deep review, MUX analysis, Vision drafting, roadmap restructure, and sprint reassignment plan were all PA output this week. This is the role operating at its intended level — strategic analysis that would take the PM hours, produced in parallel while the PM focuses on UAT and decisions.

**Lead Dev's Five Whys discipline.** The round 2 failure forced a proper root cause analysis instead of another surface-level fix. The deprecated model ID was a silent killer — the 404 was caught by error handling and never surfaced as "model not found." Without the Five Whys chain, the next fix attempt would have been equally wrong.

### What Needs Attention

**Gate still not closed.** We're at 5/9 with 3 additional fixes committed but untested. The re-test will likely pass most or all remaining scenarios, but we need to actually run it. The gap between "fixes committed" and "fixes verified in UAT" was this week's recurring lesson — let's not repeat it.

**Server restart reliability (#949).** Three occurrences this week of "fix deployed but not running": `.pyc` cache serving stale code, orphaned server processes, multiple project directories. The Lead Dev filed #949 but it's not fixed yet. This is a development friction issue that will keep biting us.

**Sprint reassignment plan unexecuted.** PA built a comprehensive plan (5 renames, 12 closures, ~40 reassignments, 10 new issues) but PM ran out of steam on Apr 9 before executing it. The backlog is increasingly misaligned with the project's actual direction. Worth prioritizing the execution.

**Deprecated model IDs as a class of failure.** The root cause of 2+ weeks of UAT delay was a stale model identifier. We should audit all model references in the codebase and consider a validation-on-startup check. Lead Dev partially addressed this with the error classifier improvement, but prevention is better than detection.

### Theme Candidate for Ship #038

"The Gate Meets Reality" — the three-round UAT arc from 0/9 to 5/9, the strategic pivot to "methodology beats code frameworks," and the crystallization of MCPB + BYOC as the distribution path. The week where the project's self-understanding caught up with what it had already built.

---

*Chief Architect Workstream Report — Apr 3-9, 2026*
