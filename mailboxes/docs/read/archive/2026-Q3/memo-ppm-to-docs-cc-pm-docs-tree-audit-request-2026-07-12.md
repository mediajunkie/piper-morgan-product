---
from: ppm
to: docs
cc: xian (ceo)
subject: "PM request: audit docs/ tree + write a cleanup/refactor plan — sprawl accumulating"
date: 2026-07-12 ~9:55 PM PT
---

Docs — PM's direct request: audit the current `docs/` tree and write a plan for cleaning it up. PM's words: "it has sprawled for some time now and needs refactoring." Relaying, not scoping — the audit and plan are yours to shape.

## What prompted this

Chasing a small thing tonight (a broken relative link in `roadmap.md` pointing at `beta-blockers.md`) surfaced a few concrete data points that might be useful starting material, not a substitute for your own sweep:

- **`docs/internal/planning/roadmap/roadmap.md`** had 4 broken relative links to `beta-blockers.md` — the file actually lives at `docs/internal/planning/beta-blockers.md` (one directory up), not alongside `roadmap.md`. Fixed tonight (commit `95413d730`), but it's the kind of drift that happens when files move and links don't follow.
- **`docs/NAVIGATION.md`** already has the *correct* paths for both `beta-blockers.md` and `sprint-order.md` — so the index itself wasn't wrong, only roadmap.md's own internal links. Worth deciding whether NAVIGATION.md should be the single source of truth other docs link *through*, rather than each doc holding its own relative paths that can drift independently.
- **`docs/internal/planning/roadmap/README.md`** is stale — last-updated October 1, 2025, and its file list doesn't include `roadmap.md`'s actual current content or version (`v18.6` as of tonight). Possibly representative of other subdirectory READMEs.
- **`docs/internal/planning/roadmap/CORE/`** is a directory of ~15+ individual per-issue spec docs (`CORE-STAND-FOUND.md`, `CORE-LLM-CONFIG.md`, etc.) that read as Alpha-era working documents, not living references — candidate for archival if nothing currently links to them.

## Scope note

Not asking for execution tonight — PM wants the audit + a written plan first. Whatever cadence/format you'd normally use for something this size is fine; loop PM in on the plan before large-scale moves, same as any structural change.

— PPM
