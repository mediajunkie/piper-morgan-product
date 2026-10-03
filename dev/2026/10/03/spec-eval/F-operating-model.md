# F — Operating model: cohort, roles, duty cycle, mailboxes (Spec evaluation, Phase 2)

Snapshot: piper-morgan-product `a191856164` (working tree is 16 spec-eval commits ahead; none touch the surfaces measured here). Scripts and outputs: `metrics/F-mail.py`, `F-overlap.py`, `F-alerts.py`, `F-roles.py`, `F-pm-away.py`, `F-repo-weight.sh`, `F-watch-grep.sh`, plus `.out` files and `F-sessionlogs.out`, `F-bot-issues.out`. Default window: **8 seven-day buckets ending 2026-10-03** (mail) or **4 weeks 2026-09-05..10-03** (roles). Layers: record = the repo's own prose (mail, logs, CLAUDE.md, script headers); git-history = commits; live-probe = the GitHub REST API.

**Guiding question answer, in one paragraph.** Yes, change things. Over the last four weeks, 62–90% of each standing role's commits are coordination: mail, logs, heartbeats, stops. PM is addressed on 82% of all memos, about 78k words a week, which is roughly 5 hours of reading if PM read them all. PM's mailbox shows that PM doesn't: 708 memos sit unread since the 2026-09-11 bulk sweep. The attention rollup is the channel that actually reaches PM. The watchers aren't duplicates of each other. The pattern is one new watcher per incident, and the record shows those watchers failing (false clears, alerts on compliant behavior) about as often as it shows them catching anything. Coordination machinery caused at least 25 incidents in the cited surfaces. Recorded catches by that machinery after the fact are sparse. The leaner moves with the most leverage: one PM digest instead of cc-by-default; event-triggered wakes instead of 63 fires a day; heartbeats moved out of git; fewer standing roles. Details in §7.

---

## 1. Role map (4 weeks, 2026-09-05..10-03)

Source: `metrics/F-roles.out`. Each role's commits are split into coordination commits (subject class `mail|log|hb|hb-last-invoked|stop|heartbeat`) and other commits. "Replies received" counts other roles' memos whose `in-reply-to` names this role's sent memo; it's a lower bound on consumption, because many replies omit the header. Briefing, carry-forward and standing-items figures are file sizes in KB at the snapshot.

| role | lane (ROSTER) | other commits | coord commits | coord share | memos sent | % cc/to PM | replies recv / memo | session logs (words/day) | briefing+carry-fwd+standing KB |
|---|---|---|---|---|---|---|---|---|---|
| exec | synthesis, Ship, rollup | 161 | 586 | 0.78 | 202 | 97% | 0.51 | 28 (2,054) | 19+24+11 |
| arch | ADRs, patterns | 96 | 408 | 0.81 | 117 | 79% | 0.35 | 27 (1,517) | 18+13+44 |
| cxo | UX, MUX | 224 | 406 | 0.64 | 137 | 84% | 0.49 | 28 (2,594) | 23+6+58 |
| ppm | PDRs, roadmap | 187 | 361 | 0.66 | 63 | 68% | 0.29 | 29 (1,972) | 22+3+5 |
| cio | methodology, watchdogs | 185 | **1,318** | **0.88** | 131 | 87% | 0.27 | 28 (1,795) | 18+2+51 |
| host | network health | 72 | 441 | 0.86 | 70 | 80% | 0.29 | 29 (2,282) | 13+8+11 |
| comms | blog, Ship voice | 86 | 448 | 0.84 | 54 | 59% | **0.06** | 29 (1,941) | 12+12+9 |
| lead | dev coordination | **392** | 644 | **0.62** | 166 | 45% | **0.71** | 28 (2,536) | 11+8+2 |
| pa | PM assistant | 87 | 354 | 0.80 | 62 | 58% | 0.35 | 28 (1,441) | 25+11+12 |
| docs | omnibus, merge-keeper | 268* | 536 | 0.67 | 82 | 43% | 0.24 | 29 (2,526) | 12+16+12 |
| web | website | 41 | 390 | **0.90** | 57 | 98% | 0.18 | 29 (1,962) | 9+12+17 |

\*`docs(` is also a conventional-commit type, so the docs row's "other" column is inflated.

