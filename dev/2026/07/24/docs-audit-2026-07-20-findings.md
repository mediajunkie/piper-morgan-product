# Weekly Docs Audit — FLY-AUDIT 2026-07-20 — Findings

**Audit issue**: #1453
**Audit date**: 2026-07-20 (conducted 2026-07-24)
**Executed by**: Documentation Management (Docs), Sonnet 4.6

---

## Completion Matrix

| Section | Status | Evidence/Notes |
|---------|--------|----------------|
| Briefing Freshness | ✅ | Frontmatter + STATUS BANNER updated; final Jul 23 numbers folded |
| Link Integrity Check | ✅ | 0 broken links in ADRs, patterns, or briefings |
| Omnibus Coverage Check | ✅ | Jul 19-23 all written this session; continuous coverage to Jul 23 |
| Sprint & Roadmap Alignment | ✅ | roadmap.md v18.7 (Jul 16) reflects current state; no new sprint since |
| GitHub Issues Sync | ✅ | 0 stale open issues (>30 days); 6 open without milestone (noted below) |
| Pattern & Knowledge Capture | ✅ with finding | 74 patterns + 1 template = 75 files; count correct. ADR index stale (9 ADRs missing) — filed as finding |
| Quality Checks (root README.md) | ✅ with finding | `pmorgan.tech` domain in root README may be stale vs `pipermorgan.ai` — flagged, PM's call |
| Quality Checks (docs/README.md) | ✅ | Version v0.8.11.0 accurate; ADR count "78" matches actual files; all referenced alpha docs exist |

---

## Section-by-Section Findings

### 1. Briefing Freshness ✅

- BRIEFING-CURRENT-STATE.md was last committed July 23 ~3:50 PM PT by Lead Dev.
- **Frontmatter drift found and fixed**: `last_updated` and `last_verified` showed "2026-07-19"
  despite the STATUS BANNER being updated July 23. Updated frontmatter to match.
- **STATUS BANNER mid-day numbers updated to final day-close numbers**:
  - Old: "264→119 today alone (waves 15–42), seven green batches"
  - Corrected: "264→105 today alone (waves 15–44), ten green batches"
  - Source: Lead Dev Jul 23 session log (`dev/2026/07/23/2026-07-23-0647-lead-code-log.md`)
- Both changes committed as part of this audit.

### 2. Link Integrity ✅

- ADR broken links: **0**
  (command: `python3 -c "import os,re,glob; B=[...]; print('broken ADR links:', len(B))"`)
- Pattern + briefing broken links: **0**
- No broken internal links in priority files.

### 3. Omnibus Coverage ✅

- Jul 14 through Jul 23: continuous, no gaps.
- Jul 19-23 omnibuses written this session (Jul 19: 575 lines HIGH-COMPLEXITY: COORDINATION;
  Jul 20: 221 STANDARD; Jul 21: 396 HIGH-COMPLEXITY: EXECUTION; Jul 22: 218 STANDARD;
  Jul 23: 395 HIGH-COMPLEXITY: EXECUTION).
- No stranded session logs in `dev/active/`.

### 4. Sprint & Roadmap Alignment ✅

- `docs/internal/planning/roadmap/roadmap.md` last updated 2026-07-16 (v18.7 fold).
- Reflects: Finish-the-Unfinished sprint active; Beta Blockers 7→24 open; Production 1.0
  gate defined; RECONNECT R2 seeded.
- No new sprint has started since Jul 16 — no update required.
- No stale "NEW:" claims found in root README (features described are ≥2 weeks old
  but the README style is evergreen, not "NEW:"-marked).

### 5. GitHub Issues Sync ✅

- Open issues stale >30 days: **0** ✅
- Open issues without milestone: **6**
  - `#1453` FLY-AUDIT: Weekly Docs Audit (the audit itself — expected)
  - `#1452` Full Test Suite backlog (working issue — backlog arc 634→105 as of Jul 23)
  - `#1451` settings/projects template test fails
  - `#1449` Real performance + coverage gates
  - `#1445` Canonical e2e fixture teardown FK violation
  - `#1411` update_issue elif-dispatched only
  - **Action**: These 5 non-audit issues should have milestone assignments. Not blocking this
    audit but worth PM's attention.

### 6. Pattern & Knowledge Capture ✅ with finding

**Pattern count**: 74 numbered patterns (001-074) + 1 template (000) = 75 files total.
`ls -1 docs/internal/architecture/current/patterns/pattern-*.md | wc -l` → 75.
README.md documents "74 patterns (001-074), plus a template (000)" — **accurate**.

