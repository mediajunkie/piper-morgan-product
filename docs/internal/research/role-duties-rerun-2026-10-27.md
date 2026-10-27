# Role duties re-run: did the Drift line move the specialist share? (2026-10-27)

**Asked by:** the 10-13 report's own test (`role-duties-operational-vs-official-2026-10-13.md`, suggestion 1): "re-run this count around 10-27. If the specialist share hasn't moved, the Drift line is being written but not acted on."
**Owner:** CIO. **Status:** second read. Next run with the next Agent 360 round.

## Answer in four lines

1. **The Drift line moved the share for some roles, not for the cohort.** Of the 9 roles measurable both times, the specialist share rose for 4 (CXO, Comms, Docs, CIO), held for 2 (Arch, HOST), and fell for 3 (Exec, Web, PA). The falls are in the week of the invitation send, when served-run checks and readiness work took the week. That's real work, but it's not on those roles' cards.
2. **Written duties are better kept than two weeks ago.** 128 of 166 duties (77%) are operational, against 65% on 10-13. 14 (8%) aren't seen, against 23%. Part of the change is shorter lists, because the 10-13 sort retired several duties, so this is not all behaviour.
3. **Moved duties still hold, and a trigger kept by habit decays in days.** Every duty moved into a mechanism is still running (13 of 13 again). Two triggers added on 10-13 as log habits have already lapsed: Web's one accessibility line per push (10-13 to 10-17, none on the 10-24 and 10-25 pushes) and Docs's merge-keeper sweep at START (last logged 09-30).
4. **PA's card and PA's week don't match.** 0 of 108 headings went to card priorities 1 and 2 (the MCP program, R7 packaging). The last MCP deploy was 10-13. The week went to served-run verification, which the card doesn't name. Either the card or the work is wrong, and that's HOST's and Exec's call.

## Method

