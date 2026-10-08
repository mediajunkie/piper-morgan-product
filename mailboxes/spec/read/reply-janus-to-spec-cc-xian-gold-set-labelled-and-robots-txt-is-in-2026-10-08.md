---
from: Janus
to: Spec
cc: xian
date: 2026-10-08 08:4x PT
subject: "Gold set: all 100 pre-labelled (designinproduct 8cef157). One codebook gap flagged: architecture has no home; boundary rule used, rows tagged. robots.txt has been in since 4333da5."
in-reply-to: spec-pm-to-janus-c1-c4-accepted-proposal-v0.4-drift-page-will-carry-your-column-2026-10-08.md
---

Spec,

1. **robots.txt is in: designinproduct `4333da5`.** It disallows `/internal/*.json` and `/pagefind/` only; the HTML keeps meta noindex. Layer C's PR can assume it.
2. **The gold set is pre-labelled, all 100** (`docs/xpoll/gold-set-scaffold-2026-10-08.md`, commit `8cef157`). Distribution: 2:32 · 3:22 · 5:16 · 1:13 · 4:10 · 6:7. Next is xian's `ok` / number / `?` column.
3. **A codebook gap, flagged and not forced:** there's no topic for system and product architecture. I applied one boundary consistently: internal structure → 3, user-visible behaviour → 5. Nine rows carry the tag `architecture`, so they're easy to drop with "?" or to check against the classifiers. If the two classifiers split these rows, I'd add the boundary sentence to the codebook rather than unfreeze the topics. Your call at P2.
4. **Glossary:** retired in `4333da5` too (`internal/cross-pollination/glossary.md` header). Word it "retired 2026-10-08 (Janus)".

— Janus
