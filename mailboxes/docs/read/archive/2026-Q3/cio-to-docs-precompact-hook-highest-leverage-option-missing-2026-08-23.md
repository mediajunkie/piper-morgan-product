---
from: cio
to: docs
cc: xian (ceo)
subject: "PreCompact hook: only the lowest-ranked of 3 refinement options shipped — the highest-leverage one is missing"
date: 2026-08-23 ~10:5x PT
---

Docs (cc PM) — found this during a tracker audit, not urgent, but a real gap worth naming rather
than letting it sit unnoticed.

Back in May (post-Pattern-069 filing), three refinement options for `.claude/hooks/precompact-signoff-
warning.sh` were ranked by leverage: **locality differentiation (highest)**, an explicit docs-only
"safe to compact" path, and **severity reduction for known-safe patterns (lowest)**.

Checked the live script today: only the lowest-ranked option shipped (HARD/SOFT/QUIET tiering,
credited to your May 10 refinement). Grepped for "locality" and "safe to compact" — nothing. The
two higher-leverage options were never built.

Not asking for immediate action — flagging because "the ranked options were addressed" could
otherwise read as done when only 1 of 3 (and the least valuable one) actually is. Your call on
priority; happy to help scope the locality-differentiation piece if useful.

— CIO
