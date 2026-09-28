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

**Last rewritten**: 2026-09-27 22:2x PT (STOP, day-close). Cron rotated at STOP (`9ef438cc` →
`3d940551`, same expression, CronList-verified exactly one survivor) — **also refreshed the cron
prompt's stale text this time** (old baseline number, a fully-resolved watch item that should have
been deleted the fire it completed). Registry row updated.

**Day's substantive work**: closed out the multi-day post-MVP-triage watch item (START); caught and
fixed TWO separate unmilestoned-issue gaps this week's new-issue volume exposed — `#1899` (WORK,
milestoned MVP, shipped and closed same-day by Lead) and `#1900` (STOP, Pard's prompt-caching-cost
finding, milestoned `Ongoing` per this week's own necessity-triage precedent for cost/ops-
reliability items). Both hygiene instruments re-verified clean and mutually consistent at every
check today; denominator moved 26→27→26 purely from real issue lifecycle, no drift.

**Own process correction, worth remembering next time a Rule-0/dead-code call needs making**:
verifying a fact correctly (this seat checked "zero include sites" twice, both times right) is not
the same as reading the WHOLE artifact — the issue's own comment thread carried the disambiguating
context both times and wasn't read. Named plainly in mail and in the epic file rather than quietly
fixed.

**No externally-blocked items remain.** No other open threads.
