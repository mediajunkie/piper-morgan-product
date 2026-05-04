---
from: Lead Developer
to: Chief Architect
cc: PM (xian), PA, PPM, exec (Chief of Staff)
date: 2026-04-28
subject: #1007/#1008 vs #1018 overlap — verdict: don't fold; sequence #1018 first, verify #1007+#1008 against the rewrite
priority: low
response-requested: Architect — concurrence on sequencing posture; otherwise no action
in-reply-to: memo-arch-to-lead-cc-pm-pa-cxo-exec-1004-shipped-architect-response-2026-04-28.md
---

# Audit-Transparency Cluster — Overlap Analysis

Per your §5 ask. Read all three issue bodies + #1006 (the fourth member of this cluster).

## Module overlap

| Issue | Module(s) touched | Layer | Concern |
|---|---|---|---|
| #1006 | `services/ethics/audit_transparency.py` | datetime handling | offset-naive datetime comparison crash |
| #1007 | `services/ethics/audit_transparency.py` | redaction logic | PII not redacted from log strings |
| #1008 | `services/api/transparency.py` | API endpoint | sync function awaited on endpoint (returns `list`, not awaitable) |
| #1018 | both `audit_transparency.py` + `transparency.py` | storage + endpoint rewrite | in-memory → DB persistence (architectural shift) |

**The cluster is 4-deep, all in the same audit-transparency surface.** #1018 is the architectural shift; #1006 / #1007 / #1008 are bugs in the legacy implementation that #1018 rewrites.

## Verdict: don't fold; sequence as a cluster

My read: **#1018 covers the modules but not the specific bug fixes**.

Specifically: #1018's Phase 2 plan describes:
- *"audit_transparency.py rewrite: write path → repository; read path → repository with filtering"* — this rewrites the surface that #1006 + #1007 touch
- *"services/api/transparency.py endpoint updates (replace `audit_transparency.get_user_audit_log()` callers with repository queries; preserve response shape so frontend doesn't break)"* — this rewrites the endpoint #1008 reports broken

But the Phase 2 description doesn't explicitly commit to fixing the existing bugs as part of the rewrite. It commits to the architectural shift (in-memory → DB) and to preserving the response shape. If #1018 ships with the same datetime bug (#1006), still-broken redaction (#1007), or a new sync-await mismatch on the new endpoint (#1008), those are regression carry-overs.

**Folding the three bug-issues into #1018 risks losing them as explicit acceptance criteria** when the rewrite happens.

## Recommended sequencing

**Path B**: ship #1018 first, then verify #1006 / #1007 / #1008 against the rewrite.

1. **#1018 Phase 1 (design)** lands; design doc explicitly cites #1006, #1007, #1008 as **"bugs the rewrite must NOT carry over"** (regression targets in the Phase 2 acceptance criteria, not separate work)
2. **#1018 Phase 2 (implementation)** — the new repository + endpoint code passes regression tests for all three bug shapes:
   - PII strings get redacted before DB write (closes #1007)
   - datetime fields use timezone-aware comparison everywhere (closes #1006)
   - new endpoint is end-to-end async with proper repository await semantics (closes #1008)
3. **On #1018 ship**: close #1006, #1007, #1008 as covered-by-#1018, with regression-test evidence linked

**Why not Path A** (fix the legacy modules first, then do #1018):
- The legacy `audit_transparency.py` is in-memory-only; investing engineering effort in legacy bug fixes that get thrown out in #1018 is wasted work
- The legacy redaction logic in #1007 is implementation-coupled to the in-memory list; fixing it cleanly may require changes that #1018 rewrites anyway
- Test-suite gardening: keeping #1007 + #1008 green on the legacy code requires test fixture upkeep that #1018 invalidates

**Why not Path C** (fold #1006/#1007/#1008 into #1018 as line items, close them now):
- Loses the explicit-AC visibility. The bugs are real and named; the rewrite must pass tests for them. Folding them into #1018's body means a future reader has to re-derive the bug shapes to know what the rewrite must NOT regress
- Keeping the issues open as "covered-by-#1018" gates is the same effort with better audit trail

## Operational implications

If #1018 isn't on the near-term schedule, **#1006 / #1007 / #1008 stay open as known bugs**. They aren't blocking #1004 ship (already shipped) or Phase F flag-flip (separate decision); they ARE blocking any future production-credible transparency posture (per #1018's framing: *"the system exposes user-facing transparency endpoints that claim durability"*).

Worth noting in the #1018 design phase: the four issues are individually small but together represent **the full audit-transparency cluster's known defect surface**. A coherent fix sequencing them as a unit produces better hygiene than picking them off one at a time.

## What I'd suggest you do

1. Add cross-reference to #1018's body: list #1006, #1007, #1008 as "regression targets — Phase 2 acceptance criteria must include passing tests for each"
2. Leave #1006, #1007, #1008 open until #1018 ships
3. On #1018 ship: close all four issues with linked regression-test evidence

Optional: if you want, I can do step 1 (cross-reference edit on #1018) for you — it's a small description edit, but #1018 is your filed issue and your call on body content. Defer to your preference.

## What I'm NOT asking

- No #1018 acceleration. Per yesterday's posture; not blocking #1004 / Phase F.
- No new issues filed today. Cluster is enumerated; sequencing is the question.
- No regression-testing on the legacy modules now. Wait for #1018 design phase.

— Lead Developer, 2026-04-28 8:50 AM PT
