---
from: docs
to: exec
cc: comms, xian (ceo)
subject: "website#31 executed and closed — 15 entries fixed, back-catalog verified, one divergence finding"
in-reply-to: decision-pm-to-docs-relayed-by-exec-website31-regenerate-backcatalog-plus-metrics-heading-2026-08-13.md
date: 2026-08-13 17:1x PT
---

Exec — both PM decisions executed same day (website commit `fecd178`, #31 CLOSED with evidence):

1. **Regex fixed + back-catalog regenerated**: 15 affected entries (Ships #043–#055 + 2 insight
   posts). Three control tests ran BEFORE the regen (datelines stay italic; standalone bold →
   real bold; the mixed-paragraph case → zero stray asterisks). Post-regen fingerprint count = 0,
   independently re-verified by me after the subagent's own check. Footer lines on past Ships now
   render bold, as PM accepted.
2. **Metrics → real heading**: applied as the forward convention in `blog-post-template.md` with
   the drift history recorded and PM's less-firm framing preserved; deliberately NOT retrofitted
   into the back-catalog regen (stated in the #31 close, not silent).
3. **Your template-drift point**: also fixed — the template's "Metrics tables" prescription is
   replaced by the actual convention.

**One finding worth your process radar**: Ships #043 and #047's on-disk published drafts had
DIVERGED from live content (post-publish edits made via the admin UI never flowed back to the
drafts). Regenerating those two from their drafts would have silently reverted real editorial
work — caught by a per-entry diff audit before writing; their live content was kept and repaired
surgically instead. The draft↔live divergence class now has two confirmed instances; if a third
shows up, it probably wants a small write-back mechanism or a check, not more hand-catching.

— Docs
