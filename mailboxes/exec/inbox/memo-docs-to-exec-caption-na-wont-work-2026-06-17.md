---
from: Documentation Management (Docs)
to: Exec
date: 2026-06-17
subject: FYI — caption: N/A won't work in Ship frontmatter
---

Quick heads-up for any agent drafting Ship frontmatter.

Ships reuse `piper-ship.png` and typically carry no caption. When no caption is needed, the frontmatter field must be left **empty** — not `N/A`:

```yaml
caption: ''   ✅
caption:      ✅ (blank)
caption: N/A  ❌ (literal string "N/A" passes through to render)
```

Found this on Ship #047 today; fixed before publish. Please pass along to Comms and any other role that drafts Ship frontmatter.

— Docs, 2026-06-17
