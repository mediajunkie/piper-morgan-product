# Proto-Pattern Tracking

_Candidates for formalization that need additional evidence before full pattern status._

**Purpose**: Track emerging practices that have been observed but not yet proven across multiple instances. Proto-patterns graduate to full patterns when they meet the evidence threshold (typically 2+ additional instances beyond initial observation).

**Review cadence**: Evaluated during 6-week pattern sweeps. Proto-patterns that meet evidence threshold get promoted; those with no new instances after two sweeps get archived.

---

## Active Proto-Patterns

### PP-002: Load-Bearing vs. Commodity Work in a Role

**Observed**: April 22–26, 2026 (Apr 22–26 leadership migration wave)
**Source**: Agent 360 v0.2 §6 candor reflections from seven retiring Chat-instance leadership roles (HOST, CIO, Comms, CXO, PPM, Architect, Exec)
**Logged here**: April 27, 2026 per PM directive
**Elevation Criteria**: confirm the distinction holds across at least one full sprint of post-migration operation (target: review during the next pattern sweep), and confirm it survives translation to Lead Dev + Docs (the two roles that did not migrate)

**Description**: Each role has a *subset* of its formal scope that is **load-bearing** (where the role's distinctive judgment lives — without this work the role isn't doing its job) and a remainder that is **commodity** (work the role owns where filesystem-direct access makes execution fast, and which can crowd out distinctive work if not bounded). The structural distinction surfaced *independently* in every Section 6 across seven role retirements — same shape, different surface manifestations. The consistency across seven different roles is structural, not coincidental.

**Cross-role manifestations** (extracted from Agent 360 §6 + handoff memos):

| Role | Load-bearing | Commodity |
|---|---|---|
| HOST | Noticing + naming dysfunction (specifically: "X is 107 days stale" beats "docs are outdated"); cross-checking memos against omnibus to detect drift | Reading omnibus comprehensively; human-network status table maintenance; session-log archival |
| CIO | Methodology audits (Mar 15 + Apr 17 produced structural insight + downstream policy); discovering and formalizing emerging patterns | Workstream-review timeline reconstruction (commodity by CIO's own naming); cross-pollination routing |
| Comms | Narrative-arc awareness (which pieces connect, what arc they form, where the gaps are — lives in role-holder's head; doesn't survive session boundaries) | Placeholder discipline once learned; calendar bookkeeping; mail delivery coordination |
| CXO | Colleague Test application + experience-quality judgment ("the Colleague Test is more important than the CXO role") | Workstream review authorship; voice-and-tone iteration housekeeping |
| PPM | Roundtable synthesis ("the distinctive function") + spec pipeline translation; quality threshold judgment | Workstream memos ("most often work, but not what makes the role distinctive"); reading 7 omnibus logs |
| Architect | Cross-project protocol decisions (Klatch alignment, URI conventions); ADR synthesis; specification-vs-existing-work review | Timeline reconstruction in workstream memos; ADR formatting housekeeping |
| Exec | Review work (Ship draft, handoff, workstream against omnibus) — judgment lives here | Tracker maintenance, handoff packaging, status synthesis |
| Lead Dev (inferred — no migration 360) | Engineering judgment + audit-cascade + closing issues with evidence | Manifest housekeeping, session-log archival, routine git mechanics |
| Docs (inferred — no migration 360) | Omnibus synthesis + canonical-verification discipline + methodology custodianship | Mailbox shuttling, calendar bookkeeping, session-log archival |

**Pattern observation**: commodity work clusters around **information management and housekeeping**. Load-bearing work clusters around **judgment, verification, and cross-context synthesis**. The risk: when Code-era filesystem access makes commodity work faster (direct reads instead of search), agents may still allocate the same time to it, causing load-bearing work to be crowded out.

**Known Instances**:
1. CXO Apr 25 §6: "the Colleague Test is more important than the CXO role" — load-bearing artifact > role identity (originally framed)
2. PPM Apr 25 §6: workstream memos as "the recurring obligation, not what makes the role distinctive" — same shape
3. Exec Apr 26 §6: review-vs-tracker split named explicitly — same shape
4. HOST/CIO/Comms/Architect §6: same shape across all four (Apr 22–25)
5. Apr 26 omnibus Core Theme #2: structural convergence across all seven independently — meta-instance

**Elevation criteria**:
- Confirm the distinction holds across at least one full sprint of post-migration operation
- Validate Lead Dev + Docs distinctions (currently inferred; need explicit reflection)
- Identify any role-distinct *anti-pattern* shape (e.g., what does it look like when commodity work crowds out load-bearing? known: HOST tracker-staleness self-reflection)

**What Would Make This a Pattern**:
- 2+ additional instances surfacing the distinction in *new* roles or cross-project (Klatch could test the framing in their leadership)
- Evidence that the framing changed someone's behavior (declined a commodity task, protected time for load-bearing) — without behavior change, it's just nomenclature
- Methodology entry codifying the discipline (HOST post-migration synthesis territory)

**Related Patterns**:
- Pattern-045 (Green Tests, Red User): commodity work *passing* doesn't mean role is *succeeding*
- Pattern-062 (Assembly Assumption): individual role-correct work doesn't compose into team-correct work; load-bearing/commodity is a Pattern-062 manifestation at the role-allocation layer

**Methodology meta-insight (PM Apr 27)**: The Agent 360 v0.2 was originally a feedback questionnaire (Mar 19 first round). It gained a second life as the migration handoff baseline (validated through Apr 22–26). It is now generating a *third-degree* value: §6 reflections are surfacing methodology-codifiable patterns that no single role-holder would have found alone. The instrument was designed for one purpose; it's compounding to three.

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