**ADR index staleness — REAL FINDING** (track as #1455 or similar):
- Actual ADR files: 78 (adr-000 through adr-079, with gaps at 067/068)
- `adr-index.md` documented count: 67 — stale
- **9 ADRs present as files but absent from the index**: 065, 066, 069, 074, 075, 076, 077, 078, 079
- ADR titles for the missing entries:
  - ADR-065: Canonical Context-Package Format (BYOC / Plugin-Packaged)
  - ADR-066: Packaging-Layer Abstraction (BYOC Plugin Per-Host Deployment)
  - ADR-069: Domain Concept Projection Contract — System of Record vs. In-Process Working State
  - ADR-074: Encryption at Rest Strategy
  - ADR-075: Configuration / Personalization Ownership — Per-User Scoping for Instance Config
  - ADR-076: Usage-Cap Enforcement (Alpha Load Backstop)
  - ADR-077: Routing-Integrity Contract (Action↔Handler Reachability)
  - ADR-078: Session-Activity Ledger + Pre-Classifier Reference Resolution
  - ADR-079: Owner-Scoping Integrity Contract
- **Note**: `docs/README.md` claims "78 decisions with rationale" which matches the actual file count
  (78 files). The index is what's stale, not the README.
- **Recommended action**: Arch to add entries for ADRs 065, 066, 069, 074-079 to `adr-index.md`
  and update the "Total ADRs" claim in the index header. This is Arch-owned since each
  entry requires accurate descriptions.

### 7. Quality Checks — root README.md ✅ with finding

Root `README.md` reviewed:
- **Domain inconsistency found**: The root README uses `pmorgan.tech` in multiple places
  (badge URL, documentation link, support section) while `docs/README.md` consistently uses
  `pipermorgan.ai` as the canonical domain.
  - Line 4: shield badge `pmorgan.tech` / link `https://pmorgan.tech`
  - Line 12: "Full documentation and getting started guides are available at [pmorgan.tech]"
  - Line 37: "[Complete Documentation](https://pmorgan.tech)"
  - Line 40: "[pmorgan.tech](https://pmorgan.tech)"
  - Memory: `feedback_canonical_link_meaning.md` says "canonical link = pipermorgan.ai"
  - **Recommendation**: PM to confirm whether `pmorgan.tech` still redirects to `pipermorgan.ai`
    and if so, whether to update the root README to use `pipermorgan.ai` directly for consistency.
- Referenced docs exist: `CONTRIBUTING.md` ✅, `docs/TECHNICAL-DEVELOPERS.md` ✅
- No outdated "NEW:" feature claims (README is evergreen in style)
- No accidental test content or markdown artifacts

### 8. Quality Checks — docs/README.md ✅

- Version `v0.8.11.0 alpha` — **accurate** (cut 2026-07-17 per BRIEFING)
- ADR count "78 decisions with rationale (as of 2026-07-09)" — **accurate** (78 actual files)
- `alpha.pipermorgan.ai` domain consistent with `pipermorgan.ai` canonical
- All alpha docs referenced exist: ALPHA_QUICKSTART.md, ALPHA_TESTING_GUIDE.md,
  ALPHA_KNOWN_ISSUES.md, ALPHA_AGREEMENT_v2.md, releases/RELEASE-NOTES-v0.8.11.0.md ✅
- `MorningStandupWorkflow` reference: not found in docs/README.md (retired via #1289 per
  previous audit note — not present, no action needed)

---

## Issues to File / Action Items

| Priority | Finding | Owner | Action |
|----------|---------|-------|--------|
| **High** | ADR index missing 9 ADRs (065, 066, 069, 074-079) | Arch | File issue; add to adr-index.md |
| **Medium** | 5 open issues without milestone (#1452, #1451, #1449, #1445, #1411) | PM | Assign milestones |
| **Low** | root README.md uses `pmorgan.tech` vs `pipermorgan.ai` | PM | Confirm domain/update |

---

## Automated Checks Run

```bash
# Broken ADR links
python3 -c "import os,re,glob; B=[...]; print('broken ADR links:', len(B))"
→ 0 broken ADR links

# Broken links in patterns + briefings  
python3 -c "import os,re,glob; results=[...]; print(f'Broken links: {len(results)}')"
→ 0 broken links

# Pattern count
ls -1 docs/internal/architecture/current/patterns/pattern-*.md | wc -l
→ 75 (74 numbered + 1 template = correct per README)

# ADR count
ls docs/internal/architecture/current/adrs/adr-[0-9]*.md | wc -l
→ 78 actual files vs index claim of 67

# Stale issues
gh issue list --state open --json ... → 0 issues stale >30 days

# Stranded session logs
ls dev/active/2026-*-log.md → none found

# Backup files
find docs/ -name "*.backup" -o -name "*.old" → none found
```
