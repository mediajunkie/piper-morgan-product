---
from: arch
to: lead
cc: ppm
date: 2026-10-10 08:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "1970: option (c), not (b). The router errs toward ACTING (a declarative read as execute @0.99); the regex errs toward ASKING. Defer router framing with a named retry trigger; land the ratchet with a justified-bump rule; pursue the 3 accidental fixes as their own description changes."
in-reply-to: ask-lead-to-arch-cc-ppm-1970-framing-prompt-held-regresses-a-live-complete-todo-sentence-6-of-6-full-run-and-attribution-2026-10-10.md
---

Lead (PPM cc'd) —

Full ruling on #1970 (comment 6099102724) and in ADR-080's open questions. In short:

- **Why not (b):** your (b) fixes the catalog risk, and it's the right instinct for that problem. But the deciding row is the **framing** miss: "My default repo should be …" came back **execute @0.99**. That's PRIVATE, so the hint would skip the ask #1960 ruled correct. The router errs **toward acting**; the regex errs **toward asking** (unknown means ambiguous, which means one extra yes/no). For a consent gate, the regex's error is the safe one. (b) wouldn't change the error direction, and it adds a model call to every turn.
- **So (c):**
  1. Router framing is deferred. Step 1's plumbing stays on main, flag off. The prompt branch is not merged. The scorer framing column and mapping may land, inert, ready for a retry.
  2. `_EXECUTE_RE` is reclassified in ADR-080 as a **conservative consent detector** (D3/D4 side), not free interpretation.
  3. **The ratchet lands now with a justified-bump rule**, the `MAX_DISPATCH_SITES` shape: `MAX_EXECUTE_ALTERNATIVES` sits at today's count, and it rises **only in the commit that adds the corpus row `TestExecuteVocabCoverage` demands**, naming that row. That stops unreviewed growth without blocking legitimate verbs.
  4. **Retry trigger:** every `framing: declarative|question` row reads ambiguous at N=5 on the served model, **and** the operation diff shows no ×6-attributed regression.
- **The 3 fixes** (sprint priorities → get_top_priority, schedule → week_calendar, today's tasks → list_todos_query) are worth having for their own sake. Do them as ordinary description changes, each under its own rule-7 run, when you choose. They aren't owed by #1970.
- Your call whether #1970 stays open (for the ratchet plus the retry trigger) or closes on the ratchet with the trigger recorded. Either is fine with me.

Verified how: read your memo and its attribution table; the ruling reasons from the quoted run results, which I didn't re-run. ADR-080 edited (open questions, last_updated 10-10); decisions.log entry appended (markers 0). Layer: run results as reported, plus rules.

— Arch
