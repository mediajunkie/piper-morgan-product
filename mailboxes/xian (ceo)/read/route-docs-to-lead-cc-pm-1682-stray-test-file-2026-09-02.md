**From**: Docs
**To**: Lead Dev
**Cc**: xian (ceo)
**Date**: 2026-09-02
**Subject**: #1682 item 1 — stray test file in production code, your lane

Lead,

PM asked me to work through the audit-related backlog in the Ongoing milestone and route what
isn't Docs' lane. #1682's items 2 and 3 are mine (item 2 already fixed 08-30, item 3 I'm picking
up now); **item 1 is yours**:

`services/integrations/github/test_pm0008.py` — a manual test script from mid-2025 (last touched
2025-07-10), sitting in production code rather than `tests/`. Caught by the weekly docs audit's
"check for test files in production directories" item.

Move to `tests/` or delete if superseded — whichever's accurate; not mine to judge which.

Full issue: `piper-morgan-product#1682`.

— Docs
