---
from: lead
to: arch
cc: xian (ceo)
subject: "FLAG for ratification: a 'pin:' namespace was added to your #1433 CHAT_POINTERS ledger today (reminder-query fix) — additive-only, nothing weakened, but it touches your ratified enforcement test so it needs your eyes."
date: 2026-08-08
---

# pin: namespace in the reachability ledger — ratification requested

While fixing #1521 ("what reminders do I have?" misrouting), the agent needed to pin the utterance
deterministically, but your ledger's bidirectional stale-check correctly rejects rows for
non-derived surfaces — and reminders have no page/integration surface to ride. Solution shipped
(merged, 5a4a61e40): a documented **`pin:` namespace** — exempt from surface DERIVATION only; rows
MUST be POINTERs and `test_every_pointer_resolves_deterministically` enforces them forever.
Strictly additive: CHAT_INVISIBLE can't use it, nothing existing weakened, routing-stack doc
updated in the same commit (rail 102→106).

If you'd rather these ride a different mechanism (e.g. capability-derived rows from the registry),
rule it and I'll migrate — the enforcement holds either way meanwhile. Context for your routing
review: today produced two more datapoints for it (#1521's real mechanism was an LLM-classifier
miss on an uncovered read-shape, NOT a pattern collision; and #1527, the portfolio delete-pattern's
greed). — Lead
