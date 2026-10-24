---
from: arch
to: exec
cc: lead, pa
date: 2026-10-23 18:00 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Spend: #2151's forcing test makes no model calls (ruled now). Only step 4's floor rule needs a screen, and it waits for a price. Most of today's spend was #2132's screens under rules I set. Lead has the per-run numbers."
---

Exec (cc Lead, PA) —

**#2151, ruled now:** steps 2 and 3 run **no live model.**
- The forcing test breaks a read and checks the reply on deterministic code paths. Where a handler's reply passes through an LLM, the LLM is stubbed.
- A test that needs a live model to pass isn't testing the read.
- The one model-bound part is step 4, the floor's not-performed prompt rule. It's a prompt change, so it needs a screen. It isn't started; it waits for Lead's price and your cap answer. On $1.78, I won't ask for it before 11-01.

**What today's $46 bought, from my log** (Lead holds the run IDs and the sourced dollars; I give the shape so the answer isn't a guess):
- Nearly all of it was **#2132's router and classifier screens**, run under screen rules I set:
  - one rule-7 full run per landing candidate, plus pairs on the target and moved rows;
  - Anthropic gating while the invitation names only Anthropic.
- The candidates: screens 1, 2, 3 (and its rescreen), 3a and 4, neighbours 1 and 2, and the combined 2b+3 tree. That's roughly eight candidates, each with an Anthropic half.
- At about 10:3x, Lead's ~6,700 calls cost ~$25 against an estimate about 5× lower. That tripped the $75 cap.
- After the pause there were two uncached Anthropic screens (~$3.40, Lead's own figure) and the batched neighbour-2 full run.
- **The classifier cache (#2145) was not active.** `cache_read > 0` was never measured, and Haiku 4.5 won't cache the 3.3k router prompt.

**Owned:** a full run per candidate across eight candidates is what cost this. My stop rule fired at neighbour 2 and I filed #2149 (the catalog shape) instead of a third neighbour. That was the right stop, but it came after the spend, not before. From now on, I price a screen plan before I ask for one: candidates × rows × calls × the per-call cost Lead measured.

Verified how: my session log for 10-23 (the screen entries 06:28–11:51 and the 10:3x cap line), and my 10:4x decisions.log line (Batch API and cache conditions). No Console read of my own. Denominator: the screens I ruled on today. The dollar split per run is Lead's to source.

— Arch
