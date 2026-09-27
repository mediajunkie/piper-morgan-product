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

**Last rewritten**: 2026-09-26 22:2x PT (STOP, day-close). Cron rotated at STOP per standard
practice (`50af07b9` → `9ef438cc`, same expression `52 6,14,21`, CronList-verified exactly one
survivor). Registry row updated with the new job id and cadence-history note.

**Day's substantive work**: (1) direct-engagement epic-order reconciliation against PM's three
fresh TSV exports — fixed 52 stale unstruck-but-closed references across 8 epics, recomputed 4
epic headers precisely, closed one coverage gap (`#1897`); (2) independently confirmed (third,
different method) the Ship #062 closed/filed-count correction, 91/57, safe for PM's public draft;
(3) `#1595` unit-4 sequencing fully resolved — Arch approved all three rules plus the `#1897`
grammar shape, folded into epic 0's narrative. Board hygiene stable all day: 30 not done / 1214
done / 0 unmilestoned; third-queue-source criteria line clean, 0 gap, denominator 30 at every
check.

**ALSO WATCH item RESOLVED (partially) — PM ruled, but the mechanical follow-through is BLOCKED,
carrying forward as a genuine blocker, not a self-deferral**: PM ruled on the 4 post-MVP proposals
— `#1423`/`#1849`/`#1892` → milestone `Ongoing`, sprint "Q - Recurring Audits"; `#1890` was left
as PPM's own call (needed vs. close). **Made the call**: `#1890` is `Ongoing`, not closed — verified
live (`git grep` for `greeting_context.html` include sites: zero; file still exists, 11.8KB;
already correctly allowlisted in `tests/test_completion_ratchets.py`'s `_dark_templates()`) — a
real, small, still-outstanding Rule-0 delete candidate, same shape as the other three, not a
"turned out unneeded" case.

**Blocked**: `gh issue edit --milestone Ongoing` for all four was refused by the Claude Code
auto-mode permission classifier (`[External System Writes]`) — confirmed via an immediate read
that none of the four actually moved (`#1423` still `MVP`). Same class of block CXO/Web hit earlier
today per the registry. Mailed Exec/PM/Lead the call + the block rather than retry-and-hope or
route around it. **Next fire (06:52 START tomorrow): check for a reply — either PM applied the
moves directly, or someone with a working grant did it on my behalf, or it's still sitting.** If
still blocked, re-flag rather than let it go silent — this is now the standing external-block item,
replacing the resolved "waiting on PM's ruling" framing.
