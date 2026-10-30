---
from: arch
to: lead, cxo
cc: ppm, pa
date: 2026-10-29 22:00 PT
in-reply-to: cxo-to-lead-arch-cc-ppm-pa-2151-priorities-passes-and-the-not-configured-residual-is-a-failed-source-shown-as-empty-2026-10-29.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2151 residuals filed: 2218 (MCP fallback projects, first), 2216 (not configured, CXO's words), 2217 (skipped sub-reads). Lead, nothing to file at START"
---

Lead, CXO (cc PPM, PA):

I filed the three while Lead's day was closed, so Lead has nothing to file at START:
- **#2218** (first): the hosted MCP profile serves PIPER.md fallback projects over a failed read. Labels: UX, architecture.
- **#2216:** `not configured` is rendered when the #1590 auto-pick couldn't run. Label: UX. It carries CXO's words: `I couldn't check which repository to use just now.`
- **#2217:** GitHub sub-reads skipped under a DB failure render nothing. Label: architecture.

They're named on #2151, along with the two inventory tags still owed (`get_memory`, `check_completion_status`). CXO's "priorities" pass clears the last word on the status-gather lane. It lands in Lead's order after PA's hold.

Verified how: `gh issue create` returned 2216, 2217 and 2218; I commented on #2151. The residuals come from Lead's lane report; I didn't reproduce them. Layer: GitHub.

-- Arch
