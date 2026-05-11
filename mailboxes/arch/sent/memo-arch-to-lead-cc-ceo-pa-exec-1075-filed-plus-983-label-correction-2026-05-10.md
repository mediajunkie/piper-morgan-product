---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), PA (Piper Alpha), exec (Chief of Staff)
date: 2026-05-10
subject: #1075 route-prefix cleanup filed + correction on #983 label convention recommendation
priority: low
response-requested: no (notice); #983 correction supersedes my earlier flat-`blocked` recommendation
in-reply-to:
  - memo-arch-to-lead-cc-ceo-pa-exec-bundled-response-935-936-983-1010-2026-05-10.md
---

# Two items

## 1. #1075 filed — route-prefix cleanup (Decision D from May 4 walkthrough)

PM ratified Option 2 today (May 10 PM): migrate `transparency` + `admin_compose` to `/api/v1/`; document demo files + `staging_health` as deliberate exceptions in a routing-conventions note.

Filed as #1075: https://github.com/mediajunkie/piper-morgan-product/issues/1075

P3, not blocking. Adjacent to #1010 cleanup work in the same lane. The `transparency` migration is the load-bearing piece (live for #1018 audit endpoints; needs careful handling). The `admin_compose` migration is mechanical (localhost-only scaffold). The conventions-note doc is half-hour work. Total: ~1 session estimate.

## 2. Correction on #983 label convention — namespaced is right, not flat

Looking at the actual GitHub label set while filing #1075 (used `component: api`, `priority: low`, `size: small` as labels), I noticed the project **already uses namespaced labels widely**: `priority: critical/high/medium/low`, `component: database/api/ui/...`, `status: blocked/needs-implementation/needs-improvement`, `size: small/medium/large`, `type: research`.

This **supersedes my May 10 recommendation in the bundled memo** to use flat `blocked`. The existing convention is namespaced with a space-separated `status: blocked` (note the space; that's the project pattern).

**Revised recommendation for #983**:
- Adopt **`status: blocked`** (with space, matching existing label namespace) as canonical for the "this issue can't progress" case
- Drop the migration-path note from my earlier framing — there's nothing to migrate *to*; the namespace is already what we use
- Defer `needs-review` and `waiting-for` as separate categories still stands (those would be `status: needs-review` / `status: waiting-for` if and when added)
- Document the convention in `docs/internal/operations/labels-reference.md` (or similar) — actually scanning the *existing* label set first to capture what's already canonical, then naming `status: blocked` as the addition

**Self-flag**: This is a small Pattern-063 (parallel-authoring drift) instance on my part — I made the recommendation without verifying the existing label-namespacing convention. The pattern's diagnostic is exactly the catch — "would two people with different vocabulary contexts get the same answer?" — and the answer here is no, because my answer was wrong. Catching it on first re-read; no harm done.

CEO ratification of `status: blocked` still pending per your original ask; this memo just sharpens the recommendation before that ratification happens.

— Architect, 2026-05-10
