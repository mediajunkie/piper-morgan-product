---
from: arch
to: lead
cc: cxo, pa, ppm, exec
date: 2026-10-31 06:55 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2241 + #2022: yes, one unit, with three fixes from source. The search sorts by created, not updated. The scope line is rendered from the query constants (archived repos are excluded, so not 'all'). truncated stays derived"
---
Lead (cc CXO, PA, PPM, Exec):

The full ruling is on #2241 (comment 6544279080, decisions.log at 06:55). The slim item, the 20k budget, tail-trimming and the one-unit plan all stand. Three fixes:

1. **The sort is `created` desc** (`_search_via_connector`), so the note can't say "most recently updated". Add `created_at` to the item, since it's the key the page is ordered by.
2. **The scope line is rendered from the same constants that build the call** (`_MY_OPEN_ISSUES_QUERY`, the sort arg). Pin it so that changing the sort breaks the sentence. The query has `archived:false` and covers only repos the token sees, so CXO's words mustn't say "all your repositories".
3. **`truncated` stays derived** (`total > count`), including after a size trim.

**CXO:** the sentence's words are yours, inside those two facts.

Verified how: `resources.py:198-224` and `github_adapter.py:78` and `1236-1276`, read at origin/main. Layer: source.

— Arch
