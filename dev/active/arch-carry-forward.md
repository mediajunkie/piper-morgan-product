---
last_updated: 2026-10-23 21:40 PDT
currency_claim: rewritten at substantive-change boundaries, verified at every START
max_age_days: 4
---

# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff for the next Architect session — current state and active threads
only. Resolved history lives in the session log (`dev/YYYY/MM/DD/`) and `decisions.log`, not here —
per PM's 2026-06-12 ruling that the session log is the durable record, and the 2026-09-22
context-floor directive that duplicating it here is exactly the accretion to cut.

---

## Environment (stable; verify at START, don't re-derive)

| Fact | Value |
|---|---|
| Host / model | Amber, Model A worktree `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` |
| Model | **Opus 5.5 (`claude-opus-5-5`) since the 2026-09-28 ~14:35 cold restart** (Pard, PM-authorized, no `--resume`). Verified from the runtime model system-reminder, not the handoff's stated intent. ⚠️ `~/.claude/settings.json` and `~/.claude-pm/settings.json` BOTH still read `claude-sonnet-5`, so the Opus model comes from a launch-time override, not the settings default. A relaunch that drops the override would silently come back as Sonnet. Check the runtime reminder after any restart (rule 7). |
| Wake mechanism | ⚠️ **SESSION CRON RETIRED 2026-09-25, PERMANENTLY — do not re-arm.** External LaunchAgent (Pard), reading the registry's `cron_expr`. Registry-vs-plist mystery resolved 09-26 with a `pm-cadence` drift guard now in place — registry is trustworthy again. **Cadence: back to 6/day `27 6,9,12,15,18,21` as of 2026-09-28 21:27 STOP** (registry col 2 edited, threshold_h 9→7). Exec's 08:0x "revert Tuesday" ruling was RETRACTED 14:5x; final 15:1x memo: PM confirmed "Monday ok" = revert today. **CONFIRMED 2026-09-29: the 09:27 fire arrived** (off-schedule for the old 3/day expression), so the LaunchAgent reads the registry's col 2 live. The prompt's `cron=` constant was regenerated to `27 6,9,12,15,18,21` by 2026-09-30 15:27, so prompt and registry agree again. (It is documentation; the LaunchAgent reads col 2.) |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Deliver to Pard directly (DIRECTORY.md "deliver it yourself", default since 2026-09-27): write the file, stage it by exact path, push to `mediajunkie/mediajunkie` main, then verify it on origin. Done 10-12 for #1952. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

⚠️ **If you're reading this cold after a restart (no `--resume`), read
`dev/active/arch-handoff-pre-opus-5.5-restart-2026-09-25.md` FIRST for the reasoning/narrative** —
but **per Pard's explicit 09-25 ruling, treat that doc as base layer once it's >48h old, not a live
description**: this carry-forward + session logs + commits are the current state; the handoff's
job shrinks to orientation once it ages. **Don't try to keep the handoff itself fresh** — that was
named directly as the wrong instinct ("I would rather your handoff go stale than your seat idle").

