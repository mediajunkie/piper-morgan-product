---
currency_claim: none
currency_claim_reason: "Rewritten at the end of every substantive fire (multiple times/day) — a
  max_age_days check would either be trivially satisfied or would need an implausibly short
  window. Declared honest per check-refresh-promises.py's --state-files mode (found ungapped/
  undeclared 2026-09-12, PPM's own seat, same self-audit pattern CXO/CIO/Exec ran this week) —
  see the prose 'Last rewritten' timestamp at the top of this file for the actual live claim."
---

# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)

**★ THIRD-QUEUE-SOURCE CRITERIA LINE (adopted 2026-09-22, per v1.33's ruling)** — run at every
START/WATCH, not just when remembered:
```bash
gh issue list --repo mediajunkie/piper-morgan-product --milestone MVP --state open --json number --jq '.[].number' | sort -n | uniq > /tmp/list1.txt
grep -oE '#[0-9]{4}' dev/active/mvp-epic-order-2026-09-09.md | tr -d '#' | sort -n | uniq > /tmp/list2.txt
comm -23 /tmp/list1.txt /tmp/list2.txt   # every MVP-open issue NOT mentioned in the epic-order file
```
**Must be `#[0-9]{4}` (4-digit only), not a bare `#[0-9]+`** — the looser regex matches informal
non-issue references already in the file's own prose (*"cousin #3," "Lead's #4"*) and produced 30
false positives against 11 real ones when first tried. Any non-empty output = a real MVP item with
no epic home; read each issue's title/body before placing, don't guess from the number alone. State
the denominator when reporting (the `wc -l` of list1.txt) per the third-queue-source discipline.

**Last rewritten**: 2026-09-23 10:33 PT (WORK). 13 issues placed into
`dev/active/mvp-epic-order-2026-09-09.md` this fire: 6 from PM's live Test-1 dogfood session on
alpha (`#1855`-`#1860`, milestoned/board-added/Status-set same-fire), 7 pre-existing gaps the
criteria line caught (`#1386`, `#1570`, `#1595`, `#1623`, `#1625`, `#1628`, `#1632` — oldest filed
2026-07-10). `#1595` (EPIC: Understanding-Layer Inversion) not bucketed — epic-scale itself, flagged
top-of-file, routed to Lead/Arch via mail (pushed `a79e670bc`) for a sequencing call. Criteria line
re-verified clean after: 0 gap, denominator 59. `gh project item-list`/`sprint-truth.py` hit the
shared GraphQL throttle mid-fire ("unknown owner type" — traced to the same rate-limit, not a gh
bug); worked around via REST `issues`/`milestones` endpoints for all verification. Full detail in
today's session log (`dev/2026/09/23/2026-09-23-0722-ppm-code-log.md`, 10:22 WORK entry). Nothing
else PM-gated carried forward.
