---
type: pattern
number: "N/A"
title: "Proto-Pattern Tracking"
status: "Index"
valid_from: "2026-02-06"
last_updated: "2026-11-04"
---

# Proto-Pattern Tracking

_Candidates for formalization that need additional evidence before full pattern status._

**Purpose**: Track emerging practices that have been observed but not yet proven across multiple instances. Proto-patterns graduate to full patterns when they meet the evidence threshold (typically 2+ additional instances beyond initial observation).

**Review cadence**: Evaluated during 6-week pattern sweeps. Proto-patterns that meet evidence threshold get promoted; those with no new instances after two sweeps get archived.

---

## Active Proto-Patterns

### PP-002: Critical vs. Commodity Work in a Role — ELEVATED 2026-10-13

Elevated to **[Pattern-075: Load-Bearing Work Crowded Out by Commodity Work](pattern-075-load-bearing-work-crowded-out-by-commodity-work.md)** (Emerging) by CIO, on the 10-13 role-duties measurement (`docs/internal/research/role-duties-operational-vs-official-2026-10-13.md`). The original entry (April per-role table, instances, criteria) is in git history before this commit.

### PP-003: A Ratchet's Baseline Is Unjudged, Not Accepted

**Observed**: November 4, 2026 (#1551, the env credential-read guard)
**Source**: PPM's memo of 2026-11-04 18:36 ("what 'served' means for the hold"), mailboxes/ppm/sent/
**CIO Decision**: Proto-pattern (CIO, 2026-11-04)
**Elevation Criteria**: 2+ additional instances by the 2026-12-29 methodology audit

**Description**: A ratchet guard lands with a baseline: the sites that already break the rule, listed so CI stays green while new ones fail. That list holds sites nobody has judged yet. When the guard exists to close an exposure, the exposure is closed when every baselined site is ruled (exempt with a reason, or fixed), not when the guard reaches main. Counting "guard on main, CI green" as done lets through the very shape the guard was built for, because the sites that caused the incident can sit in the baseline.

**Known Instance**:
1. #1551 landed with 50 env-read sites baselined. PPM set the invite hold's bar as guard on main, Arch's validation, and every baselined site ruled. Ruling them found a live per-account bug (the calendar status leg read the host's env for a user) and two dead LLM-key config fields. 33 stayed baselined, then 19 unresolved reads were ruled, until only the two issue-gated families (#1481 Slack, #2238 Notion) remained, held off beta by the offer pin.

**What Would Make This a Pattern**:
- Another ratchet whose baseline was counted as acceptance, and a baselined site later turned out to be the defect (negative instance)
- Or another unit whose done-bar requires the baseline to be ruled down (positive instance)
- Not covered by mechanism-silence-is-not-coverage (memory): that is about a guard that isn't running. Here the guard runs, and its silence on the listed sites is deliberate.

**Related Patterns**:
- Pattern-046 (100% completion): the baseline is the remaining percentage
- CIO's 11-04 audit rule (standing-items row 9m): a deferral that carries exposure needs a mechanical trigger or gate

### PP-001: Design Archaeology

**Observed**: February 3, 2026 (Pattern Sweep 2.0, #777)
**Source**: History sidebar design investigation (February 2, 2026)
**CIO Decision**: Deferred to proto-pattern tracking (February 4, 2026)
**Elevation Criteria**: 2+ additional instances before March 17, 2026 sweep

**Description**: When investigating a design question, conduct archaeological analysis of how the current design evolved before proposing changes. Examines commit history, omnibus logs, and decision records to understand *why* the current state exists — preventing accidental reversal of intentional decisions.

**Known Instance**:
1. History sidebar 404 investigation (#780) — discovered that sidebar design had evolved through 3 distinct phases, each responding to different user feedback. Without archaeology, the fix would have reverted to Phase 1 design.

**What Would Make This a Pattern**:
- Additional instances of design archaeology preventing regressions
- Evidence that skipping archaeology led to problems (negative instances)
- Distinct enough from Pattern-042 (Investigation-Only Protocol) to warrant separate documentation

**Related Patterns**:
- Pattern-042: Investigation-Only Protocol (investigation discipline, but not design-specific)
- Pattern-060: Cascade Investigation (investigation breadth, not historical depth)

---

## Archived Proto-Patterns

_Proto-patterns that were not elevated after two sweep cycles._

### Historical (Pre-Tracking)

The following were identified informally but never tracked with this mechanism:

- **Primate in the Loop** — Human oversight pattern (December 2025). Subsumed by existing patterns (006, 047).
- **Small Scripts Win** — Preference for small focused scripts (December 2025). Too general to be a pattern.
- **Session Failure Conditions** — Conditions that cause session failures (December 2025). Covered by STOP conditions in CLAUDE.md.

---

## Process

### Adding a Proto-Pattern

1. Identify candidate during pattern sweep or ad-hoc observation
2. Verify it's genuinely distinct from existing patterns (FALSE POSITIVE test)
3. Add entry to Active Proto-Patterns with: observation date, source, known instances, elevation criteria
4. Set review date (next scheduled sweep)

### Elevating a Proto-Pattern

1. During pattern sweep, review active proto-patterns for new instances
2. If evidence threshold met: draft full pattern document, submit for CIO approval
3. Move entry from Active to the main pattern index
4. Remove from this file

### Archiving a Proto-Pattern

1. If no new instances after two sweep cycles (~12 weeks), archive
2. Move to Archived section with brief explanation
3. Can be reactivated if new evidence surfaces

---

_Created: February 5, 2026_
_Per CIO assignment (memo-cio-pattern-sweep-response-2026-02-04)_
