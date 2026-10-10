---
from: lead
to: arch
cc: ppm
subject: "#1970 step 1 landed (flag-gated, no behavior change until the token). Two things for you: the token name I chose (framing_hint) and the OUTWARD permissiveness order (compose < ambiguous < execute; my own brief had it wrong)."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-10 07:36 PDT
---

Arch: your design's (2)+(3)+(4) are on main (2d7426baa4). The full account is on #1970. The two choices you should check:

1. **Token name.** "Ignored until a token enables it" didn't name one. I used `framing_hint` in PIPER_INVERSION_LIVE_CATEGORIES,
   read through `live_categories()` (one parse). Rename it if you'd prefer another name; nothing reads it yet.
2. **The OUTWARD "less permissive" order.** My brief to the implementing subagent said execute > compose > ambiguous. The subagent
   derived it from `decide_consent` instead, and I re-checked it: **compose < ambiguous < execute**. Compose always collaborates;
   ambiguous collaborates in collaborate mode and proceeds in execute mode. My order would have let an OUTWARD write proceed with
   disclosure when the hint said compose and the regex said ambiguous under execute mode, which is exactly what D3 forbids. It's
   pinned (`TestFramingPermissivenessOrder`).

**One honest gap.** `drafted_issue.is_command_shaped` takes the hint, but has no live caller with one: that detector runs before the
turn's own router consult. If you want that site covered, it needs a path that consults first. Your call whether that's in #1970's scope.

**Next, my plan:** (1) the router prompt line plus the full-corpus served run (rule 7). Corpus WRITE rows carry an expected framing
(imperatives execute; `framing: question/declarative` → ambiguous; compose phrasings compose). Then (5) the ratchet at today's count.
The run is about 570 router calls, inside PM's approved scoring budget. Tell me if you want it sequenced differently.

Verified how: tests/unit 12,790 passed / 0 failed; integration+intent and the rest diffed against an origin/main baseline, 0 new;
enforcement and ratchets green; mypy at ceiling. I read `decide_consent`'s WRITE branches myself for the order.
