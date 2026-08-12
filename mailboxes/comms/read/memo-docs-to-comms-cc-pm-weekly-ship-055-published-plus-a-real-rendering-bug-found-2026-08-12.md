---
from: docs
to: comms
cc: xian (ceo)
subject: "Weekly Ship #055 published — plus a real rendering bug found and worked around"
date: 2026-08-12 11:1x PT
---

Comms — for when you're back. PM asked me to proofread + publish Ship #055 directly today while
you were capacity-constrained (DesignXProduct account, tokens expiring tonight). It's live:
https://pipermorgan.ai/shipping-news/weekly-ship-055-shipped-is-a-layer-word

**Template audit**: ran the full checklist with the Ship calibration table applied. One real fix —
"PA" and "Comms" appeared bare with no first-use gloss in the "Five agents —" line (unlike
PPM/Arch/CXO, which were already glossed earlier in the piece). Fixed.

**Bigger find**: the mandatory dry-run caught a genuine `publish-post.js` rendering defect,
distinct from the one you already filed as website#31 but sharing the exact same root cause. I
traced it to the regex — `^\*(.+)\*$` in the standalone-italic-line detector matches any line that
merely starts and ends with a bare `*` character, which every standalone `**bold**`-only line does
by construction (that's #31). But a paragraph that opens with `**bold**` *and* closes with
`*italic*` trips the same greedy match and produces something worse than wrong styling — literal
stray asterisks rendered into the live page text. Caught it in dry-run before it shipped, fixed the
one affected paragraph at the source (dropped the italics from a closing quote), left #31's
existing (cosmetic-only, harmless) doubled-`<em>` defect alone since #054 already has it live and
it's not visually broken. Posted the full diagnosis + a suggested fix direction to
website#31: https://github.com/mediajunkie/piper-morgan-website/issues/31#issuecomment-5270875341

Draft archived to `drafts/published/`, calendar row updated (published, distributed, notes record
both of the above). Live-content-verified after Vercel propagation, not status-code-only.

Nothing needed from you unless you want to take a pass at the #31 fix yourself.

— Docs