- Same as 10-13 (that report's Method section), with three changes:
  - Duties that the current briefing marks retired are excluded and listed.
  - Roles with template "##" headings are also classified at "###" or by entry content, and the method is named per row.
  - Windows: duty evidence from the 09-27 to 10-26 logs (30 or 31 per role); focus share for 10-20 to 10-26, seven full days to match 10-13's seven. Every role has 7 logs in that window.
- Evidence came from three Sonnet subagents under a fixed brief (A: Exec, Lead, Arch, PPM; B: CXO, Comms, Docs, PA; C: Web, HOST, CIO). Synthesis and spot-checks are CIO's.
- **Spot-checks by a different method** (direct reads and the API, not the agents' keyword searches), all confirmed:
  - #992 is closed (04-30).
  - The MVP milestone is at 3 open and 1,284 closed.
  - CXO's and PA's "##" totals for the window are 147 and 108.
  - Lead's briefing says promotions need "PM's explicit word", while decisions.log 10-20 11:23 records the standing grant without a cap.
  - `services/intent/intent_service.py` is 19,468 lines.
  - The roadmap is at v19.1.
  - CIO's briefing named the 04-17 audit, m-55, 70 files and `archives/session-logs/`.
- **Limits:** one rater per role and no second rater. NOT SEEN means the keywords were absent. The focus split is a heuristic, and the method differs where headings are templates. It's comparable over time only where the method matches, as marked below.

## Per role

| Role | Duties | Oper. | Moved | Not seen | Contra. | Unclear | Focus 10-13 (10-07..13) | Focus 10-27 (10-20..26) | Same method? |
|---|---|---|---|---|---|---|---|---|---|
| Exec | 15 | 10 | 2 | 1 | 0 | 2 | 29 / 105 (28%) | 34 / 216 (16%) | yes, "##" text |
| Lead | 15 | 14 | 0 | 0 | 1 | 0 | not measurable | 80 / 335 (24%) at "###", strict | no baseline |
| Arch | 16 | 10 | 1 | 3 | 0 | 2 | 13 / 42 (31%) | 34 / 110 (31%) | yes |
| PPM | 15 | 14 | 0 | 1 | 0 | 0 | not measurable | 17 / 90 (19%) by content, strict | no baseline |
| CXO | 15 | 9 | 1 | 5 | 0 | 0 | 9 / 44 (20%) | 72 / 147 (49%) | yes |
| Comms | 15 | 13 | 2 | 0 | 0 | 0 | 8 / 36 (22%) | 30 / 110 (27%) | yes |
| Docs | 15 | 10 | 4 | 0 | 0 | 1 | 9 / 27 (33%) at "###" | 38 / 88 (43%) at "###" | yes |
| PA | 15 | 10 | 2 | 0 | 1 | 2 | about 8 / 14 at "###" | 0 / 108 at "##" (4 / 130 with priority 3) | partly |
| Web | 15 | 14 | 0 | 1 | 0 | 0 | 17 / 64 (27%) | 11 / 122 (9%) | yes; served checks (priority 4) not counted |
| HOST | 15 | 12 | 0 | 2 | 0 | 1 | 34 / 97 (35%) at "###" | about 45 / 125 (36%) at "###" | yes, heading text only |
| CIO | 15 | 12 | 1 | 1 | 1 | 0 | 0 / 70 | 1 / 79 by heading; 8 / 79 (10%) by content | heading yes; content new |
| **All** | **166** | **128** | **13** | **14** | **3** | **8** | | | |

**Not seen (14):**
- CXO (5): Colleague Test scoring, #992 voice oversight (closed 04-30, yet still listed), #950 floor monitoring, calibration through use, the triangle drift memo.
- Arch (3): the legacy-classifier retirement check (due 09-30), pattern-catalog upkeep, catalog citation audits.
- HOST (2): role assignments and recovery, watching xian's coordination overhead.
- Exec (1): routing the cross-pollination brief.
- PPM (1): Colleague Test and quality-threshold scoring (the briefing says it hasn't happened).
- Web (1): the accessibility hold (event-driven; none may have arisen).
- CIO (1): the innovation backlog (untouched since 09-02).

**Contradicted (3):**
- Lead: "promotions on PM's explicit word only", in the briefing and on the card, while Lead promotes under the standing grant (10-16, with no cap since 10-20).
- PA: the card's "never see a bearer credential in full" against a 10-23 log line saying a basic-auth string printed once. The log doesn't establish whether that string counts as a bearer credential.
- CIO: pattern sweeps listed as a duty and also called deprecated. Fixed today.

**Lapsed inside "operational"** (the act happened in the window but stopped): Web's "Pipeline:" line (10-19 and 10-20 only) and its accessibility line per push; Docs's merge-keeper sweep; PPM's ceiling recount (last 10-15); CIO's research hub (stalled since 10-06).

## Briefing lines that are wrong when read

Each role fixes its own. The subagents' notes on each row are in CIO's 10-27 scratch, and every line below was checked by direct read or the API where marked.

| Role | Line | What is true |
|---|---|---|
| Lead | Promotions "on PM's explicit word only" (lines 39 and 63; also on the card) | The standing promotion grant (10-16), cap dropped 10-20 (decisions.log 11:23). **Checked.** |
| Exec | "Roadmap (v15.0)"; the "update `exec-open-items-tracker.md` every session" lines and startup steps 3 and 4 | roadmap.md is v19.1 (**checked**); the tracker is marked superseded in the same briefing |
| Arch | `intent_service.py` 15,607 lines; about 16K lines over 32 files | 19,468 lines (**checked**); the subagent counts 59 files and 49,703 lines for the package |
| Arch | the path `reviews/2026-08-architectural-review/reorientation-plan.md` | it lives under `docs/internal/architecture/reviews/` |
| PPM | `services/intent_service/canonical_retest_scorer/` | doesn't exist (also found on 10-13); roadmap is v19.1, not v19.0 |
| CXO | #992 and #950 as standing disciplines; MVP "~50 issues" | both closed (#992 **checked**); MVP is 3 open (**checked**) |
| Comms | template-audit "16 checks as of v1.11" | the skill is at v1.16 (checks not recounted) |
| Docs | update-calendar skill v1.4; footer "Last Updated March 19"; the merge-keeper sweep "mandatory at every START" | v1.6; frontmatter is 10-13; not logged after 09-30 |
| PA | "Live, MCP v11"; milestone counts dated 10-09; "AX Testing" as a future event | v12 and v14 deployed 10-13; MVP is 3 open; the Standing duties section retires AX testing |
| Web | "No test runner or browser here"; "this host can only produce types/lint/build"; frontmatter 08-03 | jest and Chrome run, per Web's own logs |
| HOST | footer "Last Updated: 2026-09-22"; "ESSENCE v1.1 … still a draft file" | frontmatter is 10-26; ESSENCE.md is v1.1, ratified 10-25 |
| HOST | **rule 8:** the "Human Collaborator Integration" list (lines 144 and 145, **checked**) names outside people. The subagent also reports a name in the HTML comment at line 91 (the comment's position is checked; I didn't read it) | reported to Exec by line number, without names, per hard rule 8. One advisor may be xian's Piper Morgan advisor, the rule's one exception; that's Exec's to judge, and removal and history are Exec's and xian's call |
| CIO | the 04-17 audit as most recent; m-55 and 70 files; `archives/session-logs/`; pattern sweeps as a cadence; the backlog "updated at audit cadence" | **fixed today** (the 10-14 audit; m-56 and 71 files; `dev/YYYY/MM/DD/`; sweeps marked as from incidents; backlog marked dormant) |

## What this suggests (each item is the named role's call)

1. **The Drift line is acted on where the role's week allows it, and dropped when a send week arrives.** The 10-13 test anticipated a stronger trigger for this case: a dated standing-items row per role, one specialist unit per day, which carries a cost when missed. That's worth trying for the three roles whose share fell (Exec, Web, PA). It's HOST's call as role health, and each role's for its own row.
2. **A habit added as a trigger needs a mechanism within a week, or it lapses.** Web's accessibility line and Docs's sweep are both cheap to mechanize: a line printed by the push or START script, as m-36's 10-23 corollary describes (a status line where the agent already looks).
3. **PA's card needs a decision.** Its week went to served-run verification. Either that belongs on the card, or the MCP and R7 work needs time back. That's HOST's and Exec's call.
4. **Fix the wrong lines.** Lead's promotion line first, because it contradicts a standing grant that Lead uses daily.
5. **Next run** goes with the next Agent 360 round (11-06). Use the same methods per row, so the comparison holds.
