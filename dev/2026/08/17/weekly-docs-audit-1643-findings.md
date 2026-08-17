# Weekly Docs Audit #1643 — Findings — 2026-08-17

**Auditor**: Docs · **Method**: direct verification (this session) + 3 parallel research subagents
(read-only, no edits) for the automated-audit section, converged and fact-checked before any fix
was applied. Every fix below was verified against the actual file/filesystem/script before
committing — none applied from a report's claim alone.

---

## 1. Briefing Freshness

**BRIEFING-CURRENT-STATE.md's STATUS BANNER**: "Last Updated" reads August 12 (~5 days), but that
was a **CIO-lane-only touch** ("freeze monitor live in production... Engineering/CI/backlog state
below NOT re-attested this pass"). The last full engineering/CI/backlog attestation in the banner
chain is **Lead Dev's July 26 entry — 22 days old**. This is a real staleness gap, not a false
alarm from the SessionStart hook's known date-quirk (checked the in-file date directly, not the
hook). **Flagged to Lead Dev** — outside Docs's visibility to refresh; not touched.

**Docs's own surfaces** (`BRIEFING-ESSENTIAL-DOCS.md`, `ROLE-PORTFOLIO-DOCS.md`): both current
(`last_verified`/`last_updated` 2026-07-30, 18 days, under the 21-day threshold). No action needed.

## 2. Doc Currency Check (`scripts/check-staleness.py`)

**Ratio: 24 of 37 operating docs need attention** (23 stale + 1 no-dates), 13 OK.

**The clustering anti-pattern the checklist warns about is confirmed still present**: **20 of 23
stale docs (87%) share the identical `last_verified: "2026-06-19"` stamp.** This is the *same*
cluster Arch/CIO found and flagged on 2026-07-30 (documented in `ROLE-PORTFOLIO-DOCS.md`, which
recorded it as "31 of 36... a bulk stamp, not 31 verifications"). **Three weeks later, the cluster
is essentially unchanged** — a handful of individually-touched docs (ROLE-PORTFOLIO-CIO, PA) moved
off the stamp; the bulk of essential briefings and agent-protocols did not. The July 30 finding
diagnosed the mechanism correctly (bulk stamp ≠ verification) but the *fix* — a real per-doc
weekly-refresh discipline — still hasn't materialized for the 20 affected docs.

**Not personally bulk-refreshed**: per the checklist's own rule and CLAUDE.md's role-ownership
discipline, `last_verified` should only move on a doc actually re-verified by someone with
standing to attest its content. Docs's own two surfaces are current; the other 20 are each
another role's content and are flagged, not silently touched.

## 3. Link Integrity — repo-wide (not just priority files)

Ran a repo-wide sweep (subagent, read-only) rather than just the priority ADR/pattern/briefing
set the checklist names, since last week's #1584 work already covered those closely.

**63 broken links found across 33 files** (after excluding 22 false-positive regex matches —
code snippets, template placeholders — verified by inspection). **Fixed 7 high-confidence ones
this session** (all independently verified via `os.path.exists()` before committing, not applied
from the report alone):

- **ADR README** (`adrs/README.md`): total-count claim was wrong (74/000-073 claimed; actual is
  78 numbered files spanning 000-079 with 2 gaps at 067-068) — replaced the static number with a
  verify-yourself pointer, consistent with the count-rot-removal practice from last week's scrub.
  ADR-070's link was a genuine rename, fixed. **ADR-071's entry was actively wrong** — it described
  "Connector Registration Pattern" and pointed at a filename that never existed; the real
  `adr-071-user-auth-anchoring-pattern.md` is a completely different topic (content-store
  ownership, not connector registration). Corrected the entry to describe what the file actually
  contains rather than guessing a mapping — flagging this explicitly since it's the kind of
  silent-drift the audit exists to catch.
- One off-by-one directory-level link (PDR catalog reference) and one wrong-depth link
  (`pytest.ini` reference in the CI runbook) — both mechanical, both verified before fixing.
