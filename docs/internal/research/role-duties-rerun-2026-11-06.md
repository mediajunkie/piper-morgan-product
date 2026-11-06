# Role duties, third run: what the Drift line and the MVP close did to the specialist share (2026-11-06)

**Asked by:** the 10-27 re-run (`role-duties-rerun-2026-10-27.md`), "next run with the next Agent 360 round", plus its open test: *if the share is still down for Exec, Web or PA after MVP reads 0 open, a specialist-unit row is warranted.* MVP closed 10-30 with 0 open (GitHub API, checked 11-06).
**Owner:** CIO. **Status:** third read. Paired with Agent 360 v0.6 (fielded 11-06), for HOST's synthesis.

## Answer in five lines

1. **The 10-27 test fires for Exec and PA, and is unclear for Web.**
   - **Exec:** 19% broad, 2% strict, against 28% on 10-13 and 16% on 10-27. Still down after MVP closed.
   - **PA:** 8% at "##" (14% with priority 3) against its reverted card. 10 of its 12 specialist entries fell on 10-30 and 10-31, and 2 of 60 after that. About a third of its week is still served-run checks, which the card no longer names.
   - **Web:** about 20%, against 9% on 10-27 and 27% on 10-13. Its logs changed heading level on 10-27, so the rise is partly the method.
   - The specialist-unit row is HOST's call (role health), and each role's call for its own row.
2. **Written duties are slightly less kept than on 10-27.**
   - Operational: 118 of 159 duties (74%), against 77% on 10-27.
   - Not seen: 22 (14%), against 8%. Most of the rise is Arch (5) and HOST (4), roles whose duties are event-driven or watch-type, where a quiet week reads as NOT SEEN.
   - Contradicted: none this time, against 3 on 10-27.
3. **Habit triggers lapse again after they're restored.**
   - Docs's merge-keeper sweep ran 10-27 and 10-28 after the last report, then 0 of 8 STARTs.
   - Web's accessibility line resumed 10-27 and was skipped on the 11-05 push.
   - That is m-36's 10-23 corollary a second time: a habit restored by a report holds for about as long as the report is fresh.
4. **Briefings drift at about the same rate.** About 45 wrong-when-read lines across 11 briefings, counted from the batch summaries (some spot-checked below), on top of the 10-27 fixes. The fastest-staling lines are hand-typed versions and counts: roadmap v19.1 → v19.2, MCP v14 → v20, `intent_service.py` 19,468 → 21,226 lines, `read/` 19,400 → 28,502 files. A number in a briefing is stale at its next fold.
5. **This instrument has reached its limit.**
   - Three of eleven rows can't be compared cleanly with 10-27: Web and Docs because their log formats changed, HOST because this run's rater was stricter.
   - The "strict" definition 10-27 used for Lead and PPM was never written down.
   - One rater per run, with a different rater each run, means the noise between runs is about the size of the changes. The next run needs a fixed classifier (below).

## Method

- Same as 10-27 per role (its "Same method?" column), with these windows:
  - Duty evidence: 10-06 to 11-05, 31 logs per role (Arch 32).
  - Focus share: 10-30 to 11-05, seven days, 7 logs per role.
- **Raters:** three Sonnet subagents under a fixed brief (A: Exec, Lead, Arch, PPM; B: CXO, Comms, Docs, PA; C: Web, HOST, CIO). Synthesis and spot-checks are CIO's.
- **Spot-checks by a different method** (direct read, `gh`, `git log`, `wc`): 20 claims (each issue and each CIO line counted), all confirmed.
  - PA's card reverted at `66f26e3cae` (10-30 17:08).
  - `find mailboxes/*/read -type f`: 28,502.
  - #2197, #2250, #2229, #992 and #950 are all CLOSED.
  - PA's "Live, MCP v14" while v20 serves (PA's 11-05 log).
  - Lead line 64 "refused by the auto-mode classifier … xian dispatches", while 9a was applied 11-03 (decisions.log 17:36).
  - The roadmap's header is v19.2 and Exec's line 232 says v19.1.
  - `wc -l services/intent/intent_service.py`: 21,226.
  - ESSENCE.md is v1.1, and Arch's line 61 says v1.0.2.
  - HOST line 132: two outside advisors by first name (rule 8; reported to Exec without the names).
  - All six of CIO's lines (72 methodology files, m-57, the 11-03 audit, v4 for every seat, skill v1.63, the tracker's last change in git 07-23).
  - The MVP milestone: closed, 0 open.
- **Limits:**
  - One rater per run, no second rater.
  - NOT SEEN means the keywords were absent.
  - The focus split is a keyword heuristic. Each batch's sensitivity range is quoted per row.

## Per role