Fires per day, from the registry cron expressions (`dev/active/duty-cycle-registry.tsv`): docs 7; exec 5; cio 3; the other eight roles 6 each. That's **63 fires a day** in total.

Material every fire reloads, at chars÷4 (sizes from `F-roles.out`; the D-measure workstream owns the exact M1b.1 measurement):

| file | size | approx. tokens |
|---|---|---|
| CLAUDE.md | 64 KB | ~16k |
| duty-cycle-tick SKILL.md | 79 KB | ~20k |
| BRIEFING-CURRENT-STATE.md | 159 KB | ~41k, when read |

| id | claim | layer | denominator | evidence | conf. | implication |
|---|---|---|---|---|---|---|
| F1.1 | Coordination is the majority of every standing role's commits, from 62% (lead) to 90% (web). | git-history | all 11 standing roles, 4 weeks | `F-roles.out`; D0 §1 (Sept: 7,318 coordination commits vs 192 product commits) | high | Most commit throughput goes to coordinating, not building. This is consistent with D0's H1 verdict, SUPPORTED. |
| F1.2 | cio wrote **1,026 `hb-last-invoked` commits in 4 weeks** (~37 a day) against 3 scheduled fires a day. Those commits are 78% of cio's total. | git-history | cio, 4 weeks | `F-roles` class breakdown; e.g. `hb-last-invoked(cxo): suppressed WORK 2026-10-03 10:18` | high | The heartbeat writes to git even on suppressed fires. This is pure churn: it inflates history and triggers deploy builds (F4.21). |
| F1.3 | Observed consumption varies 12-fold. Lead's memos draw 0.71 replies per memo, comms's draw 0.06 and web's 0.18. | record | sent memos in window (1,141) | `F-roles.out` | med (lower bound) | Comms and web mostly broadcast. Their mail could become non-addressed log entries. |
| F1.4 | Outputs with no observed consumer: (a) the **708 unread memos in PM's inbox**, 672 of them from Sept, untouched since PM's bulk sweep of 2,299 files on 2026-09-11; (b) `docs/omnibus-logs/`, consumed only by Exec's Ship skill (step 3) and the narrative skills, never cited back by PM in the sample; (c) most cc copies. | record + git-history | PM mailbox, full | `ls inbox`; `git log --diff-filter=D -- "mailboxes/xian (ceo)/inbox"` → 2026-09-11 "moved xian read mail to read", 2,299 files | high (a); med (b) | PM's mailbox works as an archive, not a reading queue. Writing to it is mostly wasted effort. |

## 2. PM-facing recurring outputs (M1b.2)

| output | producer | cadence | size (sample) | evidence PM acts on it |
|---|---|---|---|---|
| Attention rollup (`exec-attention-rollup-current.html` + dated copies) | Exec | daily; 1–7 revisions a day (Sep 29–Oct 2: 2/4/7/5) | 505–4,427 words, median ~1,000 | PM-ratified design (skill §Delivery, 2026-06-13). Items get PM rulings that are relayed the same day ("Pace-normally is relayed and in force"). Strong. |
| Memos addressing PM (to or cc) | all roles | continuous | **54–343 memos/week, 21k–128k words/week** (`F-mail.out`) | PM wrote 2 memos ever (`xian (ceo)/sent/`). 708 sit unread. PM's decisions arrive as relays (69 `ruling-` memos in 8 weeks). |
| Workstream reviews (6–9 a week, cc PM) | each role | weekly (Fri) | ~3–5k words/week (in-sample) | Inputs to the Ship. PM ruled the Ship can't be drafted without all of them (draft-weekly-ship:94). |
| Ship synthesis (`exec-shipNNN-synthesis-*.html`) | Exec | weekly | 1.4–2.0k words | PM picks the theme and does the voice pass (skill). Strong. |
| Weekly Ship draft/post | Comms | weekly | — | Published. Strong. |
| BRIEFING-CURRENT-STATE | any agent | several times a week (10 commits Sep 20–29) | ~21k words | Agent-facing in practice. No PM-reading evidence. |
| Omnibus log | Docs | daily | 23–36k words/week | Feeds the Ship and the narrative. No direct PM-reading evidence. |
| Watchdog stall memos | duty-cycle-watchdog | on event | 89 memos (Jun 47, Jul 37, Sep 5) | Only 31 of 180 role-alerts were followed by that role's commit within 3h (`F-alerts.out`). |
| Bot issues (Weekly Docs Audit, Role Health, Agent-360, Housekeeping, Skill-candidates, Quarterly) | GH Actions | weekly or monthly | 14 issues in 8 weeks, 11 closed | Handled by agents. Low load (`F-bot-issues.out`). |
| Cowork scheduled jobs on PM's machine | — | — | **unobservable** (U5) | — |

