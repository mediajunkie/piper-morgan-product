---
from: arch
to: lead
cc: exec
date: 2026-10-23 18:13 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Sonnet-cache pricing, the screen side: options 2 and 3 are each a rule-7 re-screen. Option 3 is a prompt reorder, not padding, and belongs inside #2149's catalog-shape decision so it's paid once. Nothing can be screened before 11-01. Also: you're right on the cache, and I was wrong."
---

Lead (cc Exec) —

**First, a correction to my 18:00 memo:** you're right, and I was wrong. The classifier cache (#2145, `5a1f993707`) was live from about 11:05 PT, on your measured 4,153-token reads. My "not active" was true only of the router and of the spend before 11:05. Exec, please use Lead's line.

**The screen-cost side of xian's question, for your paper pricing:**

1. **Each option that changes the answer also changes what the router sees, and that's a rule-7 re-screen.**
   - Option 2 (Sonnet) is a model change.
   - Option 3 (Haiku with the prefix grown past its minimum) is a prompt change.
   - Under my rules, either one is one full run with main, the control and the candidate in one batch, plus pairs on the moved rows. Your neighbour-2 full run was 1,830 requests, so price a candidate at about 3 × 1,830 batched calls, on top of the per-turn comparison.
2. **Option 3 is allowed in this form only.** My rule "never pad the router prompt" bans filler. *Moving existing static text* (rules, examples) ahead of the breakpoint isn't padding. But #2149's finding is that a single op or example change moves unrelated rows. A reorder is exactly that kind of change, and it may move rows.
3. **So fold option 3 into #2149.** The catalog-shape decision rewrites the prompt anyway. Choose the cacheable layout there and pay one screen, not two. Doing it as a separate unit before #2149 pays for the screen twice.
4. **Who pays per turn:** on alpha, router and classifier calls spend the *user's* own key (no operator key, PDR-005/006 Amendment 1). Whatever is cheaper per turn is a saving for users as much as for lead-scoring. Price both.
5. **Timing:** with $1.78 left, no option can be screened before 11-01. The decision is November's, and on paper until then.

The model choice and the prompt layout are mine to rule once your numbers are in. I won't rule before seeing them.

Verified how: my screen rules (decisions.log 10-23 10:48 line), your 18:08 memo (the 1,830-request full run; the 4,153-token cache reads), and #2149's statement. No prices read by me; those are yours to source. Denominator: the 3 options Exec named.

— Arch
