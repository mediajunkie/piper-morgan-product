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

**Last rewritten**: 2026-09-22 22:22 PT (STOP). **Spring-cleaned this file per Exec's context-floor
item 4a** — deleted ~2,200 lines of resolved/superseded history (Prior-chain entries back to
09-16, a July predecessor-handoff section, a stale cron block referencing a job id and expiry date
from 09-14/21, long since superseded many times over). None of it was load-bearing: the durable
record for all of it already lives in the dated session logs (`dev/2026/MM/DD/…-ppm-code-log.md`),
per PM's 2026-06-12 one-place-for-logging ruling — this file's job is current state and active
threads only, not a second copy of history. **Day closed clean, DAY-CLOSED sentinel written.**
`sprint-truth.py` fresh at STOP: `0 unmilestoned`, no delta, criteria line clean (0 gap). **Nothing
PM-gated carried forward** — no open PPM or Arch action pending on anything from today.
