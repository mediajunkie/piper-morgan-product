# M1 Methodology Audit: Document References Report

**Audit Window**: March 15 — April 11, 2026 (inclusive)
**Report Date**: April 17, 2026
**Prepared by**: PA (Piper Alpha), per CIO request (memo 2026-04-16)
**Data Source**: 128 session logs and working files across 27 days in `dev/2026/{03,04}/`
**Methodology**: Counted distinct files referencing each doc class (multiple occurrences in one file = 1 count). Mailbox memos excluded per CIO scope. Files dated Apr 12+ excluded.

This is input to the M1 audit, not the audit itself. Interpretation is CIO's.

---

## A. Methodology-Core Docs

### Referenced During Audit Window

Only 2 numbered methodology docs appear in session logs:

- **methodology-20** (omnibus session logs): 3 files — *docs-code agents exclusively* (2026-03-17, 2026-03-20, 2026-03-23)
- **methodology-22** (roundtable synthesis): 2 files (2026-03-21 ppm-opus, 2026-03-23 docs-code-opus)

Unnumbered methodology-core references:
- **methodology-core** (directory/index mention): 5 files — mixed roles (CIO, Docs, PA)
- **gameplan-template**: 1 file (2026-04-04 lead-code-opus)
- **HOW_TO_USE_MULTI_AGENT** / multi-agent pattern language: 2 files (2026-03-21 lead-code, 2026-03-26 comms)

### Silent During Audit Window

The following 20 numbered methodology docs were **not referenced** in any session log during the window:

`methodology-00, -01, -02, -03, -04, -05, -06, -07, -08, -09, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -21`

Unnumbered silent: `chat-protocols.md`, `claude-code-workflow.md`, `enhanced-autonomy-*.md` — zero hits.

---

## B. Patterns

### Top Cited

| Pattern | Distinct files | Role distribution |
|---|---|---|
| **Pattern-062** (Assembly Assumption) | 14 | Exec (5), Arch (3), CIO (3), Lead-code (2), Docs (1) |
| **Pattern-045** (Green Tests, Red User) | 12 | CXO (4), PA (2), Lead-code (2), Docs (1), Comms (1), Exec (1) |
| Pattern-063 | 6 | Mixed (Arch, Lead-code, Exec) |

### Load-Bearing Pattern Status

- **Pattern-045**: 12 files across 6 roles. Present throughout the window; appears systemic (cited as completion-discipline concern).
- **Pattern-062**: 14 files across 5 roles. Heavily cited by Exec and Architecture; appears as *problem diagnosis* language (e.g., "textbook Assembly Assumption composition bug" in ADR-059 review), not prescription.

### Silent Patterns

No patterns beyond those listed above were confirmed referenced during the window. Pattern files with dedicated docs in `docs/internal/architecture/current/patterns/` but zero references during the window appear to be numerous (exact list not enumerated — can be produced on request).

---

## C. ADRs

### Top Cited

| ADR | Distinct files | Note |
|---|---|---|
| **ADR-060** (floor-first routing) | 26 | Central to Phase 2-3 migration; pervasive across Exec, Arch, PA, Docs |
| **ADR-059** (Workflow Dispatcher) | 17 | Heavy approval cycle Mar 19–21 |
| ADR-039 | 6 | Original routing framework; superseded in philosophy by ADR-060, infrastructure retained |
| ADR-049 | 4 | ProcessRegistry; on hold pending ADR-059 implementation |
| **ADR-054** | 1 | PA agent, 2026-03-30 |
| **ADR-053** | 1 | PA agent, 2026-03-30 (same session as ADR-054) |
| **ADR-045** | 1 | Single reference |
| ADR-035 | 1 | Single reference |
| ADR-023 | 1 | Single reference |

### Load-Bearing ADR Status

- **ADR-060**: 26 files — dominant reference of the window; appears as organizing architectural principle for M1.
- **ADR-054** & **ADR-053**: 1 file each (same PA session) — minimal surface area in session logs during the window despite being foundational to composting pipeline / trust graduation respectively.
- **ADR-045** (object model grammar): Single reference. Given its constitutional role, the low count may reflect internalization rather than neglect — worth CIO attention either way.
- **ADR-059**: 17 files — visible multi-role coordination during the Mar 19–21 review cycle.

### Silent ADRs

ADRs with zero references during the window: 001–022, 024–034, 036–038, 040–048 (except 045), 050–052, 055–058, 061+.

---

## D. PDRs

| PDR | Distinct files |
|---|---|
| **PDR-004** | 17 |
| PDR-001 | 8 |
| PDR-003 | 6 |
| PDR-002 | 5 |

PDRs 005+: zero references.

PDR-004 is the dominant PDR citation of the window, with no clear role clustering — likely an active standard being invoked across workstreams. The Apr 16 PDR-004 paraphrase-drift incident (Docs → CXO correction) is consistent with a doc under frequent reference where paraphrasing can drift.

---

## E. Concentration Observations (for CIO)

1. **ADR-060 dominance (26 files)**: Floor-first routing is the organizing architectural principle of the audit window. Reference clusters: Exec planning (Mar 19–21, Mar 30–31) and implementation coordination (Apr 10–11).

2. **Pattern-062 as diagnostic language (14 files)**: Assembly Assumption is cited as *problem diagnosis*, not prescription. Organizational fluency in naming structural composition failures is a methodology signal.

3. **Pattern-045 systemic spread (12 files, 6 roles)**: Completion discipline referenced across Exec, CXO, PA, Docs, Code, and Comms. No role clustering — appears to function as universal methodology concern during the period, consistent with the M1 UAT failures that surfaced it at scale.

4. **Methodology-core silence** (20 of 22 numbered docs silent): Only methodology-20 (omnibus) and methodology-22 (roundtable) appear in session logs. This is consistent with two hypotheses — (a) the principles are internalized and operate via CLAUDE.md principles rather than methodology-core citations; (b) structural disconnect between the methodology-core directory and active agent work. The Flywheel archaeology reformulation decision (CIO memo 2026-04-16) indirectly supports hypothesis (a).

5. **PDR-004 dominance + ADR-045 near-silence**: Both are constitutional-level docs. PDR-004 cites heavily (17), ADR-045 cites once. If both are load-bearing but one leaves heavy traces and the other doesn't, the asymmetry may be worth examination in the audit.

6. **ADR-059 approval cycle visibility**: 17 files across ~5 days indicates heavyweight architectural decisions get explicit multi-role engagement. Lighter decisions may be invisible in session logs — a methodology observation about what the log-based archaeology can and can't see.

---

*Data-gathering artifact. Available for extended queries (specific date ranges, role-specific cuts, co-occurrence analysis) if CIO needs refinement for the audit draft.*
