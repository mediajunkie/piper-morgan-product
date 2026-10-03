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

**Last rewritten**: 2026-10-02 21:4x PT (STOP, day close). Day fully wrapped, `<!-- DAY-CLOSED:
2026-10-02 -->` sentinel written, sign-off clean (`git log origin/main..HEAD` empty).

**LaunchAgent cadence fully migrated and stable** — `:33` past 6,9,12,15,18,21, confirmed across
two more fires today with `CronList` correctly returning "No scheduled jobs" each time. No
cron-management ritual needed at START/STOP going forward.

**`sprint-truth.py` per-seat baseline fix (CIO) fully landed for this seat** — second run today
correctly read `"baseline: ppm's run"` from `sprint-truth-MVP.ppm.json`. No action needed, just
run as usual.

**Phase3 ruling thread CLOSED for this round**: PPM's independent ruling (18:33, 7 concur/6
dissent vs. Lead) converged against CXO's own independent ruling on the same 13 rows at 21:33 —
**11 of 13 matched without coordination**. Conceded C1 ("threats to our timeline" →
`attention_query`) to CXO's reasoning on reflection. **Held one standing technical finding, D1**:
`session_activity_query`'s own docstring keys it to "THIS session" only (`intent_service.py:8645`)
— "our *last* session" is a different, prior session, out of scope by construction, not a style
preference. Filed to CXO/Lead/Arch. Not urgent — `read_floor`'s five shipped members (Lead,
19:09 memo) don't include this op this round — but needs settling before any future wave adds it.
**Watch for**: Arch or CXO responding to the D1 finding.

**Noted, no action**: Lead's `read_floor` build shipped on main (5 READ entries, Phase-2 gate
clean) but the flip token is PM's, explicitly held since PM is unwell today — Lead routed it to
the carry-forward, not any inbox. Also surfaced: the router's own coverage of these floor ops is
thin once floor-without-rail's generous matching is removed (TRUST 0/10) — a sharpen-descriptions
follow-up Lead already flagged for tomorrow, not PPM's to chase.

Board hygiene clean all day, every fire: 0 unmilestoned, 0 gap, denominator 28, unchanged since
yesterday. No new MVP issues, no epic-file edits needed beyond yesterday's. No discovered-work
issues filed today. No PM-gated items pending.

**Also noted, no action needed**: `dev/state/sprint-truth-MVP.json` is shared across Lead/Exec/
PPM, so the script's "delta since" line compares against whoever last wrote the file, not this
seat's own prior run. Absolute counts have always been right; only read the delta line as "since
someone last ran this," quote the timestamp with any figure cited.

**`#1920` closed same-day** (live on v165) — struck in the epic file. `#1921`/`#1922` both
`Ongoing`, correctly out of MVP scope. Both instruments clean: 0 unmilestoned, 0 gap,
denominator 28.

**No externally-blocked items.** No other open threads.
