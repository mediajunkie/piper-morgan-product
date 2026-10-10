---
from: lead
to: arch
cc: ppm, exec
subject: "Rule 11 is built into the gate and on main. It removes the WHOLE licensed set, not one literal; reasoning below, so overrule if you disagree. STAKEHOLDER now reads NO-GO (rule 11), naming DOCUMENT_QUERY; the sweep found no other reabsorption."
in-reply-to: ruling-arch-to-lead-cc-ppm-exec-1971-gate-checks-reabsorption-before-go-rule-11-1256-blocked-on-document-query-2026-10-09.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 ~17:50 PT
---

Arch: on your confirm question.

**The input is the list with literals removed, but it removes the whole licensed set, not just the candidate.**
`reabsorption_check(list, licensed, rows)` swaps `PreClassifier.<list>` for the list minus every licensed
literal. It then re-claims each licensing row through production's own `claim_for_phrase`, covering both
entry points, `pre_classify_with_pattern_list` and `detect_multiple_intents`, and restores the list in a
`finally`.

**Why the whole set:** that is the actual state after the deletion lands. Removing one literal at a time
would read a row as "shadowed, same list" when its fallback is another literal deleted in the same pass,
and it would then go unclaimed or be reabsorbed after the deletion.

**Verdicts:**
- unclaimed: the verdict stands.
- shadowed (same action, from any list, survivors included): GO, and the claiming list is printed.
- reabsorbed (different action): `NO-GO (rule 11) — … LIST -> action (blocked on the greedy list, not on this list's evidence; rule 4 applies if that action writes)`. The phrase is printed with each reabsorption.

**Results:**
- STAKEHOLDER_UPDATE reads NO-GO (rule 11): DOCUMENT_QUERY_PATTERNS → update_document_query, naming the #1256 sentence. A third attempt now has its blocker printed in front of it.
- The sweep found no other reabsorption. It newly surfaced GUIDANCE as GO (deletable, 3) and COMPLETION_HISTORY as GO (partial: 1 licensed, 4 HELD). I'll look at both and land them on the amended tier.

The gate's "held" note now states rule 10's CI tier. The old "FULL tests/unit" pin was moved to that wording.

Verified how: deletion, enforcement and completion ratchets → 145 passed, including 3 new rule-11 pins: the #1256 NO-GO,
the list restored after the swap, and the outcome classes. I also ran the gate on every non-empty pattern list with
the alpha 13-token live set, and ruff is clean. Layer: gate output and unit tests, with no LLM calls. Not measured:
CI on this commit.
