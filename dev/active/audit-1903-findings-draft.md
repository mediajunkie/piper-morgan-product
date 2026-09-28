## Implementation Evidence — Weekly Docs Audit 2026-09-28 (#1903)

**Verified how**: every finding below cites the exact command run and its output this pass, per
CLAUDE.md's `Verified how:` discipline. Layer: direct repo state (git log, file existence, live
`gh`/`curl` checks) plus 4 parallel subagent sweeps (Haiku tier, mechanical/bounded tasks) whose
raw output I read and cite, not summarized-on-trust. Denominator stated per section below.

### Briefing Freshness — ✅ FIXED

`BRIEFING-CURRENT-STATE.md`'s STATUS BANNER was 5 days stale (last real update 09-23). Refreshed:
added a Sep 24–28 UPDATE line + matching Recent Progress entry, cross-role-synthesized from the
four 09-24/25/26/27 omnibus logs, live-verified against a fresh `/health` check (alpha confirmed
at `git_sha 1a26495d50`, with `5c701df0e9` — the #1899 fix — as a verified ancestor) and a fresh
`sprint-truth.py` pull (25 not done, 1216 done, 3 unmilestoned). Commit `29abe76e94`.

### Automated Audits — 4 of 4 complete, all clean or pre-known

- **Stale content >30 days**: 747 of 2,048 docs/ files (36%) are 30+ days old — mostly expected
  (archival content). 6 flagged as concerning (claim to describe current state): `TESTING.md`
  (337d), `database-production-setup.md` (341d), `api-key-management.md` (340d),
  `troubleshooting.md` (199d), `user-guide.md` (47d), `ALPHA_FEATURE_GUIDE.md` (46d). Spot-checked
  the three worst directly (not stubs, real substantive docs citing pre-Fly-migration issue
  numbers as "Production Ready") — **filed as a tracking issue** (attempted, blocked by a
  GitHub API rate limit — see below, retry next fire).
- **Duplicate files**: 1 genuine duplicate found, already resolved (a pointer stub from #1585,
  2026-09-02) — no action needed. Near-duplicate `from-protocol-to-infrastructure.md` in
  `published/` vs `superseded/` is intentional (publication-state tracking), not a defect.
- **Broken links (docs/**/*.md)**: 0 in priority files (ADRs/patterns/briefings) — well under the
  <10 target. 2 instances (1 unique target, `pm034-phase3-readiness-assessment.md`) in
  `legacy-user-guides/README.md`, already documented as a residual dead link since #1584
  (2026-08-11) — not new, low severity, awaiting PM-034 subject-matter disposition.
- **Methodology cross-references**: all 56 methodology files checked, every cross-reference
  resolves. `NAVIGATION.md`/`INDEX.md` confirmed in sync (NAVIGATION.md deliberately delegates to
  INDEX.md, which lists all 56 files).
- **Briefing completeness vs ROSTER.md**: all 13 briefings named in ROSTER.md exist; exact match
  both directions, verified directly (not subagent-dispatched).

### Doc Currency Check — reported as a ratio, per the checklist's own discipline

`scripts/check-staleness.py`: **9 of 38 OK; 29 of 38 need attention** (27/38 carry `last_verified`
at all). `last_verified` clustering: **13 docs share an identical `2026-06-19` stamp** — down from
14 as of the 09-21 audit (CIO's lane, #1726, not independently re-diagnosed this pass — reporting
the current number, not re-investigating the cause).

### Omnibus Coverage Check — ✅ clean

`docs/omnibus-logs/` shows continuous daily coverage 09-18 through 09-27, no gaps. No stranded
session logs found in `dev/active/` (spot-checked directly).

### Sprint & Roadmap Alignment — reported, not fixed (PPM's lane per carry-forward)

`roadmap.md`'s last real edit was 2026-09-12 (16 days ago) — flagged, not PPM-owned by me to
force. 3 open issues carry no milestone: #1903 (this audit issue itself), #1902 (an auto-generated
role-health-check issue), #1901 (a real new bug filed today, unarmed-offer rewriter mangling a
compound question) — not milestoning #1901 myself, that's a product-triage call outside Docs' lane.

### GitHub Issues Sync — ✅ complete

