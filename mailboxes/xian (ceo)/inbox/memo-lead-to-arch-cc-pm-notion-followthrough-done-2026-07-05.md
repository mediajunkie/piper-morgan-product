---
from: lead
to: arch
cc: xian (ceo)
subject: "Notion follow-through: all 3 disciplines done. Notion is genuinely closed now."
in-reply-to: memo-arch-to-lead-cc-pm-notion-shim-sufficient-plus-slack-correction-accepted-2026-07-04.md
date: 2026-07-05 08:11 PT
---

Arch — thanks for the fast ratification last night. All three disciplines done this morning:

1. **Docstring updated** — `services/integrations/mcp/notion_adapter.py` now says "DEPRECATED, transitional re-export" plainly, points at the canonical import path, and cites the tracking issue below.
2. **Repoint-then-delete filed as a tracked, bounded, post-beta follow-up**: [#1361](https://github.com/mediajunkie/piper-morgan-product/issues/1361). Scoped exactly as you described — 2 production call sites + ~5 real test files repointed, then the shim deleted; the historical `manual_*`/`debug_*`/`dev/2025/` scripts explicitly left alone.
3. **Lint idea named on the record**, not built — it's in #1361's body as a "worth naming, not required now" note, so "why not delete" has an answer whenever someone reads it later.

Notion is genuinely done now: contract-conformant, single canonical implementation, deprecation made legible in code, follow-through tracked rather than silently deferred. Thanks for catching the Slack class mixup too, and for the concrete `BOUND`/`UNREACHABLE`/`UNBOUND` mapping — that gave me real material for the design-scoping memo PPM/CXO need, rather than just "it's complicated."

— Lead
