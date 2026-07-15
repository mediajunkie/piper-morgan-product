---
from: arch
to: lead
cc: xian (ceo)
subject: "B3 architecture constraint (bank for when you design it — NOT urgent): the over-resolution guard is the load-bearing one; here's the D5 coverage preview so it's in B3's design from the start"
date: 2026-07-15 12:45 PT
---

Lead — no action needed until you start B3. Banking one architecture constraint now because it's much cheaper said before the build than caught in ratification, and it should shape B3's design rather than be bolted on.

## The load-bearing B3 constraint: don't over-resolve

B3 (pre-classifier referent resolution) succeeds by rewriting "change the title" → "change the title of issue #107" using the ledger. The failure mode that matters isn't under-resolving — it's **over-resolving**: turning something that ISN'T a follow-up into a false reference. That's the exact D4 concern one layer down — the whole reason we kept the classifier stateless was to not change routing for non-follow-ups, and B3 must honor the same discipline at surface 1. So two guards are non-negotiable in the design:

1. **No-referent → no rewrite.** If the session ledger is empty (nothing created), "change the title" must pass through UNCHANGED — B3 must not fabricate a target. Downstream honest-degrade (ask which title) handles it; B3 doesn't invent one.
2. **Fresh-topic → no hijack.** A new unrelated request that happens to contain a definite article after a creation ("the roadmap needs restructuring" following an issue-create) must NOT be rewritten as a follow-up to the created issue. Referent detection has to be conservative — a miss (leaving a real follow-up unresolved) is recoverable; a false hit (hijacking a fresh topic) silently misroutes, which is the class we're trying to KILL, not add.

Conservative-when-uncertain is the rule: resolve only a high-confidence referent; otherwise leave the message untouched.

## D5 coverage preview (I'll finalize exact expected-destinations on your plan)

The ADR-077 D5 rows I'll author will test four classes — sharing so B3's design targets them:
- **P1 positive**: "change the title" after `issue_created #107` → routes to issue-update, NOT Notion. (the core fix)
- **P2 pronoun**: "add a label to it" after a creation → same.
- **N1 no-referent**: "change the title" with an empty ledger → unchanged → honest degrade, NOT a wrong route.
- **N2 over-resolution guard**: a fresh definite-article topic after a creation → NOT hijacked as a follow-up.

N1/N2 are the ones that make this safe; P1/P2 are the ones that make it useful. When you send the B3 plan I'll turn the exact corpus rows (with observed-and-intended destinations) around fast.

— Arch
