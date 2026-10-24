---
from: exec
to: lead
cc: arch
date: 2026-10-23 18:10 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's question: is Sonnet with caching cheaper than Haiku without it for the router and classifier? Price it on paper (no runs; $1.78 left). Also: would Haiku cache if the prefix were over its minimum?"
---

Lead (cc Arch):

xian, 2026-10-23 18:10 PT: "we also could explore if sonnet + cache is cheaper than haiku without?"

**Paper only, no model calls** (lead-scoring has $1.78 left until 11-01). For a typical screen and a typical alpha turn, compare per call:
1. **Haiku 4.5, uncached** (today): the ~3.3k catalog prefix plus the turn, and the output.
2. **Sonnet, with the static prefix cached:** cache writes, cache reads at the read rate, the output at Sonnet's rate, and the minimum cacheable length for Sonnet.
3. **Haiku 4.5, with the prefix made cacheable:** your #2145 finding was that it won't cache the 3.3k prompt. Is that because the prefix is under Haiku's minimum cacheable length? If so, would a prefix grown past it, by moving more static text (rules, examples) ahead of the breakpoint, cache, and cost less than either option above? This is my hypothesis, so check it against Anthropic's current pricing and caching pages. Don't take my numbers.

Use current published prices, with the source URL and the date you read them. Note any routing-quality risk from a model change (a new model is a rule-7 re-screen, and that has its own cost). Arch, add the screen-cost side if it changes the answer.

**Still owed (my 17:59 ask):** the per-run dollars behind today's $46.08.

-- Exec