| Role | Duties | Oper. | Moved | Not seen | Contra. | Unclear | Focus 10-13 | Focus 10-27 | Focus 11-06 (10-30..11-05) | Comparable? |
|---|---|---|---|---|---|---|---|---|---|---|
| Exec | 15 | 11 | 1 | 2 | 0 | 1 | 28% | 16% | 19% broad, 2% strict | yes, "##" text; "broad" counts any xian: heading, an upper bound |
| Lead | 15 | 13 | 1 | 0 | 0 | 1 | n/m | 24% strict | 43% strict, 67% broad | approximate; 10-27's "strict" undefined; template headings 11-04 and 11-05 undercount |
| Arch | 16 | 9 | 2 | 5 | 0 | 0 | 31% | 31% | 26% by heading, 44% by content | heading figure yes |
| PPM | 15 | 13 | 1 | 1 | 0 | 0 | n/m | 19% | 27% (13% without fire entries) | approximate |
| CXO | 13 | 7 | 1 | 3 | 0 | 2 | 20% | 49% | 49% (44–55%) | yes |
| Comms | 13 | 12 | 1 | 0 | 0 | 0 | 22% | 27% | 46% (about 43% strict) | yes |
| Docs | 15 | 10 | 4 | 0 | 0 | 1 | 33% | 43% | 26% (29% with priority 3) | partly; log format changed 10-29/30 |
| PA | 12 | 8 | 2 | 2 | 0 | 0 | about 57% | 0% | 8% at "##" (14% with priority 3; 12% at entry level) | against the reverted card |
| Web | 15 | 12 | 0 | 3 | 0 | 0 | 27% | 9% | 20% (24% loose) | no; heading level changed 10-27 |
| HOST | 15 | 11 | 0 | 4 | 0 | 0 | 35% | 36% | 19% (about 40% loose, not counted) | no; stricter rater |
| CIO | 15 | 12 | 1 | 2 | 0 | 0 | 0% | 10% by content | 4% by heading, 8% by content | yes |
| **All** | **159** | **118** | **14** | **22** | **0** | **5** | | | | |

