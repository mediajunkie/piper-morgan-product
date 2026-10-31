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


**Last rewritten**: 2026-10-08 12:5x PT (12:33 WORK fire: #1889 copy ruled, #1963 placed).

**Mechanism state**: LaunchAgent cadence (`:33` past 6,9,12,15,18,21), `CronList` "No scheduled jobs" is normal, no cron ritual. `sprint-truth.py` reads `dev/state/sprint-truth-MVP.ppm.json`. No pytest/venv on this seat: handler tests are "unverified, not run".

**ROUTING**: PM's mailbox is retired. Never write to `mailboxes/xian (ceo)/`; nothing is addressed to or cc'd to PM. Needs PM -> address to `exec`, name which of the three conditions in the subject. Asks to PM (via Exec): what it is, why it matters, what I recommend, one answer; no bare issue numbers. Never pair close/fix/resolve with `#N` in commit messages or mail subjects. Mail filenames must be <= 180 chars.

**GATE STATE (re-verified 18:33 fire by the criteria line): MVP open = 13, gap empty. #1942 CLOSED by Lead 17:03 PT with a quoted live answer on alpha `99289b6690`.** The 13: #1386 #1595 #1889 #1913 #1886 (gate-core and pending), #1943 #1951 (admitted 10-06, `Owner: lead`), and the six Epic 0 evidence items HELD IN PLACE by PM as a watch item: #1579 #1623 #1771 #1783 #1843 #1860. **#1886 now carries a `Gate class: 4` line** (added this fire, reflecting PM's direct 10-07 ruling "Gate" over the PPM/Exec Production recommendation) — closes OPEN item (5) below.

**PM rulings applied 10-06 (Exec relay 14:03)**: admit #1942 #1943 #1951 = FIRST slip-ledger entry (cause b, dates unchanged: design partners Fri 10-23, hard stop Fri 10-30; brake not triggered); #1949 stays out (Production, #1595). Closed #1930 #1885 #1867 #1925 (#1880 closed earlier by Lead, residue tracked by #1776, deploy unverified). 11 of 12 moved to Production (#1832 already closed), plus #1852 #1735 #1907. Decision B: invitation = GitHub only (wording in the standard's Class 4 section). C1 #1735 Production, not descoped, option C needs a formal proposal from its advocate (told CXO). C2 #1907 Production (CEO uses an iPad). C3 #1925 closed, question to an Ongoing issue (#1953 CI split, Owner pard; #1954 mint two replacement invites, Owner host). C4 #1946 Production. Ledger rows for every step are in `docs/internal/planning/beta-gate-standard.md`; epic-order entry added. Weekly admissions-by-class line for the rollup can start now.

**Done today (10-06) to carry**: Decision D landed (standard section "Issue ownership"; `Owner:` line on every NEW issue, no backfill, milestone default when absent). #1386 body rewritten for GitHub-only. #1955 filed (which-reminder dead end, Production, `Owner: lead`). Lead landed the re-judge (`ddda204de8`, 30 rows); I conceded the two list-projects rows and the two ledgered REVIEW rows stay asserted; the three real misses on asserted rows are Epic 0 evidence, not gate items. Main CI 12 of 12 green at 21:3x.

**OPEN, mine**: (1) ✅ DONE (12:33, then reopened and re-closed 15:33) — keep/strike call on the beta-invitation known-issues candidates. #1955 reminders and #1957 Reset-to-Defaults KEPT at 12:33 and unchanged since. **#1735 personality: STRUCK at 12:33 on Web's inconclusive behavioral pair, then REINSTATED at 15:33** after CXO read the source at origin/main (13:22, `rule-cxo-...-1735-answered-from-source...md`) and found the stored Warmth key's own docstring says it "does not shape any prompt" — PPM re-verified that docstring and the consumer grep directly before reversing (didn't just take CXO's word). Doc updated (`99289b6690`), mail sent to CXO cc Comms/Exec/Web/Lead/Arch (`mail-send 1c3491bfe`). All five known-issues lines now settled; nothing left on my side before PM's final pass. (2) ✅ RESOLVED — folded into (1). (3) Roadmap fold (open half of #1644) after Fri 10-09 confirm-or-move — not due yet. (4) GUIDANCE/floor re-point batch (UPDATED 10-08 10:4x): Decision F ruled wait-and-see (decisions.log:2385). Conditions A and B both MET (Lead's served probes on alpha e8ecd10d5a; CXO ruling). LANDED on main: four re-points to floor (3 GUIDANCE phrases + `not sure what to do about this`), each with its own `rejudged` ledger entry, offline re-verdict 6/6 MATCH, no spend; reply mailed (`mail-send 444135a92`). HELD: `advise me on this decision` (router names get_contextual_guidance @0.85, floor would MISMATCH). `analyze the risk` unchanged and now RULED final: it is a live ANALYSIS survivor literal (ledger `surviving_literals`), expectation stays `analyze_blockers`, CXO declined a served comparison; reopen only if a served reply shows invented subject or blame (Arch + CXO, 10-08 10:4x). `advise me` hold concurred by both. STILL OWED by others: rest of the parked batch (get_project_status x2, get_top_priority `what now`, non-ledgered floors) rides Lead's next catalog-change full run (rule 7); CXO's served floor probe of `show the team calendar`. #1962 (CXO's UX copy note) placed Production + board 10:4x, `Owner` named in body (CXO copy, Lead wiring). (5) ✅ DONE (12:33) — `Gate class: 4` line added to #1886. (6) Start the weekly admissions-by-class line in the rollup — not yet started, no rollup compile due today; pick up when a rollup is next being assembled.

**#1889 (10-08 12:24)**: Lead's ask to CXO (cc PPM) delivered the two copy calls (standup disclosure line per format; Radar empty card on source failure) with drafts. Gate: waiting on CXO's wording or "drafts fine", then Lead builds (~1 day, no spend). CXO RULED 12:5x (edited both; example card dropped; #1963 filed for the populated-Radar case, I placed it Production + board, reply `mail-send fe0398e698`). Lead BUILT #1889 + #1963 on main `ef12f7af52` at 12:42 (31 tests, browser render, plus home-aside and toast fixes); both stay OPEN for CXO's acceptance and a served check on alpha after the next promotion. #1964 (`/generate` formatter honesty, predates #1889) placed Production + board. Waiting on CXO's acceptance and the promote; I do not close either. CXO ACCEPTED the strings 13:0x with ONE defect for Lead to fix inside #1889: the green check under a partial read in /generate markdown+Slack. CXO also ruled #1964 copy (no raw user id, drop Saved/Generated lines, Blockers -> Watch; delete the formats if no live consumer). Closure of #1889/#1963 waits on the alpha served check (Lead offered; CXO verifies from quoted output). Lead FIXED the green-check defect (5e6ec8d2d8) and applied the #1964 polish 13:00; kept the /generate text formats (public API route, a command url_path, in Slack reminder help), so deleting it is a product decision, not copy; #1964 is CXO's to accept. CXO ACCEPTED the fix and CLOSED #1964 (13:1x; verified by source read). #1889/#1963 stay open for the alpha served check. Nothing owed by PPM on the strings. NEW 15:5x: #1965 (Lead found: Radar/standup GitHub read turns failures into VERIFIED_EMPTY; OAuth users maybe unauthenticated) PLACED MVP by me, epic 5, gate 13 -> 14; blocks #1889/#1963 live check; Arch ruled (a) strict call carrying DegradationReason, then (b) adapter's grant-aware resolver; Arch asked Lead/PA to file a converge-callers issue (place it when it exists). Notice mailed to Lead cc arch/pa/cxo. CXO ruled #1965 disclosure copy 16:0x: until (b) lands ship ONLY the existing 'couldn't reach' line for every strict-call failure (no 'isn't connected' line, false for OAuth users before (b)); reason-specific table turns on when the reason comes from the resolver; Lead sends rendered strings per reason once (b) is in. Nothing asked of PPM. PA 15:3x: the grant resolver does NOT handle PAT-only users (PAT is a live Settings option); recommends the one resolver carry BOTH legs (grant, then user's own PAT) so (b) doesn't regress PAT users; filed #1966 (converge GitHub credential resolvers; (i) keep PAT / (ii) retire PAT is PM/Arch decision). I placed #1966 Production + board 16:2x. Arch RULED 15:5x (10-08): (a) landed db0b3a8741 (reason carried, copy unchanged); (b) = one resolver, two legs (grant, then user's own PAT), read-time PAT leg, NO bind-on-save; stale OAuth + working PAT -> PAT serves, resolver reports both legs; status claims derive from the resolver (#1966 scope); verify PAT-as-bearer on github-mcp-server first, else native REST transport; served alpha check needs an OAuth-only AND a PAT-only account. So (i) keep-PAT is the working state; (ii) retire-PAT is no longer a gate, no Exec routing. #1966 stays Production (comment posted); move to MVP only if Settings status is shown to mislead a beta-path tester after (b). Lead LANDED #1965 (b) 16:14 (56b1ccd2f9): one resolver, grant then PAT then CONNECT_REQUIRED; per-reason copy live (connector name 'GitHub' substituted for the label in reason sentences, CXO to approve); rendered strings sent to CXO for acceptance. Remaining to close #1889/#1963/#1965: alpha promote, then served check with an OAuth-only AND a PAT-only account (PAT on its owner's own PAT); Lead says 'PM provisions that' (account provisioning is not mine; not a gate-size change). CXO ACCEPTED the per-reason copy 16:20 (substitution approved; both readings stand; mixed Radar card gap fixed by Lead in bc621858c8, pinned; docstring fix applied; PA's BOUND-grant-missing edge left). CXO owes the Settings status copy for #1966 (incl. stale-OAuth + PAT case); #1966 stays Production. WATCH: the alpha promote and PM-provisioned accounts, then the served check with a quoted reply for EACH of OAuth-only and PAT-only (CXO wants both); that closes #1889/#1963/#1965. If Lead folds #1963 into #1889 and the ~1 day sizing changes, update #1889's Sizing paragraph.

**Deadlines**: Wed 10-07: DONE (#1889 size and criterion 3 re-run size both in); criteria 2/4/5 sizing from Lead still owed, not a PM item. Thu 10-08 21:59 PDT: Phase 3 tail. Fri 10-09: confirm or move the date + roadmap fold. Re-plan trigger: gate grows, or Epic 0 tranche slips past 10-14. Arch's ADR-080 docs work (intent-routing-stack, domain-models, diagram, 10-09/10-12) belongs to Docs, nothing owed from PPM.

**Watch for**: Lead's re-judge commit and full-corpus re-run (regression delta vs 08-12 should be zero; claim rests on his run); usage stop line 95% weekly meter (~71% at 17:26; window ends Thu 10-08 21:59; tell Exec at 95%); any new MVP-milestoned issue without a `Gate class:` line (triage same fire); #1957's fix (not yet owned/sized, Production milestone only).

**Placing issues**: `gh issue edit N --milestone MVP|Production|Ongoing`, `gh project item-add 1 --owner mediajunkie --url <url> --format json --jq .id`, then `gh project item-edit --id <id> --project-id PVT_kwHOADE-8s4A-JwA --field-id PVTSSF_lAHOADE-8s4A-JwAzgxpGyU --single-select-option-id e7d1c990`. Plain single or `&&`-chained commands only (shell functions/for loops of gh writes were denied by the auto-mode classifier; do not work around). No Sprint-field or label edits by PPM.

**Mailbox send recipe** when non-mailbox commits coexist: stage and commit the non-mailbox files by name first (inbox moves and new memos stay unstaged), push, then `scripts/mail-send.sh "<subject>" <every changed mailbox path>` (include cc copies, sent mirror, inbox AND read paths of moves, `mailboxes/ppm/read/MANIFEST.md` via `scripts/regenerate-mailbox-manifests.py --role ppm`).

**10-07 09:33 state**: #1956 reshaped by Lead (140a606928), main 12 of 12 green; Lead closes #1956 after tonight's nightly goes green (verify at 18:33 or next fire). Sizes in: #1889 about one working day (gated on two CXO copy calls); criterion 3 re-run one working day plus a held half day (CXO+Lead confirmed; #1386 body Sizing paragraph rewritten). STILL OWED: Lead's sizing of criteria 2, 4, 5. CXO scenario refresh at dev/2026/10/07/1386-criterion-3-scenario-refresh-2026-10-07.md.

**10-07 12:33 state**: Main CI still 12/12 green. Web's push + credential read got PM's direct go in Web's own session (bypassed Janus relay); invite button + CIO plugin wording live on website main (a08efac); both alpha checks (#1735/#1955) ran on the PM-funded key and results folded into PPM's keep/strike call above. Alpha promote attempted twice and failed safely both times (ImageRef, then content-parity vs stale staging) — PM believes it shipped; it did not. Exec asked Lead to hold product-path pushes to main until a fresh promote lands; watch, not a PPM action. Support page (/support) done on Web's branch, needs PM's direct ship-go.

**10-07 15:33 state**: Main CI 12/12 green, no change since 09:34. #1735 reinstated (see OPEN item 1). Exec confirmed no provisioned-key tester path exists (PM's 10-05 bring-your-own-key ruling stands) — no new copy needed for the quota message. Web corrected its own earlier #1955 side-note: only the Friday reminder confirmation reads "next Friday" misleadingly (Monday's "next Monday" is fine); low severity, not filed. Lead's #1886 router-probe spend (~$0.03) already approved and run by PM, 9/10 as ruled, one hole open with Arch.

**10-07 18:33 state**: Main CI 12/12 green. Alpha promote HAS landed (alpha serves `99289b6690`, per Lead's #1942 close and READY memo). PM approved the beta-invitation doc as written at 16:34 (Exec relay), doc status line updated; invitations go last, recipients unnamed. /support is live (Web 37bf522), revoke sentence off until PA's fix is seen working. #1956 nightly schedule path unproven until the 00:00 PT run; recheck at 06:33 (Lead closes it). I mistakenly re-armed a session cron this fire (CronList empty is NORMAL on this seat); deleted it same fire.

**10-08 06:33 START state**: Main CI 12/12 green (mypy ceiling red cleared overnight). #1956 CLOSED by Lead 06:24 PT on a green schedule-path nightly (run 37742950185). Gate unchanged: MVP open = 13, gap empty. Mail empty, scan 0 candidates. Decision F: I recorded "unruled" at START; corrected 09:3x, see OPEN (4). #1886: Lead built to the ruling, 9-of-10 live probe, one hole (tighten CLARIFY to confirm) with Arch/Exec; not mine.

**Externally blocked**: Lead's choice of next scoring run for the rest of the parked batch (Decision F is ruled: wait and see); CXO's served `show the team calendar` floor probe; PM naming invitation recipients; Lead's sizing of criteria 2, 4, 5; CXO's #1889/#1963 acceptance and an alpha promote; PA's Revoke fix (gates Web's revoke sentence).

**18:3x (10-08) placement sweep**: found #1958/#1959/#1960/#1961 (Lead/Web-filed 10-07 and 10-08, UX/copy/honesty defects) open with NO milestone; placed all four Production + board + Status, comments with reasons. #1961 (LLM strikethrough on an open overdue todo) is the judgment call: move to MVP if it reproduces or CXO rules it gate-class; known-issues line is Comms/CXO's call. Gate stays 14.


## Day-close 2026-10-08 21:3x PT
Gate 14 open MVP (see log). Tomorrow first: Fri 10-09 confirm-or-move date plus roadmap fold; weekly admissions-by-class rollup line; WATCH: alpha promote and PM-provisioned OAuth-only/PAT-only accounts for #1889/#1963/#1965 served checks (CXO verifies). Freeze-detect rc=1 at 21:33 was busy-cohort suppression (108 commits), not a freeze.


## 10-09 06:37 START
Brake FIRED (second slip = #1965 admission, found and ledgered 10-09). Memo to Exec cc Lead sent: PM chooses hold 10-23/10-30 (my rec), cut scope, or later date. BLOCKED on PM's answer (filed 10-09; smallest answer: "hold" or a date); Exec escalation if no answer by Sat 10-10 06:33. Roadmap v18 fold waits on it. Owed from Lead: Phase 3 tail status (no report found). New rule for me: every MVP placement = ledger row + `Gate class:` + `Owner:` in the same fire. Weekly admissions-by-class rollup line still to do (unblocked).

### 10-09 07:05 update (mail wake: four Lead/Arch memos)
- Phase 3 tail is stated as **125 routing literals (recount 10-09: FILE_REFERENCE's 30 are a context flag, not routing; no deletion)**. Ratchet ceiling stays 155. Ledgered as a recount, NOT a slip; 0 days; the ~2-day estimate and ~110-120 band unchanged. Never present 125 as progress.
- PM's spend answer is now conditioned: the ~$1.70 scoring run uses the key in Lead's seat Keychain (masked …6wAA, unverified whether it is the capped `beta-testing` key). A useful PM answer is "yes, on key X" (cap raise first, or a different key placed via KeychainService). Lead sent this to Exec directly; no PPM memo owed. Part-run is no evidence (rule 7).
- Still blocked on PM via Exec: hold/move the dates; the spend yes. Exec escalation if no answer by Sat 10-10 06:33.

## 10-09 09:36 update
- #064 workstream review filed (dev/2026/10/09/workstream-064-ppm-2026-10-09.md, mailed to exec). Nothing else changed: gate 14 open MVP, slips 3, 0 days moved, brake fired. Still waiting on PM via Exec: hold or move 10-23/10-30, and the spend "yes, on key X" (escalate Sat 10-10 06:33). Roadmap v18 fold waits on the date answer.

## 10-09 mail-wake update
- PM ANSWERED (09:46, via Janus/Exec): HOLD 10-23/10-30, watch for slippage; scoring run approved. Ledgered. Tripwire stays: Epic 0 evidence tranche not done by Wed 10-14, or the gate grows -> bring the choice back same day. Roadmap v18 fold is unblocked (Docs's). Escalation to Exec on Sat 10-10 06:33 is no longer needed. Remaining: #1889/#1963/#1965 closure (test accounts per CXO's source read, alpha promote, CXO served check); #1966; Lead's criteria 2/4/5 sizing; #1886 (Lead's).

## 10-09 10:0x update
- Lead corrected the Phase 3 tail: ~56 deletable now, ceiling 155->~99, tail 125->~69, no spend; deleting today. Slip row annotated, NOT reversed. WHEN Lead reports the deletion landed + gate-measured: ledger a symmetry row (count stays 3, 0 days), tripwire Wed 10-14 check.
- ROADMAP v18->v19 FOLD is mine (Docs confirmed, #1644 open half). Deferred to a FRESH SESSION: first item 10-10 06:33. Inputs: dates held 10-23/10-30, gate 14 (standard), release-model.md, slip ledger, decisions.log since 07-16.

## 10-09 11:23 update (supersedes the 10:0x entry above)
- Lead's 56-literal batch WITHDRAWN (did not land, 95 regressions). Tail still 155/125, ~2-3 working days, Lead re-measures Monday 10-12. Tripwire Wed 10-14 is AT RISK. Slip 06:40 stands.
- #1969 ledgered as 4th entry (gate 15, 0 days, Gate class/Owner added). Waiting on PM via Exec: does "gate grows again" count; option to move criterion 3 to Production. When ruling arrives: ledger it, move the issue if told, update order doc.
- Still: ledger Lead's resolution row when a deletion lands and gate measures; roadmap v18->v19 fold = fresh session 10-10 06:33; #1889/#1963/#1965 closure; #1966; Lead's criteria 2/4/5; #1886 (Lead's).

## 10-09 12:52 update (supersedes the 11:23 entry where they differ)
- #1969 CLOSED 12:50 PDT (Lead, ca5eebb8d7); gate 15 → 14; close row ledgered. Slips stay 4 logged, 0 days moved. Criterion 3 moot (no Production move needed).
- Open for PM via Exec: the gate-growth question is narrower (grew to 15, back to 14 same day); the Epic 0 tail tripwire (Wed 10-14) is the live one. Phase 3 tail still 155 / routing 125; Lead is writing corpus rows now; Monday 10-12 re-measure is the number I ledger against 10-14.
- Blockers unchanged: #1889/#1963/#1965 closure, #1966, criteria 2/4/5 sizing, #1886 (Lead's), roadmap v19 fold (fresh session 10-10 06:33 START).

## 10-09 13:29 update
- Phase 3 held rows: expectations ruled (mail to Lead). Delete family = 3 named survivors until #1935 (Arch, option c); band arithmetic corrected to 155 minus 44 = 111 best case (not 113). 10-14 target NOT redefined. Waiting: Lead lands rows, runs the approved scoring run; Monday re-measure.

## 10-09 13:44 update
- Lead landed Phase 3 rows (`41da0296a2`): corpus 563, 27 literals licensed under alpha's live set, projected ceiling ~128 / routing ~98 pending the deletion lane (rule 10). Projection, not a landed number; no band change by me. Lead owes Monday 10-12 re-measure.
- #1970 (consent framing to router) placed Production + board by me 13:4x, Owner Arch design / Lead build. Gate 14, unmilestoned 0.
- Arch ruled `framing: declarative` asserted NOT-EXECUTE; both held rows land. CXO owns the consent-behavior-change reaction (five verbs).

## 10-09 15:55 update
- Lead measured the Phase 3 tail: ceiling 129 / routing 99 after 26 rule-10 deletions (quoted; I re-counted the ceiling = 129, 36 lists; 99 not re-run). Recount, not a slip; 0 days; ledgered in beta-gate-standard.md.
- LEDGER CALL: Wed 10-14 check reads the ceiling (headline) with routing beside it; band 110-120 not yet met on ceiling (129). Whether "tranche done" means ceiling/routing/other = PM's, asked via Exec 15:5x. Do NOT redefine the tripwire myself.
- Next: Mon 10-12 Lead re-measure -> resolution row; Wed 10-14 check same day to Exec if tripped.

## 10-09 16:05 update
- Red main `Tests` was Lead's IDENTITY deletion (7 pins outside tests/unit); fix 95c8a9286d; run on 75a8eb0232 in progress at 16:05. WATCH it: red -> mail Lead. Alpha promotion of the 26-deletion batch HELD until green (Lead agreed).
- Rule 10 amended by Arch: CI full tier, llm mark = retirement needing row citation. Supersedes "full tests/unit" wording.
- Tripwire reading question is on rollup v119; Exec relays PM's answer (OWED to ppm). Until then 10-14 check reads ceiling (129) with routing (99) beside.

## 10-09 16:25 update
- Main `Tests` GREEN on 75a8eb0232 (verified by me; 12 of 12 workflows). Promotion hold condition met; promotion itself is PM's. Watch item closed. Chunk 8 (6 literals) pending on amended rule 10; ceiling will drop below 129 when it lands (Lead's figure, ledger as recount).

## 10-09 16:40 update
- Ceiling 124 (my recount). Recount, not a slip; ledgered. Band 110-120 not met yet. Watch: CI `Tests` on chunk 8's commits. Routing tail after chunk 8 unknown to me.

## 10-09 17:55 update
- #1973 landed, no restores. Ceiling 121 (my recount), routing tail 91 (Lead's). Ledgered recount, slips 4, 0 days. Band 110-120 not met (121). Watch: Tests CI on f0ac5db8d0 (in progress 17:54). 10-14 check reads ceiling with tail beside; PM's reading still owed via Exec. Surface-2 credit Anthropic-only (OpenAI 429) is with Exec.

## 10-09 18:35 update
- Tests CI watch item CLOSED: green on f0ac5db8d0 (landing head). Ceiling 121, tail 91 (Lead's). Slips 4, 0 days. Nothing new in mail. Same deferrals + blockers as 17:55.

## 10-09 18:55 update
- Alpha at 4bd1a236e9 (verified), same code as f0ac5db8d0; deletion batch landed + promoted. Served checks unrun (Lead's credential question). Ceiling 121 / tail 91. Slips 4, 0 days. Tripwire reading still owed via Exec.

## 10-09 21:35 STOP
- Day closed (DAY-CLOSED marker in the session log). Tomorrow 10-10 06:33 START: fresh-session roadmap v18->v19 fold (open half of #1644); read Exec for PM's tripwire reading; Lead's served checks status; Mon 10-12 re-measure is the resolution row; Wed 10-14 tripwire check. Gate 14, slips 4, 0 days, ceiling 121 / tail 91 (Lead's).

## 10-10 05:21 update — roadmap v19 fold DONE
- ROADMAP v18->v19 fold landed (open half of #1644): v19.0, archive at historical/roadmap-v18.10-2026-10-10.md. Sections Exec Summary / MVP Sprint Status / Autonomous Ops / Distribution banner-marked HISTORICAL, not rewritten. If PM or Docs want those four rewritten rather than bannered, that is a separate pass.
- OPEN, mine: Enterprise milestone due_on mismatch (GitHub 2028-10-30 vs decisions.log 09-06 2027-10-30). Send to Exec for PM (not mine to set). Tripwire label is Wed 10-14 (my inference; xian never named a day).
- #1644 CLOSED by Docs 10-10 after its audit re-run came back clear (Docs memo filed to read/). Only the Enterprise due_on mismatch remains, with Exec for PM.
- 10-10 05:39: Exec acked Wed 10-14 (relabelled its files, row 83 closed) and put the Enterprise due_on question (2027 vs 2028) on the rollup. WHEN Exec relays PM's answer: update the roadmap Timeline Enterprise bullet (drop "unreconciled"), note it in the log. Blocker: PM's answer via Exec.
- 10-10 13:07 xian via Janus (13:06): (1) Web runs alpha's served checks (#1959, #1960, "delete the first two reminders", and Lead's list) with its existing test login; Web reports to Exec and Lead. This replaces the "Lead's credential question" blocker on served checks, and moves who runs the checks for #1889/#1963/#1965 closure evidence (watch Web's report; CXO's served-check role on those three is unchanged until Exec/Lead say otherwise). (2) Spend limit raised by xian, number not given; Lead to confirm next scoring call served; I treat the scoring blocker as lifted per xian, not measured (ledger note updated). (3) OpenAI top-up pending, do not count OpenAI legs. (4) "No Undo" crossposts done (Docs's). Still open: Enterprise due_on (PM via Exec); tripwire reading of "tranche done"; Mon 10-12 re-measure; Wed 10-14 check.
- 10-10 13:17 xian via Janus: tripwire reading ANSWERED. "Yes, take Exec's rec, leaving it as PPM set it": Wed 10-14 check reads the ratchet ceiling (headline) with the routing tail beside it. Ledgered in beta-gate-standard.md. Remove "tripwire reading" from the open list. Still open: Enterprise due_on (PM via Exec); Lead's served-scoring confirmation; Web's served-check report; OpenAI top-up; Mon 10-12 re-measure; Wed 10-14 check (state the ceiling-vs-band reading that day, via Exec).
- 10-10 18:4x Lead ask (18:28): fresh full run exposed 8 masked ledger rows; 6 restores + 2 surface-2 credits land tonight, ceiling 121->127 (Lead's). I replied: re-judge `I need a status report` -> get_project_status; `where should my focus be today` -> get_top_priority, CXO owns the 10-01 original (needs CXO yes/no). OWED: after Lead's landing commit, re-count the ceiling with `scripts/pattern_literal_counts.py` and ledger the figure; when CXO answers, ledger it. Classification of the 127 recount (rule (c) candidate) waits for Mon 10-12 + PM via Exec; I propose no date.
- 10-10 18:5x re-judges CLOSED: CXO yes on status/progress report -> get_project_status, NO on focus-today (stays attention_query; I conceded). Arch approved the 8-row disposition + freshness rule. OWED still: re-count ceiling after Lead's landing commit (Lead's figure 127); classification of the recount (rule (c) candidate) Mon 10-12 + PM via Exec. NOTE host fault: bare `gh` times out since the 10-10 reboot; use `GODEBUG=netdns=go gh ...` (Pard; fix needs xian's sudo). A bare timeout = "unverified", not red.
- 10-10 19:1x Lead landed (merge 1110c6a03a); I recounted ceiling = 127 (36 lists). CI on the merge in progress at 19:1x: re-check `GODEBUG=netdns=go gh run list --workflow Tests --branch main`. Open and not mine: Arch (two liveness evaluators disagree), CXO (progress report row). Classification of the recount waits Mon 10-12 + PM via Exec.
- 10-11 08:2x Lead's early re-measure: ceiling 127 (PPM recount 127), tail 97. Sizing in beta-gate-standard.md. My arithmetic: headline needs -7; PORTFOLIO 2 (Lead running today) + STATUS 2 (Arch liveness fix) + rule-10 bucket 20 could reach band without router work. Wed 10-14 check = "at risk", not "likely trip". I answered #1951 verdicts (link-repo REVIEW; key-tasks floor). OWED: Mon 10-12 resolution row on Lead's reconfirm; Wed 10-14 check (print ceiling + tail, via Exec). Seat note: 21:33 and 06:33 fires did not run (no heartbeat commit since 19:14); 10-10 log wrapped late 10-11.
- 10-11 08:4x Arch: evaluator split = mis-serve proof (not floor liveness); 2 of 6 restores claim the wrong op (focus-today, upcoming milestones) so restore nothing; STATUS partial (2) licensed now (127->125); focus-today literal waits on CXO; filler stays in tail = 97 (supersedes my NOT_ROUTING note). Ledgered. I advised "land the restores" on 10-10 without a claim-vs-ruled-op check: own it if asked. Wed 10-14 stays "at risk".
- 10-11 08:5x Gate reachability corrected: Lead's sequence 127->124->121->120; below 120 needs CXO's #1974 ruling (16 pleasantry literals held). Wed 10-14 most likely reads 120-124 = likely trip (supersedes "at risk"). Heads-up sent to Exec (no PM ask yet). #1951 closed by Lead. My earlier sum wrongly counted PORTFOLIO 2 (HELD): corrected. OWED: Mon 10-12 resolution row; Wed 10-14 check (print ceiling + tail 97, trip -> Exec same day); watch for CXO's #1974 ruling and Lead's landings (COMPLETION_HISTORY lane, STATUS+PRIORITY, PORTFOLIO).
- 10-11 08:5x CXO ruled #1974 KEEP: 26 pleasantry literals permanent floor; band unreachable below 120 (cheap path ends 120-122). PM-needed memo sent to Exec: what does Wed 10-14 read against (band as set / re-based / other)? Until answered the Wed check reads against the band as set, permanent floor named beside. Rule (c) classification Mon 10-12 (after Lead's reconfirm). Do NOT redefine the band myself. Wed: print ceiling + tail 97 + permanent-floor note, via Exec the same day if it trips.
- 10-11 08:5x Lead landed COMPLETION_HISTORY (merge 9cb5e45c1e): ceiling 124 (PPM recount 124), tail 94 (Lead's). Lane running STATUS 2 -> PRIORITY 1 -> PORTFOLIO 1: 124->122->121->120 = Wednesday best case (band top edge). Tail headline form on Wed: "N, of which 26 are a ruled permanent floor (#1974)". OWED: check Tests conclusion on 9cb5e45c1e (`GODEBUG=netdns=go gh run list --workflow Tests --branch main`); recount after each lane landing; PM's answer on Wed reading (via Exec).
- 10-11 09:0x Permanent floor = 29 (not 26); Wed tail headline: "94 literals, of which 29 are a ruled permanent floor (#1974)". Ceiling 124 now; best case Wed 120. Correction sent to Exec.
- 10-11 10:0x Lead landed STATUS 2 + PRIORITY 1 (merge 6bb22031a6): ceiling 121 (PPM recount 121). PORTFOLIO last literal HELD on #1884 two-topic finding, a question for Arch; until then Wed best case = 121 (one above band top). Exec updated. OWED: Tests conclusion on 6bb22031a6 (was in progress 10:0x); Arch's ruling; recount after any landing; tail figure from Lead for Wed.
- 10-11 10:1x Arch: two-topic turn = plan row (N=5 all validating). Lead measured plan 6/6, resolver VALID 5/5, rows landed (83e43833cd). Gate rule 11 reads it reabsorbed; Lead asked Arch for a plan-aware exception. Wed reads 120 only if Arch approves + lane lands by Wed, else 121. OWED: recount after any landing; Tests conclusion on 6bb22031a6 and 83e43833cd.
- 10-11 10:4x Plan-aware rule 11 built (03664e599b); PORTFOLIO last literal holds at 121 on #1977 (generalize #1416 residue rule; Lead's design pass from 12:17 fire; needs rule 7 run). #1977 placed Production + board by me, NOT MVP (admission would grow the gate = PM's call). PM-needed memo to Exec: Wed reads 121 unless #1977 lands first; if PM wants 120 by Wed, admit #1977 with Gate class line (slip entry, 0 days). Do NOT admit or write a slip row until PM/Exec say.
- 10-11 10:5x Arch corrected his rule: PORTFOLIO's 121->120 needs BOTH #1977 steps (step 1 residue rule, nod given, rule 7; step 2 CXO acknowledgement, served-reply check). Wed realistically reads 121. Exec told. #1977 stays Production; no admission without PM.
- 10-11 11:3x #1977 step 1 landed (0ba7b951e5). Ceiling 121 (recount). PORTFOLIO "planned, fallback unacknowledged" until step 2 (CXO ack; served-reply check). I told Lead: Production placement does not gate the work; start step 2 now. OWED: recount after step 2 lands; Wed 10-14 check; Tests conclusion on the merges; PM/Exec on the Wed reading.
- 10-11 11:5x #1977: cue widened (7e7a859707), trade row deposited, step 2 lane running. Flag flips only on a QUOTED SERVED reply (local server OK), then PORTFOLIO deletion lane -> 120 on CI full tier. Ceiling 121 until then. OWED: recount after the deletion lands; tell Exec when the flag flips or the deletion lands (Wed 120 now plausible); Wed 10-14 check.
- 10-11 12:4x #1978 (Lead: Anthropic key-format rule {100,} refuses 99-char org-workspace keys; fix {40,} on main 4121b14b78; alpha 4bd1a236e9 still old): ADMITTED to MVP by me, Gate class 4, Owner lead, board, order doc epic 9, ledger FIFTH ENTRY (13->14, 0 days). Tripwire clause "gate grows" met on its face: PM-needed memo to Exec. Slips now 5. OWED: close-out when fix promoted + served add-key check; gate back to 13; Wed 10-14 check.
- 10-11 12:4x #1978 CLOSED by Lead 12:22 PDT (gate back to 13; my symmetry row written; slip entry 5 stands; alpha still old until promotion, served add-key check on Lead's post-promotion list). #1977: Lead flipped step-2 flag (6127d246df) on case 1; Arch/CXO hold crossed it: flag back to False until the #1884-shaped served case + pinned coverage rule; PORTFOLIO lane unmerged until then. Ceiling 121 on main. Exec updated.
- 10-11 13:2x #1977 licence measurement (Arch's preregistered 20): 0 silent partials, 6 neither (threshold 2) = HOLD. PORTFOLIO last literal STAYS; ceiling 121; Wed reads 121. Step 2 is covered-branch-only, flag False. #1977 admission no longer changes the number. Exec updated; PM question = what Wed reads against (band as set / re-based / other); I bring it Wed if no answer. Cheap path to 120 closed unless new preregistration or router fix.
- 10-11 13:1x HOLD accepted (Arch/Lead): trigger = #1979 ("summarize my current work" -> upload prompt; filed by CXO); when its fix lands re-run the SAME preregistered 20, then decide PORTFOLIO literal. I placed #1979 Production + board (no Gate class; admission = PM's call). Wed reads 121. OWED: watch #1979 fix + rerun + deletion; recount after any landing.

- 2026-10-11 19:0x — Lead→Arch (cc PPM): #1979 fix designed; cause is the summarize_document rail ownership guard, not router/catalog. Part A built on side branch `claude/lead-1979-conversation-source-floor` (0efe6f4c99), held for Arch's nod; no full run owed (no catalog change). Part B (prompt example) is Arch's call, unbuilt. Served-layer check owed by Lead before landing. Then same-20 re-run → PORTFOLIO deletion → 120. Wed reads 121 unless all three land first. No PPM action; ceiling recount after any landing.

- 2026-10-11 19:2x — #1979 part A LANDED on main (39398a32af). Lead's same-20 on the fix branch: 0 silent partials / 0 neither / 20 both (Lead's figures). Waiting on Arch: does the branch run count or re-run on main. Then PORTFOLIO deletion → 120. My recount after landing: 121. Wed reads 121 unless the deletion lands first. CXO closes #1979 on the served quotes. No PPM action; recount after the PORTFOLIO landing.

- 2026-10-11 19:4x — Arch RULED branch run counts (tree identical); PORTFOLIO deletion lands after CI Tests on 39398a32af is green → 120 expected. My recount stays 121 until Lead reports the landing; then recount and ledger. #1984 (CXO, cold two-topic reply) placed Production. Wed reads 120 if the deletion lands first, else 121.

- 2026-10-11 19:3x — CXO accepted and closed #1979 (served quotes read); #1984 already placed Production. Nothing from CXO blocks the PORTFOLIO deletion. Still waiting: CI green on 39398a32af, Lead's landing, then my recount (121 now, 120 expected).

- 2026-10-11 19:4x — PORTFOLIO last literal LANDED (8531742988). My recount: 120 (36 lists); main CI 12/12 green. Lead's tail 90 (29 floor), unverified. Wed 10-14 reads 120 (top edge of band), tail "90, of which 29 are a ruled permanent floor (#1974)". #1984 two halves are Lead's (Production, no Gate class). Remaining: PM's Wed-reading question, Enterprise due_on, Lead's Mon reconfirm → rule (c) row. At Wed: re-print ceiling + tail; bring to Exec same day only if tripwire trips (epic 0 tranche not done / gate list grows).

- 2026-10-11 19:5x — Lead: #1984 half 1 landed (66159f1ecc); half 2 not fixed (router-input change, full-run lane, Lead's/Arch's). Ceiling recount 120 unchanged. No gate effect; both halves Production.

- 2026-10-11 20:1x — #1984 half 1 fully landed + CXO accepted (copy, label rows, lowercase-first rule 51db50efd0). Half 2 = Lead's design to Arch: read_floor_3 adapter wave (get_project_status, maybe get_top_priority), full corpus run, flips 22+25 lenient rows to real scoring. Not tonight; Arch's call whether the lane opens. WATCH: if it opens, ask Arch/Exec whether it is Epic 0 tail (slip source (b)) or a Production lane BEFORE the Wed 10-14 check. Ceiling 120 unchanged (adapters aren't literals).

- 2026-10-11 20:2x — Arch GO read_floor_3 wave (STATUS+PRIORITY, tomorrow START, 4 conditions); Lead corrected: get_project_status is already in the grammar, a description edit (branch claude/lead-1984-status-description, unmerged) fixes #1984; wave is a separate question for Arch. My reading: no slip, not an admission, it's the existing open Epic 0 question (10-02 scope-doc entry). Ceiling 120 unchanged. For Wed read: STATUS/PRIORITY match-rate drop = correction not regression. Hold on a side branch is Lead's; watch whether anything lands on main.

- 2026-10-11 21:0x — Arch accepted Lead's correction: wave NOT opened for #1984 (supersedes the 20:2x GO; revisit when the deletion lane takes STATUS/PRIORITY_PATTERNS). Description edit (branch 40b3c95b33, held) lands at Lead's 10-12 START after the full run + served check. Ceiling 120. Watch item closed.

- 2026-10-12 07:1x — Lead report: #1984 half 2 description path NO-GO under Arch's condition (4) (W1 full run 13 improved / 8 worsened, 4 attributed; W2/W3 keep 3). Branch held 40b3c95b33, main unchanged. Three levers (a land W2 as a trade / b narrow session_activity_query / c known miss, CXO decides closing on half 1) await ARCH's ruling. Ceiling 120 unchanged (Lead re-read it too). No gate effect; no PPM action.

- 2026-10-12 07:4x — #1984 half 2 CLOSED OUT as a KNOWN MISS: Arch refused (a); (b) failed the screen on 2 rows; (c) applied on main (corpus-row note), CXO retitles + keeps #1984 open. No gate effect; ceiling 120. Watch: "let's analyze the risk here" (ANALYSIS survivor at router margin) tips to CLARIFY under any catalog edit — carry it into the next catalog candidate/ANALYSIS lane. Remaining: Lead's Mon reconfirm (rule (c) row); PM's Wed-reading answer + Enterprise due_on.

- 2026-10-12 07:5x — Arch ack: (c) verified on main; "let's analyze the risk here" (yaml:1973) is now a standing member of every catalog/router-input ×6 screen (decisions.log). My watch line is covered by Arch; no separate PPM ledger entry needed. #1984 closed for Arch; retitle is CXO's.

- 2026-10-12 08:1x — Exec relayed xian: Enterprise = 2028-10-30 (fixed: decisions.log correction appended, roadmap bullet rewritten; CLOSED). Sent Exec the re-based band (155−(44−29)=140, ~139–149; Wed 120 reads ~20 below; I recommend the split 29 floor + 30 FILE_REFERENCE + 61 router-quality instead) and the two-line hold/#1978 statement. xian still to choose on the Wed reading; Exec puts it on his card. Still open: Lead's Mon reconfirm (rule (c) row).

- 2026-10-12 08:4x — Web's alpha served turns 5/8: ceiling unaffected (120). #1985-#1991 placed Production + board. #1985/#1990 = possible Class 3 (false "nothing urgent"); NOT admitted; PM-needed question sent to Exec (admit one of them vs leave on Production + known-issues list). If admitted: add Gate class line + Owner, ledger sixth slip entry (gate 13→14, 0 days), tripwire clause "list grows" met → PM same day. Duplicates for Lead: 1985/1990, 1986/1989, 1988/1991.

- 2026-10-12 08:4x — #1985 root cause fixed on main (5d5f7ec88e, Lead); shape (b) nodded by CXO; #1989/#1990/#1991 closed as dups; Helsinki landed. My Class 3 lean → leave Production, admit only if post-promotion Web re-run still shows false "nothing urgent". Update sent to Exec. Trigger: next promotion → Web re-run set → CXO reads. Ceiling 120.

- 2026-10-12 08:5x — #1986: Arch reversed #1754 for thanks/farewell (option 1 GO, 6 conditions; literals byte-identical, ratchets don't move; truth test for the thanks line). No gate effect, ceiling 120. Recount after Lead lands it just to confirm byte-identical (expect 120). #1992 (render half of #1988) placed Production.

- 2026-10-12 09:0x — #1986 LANDED (8ebe568035); my recount 120 (byte-identical patterns, as Arch's condition 1 required). #1985 (b) on main (bb4066fc00). Waiting: Web's served re-run at next promotion (trigger for any Class 3 admit of #1985), Arch's rulings on Lead's two findings (not mine), PM's low-urgency OK, xian's Wed-reading choice, Lead's Mon reconfirm.

- 2026-10-12 09:1x — #1986 condition 2 tightened + landed (cd43832626): durable owner-checked turn count licenses the empty thanks line, else "You're welcome." Compound examples ride next catalog batch (trigger = that batch's rule-7 run). #1993 (test-order leak) placed Production. Ceiling 120, no gate effect.

- 2026-10-12 09:2x — CXO: missing conversation row stays zero (empty form); adds a 31-minute-idle thanks to the served set; closes #1986/#1985 on quoted replies. No gate effect.

- 2026-10-12 09:3x — Arch accepted cd43832626 plus a one-line belt (empty thanks form needs durable zero AND no in-memory assistant turn); Lead's to add. No gate effect, patterns untouched.

- 2026-10-12 09:3x — Lead: #1986 belt landed (d23849fb9f); nothing owed on #1985/#1986 from Lead; CXO closes both on Web's quoted replies at next promotion. #1994 (weekly FLY-AUDIT, auto) placed Ongoing per precedent. Ceiling 120.

- 2026-10-12 14:4x: xian's answers via Exec: alpha promotion approved (Lead runs; xian clicks); #1985 stays Production, re-run set stands, bring back only if still false; #1978 in-and-out does not count against the hold; Wed band question: pros/cons coming from Exec, until then check against band as set. Ledgered in beta-gate-standard.md. PM-OK blocker on #1985 is now CLEARED.

- 2026-10-12 16:5x: CXO closed #1985/#1986 on Web's alpha re-run (trigger did not trip). #1998 [HONESTY] compound floor answer filed: placed Production, NOT admitted; PM decision asked via Exec (memo 16:50). If PM admits: Gate class 3 line, Owner, sixth slip entry (13->14), Wed tripwire met. #1999 Production. Waiting on Lead's cause check for #1998.

- 2026-10-12 17:0x: Exec: #1998 NOT admitted (already fixed as #1997, xian's standing answer); if the served re-run after next promotion still shows it, bring to Exec. Lead closed #1998/#1999 as dupes of #1997/#1996. Arch #2000 + #1995 placed Production. PM-decision deferral on #1998 CLEARED. Armed-slot question settled (Arch+Lead).

- 2026-10-13 13:5x: xian picked reading C for Wed 10-14 (band as set = tripwire, split beside it). Floor answered to Exec: 29 ruled permanent, 30 FILE_REFERENCE out of scope but not ruled permanent (Arch's read owed by Wed), 61 unruled. Wed check: print ceiling 120-ish headline + 3-way split + Arch's read on the 30 + tripwire result; bring to Exec same day. xian-pick deferral CLEARED.

- 2026-10-13 14:5x: CORRECTION: Arch ruled the 30 FILE_REFERENCE removable/inert at 13:38 (floor = the 29). Wed check split: 29 permanent / 30 removable (Lead's unit; ceiling 90 if landed) / 61 unruled. CIO duty rows answered, briefing fixed a817b5d773. Check origin/main for fresh rulings BEFORE sending any memo that says "pending X".

- 2026-10-14 09:3x: xian ruled Wed tripwire Option 1 (MVP does not wait for the 61; met on the number; no slip) + Option 3 (Arch names day-one paths, Lead checks the 61; list or "none" to PPM cc Exec, before 10-23). On arrival: classify each finding against the Gate classes before any MVP issue; routing miss alone = corpus row. Owner of the check: Arch+Lead; mine is the classification and ledger.

- 2026-10-14 09:5x: Option 3 result from Lead: none of the 61 misroutes a day-one turn; no MVP issue; ledgered. Wed tripwire closed on the number. Remaining Epic 0 post-MVP notes (cold "change ... to" row; PORTFOLIO's 14) are Lead's doc §4, not gate items.

- 2026-10-14 13:xx: #2009 (nullable owner_id on 8 tables) placed Production. Trigger to re-place: PM-hand count (Arch's corrected SQL) shows tier-A non-zero or feedback user_id NULL = real data -> classify Class 1/2 and bring to Exec for admission. Result arrives via Exec/Lead/#2009.

- 2026-10-14 13:4x: #1771/#2007/#1783 landed (bc3ede7e35), close on CXO served readings after next promotion. #1943 rework (1) HELD ba732d825a; lands with the clear_todos flip = PM's token on alpha's live flag. When Lead asks for the flip, route to Exec as a decision/ruling item; recount the ceiling after it lands (17->10 ratchet row, regex deletions).

- 2026-10-14 14:0x: Arch ruled #1943 Risk 1 = (a), coupled to the clear_todos flip, with a legacy-path probe at the flip; if it dead-ends, fix (c) = add clear_todos to ACTION_REGISTRY (a grammar change, owes a rule-7 full run; recount ceiling after). Risk 2: disclosure sentence removed (31f936c5c9). Landing waits on PM's flip + probe. No gate effect.

- 2026-10-14 14:2x: Lead: #1943 (c) built (clear_todos into ACTION_REGISTRY + example), rule 7 PASS (x6 identical on 11 rows; full run 472/532, both named regressions identical on main). Standing member "let's analyze the risk here" reads CLARIFY x5 / analyze_blockers x1 on MAIN today = below 6/6 -> Arch's watch (goes to Arch, ANALYSIS margin fix precedes the next catalog candidate; Lead reported to Arch). My thanks/farewell registry examples therefore wait behind that margin fix (blocker: Arch's ANALYSIS fix). Ceiling 90 unchanged. Still held for PM's flip.

- 2026-10-14 14:xx: Arch accepted #1943 (c) (lands only with PM's flip); standing-member watch tripped; ANALYSIS margin fix (additive ACTION_EXAMPLES line, own rule-7 run, member 6/6 on candidate) precedes every later catalog candidate except (c). My thanks/farewell registry examples ride AFTER that fix (blocker: Lead's margin fix). No gate effect.

- 2026-10-14 12:5x: ANALYSIS margin candidate accepted by Arch (b) (member 6/6; 478/532; list-my-projects row re-pointed to list_projects); lands after PM's promotion; it is the catalog unit that clears the way for MY thanks/farewell registry examples (own rule-7 run, additive ACTION_EXAMPLES form, member in the screen). #2010 placed Production; reclassify if "import an existing project" has no chat path (ask Lead/CXO result). P8 "list my projects" served quote at next promotion.

- 2026-10-14 13:2x: #2011 built (held, lands after promotion); CXO ruled copy by tier. PPM: Production stays. Watch list for Class 3 (capability claim that does not exist, on a day-one reply): "import an existing project" (#2010), todo "reprioritize" (l.268), templates 179 "track going forward", files_consciousness 176, toast "Want to try again?". Ask/await Lead's reachability check; confirmed false capability -> classify -> Exec for admission.

- 2026-10-14 13:3x: #2011 five calls ruled (Arch). Watch list now four: "import an existing project", todo "reprioritize" (l.268), templates 179, files_consciousness 176. Toast removed (Arch: 3 formatters have no consumer; deleted).

- 2026-10-14 13:4x: Arch: consciousness templates.py/injection.py unreachable (pending Lead's confirmation) -> templates 179 off the watch list. Watch list now three: "import an existing project", todo "reprioritize" (l.268), files_consciousness 176 (each needs Lead's reachability check).

- 2026-10-14 14:0x: #2011 shrunk 53->20 (held 157ac5c90a). Watch list now ONE: "import an existing project" (#2010; chat path unconfirmed). "reprioritize" failed Lead's check, rewritten on the branch (offer of help, not Class 3 in my read). Held branches awaiting PM's promotion: #1943 (c) + flip, ANALYSIS margin, #2011 shrink, #1771/#1783/#1843 served readings after it.
- 2026-10-14 17:5x: #2009 re-place trigger CLEARED. Arch (citing xian's production count, unverified by me): tier A all zero, feedback user_id zero, project_integrations 3 of 3 null owner_id (tier B). Stays Production; no re-place, no admission. Build is Lead's (from_domain fix in same change as NOT NULL).
- 2026-10-14: #2009 built and held (0a1a1ae077, Lead; lands with batch after PM's promotion). Stays Production. Lead proposes follow-up issues (knowledge_nodes/edges owner threading, #1420 residual; items.list_id NOT NULL) pending Arch's rulings. When filed: place Production (no Gate class evident); ask them for nothing. Re-count nothing (no literal change).
- 2026-10-14 ~18:3x: #2013 (KG owner threading) and #2014 (items CHECK+FK) placed Production + Product Backlog with Gate-class comments. #2013 re-classify trigger: non-zero production count of knowledge_nodes/edges before landing (Arch: PPM classifies; Class 1/4 question to Exec). #2014 trigger: count shows listless items with real user data. #2009 branch now ee085308bc, held for PM's promotion.
- 2026-10-14 18:4x: #2012 (Test says "successful" on revoked grant) placed Production provisionally; Class 3 on its face; DECISION memo to Exec asking admit-or-not (would be open MVP 9→10, slip row 6, 0 days). Blocker: xian via Exec. On "admit": move to MVP, ledger row, criteria line.
- 2026-10-14 18:5x: #2015 placed Production (no live caller; Gate class none). #2013 held 600fd41372 (chained on #2009 branch; 7 held branches; migrations chain q2009nn -> r2013kgnn -> #2014's). KG POST routes were failing outright, so #2013's non-zero-count trigger is near-dormant. #2014 count-first query is a production read on xian's slot via Exec.
- 2026-10-14 19:0x: #2014 held c4a3c9619e (chained after #2013; revision s2014items); #2014/#2015 already placed Production. Two read-only production counts go on xian's next read slot via Exec (Lead's ask to Exec; the revision stops the deploy loudly if either is non-zero). Re-classify trigger for #2014 now = those counts non-zero.
- 2026-10-14 20:3x: Janus relayed xian (20:20): "yes add #2012 to the MVP list". My GitHub write (milestone MVP + body Gate class/Owner lines + comment) was DENIED by the auto-mode classifier; NOT done, nothing written to the ledger. #2012 is still on Production. Blocker: user to allow the write or confirm via Exec. On go: milestone MVP, body lines, comment, sixth slip row (0 days), criteria line 9 -> 10.
- 2026-10-14 21:0x: xian leans against irreversible bulk delete (via Lead); flip not requested. My recommendation sent to Exec: hold flip (D), gate on reversibility (C), interim B for N>1 delete. On xian's yes: file C as Production issue. Ceiling stays 90. Blocker: xian via Exec.
- 2026-10-14 21:2x: #2012 admitted (slip row 6, 0 days; order doc + criteria line done). xian approved bulk-delete recommendation: flip held, #2019 cap (Lead, 10-15 batch), #2021 soft delete (mine, filed). Placed Production: #2017/#2018 (Class 4 candidates), #2019, #2020, #2021. DECISION memo to Exec: admit #2017/#2018? (lean yes), #1943 re-place? (lean yes, symmetry row), #2020 (lean no). Blocker: xian via Exec. Do not write slip row 7 or an un-admission row without word.
- 2026-10-15 10:48: xian (direct): #2017/#2018 admitted Class 4 (slip row 7, 0 days); #1943 to Production (symmetry row); #2020 not admitted. Open MVP 10. Slips 7. Counts + promotion suggested to Exec with xian.
- 2026-10-15 11:1x: CORRECTION: #2014 counts were done 10-14 (0/0, xian); deferral removed. #2013 count trigger dropped. Promotion: xian's word only (Lead Step 0 READY f76a307ecb). Ceiling 90 after the 20 landings. Asked Lead/Arch whether the thanks/farewell registry-examples unit is still owed (margin fix now on main) or moot after #1986.
- 2026-10-15 11:2x: thanks/farewell registry examples DROPPED from PPM's list (Arch: catalog hygiene, not moot, rides Lead's next rule-7 catalog batch; no product acceptance). Step 0 READY stands (Lead correction: staging now f5c8e33c63, gate probe accepts). Promotion: xian's word only.
- 2026-10-15 16:5x: Class 3 watch (honesty, PPM's): Arch found the floor LLM narrating an action code never took ("standup cancelled", #2033; 0 hits in services/). Arch did not file the wider class; if a second instance shows on a served run, file a tracking issue and ask Exec whether it is a Class 3 gate item.
- 2026-10-15 17:2x: DECISION to Exec: admit #2040 Class 3 (lean yes; would be slip row 8, 8 open MVP); #2042 LLM-narration class tracking filed (lean: gate instances, not the class). #2041 placed Production. Blocker: xian via Exec.
- 2026-10-16 07:1x: xian (via Janus, Exec agreeing): #2040 ADMITTED Class 3 (slip row 8, 0 days; open MVP 7); #2042 tracked, instances gated, no class gate. #2040 closes on its served reading after the next promotion.
- 2026-10-16 08:1x: #2048 ADMITTED MVP Class 3 under xian's standing #2042 word (first served instance; slip row 9, 0 days; open MVP 8). #2049, #2050 Production. CXO closed #2008/#2044/#2039/#2033/#2035 (all Production, no ledger rows). Relayed to Exec for correction if the standing word is misread. Blocker on #2048: Lead's trace and fix, then served.
- 2026-10-16 08:2x: #2040 CLOSED on served lines (symmetry row; open MVP 8 -> 7). Twins settled by CXO (#2049→#2045, #2050→#2046 dup). #2051 Production, tracked on #2042 not gated (non-answer, not false; re-place if the named retype fails or a false result is stated). Arch's #2047 catalog fix covers routing only; #2048 floor reach still open (needs alpha log provenance: Lead/Arch). Watch: Web's stale repeat-count observation (per-conversation cache?), Lead to weigh; if filed and it serves a false count on a golden path it is a #2042 instance to gate.
- 2026-10-16 08:3x: #2012 CLOSED (served four-state; row; 7 -> 6); #2052 ADMITTED Class 3 under standing #2042 word (row 10; 6 -> 7; re-place if Lead's repro shows GitHub-side staleness). #2053 Production. Promotion grant in force (Lead dispatches); 'xian's word for promotion' deferral retired. #2045/#2046 reopened by Lead (Production, unchanged).
- 2026-10-16 08:4x: #2054 (intent cache shares context dict; principal can cross users) placed Production; DECISION to Exec: admit Class 2 (lean yes; would be row 11, 7 -> 8). Also concurred with Arch's queue jump + lone promotion on product grounds. Blocker: xian via Exec.
- 2026-10-16 08:5x: #2052 stays admitted pending Web's timed served run or Lead's repro (GitHub search lag → un-admit). #2055 Production. #2048 fix landed 5f75809572 (served close after next promotion).
- 2026-10-16 08:5x: #2048 closes on served acceptance AND Arch's D4 read-only-on-adoption guard; promotion held until the guard is green. #2052: Web's timed run green-lit; GitHub search lag likely → un-admit expected if the count self-corrects in one chat.
- 2026-10-16 09:0x: #2052 UN-ADMITTED on its trigger (GitHub search lag, Web's timed run; CXO: acceptable). Symmetry row; open MVP 7 -> 6. #2054 admission still with Exec.
- 2026-10-16 09:1x: #2057 (how-to archives/adds; live on alpha, pre-existing) Production gated through #1595 (Arch's Phase 3 tail); FYI to Exec. #2056 Production, re-place to a Class 2 ask if the context_assembler cache crosses users.
- 2026-10-16 09:5x: CORRECTION (Exec): the machine-account GitHub login was done 10-15 (xian; Web built the PAT and OAuth test accounts; S5's OAuth leg passed). My 'machine-account login: xian' deferral was stale since 10-15 afternoon; retired. Arch validated #2057 (3520460620); all three wider changes are within the rule; the promotion needs nothing further from Arch.
- 2026-10-16 13:0x: xian ADMITTED #2054 Class 2 (row 11, 6 -> 7). Under his 12:52 principle ('bugs ok, not cavalier with user data or privacy'; Exec: use it for placement), admitted #2059 and #2060, Class 3 privacy, false /privacy claims (row 12, 7 -> 9). All three close live on alpha. Standing principle: privacy and user-data issues are gate items.

- 2026-10-16 15:3x OWED EVERY WEEKLY REVIEW (xian 15:25 via Exec): the count of served instances of a tracked class that I admitted on my own judgment that week, and how many later came out. Through 10-16: 2 admitted (#2048, #2052), 1 came out (#2052). First due in the Ship #066 review (window 10-16 → 10-22). Recorded in the gate standard §Standing rulings.
- 2026-10-16 16:0x OWED: the beta-form read for the design-partner invitation, on the morning it goes. Check four conditions: #2054 served; #2059 (third pass) and #2060 served; the uploads backfill run with zero remaining; no Class 1 open on MVP. Then one line to Comms: beta form or alpha form, never both. #2062 and #2063 placed on Production (#2063 re-place trigger: an invitation beyond the design partners before Production). #2056 item 2 watch retired (checked, no fix).
- 2026-10-16 16:1x The 10-23 bar is recorded (xian 16:07): privacy and security closed and live, the rest disclosed. The known-issues review page is at docs/internal/planning/design-partner-known-issues-review-2026-10-16.md; it waits on xian's review with me (via Exec). Update its rows as items close (#2048 is likely first). Ledger each review outcome. #2061 waits on xian (Exec leans admit).
- 2026-10-16 16:1x OWED: map each of xian's Terms and invitation commitments to a mechanism (test, gate class or served check) once his scaffold answers come back via Comms (docs/internal/design/terms-scaffold-for-xian-2026-10-16.md). Goes into the design-partner invitation.

## 2026-10-16 21:3x STOP: day-close (carry into 10-17)
- **Gate: 8 open MVP.** #1386, #1595, #1913, #2017, #2018, #2064, #2065, #2071. Slips: 0 days moved on every row. Dates 10-23 and 10-30 unchanged.
- **Must-close before partners** (16:07 bar): #2064, #2065, #2071. All ride tomorrow's first promotion slot.
  - #2064 needs xian's live count.
  - #2065 needs Comms' fix 4 (xian's OK) and CXO's served page.
  - #2071 needs a served two-account check (Web), with the unchecked card line quoted per CXO.
  - Ledger each close and update the review page's must-close list.
- **Waiting on xian, via Exec:**
  - admit #2072 (asked 21:35; recommend yes);
  - the known-issues review: section B now has #2042, GitHub create, #2019/#2021, #2067, #2068, #2069;
  - what 10-23 means with no partners named;
  - the backfill zero-count;
  - S5 for #2031;
  - Comms' fix 4;
  - the alpha@ invite line.
- **Lead's lanes tonight:** #2064b, #2071, #2068 with #2070, and #2069. If #2068 and #2069 land live, drop their rows from section B.
- **#2066:** placed Production; its trigger fired on #2071 and is now spent.
- **Owed:**
  - the weekly count of PPM-judged admissions (Ship #066 review): 2 admitted, 1 came out (#2052), and #2048 closed;
  - the beta-form read on the morning an invitation goes, with #2071 now in the conditions;
  - the Terms commitment-to-mechanism map once xian's scaffold answers return.


## 2026-10-17 21:3x STOP: day-close (carry into 10-18)
- **Gate: 9 open MVP.** #1386, #1595, #2017, #2018, #2064, #2072, #2077, #2078, #2080. Slips: 0 days moved on every row. Dates 10-23 and 10-30 unchanged.
- **Must-close before partners:**
  - **#2064:** xian's count run. Lead's line: `fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py web-fresh-test"`.
  - **#2077:** fix 6c3206dd35 rides Sunday's first promotion, then xian checks the field stays empty in his browser.
  - **#2078:** d82b5ce4b3 rides the same promotion, then a fresh invited sign-up through the wizard page in a browser. **Blocked on the invite mint:** HOST's mint was denied by the classifier, so it needs xian's seat rule or his `--apply`. Exec has it.
  - Ledger each close and update the review page's must-close list.
- **Sunday's served closes, not must-close:**
  - **#2072:** #2076 served, then CXO.
  - **#2080:** PA's chain, against CXO's 18:32 acceptance.
  - **#2069 and #2075:** when they pass, drop their section-B rows.
  - **#2079:** Production; one served line.
- **Beta-form read:** the backfill condition was met 10-17 (C2, 0 plaintext). The read is still the alpha form until #2064 and #2077 are closed and live. Send Comms the one line on any invitation morning.
- **Waiting on xian, via Exec:** the known-issues review (sections A and B), what 10-23 means with no partners named, the alpha@ invite line, and the invite mint.
- **Owed:**
  - the Ship #066 weekly count: 3 PPM-judged admissions (#2048, #2052, #2080), 1 came out (#2052);
  - the Terms commitment-to-mechanism map, once xian's scaffold answers return.
- **Main CI:** Tests was red at 3311d40219 (the #2079 pin). Lead's fix 9b7a46c883 was running at 21:33. Check it at START.

## 2026-10-18 21:3x STOP: day-close (carry into 10-19)
- **Gate: 7 open MVP.** #1386, #1595, #2017, #2018, #2067, #2077, #2078. Slips: 0 days moved on every row. 10-23 is the invite checkpoint (xian assesses the alpha and approves inviting); 10-30 is the target for the first partner's access.
- **Must-close before partners (three):**
  - **#2077:** fix 6c3206dd35 is live on alpha. It closes on xian's field-empty check in his browser.
  - **#2078:** fix d82b5ce4b3 is live. It closes on a fresh invited sign-up through the wizard page, using a code from xian's bank (`~/.piper-shared/xian-invite-bank-credential-20261018.txt`; never quote a code in full).
  - **#2067:** landed e13bf3c65f. Monday's promotion, then CXO's served modal check.
  - Ledger each close and update the review page's must-close list.
- **Beta-form read:** the alpha form until #2077 closes live (backfill met; no Class 1 open). After that, send Comms the one line on any invitation morning.
- **Waiting on xian:** section A of the known-issues review (#2017, #2018, #1595), at the 10-23 assessment.
- **Owed:**
  - the readiness read for Exec: write it at the 10-22 START;
  - the Ship #066 weekly count (3 PPM-judged admissions so far; #2052 came out; #2048 and #2080 closed);
  - the Terms commitment-to-mechanism map, once xian's scaffold answers return.
- **Main CI:** 12 of 12 green at 21:33. Alpha `83a2f4e40c`.

## 2026-10-19 21:3x STOP: day-close (carry into 10-20)
- **Gate: 13 open MVP.** Ten must-close: #2089, #2091, #2092, #2094, #2095, #2096, #2097, #2098, #2100, #2101. Also open: #2018, #1595 (both LISTED as known issues), and #1386. Slips: none written. 10-23 is the invite checkpoint ("isn't sacred", per xian 15:05); 10-30 is the target for the first partner's access.
- **Tuesday:**
  - The 07:00 promotion carries every landed fix (#2091, #2092 handler half, #2094, #2095, #2096, #2097, #2100), plus pool_pre_ping and the keychain bounds.
  - Ledger each served close (Web's rows, CXO's acceptance), and update the review page's must-close list.
  - Lead rebuilds #2098 and the #2101 thread surface.
  - #2101 and #1386 criterion 2 close on a full 61-query canonical run on alpha, judged by `claude-sonnet-5-5`.
  - Scenario A and #2103's served pass run after the promotion. If #2103 breaks a step, take it to xian as a Class 4 admission.
- **#2085 track 2:** the email leg is met. It's accepted when the assigned-issue backup is in and forced once (PPM, 10-19 21:3x).
- **Waiting on xian:** the #2087 console (kit ready); the invitation lines (four known-issue lines and the Calendar paragraph); the Terms scaffold answers.
- **Owed:**
  - the beta-form line to Comms on any invitation morning;
  - the readiness read for Exec at the 10-22 START;
  - the Ship #066 count: 3 PPM-judged admissions (window 10-16 → 10-22).
- **Main CI:** 12 of 12 green at 21:33. Alpha `e801b1a309`.

## 2026-10-20 21:3x STOP: day-close (carry into 10-21)
- **Gate: 9 open MVP.** Six must-close: #2089, #2091, #2092, #2096, #2100, #2112. Also open: #2018 and #1595 (both listed as known issues), and #1386. Slips: none written. 10-23 is the invite checkpoint; 10-30 is the target for the first partner's access.
- **Thursday 10-22 (PA, Lead confirmed):**
  - xian signs in to the throwaway Google account and connects it on `web-seed-1386` (target ~09:00; no chat). Web checks the events and gives PA the go.
  - PA runs #1386 on `web-seed-1386` (no later than 12:00), then the OpenAI run on `web-openai-run`, on the same build. Lead holds promotions.
  - The 16:18 rule: if the calendar isn't seeded by 12:00, the nine rows run unseeded, count as they fall and are reported separately. One run.
  - **OpenAI bar** (my 18:2x memo): hard conditions, no wrong provider named, within 5 points on matched rows. If it fails or doesn't run, the invitation says Anthropic only.
  - After both runs, Web asks #2112's, #2091's and #2092's connected rows on `web-seed-1386` (CXO accepted 19:41). #2092 also needs xian's one line.
- **#2100:** the three strings are accepted. Owed: the capability reply's Notion line, served (Web), and a Notion-bound row. I suggested a throwaway Notion (CXO to answer).
- **#2096:** xian's admin read. **#2089:** not served yet.
- **Ledger** each served close; update the review page and the order doc.
- **Checklist** (`beta-formalities-checklist.md`):
  - the keys row: Anthropic only unless the OpenAI run passes;
  - the restart row: CIO's grant condition 3; Lead's quiet count Wednesday; the staging row needs a staging invite (an attended mint);
  - the trust-lines row: two reads open, the null-ciphertext count and Fly backups.
- **Owed:**
  - the beta-form line to Comms on any invitation morning;
  - the readiness read for Exec at the 10-22 START;
  - the Ship #066 count: 3 PPM-judged admissions (window 10-16 → 10-22; today's admissions were all on xian's word);
  - the Terms map, once xian's answers return.
- **Main CI:** 12 of 12 green at 21:33. Alpha `edf95b5c0c` (the tenth promotion, 19:21).

## 2026-10-21 21:3x STOP: day-close (carry into 10-22)
- **Gate: 8 open MVP.** Five must-close: #2085, #2091, #2092, #2096, #2112. Also open: #2018 and #1595 (listed as known issues), and #1386. No slips written. 10-23 is the invite checkpoint; 10-30 is the target for the first partner's access.
- **Thursday 10-22:**
  - The calendar is connected on `web-seed-1386`: the Calendar API is enabled in "Piper Morgan (Alpha)", and Test passed at 10:27.
  - PA runs #1386 by 12:00, then the OpenAI run, on the build `/health` names at the start. Lead holds promotions.
  - **The calendar-seeded rows are six (Q8, Q33, Q34, Q35, Q61, Q62), not nine.**
  - OpenAI bar as set on 10-20, using PA's 36 matched rows.
  - After both runs, Web asks the connected rows for #2112, #2091 and #2092. #2092 closes on "Do I have any meetings this week?" naming the seeded events (CXO and Lead 18:1x). Web also reads the Stage 3+ palette row for #2108.
- **#2085** (Class 4, admitted 15:01): CIO proposes the protection for main, xian rules on it, Lead builds the external restarter, then an attended injected-stop test. Memory is 512 MB since 14:12. There's a conditional checklist row for the interim restart line if 10-30 comes first.
- **#2087:** two Google Cloud projects. Lead maps them after Thursday, and xian picks the home before 10-30. Both invitation Calendar lines are applied; HOST's send check picks one on the morning.
- **#2096:** xian's admin read.
- **Staging restart row:** blocked on staging's master key (HOST, on xian's word). Web can run it until Thu 22:00.
- **Owed:**
  - **the readiness read for Exec at the 10-22 START** (for xian's 10-23 assessment);
  - the beta-form line to Comms on any invitation morning;
  - the Ship #066 count (window ends 10-22): 3 PPM-judged admissions; the admissions on 10-20 and 10-21 were on xian's word;
  - the Terms map, once xian's answers return.
- **Main CI:** 12 of 12 green at 21:33. Alpha `76789a8988`, healthy.

## 2026-10-22 21:33 STOP: day-close (carry into 10-23, xian's checkpoint)

- **Gate: 6 open MVP, 3 must-close.**
  - **#2085:** route (1), a restart without the lease (Arch 17:14). Lead builds, Arch reads the diff, xian pushes, then a second attended test at xian's time.
  - **#2132:** Arch ruled (i), the handler-only split, first; then single catalog edits screened ×6. Lead starts at the 10-23 START.
  - **#2096:** xian's admin read.
  - Also open: #2018 and #1595 (known issues) and #1386.
- **Waiting on xian, via Exec:**
  - admit #2142 (Class 3, calendar events as "activity from your repo"; Lead: small, rides with #2132's split);
  - fold #2138 into #2132's close (my 18:34 ask);
  - accept a triaged criterion 2.
- **#1386 criterion 2, on the 18:30 re-run:** routing 90.2% after triage (raw 88.5%); expected-pass 92.7% after triage (raw 46.3%). Recorded on #1386, boxes **not** ticked; the raw figures are read first.
- **Invitation:**
  - **Anthropic only.** The OpenAI run met the hard conditions but scored −21.4 on matched rows, plus #2139.
  - The Calendar line is the plain connect step (the Alpha project is verified).
  - The restart line has no fixed hour.
  - The key line names the 5-day backups.
  - The Terms map is closed under Option 2.
  - Open: the ciphertext count (HOST or xian), HOST's send-morning checks, and xian's rewrite.
  - The Comms beta-form line goes on the invitation morning, after a recheck that no Class 1 or 2 is open.
- **Placed today:** #2125, #2127, #2128, #2129, #2130, #2131, #2132 and #2133 to #2135, #2137 to #2140 and #2142 on Production (#2128 and #2132 later admitted); #2126 on Ongoing.
- **Ship #066 count:** admissions this week on xian's word, as on 10-20 and 10-21. Today's three (#1524, #2128, #2132) were PPM proposals that xian admitted. The window ends today; whoever drafts Ship #066 counts from the ledger rows.

## 2026-10-23 21:33 STOP: day-close (carry into 10-24, Saturday)

- **Gate: 3 open MVP** (#2018 and #1595 are known issues; #1386 is the close-out). **Must-close: none.** Invitations are xian's to time.
- **Invitation morning (xian names it):** (also recheck the #2122 known-issues line: search still unsupported, uploaded-file asks work; Comms 10-24 17:56)
  - recheck that no Class 1 or 2 is open;
  - send Comms the beta-form line;
  - recheck checklist rows 21 and 22.
- **HOST's open send items** (none of them PPM's): the Terms text (xian), the wizard and code checks (Web), the stored-key count (Lead and xian), Calendar after #2087, Comms' packet, and the roster.
- **Sprint relabel waits on xian adding three options** in the web UI: `PROD-HONESTY - Failed Reads Say So`, `PROD-DATA - Data Boundaries, Privacy & Terms`, `PROD-CONVO - Conversation Reliability`. Then:
  - relabel about 20 issues to H, 22 to D and 28 to V, one item at a time;
  - move PROD-INFRA's rows to D or Q.
  - The tables are in `production-sprint-proposal-2026-10-23.md`. Regenerate them from a fresh board export first.
- **Map review:**
  - **After xian's Saturday read:** file C1's two issues (deletion with purge, and export), and move #651 and #336 into D as children of #2062.
  - C6 (Readiness lane or Ongoing) goes to xian as one line.
  - Arch's C2 and C5 answers are still to come; reply when they arrive.
  - F18 needs a body read of the "about 50" no-promise issues before xian rules.
  - Round 3 (the living-map brief) starts when Exec opens it.
- **#2151 (honesty sweep):** Lead extends FLOOR-ABSENT to six gathers, then GH-NONSTRICT. These are Production work, not gate items.
- **Main CI:** 12 of 12 green at 21:33. Alpha healthy.
- **Round 2 (21:36):** C5 and F29 moves applied in the plan (H 25, V 29, E 27; 221 open). F28 waits on PA via Exec.
- **10-24 06:3x, for the C1 filing:**
  - The deletion issue carries Arch's constraint: a deletion record outside the snapshot (owner id plus time, no content), re-applied after any restore.
  - Its text quotes retention as a number tied to F1, following HOST's rule: whoever changes retention changes the promise in the same change.
  - C6: Exec, HOST and Arch are on the Readiness lane (only Terms-backed items gate); CXO leans Ongoing.
  - F28: xian's word on his own PoC install, via Exec.

## 2026-10-24 21:33 STOP: day-close (carry into 10-25, Sunday)

- **Gate: 3 open MVP** (#2018, #1595, #1386). **Must-close: none.** #2167 closed served before admission, so there's no ledger row. #2154's admission and close rows are written.
- **Waits on xian (via Exec):**
  - ratify `docs/internal/product/promises.yaml` (20 promises; E6 waits on ESSENCE v1.1). Then create the `promise:` and `seam:` labels and apply promise, seam, journey and surface labels by reading each body. Hand-check every red cell, then publish `production-map.html` as one artifact link;
  - the 3 Sprint options (PROD-HONESTY, PROD-DATA, PROD-CONVO). Then relabel H, D and V per item from a fresh snapshot;
  - F28 (#1242, #1244, #1245): his PoC install;
  - the invitation morning: recheck no Class 1 or 2 open, send Comms the beta-form line, recheck checklist rows and the #2122 line (search unsupported; upload works). Comms can drop the sharing line (CXO 20:21: Share hidden, pass).
- **Friday 10-30:** first since-last diff against `dev/snapshots/project-board-2026-10-24.tsv`; take a fresh snapshot first.
- **Watch:** #2171 (H, Lists "Items: 0"), Lead's provider display-name nit on #2167's dialog (not a gate), #2166's D repair (Arch's shares table).
- Main CI 12 of 12 green at 21:33; alpha healthy on `228f3cec14`.

## 2026-10-25 15:33 WORK (interim)
- Waiting on Exec: the backward edge #1706 (PUB) → #1441 (C), and #2018 (MVP) blocked by #2172. Both are Sprint or admission calls; I wrote no row.
- Waiting on others: Arch's word on whether #1706's edge is truly "must close before"; Web's consent-page run on #2175; CXO's Friday spot-check (no green cell yet).
- Map: v4 at https://claude.ai/artifact/63oejcubP3zEj617nFAN68. The snapshot now carries `state_reason`. The Friday 10-30 since-last diff is due.
- Placed today with the Sprint field blank (PM-gated): #2174 (C) and #2175 (PUB).

## 2026-10-25 21:33 STOP: day-close (carry into 10-26, Monday, send morning)
- **Send morning (trigger: xian's send, about 07:00):**
  - Recheck the known-issues lines' issues: #1595, #2042, #2021, #2018 and #2087 open; #2019, #2122 and #2101 closed as of 18:36. Strike any whose issue has closed, and tell Comms.
  - Recheck for open Class 1 or 2 issues and for the MVP gate (#2018, #1595, #1386).
- **Carry-over promise: DONE 10-26 18:36 (commit time).** T9-carry-over is in promises.yaml (private-beta), with #2157 labelled and the map at v9.
- **Waiting on Exec:**
  - The backward edge #1706 (PUB) → #1441 (C). Arch calls it a hard edge, so the fix is a Sprint move.
  - ~~#2018 (MVP) is blocked by #2172~~: settled 10-26 12:34. #2172 closed (pins-only), and Exec was told the question is moot.
  - The #1706 move is a Sprint call; I write no row.
- **Waiting on a promotion (#2177, manifest unknown; HOST backs pull by digest, which goes to PM via Exec):**
  - Served rows for #2176, #2172 and #2171. alpha `eaba23311d` doesn't yet carry `8bb53cf107`; unverified tonight.
- **Placed today with the Sprint field blank (PM-gated):** #2174 (C), #2175 (PUB), #2176 (H), #2177 (Q), #2178 (C).
- **Map:**
  - v6 at https://claude.ai/artifact/63oejcubP3zEj617nFAN68. The snapshot now carries `state_reason`; 5 edges are recorded.
  - Friday 10-30: the since-last diff (fresh snapshot, regenerate, republish to the same URL).
  - CXO's spot-check waits on a green cell.
- Plan total 208 open, which matches the snapshot.

## 2026-10-26 21:33 STOP: day-close (carry into 10-27, Tuesday)

- **Done today:**
  - Invitations sent at 21:00 (xian's report via HOST).
  - T9-carry-over registered, with #2157 labelled; map at v9.
  - Roadmap v19.1, with the send noted by 21:35.
  - The #2018←#2172 question to Exec is settled by #2172's close.
- **Waiting on Exec, then PM:** the backward edge #1706 (PUB) ← #1441 (C). It is a Sprint move, and I write no row.
- **Waiting on xian:** the #2018 recovery run (rollup v624, PA's card `8d29e7a8c0`). CXO judges the served words. When #2018 closes, MVP is #1595 plus #1386.
- **10-27 07:00:** Lead promotes alpha (#2177, pull by digest). Re-read `/health` for the new sha at the 09:33 fire. If it changes, the known-issues lines need a recheck only if the delta touches their code.
- **Fri 10-30:** the since-last diff (fresh snapshot, regenerate, republish the same artifact). The baseline hard stop and MVP `due_on` are unchanged; PPM proposes no date.
- **CXO's Friday spot-check:** waits for a green cell.

## 2026-10-27 21:33 STOP: day-close (carry into 10-28, Wednesday)

- **Alpha:** `a1f46faafc` (promoted 20:27, by digest). #2177 and #2181 are both closed.
- **#1706:** Arch ruled 10-27 18:29 that #1703 is not blocked by #1441, so (b) stands and my (a) is withdrawn. The Sprint move (#1706 out of PUB) waits on xian via Exec. I write no row.
- **#2182:** split from #2151 and closed the same evening, pins-only (1 of 4 rows served). The #1703 ← #2182 edge is met.
- **Waiting on xian:** the #2018 recovery run (rollup, PA's card). Once it closes, MVP is #1595 plus #1386.
- **Fri 10-30:** the since-last diff (fresh snapshot, regenerate, republish the same artifact). The map is at v12. No date is proposed.
- **CXO's Friday spot-check:** waits for a green cell.

## 2026-10-28 15:30 WORK (interim)

- **Gate:** 3 open MVP (#2184, #1595, #1386). #2018 closed served 14:36 (PA, on CXO's ruling); ledger close row is in. #2184 was admitted 10:26 (FORTY-SECOND ENTRY, Class 3, PPM's judgment under the 10-16 standing words, relayed to Exec with a one-word undo).
- **#2184 close bar (PPM, comment 6478708881):** the served two-step ("can you show me issues from just one milestone?" then "MVP") must answer from a `milestone:"MVP"` read, or say code's plain can't-list line. The one-step read is already served PASS (PA 14:30). The pick is built on `claude/lead-2184-pick` `62f0adfff8` (unnumbered, title-only, header names repo and milestone). It lands after #2186 Open 1 on a promotion, and the two-step check is the promotion after that (Lead runs it, CXO judges the header).
- **PUB now leads with the #2042 confabulation class:** #2042 (diagnosis), #2183, #2185 (count line scope: CXO asked PA which scope the 263 was), #2186 (unit 1 landed; Open 1 on a branch; unit 2 owed).
- **H gained** #2187, #2188 and #2189 (10-28). #2189's sweep seat and method are Arch's to name.
- **Still waiting:** #1706's Sprint move (xian, via Exec); Fri 10-30 since-last diff (its date); CXO's Friday spot-check (a green cell).
- **Map:** v15 at https://claude.ai/artifact/63oejcubP3zEj617nFAN68.

## 2026-10-28 21:33 STOP: day-close (carry into 10-29, Thursday)

- **Gate:** 3 open MVP (#2184, #1595, #1386). #2018 closed served 14:36.
- **#2184:** alpha `49e0904c3c` carries the pick and the repo fix (`992b47fbc8`). The close waits on the served two-step (Lead runs it, CXO judges the header). If Lead posts PASS, Lead closes it, and PPM writes the ledger close row (gate 3 → 2).
- **#2189:** persist ruled. Lead's plan in CXO's order: the row 1 slice (carrying 8, 10, 11 and 19), then the nonces onto Redis, then the row 3 table. The row 3 migration needs xian's word via Exec. #2187, #2188, #2189 and #2190 are all in H.
- **PUB leads with #2042** and its kin #2183, #2185 and #2186.
- **Waiting:** #1706's Sprint move (xian, via Exec); Fri 10-30 since-last diff; CXO's spot-check (a green cell).
- **Map:** v16 at https://claude.ai/artifact/63oejcubP3zEj617nFAN68. Plan total 209.

## 2026-10-29 15:33 WORK (interim)

- **Gate:** 3 open, #2205 (Class 4), #2201 and #1386. FORTY-FIFTH admission was #2205.
- **Order (PPM 15:27, #1386 comment 6509789041):**
  1. 67daf6c261 to alpha (it carries #2199, #2200, #2201).
  2. PA's arm-path read and the B re-run.
  3. #2205 lands with Arch's four conditions; CXO's strings passed at 15:25. Then Tests and READY.
  4. Third promotion inside the freeze.
  5. xian re-runs A3 and A4 on fresh accounts.
  6. Row 2 and row 4, once each, on that build.
  7. Row 5 final read, row 6 (the beta letter's final draft), then go/no-go.
- **Row 5 interim:** 0 P0, 0 P1 since 10-26; CI 12/12 green.
- **Row 6:** no beta draft yet; it waits on xian and HOST, 10-30 at the earliest. HOST will raise the #2184 alpha-partner note there.
- **Briefing MVP line:** says 3 open (fixed 15:28). Update it as rows close.
- **Carried:** #1706 Sprint move (xian via Exec); Fri 10-30 since-last diff; CXO spot-check.
- **18:33 update:** Arch GO on #2205's four deltas; Tests green on 1bf24cf4c8. The third promotion waits only on Lead's READY mail, then xian's dispatch; xian is ready for A3 and A4 tonight. #2200, #2199 and #2201 closed served. #2184's line now goes to the three alpha partners as a note (form is xian's call via Exec) and in the beta letter, with the "Launch" placeholder. **Strike both when #2184 closes served.** 110 closed Production issues backfilled with a Sprint (record: `dev/active/production-closed-sprint-backfill-2026-10-29.md`); 5 set aside for xian (#1647, #1662, #2081, #2083, #2146).

## 2026-10-29 21:33 STOP: day-close (carry into 10-30, Friday)

- **Gate: 2 open MVP, #2205 and #1386.** Alpha serves `e234776150` (the third promotion, #2205). xian ran or is running A3/A4 on two fresh accounts; on CXO's PASS, close or confirm-close #2205, then the ledger row (2 -> 1), the order-doc line, the briefing MVP line and a #1386 note. Gate becomes #1386 alone.
- **#1386 rows:** row 4's tests/security box green on `e234776150` (ticked); alembic-head and `ENCRYPTION_MASTER_KEY` boxes open, owner unnamed, confirm at row 5. Row 2 (PA) once on `e234776150` after A3/A4. Row 5 is mine: no P0/P1 since 10-26, CI green (12/12 at 21:33). Row 6: beta letter final draft (Comms, after HOST and xian, 10-30 at the earliest). Then xian's go/no-go.
- **Production 224 open**, plan matches (0 unplanned). #2210 and #2211 placed in Production, Q, 21:36; map v28. Strike #2184's lines (partner note record, beta known-issues) when it closes served.
- **Carried:** xian's call on the 5 set-aside closed issues (#1647, #1662, #2081, #2083, #2146); the #1706 Sprint move (xian via Exec); Friday's since-last diff; CXO's spot-check.

## 2026-10-30 06:33 START (interim)

- Friday since-last diff done (`dev/active/production-weekly-diff-2026-10-30.md`); the generator no longer counts closed-in-both issues as scope. Next weekly diff: Fri 11-06 against `project-board-2026-10-30.tsv`.
- #2216-#2218 replace #2212-#2214 in H. Production 228.
- Today is the gate standard's hard stop (10-30); gate 2 open (#2205, #1386). Dates are xian's.
- Otherwise as at 10-29 STOP.

## 2026-10-30 21:33 STOP: day-close (carry into 10-31, Saturday, letters morning)

- **MVP gate PASSED.** #1386 and the MVP milestone closed on xian's Go (17:03). The hard stop held, 0 days moved. Ledger row in beta-gate-standard.
- **Beta letters:** xian sends them Sat 10-31 morning; HOST mints codes with him. The letter is final with 9 known-issue lines. My send-time check is 9 of 9 (19:51, #1386 comment 6538036530). Re-check only if something changes before the send: a promotion, an issue closing, or an edit to the block. The Slack inbound gate is off (PA read `disabled` at 20:25). Open at STOP: Exec's #2218 question (can a beta account reach the hosted MCP?). PPM answered that the beta scope doesn't offer it; PA and Lead read reachability.
- **Freeze:** no promotion until the letters go.
- **10-31: this list now gates the v0.9.0.0 tag** (Lead tags after it; the bump is on main at c9791112d8). Tag rule in my 10-31 memo to Exec and Lead: rows 2 and 3 hold and every check is quoted; only a regression, or a failure of something the letter says works, blocks. I send Lead "tag: go" or "tag: held".
- **NEXT PROMOTION CHECK LIST** (the full text is in my 20:36 memo to Exec, `ppm-to-exec-cc-arch-lead-cxo-pa-2238-placed-next-promotion-check-list-…`). The build carries #2225, the #2230 setter validation, #2236 parts 1 and 2 with #2233 and the four fixes (93bd29ccd7), #2237 with the connect listing (a3b3645787, 5c7f15d794), and #2218 if it lands.
  - Row 2: a full canonical run, after PA updates Q45's expected route to action.
  - Row 3: A1 and A2, plus B's confirm and the reverse case.
  - Served checks, each quoted:
    - #2225: three turns.
    - #2236: the capability reply, plus "couldn't check" on a failed status read.
    - #2233: Q1 stops after the name; the due line shows once on a greeting or todo list.
    - #2236 fix 3: the empty insights reply.
    - #2237: greyed cards with no button, the wizard, "connect my slack", and direct POSTs refused.
    - (#2218 dropped: served on MCP v15 10-31 06:53, closed.) Lead's reads: #2206, the notice line, the text-block pick.
  - Then read `gh issue list --state closed --label fix:not-served` and take labels off only on a quoted check.
  - Then re-check the letter's lines: line 7 (#2225) and line 9 (#2236) are struck from later editions on their served checks.
  - Separately, the set_default_repo flip (xian's word; CIO, or HOST with xian present), then PA's probe and one row 2 run.
- **Tracking audit (xian's test):** 28 product issues, 27 open plus #2225 (`fix:not-served`). Rule in decisions.log 17:09.
- **Board:** Sprint set on all open Production issues on xian's yes (81, 19:5x). New ones since have empty Sprints: #2238 (C → PROD-RECONNECT) and #2239 (PUB). I asked Exec whether xian's yes stands for new placements.
- **Plan:** 241 open, 0 unplanned. Map v44 at https://claude.ai/artifact/63oejcubP3zEj617nFAN68; republish after this STOP's rebuild.
- **First Production sprint candidates** are ready for xian's priorities talk after the letters (`docs/internal/planning/first-production-sprint-candidates-2026-10-30.md`). Exec sets up the conversation.
- **Carried:** xian's call on the 5 set-aside closed issues (#1647, #1662, #2081, #2083, #2146), via Exec; the #1706 Sprint move (xian via Exec, not resolved today); CXO's spot-check. Next weekly diff Fri 11-06 against `project-board-2026-10-30.tsv`.
