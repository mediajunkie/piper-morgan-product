# Omnibus Log: August 5, 2026

**Day**: Wednesday
**Sessions**: 11 (Lead Developer, Documentation Management, Chief Architect, Chief of Staff, HOST, Communications Director, CXO, CIO, PPM, Piper Alpha, Web)
**Day Type**: HIGH-COMPLEXITY — COORDINATION
**Justification**: Not 11 independent parallel tracks — one dominant cross-cutting investigation (the 06:46 duty-cycle freeze-alarm / heartbeat / dispatch-latency thread) drew measurements, retractions, and corrections from essentially every role across the entire day, with explicit citation and credit-correction between roles (Arch↔HOST↔PA↔CIO↔Comms↔CXO↔PPM↔Web all directly reference and build on each other's specific numbers within hours). A second, equally cross-cutting thread ran in parallel: PM's direct Radar/Jake question, routed through Janus, answered independently by CXO and PPM and then explicitly reconciled after they gave PM two different answers 20 minutes apart. A third, smaller thread (Comms' "correction must land at the claim" rule) propagated from Comms → PA → Web within the day and each found real live defects.
**Git Commits**: 20+ (fixes, skill bumps, corrections, Ship #054 publish)

---

## Chronological Timeline

- **06:27** — **Web** START. Wake-time heartbeat emitted first, unconditionally, before any other step (`dev/heartbeats/2026-08-05/web.tsv`, 06:28:00) — first-ever web.tsv write, testing last night's carry-forward commitment.
- **06:30–06:36** — **Web** Mail loop, 4 memos — Arch/HOST/PA all retract their "belt can't see busy roles" framing, converge on the real defect (a commit is only valid liveness evidence at the instant it lands).
- **06:37** — **Web** Task loop — marks wake-heartbeat item DONE, reframes as ongoing practice.
- **06:42** — **Comms** START. Runs the heartbeat-surface check owed to CIO first — predicted the surface would fill with most timestamps after 06:46; **prediction wrong on its weakest premise**: at 06:42 the surface held only ONE file (web.tsv).
- **06:42:58** — **Comms** Emits own heartbeat deliberately at Step 1 (not skill-specified Step 5b) to test CIO's fix; lands within 6 seconds — confirms START-always-writes works, flags that Step-1 placement isn't representative of normal Step-5b timing.
- **06:43:48** — **Comms** Surface check two minutes before sweep — six roles awake, only two (web, comms) have rows; predicts wrong failure mode ("doesn't write" vs. actual "writes late").
- **~06:47** — **Lead Developer** START. Notes 06:46 watchdog alarm fired on arch+lead again; treats own commit as liveness disproof. Runway 2-3 days; #1467 streak accounting.
- **06:50–07:00** — **Lead Developer** Canonical routing check 61/61 (Q22 floor); #1467 streak posted honestly (post-#1460 reset, streak 2 of 3).
- **06:57** — **Chief Architect** Fire 1 START. Heartbeat written unconditionally. **Measures the real root cause**: cron minute `:27`, fire arrives `:57` — a systematic +30 min. Derives the "20-minute dead zone": grace (10 min) expires 06:37, sweep runs 06:46, fire actually lands 06:57. Concludes `FIRST_FIRE_GRACE_MIN` must rise to 40-45, not step-placement fixes. Sends to CIO+HOST+Comms+PA+PPM — then discovers HOST proposed exactly this (grace 45) on 07-30, corrects publicly to credit HOST.
- **07:00** — **HOST** Fire 1 START. Builds a five-seat timing table (web, comms, lead, arch, host) — shows lead complied (emitted at wake) and was STILL flagged (landed 7 min after sweep); shows HOST cleared by exactly 1 minute — "not by health, by grace." Concludes grace is computed from registry slot, not scheduler wake time.
- **~07:01** — **HOST** Own heartbeat lands.
- **07:05** — **Comms** Watchdog alarm fires on exactly the two roles Comms had already measured as "woken but unwritten" two minutes before the alarm existed. Confirms the mechanism chain end-to-end.
- **07:07:48** — **Chief Architect** Heartbeat lands — "correctly flagged" per HOST's corrected table.
- **07:12** — **Piper Alpha** START. Prior day (08-04) log NOT properly closed — runs missed close first. `grep -c "DAY-CLOSED"` on yesterday's log returns 2 (both false positives); strict pattern confirms NOT CLOSED, confirming the 07-30 fix works. Finding 2: heartbeat surface went 2→6 overnight, PA's own pessimism from yesterday was wrong.
- **07:14** — **Piper Alpha** Observes STALE list is a clean partition by cron-minute cutoff at that instant; **initially reports "perfect 9/9 rank order, zero exceptions" — later retracted same day** as an artifact of one observation instant (write order ≠ cron order).
- **07:17** — **CXO** START. Reads the heartbeat surface BEFORE own write to avoid contaminating the reading. Confirms Comms' prediction on the "runs too late" defect (4 of 6 landed after 06:46). Own heartbeat lands 07:17:58, cron `:47` → fire `:17` = exactly +30, supporting PA's "additive per-seat" model.
- **~07:20 (amended ~07:5x)** — **CXO** Amends own causal story after reading Arch's mail: the cause isn't end-of-fire placement, it's dispatch latency (harness delivers fires ~30 min after cron minute). Corrects Comms' 06:50 "missing rows" retraction as wrong via a snapshot showing lead/host/arch/pa had all written, just late.
- **07:22** — **PPM** START. Ship #054 publishes today.
- **07:35** — **PPM** Derives the sweep's actual denominator from the registry (sweep 06:46 + grace 10 → exactly 4 of 11 roles "in window") — concludes "no other roles stale" is not a finding since 7 were never examined (m-44 at the coverage layer). Corrects own wrong prediction from yesterday's carry-forward.
- **07:27** — **Docs** Fire 1 START. Prior day closed clean. Wednesday = no Docs-owned day-trigger. Genuine quiet hold; heartbeat write confirmed behaviorally.
- **08:00** — **PM engages Docs directly**: Weekly Ship #054 ready for proofread + publish.
- **08:01** — **PM check-in with Exec** (pre-fire): Ship #054 status, Jake's follow-up loop already closed (PM replied 7/25).
- **09:02** — **Chief of Staff** START. Janus relays PM's **TEN-STEP weekly-reporting spec** (durable standard, first time stated clearly, triggered by #054's report gap).
- **09:10–09:25** — **Chief of Staff** Codifies the ten-step cycle into two canonical surfaces (process guide + `draft-weekly-ship` skill v1.10, new Step 2c hard gate); notifies Docs of new Friday-early obligation (first instance Aug 7).
- **09:27** — **Web** Fire WORK. Mail loop — cron-scheduler thread escalates: Arch's dead-zone measurement, PA's rank-order generalization, HOST's five-seat table, CXO's evidentiary catch on Comms' retraction, PPM's exact 4-of-11 derivation. Web's own datum (+6 min) breaks the pattern rather than confirming it.
- **09:30** — **Comms** Ship #054 shipped to Docs (publish-ready); runs the beats primary-source pass EARLY against `dev/2026/07/16–28/` logs — Beat 24's "more than half" is NOT SUPPORTED (actual 24%); Beat 25 richer than drafted; Beats 26/27/28 confirmed with quotable evidence.
- **09:42** — **Comms** Ship #054 confirmed PUBLISHED. **Retraction 1**: "missing rows, not late rows" was wrong — 9 of 10 fired roles wrote, just late. **Retraction 2**: Comms' own Step-1 placement proposal is refuted by her own row — landed +30 min late even at Step 1, because dispatch (not placement) is the cause.
- **09:47** — **Lead Developer** #1484 follow-ups land (`ddfcd2bbb`) — Arch's positive control + CXO's fail-safe catch-all; #1487 filed (template-embedded render functions unreachable by JS test harness).
- **09:57** — **Chief Architect** Fire 2 WORK. Emits heartbeat as literal first action — still suppressed (`--if-quiet` keys on any commit that day). PA discriminates Arch's H1 (fixed `:57` slot) from H2 (additive +30) — Arch's own seat can't distinguish them, but PA's `:42` cron landing at `:12-15` kills H1. Confirms grace is already computed additively per-role in code.
- **10:00** — **HOST** Fire 2 WORK. Heartbeat-first measured at 7 seconds (vs. yesterday's 24 minutes). Recommends "emit before you sync" as the checkable form. Takes Arch's correction: latency is dispatch, not the START procedure.
- **10:05** — **Comms** An abandoned regex search completes in background — returns EMPTY for all three beat claims including Beat 26 (which Comms had independently confirmed TRUE) — a control demonstrating the search pattern structurally couldn't match; distinguishes "absence" (weak) from "contradiction" (strong) evidence.
- **10:12** — **Piper Alpha** Fire 2 WORK. Pulls ground truth from heartbeat tsv write-timestamps directly. **Claim 1 dead** ("additive ~+30" wrong across seats, range +6 to +40); **Claim 2 dead** ("perfect 9/9 rank order" was one-instant artifact); **Claim 3 survives** (9h overnight gap vs 7h threshold is structural). Pre-registered falsifier fires: ppm never wrote — reveals a third state, "alive but not emitting."
- **10:17** — **CXO** Fire 2 WORK. **Major correction**: Janus/PM ground truth shows Jake's reply was NEVER open — PM replied same-day 07-25. CXO had been the one repeating "10 days overdue" to PM for days; traces why four roles independently got this wrong (evidence lived in PM's personal email, invisible to every cohort surface — m-45 with a shared corpus, not a shared procedure). Catches own portfolio citing two issues (#950, #992) closed in April.
- **10:22** — **Web** Task loop — updates carry-forward with timing-anomaly thread. / **PPM** Fire 2 WORK — PA's falsifier fired on PPM; confirms it was own omission (skipped Step 5b at 07:22 START), not the mechanism; adopts wake-emission going forward.
- **10:27** — **Docs** Fire 2 WORK. Files **website#31** for the converter double-`<em>` bug PM caught in Ship #054's rendering (bug live since at least #039, affects 15+ Ships) — two decisions handed to PM (fix-forward-only vs. regenerate back-catalog; whether Metrics becomes a real `###` header).
- **10:37** — **CIO** START. **The 06:46 alarm fired a sixth consecutive morning** despite heartbeat adoption going 2/11 → 10/11 overnight — because heartbeats land AFTER the sweep, not before. Ships `FIRST_FIRE_GRACE_MIN` 10→45.
- **~11:0x** — **CIO** Discovers HOST proposed grace-45 on 07-30 already (three independent derivations sitting unshipped for 6 days). PA root-causes the REAL defect as arithmetic, not tuning (`expected_threshold` counted the current fire-hour as already landed) — CIO ships the `<`/`>=` fix, verified as a pure function. CIO retracts own "late cluster" (host/pa/ppm) as a measurement artifact (read last line of tsv instead of first).
- **12:27** — **Web** Fire WORK. Mail loop — cron-scheduler thread self-corrects sharply: PA retracts "uniform +30" and "perfect rank order" using ground truth; PPM finds own pre-registered "miss" was self-inflicted; Comms retracts both morning claims; HOST/Arch report "emit first" measured not asserted, confirm grace is already additive per-role.
- **12:42** — **Comms** ppm's absence resolved (confirmed skipped, not suppressed). Deliberately pivots off the heartbeat thread to protect tomorrow's post deliverable.
- **~12:xx-15:xx** — **Comms** Pre-passes Tuesday Aug 6 post ("Drained on Paper") a day early — mechanically clean, 2 open `[PM:]` questions, names two proposed cuts.
- **12:47** — **Lead Developer** **#1467 CLOSED** — streak 3-of-3 met, confirmation recorded in-corpus.
- **12:57** — **Chief Architect** Fire 3 WORK. Reviews Pard's (cross-project) Amber-fleet stand-down runbook — finds `ls-tree` gate command isn't recursive (reads RED for every resident, always); finds the gate measures an agent-authored filename, not evidence; finds nothing re-arms crons after reboot. Flags that grace-45's justification conflates two different latencies — real margin is 5 min, not 15.
- **13:00** — **HOST** Fire 3 WORK. Relays Arch's runbook review to Pard (Arch has no channel). Adds own gap: gate runs at T-30m, reboot at T — anything committed in that window is un-handed-off by construction.
- **13:12** — **Piper Alpha** Fire 3 WORK. Finds CIO's retraction (of the "late cluster") reached mail but NOT the shipped code — `duty-cycle-freeze-check.sh:57-59` still asserted it. Lands the correction directly in code with the corrected per-role table. Nearly repeats the same error while fixing it — caught before publishing an implausible number.
- **13:17** — **CXO** Fire 3 WORK. Answers PM's direct Radar question (via Janus) from source: Radar is NOT in "bucket A" (cosmetic UI cuts); web UI not being retired; PDR-005 (PM-ratified 06-05) preserves a thin bespoke UI. Finds the actual cause: PDR-006 contradicts itself 124 lines apart. Can't yet determine which numbered MUX surface Radar corresponds to — states this honestly rather than guessing.
- **13:22** — **PPM** Fire 3 WORK. Runs wake-emission heartbeat first. Answers PM's plain-English Radar questions.
- **13:27** — **Docs** Fire 3 WORK. Applies own new "scan every fire" lesson and finds the scan itself was broken (filename-pattern grep missed real primary-recipient memos whose frontmatter said `to: docs`). Rebuilds scan to parse frontmatter directly; surfaces and closes six stale memos, some over a week old.
- **15:27** — **Web** Fire WORK. Mail loop — thread tapering to close: CIO shipped grace 45 (credited to HOST); Arch flags the margin caveat (5 min not 15); PA finds own retraction never reached the shipped code, fixes the comment.
- **15:32** — **Web** Task loop — marks cron-latency thread FULLY CLOSED.
- **~15:42** — **Comms** PA's "correction must land at the claim, not just the artifact" rule turns into a self-check — Comms runs it on her own two most-recent docs, finds and fixes 2 hits.
- **15:47** — **Lead Developer** Quiet hold — CI green, no PM word yet.
- **15:57** — **Chief Architect** Fire 4 WORK. HOST relays Arch's runbook review to Pard and finds the gap Arch missed. Arch re-ranks HOST's own three proposed fixes — the "cheap" option HOST ranked third is actually the only one that closes anything.
- **16:00** — **HOST** Fire 4 WORK. Accepts Arch's re-rank. Four fires now show dispatch as a stable per-seat CONSTANT (not jitter) — +23.5–23.6 min, 3-second spread over 10 hours.
- **16:12** — **Piper Alpha** Fire 4 WORK. Runs Comms' "correction must land at the claim" rule on own artifacts — finds a **live false legal claim** in `docs/legal/privacy-policy-DRAFT.md:139` (GitHub credential revocation misrepresented, 46 lines below PA's own 08-04 correction). Names the third-order trap: an audit-grep for a retracted claim matches its own correction text.
- **16:17** — **CXO** Fire 4 WORK. Discovers she and PPM gave PM two different answers to the same Radar question 20 minutes apart — PPM said "there is no web page" (wrong); CXO's framing is more accurate but incomplete. Adopts PPM's sharper distinction. Flags a real open question (#1237 "all four" vs "3-of-4") without asserting an answer.
- **16:22** — **PPM** Fire 4 WORK. Realizes own "there is no web page" answer to PM was WRONG — PDR-005(b), which PM personally ratified, preserves a thin bespoke UI. CXO caught it. Names the process lesson: reconcile-then-send, not send-then-reconcile.
- **16:27** — **Docs** Fire 4 WORK. Genuine quiet hold — mail scan (fixed) finds nothing new addressed to docs.
- **16:37** — **CIO** Fire WORK. Cross-project debugging with Klatch (Pard/Janus/Argus) — finds their 9am fire's "95 bytes" was discarded stderr, not logged. Notes Klatch's wrapper-written liveness log is architecturally better than Piper's agent-written heartbeat. PA catches that CIO's own retraction never reached the code.
- **18:27** — **Web** Fire WORK. Mail loop — tests Comms/PA's rule against own two most-recently-authored docs, finds and fixes one real instance (`BRIEFING-ESSENTIAL-WEB.md`).
- **18:47** — **Lead Developer** Quiet hold.
- **18:57** — **Chief Architect** Fire 5 WORK. Replicates HOST's dispatch-constant finding on own seat, tighter (+30m 13-14s, 1-second spread across 4 fires). HOST catches an over-generalization in Arch's framing. Pre-registers tomorrow's prediction so it can fail.
- **19:00** — **HOST** Fire 5 WORK. Arch replicates HOST's dispatch constant on a second seat and corrects HOST's over-generalization about landing point.
- **19:12** — **Web** Task loop. / **Piper Alpha** Fire 5 WORK — supplies the "third dispatch seat" HOST asked for; drafts a plugin manifest, finds a PDR-006 gap (documents only local `command`-based MCP servers, not the hosted endpoint) — states the negative claim's limits precisely.
- **19:17** — **CXO** Fire 5 WORK. Closes own open question from Fire 3 — establishes Radar's rendering IS "Surface 1" (history sidebar) via #1236, roadmap.md:127, PDR-005:53, and three cross-client-variant commitments. Names the durable finding: "5 of 7" MUX surfaces scoped for 1.0 but the five members are never enumerated.
- **19:22** — **PPM** Fire 5 WORK. CXO's Surface 1 finding lands; PPM verifies every citation independently and adds Surface 1 is ALSO estimated/"unblocked NOW." Deliberately keeps the reply short (third answer to PM on the same question).
- **19:27** — **Docs** Fire 5 WORK. Finds a second mail-scan format gap (bold-markdown `**To**:` vs YAML frontmatter). Closes two real multi-day-old items: rules BRIEFING-CURRENT-STATE.md does NOT need derived-ness treatment; rules Web is Tier 2 (not Tier 3) in ROSTER.md, full reasoning recorded in the doc.
- **20:32 (cron) / 21:02 (actual fire)** — **Chief of Staff** Fire 2, WORK→STOP. **Weekly Ship #054 PUBLISHED**, live. Jake decisions: 3 answered by PM, 3 worked by Exec tonight — plain-English doc leading with the Radar resolution. Pard's Amber env-var caveat landed in the keys-setup doc.
- **21:39** — **Web** Fire STOP. Mail loop — Docs' Tier 2 ruling closes a 2-day-old item Web had flagged; cron-dispatch thread continues.
- **21:47** — **Lead Developer** Fire STOP. PA's phase-0 plugin-manifest finding noted for tomorrow. CI green all day. Day-close: quiet consolidation, #1467 closed, #1484 follow-ups landed, #1487 filed.
- **21:57** — **Chief Architect** Fire 6 STOP. Closes PA's Phase-0 PDR-006 risk at the primary source — confirms remote MCP (`http`/`sse`/`ws` with `headersHelper`) IS supported; `headersHelper` becomes the named carrier for PDR-006 condition 1.
- **22:07** — **HOST** Fire 6 STOP. Own "dispatch is a per-seat constant" claim from earlier is **falsified by HOST's own next fire** (5 fires at +23m3x, 6th at +30m22s). Withdraws the per-seat-grace proposal built on it.
- **22:12** — **Piper Alpha** Fire 6, final. Arch's PDR-006 fix confirmed — PA's own earlier "none found" search revealed to be a truncated `grep | head -8` that evicted the true positive. PA's own pre-registered dispatch-latency prediction FAILS — number is identical, meaning the arch/pa seat delta PA had told everyone to discard "may be real."
- **22:17** — **CXO** Fire 6 STOP. PPM independently verifies CXO's Surface 1 determination. Flags own measurement resolution (minutes, not seconds) as insufficiently precise to count as corroboration.
- **22:22** — **PPM** STOP. Emits heartbeat as STOP (catches own cron-prompt bug — hardcoded WORK). Records Arch's #1462 resolution.
- **22:27** — **Docs** Fire 6 STOP. Final mail check, all cc-only broadcast traffic. Day-arc: Ship #054 headline, converter-bug find, mail-scan methodology fix, two roster/tier rulings.
- **22:37** — **CIO** Fire STOP. Pre-registered `UserPromptSubmit` probe FIRES LIVE — establishes a better clock for the dispatch-latency thread (+30m00.0s exactly). PM calls a review of CIO's own duty-cycle design after Pard's self-report — CIO goes to source and finds Pard actually followed CIO's design; endorses disarming 9 of 12 Klatch fires.

---

## Canonical References

- **PDR-005: Bring Your Own Chat — Distribution Model** (`docs/internal/product/pdr/PDR-005-bring-your-own-chat.md`) — §53, 65, 74, 84, 122, 135, 245, 288, 328 cited by CXO/PPM for the Radar/Surface-1 chain; rule (b) preserves a thin bespoke UI, verified against the ratified text rather than paraphrased.
- **PDR-006: Hosted MCP Endpoint + Plugin Distribution Model** (`docs/internal/product/pdr/PDR-006-hosted-mcp-plugin-distribution.md`) — found to contradict itself at :163-164 vs :287 ("not rejected entirely" vs "surface being retired"); condition 1 (fail-closed `owner_id`) gets its carrier (`headersHelper`) confirmed by Arch's fetch of the primary plugins-reference doc.
- **roadmap.md** (`docs/internal/planning/roadmap/roadmap.md`) — :127 cited for Surface 1 / Phase 2.1 "unblocked NOW"; :145 cited for the #1237 3-of-4 record.

---

## Executive Summary

### Core Themes
- The 06:46 freeze-alarm/heartbeat saga reaches full technical resolution: not a heartbeat bug but ~30-minute structural dispatch latency plus a 10-minute grace window plus a threshold-arithmetic bug, fixed in two shipped changes (grace 10→45, `<`/`>=` threshold fix) — with credit repeatedly mis-attributed and self-corrected across the day.
- PM's direct question ("are we losing Radar?") triggers a same-day cross-role investigation that finds the actual cause was a self-contradiction inside PDR-006, resolved with CXO/PPM converging on Radar/Surface-1 being scheduled, not cut.
- "A correction that stops at the mailbox hasn't happened" emerges as the day's dominant methodology finding, independently rediscovered by CIO, Comms, and PA, and found to have caused a live legal misrepresentation in the privacy-policy draft.
- Weekly Ship #054 ("Clear Is Not a Measurement") publishes end-to-end (PM→Comms→Docs) and PM's own follow-up question uncovers a genuine multi-Ship rendering bug (website#31) silently live since #039.
- Multiple roles discover and retract their own measurement errors within the same day (PA: 2 dead claims; CXO: false Jake-overdue claim carried for days; HOST: falsified own "dispatch constant"; CIO: retracted "late cluster"), producing a strong week-long thread on checking ground truth vs. reasoning from a single seat.

### Technical Details
- `FIRST_FIRE_GRACE_MIN` shipped 10→45 (CIO, credited to HOST's 07-30 proposal) — clears max on-time seat with only 5 minutes margin.
- `expected_threshold` arithmetic bug fixed by PA/CIO: counted current fire-hour as already-landed, producing a false 7h gate against a real 9h overnight gap; fixed via strict `<`/`>=`, verified as a pure function.
- Dispatch latency established as a stable **per-seat constant** (not jitter): arch +30.2min (1s spread/9hr), host +23.6min (3s spread/10hr — later falsified by its own next fire), pa +30m17s (4s spread/12hr), web +6min (outlier, unexplained).
- CIO's `UserPromptSubmit` pre-registered probe fires live at 22:37, establishing a cleaner instrument (cron-to-hook-arrival = +30m00.0s exactly) than commit-timestamp inference.
- #1484 (Slack settings gate) verified end-to-end by Arch — 3 tests pass; catch-all-copy default flagged as wrong by CXO; structural gap found — the branch deciding user copy is inside a Jinja template unreachable by the JS test harness.
- website#31 filed: blog converter regex bug (`^\*(.+)\*$`) double-wraps bold-only lines in `<em>`, live since Ship #039, affecting 15+ published posts.
- PDR-006 gap (local-only MCP `command` servers documented) closed by Arch — remote MCP (`http`/`sse`/`ws`, `headersHelper`) IS supported.
- Pard's Amber stand-down runbook reviewed by Arch/HOST: non-recursive `ls-tree` gate, agent-authored-filename evidence problem, T-30m-to-T live-session gap, no cron re-arm after reboot.

### Impact Measurement
- Heartbeat surface adoption: 2 of 11 roles (yesterday) → 10 of 11 by this morning's START.
- Sixth consecutive morning of the false 06:46 alarm before both root causes are fixed same-day.
- Ship #054 published live, syndicated, full v1.5 template audit clean.
- Three roles (PA, Web, Comms) find live "stale correction" defects within hours of the rule propagating — one is a legal misrepresentation in a privacy-policy draft.
- A four-day-carried false claim (Jake's reply "10 days overdue," repeatedly relayed to PM) is corrected — PM had actually replied same-day, 07-25, via a channel invisible to every cohort surface.

### Session Learnings
- "Checking ground truth beats reasoning carefully" recurs across at least six independent instances today (PA, HOST, CIO, Comms, CXO, Web all catch themselves generalizing from a single seat/instant as if it were a cohort-wide law).
- "A correction that stops at the mailbox hasn't happened" hardens into a working rule after CIO's own shipped-code retraction is caught by PA, then Comms/PA/Web propagate a stronger version.
- Verification-instrument failures recur: HOST measures the wrong exit code; CXO's shell calls silently abort on unquoted globs (twice); PA's `grep | head -8` false-negatives via truncation; three separate "count is not a marker" traps.
- Denominator discipline (m-44) is central: PPM/PA/CXO all independently derive that the sweep's "no other roles stale" silently examined only 4 of 11 roles.
- Pre-registered falsifiers (stated before the result) repeatedly pay off — PA's ppm prediction, Arch's tomorrow-decomposition prediction, CIO's probe ambiguities.
- Cross-project coordination (Klatch/Pard/Janus/Argus) surfaces a genuinely better-designed liveness mechanism (wrapper-written vs. agent-written heartbeat) that CIO explicitly credits rather than defends the home design.
- PM's own instruction discipline (no manufactured urgency, "I am a Time Lord") is explicitly honored multiple times (PPM, CXO, Exec) when delivering Jake-decision material.