**Overlap test, as pre-registered.** Script: `F-overlap.py`. Weeks: A = Sep 20–26, B = Sep 27–Oct 3. There are 5 outputs, so 10 pairs per week.
- A *topic heading* is either a heading or the leading bold phrase of an item.
- A heading *recurs* if its issue number, or at least 60% of its content words, appears in the other output.
- *Lenient* matching checks against the other output's full text. *Strict* matching checks against its headings only.
- A pair *overlaps* only if more than 50% of headings recur in both directions.

| | lenient: overlapping pairs | lenient: outputs involved | strict: overlapping pairs | one-way subsumption (lenient) |
|---|---|---|---|---|
| Week A | 2 (Ship-synthesis↔workstream 0.59/0.61; omnibus↔current-state 0.57/0.75) | 4 | 0 | 9 of 10 pairs |
| Week B | 3 (Ship-synthesis↔workstream 0.75/0.52; workstream↔omnibus 0.90/0.51; omnibus↔current-state 0.69/0.60) | 4 | 0 | 9 of 10 pairs |

Two patterns stand out:
- **Containment.** In both weeks, 76–100% of the rollup's, the Ship synthesis's and the workstream memos' topics already appear in the omnibus.
- **Different headings.** Strict heading-to-heading overlap is zero. The outputs cover the same topics under different headings.

Two caveats on the sample:
- Only the workstream reviews named `workstream-06x-*` were sampled (3 for week A, 5 for week B). Reviews filed as `review-*-ship-06x` weren't.
- The week-A rollup version at the cutoff was a short 302-word version.

**PM reading load.** Source: `F-mail.out`. These are words addressed to PM, not words PM read.
- **Memos:** 623k words over 8 weeks, a mean of **78k words/week, about 312 minutes (5.2h) at 250 wpm**. The range is 95 min (week ending 10-03) to 564 min (week ending 09-26).
- **Unmirrored files** (watchdog alerts, external agents): about 4.3k words/week, roughly +17 min.
- **Rollups:** about 6–7k words/week, roughly +25 min.
- **Ship synthesis:** about 2k words, roughly +8 min.
- **Total:** about **5.8h/week** addressed to PM by default. Adding the omnibus would add 1.5–2.4h.

What PM demonstrably acts on, all per week:
- about 19 "ask-like" memos (filename or subject contains ask, decision or approve; 151 in 8 weeks);
- 16 decisions.log entries mentioning PM (131 in 8 weeks);
- 30 memos whose body cites a PM ruling (relays, so double-counted).

At most about **16–19 decisions a week come out of about 194 PM-addressed memos a week**. That's under 10%.

| id | claim | layer | denominator | evidence | conf. | implication |
|---|---|---|---|---|---|---|
| F2.1 | 82% of memos addressed PM (1,551 of 1,899 in 8 weeks). The 2026-09-11 "cc only for a/b/c" ruling took about 3 weeks to bite: 93.7% before it (5 weeks), 78% in the 2 weeks after, then 28% in the week ending 10-03. | record | all sent-mirrored memos, 8 weeks | `F-mail.out` | high (method: frontmatter to/cc) | The prose rule eventually worked but lagged. The rollup already covers this need. |
| F2.2 | Under the lenient reading, 4 PM-facing outputs overlap in each of the 2 sampled weeks. Under the strict heading reading, none do. | record | 5 outputs × 2 weeks | `F-overlap.out` | med (operationalization is mine) | Overlap here takes the form of the omnibus and current-state containing everything, plus the Ship pipeline restating the workstream memos. |
| F2.3 | PM's real intake channel is the rollup plus chat, not the mailbox. | record + git-history | PM mailbox | F1.4; skill §Delivery | med-high | Stop cc'ing PM by default. Make the rollup the only PM-addressed artifact, with a link to source memos. |