- **10-23, closed at 21:4x** (alpha `5c654971e5`, healthy, promoted 19:3x; Tests green on `55ba453e76`; Code Quality green on `f99ad9e0cf`; full detail in the 10-23 log and decisions.log):
  - **MVP gate: the last must-close (#2132, with #2138) is CLOSED.** Invitations are xian's to time.
  - **#2151 (read claims), step 3, Lead's lane. Arch validates each landing from source plus Tests.**
    - **Validated:** the six from 18:xx, plus 8fee74485d/83ec7edff9 (local git on the hosted signal; served PASS), CAL-SWALLOW ×3 and ACTIVITY-READ-FAILED. KNOWN_RED is 19; UNREGISTERED_KNOWN is 9.
    - **f57a31faf8 FLOOR-ABSENT, open-issues gather: gather half OK, read half OPEN.** The ruling (21:28) for all seven gathers: strict read underneath (through the connector resolver); a pin at the bottom layer; CONNECT_REQUIRED = not performed; `_github_repo_resolves` three-state. **Lead does the other six gathers plus GH-NONSTRICT on 10-24. Read each diff for these four points.**
    - Still to come: the trust flag; the tag fold; the `is_configured` bool readers; the MCP colleague-model red row; the no_credential → not-connected follow-up; the step-4 prompt rule (needs a priced screen).
  - **#2137: CLOSED** (21:3x) on Web's served PAT-only row. CXO's caveat: the binding table wasn't read.
  - **Still open from 10-22's rulings:** #2139 (doc from the conversation: the handler string rides with the handler fix; routing is a catalog screen) and #2135 (trust stage; dormant, tripwire landed). #2085 and #2146 are CLOSED.
  - **#2146 (restarter):** stop24 is armed until about 15:47 PT Saturday 10-24. Guard 2 counts only bot-triggered prior restarts.
  - **Map review:** round 2 answered (21:33): C2, C5, F28, F29, and F8a's staging requirements. **xian reads the list Saturday**, and Exec merges it into the round-3 brief. **F28 waits on PA:** does any live install run the POC skills? Exec routes the question.
  - **The Haiku 5.5 router/classifier screen** (rule 7, same batch, about $4) waits for 11-01, or for a separate cap from xian through Exec. It is screened before #2149.
  - **Own misses 10-23:**
    - guessed "10:4x" and "18:1x" stamps (fixed before anyone acted);
    - "classifier cache not active" (wrong: live from 11:05; corrected);
    - two memos sent without their cc copy or sent mirror (cc added the same turn);
    - a filename over the 180-character cap (mail-send refused it).
- **10-20** (alpha serves 0.8.14.0, `d1c64a92e3` at 17:37; Tests success `edf95b5c0c`, Code Quality success `6c6e205660`; full detail in the 10-20 log and decisions.log):
  - **#2101 (alpha stalls):** the cause was the synchronous Anthropic call on the event loop. `to_thread` stays (no AsyncAnthropic per request). Three conditions built in `cb11e68eac` and validated: timeouts, the dedicated `llm-provider` executor, the AST pin. Closing run: 61 of 61 turns, 0 blocks. Close is Lead's; condition 2 under concurrency gets its first read from partner traffic.
  - **Shadows:** paused on alpha (xian unset both, 12:07). #2109 (`49b30d987b`) validated. Re-enable conditions (decisions.log): an Arch ruling naming the consumer; #2109 live; sample ≤0.1; a `PIPER_SHADOW_LLM_KEY` from a workspace xian names.
  - **#2112 (calendar asks answered with the date):** ruled no grammar change; the router's NONE stands on a live category (`3b7fbb46fb`, validated). Behaviour accepted on served quotes; PA's reproduction released. The floor's calendar fact `1fb8e14757` was validated; my reads-line fix was accepted by CXO. **Open: the connected-account row only (xian's calendar account, via Exec).** A fixed reply is pre-authorised by CXO if a promise of conflict checks returns.
  - **#2113:** #1730 Gap-2 ratchet upheld (ask only when armed); the imperative serves; the question form needs a pending-action carrier, Lead's unit.
  - **#2121 / #2123:** the activity read now goes through `resolve_credential`; a missing credential is `read_failed`. **Ruled #2123:** with a principal present, a GitHub read uses that principal's credential, never a system session. Fix `dedbe6e3ad` validated (Tests `9e7bd077af`). Not live until the next promotion. Alpha has no env GitHub token (PA). The "system" keychain row is unread (DB), inferred absent from a public-repo None at 16:48. **Open: CXO's served cross-account row (needs a second GitHub account with a private repo).**
  - **10-19 waits resolved:** #2091, the #2098 rework, the #2101 surface all landed and were validated.
  - **Own misses 10-20:** wrote "alpha's capped platform key" (alpha has none; it was the test workspace's cap). Proposed an INFO-level stream grep as a confirmation (alpha emits no INFO). Guessed a memo date ahead of the clock (mail-send refused it). zsh doesn't word-split an unquoted `$P`; use `${=P}`.
  - **Watches:** the next promotion (#2123, the reads-line fix); CXO served acceptance of #2094/#2095/#2096/#2100/#2098; #2100's three Notion handler strings (Lead and CXO); #1386 criterion 2 (PPM and Lead); #2092 (xian via Exec); #2079 (Web).
- **10-19** (alpha `e801b1a309`, main green on Tests `5e17e627a2`; full detail in the 10-19 log and decisions.log):
  - **Ruled today:** #2083 deviation accepted; binder ratchet (#1943, per-file shrink-only ceilings, 298 in 24 files, `00db028cfa`); #2091 (day as a router `when` arg, code resolves it, the label names the date); #2094 (router titles list); #2095 (ADR-078 D1 amended: the ledger records every create); #2096 (census 30, PM-005 store, JSON body); #2100 (CHAT_READS); #2101 (async KeychainService via `to_thread` plus an AST ratchet; the read cache made process-wide).
  - **Validated:** #2094, #2095 (pin tightened `fc17eab244`), #2096, #2100 (`8e9963aa2c`), the cache `2acf8af82d`, the ratchet, the radar fixture fix `f9ddb2ba88`. **Rejected:** #2098 (its marker binder rewrote a title from "call it out in the release notes"); reverted `f260d8ed5b`.
  - **Practice since 10-19:** validate against the Tests run on the landing's sha, not only its own pins (my 10:10 #2083 sign-off was on an already-red sha).
  - **Waiting on Lead's builds (validate on landing):** #2091 (its commit must also update CHAT_READS' Calendar entry); the #2098 rework via `classify_armed_reply(answering_operations={"update_issue"})`; the #2101 `to_thread` surface with a per-name generation counter, the one-process docstring note, the AST ratchet and a concurrency pin.
  - **Waiting on others:** CXO's served acceptance of #2094/#2095/#2096/#2100 and the honest-stem prompt line after Tuesday's promotion; #2101's close on Web/PA's load re-measure; #2092 on xian's calendar answer; #2079 is Web's.
- **10-16** (normal pacing; alpha promoted 07:49 to 6bb955919d; promotion grant in force, Lead dispatches):
  - **Promotion, as of the 12:27 fire:** alpha still serves 6bb955919d (/health). 10:51 dispatch refused by the gate (staging ran a red sha; CIO: a refusal is not a promotion). xian said yes to a third today; the 11:33 dispatch passed every gate and failed on Fly's partial outage (API 500). Lead retries when Fly is operational, before 21:00, else tomorrow. The waiting build carries #2057, the #2048 guard and #2054. #2024 is in 6bb955919d, awaiting CXO's served read.
  - **Closed by CXO on served reads:** #2008, #2044, #2039, #2033, #2035, #2040, #2037, #2012, #2029. #2052 closed as not a defect (GitHub search lag). The 10-15 served-read watches are done, except #2031's no-token card (S5 with xian).
  - **Ruled today** (all in decisions.log):
    - **#2041:** one question per composed turn, precedence pause > write offer > hint. A READ sibling's write offer is carried. Landed 051a06dd55, validated.
    - **#2047:** registry-only canonicals describe and exemplify only what no other op serves; move the 'List my projects' example off manage_portfolio. Lead ships it as one rule-7 batch.
    - **#2048:** route by registry disposition (dbc15b3b7d). D4 guard: an adopted category runs reads only (3adefb2d57 + 70e2fddb23, validated 09:27).
    - **#2054** (filed by me): IntentCache shared one mutable context dict across hits, a cross-user principal path. Deep-copy fix 88dada46f8, validated. PPM asks xian to admit it as MVP Class 2.
    - **#2057:** a how-to question wrote through surface 1 (pre-existing, live). Two parts: legacy writes go through rail consent, and a question never writes in either mode (FRAMING_QUESTION). Lead lane building; gated through #1595.
    - **Promotion hold** (mine, 08:43) lifts on the #2048 guard plus Tests green; #2057 follows a build later.
    - **ADR-075 OQ-3 amended:** the notice goes on the next greeting or help reply, never under a list (#2055, Lead).
  - **Evening state (21:27 fire, written 21:28):** alpha promoted 17:09 to d741214b6c (#2054, #2059, #2060, #2061 live, all closed). MVP gate 8 (PPM); must-close set #2064, #2065, #2071. Validated on main, waiting on tomorrow's first promotion: #2064 (176d66a53c + f7e5a4ca45: pre-flight, refresh refuses missing user, 30-min recount; close = live + xian's count), #2071 (a589e907d2, per-principal Test result; close = live + Web two-account served). #2069 in Lead's Opus lane on my ruling (router args; reply from stored row) plus a 21:28 condition: the consent line names the target from the handler's own source. Validate #2069 on landing.
  - **Own misses 10-16:** guessed 'xx:Nx' stamps in two GitHub texts (fixed; memory updated). My #2048 'nothing written before' claim was wrong for surface-1 phrasings (corrected on #2057). I traced only the orchestrator path for #2035/#2041, which caused the #2041 regression.
  - **Watches:**
    - Lead: the #2057 lane (validate on landing), #2055, #2056 (context_assembler cache check), the #2047 batch, #2023, #2021, #2051;
    - xian: #2054 admission and a lone promotion;
    - PM: #1028.
- **10-15** (RUN-HOT until 22:00 tonight):
  - **#1771 standup exits, ruled and largely landed** (Lead e08a9bcd50 → 022dc3074c → f76a307ecb; ADR-049 #1771 amendment written):
    - The #888 hatch splits END {cancel, quit, exit} / PAUSE {stop, never mind}, and `skip` is not an escape word.
    - An unstarted standup (INITIATED) closes rather than suspends; the handler supplies copy only.
    - At the invitation, only `is_bare_decline` plus DEFER leave, and the quick bypass is whole-message.
    - **Open (Lead):** "please" stripped at the hatch; "skip <flow name>" as a flow-specific #1529 exit; the `contains_deferral` helper (decisions.log 10:24).
  - **#2010 census offer_hint signal** validated (46899c547f). **#2024** filed (offer = one yes/no question; directive arms dropped; CXO copy in). Lead builds.
  - **#2019 cap** validated in source (bf03ac3ab2). Bare "later" at the resume offer is a KNOWN MISS (safety pin only; revisit on CXO's served read with a whole-message entry).
  - **#2027** (dead standup suggestion lists): all 17 deleted (f76a307ecb); CXO closes on the served read. My #2028 was a duplicate, closed.
  - **Thanks/farewell compound registry examples:** NOT moot after #1986 (the examples are compound, the op is pure-only), but hygiene. They ride the next catalog batch's rule-7 run; no standalone run.
  - **Afternoon/evening rulings** (all in decisions.log 15:45–17:27, stamps corrected to commit times):
    - #2024 validated; **#2030** composed turn = one question, armed, asked last; **#2041** write offer outranks hint.
    - **#2035 rule:** an offer whose yes leads to a WRITE arms the #846 store with its own landing, never the #852 hint. CXO shape B. The #1977 replay is outside the rule.
    - **#2031:** the card derives from resolve_credential (B4). Landed; `github_oauth_bound` gone from integrations.py.
    - **#2037:** stale detection must be a response field, not a copy substring. Lead's flag is owed; #2037 doesn't close on the substring.
    - **#2033** (the floor narrated "standup cancelled"): fixed line from code ahead of the floor. **#2040:** "whole list" only on a recorded one-turn ListComplete fact.
    - **#2042 class:** track, gate instances. Ladder: code-first answers; a log-only `#N` unsourced-reference metric; floor eval rows.
  - **Own misses 10-15:** the #2028 duplicate; "11 entry points" (by-name grep, real 21); timestamps drifted all day (fixed 18:28; memory updated).
  - **Watches** (normal pacing from Fri 10-16):
    - xian's promotion word (alpha still 6f2916d10f), then the served reads for #2010/#2035 S3, #2030/#2041, #2037, #2031, #2040, #2033, #2008 and the #1783 close;
    - Lead: #2023 (now also covers the standup INITIATED stage), #2021, the #2037 flag, the #2042 metric if PPM places it;
    - xian: #2040 MVP admission; PM: #1028.
- **10-14** (history rewrite overnight; RUN-HOT window until Thu 10-15 22:00):
  - **Option 3 = none.** STANDING CONDITION: no referent-dependent write (update_issue) enters FLIP_WRITE_ALLOWLIST until the live consult stands down on a Stage-0 referent.
  - **Acceptance contract landed** (#1843 CLOSED by CXO on served; #1771/#2007, #1783 await served reads). #1783's cap is GitHub lists only (needs a GitHub account with >5 issues); #1771's resume check needs `stop` as the leave word until #2023 lands.
  - **Bulk delete (xian approved PPM's rec, 21:0x):** clear_todos flip HELD (#1943 branch 6fd438bba0 stays held); **#2019** caps N>1 delete in the delete handler (all entry paths), Lead builds 10-15; **#2021** soft delete, 7-day window then purge, built to MY DESIGN NOTE `docs/internal/architecture/design-records/design-note-todo-soft-delete-undo-2026-10-14.md` (exit criteria lift #2019; first instance of #336). "clear" ASKS (D4); CXO conceded.
  - **#2009 chain (Lead, held behind the promotion):** prod counts in (tier A 0; project_integrations 3/3 → same-migration backfill). #2013 (KG owner threading; the KG POST routes were failing outright, not orphaning; my earlier read corrected) and #2014 (items CHECK per discriminator + FK ON DELETE SET NULL; delete_list removes base items; validated ca51b60756) (xian's prod counts were DONE 10-14 20:56: 0 and 0, on #2014; I'd carried this as owed until 10-15 11:2x). #2015/#2016 are Lead's.
  - **#2012 validated** (54989e1ce5): Test derives from resolve_credential, both legs. Served per-leg check is CXO's after promotion.
  - **#2023 RULED:** mid-process reply judged by the LLM against the held question (ANSWER/REQUEST/UNSURE), not the router, not a pattern; corpus rows before build. Watch Lead's build.
  - **#2011 census** held at 94310057c7 (16 holders). ANALYSIS margin fix held. Both ride the next promotion.
  - Standing member "let's analyze the risk here" TRIPPED 5/6 on main: the ANALYSIS margin fix precedes every catalog candidate after (c).
  - **Watches:** PM's promotion → CXO/Web served reads (#1771, #1783, #2012 per leg, #1987); #2023 build; #2021 build after #2019.
- **10-13**:
  - **Role card** at the top of the briefing (`144578829f`); the session-start hook prints it. Each day's first fire writes a Drift: line (tick v1.51).
  - **Rule 7, perturbation-sensitive ledger** (decisions.log 07:4x). The meeting licence row was stabilized by `d13dafd172` (accepted). **Watch:** main's own ×6 on the standing member "let's analyze the risk here". If it reads below 6/6, the ANALYSIS margin fix goes ahead of the next catalog candidate (Lead reports it).
  - **#1987 both halves landed; my condition is met** (pins `a9f8cd16d1`). **Watch:** the served check (AC 3) after the next promotion, which is PM's hand.
  - **ADR-070 Amendment B** (`cf0615061a`): one credential resolver per connector. Answers Agent 360 candidate 7(3) (no PDR); candidate 4 agreed.
  - **FILE_REFERENCE_PATTERNS: ruled inert and removable (`4905a9d746`); Lead DELETED them (`eb9eb41b2e`, validated).** Ceiling 120 → 90. Wednesday's number is 29 floor + 61 router-quality.
  - **adr-index.md is GENERATED: never hand-edit it.** Edit the ADR's Status line and run `derive-adr-index.py`. It is registered in `check-derived-drift.sh` (`0718489509`).
  - **Legacy-classifier retirement check (due 09-30) was missed; stated 10-13: not met.** Re-check trigger: the #1595 Phase 3 tail reaches the ruled floor.
  - CIO role-duty rows answered (8/8); CIO re-runs the count on 10-27.
- **10-12 (morning)**:
  - **#1984 half 2 CLOSED for Arch as a KNOWN MISS (option c).** Option (a), the trade, was refused because its improvements were unattributed. The (b) screen failed on 2 rows. The corpus row is ledgered with expected=plan. #1984 stays OPEN, and the retitle is CXO's.
  - **STANDING:** "let's analyze the risk here" (yaml:1973) is in every catalog-candidate ×6 screen.
  - The compound thanks/farewell registry EXAMPLES ride the next catalog batch (trigger: that batch).
  - **#1986 LANDED** (`8ebe568035`, then `cd43832626`, then the belt `d23849fb9f`, all verified in source). This **reverses #1754 for thanks/farewell**. The empty thanks form needs a durable zero AND an empty in-memory window; anything unknown serves "You're welcome."
  - ~~Watch: Web's served set~~ → **DONE 10-12 pm**: Web ran 12 turns on alpha 651756d520 and CXO closed #1985/#1986 on the quotes.
- **10-12 (afternoon/evening)**:
  - **Turn 2 ruled:** a canned reply counts as a delivered turn, kept as built (concur with CXO).
  - **Turn 9 ruled:** the no-number "Which todo should I remove?" ask arms nothing, so condition 3 holds and `_armed_offer_signal` is not widened.
  - **#2000 CLOSED** (`166d876f4f`): the census predicate now sees a mid-line `?`.
  - **#1987 half 1 accepted** (`5fd92b0019`): the just-created referent, gated by a confirm. Bounds and the retirement trigger are in decisions.log 19:1x.
  - **Watch:** #1987 half 2 (numbered pick), Lead's next START. It MUST arm via the #846 store (the #1906 shape) and be pinned both ways against the thanks short-circuit. The condition is written on the census row (test_architecture_enforcement.py ~4302).
  - **PR #1952 MERGED** (`8c3c56c0d6`) by Lead after my review comment. The first live gate run read fresh (run 38331164368). Lead keeps reading later deploys for a stale pick.
  - **Merges:** I can't approve-and-merge a PR on the mediajunkie account (refused as a self-approval). Review as a comment and hand the merge to the owning seat (memory `feedback_pr_review_and_merge_by_a_separate_seat`).
  - **#1993 filed** (test-order leak, 47 rows; reproduce first).
- **SPRINT GOAL (PM-locked 10-03, week ending Thu 10-08)**: finish epic 0 Phase 3 deletions for every live-wave list. Lead owns it. Arch's part is **same-fire
  ruling turnaround**. Quota is expected to run out around Wed 14:10, so plan for 4 days. **Both upstream gates were ALREADY CLEARED when I named them**: read_floor went live ~09:5x 10-03 (PM flip, TRUST 15/15 after descriptions) and #1920 CLOSED 10-02.
  DISCOVERY/TRUST/MEMORY/ANALYSIS read GO (partial) and are the week's first lanes. Lead is restarting onto Opus 5.5.
- **10-09**: Phase 3 scope = routing tail 125 (recount), ceiling 155. **Lead's 56-literal batch FAILED 95 unit tests and was REVERTED (11:17); the tail is still 155. #1969 filed. Standing rule 10 written** (a zero-row partial is held; a full tests/unit run before any landing; a failing test becomes a corpus row). **#1969 CLOSED 12:50 (`ca5eebb8d7`): the gate enforces rule 10 (NO-GO for held zero-row literals, verified in source); the 7 landed partials are clean; MVP gate 15→14.** Lead drafted 47 rows for the held literals; **Arch ruled the 3 project-delete literals (corrected from 5, b94c03443) are survivors until #1935** (62a73340b); PPM ruled the expectations. **Rows landed `41da0296a2` (corpus 563; 27 literals licensed; ceiling ~128 if the deletion lane is green).** Ruled `framing: declarative` (asserted NOT-EXECUTE); **#1970** (framing to the router; step 1 plumbing on main, flag off; **router framing DEFERRED 10-10 (option c: the router errs toward acting)**; ratchet with justified bump; retry trigger in ADR-080). **Deletion lane LANDED 15:4x: 26 deleted under rule 10, ceiling 155→129 (Arch re-ran pattern_literal_counts: 129/36 lists), routing tail 125→99.** 129 is above PM's 110–120 band; PPM decides which number the 10-14 check reads. The remainder needs router/catalog work (load-bearing survivors, 11 clear-family rows, #1935). Not on alpha until the next promotion. **Main Tests went red from the IDENTITY deletion (7 pins outside tests/unit); Lead fixed it in `95c8a9286d`; rule 10 amended to CI full tier; main Tests GREEN on `75a8eb0232` (Arch verified via gh); promotion is PM's hand. **#1973 LANDED (2ae31d1673): 9 rows → 5 router N=5 + 4 surface-2 N=5, no restores; GUIDANCE emptied. Ceiling 121 (Arch verified), routing tail 91. The gate reads no list GO; the remainder needs rows or router/catalog work.** **Scoring back by 18:28 10-10** (Lead ran a fresh full run); 8 masked rows → 6 restores + 2 surface-2; ceiling 121→127 landing; **freshness rule adopted**. **Post-reboot: api.github.com hangs in the macOS resolver (known fault, Pard); use `GODEBUG=netdns=go gh` until xian runs the mDNSResponder HUP.** Earlier: SCORING OUTAGE 10-10 10:0x (Lead's Anthropic workspace capped until 11-01; OpenAI 0 credits): catalog changes and deletions frozen until PM picks (a) raise, (b) other key (must be the served model), or (c) wait. Rule 7 spend shape added. **ALPHA PROMOTED 18:34 to `4bd1a236e9`** (code = f0ac5db8d0, Tests green): Phase 3 deletions through #1973 are live. Watch: Lead's served checks on the test account (blocked on a credential-file permission question) and PM's test card. (Earlier: chunk 8 landed, ceiling 124. #1971 ruled → standing rule 11 (reabsorption before GO; #1256 literal blocked on DOCUMENT_QUERY). Rule-11 sweep: GUIDANCE held on rule 10 (#1972 was a misread, closed; my rule-6 ruling WITHDRAWN 19:5x), COMPLETION_HISTORY held on #1973 (threshold in every arm; 9 past rows → N=5 router, else surface-2 rule 3, else restore; one commit).** re-measure Mon 10-12 against the 10-14 tripwire. #1960 copy landed; CXO closes it from the alpha served reply. **Promotion gate SATISFIED** (Exec read 13/13 tokens 10:12). Prod-exec boundary: **CIO's option 3** (rule names the fly command, no shell, payload self-validates; my option 1 was circular)
  matcher probed twice by CIO; **final allow+deny lines approved for xian** (residual = target-only misdirection, named). Ship #064 review filed. **Watch for**: the batch commit names its 13 tokens (and gate constant to 13); xian's yes on the fly-form lines; the mint grant swapped to fly form. **prod_user_lookup.py APPROVED by Arch (11:2x)**, with nits (fullmatch; lift the DB helpers). HOST APPROVED too (--all ok, with conditions). **Arch's approval is conditional on the remote no-shell probe** (`-C "echo a; echo SHELL_RAN"`, no deploy needed). **The burn split and both nits are DONE (`9e1fa372cb`, verified in source)**; mint_mcp_token self-validates. **The probe is CLEAN** (HOST 11:58, on xian's go), so Arch's approval is unconditional. HOST file = (A) ask plus deny (2acfa33a3); CIO and Pard assemble it for Janus and xian. **Rule install HELD until the probe (ed131a34a)**; HOST had said install-now. Mode question: doc facts sent to CIO (a06df5251); recommended ask: Bash(fly *) with HOST staying on auto; CIO answers xian. Watch: the probe result, the burn split, mint_mcp_token in the same pass, deploy, xian's lines.
- **10-08**: clear family landed (`a53d3458a5`, clear_todos not live, PM token). #1886 landed and **verified in code** against the corrected rule. **#1965 (a)+(b) LANDED and verified in code** (one resolver, two legs; env token impossible for real users). **Watch for**: #1966 (status from resolver), alpha served checks (OAuth-only + PAT-only accounts) closing #1889/#1963, and the next catalog-change full run (week_calendar clause + PPM batch).
  **Mail convention**: add `reply-to: piper-morgan-product:mailboxes/arch/inbox/` to every memo.
- **10-07**: #1886 ruled and **corrected** (only the answering set binds; CLARIFY/low/error confirms; Lead landing `71693dd849`). clear_todos landing points ruled (marker, not blanking; a per-carrier answer set; the transition guard has a named retirement). The destructive condition was restated for the args path (ids shown == ids changed).
  E2E red = empty CI key, now #1956 (reshape to manual/local, Exec routed). **Watch for**: #1886 on alpha (served-answer probe), the clear_todos landing after the full-corpus run (PM's cost ruling), and CXO's source check of #1886.
- **10-06 (a) progress**: complete_todo steps 1–5 DONE (served answer right in-process). Step 6 (retire the single-ordinal binder) next. **clear_todos ruled as a resolver entry** (re-enters the rail as
  complete_todo/delete_todo). **Standing rule: any catalog change triggers a full-corpus re-score.** Watch for: CXO's clear-family strings, the clear_todos build (does it re-enter the rail rather than calling handlers?), and (DONE: alpha `99289b6690` promoted 10-07 with complete_todo live; "first three" served on the test account, Lead 16:28, REST-verified).
- **10-05 21:4x rulings**: #1832 GO. #1925 latency is report-not-assert plus a hang ceiling. #1522: persistence delete (table drop needs a stated row count and a reversible schema), Places/Docs removal pending CXO,
  dual-write retire plus the dormant `get_github_repository` fallback. **Lead opens the (a) args-flip plan at the next START.** Watch for: review of that plan (enumerating confirm, served-answer probe).
- **⭐ DIRECTION 10-05 — PM CONFIRMED 10-06; ADR-080 ACCEPTED** (all 3 surfaces drafted and reviewed 10-06; routing-stack awaits **Lead's sign-off** only; provenance rule added; diagram render passes): 'LLM decides meaning; code decides permission.' Doc: `docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-2026-10-05.md`.
  Next: one Intent shape plus served-answer 'ready' probes, then the args flip for complete_todo and the clear family, then other writes, then a ratchet on floor-internal regexes. **Watch for**: PM's answer,
  Lead's args-flip build (review: does the confirm enumerate? is the live probe asserting the served answer?), and #1947 fixed rather than frozen.
- **#1458 RESCOPED 10-05** (gates the first MCP directory submission): PA subagent builds, **arch reviews behaviourally** (read the two-token interleaved test output). **CLOSED 10-05 by PA** (pin + N=2; MCP v10).
- **10-05**: read_portfolio RELEASED (the live list_repos probe passed: route=inversion, reply from the list handler, not portfolio_help). **PM said YES** to deploying main, then flipping all three tokens.
  **Watch for**: the deploy plus flip landing, then Lead's re-score and deletion lanes on the live flag. CXO's open probe ('repos on github' → project 'github') is a corpus/gate fix, not a regex.
- **10-04 21:3x**: rail-owns-rail-keys AMENDED to (a), split predicate (claims_category for the orchestrator), plus **adapter parity landing WITH it** (per-adapter parity pins).
  (b) rail-per-sibling is a follow-up using the 09-26 sequencing. read_portfolio stays held until (a) + parity + the live list_repos probe. **Watch for**: Lead's unpark report, then tell Exec to release.
  **Standing self-check from 10-04's three misses**: before ruling on a gate or predicate change, grep EVERY caller and read the fallback.
- **10-04 18:5x — THE RAIL OWNS RAIL KEYS** (standing): can_handle must decline every rail key. **read_portfolio token HELD** (via Exec) until the fix plus a live probe of list_repos.
  **Watch for**: Lead's fix and pins, and the routing-stack doc update. Applies to every future PORTFOLIO/canonical-category token.
- **10-04 15:5x**: #1926 is closed via the unlink claim re-point (with a surface-2 residual probe). Coverage is corpus-driven. **Pard's health-gate patch is INERT**: watch that it's wired
  and proven by a forced-red run before it's applied. #1933 landed clean (0/100).
- **10-04 12:5x**: list_projects reuses the live entry, and search_projects joins read_portfolio (re-gate before PM's flip). Edit literals STAY (my miss reversed). #1933 effect-aware deletion
  endorsed. **Watch for**: #1933's re-verification of the 4 ledgered misserved rows (any fail means the literal is restored), and the complete_todo + portfolio part 2 builds.
- **10-04 rulings**: complete_todo goes ahead under the execute-vocab coverage test (with the 'clear' shared predicate). manage_portfolio split ruled, with delete waiting on #1930. FILE_REFERENCE is out of Phase 3.
  Tokens read_floor_2 / read_canonical / read_portfolio are with PM via Exec (deploy first). **Watch for**: the coverage test landing, and the #1930 ruling (which reopens delete's shape).
- **Phase 3 rail shapes RULED 10-03 18:5x**: one entry per effect class. Wave 2 approved. manage_repos → list/link/unlink. Canonical reads get adapters. manage_portfolio
  (inventory ruled 10-04). Ceiling 155. **Watch for**: the unlink build meeting CXO's 5 constraints, and stakeholder_update's persistence check.
- **Mail routing changed 10-03**: never cc or address PM. PM items go to Exec, with the type named in the subject.
- **read_floor LIVE 10-03 ~09:5x** (PM flipped it). Gate is GO (partial) for its 4 lists. Watch the deletions only.
- **#1606 CLOSED 10-02 (v163)**, built to my 5 conditions (plus verbatim `text`). **Gate (d) GO 10-02** with the served model printed and N=5. PRIORITY/GUIDANCE/STATUS
  deletions are Lead's today. **#1899 write erosion**: shape ruled (cross-family write release plus an explicit exit, both carriers). **Watch for**: CXO's product call,
  and Lead not shipping (a).
- **MCP read-only tool (2026-10-01)**: PM approved it via PA (ChatGPT is tools-only). I concurred with 4 conditions (compose the resource handlers, an allowlist
  test, no LLM, amend PDR-006:276). **Watch for**: Lead's build. Re-review if it re-implements reads or adds an unallowlisted tool. MCP v8 is live (Host-header fix).
- **MCP Phase C / OAuth AS — LANDED, REVIEWED, APPROVED (09-26, `645ce6412d`, alpha v146 / MCP
  v6).** My identity-binding condition verified directly in the shipped code
  (`services/mcp/server/oauth_provider.py:228`'s `_refuse_code`) and its real, non-vacuous test
  (`tests/unit/services/mcp/server/test_oauth_as_unit4.py:584`) — not taken on Lead's description.
  **Program is fully PA's now; nothing owed by arch** unless PA/Lead surface something new. The
  one still-unexercised thing (a real external client, ChatGPT, hasn't done a live token exchange
  yet) is PA's first-contact check, not mine.
- **#1595 Phase 3 — TEMPORAL DELETED 2026-10-01 (`dfec3e908d`) per my ruling** (rail entry in place, rows sorted). The gate false-live fix
  was verified in code (`68bd65b5bb`). CALENDAR deleted too (ceiling now 440). Keyless: **no zero-LLM path** (#1818(b) extended). The Slack missing-#1807-gate
  finding is recorded on #1481. Nothing owed by arch.
- **#1595 (Inversion Phase 2, epic 0) — unit 4 LANDED 09-26 (`3d8168b1e1`); #1897 filed for unit
  4b, grammar shape ruled, not urgent.** Unit 4's shape (ii) + confirm-pause sequencing both landed
  clean, no second dispatch site, MAX_DISPATCH_SITES 0→0. **Real finding, not a defect**: surface
  1's splitter structurally can never emit a read+write sibling pair (every pattern group is a read
  lane; the destructive guards decline write-shaped asks at surface 1) — so unit 4's rail loop is
  correctly built but #1606 still can't reach it, because the split itself never happens. Fix is
  #1897/unit 4b: the router gains a new `outcome="plan"` + `operations: List[...]` field, strictly
  additive, never touching the existing single-op contract — shaped 09-26, ruled NOT urgent (Lead's
  own framing: "rides the next alpha release," agreed rather than overridden). One real risk named:
  the prompt change ("or return a plan") could regress single-op accuracy — recommend measuring
  before shipping, same discipline as this week's #1772. **Nothing further owed unless/until
  someone builds 4b.**
- **LLM gateway question (PM/Themis, via Exec) — ANSWERED + CLOSED 2026-09-28.** Investigated
  directly: a single gateway (`services/llm/clients.py`'s `LLMClient`) already exists — 11 real
  call sites (not the 113-files-referencing number), all constructor-injected, fallback/logging/
  spend already centralized. Only gap: prompt caching (Pard's finding, already routed to Lead;
  belongs inside the existing gateway, one change). No formal architecture review needed. Wrote
  `docs/internal/architecture/current/design-record-llm-client-single-gateway-2026-09-28.md` so
  the question doesn't need re-investigating next time. Replied directly to Themis
  (`designinproduct/docs/mail/`, per Exec's own routing expectation). **Nothing further owed.**
- **#1899 (Phase 3 first deletion, armed-carrier discriminator erosion) — CONCURRED, scope
  confirmed 2026-09-27.** CXO ruled the mechanism (reads-only release: consult router, release
  only on high-confidence READ verdict). Closed CXO's own honestly-flagged denominator gap — CXO
  checked only `todo_handlers.py`'s site (#1654); verified `first_contact.py`'s FTUX carrier
  (#1688) is structurally identical (its own comment says so) and the fix generalizes cleanly to
  both. `intent-routing-stack.md`'s five-consumer inventory already correct, nothing to fix.
  **Nothing further owed unless Lead's build surfaces something new.** Deploy hold is PM's, not
  architecture's to lift.
- **m-55 (A Name Is Not a Definition) — FILED 2026-09-25**, Emerging, CIO-ruled. Two same-author
  instances (#1818, #1744), explicitly 0-cross-author. Watch for a second author hitting the same
  shape — that's the Proven-bar signal, not mine to manufacture.
- **#1772 — mechanism + copy rulings both LANDED 2026-09-25 (`35854f46ec`/`422d32f1db`).** Nothing
  owed by arch. Remaining half (measuring CXO's exact new string, ~20 completions) is Lead's ask to
  PM for budget — watch the issue for the number, no ruling pending on my side.
- **Deployment pipeline — plan v0.4 §4f ruled 2026-09-29.** Droplet decommissioned + `origin/production` retired
  (PM via Lead). §4f: alpha = promotion of staging's image (never rebuild); two per-app tokens, alpha's behind a
  reviewer-gated GH environment; staging Redis gates the promotion gate. Staging tooling deleted by Lead; ADR-007
  Superseded. Pard built `fly-deploy.yml` (`a0f1722827`). I reviewed it and 4 fixes landed in `c3579d3049`, re-reviewed 18:3x (all correct, pin
  verified). Pard also closed the torn-read race (`cb23b21afd`, ref→sha→ref2 guard). One mid-rollout window is named as unverified
  (if Fly's ImageRef flips before the machine swaps, the fix is a sha LABEL on the image). **Signed off, unproven until it runs.** Pard declined the mid-rollout fix (hypothetical) and named it in the failure text (`e540bbee42`); I concur.
  **10-01: §4e LIVE**: the staging token was minted and staging auto-deploys (it read `1d970ff436`, a log commit). Trigger ruled 10-01: `paths-ignore` mirrors
  `.dockerignore` (NOT docs/, which is read at runtime). My burst estimate and the sha==tip proxy are retracted. **#1849 CLOSED (verified 10-02).** Watch for: Pard applying the trigger rule, and the alpha env/secret setup before the first promotion.
  closes). Trigger-churn revisit: 1 week after the staging token exists. Lead hand-deploys alpha until (c) is real.
- **#1744 — CLOSED (re-verified via `gh issue view` 2026-09-25, no longer carried as open).** Per
  this morning's kickoff memo: closed end-to-end this week, ruleset bot-delivery proven. The
  "real remaining step" this file used to carry (re-run the scope-guard Action's own delivery test)
  is done — clearing it rather than letting a resolved item sit here past its own resolution.
- **Q5 denominator** — PM ruled idle-is-legitimate (09-18); the enumeration (role-scoped vs. flat
  three-surface test) is still open. My recommendation on record: adopt the flat test.
- **Bets 001–003** — all three `PM TO FILL` markers still present as of 09-21 evening. PM's own
  "this weekend" window passed; not re-nudging, just tracking.

## Standing hard rules (load-bearing; full incident detail in decisions.log if ever needed)

1. Never glob the inbox — read-then-append-to-move-list in the same call; verify drains at trunk.
2. State the scope IN the ruling — name the object, a non-covered adjacent thing, the clauses.
3. Verify the claim before ratifying, always — a check run five minutes ago isn't a check run now.
4. A `grep` line-hit is a pointer, not a quote — a claim about what N sites DO requires opening N
   sites, including the branch below the cited line.
5. A denominator that doesn't travel with its number isn't a denominator.
6. Before claiming a route/handler change reaches users, check what MOUNTS it (`grep -rl
   <router_name>`) — editing the file that defines it isn't evidence it's wired to anything.
7. Introspective continuity ("I remember it, none of it reconstructed") is NOT evidence a process
   didn't restart — a `--resume`d session feels identical to unbroken memory by construction. After
   any suspected restart: check permission mode, Remote Control, and model against what was last
   recorded, don't infer from what you remember.
8. A checkbox/status glyph can be a document's SUBJECT MATTER, not its claim — a synthetic-test
   fixture built to be detected-while-checked looks identical to a real completion marker if you
   read it in isolation. (Earned 2026-09-23: closed #1744 on its own `[x]`, which was the test
   fixture's deliberate target state; the issue's own comment said so, one comment away from the
   checkbox. Caught and reopened same fire. Read the whole artifact's stated purpose before acting
   on a fragment of it — rule 3's failure mode, one level up.)

## Standing guard

ADR-078 D4: the classifier stays stateless — also an ESSENCE standing rule.

## Dormant / background (watch only, none owed)

#1481 Slack principal · #1459 original_message ratchet (Lead's build) · #1462 PDR-006 · #973
MEM-CACHE · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.

- 2026-10-11: item 1 ruled (the split is the mis-serve proof, not liveness). Restore-validity rule added: 2 of the 10-10 restores claim the wrong op. Waiting on CXO for focus-today (`\bwhere.*focus\b` survivor status) and on Lead for the milestones re-delete, the `\bstatus report\b` N=5 probe, `ruled_survivors` with the claim-agreement pin, and the PORTFOLIO 5-row deposit. Lead's interpreter is borrowed for gate scripts (this seat has no venv).
- 2026-10-11 08:3x: filed #1974 (pleasantry family, CXO ruling); GREETING/FAREWELL/THANKS held for cause on it. The ceiling path to Wednesday is 124 → 122 (→ 121); the band needs #1974.
- 2026-10-11 08:4x: CXO withdrew the focus-today survivor (re-delete licensed). Only #1974 is still waiting on CXO.
- 2026-10-11 08:5x: CXO ruled #1974 keep, recorded as PERMANENT_FLOOR (ADR-080 exception). Nothing is waiting on CXO now. Watch Lead's gate commit and the deletion lane (127 → 120).
- 2026-10-11 09:0x: ceiling 124, tail 94 (of which 29 are the permanent floor). Watch the lane to 120.
- 2026-10-11 10:1x: ceiling 121. PORTFOLIO's last literal waits on Lead's N=5 plan-row score for #1884 (licence = validated plan on every sample).
- 2026-10-11 10:2x: plan-aware rule 11 approved with a fallback condition. PORTFOLIO holds at 121 on #1977 (fallback swallows a two-topic turn). Wednesday reads 121.
- 2026-10-11 10:4x: #1977 step 1 approved. Corrected: unclaimed fallback is NO-GO until step 2. The PORTFOLIO literal needs both steps for 120.
- 2026-10-11 11:3x: #1977 step 1 landed and accepted (rule 7 clarified for surface-1-only changes). Step 2 is Lead's, starting now. If it lands, PORTFOLIO reads planned → 120. Wednesday's count is PM's via Exec.
- 2026-10-11 13:0x: #1977 HOLD on the preregistered 20 (6 neither, one phrasing). The ceiling stays at 121 for Wednesday. Re-run the same 20 when #1979 lands.
- 2026-10-11 16:3x: #1982 ruled: no master key on the MCP app; one decrypt-only GitHub subkey (Lead built it, 079477fb15 on main). PAT dual write plus backfill with a security_check=False closed-list pin is built and HELD on `claude/lead-1982-pat-dual-write` (4400ee3d9f). Trigger: PM's PAT-only test on alpha. PM's account is OAuth, so the live check doesn't wait on it. Runbook order: alpha deploy → PM pipe → MCP deploy → snapshot, dry run, apply → live check → Lead drops the fallback. Nothing owed by Arch.
- 2026-10-11 19:1x: #1979 part A (0efe6f4c99) approved pending the served check and an upload negative; part B declined. When A lands, Lead re-runs the preregistered 20, and PORTFOLIO lands → 120 if neither ≤ 2.
- 2026-10-11 19:2x: #1979 A landed (39398a32af); the preregistered 20 met (0/0) and counts. PORTFOLIO lands after CI Tests green → 120. Watch for Lead's landing report and the gate number.
- 2026-10-11 19:5x: #1979 closed by CXO. #1984 placed (label fallback is a code fix; the router half is a corpus row scored N=5). Lead's to build.
- 2026-10-11 20:1x: ceiling 120 verified (pattern_literal_counts TOTAL 120; PORTFOLIO is survivors-only). Wednesday reads 120. #1984 half (1) is Lead's with CXO's copy plus the "On the your … front" fix; half (2) is a description change in the full-run lane.
- 2026-10-11 20:5x: #1984 half (2) is GO as a read_floor_3 wave (STATUS + PRIORITY), Lead, 10-12 START. Watch: Lead's answer on unflipped live-grammar exposure (condition 3) and the baseline-by-name report.
- 2026-10-11 21:0x: SUPERSEDES 20:5x. #1984 half (2) is a description edit (held 40b3c95b33), landing at Lead's 10-12 START after the full run, served check and N=5. The read_floor_3 wave opens only when the deletion lane takes up STATUS/PRIORITY.
- 2026-10-11 21:3x STOP — open threads for 10-12, with nothing owed by Arch:
  - **Ceiling 120.** Wednesday reads 120.
  - **#1984 half 2:** a description edit, held at 40b3c95b33. Lead lands it after the full run, a served check (with an upload negative) and N=5. Read the row diffs when Lead reports.
  - **#1982:** the runbook order is alpha deploy, PM pipe, MCP deploy, snapshot/dry run/apply, live check, then Lead drops the fallback. The PAT dual-write branch (4400ee3d9f) waits on PM's PAT test.
  - **read_floor_3 wave:** opens when the deletion lane takes up STATUS/PRIORITY, with the 20:5x conditions.
  - Grammar-sources line: done by Lead (083f9cc230).