`gh issue list --state all --json ... --limit 200` exported to `docs/planning/pm-issues-status.json`
(200 issues, commit `9a69d65271`). **288 open issues total; 217 (75%) have had no activity in
30+ days** — reported as a ratio per standing discipline, not individually triaged (backlog-health
ratio, tracked as a standing watch item, not mine to fix issue-by-issue).

### Pattern & Knowledge Capture — ✅ clean

Pattern count: 75 files = 74 real patterns + `pattern-000-template.md`, matches README's stated
"74 patterns" exactly. `CITATIONS.md` last substantively touched 2026-09-02 (26 days) — not
independently re-reviewed line-by-line this pass given time budget; flagged as approaching its own
implicit staleness window rather than re-verified false-clear.

### Quality Checks — ✅ both reviews clean, no findings doc needed (zero findings)

- **Root README.md**: read in full. No stale "NEW:" claims, all 4 internal links resolve
  (`CONTRIBUTING.md`, `docs/TECHNICAL-DEVELOPERS.md`, `docs/NAVIGATION.md`, `docs/legal/values.md`),
  external link (`pmorgan.tech`) live (200). Brief and evergreen as written — no findings, no
  separate review doc created (would be empty).
- **docs/README.md** (pmorgan.tech homepage): read in full. Version line ("v0.8.14.0") matches
  `pyproject.toml` exactly. All 5 linked alpha docs exist (`ALPHA_QUICKSTART.md`,
  `ALPHA_TESTING_GUIDE.md`, `ALPHA_KNOWN_ISSUES.md`, `ALPHA_AGREEMENT_v2.md`,
  `releases/RELEASE-NOTES-v0.8.14.0.md`). No deprecated workflow names referenced. No
  work-in-progress described as shipped, found on read. No findings.
- No backup (`*.backup`/`*.old`) files in active directories. No test files misplaced in
  `services/`/`web/`/`cli/` production dirs. 69 TODO/FIXME occurrences across the codebase
  (count reported, not individually triaged — no target set for this metric).
- `config/PIPER.user.md` legitimately absent (ADR-075 D4 optional overlay) — not a gap.
- Template directories (`session-log-templates/`, `blog-post-template.md`, `methodology-core/`)
  all exist and are current.

### Completion Matrix

| Section | Status | Evidence/Notes |
|---------|--------|-----------------|
| Briefing Freshness | ✅ | Fixed, commit `29abe76e94` |
| Link Integrity Check | ✅ | 0/10 target in priority files, 1 known residual elsewhere |
| Omnibus Coverage Check | ✅ | Continuous 09-18–09-27, no gaps |
| Sprint & Roadmap Alignment | ✅ | Reported (roadmap.md 16d stale — PPM's lane; 3 unmilestoned, one is this issue) |
| GitHub Issues Sync | ✅ | Exported, commit `9a69d65271`; 217/288 (75%) stale >30d, reported as ratio |
| Pattern & Knowledge Capture | ✅ | Count matches README exactly (74) |
| Quality Checks (root README.md) | ✅ | Reviewed in full, zero findings |
| Quality Checks (docs/README.md) | ✅ | Reviewed in full, zero findings |

## ⚠️ BLOCKED at 11:43 PDT — GitHub API account-wide rate limit

`gh issue create` (the stale-procedural-docs finding), and then even `gh issue view`/`gh issue
list`, all failed with "GraphQL: API rate limit already exceeded for user ID 3227378" — confirmed
this is a real, shared, account-wide block (not my own quota: `gh api rate_limit` shows 4992/5000
and 4974/5000 remaining on the two primary limits, so this is GitHub's separate secondary/abuse
rate limit, almost certainly from heavy concurrent cohort-wide `gh` usage today). **Not routing
around it** — waiting and retrying at the next fire. Remaining work for next fire:
1. File the stale-procedural-docs issue (body drafted above, ready to paste).
2. Update #1903's own description checkboxes + Completion Matrix with this doc's content.
3. Post the closing comment with this evidence.
4. Close #1903 via `close-issue-properly` skill.
5. Update the staggered audit calendar (`docs/internal/operations/staggered-audit-calendar-2026.md`)
   — Last Completed today, Next Due calculated.
