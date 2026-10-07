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


**Last rewritten**: 2026-10-07 15:3x PT (15:33 fire).

**Mechanism state**: LaunchAgent cadence (`:33` past 6,9,12,15,18,21), `CronList` "No scheduled jobs" is normal, no cron ritual. `sprint-truth.py` reads `dev/state/sprint-truth-MVP.ppm.json`. No pytest/venv on this seat: handler tests are "unverified, not run".

**ROUTING**: PM's mailbox is retired. Never write to `mailboxes/xian (ceo)/`; nothing is addressed to or cc'd to PM. Needs PM -> address to `exec`, name which of the three conditions in the subject. Asks to PM (via Exec): what it is, why it matters, what I recommend, one answer; no bare issue numbers. Never pair close/fix/resolve with `#N` in commit messages or mail subjects. Mail filenames must be <= 180 chars.

**GATE STATE (re-verified 15:33 fire by the criteria line): MVP open = 14, gap empty, no delta since 12:40.** The 14: #1386 #1595 #1889 #1913 #1886 (gate-core and pending), #1942 #1943 #1951 (admitted 10-06, `Owner: lead`), and the six Epic 0 evidence items HELD IN PLACE by PM as a watch item: #1579 #1623 #1771 #1783 #1843 #1860. **#1886 now carries a `Gate class: 4` line** (added this fire, reflecting PM's direct 10-07 ruling "Gate" over the PPM/Exec Production recommendation) — closes OPEN item (5) below.

**PM rulings applied 10-06 (Exec relay 14:03)**: admit #1942 #1943 #1951 = FIRST slip-ledger entry (cause b, dates unchanged: design partners Fri 10-23, hard stop Fri 10-30; brake not triggered); #1949 stays out (Production, #1595). Closed #1930 #1885 #1867 #1925 (#1880 closed earlier by Lead, residue tracked by #1776, deploy unverified). 11 of 12 moved to Production (#1832 already closed), plus #1852 #1735 #1907. Decision B: invitation = GitHub only (wording in the standard's Class 4 section). C1 #1735 Production, not descoped, option C needs a formal proposal from its advocate (told CXO). C2 #1907 Production (CEO uses an iPad). C3 #1925 closed, question to an Ongoing issue (#1953 CI split, Owner pard; #1954 mint two replacement invites, Owner host). C4 #1946 Production. Ledger rows for every step are in `docs/internal/planning/beta-gate-standard.md`; epic-order entry added. Weekly admissions-by-class line for the rollup can start now.

**Done today (10-06) to carry**: Decision D landed (standard section "Issue ownership"; `Owner:` line on every NEW issue, no backfill, milestone default when absent). #1386 body rewritten for GitHub-only. #1955 filed (which-reminder dead end, Production, `Owner: lead`). Lead landed the re-judge (`ddda204de8`, 30 rows); I conceded the two list-projects rows and the two ledgered REVIEW rows stay asserted; the three real misses on asserted rows are Epic 0 evidence, not gate items. Main CI 12 of 12 green at 21:3x.

**OPEN, mine**: (1) ✅ DONE (12:33, then reopened and re-closed 15:33) — keep/strike call on the beta-invitation known-issues candidates. #1955 reminders and #1957 Reset-to-Defaults KEPT at 12:33 and unchanged since. **#1735 personality: STRUCK at 12:33 on Web's inconclusive behavioral pair, then REINSTATED at 15:33** after CXO read the source at origin/main (13:22, `rule-cxo-...-1735-answered-from-source...md`) and found the stored Warmth key's own docstring says it "does not shape any prompt" — PPM re-verified that docstring and the consumer grep directly before reversing (didn't just take CXO's word). Doc updated (`99289b6690`), mail sent to CXO cc Comms/Exec/Web/Lead/Arch (`mail-send 1c3491bfe`). All five known-issues lines now settled; nothing left on my side before PM's final pass. (2) ✅ RESOLVED — folded into (1). (3) Roadmap fold (open half of #1644) after Fri 10-09 confirm-or-move — not due yet. (4) Turn-2 GUIDANCE probe and floor-served re-points parked on PM's API-cost ruling (Decision F) — externally blocked. (5) ✅ DONE (12:33) — `Gate class: 4` line added to #1886. (6) Start the weekly admissions-by-class line in the rollup — not yet started, no rollup compile due today; pick up when a rollup is next being assembled.