- **3 dead links in `methodology-core/INDEX.md`** pointing at a `/methodology/` Python package
  deleted 2026-07-26 (Arch's fix-or-delete ruling, ADR-028 superseded, zero importers) —
  repointed to the preserved design record rather than left dangling.

**Not fixed this session, tracked as residual** (56 of the 63): the `legacy-getting-started/` and
`legacy-user-guides/` clusters (25 links, all pre-reorg PM-034/architecture-dir dead references —
same class already flagged as residual in #1584 and now excluded from the public site build, so
lower urgency); 5 phantom screenshot references (already tracked from last week); a scattering of
single-instance dead links in design docs, PDR-003, omnibus-logs (2026-01-04, historical record —
not touched per session-log-preservation norm), and internal tooling docs — filed as a tracking
issue rather than fixed ad hoc (see §8).

**Separately flagged, not a filesystem break**: Comms's 08-13 finding of 18 links on KEEP-scoped
pages pointing at now-site-excluded content — those resolve on disk but will 404 once Jekyll
rebuilds. Still open per that thread; not re-litigated here.

## 4. Cross-Reference & Completeness Checks

- **methodology cross-references**: 66 checked (60 markdown links + 6 wikilinks) + exhaustive
  bare-number-reference sweep (`methodology-NN`, `m-NN`) — **0 broken**.
- **INDEX.md completeness**: **methodology-48 and -49 were missing from the catalog** — filed
  2026-08-10 and 2026-08-12 respectively, never added to `INDEX.md`. Same exact gap-shape as the
  one the Aug 10 audit fixed for 43-47 (a doc's own footer documents the prior fix). **Fixed** —
  both entries added, statuses/attributions verified against the actual files.
- **NAVIGATION.md**: one stale count ("48 development methodologies," actual is 50 files, now 51
  after m-48/49's proper filing) — dropped per the same count-removal practice used elsewhere in
  this doc last week. **More significantly: NAVIGATION.md's "Essential Briefings" quick-start list
  was missing Web (active since ~June) and ETA (dormant, but roster-listed) entirely** — 10 of 13
  roster roles listed, not a stale count but a genuine omission. Fixed. **CLAUDE.md's own role
  table had the same gap for ETA** — fixed there too.
- **Briefing completeness vs ROSTER.md**: all 13 roster roles have a corresponding briefing file
  and vice versa — clean, no fixes needed (the omission was in the *derivative* quick-start lists,
  not the roster/briefing pairing itself).
- **Duplicate files**: 5 same-basename clusters found (excluding 89 legitimate README.md
  instances) — 4 already reconciled or confirmed-not-duplicates per last week's #1585 work
  (spot-checked, still holding). **1 still open**: `universal-list-architecture-guide.md` exists
  at two paths with diverged content, both from a September 2025 reorg, no canonical marker in
  either. Flagged to Lead Dev (technical-implementation content, outside Docs's lane to arbitrate)
  rather than guessed at.

## 5. Omnibus Coverage — a real gap found and being closed

**Unbroken coverage 2026-07-27 through 2026-08-13** (18 consecutive days). **Genuine gap: 08-14,
08-15, 08-16 have no omnibus despite real, heavy session-log activity** (15/17/15 role logs
respectively) — not a quiet-period false positive. This is Docs's own cadence lapsing while
attention went to the docs-site scrub (08-14), a lighter Saturday (08-15), and two publishes plus
a confabulation-report catch (08-16). **Backfill in progress**: one-day-per-subagent, sequentially
(the pattern PM endorsed for the earlier 5-day gap), starting with 08-14. Will report completion
separately as each lands rather than holding this issue open for it.

## 6. Sprint & Roadmap Alignment

- `roadmap.md`'s header states "Date: July 16, 2026" but the file's git history shows a touch on
  **August 6** not reflected in the header/changelog trail — a real discrepancy, flagged to PPM
  (roadmap owner) rather than guessed at or silently stamped.
- GitHub issues: **313 of 314 open issues carry a milestone assignment** (the one exception is
  this audit issue itself, which is expected — audit issues aren't milestone-scoped). Ran via
  paginated REST after GraphQL returned intermittent 503s this session (noted for awareness, not
  actionable — transient GitHub-side).

## 7. Pattern Catalog & Quality Checks

- **Pattern count verified exact**: 75 files (000-074), zero gaps, zero duplicates — matches
  README's claim precisely. No fix needed.
- **CITATIONS.md**: 578 lines, no incompleteness markers found on inspection.
- **Root README.md + docs/README.md**: both clean. Root README's Apache 2.0 badge now matches a
  real `LICENSE` file at repo root (resolves an earlier-flagged concern about a license badge with
  no backing file). docs/README.md was scrubbed in depth last week (08-12) as part of the
  docs-site work and remains current. No "NEW:" staleness, no version mismatch (both README and
  `pyproject.toml` agree on v0.8.11.0).

## 8. Discovered Work — tracking issue

Filed as **#1644** for the residual link-integrity items (56 of 63, §3) and the roadmap-date
discrepancy (§6) that don't have an obvious single owner or safe unilateral fix.

---

## Completion Matrix

| Section | Status | Evidence |
|---|---|---|
| Briefing Freshness | ✅ | §1 — real gap found (22-day engineering staleness under a 5-day banner), flagged to Lead Dev |
| Link Integrity Check | ✅ | §3 — 63 found, 7 fixed + verified live, 56 tracked (issue filed) |
| Omnibus Coverage Check | ✅ | §5 — genuine 3-day gap found, backfill in progress (sequential, per established pattern) |
| Sprint & Roadmap Alignment | ✅ | §6 — roadmap date discrepancy flagged to PPM |
| GitHub Issues Sync | ✅ | §6 — 313/314 milestone coverage verified via REST (GraphQL 503s this session) |
| Pattern & Knowledge Capture | ✅ | §4, §7 — INDEX.md gap fixed (m-48/49), pattern count exact, CITATIONS spot-checked |
| Quality Checks (root README.md) | ✅ | §7 — clean, LICENSE/badge mismatch resolved |
| Quality Checks (docs/README.md) | ✅ | §7 — clean, already current from last week's scrub |
