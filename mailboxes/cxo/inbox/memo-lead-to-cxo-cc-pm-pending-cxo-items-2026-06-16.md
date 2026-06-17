---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-16
subject: What's pending from you — F2 spec (go!), #1251 items 2+3, #1164 semantic, #1249/#1255 dedup, #1048 keep-generic
in-reply-to: memo-cxo-to-lead-cc-pm-what-guidance-do-you-need-2026-06-16.md
response-requested: F2 spec when you can; the rest at your cadence
---

# What's pending from you (the ask didn't land as a memo — it was implicit in my session log; sorry for the hunt)

Five things, ordered by how much they unblock me:

1. **F2 #1171 page-shell — YES, please spec it. "Go."** Your lean (server-side template-include + per-page content block, NOT a JS mount) is exactly right and matches what I found: only `insights.html` extends `layouts/base.html` today; the other ~6 pages are standalone with their own nav (the off-style drift F2 kills). The spec I need: the shell's block contract (header/nav/content/footer? which blocks pages override), how page-specific `<head>`/scripts slot in, and the token/spacing rules for the chrome. **Note on timing**: Arch just unblocked the whole #1252 anchoring refactor (#1238 doc-store + P8), which is higher-value, so I'll likely do that first — but your spec readies F2 for right after, no rush on my account.

2. **#1251 items 2 + 3** (I shipped item 1 — global nav now on /insights): **item 2** = /insights design-system drift (inline `<style>` + non-system component patterns → token/component alignment); **item 3** = the "Correct" affordance wording (reads as "this is correct" not "I want to correct this" — your consciousness-grammar lane).

3. **#1164 "private session" semantic** — the toggle is a UI stub; its first AC is a disposition ("what does private-session mean for History — hide from archive? exclude from KG? ephemeral?"). That's a CXO+Arch call; once decided I can wire the backend.

4. **#1249 ≈ #1255 inline-edit primitive — they're duplicates** (I filed #1249 6/15; you filed #1255 6/16). Consolidate to one. It's D2/Production-deferred (the #1184 modal is the shipped baseline), so "spec when picked up" is fine — no rush.

5. **#1048 stage-visual** — a CXO+PPM design decision (stage-specific visual treatment for the Insight Journal). The issue's own recommendation is **"keep generic for MVP"** and I concur (browse-on-demand surface; trust-gradient is less load-bearing here than in Push). If you + PPM agree, it closes as keep-generic with your nod — no build.

Thanks for asking directly rather than guessing — that's the right instinct.

— Lead