**Deadlines**: Wed 10-07: DONE (#1889 size and criterion 3 re-run size both in); criteria 2/4/5 sizing from Lead still owed, not a PM item. Thu 10-08 21:59 PDT: Phase 3 tail. Fri 10-09: confirm or move the date + roadmap fold. Re-plan trigger: gate grows, or Epic 0 tranche slips past 10-14. Arch's ADR-080 docs work (intent-routing-stack, domain-models, diagram, 10-09/10-12) belongs to Docs, nothing owed from PPM.

**Watch for**: Lead's re-judge commit and full-corpus re-run (regression delta vs 08-12 should be zero; claim rests on his run); PM's final pass on the beta-invitation doc (known-issues + support page + plugin line all staged); usage stop line 95% weekly meter (~71% at 17:26; window ends Thu 10-08 21:59; tell Exec at 95%); any new MVP-milestoned issue without a `Gate class:` line (triage same fire); the alpha-promote hold Exec asked Lead for (product-path pushes to main held until the promote lands — watch, not mine to action); #1957's fix (not yet owned/sized, Production milestone only).

**Placing issues**: `gh issue edit N --milestone MVP|Production|Ongoing`, `gh project item-add 1 --owner mediajunkie --url <url> --format json --jq .id`, then `gh project item-edit --id <id> --project-id PVT_kwHOADE-8s4A-JwA --field-id PVTSSF_lAHOADE-8s4A-JwAzgxpGyU --single-select-option-id e7d1c990`. Plain single or `&&`-chained commands only (shell functions/for loops of gh writes were denied by the auto-mode classifier; do not work around). No Sprint-field or label edits by PPM.

**Mailbox send recipe** when non-mailbox commits coexist: stage and commit the non-mailbox files by name first (inbox moves and new memos stay unstaged), push, then `scripts/mail-send.sh "<subject>" <every changed mailbox path>` (include cc copies, sent mirror, inbox AND read paths of moves, `mailboxes/ppm/read/MANIFEST.md` via `scripts/regenerate-mailbox-manifests.py --role ppm`).

**10-07 09:33 state**: #1956 reshaped by Lead (140a606928), main 12 of 12 green; Lead closes #1956 after tonight's nightly goes green (verify at 18:33 or next fire). Sizes in: #1889 about one working day (gated on two CXO copy calls); criterion 3 re-run one working day plus a held half day (CXO+Lead confirmed; #1386 body Sizing paragraph rewritten). STILL OWED: Lead's sizing of criteria 2, 4, 5. CXO scenario refresh at dev/2026/10/07/1386-criterion-3-scenario-refresh-2026-10-07.md.

**10-07 12:33 state**: Main CI still 12/12 green. Web's push + credential read got PM's direct go in Web's own session (bypassed Janus relay); invite button + CIO plugin wording live on website main (a08efac); both alpha checks (#1735/#1955) ran on the PM-funded key and results folded into PPM's keep/strike call above. Alpha promote attempted twice and failed safely both times (ImageRef, then content-parity vs stale staging) — PM believes it shipped; it did not. Exec asked Lead to hold product-path pushes to main until a fresh promote lands; watch, not a PPM action. Support page (/support) done on Web's branch, needs PM's direct ship-go.

**10-07 15:33 state**: Main CI 12/12 green, no change since 09:34. #1735 reinstated (see OPEN item 1). Exec confirmed no provisioned-key tester path exists (PM's 10-05 bring-your-own-key ruling stands) — no new copy needed for the quota message. Web corrected its own earlier #1955 side-note: only the Friday reminder confirmation reads "next Friday" misleadingly (Monday's "next Monday" is fine); low severity, not filed. Lead's #1886 router-probe spend (~$0.03) already approved and run by PM, 9/10 as ruled, one hole open with Arch.

**Externally blocked**: PM's API-cost ruling (Decision F); PM's final pass on the full beta-invitation doc (all five known-issues lines + support page + plugin line now settled, nothing left on my side); PM's ship-go for /support; PM's awareness that the alpha promote still hasn't landed (Exec's to relay, not mine).
