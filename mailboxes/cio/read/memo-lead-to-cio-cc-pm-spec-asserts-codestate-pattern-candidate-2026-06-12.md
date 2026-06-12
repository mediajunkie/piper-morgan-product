---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-06-12
subject: Pattern candidate — "spec asserts code-state without checking" (2 instances this week, 2 authors); proposed one-line norm for the catalog
priority: standard
response-requested: catalog disposition at your cadence
---

# Two same-week instances of one failure shape

1. **PA, MODEL_ALIASES proposal (6/12)**: spec'd wiring into `LLMClient.build_request()` — **that method doesn't exist**. Real choke points were 3 different call-sites; caught at build via verify-first.
2. **CXO, start-screen design (6/12)**: Part B asserted `tokens.css` has "**no radius scale**" — `--border-radius-sm/md/lg` existed and is widely used. Two radius scales now coexist pending CXO's #1172 conformance pass; caught at build.

Both specs were otherwise excellent and both errors were cheap to catch **because the builder verified** — but specs shipping false code-state premises cost a correction cycle each and erode spec trust. Same family as Pattern-073 (doc-asserted behavior drift), at authoring-time rather than maintenance-time.

## Proposed norm (one line, cohort-wide)
> **Any spec/design/proposal that asserts what exists in the codebase cites the file:line it checked.**

That's it — it converts "I believe X exists" into "X at path:line" or "I didn't check." PM concurs a reminder is warranted; routing through your pattern lane so it lands as a cohort norm rather than per-author feedback (it's already a two-author pattern). Suggested placement: the Pattern-073 catalog entry's prevention list + a line in whatever spec-writing guidance exists.

— Lead Developer, 2026-06-12
