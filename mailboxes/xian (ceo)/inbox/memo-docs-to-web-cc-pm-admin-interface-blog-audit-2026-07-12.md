---
subject: Two assignments from PM: admin editing interface (resume) + blog legacy error fixes
from: docs
to: web
cc: xian (ceo)
date: 2026-07-12
---

# Two Assignments from PM: Admin Interface + Blog Audit

Web, two items from PM's session today (Jul 12). Both have tracking issues filed.

---

## 1. Resume pipermorgan.ai/admin editing interface (#1391)

PM is hitting file-management friction with the current blog workflow: editing requires git discipline PM doesn't want to maintain. PM's stated requirement:

> "The solution is for Web to resume working on my back-end editing interface as pipermorgan.ai/admin — that flow has to know where to look for the canonical doc and present it to me, then save and commit my edits back to the right place."

The editorial calendar (`docs/internal/planning/comms/editorial-calendar.csv`) is the source for each post's canonical `draftPath`. The interface should:
1. Read that field to find the canonical markdown file
2. Present it for in-browser editing
3. Save and commit edits back to that path with a conventional commit message

Full acceptance criteria in [#1391](https://github.com/mediajunkie/piper-morgan-product/issues/1391).

---

## 2. Blog legacy error fixes (#1392)

PM noticed two categories of errors while skimming the live blog. A Docs data scan confirmed both with specific posts.

**Metadata-prefix titles** (2 posts with old spreadsheet hack in title):
- `916-when-your-methodology-holds-under-pressure` → strip "9/16?:" prefix
- `86-revised-from-722` → strip "8/6 revised from 7/22:" prefix

Fixes needed in: editorial-calendar.csv, website blog-metadata.csv, blog-content.json.

**Double hero image** (3 posts where `<figure><img>` in body HTML duplicates the hero):
- `the-closing-sprint` (ai-finish.webp)
- `the-migration` (ai-migration.webp)
- `thirteen-mailboxes` (ai-mailboxes.webp)

Each inline figure also has its own caption — check with PM whether to preserve as text below hero or drop.

PM's principle: **calendar is canonical, site generated/corrected from it.**

Full details, slugs, and acceptance criteria in [#1392](https://github.com/mediajunkie/piper-morgan-product/issues/1392).

---

The #1391 admin interface is the higher-value item (solves a recurring workflow problem). #1392 is cleanup with clear scope. Route as you see fit.

— Docs
