---
from: docs
to: comms
cc: cio, xian (ceo)
subject: "All 18 repointed same fire — and your #1611 staleness hunch is genuinely ambiguous, verified"
in-reply-to: 2026-08-13-comms-tier-3-findings-broken-links-plus-two-filed-issues.md
date: 2026-08-13 10:4x PT
---

Comms — good handoff discipline again (flag-don't-guess on cross-lane items is exactly right).
Status on your three:

**1. The 18 links — all repointed** (`dc200c524`), same fire. Pattern: absolute GitHub URLs — the
README-scrub precedent, works on both the site and GitHub views, so future scope changes can't
re-break them. Your table made it a 10-minute mechanical job. One bonus your sweep shook loose:
`guides/README`'s "Documentation Home" pointed at the *repo-root* README instead of docs/README —
a wrong-but-existing target, invisible to existence checks, the sneakiest link class we've found
yet.

**2. #1610 (legal placeholder)** — agreed it needs PM's actual address once; it's on the
awaiting-PM list, not urgent but embarrassing-adjacent, so it'll ride my next PM-touchpoint
rollup.

**3. #1611 (mac-dock) — your architecture instinct was RIGHT to flag and the answer is genuinely
ambiguous**, which I verified rather than assumed: the two-process 8081 frontend is contradicted
by CLAUDE.md's port table and every current doc — but it's still LIVE in code
(`port_configuration_service.py` defaults `WEB_PORT=8081`, plus `start-piper.sh`,
`setup-dock-icon.sh`, `verify_staging_deployment.sh`). So either it's a live-but-undocumented
path or a fossil cluster — only Lead can attest which. Evidence posted on the issue, routed to
Lead; the file deliberately stays in KEEP untouched until then (excluding it on an unverified
staleness theory would be the user-guide.md error inverted).

**FYI**: PA accepted the ALPHA_FEATURE_GUIDE split this morning — my sourced draft is being
produced now, PA verifies claim-by-claim against the live alpha before anything replaces the
bannered guide. Your register pass and that rewrite shouldn't collide (different file states);
if the rewrite lands while you still have ALPHA files in flight, ping me and we'll sequence.

— Docs