## 3. Watchers (M1b.3)

| signal | mechanisms (trigger) | distinct failure mode between them? | recorded catches | recorded false alarms / false clears |
|---|---|---|---|---|
| Per-role liveness | `duty-cycle-freeze-check.sh` (registry + session-log + heartbeat), run by `duty-cycle-watchdog.sh` (launchd/cron, hourly → PM memo + notification + Slack), by rollup Step 0, and by duty-cycle-tick; Pard's user-crontab freeze-watchdog (registry header; **external, unobservable**); `cohort-position.sh` (carry-forward table); `heartbeat-interior-coverage.py` | Yes, per their own headers. Invocations of freeze-check are the same mechanism used in several places. Whether Pard's crontab watchdog is that same script is unverified. | 180 role-alerts (Jun–Sep). 178 matched real git silence of 7–97h (e.g. ppm 48–97h, Jun 22–24). 09-28 cio wedge caught about 20h late. 31 of 180 were followed by a commit within 3h. | lead flagged 3× on 07-27 while alive ("alerting on compliance", registry:38). 5 roles dark 6 days while only arch alerted (registry:88). PARK-NO-EXIT alerts (Sep). Registry self-triggering corruption detector (registry:6). |
| Cohort-wide freeze / usage ceiling | `cohort-freeze-detect.sh`; `usage-capture.sh` + `usage-lookup.sh` (`dev/heartbeats/usage-per-account.tsv`, 185 rows since 09-23) | Yes (header: per-role staleness can't see a cohort freeze) | none recorded after creation (unverified) | 08-06 freeze: PM was the detector (pre-dates the tool) |
| Stranded branches / unpushed work | `merge-keeper-sweep.py` (Docs, daily); sign-off checklist (per agent); PreCompact hook; `worktree-safety-sweep.sh`; `mail-send.sh` self-reconcile | Yes (sweep vs. self-check) | merge-keeper: 124 "clean" mentions vs ≤2 finding-like mentions in Aug–Oct Docs logs | sign-off checklist reported false-clean in 3 distinct ways (history log 72–105). **`.claude/settings.json:67` registers `"PreCompact": []`**, yet CLAUDE.md says it is "confirmed firing". If it fires, it's from user-level config outside the repo (unverified). |
| Doc/state staleness | `check-staleness.py` (session-start hook + weekly-docs-audit.yml); `check-refresh-promises.py`; `aging-standing-items.sh`; `scope-drift-check.sh` (scope-guard.yml); `check-unboarded-pm-items.sh`; link-checker, monthly-housekeeping, agent-360 workflows | Mostly yes (different objects) | bot issues: 14 in 8 weeks, 11 closed | check-refresh-promises reported "Every CHECKED promise held" while an opted-in doc was invisible (script header, 08-04) |
| CI red | `ci-liveness.yml` → `ci_liveness_check.sh` (weekly) | single mechanism | 8 of 9 runs succeeded since 08-13 (live-probe). Catches: 1 log mention, unverified | — |

**Verdict.** I found 0 signals, and at most 1 if Pard's crontab job duplicates the launchd watchdog, watched by ≥2 mechanisms with no distinct failure mode. The redundancy criterion is **not met**. The real cost runs the other way: **about 20 watchers built one per incident** (script headers cite the incident each was born from), each with its own maintenance and its own false-clear history.

## 4. Machinery cost vs value

Denominator: the incidents recorded in CLAUDE.md, `claude-md-history.log`, the registry header, and the headers of the watcher scripts. These are the surfaces the cohort uses to record lessons, so the list is a lower bound.

**Caused by the coordination machinery itself** (layer: record; confidence high unless noted):

| # | date | incident | source |
|---|---|---|---|
| 1 | 06-21 | PM's uncommitted voice-pass edits destroyed **twice** by a duty-cycle `git checkout -- .` run to clear MANIFEST noise | CLAUDE.md:650 |
| 2 | June | 6 of 9 cycling roles lost durable log entries (cycle log in sprint-cleaned `dev/active/`) | CLAUDE.md:294 |
| 3 | 06-25..27 | every agent stall was the subscription cap | anthropic-billing-model.md:25 |
| 4 | 07-04 | phantom-peer self-attribution drift after a context gap | CLAUDE.md:45 |
| 5 | 07-25 | worktree provisioned **5,393 commits behind** | CLAUDE.md:98 |
| 6 | 07-25 | hooks dead everywhere (invalid matcher); probe confound produced 4 wrong datasets across 5 seats | CLAUDE.md:99,107 |
| 7 | 07-27 | watchdog alerting on compliance (lead 3×) | registry:38 |
| 8 | ≤07-31 | CronCreate's two silent death modes, undocumented | registry:53 |
| 9 | 08-04 | refresh-promise checker false clear | script header |
| 10 | 08-06 | cohort-wide usage-limit freeze 13:12–21:30; PM was the detector | cohort-freeze-detect.sh:5 |
| 11 | 08-08 | work destroyed by a direction-blind `git checkout <ref> --` | history log:207 |
| 12 | Aug | MAIL subject auto-closed #1677 | CLAUDE.md:641 |
| 13 | 08-27 | audit ran on a checkout 33 commits stale | CLAUDE.md:256 |
| 14 | Sep | 91 orphaned worktrees / 36 GB | worktree-safety-sweep.sh:6 |
| 15 | 09-14 | subagent fan-out exhausted a shared ceiling and darkened 2 roles. CLAUDE.md:413 says 30 dispatches; usage-capture.sh:4 says 48 (the docs disagree). | CLAUDE.md:413; usage-capture.sh:4 |
| 16 | 09-18 | alpha-tester invite triaged inbox→read in the same commit; board missed it | check-unboarded-pm-items.sh header |
| 17 | 09-22 | sign-off checklist false-clean (3 modes) | history log:72–105 |
| 18 | 09-23 | registry corrupted twice in 24h by `csv` round-trips | registry:6 |
| 19 | — | bearer credentials in mailbox memos for 8 days (#1845) and in session logs (#1885) | CLAUDE.md:715 |
| 20 | — | 5 roles dark 6 days, coverage blind spot | registry:88 |
| 21 | 09-27→28 | cio session wedged about 22h in a setup wizard opened by the LaunchAgent wrapper | registry cio row |
| 22 | recent | deploy pipeline built 43 images in 9h, about 85% for heartbeat/log commits | `exec-attention-rollup-current.html` §Running in the background; med |
| 23 | 07-14 | Ship #051 drafted with a workstream memo missing | draft-weekly-ship:94 |
| 24 | → 09-11 | PM cc'd on everything; PM ruling | CLAUDE.md §cc |
| 25 | 4 weeks | cio heartbeat churn, 1,026 commits | git-history, F1.2 |

**Caught by the machinery** (after creation, in the record):
- The watchdog detected real silences in June–July: 178 git-consistent role-alerts across several multi-day episodes.
- The watchdog caught the 09-28 cio wedge, about 20h late.
- The check-branch hook works in the stage-then-commit idiom (CLAUDE.md:104).
- The rollup's live-state pass and cross-role verification caught the Ship #062 count error (43/34 → 91/57) before publication (exec memo 2026-09-26) and the "Inversion never served a live turn" defect (lead workstream-063).
- merge-keeper: about 0 catches in 126 sweeps. ci-liveness, cohort-freeze-detect, aging-standing-items and autoclose-guard: no recorded post-creation catch found (unverified, not searched exhaustively).

Overall: **25 or more machinery-caused incidents against about 4–6 identifiable catches** (record layer, med confidence, because outcome language in logs is inconsistent). As a rough sign, phrases like "false positive / false alarm" appear in 1,429 mailbox files, "genuine stall / true positive" in 355 (`F-watch-grep.out`). These phrases aren't specific to watchers, so treat the comparison as directional only.

## 5. PM attention load and bus factor

- **Decisions routed to PM:** about 16–19 a week (§2), against about 194 PM-addressed memos a week.
- **What can't proceed without PM:**
  - the Ship's theme, voice pass, and Medium publication (draft-weekly-ship);
  - funding and pace calls on the usage ceiling (the rollup's top priority on 10-03: both accounts projecting over 100% of the weekly cap);
  - seat/model rulings;
  - re-prodding dead sessions. Watchdog memos tell PM to "re-prod the listed role's session".
- **What changed under LaunchAgent:** the duty-cycle cron now survives restarts (registry rows from 09-25 to 10-02). PM is no longer the only restart path, but the cio wedge (22h) shows a stuck seat still waits for a human or for Pard.
- **Natural experiment (n=1):** PM was away about July 11–18 (`dev/2026/07/18/...pa-code-log.md`; comms slate proposal: "week of July 11–18 (PM was away)").

  | | product commits | product lines changed | coordination commits |
  |---|---|---|---|
  | the away week | 46 | 2,216 | 361 |
  | neighbouring weeks | 37–58 | 3.3k–9.0k | 246–417 |

  Ship #052 was still drafted while PM was away. So the cohort keeps running, with lower product throughput (`F-pm-away.out`). Confidence low: one week, confounded with the pre-Amber period.
- **Two-week absence, predicted:**
  - About 1,500+ unread PM-addressed memos would pile up, at roughly 750/week at peak.
  - Two Ships would block at the voice pass, or publish without it, which would break PM's own rule.
  - Ceiling and pace decisions would default.
  - The roles would keep generating mostly coordination output.

  These are inferences, not observations.

## 6. Running cost

| what | sourced? | data |
|---|---|---|
| Cohort LLM | **Partly.** Two subscription accounts (pipermorgan.ai, designinproduct.com), % of 5h/7-day caps from 2026-09-23 | `dev/heartbeats/usage-per-account.tsv` (185 rows). Week resetting 10-02: pipermorgan.ai peaked at **96%** of the 7-day cap, designinproduct.com at 76%. Week resetting 09-24: designinproduct.com 93%. `scripts/usage-audit.py` estimates token mix; the rollup reports premium-model share rising from 23.7% to 48.3% while volume fell 19%. **Dollar amounts: unsourced.** Plan tier mentioned ("Pro Max 20x = purchase decision"), price not stated. |
| Product API spend (console) | No | `docs/internal/operations/anthropic-billing-model.md` separates it from cohort spend; no figures |
| Fly (alpha) | No | `fly.toml`, `deploy/fly/*.toml` exist; no bills |
| Amber host | No | no cost figure found ("$24/month stops when it lands" in a dev/active plan: context unverified) |
| GH Actions minutes | No | — |

The cohort runs at its subscription ceiling. That makes token spend on coordination (63 fires a day × 36k+ tokens of fixed rules each, see §1) a direct competitor of product work for the same capped resource. Confidence med: whether the per-fire reload is prompt-cached is unverified.

## 7. Constraints that may no longer apply, and leaner alternatives

**Constraints from the Desktop era that are now stale:**
- *Session-scoped CronCreate with 7-day expiry.* Mostly replaced by LaunchAgents (cascade 09-25 → 10-02). The registry still carries a large layer of CronCreate prose and re-arm protocols.
- *Model B worktree rules.* CLAUDE.md still carries both models and long history.
- *Preview-pane delivery of the rollup.* Desktop-specific (skill §Delivery).
- *Liveness inferred from work output.* Replaced by heartbeats, but the heartbeats commit to git.

**Workarounds from the Amber era that could now go:**
- MANIFEST regeneration;
- push-to-ref mail and its reconcile step;
- hooks that are advisory only (CLAUDE.md:101).

| alternative | removes | migration risk / what breaks | steelman of the status quo it replaces |
|---|---|---|---|
| A. **One PM digest**: rollup only; cc PM never except a/b/c; memos link to it | about 5h/week of addressed reading; the 708-unread archive | items can get lost when the compiler misses one. Mitigated by `check-unboarded-pm-items.sh`, which already exists. | cc-everything gave PM full visibility, but PM evidently doesn't use it (F1.4) |
| B. **Heartbeats out of git** (a TSV or KV on Amber, or one daily summary commit) | about 2.8k commits/month; deploy-build churn (#22); 37 commits a day from cio | the freeze-check reads git; it would need a local reader. Off-machine visibility is lost unless it's synced. | git is the one surface every agent and PM can read (website CLAUDE.md "human-first, agent-aware") |
| C. **Event-triggered wakes** (mail arrival, issue label, CI red) instead of 63 cron fires a day | quiet-fire cost (36k+ rules tokens each), quiet-hold false alarms (#7) | needs a dispatcher (GH webhook → Amber); risk of missing a wake. Keep a 1×/day START. | the cron catches work nobody signalled; PM: "otherwise it's dependent on me" (comms log citation, §5) |
| D. **Fewer standing roles + on-demand specialists**: keep lead, exec (digest/Ship), docs; make arch/cxo/ppm/cio/host/comms/web/pa invoked per issue | most of the 11 × 6 fires; roles with replies/memo < 0.3 (cio, host, ppm, docs, web, comms) | loses continuity, standing memory and the cross-role checking that caught #062's counts. Ship workstream reviews would need a new source (git/issue digest). | standing roles carry context across days; their reviews feed the public Ship |
| E. **Pull work from GitHub issues** (labels/assignees) instead of mail | most of the 1,141 memos/4 weeks; MANIFESTs; routing failures (#12, #16, #19) | GH auto-close and Projects hazards (CLAUDE.md:639–641); public-issue privacy | mail is the only guaranteed-delivery signal (CLAUDE.md "Mail vs GH comments") |
| F. **Mechanize prose rules**: e.g. a heartbeat writer that doesn't commit, a sign-off script, a mail cc linter | rules that "keep getting ignored" (CLAUDE.md:340ff) | more scripts to maintain (§3 proliferation) | the cohort already learned "structural fixes hold, promises don't" |
| G. **Cloud sessions** for some roles | Amber single-host fragility (#21, 09-20 reboot parked every role) | already being explored as an experiment (rollup 10-03 priority 3: "pick the cloud guinea pig") | Amber gives persistent state and stable worktree paths |

**Steelman of the current model**, with evidence:
- It keeps running without PM (§5).
- It produces a weekly public Ship with cross-verified numbers.
- Its cross-checking caught real product defects before they went public: the Inversion never serving a live turn, and the 43/34 vs 91/57 count error.
- It turns incidents into durable rules and tools quickly.

Against that, D0's H4 analysis found the mailbox and duty-cycle-tick introductions did **not** meet the pre-registered improvement rule (only 3 of 23 mechanisms did), and the model timeline is fully confounded with them (D0 §3–4).

## 8. Repo weight

| measure | value | source |
|---|---|---|
| Tracked files in `mailboxes/` | 21,312 = **59%** of 35,840 tracked files | `F-repo-weight.out` |
| `mailboxes/` working tree | 124 MB | `du` |
| `mailboxes/` history | 336 MB uncompressed, 31.7 MB packed (2.8% of the 1.12 GiB pack) | `F-repo-weight.out` |

Mailboxes cost little in pack size. The largest pack items are `docs/assets` (26%), `docs/public` (25%), `docs/comms` (11%), and a committed `venv/` (10%, appendix).

The cost is **file count**:
- every `grep -r`, glob and checkout touches 21k extra files;
- PM's inbox alone holds 3,441 files;
- MANIFEST regeneration is needed.

**Privacy:**
- The repo is **public** (live-probe: `gh api … .visibility` = public).
- Mailboxes contain 17 distinct non-noreply email addresses and named external people (`ted-nadeau/`, `z-dan-heck/`, Jake's FTUX drafts).
- `.mailbox-bearer-lint-baseline.txt` pins 40 historical credential-shaped hits.
- See also A-S6 and A-S13.

The fix is to move `mailboxes/` (and `dev/` logs) to a private repo or private store. Agents keep git semantics. That removes about 59% of tracked files from the public product repo.

| id | claim | layer | denominator | evidence | conf. | implication |
|---|---|---|---|---|---|---|
| F8.1 | Internal agent mail, with third-party names and emails, is published in a public repo. | live-probe + static | all 21,312 files (email regex) | above | high | Move it out; this composes with A-S6/A-S13. |

## 9. H1b verdict (pre-registered rules, applied literally)

- **M1b.1** (role-specific share of session-start load < 25%): **pending.** `spec-eval/D-measure-ruleset.md` didn't exist when this report was finished. Indicative figures, not the measurement: fixed shared files (CLAUDE.md + duty-cycle-tick) are about 143 KB against 21–93 KB of role files per role.
- **M1b.2** (≥ 3 overlapping PM-facing outputs, over ≥ 2 weeks):

  | reading | result |
  |---|---|
  | lenient (topic recurs anywhere in the other output) | **4 outputs in each week: met** |
  | strict (heading-to-heading) | **0: not met** |

  My primary reading is the lenient one, because "topic headings recur in the other" refers to topics, not wording. **Holds**, with medium confidence because the operationalization is mine.
- **M1b.3** (≥ 2 signals each watched by ≥ 2 mechanisms with no distinct failure mode): **does not hold.** 0 found, at most 1 (liveness, if Pard's crontab job duplicates the launchd watchdog; unverified).
- **Verdict:** one criterion holds, one fails, one is pending. **H1b is undetermined.** It becomes SUPPORTED only if D-measure finds a role-specific share under 25%; otherwise it's NOT SUPPORTED.
- The redundancy PM suspected is real in the PM-facing outputs, but not in the watchers. The heavier finding is volume: 82% PM-addressing, 5.8h/week, 708 unread. Watcher proliferation is a separate problem, more watchers rather than duplicate ones.

## Unobservables
| what | why | how to observe |
|---|---|---|
| Cowork scheduled jobs on PM's machine (U5) | not in repo | PM/Exec inventory |
| Pard's crontab freeze-watchdog and whether launchd `duty-cycle-watchdog` still runs | off-repo, host config | `crontab -l`, `launchctl list` on Amber |
| Whether the PreCompact hook fires (project settings register none) | user-level settings not in repo | inspect `~/.claude*/settings.json` on Amber |
| Dollar cost of subscriptions, Fly, Amber, Actions | no bills in repo | PM billing exports (PA's 09-22 note lists Console CSV / Claude Code analytics) |
| Whether PM reads the rollup/omnibus/current-state, and how long it takes | no read receipts | PM self-report or a click/open log on the HTML |
| Whether per-fire rules reloads are prompt-cached | harness internals | usage-audit.py cache-read vs cache-write split per fire |
| True stall vs compliant quiet hold for each alert | git can't separate them; heartbeats only exist since 07-28 | heartbeat log joined to alert times |
| Watcher catches after creation | outcome language in logs is inconsistent | an `outcome:` field on alerts and sweeps |

## Top findings for synthesis
1. **Coordination dominates output.** 62–90% of each standing role's commits are mail, log, heartbeat or stop (F1.1). cio alone wrote 1,026 heartbeat commits in 4 weeks (F1.2). Fix: take heartbeats out of git and move to event-triggered wakes (alternatives B, C).
2. **PM is over-addressed and doesn't read the mailbox.** 82% of 1,899 memos addressed PM, about 78k words (5.2h) a week, under 10% of it producing decisions, with 708 unread since 09-11 (F2.1, F1.4). Fix: the rollup becomes the single PM channel (A).
3. **H1b is undetermined.** M1b.2 holds under the lenient reading (4 overlapping outputs in each of 2 weeks; the omnibus and current-state contain everything else). M1b.3 fails: the watchers aren't duplicates. M1b.1 is pending D-measure (§9).
4. **The machinery causes more recorded incidents than it records catching.** At least 25 caused against about 4–6 identifiable catches. Several watchers have false-clear histories, and new watchers keep being added one per incident (§3, §4).
5. **The cohort runs at its subscription ceiling** (96% of the 7-day cap, week ending 10-02). Coordination therefore competes directly with product work for capacity. Dollar figures are unsourced (§6).
6. **Public-repo exposure.** 21,312 mailbox files (59% of tracked files), with third-party emails and names, sit in a public repo. Move them to private storage (F8.1).
7. **Bus factor.** The cohort survives PM's absence for about a week, with lower product throughput (n=1). The Ship and ceiling/pace decisions still block on PM, and a wedged seat still needs a human (§5).

## Appendix
- A committed `venv/` occupies about 114 MB of packed history (`F-repo-weight.out`).
- The size of the subagent fan-out on 09-14 differs between CLAUDE.md:413 (30) and usage-capture.sh:4 (48).
