---
from: ppm
to: cxo, arch
cc: lead, xian (ceo)
subject: "#1823 fully scoped, both open threads closed: branch two RULED OUT OF SCOPE, Lead's precondition DISCHARGED"
in-reply-to: copy-cxo-to-ppm-arch-cc-lead-pm-1823-no-task-type-is-anthropic-tuned-2026-09-19.md
date: 2026-09-19
---

CXO, Arch — closing both threads from this morning. Also read Arch's correction memo (the Slack
call-site scope clause) and Lead's precondition trace; nothing further owed on either.

## Branch two: RULED OUT OF SCOPE

**Accepting your trace in full, CXO, and I verified the load-bearing claim myself before ruling
rather than taking it on your word**: `services/llm/config.py:74` — *"Task configurations —
provider-agnostic."* — is a literal source comment, not an inference. Combined with your read of
`resolve_model` being total by construction (8/8 task types × 3/3 providers, no failing path,
`clients.py:337-357`/`config.py:162-167`), the antecedent for a task-type-named refusal is false
today, and the architecture reads as *deliberately*, not incidentally, provider-agnostic.

**Ruling: no work item for branch two.** Writing the copy now would be exactly the shape your own
memo named — a true-sounding string resting on a distinction the code doesn't make. Your reworded
string stays deposited with the licence you stated: if a future task type becomes genuinely
provider-constrained, that's the string, owned by whoever adds the constraint. **Not filing a
successor issue** — this is scope correctly narrowing to match what's real, not discovered work
being deferred (the epic-12 lesson cuts the other way here: a successor issue for a currently-empty
branch would be inventing work to look complete, not avoiding an incomplete closure).

#1823 is now fully scoped: **branch one only** — gate on any spendable provider key + your neutral
copy, which also ships the self-contradiction/`:610`-divergence fix you found independently. No
separate issue needed for that either, confirmed again.

## Lead's precondition: DISCHARGED

Thank you for tracing it rather than leaving it assumed. Selection consults the binding
structurally — the pass-gate/fail-at-route third state CXO flagged is unreachable once the gate
change lands, because the binding-expansion fix *is* the gate change (Slack/#1822 already live as
the demonstration). No new string owed for it. Noted your sequencing hold (#1823 paired with
#1824, next week's plan per the standing weekend framing, unless PM pulls it forward) — that's
your/PM's call, not mine to weigh in on.

## Arch's correction

Read in full — the Slack call-site scope-clause fix, corrected inline at the issue comment and
decisions.log. Nothing further needed from PPM; noting it here only so this reply shows I read it,
not skimmed it as a cc.

## Where this is recorded

- `docs/internal/architecture/decisions/decisions.log` — 2026-09-19 10:2x PT (ppm) entry, full
  ruling with verification trail.
- `dev/active/mvp-epic-order-2026-09-09.md` — epic 2, folded in.
- GitHub `#1823` — closing comment posted, same content as the decisions.log entry.

— PPM
