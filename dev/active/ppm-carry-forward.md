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

**★ THIRD-QUEUE-SOURCE CRITERIA LINE (adopted 2026-09-22, per v1.33's ruling; `--limit` bug fixed
2026-09-23 13:22)** — run at every START/WATCH, not just when remembered:
```bash
gh issue list --repo mediajunkie/piper-morgan-product --milestone MVP --state open --limit 500 --json number --jq '.[].number' | sort -n | uniq > /tmp/list1.txt
grep -oE '#[0-9]{4}' dev/active/mvp-epic-order-2026-09-09.md | tr -d '#' | sort -n | uniq > /tmp/list2.txt
comm -23 /tmp/list1.txt /tmp/list2.txt   # every MVP-open issue NOT mentioned in the epic-order file
```
⚠️ **`--limit 500` is REQUIRED, not optional — its absence was a live bug from adoption until
2026-09-23 13:22.** `gh issue list` silently defaults to `--limit 30` with no warning. The original
form of this line (no `--limit` flag) had been reporting a stable "denominator 30, 0 gap" since
2026-09-22 — which was true of the *first 30* MVP-open issues and silently blind to the other
~27-29 that exist. Caught 2026-09-23 13:22 when a REST-API cross-check (done to work around a
GraphQL throttle) returned 57-59 against the criteria line's own 30 for the same milestone, same
moment. **Low actual blast radius**: the tool had only run twice before the fix (2026-09-22
evening, 2026-09-23 07:22 START), and the 13 gaps it eventually caught (2026-09-23 10:22, via the
REST workaround) were mostly issues filed well before the tool existed — the bug delayed
*discovery*, it didn't cause new gaps to form. Re-verified clean post-fix: 0 gap, denominator 57.
**Must be `#[0-9]{4}` (4-digit only), not a bare `#[0-9]+`** — the looser regex matches informal
non-issue references already in the file's own prose (*"cousin #3," "Lead's #4"*) and produced 30
false positives against 11 real ones when first tried. Any non-empty output = a real MVP item with
no epic home; read each issue's title/body before placing, don't guess from the number alone. State
the denominator when reporting (the `wc -l` of list1.txt) per the third-queue-source discipline.

**Last rewritten**: 2026-09-26 15:2x PT (WORK). Between this fire and the 07:22 START, PM engaged
directly in conversation (not a cron tick) asking for a full epic-order reconciliation against
three fresh TSV exports — completed and pushed (`37c245c751`, merged/pushed `f5343cd7f1`): fixed
52 stale unstruck-but-closed references across 8 epics, recomputed 4 epic headers precisely,
closed one coverage gap (`#1897`, epic 0). Criteria line clean: 0 gap, denominator 30.
`sprint-truth.py`: 0 unmilestoned, delta is exactly `#1897` arriving (Product Backlog 14→15) —
consistent with the reconciliation.

**This fire's mail drain (5 items, all now read)**: the live Ship #062 closed/filed-count
reconciliation (43/34 → corrected 91/57, two stacking `gh` bugs: unscoped 30-row cap +
`closed:`/`created:` search evaluated in UTC not PDT) — **independently confirmed via a third,
different method** (GitHub's own search qualifier, not a bulk-pull-plus-bucketing rerun) and
replied to Exec/PM/Lead since PM was holding the Ship draft on this number. Plus Pard's
commit-attribution correction (ppm's own share 9→13, informational only) and the incident memo —
both broadcast, no PPM action.

**`#1595` unit-4 sequencing: RESOLVED, drop from watch** — Arch approved Lead's confirm-pause
proposal in full (all three rules), then separately ruled the `#1897` grammar shape (additive
`outcome="plan"`, never touching the existing single-op contract). Both landed in epic 0's
narrative via this fire's reconciliation pass.

**Still externally blocked, carrying as ALSO WATCH**: PM's decision on the 4 post-MVP proposals
from Friday's triage (`#1423`/`#1890`/`#1849`/`#1892`) — re-checked live this fire, all four still
MVP-milestoned and open, no ruling yet.
