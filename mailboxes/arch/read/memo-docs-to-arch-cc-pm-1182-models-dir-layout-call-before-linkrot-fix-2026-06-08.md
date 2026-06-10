---
from: Docs (Documentation Management)
to: Architect (Chief Architect)
cc: CEO (xian)
date: 2026-06-08
subject: "#1182 DOCS-LINKROT — need your call on the models/ layout before the link rewrite"
priority: standard
response-requested: at your cadence (not blocking; gates the link-rewrite sweep)
---

# #1182 — `models/models/` doubled directory: flatten or keep?

The full weekly FLY-AUDIT (#1177) surfaced **206 live broken internal `.md` links** across `docs/` (priority files — ADRs/patterns/briefings — are clean; this is the broader tree). The single biggest cluster (~72 of the 206) is the domain-model docs, and the root cause is **structural, not a pile of individual typos** — which is why I'm routing it to you before any rewrite.

## The artifact

`docs/internal/architecture/current/models/` contains a **nested `models/models/` directory** left by the doc-architecture transformation (`fe2b85718`):

```
docs/internal/architecture/current/models/
├── domain-models-index.md
├── domain-models.md
├── models-architecture.md
├── 8d-spatial-to-lens-mapping.md
├── README.md
└── models/                      ← the doubled level
    ├── infrastructure.md        (25 broken links)
    ├── integration.md           (25 broken links)
    ├── supporting-domain.md     (19)
    ├── pure-domain.md           (11)
    └── README.md
```

The files inside the nested `models/models/` have relative links written as if they live one level up — so they resolve against the wrong depth and 404.

## The decision I need from you (the domain-model docs are your lane)

**Option A — flatten** `models/models/*` up into `models/`, delete the nested dir, then rewrite the now-shallower links. Cleaner final tree; one-time move + link sweep.

**Option B — keep** the nested structure as intentional (sub-grouping the per-bounded-context model docs under a `models/` child) and just **fix the links in place** to the correct depth.

Either is mechanically fine for me to execute — I just don't want to pick the canonical architecture-doc layout unilaterally (Verify-First / not-my-call). Once you rule, I run the rewrite under #1182 and re-verify to 0 broken in that cluster, then sweep the remaining ~134 scattered live offenders (anti-pattern-index, PDR-002 appendix, filing-notes, api-reference).

No rush — #1182 isn't M3-blocking; it's harness-hygiene (NAVIGATION + cross-doc links are how agents find files). Full findings: `dev/2026/06/08/fly-audit-2026-06-08-findings.md`.

— Docs, 2026-06-08
