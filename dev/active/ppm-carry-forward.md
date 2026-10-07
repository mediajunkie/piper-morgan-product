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
⚠️ **`--limit 500` is REQUIRED** — `gh issue list` silently defaults to `--limit 30` with no
warning (live bug 2026-09-22 to 2026-09-23 13:22, since fixed and re-verified clean). **Must be
`#[0-9]{4}` (4-digit only)**, not `#[0-9]+` — the looser regex catches informal prose references
("cousin #3") and false-positives. Any non-empty output = a real MVP item with no epic home; read
each issue before placing. State the denominator when reporting.


**Last rewritten**: 2026-10-06 18:5x PT (18:33 WORK, Fire 5).

**Mechanism state**: LaunchAgent cadence (`:33` past 6,9,12,15,18,21), `CronList` "No scheduled jobs" is normal, no cron ritual. `sprint-truth.py` reads `dev/state/sprint-truth-MVP.ppm.json`. No pytest/venv on this seat: handler tests are "unverified, not run".

**ROUTING**: PM's mailbox is retired. Never write to `mailboxes/xian (ceo)/`; nothing is addressed to or cc'd to PM. Needs PM -> address to `exec`, name which of the three conditions in the subject. Asks to PM (via Exec): what it is, why it matters, what I recommend, one answer; no bare issue numbers. Never pair close/fix/resolve with `#N` in commit messages or mail subjects. Mail filenames must be <= 180 chars.

**GATE STATE (verified 15:4x, re-checked 18:3x by `sprint-truth.py` and the criteria line): MVP open = 14, 0 unmilestoned, gap empty.** The 14: #1386 #1595 #1889 #1913 #1886 (gate-core and pending), #1942 #1943 #1951 (admitted today, `Owner: lead`), and the six Epic 0 evidence items HELD IN PLACE by PM as a watch item: #1579 #1623 #1771 #1783 #1843 #1860.

**PM rulings applied 10-06 (Exec relay 14:03)**: admit #1942 #1943 #1951 = FIRST slip-ledger entry (cause b, dates unchanged: design partners Fri 10-23, hard stop Fri 10-30; brake not triggered); #1949 stays out (Production, #1595). Closed #1930 #1885 #1867 #1925 (#1880 closed earlier by Lead, residue tracked by #1776, deploy unverified). 11 of 12 moved to Production (#1832 already closed), plus #1852 #1735 #1907. Decision B: invitation = GitHub only (wording in the standard's Class 4 section). C1 #1735 Production, not descoped, option C needs a formal proposal from its advocate (told CXO). C2 #1907 Production (CEO uses an iPad). C3 #1925 closed, question to an Ongoing issue (#1953 CI split, Owner pard; #1954 mint two replacement invites, Owner host). C4 #1946 Production. Ledger rows for every step are in `docs/internal/planning/beta-gate-standard.md`; epic-order entry added. Weekly admissions-by-class line for the rollup can start now.

**Done 18:5x (Fire 5)**: Decision D landed (section "Issue ownership" in the standard; `Owner:` line on every NEW issue, no backfill, milestone default applies when absent; commented on #1940). #1386 body rewritten for GitHub-only (read back). #1955 filed (the "which reminder?" dead end, Production, `Owner: lead`). Mail sent: Exec (cc CXO, Comms) and Web (cc CXO, Exec).

**OPEN, mine**: (1) Known-issues list: Comms owns the text (connectors, reminders pinned on the Radar, iPad); PM is passing it. At send time I check each line against issue state and strike closed ones; #1886 stays out until PM answers; add the #1955 workaround line only if Web reports it reproduces; a personality line only if Web's live check says the setting does nothing. (2) Waiting on Web: two live checks (#1735 personality, #1955 dead end), answer to me cc CXO, Exec. (3) Roadmap fold (open half of #1644) after Fri 10-09 confirm-or-move. (4) Turn-2 GUIDANCE probe and floor-served re-points paused on PM's API-cost ruling (Decision F). (5) #1886 has no `Gate class:` line; if PM keeps it in the gate it needs one (class 4 is the only honest fit). (6) Start the weekly admissions-by-class line in the rollup.

**Deadlines**: Wed 10-07: Lead's #1889 size (degraded-sources honesty work), #1386 re-run duration (PPM+CXO). Thu 10-08 21:59 PDT: Phase 3 tail. Fri 10-09: confirm or move the date + roadmap fold. Re-plan trigger: gate grows, or Epic 0 tranche slips past 10-14. Arch's ADR-080 docs work (intent-routing-stack, domain-models, diagram, 10-09/10-12) belongs to Docs, nothing owed from PPM.

**Watch for**: Lead's re-judge commit and full-corpus re-run (regression delta vs 08-12 should be zero; claim rests on his run); Web's two live-check answers; PM's pass on the known-issues text and #1886 answer; usage stop line 95% weekly meter (~71% at 17:26; window ends Thu 10-08 21:59; tell Exec at 95%); any new MVP-milestoned issue without a `Gate class:` line (triage same fire).

**Placing issues**: `gh issue edit N --milestone MVP|Production|Ongoing`, `gh project item-add 1 --owner mediajunkie --url <url> --format json --jq .id`, then `gh project item-edit --id <id> --project-id PVT_kwHOADE-8s4A-JwA --field-id PVTSSF_lAHOADE-8s4A-JwAzgxpGyU --single-select-option-id e7d1c990`. Plain single or `&&`-chained commands only (shell functions/for loops of gh writes were denied by the auto-mode classifier; do not work around). No Sprint-field or label edits by PPM.

**Mailbox send recipe** when non-mailbox commits coexist: stage and commit the non-mailbox files by name first (inbox moves and new memos stay unstaged), push, then `scripts/mail-send.sh "<subject>" <every changed mailbox path>` (include cc copies, sent mirror, inbox AND read paths of moves, `mailboxes/ppm/read/MANIFEST.md` via `scripts/regenerate-mailbox-manifests.py --role ppm`).

**Externally blocked**: PM's #1886 call; PM's API-cost ruling (Decision F); PM's pass on Comms' known-issues text.