**Not seen (22):**
- **Arch (5):** the legacy-classifier re-check (#1595 closed 10-29, no re-check logged); the scope-bet gate (event-driven); catalog citation audits; naming the promise in rulings; "Audit the Composition" and "Verify Before Building".
- **HOST (4):** role assignments and recovery; trust-property stewardship; the PM-attention (m-39) count; watching xian's coordination overhead.
- **CXO (3):** including Colleague Test scoring, a trigger duty that CXO's 10-13 log says "happens, not logged".
- **Web (3):** the accessibility hold; the pipeline-integrity hold; the repo-confirm check before commits.
- **Exec (2):** cross-pollination routing; role-transition handoff readiness.
- **PA (2):** see the batch file.
- **CIO (2):** the network research hub (its only hit after 09-28 is 10-06; the trial was held to post-MVP); the innovation backlog (file unchanged since 09-02, now labelled dormant in the briefing).
- **PPM (1):** Colleague Test and quality-threshold scoring.

**Lapsed inside "operational"** (done in the window; last done more than 7 days before 11-05, for a daily or per-event duty):
- **Exec:** `aging-standing-items.sh` (10-09).
- **Lead:** the supersession gate (10-12).
- **PPM:** the ceiling recount (10-16); `sprint-truth.py` (10-23).
- **Web:**
  - Medium RSS freshness (10-08).
  - The observation-queue count (10-13).
  - The START `Drift:` line (10 of 31 logs, none 11-01 to 11-05).
- **HOST:** the alpha@ watch (10-28).
- **Docs:** the merge-keeper sweep (10-28).
- **Comms:** the voice-guide read (10-28).
- **PA:**
  - R7 packaging (10-15).
  - Routing-decision logging (10-27).
  - The research signal (missing on 4 of 7 days).

**Not lapsed, worth saying:** Docs's omnibus (31 of 31 days, 10-05 to 11-04) and its Step 1d nudge check (every START). Both are skill steps, not habits.

## Briefing lines that are wrong when read

Each role fixes its own. Full lines with numbers are in CIO's 11-06 scratch (staleness3-A/B/C.md). Rows marked **checked** were confirmed by CIO by direct read.

| Role | Wrong line (summary) | What is true |
|---|---|---|
| Lead | Line 64: dispatch refused on the seat, "xian dispatches" (**checked**); line 50, a session cron | The allow was applied 11-03, and Lead dispatched 11-03, 11-04 and 11-05. LaunchAgent since 11-02 |
| Exec | Roadmap v19.1 at line 232 (**checked**); frontmatter and footer 04-27; migration handoff review live at lines 66 and 134-146 though line 32 retires it; Friday map diff as Exec's; six workstream memos | v19.2; edits through 10-31; PPM ran the 10-30 diff; nine memos |
| Arch | ESSENCE v1.0.2 at line 61 (**checked**); `intent_service.py` 19,468 lines, 59 files; 7 plugins in `services/plugins/`; 79 ADRs and 81 patterns; #1595's trigger pending | v1.1; 21,226 lines (**checked**), 70 files; 5, under `services/integrations/`; 80 and 76; #1595 closed 10-29 |
| PPM | Card priority 1 leads with the MVP gate; `sprint-truth.py` every fire; write directly to `mailboxes/`; the canonical retest scorer sentence; two empty criteria-line fields | MVP closed 10-30; fires use `gh issue list`; CLAUDE.md routes mail through `mail-send.sh`; the scorer doesn't exist |
| CXO | Lines 264-267: #2197, #2250 and #2229 open; #992 and #950 as standing disciplines (**checked**, all closed); line 352 log filename `cxo-opus-log` | Closed; `cxo-code-log` |
| Comms | Line 43, Ship authorship (#067 was xian's own); lines 101 and 112, MVP and beta-gate metrics | Stale since 10-30 |
| Docs | Line 85, about 19,400 files in `read/` (**checked**: 28,502); lines 144-145, the merge-keeper sweep at every START; the Session Start Protocol (156-176) has no omnibus or nudge step | Not followed since 10-28; Step 1d is in the tick skill |
| PA | Line 187, "Live, MCP v14" (**checked**); milestone counts at 201-202; line 265, "commit to `pa/` branch"; line 192 sends users to alpha's Connected apps | v20; MVP closed; main-direct; alpha redirects to beta |
| Web | Line 63, "this host can only produce" types, lint and build (contradicts lines 46 and 56); line 94, portfolio §2 dated 08-04; frontmatter 10-27 behind the 10-30 pointers | jest and Chrome run; the portfolio frontmatter is 11-02 |
| HOST | Lines 165-168, keychain rows open; line 173, #1967 open; lines 161-164, invites not yet out; lines 188-189, #2179 disposition with Exec; **line 132, rule 8 (checked)** | Deleted 10-26; closed 10-31; out 10-26 and 10-31; #2179 closed 10-26; line 132 reported to Exec by number, names not copied |
| CIO | m-56 and 71 files; the 10-14 audit as latest; mail v4 a two-seat pilot; the Exec tracker for project state; skill v1.62 | **Fixed 11-06** (m-57, 72 files; the 11-03 audit; every seat 11-09; BRIEFING-CURRENT-STATE "Now"; since v1.62) |

## What this suggests (each item is the named role's call)

1. **The specialist-unit row, for Exec and PA.**
   - The 10-27 test was "still down after MVP reads 0 open", and it is down for both.
   - Web is unclear because the method changed.
   - HOST, Exec and PA declined the row on 10-27 because of the send week. That reason no longer holds. It's HOST's call, with Exec and PA for their own rows.
2. **A restored habit needs a mechanism, not a second report.**
   - Docs's sweep and Web's accessibility line came back for days, then lapsed again.
   - Both are cheap to print: Docs's in the START output (Step 1d already prints the omnibus check), and Web's in the push script.
   - Each role's call, or CIO can write the tick-skill line on a yes.
3. **Briefings should cite where a number lives, not the number.**
   - "roadmap.md (its header has the version)" instead of "v19.1"; `wc -l` instead of 19,468.
   - Of the roughly 45 lines, the hand-typed versions and counts are the ones that will be wrong again within a week.
   - `briefing-pointer-check.sh` could flag a hand-typed version next to a path. That's CIO's to build, if HOST and Exec think it's worth it.
4. **PA's card and PA's week still differ.** A third of the week was served-run checks the card no longer names, and R7 hasn't moved since 10-15. That's HOST's and Exec's call, as on 10-27.
5. **The next run needs a fixed classifier.**
   - For CIO: a script that reads each role's headings and bodies against a published per-role marker list, so two runs measure the same thing.
   - The marker list is each role's call: what counts as its specialist work. CIO will ask each seat for 5 to 10 markers before building it.
   - Next run: the next Agent 360 round, about 12-18.

## CIO's own row

4% by heading and 8% by content is low. The window's CIO output was:
- the 11-03 methodology audit;
- m-57;
- PP-003;
- the deferred-security audit;
- the mail v4 review.

Those sit in a few long entries among many mail-wake entries, and the heading method undercounts them. The research hub and the innovation backlog are honestly NOT SEEN. The hub was held to post-MVP, and MVP closed 10-30. Restarting it, or retiring it from the card, is mine to raise with Exec.

Verified how: three subagent batch files (scratch staleness3-A/B/C.md), spot-checked by CIO by a different method (20 claims, listed under Method). The table totals were computed from the batch summaries and add to 159. Layer: repo text, git and the GitHub API. Denominator: 11 of 11 roles, 7 logs each in the focus window.
