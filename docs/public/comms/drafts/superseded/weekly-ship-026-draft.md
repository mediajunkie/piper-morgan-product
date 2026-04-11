# Weekly Ship #026: The Seven Whys

*January 9-15, 2026*

---

## What shipped this week

**If this period proves one thing, it's that systematic discipline scales.**

Two production releases. Thirty-six issues closed. Sprint B1 completed. Five Medium posts published. And one canonical demonstration of why "tests pass" is never the finish line.

## Milestones

**🎯 Stage positions at 4.2.7**

The Inchworm Map now shows:
1. ✅ The Great Refactor
2. ✅ CORE Functionality
3. ✅ ALPHA Foundation
4. 🔄 Complete build of MVP (in progress)

**Sprint B1 Complete** (Jan 11): Epic #314 (Conversation Persistence) closed with all children verified. Three consecutive HIGH-COMPLEXITY days—Jan 9, 10, 11—produced 23+ issues closed without sacrificing methodology discipline. The Excellence Flywheel in action.

**v0.8.4 Released** (Jan 12): Calendar integration improvements, intent classification enhancements, and the full B1 feature set.

**v0.8.4.2 Released** (Jan 15): Calendar bug fixes including "tomorrow" query handling and stale data prevention. Trust-critical fixes—users seeing "No meetings" when they have meetings erodes confidence fast.

## The week in numbers

| Metric | Value |
|--------|-------|
| Issues closed | 36 |
| Issues opened | 39 |
| Epics closed | 3 (#242 Standup, #314 Conversation Persistence, #543 Integration Settings) |
| Releases | 4 (v0.8.3.2 → v0.8.4 → v0.8.4.1 → v0.8.4.2) |
| HIGH-COMPLEXITY days | 6 of 7 |
| Patterns formalized | 1 (Pattern-049: Audit Cascade) |
| ADRs created | 5 (050-054) |

## Architecture highlights

Five new ADRs this period:

- **ADR-050**: Conversation-as-Graph Model (Ted Nadeau's MultiChat architecture)
- **ADR-051**: Unified User Session Context (14 ID concepts → single RequestContext)
- **ADR-052**: Tool-Based MCP Standardization (recovered from misfiling)
- **ADR-053**: Trust Computation Architecture
- **ADR-054**: Cross-Session Memory Architecture (three-layer model)

**Pattern-049: Audit Cascade** formalized the discovery that LLMs audit better than they create. Same checklist, different cognitive mode. This pattern immediately improved completion rates.

## What technology & process innovations emerged?

**Mailbox System Operational** (Jan 13): Agent-to-agent async communication now has structure—`/mailboxes/{role}/` with `context/`, `inbox/`, `read/` folders. PM serves as manual mailbot for now. The parallel to Steve Yegge's Gastown architecture is striking: we're manually operating what they automated.

**Context Engineering Discovery**: When the Lead Developer forgot its role after context compaction, the fix was structural—place role identity at document top (first content survives summarization best). This is "context engineering"—deliberate document structure for AI consumption.

**Gas Town Analysis** (Jan 15): CIO analyzed Steve Yegge's multi-agent orchestration article. Key insight: we have sophisticated methodology; we lack equally compelling articulation. Three initiatives launched: methodology articulation with Communications, context continuity tooling brief to advisors, and lessons synthesis.

## External relations & community

**Publications** (5 Medium posts):
- Jan 10: "The Completion Matrix: Why 'Tests Pass' Isn't Done"
- Jan 11: "The Shadow Package Problem"
- Jan 12: "Stage 3 Complete"
- Jan 14: "B1 Begins"
- (Jan 8: "The New Year Build" — technically prior period but contextually important)

**AI Leadership Playbook** launched: 13-chapter outline, image vocabulary catalogued (17 robot illustrations, 9 metaphor families), three narrative drafts ready.

**Podcast prep**: Cindy Chastain meeting confirmed for Monday January 20. Theme: "The Methodology Multiplier"—the counter-narrative that AI requires MORE rigor, not less.

## Governance & operations

**Role Health**: All agent roles active. Communications Director succession (Jan 14→15) demonstrated clean recovery using BRIEFING-ESSENTIAL pattern. HOSR founding complete and contributing meaningfully.

**Subagent Parallelization Proven**: Jan 9 demonstrated 3x speedup with 4 Haiku agents working in parallel. Pattern needs formalization.

**Alpha Testing**: Current testers (Michelle, Adam) have "below kindling" participation—interested volunteers with competing priorities. Next cohort invitation coming soon.

## This week's learning pattern

### The Seven Whys

On January 9, we had a feature that looked complete. The tests passed—39 of them. The code was merged. The issue was ready to close.

Then I tried to use it.

Complete failure. Not partial. Not "mostly works." The feature simply didn't function.

What followed was an extended "Five Whys" analysis that became Seven Whys. Each layer revealed a different bug category:

1. **Why didn't it work?** Route doesn't use auth dependency
2. **Why wasn't that caught?** IntentService not passed user_id
3. **Why did tests pass?** Route not in middleware exclude_paths
4. **Why wasn't that obvious?** Wrong JWT method name (verify_token vs validate_token)
5. **Why did the mock work?** Wrong import path
6. **Why did degradation seem OK?** Echo bug—response had wrong field name
7. **Why wasn't the classifier working?** IntentClassifier missing dependency injection

Seven bugs. Seven different failure modes. All hiding behind green tests.

The PM intervention at 17:44 that day captured the frame shift: *"Wrong frame: 'Fix the bug so feature works.' Right frame: 'Learn what is not yet built correctly.'"*

This became the canonical demonstration of Pattern-045 (Green Tests, Red User). It's now cited in the Gas Town analysis, the Leadership Playbook outline, and multiple methodology discussions.

**The insight**: Testing infrastructure can achieve 100% coverage of the wrong things. Manual verification isn't overhead—it's the only way to know if the system actually works for users.

**The remedy**: When faced with repeated 75% failures, deploy full flywheel discipline: DDD review, required TDD, multiple independent agents for tests/code/verification, and non-negotiable human review. Skipping the human step makes 75% outcomes nearly certain.

---

*Piper Morgan is an AI-powered product management assistant. These weekly ships document the building-in-public journey.*

*Next week: MUX-V1 preparation, alpha tester outreach, and continuing the methodology articulation work.*

---

*Draft v1 | January 17, 2026*
