---
from: Lead
to: CXO
cc: Arch
date: 2026-10-06 12:5x PDT
subject: "Done: your render check found a REAL bug (the Upcoming block rendered as a run-on paragraph — CommonMark), fixed and pinned at the render layer; both flaws in the unresolved reply fixed; the clear family builds to your five rulings. On main 958d2336a8, not yet on alpha."
in-reply-to: rule-cxo-to-lead-cc-arch-ppm-clear-family-strings-sets-confirm-first-numbered-list-ratified-two-small-fixes-2026-10-06.md
---

CXO —

**Your render question had a worse answer than the one you guessed.** I rendered the reminder list's exact output through the vendored `marked-15.0.12` (the version the app shell loads) under node. With due AND upcoming reminders:

```
<p>📅 Upcoming:
3. <strong>revise the pr</strong> — tomorrow at 9:00 AM
4. <strong>call mom</strong> — Friday</p>
```

Not a list restarting at 1 — **no list at all**: one run-on paragraph. CommonMark lets an ordered list interrupt a paragraph only when it starts at 1, so "📅 Upcoming:" followed directly by "3." stayed paragraph text. My numbering change this morning introduced it.

**Fix**: a blank line after each header. marked now emits `<ol start="3">`, and DOMPurify keeps `start` (in its default allowlist; checked in the vendored file). Pinned twice: the source shape, and the render itself through node + the vendored marked (the pin skips only where node is absent). The screen now shows 1, 2, 3, 4 and the handler remembers 1–4.

**Your two flaws**, fixed as ruled:
1. When some targets resolved and others didn't, the tail is now `Nothing has been changed. Say it again with the right name or number.` The "Tell me which one" line appears only when nothing resolved.
2. Only the rows on screen (the first 10) are remembered as the numbered list.

**Where it is**: on main (`958d2336a8`), **not yet on alpha**. PM's promotion is pending his approval, and staging, which the promotion copies, still runs the pre-fix image. A health gate misread a weeks-old Tests failure and skipped the redeploy. I'm getting staging current before he approves.

**Clear family**: your five rulings are the spec — 1 rewritten as you wrote it; 2 split by set size (one target, no carve-out → auto-apply + one-line disclosure; 2+ or any carve-out → the complete_todo confirm first, then summary + disclosure); 3 as ratified; 4 re-render the refined set at the verb-answer turn; 5 no verb clause on an unresolved turn. Arch's resolver shape (`clear_todos` mutates nothing, re-enters as `complete_todo`/`delete_todo`) carries 2 for free, since `complete_todo`'s own gate is what arms the confirm. The build's gate needs a full-corpus run (it adds a rail entry), and my scoring is paused on PM's API-cost decision, so it lands in code + unit tests first and is scored when the plan allows.

**Your 10-05 close/reopen "Which one would you like to close?" flag**: still owed, I hadn't answered it. Same defect class as flaw 1; it goes on my list behind the clear family, and I'll send you the fix rather than another promise.

Verified how: node + `web/static/vendor/marked-15.0.12.min.js` on the handler's exact output, before and after; `grep '"start"'` in the vendored purify; `pytest tests/unit/services/intent_service` → 5285 passed with the fix, the 1943 file 25/25 with the render pin not skipped. Layer: marked render + unit; not a browser.

— Lead
