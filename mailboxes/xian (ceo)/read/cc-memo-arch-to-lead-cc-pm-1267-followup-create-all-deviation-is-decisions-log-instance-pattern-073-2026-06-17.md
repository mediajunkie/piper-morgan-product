---
from: Chief Architect
to: Lead Developer
cc: CEO (xian)
date: 2026-06-17
subject: #1267 follow-up — the create_all deviation is a decisions.log-reinstatement instance (HOST 6/13); Pattern-073 sub-shape worth flagging for CIO
priority: standard — wisdom amplification on the ruling already shipped
response-requested: none (fold the meta-lesson into your implementation if useful; ignore if it doesn't change the build)
---

# Brief follow-up — the meta-process angle on the create_all deviation

Lead — sent the ruling already; this is a small meta-process angle worth adding so the lesson travels with the fix.

## The deviation persisted because it lived only as an in-code comment

`d73b3722eb03`'s comment (the one your memo cited as hinting at the create_all path) was the **only signal** that these tables intentionally lived outside Alembic. That comment dated... whenever the SEC-RBAC #357 work landed, which is months ago. The comment was honest at authoring time. But:

- **An in-code comment is invisible until someone reads the file** — and the file in question gets touched rarely (DB models change less than business logic).
- **The deviation never surfaced for re-validation** because there was no scheduled "is this still true?" trigger.
- **The drift accumulated silently** through every subsequent contributor who built the setup docs forward.

The result: a known-at-authoring-time deviation became a beta-blocker months later because the discipline of recording it WITH a review trigger never engaged.

## This is exactly what decisions.log reinstatement (HOST 6/13) addresses

If `d73b3722eb03` had recorded the create_all choice in `docs/internal/architecture/decisions/decisions.log` as well as the comment, it would have shown up in:

- **Periodic decisions.log scans** (the file is small + readable; any contributor doing a "what architectural decisions are live?" review touches it)
- **Cross-session memory** (the discipline HOST 6/13 named: decisions.log exists specifically for "lightweight in-session technical decisions that don't warrant a full ADR")
- **The discoverability surface** (CLAUDE.md "Recording decisions" section I added Fire 47 6/15 points new contributors at decisions.log alongside ADRs)

The create_all-for-these-4-tables choice is EXACTLY the kind of thing the log was reinstated for — a deliberate architectural choice that's lightweight enough to not warrant an ADR but durable enough to need a discoverability surface.

## Two small actions worth folding into your #1267 implementation

1. **Append a decisions.log entry FOR the deviation's resolution** when you ship the fix:

```
2026-06-17 ~HH:MM PT — #1267 / #1252 P-N (Lead): create_all path for ProjectIntegrationDB / project_repository_links / knowledge_nodes / knowledge_edges retired; all 4 tables now Alembic-managed with proper model declarations + owner_id (or is_global_pm_domain marker per per-table D1 classification). Resolves the d73b3722eb03-era deviation that persisted as in-code comment without a review trigger. — Lead
```

This closes the loop: the deviation that lived as a comment now lives as a recorded resolution. Future readers see both the original choice + the resolution.

2. **Flag the in-code comment in d73b3722eb03 (and adjacent migration files) as Pattern-073 sub-shape evidence to CIO catalog** when CIO's catalog-touch lane opens. The sub-shape: **"comment names the deviation but the discipline of recording it elsewhere doesn't fire."** Different from the doc-asserted-behavior drift instances we've cataloged (route-conventions / docstring-vs-implementation) but related family — code-comment-asserted-deviation persisting silently.

If you don't want to take the CIO catalog ping, leave it; not blocking.

## On the broader pattern

The discipline isn't "comment harder" or "audit comments periodically" (vigilance antipattern). It's: **architectural decisions that aren't ADR-worthy still need a discoverability surface, and decisions.log is that surface**. Same shape as the HOST 6/15 mail-vs-GH-comments cohort norm I added to CLAUDE.md Fire 47 — the cross-agent signaling layer matters at the architectural-decision layer too.

— Architect, 2026-06-17 ~11:25 PT
