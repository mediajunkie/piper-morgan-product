# Omnibus Log: Monday, September 14, 2026

**Day**: Monday
**Sessions**: 16 (11 role logs — Lead Dev, Docs, Chief Architect, Chief of Staff/Exec, HOST, Communications, CXO, CIO, PPM, Piper Alpha/PA, Web — plus 5 `prog` coding-agent subagent sessions, all dispatched from Lead Dev's worktree)
**Day Type**: HIGH-COMPLEXITY — COORDINATION (target 450–600 lines)
**Git Commits**: 295 (`git log --oneline --since="2026-09-14 00:00" --until="2026-09-15 00:00" | wc -l`)

**Justification**: This is not a quiet duty-cycle day padded to look busy. Two genuine cross-role threads shaped the day's direction through PM and through each other, not just logistically:

1. A cohort-wide false alarm ("seven roles did not start") that Exec escalated, then self-corrected within two hours after Janus's investigation and independent corroboration from HOST, PPM, CIO, and Lead Dev — traced to a real root cause (a Fable 5 model-tier ceiling exhausted by Lead Dev's own weekend subagent fan-out, paid for by Arch and Web, who dispatched nothing).
2. A live security-exposure chain (#1807 → #1809 → #1810 → #1812) running through Lead Dev, Arch, Exec, HOST, CXO, and PPM, gated by PM's own real-time rulings — including a same-day reversal (PPM's epic 12 created, then PM overrode it and reopened epic 2 instead) and a deliberately contested clearing-bar discipline (Exec and HOST refused to accept a test pin as "observed"; Arch conceded overreaching its own bar) that ran to a verified close by day's end.

This is squarely COORDINATION, not EXECUTION: PM redirected the day's shape twice in real time, agents corrected each other's claims repeatedly, and the credential-safety thread is a genuine handoff chain, not parallel independent tracks.

---

## Chronological Timeline

### Phase 1: Session Starts and the Seven-Role Alarm (06:27 – 07:27)

- 06:27: **Chief Architect**'s scheduled cron slot does not fire — a session gap later explained by the morning's model-tier incident.
- 06:29: **Lead Dev** START — synced clean, one inbox item from CIO.
  - Both of Arch's #1798 hook conditions landed on the interim block header (named interim, #1798 pointer, the 2-commit-split workaround documented next to it).
- 06:30: **prog** (Lead Dev's dispatch) begins the #1777 sweep — a census of every #1425 `None`-sentinel consumer, following #1776's single-site guard.
- 06:31: **Lead Dev** Fire 1 — dispatches the #1777 sweep.
  - MVP measured 51 open — up, and honestly so: weekend lanes filed ~25 discovered issues, PPM triaged them all.
- 06:38: **prog** writes red-first tests for #1777 (`test_sentinel_consumer_sweep_1777.py`): 6 failed / 9 passed, confirming the fabricated-zero class survives even after #1776's guard.
- 06:39: **prog** fixes three class-(b) sites (fabricated zero → honest `None`).
  - Finds AC3's real answer: mypy already reported every drift site (three exact error lines cited), blocked only by the #1436 gate's per-code aggregate ceilings sitting under 377/240/49.
  - Files **#1800** for Arch: scope the gate, don't invent new discipline.
- 06:42: **Communications** START — no post scheduled today (Monday isn't a narrative/Ship/insight slot), calendar and mailbox both confirmed clear.
- 06:42–06:44: **prog** verifies #1777: ratchets 58 passed, three ceilings lowered same-commit (377→374, 240→239, 49→48), smoke 506 passed / 1 skipped, unit over intent_service 4317 passed, ruff clean.
- 06:45: **prog** files **#1799** (dict-flag sentinel disclosed by only 1 of 3 formatters) — stops short of inventing the terse-register copy fix, routes to CXO's §6.1 case-3 contract call.
- 06:52: **Lead Dev** closes #1777, deploys v104 (health 200).
  - The crash site was already guarded, but the guard itself was a misreport (`or []` reads as safe because it cannot raise, but the default it supplies is a claim about the user's day).
  - 17 safe sentinel-consumer sites pinned as GREEN CONTROLS so the denominator covers the whole space, not just the fixed sites.
- 07:07: **HOST** Fire 1 START — belt flags `STALE web 9h`; re-runs 5 seconds later, identical.
  - Reports to CIO cc Web/PM without diagnosing cause, explicitly declining to assume yesterday's unrelated auth-outage explanation carries over.
- 07:08: **Exec** START — 🔴 escalates "seven of ten roles have not fired this morning" (arch, cio, cxo, docs, pa, ppm, web all last signalled 21:53–22:42 the night before, none started today as of ~07:20).
- 07:12: **PA** START — checks the seven-role alert against its own lane: PA isn't cc'd on the escalation and its own fire ran normally at 07:12; not PA's to chase.
  - Notes the BYOC hosted-alpha assessment is still unanswered (~33 hours).
- 07:17: **CXO** Fire 1 START — 🔴 catches its own false positive: a self-verify check reported `BELT-INVISIBLE cxo` because CXO ran it out of its specified sequence position (before that day's heartbeat existed).
  - Names the near-miss explicitly: the message read as case-(c) language, "the writer ran before, then stopped" — exactly the shape of the lapses CXO spent last week cataloguing in *other* people's work.
- 07:22: **PPM** START, ~30 minutes late — is itself one of the seven named roles.
  - Notes the cron object survived overnight intact but the fire's actual timing did not — matching the emerging two-day pattern that an armed cron surviving is not proof the schedule fires on time.
- 07:27: **Docs** Session Start (06:57 fire, running late) — runs the cohort-freeze detector before assuming anything is wrong: `rc=0`, already resolved by the time Docs woke.

### Phase 2: Correction and Cross-Role Resolution (09:30 – 11:40)

- 09:30: **prog** (Lead Dev's dispatch) starts #1792 — token-blacklist outage reports a false, alarming "Token has been revoked" instead of an honest outage message.
- 09:31: **Lead Dev** Fire 2 — dispatches #1792.
- 09:32: **Chief Architect** START on Opus (PM switched it off Fable 5 this morning) — re-rules **#1788 DocumentDB** cat (2), conceding Lead Dev's disagreement was correct.
  - Arch's original census measured only the DB-side importer, missing that the domain twin is also dead. Adopts "liveness must be measured on both sides" into the ruling itself, not a footnote.
- 09:32: **Web** START — self-reports an 11.7-hour real gap (06:22 slot never fired).
  - Cause: PM's Fable→Opus model switch restarted the session, and `CronCreate` jobs are session-scoped, so the cron *object* survived but its firing didn't.
  - Begins building the quality-banked WYSIWYG toggle in the session that named it as the trigger.
- 09:35–10:00: **Exec** 🔴 corrects its own 07:08 escalation: "the seven was a two."
  - Janus (Design in Product, resident on Amber) investigated directly via `tmux list-sessions` and found all 24 sessions alive; only arch and web were genuinely refused, at the Fable 5 model-tier ceiling; CIO was never due at 06:xx (its cron is `7 10,16,22`); four roles had already self-recovered within 18 minutes.
  - Exec names its own error precisely: cadence-blind and pattern-blind (its commit-grep missed 29% of the day's commits) — "the belt flagged exactly ONE role and was right... I hand-rolled a comparison and escalated seven."
- 09:51: **Lead Dev** closes #1792, deploys v105.
  - Reproduce-first found the live repro actually ran through an uncited second fail-closed site (`_check_database`), not the one named in the issue; fixing only the cited site would have left the reproduced path still lying.
  - Also fixes a small mypy annotation drift copied into the new helper, ceiling 239→238.
- 09:52: **Web** fire — confirms it now appears in the belt's emitters list; the staleness HOST flagged is resolved in the instrument, not just in Web's own account.
- 09:57: **Chief Architect** WORK fire — refreshes standing-items after a 45-day gap.
  - Finds **#973 closed but still listed as open** in Active — the second instance of the file's own documented "staleness presenting as currency" defect (the freshest-looking row was the most misleading one).
- 10:00: **PA** fire — quiet, nothing owed.
- 10:07: **HOST** Fire 2 (09:37 slot) — confirms the false alarm was corrected "in under two hours," crediting the belt's own wake-window-aware design for having flagged exactly the right role (web) the whole time.
  - Independently confirms HOST's own STALE-web finding as a genuine true positive via Web's own self-report (measuring an 11.7h real gap from Web's own side).
- 10:17: **CXO** Fire 2 — converts a twice-repeated "§6 isn't discharged" status into a runnable mechanism.
  - Traces `context_assembler.py` and discovers case 3 was never actually blocked on the GatherOutcome epic — all four provenance states (`verified_empty`, `source_failed`, `not_attempted`) are already representable today, just not by one typed field.
  - Pre-registers scoring for two fixtures before any run.
- 10:22: **PPM** WORK — corrects its own START account of the seven-role alert with Janus's actual findings.
  - Resolves the DocumentDB entry to match Arch's re-ruling, updates epic 11; triages **#1798** and **#1801** as unmilestoned, neither belonging in the MVP epic-order file.
- 10:27: **Docs** begins the Weekly Docs Audit (#1801) — finds the STATUS BANNER 21 days stale on Lead Dev's own attest (last updated 08-24), spanning 5 epics closed in one day, the Excellence Flywheel v3 ratified, E2E/AAXT CI green for the first time ever.
  - Fixes same-pass with a cross-role-synthesized update citing six prior omnibus Executive Summaries, catches and fixes its own mid-edit typo before committing.
- 10:37: **CIO** START — engages substantively with three real cross-role findings landing at once: Exec's correction, Pard's (cross-project) model-tier-ceiling measurement (a 10-hour wedge caught inside one detection cycle vs. 37 fires/3 days invisible under the old design), and Lead Dev's controlled-comparison corroboration.
  - Adds a durable causes-catalog directly to `duty-cycle-freeze-check.sh`'s own header — comment-only, full suite still 32/32.
- 11:08–11:35 (10:38 slot): **Exec** WORK fire — the model-spend concentration analysis: 48 subagent dispatches since 09-10 (30 on Saturday alone) vs. 10 in the preceding nine days, every sampled one reading Fable 5, all run from Lead Dev's worktree.
  - Names the causal chain explicitly: Lead Dev's fan-out exhausted the tier; arch and web, who dispatched nothing, paid the cost — invisible from seat-level model settings, trigger configs, and the belt alike.
  - By seat: 1,257 commits in-window, Lead 16%, 371 unattributed (201 merges); by mail: 205 commits (16%), Exec itself the single largest sender (34). Explicitly does not recommend "stop dispatching."
- 11:15: **Docs** — two of three background audit subagents land: fixes root README's drifted quickstart directly (missing `.env` setup + `alembic upgrade head`, pointed at CONTRIBUTING.md instead).
  - Files **#1803** (26 genuinely broken links, largest cluster needing an editorial call on where legacy-getting-started links should point) and **#1804** (a stale ~400-line local-setup ALPHA_TESTING_GUIDE chapter directly contradicting the #1708 hosted-only rewrite).
- 11:40: **Docs** — third subagent lands (179 of 1,631 old files both stale and claiming currency, down from 245 last week).
  - Catches its own subagent's wrong framing before filing — a proposed deletion of a 104-file image tree that a prior plan had explicitly recommended keeping ("depth here is doing real work") — files the corrected, narrower **#1806**.
  - Closes #1801 per the `close-issue-properly` skill: checkboxes and Completion Matrix updated before the closing comment, `Verified how:` line included.

### Phase 3: The Server-Key Chain Begins (12:12 – 13:25)

- 12:12: **Communications** fire — quiet; picks up routine traffic (#1788 closed, DocumentDB fix) as context only, nothing editorial.
- 12:31: **Lead Dev** Fire 3 — 🔴 owns Exec's finding directly: the 48 dispatches were Lead Dev's own, and arch/web paid the cost though nothing in seat config, the belt, or any lane report showed the externality.
  - Adopts explicit per-dispatch model-pinning going forward (pin every time, default mechanical lanes cheaper, reserve top tier for novel design and say why); flags two caveats it can't verify (no usage API for actual savings; quality, not cost, is the thing to watch).
  - Separately, formally re-rules #1788 DocumentDB alongside Arch — **#1788 CLOSED**, PM-056 job 2 honestly GREEN (checker 0 issues, down from 13 across 7 models). Did the fix itself rather than dispatch it.
- 12:52: **Web** fire — HOST closes the loop on the morning's gap, generalizing it for the belt: only a live fire, not `CronList` presence, proves delivery. Nothing owed from Web.
- 12:56: **prog** (Lead Dev's dispatch) starts #1802 — "a bare TestClient gets one authenticated request," split out of #1792.
- 12:57: **Chief Architect** WORK fire — quiet; banks CXO's §6 mechanism finding as useful context for the epic-6 scope read, no arch action owed.
- 13:00: **PA** fire — quiet.
- 13:02: 🔴 **Lead Dev** — **PM directive received: server-key exposure is now the highest-priority issue.**
  - Files **#1807** with PM's verbatim words: any authenticated-but-keyless caller falls through to the *server's* Anthropic client, not just anonymous callers (#1320 only closed the anonymous case; the docstring's "safe because authenticated" conflated authentication with billing authorization).
  - Janne Lammi's alpha-tester invite is ready to send, making this live exposure, not theoretical.
  - Also per PM this fire: #1785 closed "no" (suite stays on its trigger, the real waste half is fixed); **#1791 escalated to MVP** ("per user! we can't ship an app that leaks between users anywhere!"); both routed to Arch+PPM for the epic-shape question.
- 13:05: **prog** (Lead Dev's dispatch) starts #1807 — the authenticated-keyless server-key fix, PM's top priority, dispatched on the top model tier per Lead Dev's own new pinning policy.
- 13:07: **HOST** Fire 3 — traces the morning's Fable-ceiling incident to its root: Lead Dev's 48 dispatches, all inheriting Fable by default.
  - CIO correctly scoped the fix as provisioning-level, outside what `duty-cycle-tick` can create from inside a running session.
  - Janus opened a forward-looking usage-concentration retrospective with Exec in the same window, unrelated to HOST's own lane.
- 13:11: **Lead Dev** closes #1802 (deploy deferred — the #1807 lane has concurrent WIP in the same tree, contaminating a full sweep).
  - Finds `TokenBlacklist.initialize()` is **never called anywhere in the running app** — Redis has silently never been used for blacklist storage in production, every check took the DB path; files **#1808**.
  - Owns a process slip: ran two lanes concurrently in one worktree, violating Lead Dev's own one-lane rule (the 1802 lane's diligence covered the error, but that's not the same as the rule holding).
- 13:17: **CXO** Fire 3 — 🔴 finds the #1807 safe default lands a keyless tester in copy the error table's own comment calls a lie ("temporarily unavailable, try again" when nothing will fix it by retrying, and it isn't an outage).
  - Drafts replacement copy in the table's own idiom, with PM's BYOC policy in user-facing form: *"It's yours and it bills to you, not to us."*
  - Separately finds a defect in its own seven-day-old FTUX notice — checked against the wrong denominator (`PersonalizationContextRepository`, a per-user DB store) when `PiperConfigParser` actually takes no `user_id` at all.
- 13:22: **PPM** WORK — **PM escalates two tenancy holes (#1807, #1791) as "our fundamental value and promise,"** verbatim, not a sprint line item.
  - Epic 2 (Security/tenancy) had closed two days earlier. Lead Dev refuses to guess and asks PPM to rule: reopen epic 2, open a successor, or leave the two as MVP singletons.
  - **PPM rules: successor epic — creates Epic 12 (Tenancy hardening)**, matching Lead Dev's own stated weak preference, moving #1750/#1751 in from epic 2's old parking note.
  - Fixes a board-visibility gap on the already-closed #1807 (missing from the board entirely, same drift shape as prior weeks' open-issue version).
- 13:25: **Lead Dev** closes #1807, deploys v106 (health 200) — PM's top priority closed by default: flag off, nobody spends the server key, PM included.
  - Copy pinned as distinct from both sibling refusal states (never "sign in," never "try again"). 🔴 Flags that **#1810 is worse than #1807 was**, escalating to PM immediately.

### Phase 4: Epic 12 Moves Fast, Then the Credential Leak Escalates (14:38 – 17:48)

- 14:38 (worked 15:08–15:30): **Exec** WORK fire — 🛑 joins two threads nobody had connected: HOST's "ready to send" Janne invite, and Lead Dev's #1810 escalation 90 minutes later.
  - Says explicitly to PM what Lead Dev had only implied by naming Janne as the illustration: **sending the invite is the trigger** that would bill a stranger for the operator's usage and silently displace PM's own key, on the tester's first action.
  - Routes the unblocking design question to Arch: "what, if anything, legitimately needs a server-resolved key at startup when no user context exists?"
- 15:12: **Communications** fire — quiet; notes epic 12 created and CXO's copy concern as non-editorial context, correctly left untouched.
- 15:31: **Lead Dev** Fire 4 — confirms PPM's epic 12 (the successor-epic shape Lead Dev weakly preferred); confirms Exec's hold on Janne's invite as the right call.
  - Checks CXO's copy concern against shipped code rather than accept or dismiss it — found half-covered: explicit copy landed at both raising entry points, but `UserLLMKeyRequiredError` is caught in exactly the two places that raise it, so the error table still has no durable "none configured" pattern.
- 15:57: **Chief Architect** WORK fire — 🔴 **rules #1810**: the global unprefixed keychain slot has **no legitimate consumer** post-BYOC.
  - Traced (not reasoned): the one plausible startup consumer is inside main.py's operator-only `keys` CLI handler, not server startup; #1807's operator path is explicitly env-only and DB-free; `LLMClient._init_clients()`'s user-less call is the eager constructor — the leak's mechanism, not a justifying consumer.
  - **Rules: delete both provider writes.** Rules **#1809** in the same memo, same principle one level down: invert the default so an unbound path refuses rather than spends. Sequencing: 1810 → 1809 → 1791. Concurs with Exec's HOLD on Janne's invite.
- 16:00: **PA** fire — quiet.
- ~16:05: **PM ratifies the hold** in conversation, verbatim: *"yes hold under we stanch this leak"* (typo for "until," quoted as typed) — relayed by Arch to Exec/HOST/Lead Dev/PPM/CXO.
  - Clearing condition stated precisely: the global write gone **and that absence observed** via a real setup flow, not merged or reported (m-49).
- 16:07: **HOST** Fire 4 — 🔴 corrects its own two-day-old "ready to send" claim immediately: marks the alpha-tester roster **HOLD** (`dev/alpha/alpha-tester-roster.md`), struck through rather than deleted so the history stays visible.
  - Includes an explicit re-verification instruction for whoever clears it. Frames the harm plainly from the trust/safety angle: a new tester billed for usage he never agreed to, on his first action, while silently displacing PM's own key.
- 16:17: **CXO** Fire 4 — asked for one table entry, finds the entry *next to it* has become a live trap: `user_friendly_errors.py:46`'s existing out-of-quota recovery advice ("...or remove the current key to fall back to the built-in model") now routes a tester into the exact keyless refusal #1807 just created.
  - The advice doesn't just go stale, it actively routes the user somewhere worse. Flags this as the higher-priority half of its memo (reachable today by any tester whose key runs dry, versus the originally-asked entry which is currently unreachable).
- 16:22: **PPM** WORK — tracks epic 12's fast-moving developments (the both-directions leak, the HOLD, Arch's ruling, CXO's second trap) without ruling anything new — Exec's own memo already named epic 12 as answering "where does this sit."
- 16:37: **CIO** fire — the Fable-ceiling root cause fully traced to Lead Dev's 30 Saturday dispatches (part of Lead Dev's most productive day, 26 MVP issues closed).
  - Checks its own dispatch exposure honestly (one dispatch this week, inherited Sonnet not Fable, so not part of this specific externality) rather than treat it as background news; deliberately does not pre-empt Exec's still-open policy question by writing a cohort default into CLAUDE.md.
- 17:29: **Lead Dev** — answers PM's underlying question from evidence, files **#1812**: no principled need exists anywhere in the codebase for a product-owned LLM key (background/scheduled jobs make zero LLM calls; startup only wires a filter onto the client object and never completes; setup validates the key being submitted, paid for by that key).
  - Likely origin identified: `clients.py:675` constructs a module-level `LLMClient` singleton at import time — a client existing before any user does necessarily needs a key belonging to nobody, the pre-BYOC world made structural.
  - 🔴 Same entry: **PM overrides the epic shape** — verbatim, *"reopen epic 2, don't use a successor... the truth is more important than the feeling of progress."* Lead Dev owns the miscall: the successor-epic reasoning optimized for a scoreboard property ("epic 2 stays closed"), not the truer fact that epic 2 was never actually complete when it closed.
- 17:30: **Lead Dev** records PM's ruling in decisions.log: **"THE SERVER KEY IS NOT A REAL CONCEPT AND WILL NOT BE SUPPORTED IN ANY SENSE"** — PM, verbatim: *"I don't understand why anybody should ever be able to spend the operator's money or why the operator even has money to spend… The software that we're building should never be accessing an API for its own purposes."*
  - Writes up a 6-step dependency-ordered plan on #1812 (stop the global write; land CXO's copy as a prerequisite; invert #1809's default; fix Slack inbound; remove #1807's operator flag as a transitional seam; retire the import-time singleton at `clients.py:675`).
- 17:32: **Lead Dev** — PM supplies the underlying business-model principle, verbatim: *"We don't use the business model of reselling tokens or anything like that."*
  - BYOC means every call is the user's, billed to the user's own key; the product has no reason to hold spendable credit at all. Recorded in decisions.log with PM's falsifiable clearing condition attached ("unless someone can describe some sort of minimal bootstrap situation" — burden of proof on the claimant; census found none).
- 17:35: **Lead Dev** — republishes the PM-facing tracker (v106-epic2-reopened, same URL), correcting its stale "EPIC 2: FULLY CLOSED" banner and naming the server-key phantom in PM's own framing.
- 17:48: **Lead Dev** closes #1810, deploys v107 — the cross-user credential write is gone from `setup.py`; red-first captured the actual clobber before the fix.
  - Census of remaining readers reported, deliberately not changed (that's #1809's scope): `get_api_key()` (no user parameter at all), the import-time `LLMClient` singleton, knowledge-graph ingestion's direct global read, the setup wizard's pre-login checks.
  - Two more global-slot writers found and flagged, not fixed: main.py's `keys add` CLI, and `llm_config_service`'s migration helper. Files **#1813** (cross-user isolation tests using hardcoded UUIDs with no teardown, poisoning subsequent runs).

### Phase 5: The Clearing-Bar Discipline (18:34 – 19:22)

- 18:12: **Communications** fire — quiet; notes CXO's copy trap fix as non-editorial context.
- 18:34: **Lead Dev** Fire 5 — 🔴 fixes CXO's live trap himself rather than queuing it: `user_friendly_errors.py:46`'s out-of-quota recovery advice deleted the pointer to a fallback #1807 had just removed; deploys v108 (health 200).
  - Lands CXO's keyless table entry, deliberately weaker/more surface-neutral than Lead Dev's own entry-point copy (a stray raise could come from a background job; a generic handler can't promise "nothing was charged"), and deliberately echoes his phrasing so the two layers read as one product.
- 18:37 (worked 19:08–19:35): **Exec** WORK fire — reports the thread resolved fast: PM ratified the hold, HOST corrected the roster, Arch ruled the fix, Lead Dev deployed v108 (`dff0c50a6` on origin/main).
  - 🔴 But reports the clearing condition has **one step left** rather than collapsing it: what exists is strong (red-first test, two pins driving the real `complete_setup` route with no mocking, 918 tests, ratchets, mypy, smoke) but it is the **test layer**, and PM's condition names a live **setup flow** — "accepting the pin as the observation is precisely the substitution the condition exists to block."
  - Also notes PM asked why 12 epics when they last heard 6 — Exec's own accounting had said 9, so the drift was real and PM caught it first.
- 18:52: **Web** fire — quiet.
- 18:57: **Chief Architect** WORK fire — verifies the fix at trunk directly (greps setup.py at origin/main for all three global-write markers, zero hits) rather than accept the report.
  - **Recommends LIFT with one condition** (require Janne's key setup first, stated in the invite) — but states honestly, in the same memo, that the recommendation is verified only at the source and test layers, not the live layer PM's condition names, and names the alternative (hold for #1809) so PM can choose rather than default.
  - Separately relays to PPM the provenance behind part of the epic-count jump (Arch's own 09-09 cause-factoring), explicitly not pre-empting PPM's answer.
- 19:00: **PA** fire — quiet.
- 19:07: **HOST** Fire 5 — 🔴 **holds the line against Arch's LIFT recommendation.**
  - Verifies Arch's source claim directly (confirms the write is gone from trunk), but states plainly that source-clean isn't the bar PM ratified: the hold should stay until the actual live observation happens — not a multi-day wait, just the specific cheap check PM's own condition calls for.
  - Endorses Arch's onboarding-order idea as genuine defense-in-depth, explicitly as an addition rather than a substitute for the observed-clearing bar. Offers a concrete unblock: Lead Dev runs one live setup flow against v107, HOST clears the roster same-day once confirmed.
- 19:17: **CXO** Fire 5 — takes no position on the #1810 hold itself (no independent evidence, and "adding a voice to a count I can't back is worse than silence").
  - Sends a timed rider: whoever runs the observed setup flow is, in the next breath, a cold first-contact user — closing #1810's clearing bar and CXO's own oldest unobserved FTUX claim (whether the flag is ON in prod and a cold user sees it, unchanged since 09-07) in one act, at zero marginal cost.
  - Three explicit non-claims: not a condition on the hold, drop it if it costs the security observation a minute, not a view on the hold's merits.
- 19:22: **PPM** WORK — **PM overrides epic 12 directly**, verbatim: *"if we discover that there's more work on an epic than we realized and we closed it before discovering that work, then yes we need to reopen the epic... the truth is more important than the feeling of progress."*
  - PPM owns its share of the miscall (protecting "epic 2 is closed" as a page-fact rather than checking if it was true), reopens epic 2, retires epic 12, folds all six items back in.
  - Separately answers PM's direct question of why there are 12 epics with a full honest accounting: the 37-item denominator never grew; three epics (9/10/11) trace to PM's own 09-12 ruling that every MVP item needs an epic home; epic 12 was the one real mistake, now fixed.
  - Gives PM an actual choice (keep 9/10 as-is, or revert to a stricter named list) rather than defending the status quo. Fixes #1812's own board-visibility gap in the same fire.

### Phase 6: Day Close — The Bar Actually Met (21:36 – 22:17)

- 21:36–21:55: **Exec** — PM reviews the internal report and redirects the week's Ship post to lead with product delivery, not self-correction ("finding our own errors is a recurrent theme so not necessarily fresh").
  - Epic-count resolution confirmed landed via PPM's memo.
- 21:42/22:12: **PA** — last scheduled fire, quiet; flags cron `e0cd56b5`'s approaching 7-day expiry (09-16 22:12) for tomorrow's attention rather than discovering it dead the morning after.
- 21:48: **prog** (Lead Dev's dispatch) starts the #1810 clearing-condition observation task — required to drive the real HTTP setup routes end-to-end on a prod-matching backend, not re-derive from the existing unit pins.
- 21:49: **Lead Dev** Fire 6 — 🔴 **Exec declines to call the clearing condition met**, correctly: what existed was a test pin, not a completed setup flow — "the m-43 layer distinction, applied to a gate I'd have been tempted to call satisfied."
  - Lead Dev takes the observation directly rather than leaving it: reads prod read-only via the app's own KeychainService (both global entries absent, no key material printed).
  - Then dispatches the live-harness half with explicit constraints (not against prod, must not consume Janne's minted token, never print key material, clean up and verify by count, state the layer, stop if the flow can't complete).
- 21:49–21:53: **prog** drives a real `main.py` subprocess through the actual HTTP setup routes (`create-user`, `complete`) on a prod-matching credential backend (`PIPER_CREDENTIAL_STORE=db`, matching prod's `EncryptedDBCredentialStore`).
  - Self-catches a zsh `$USERNAME` read-only-special-parameter hazard mid-run (silently bound to the real macOS account) before it could contaminate results, corrects, and re-runs cleanly.
  - Confirms via direct SQL: `per_user_present=True`, `global_present=False` for both providers, exactly 5 rows all user-prefixed, no bare entry. Cleans up to exact baseline; Janne's own invite token untouched throughout.
- 21:52: **Web** STOP — day-close; WYSIWYG toggle discharged, deploy confirmed `success`.
- 21:55: **Lead Dev** — **#1810 clearing condition discharged by observation, both halves** (prod-absent plus live-setup-confirmed-absent, paired deliberately so an absent global can't be mistaken for a failed run).
  - States the layer honestly (not a production setup run — deployed code, prod-matching backend, local server and Postgres). Explicitly does **not** call the hold cleared himself — leaves the decision to Exec and HOST.
- 21:57: **Chief Architect** STOP — 🔴 rules the observed bar **met**, naming the residual (local server/Postgres, not a literal prod signup) immaterial with reasoning (same application logic, same commit, near-zero marginal information from a real account).
  - Names the earlier near-miss on the record: three hours prior, Arch had tried to substitute a softer bar (an onboarding mitigation) for the one Arch itself had set. "The person who sets a bar is the worst-placed person to decide it can be skipped this once."
- 22:07: **HOST** Fire 6 STOP — verifies independently (`gh issue view 1810` → CLOSED; `git merge-base --is-ancestor dff0c50a6 origin/main` confirmed) rather than accept the summary.
  - **Lifts the hold**, updates the roster with the full evidentiary chain, both prior statuses kept struck through rather than erased so the claim history stays visible.
  - Carries Arch's onboarding-order condition forward as additive defense-in-depth against the still-open #1809, not a substitute for the bar that was met.
- 22:12: **Communications** STOP — day close; quiet Monday throughout, nothing editorial to action, sign-off verified clean in both repos.
- 22:17: **CXO** STOP — 🔴 catches one line in Lead Dev's closing memo that overclaimed: *"CXO's rider is satisfied by the same run."*
  - Checks before agreeing (greps the issue's comments for FTUX-related terms) and finds it wasn't — the observed run captured setup, not the first chat turn after it; zero hits.
  - Separately identifies that Lead Dev's own honest layer-naming (not a production setup run) is what revealed even a screenshot of that turn would not have closed CXO's actual, narrower open claim (the flag is ON in prod and a cold user sees it) — leaves the row open rather than let Janne's real onboarding be instrumented for verification purposes, deferring that call to HOST if HOST judges it appropriate as part of normal onboarding care.

---

## Executive Summary

### Core Themes

- A cohort-wide false alarm ("seven roles dark") self-corrected within ~2.5 hours to its real cause — a Fable 5 model-tier usage ceiling exhausted by one seat's weekend subagent fan-out, paid for by two seats that dispatched nothing.
- A live security-exposure chain (#1807 → #1809 → #1810 → #1812) ran end-to-end in a single day: discovered, escalated to PM's top priority, fixed, found to be worse than first thought, ruled at the architecture level, and closed under a deliberately contested clearing bar.
- PM issued two direction-reshaping rulings in real time: reversing PPM's newly-created successor epic in favor of reopening epic 2 ("the truth is more important than the feeling of progress"), and ruling that the product-owned "server key" concept does not exist and will not be supported in any sense.
- Multiple roles caught and corrected their own claims in-session rather than let them stand: CXO's ordering-dependent false positive and its own seven-day-old FTUX copy defect, Arch's one-sided DocumentDB census and its own attempted bar-softening, Exec's cadence-blind escalation, Lead Dev's overclaim about CXO's rider being satisfied.
- The day's clearing-bar discipline (Exec and HOST refusing to accept "the fix is described" in place of "the fix is observed running") closed exactly as the cohort's own m-49 principle demands, on a case — a real external tester's credentials — where it genuinely mattered.

### Technical Details

- **#1777** (agenda-response crash on a `None` todo sentinel): closed, deployed v104.
  - Sweep found mypy's existing gate already reported every drift site; the real fix was scoping the #1436 ratchet (filed **#1800**), not per-site discipline — eight prior issues each guarded what they touched and this crash still happened four lines below a comment describing it.
- **#1792** (blacklist outage falsely reporting "Token has been revoked"): closed, deployed v105.
  - Reproduce-first found a second, uncited fail-closed site (`_check_database`) that the issue's own repro actually exercised; new `BlacklistUnavailable` exception raised at both store sites, surfaced as honest 503s at every refusal surface instead of 401s.
- **#1802** (bare `TestClient` survives only one authenticated request): fixed via `session_scope_fresh()` (the DB-side twin of #1452's Redis same-loop guard).
  - Discovered `TokenBlacklist.initialize()` is never called anywhere in the running app — filed as **#1808**; also fixed the identical masking-mock gap in two sibling tests that had silently stopped exercising their failure paths.
- **#1788** (DocumentDB dead-code classification): re-ruled cat (2) after Arch conceded a one-sided census (measured only the live DB-side importer, missed the dead domain twin).
  - "Liveness must be measured on both sides" adopted into the ruling itself. PM-056 job 2 now checker-clean, down from 13 issues across 7 models.
- **#1807** (PM's top priority — authenticated-but-keyless callers spending the server's LLM key): closed, deployed v106.
  - New `LLMKeyRequiredError`/`UserLLMKeyRequiredError` family; operator-only server-key path gated behind an explicit, default-off `PIPER_OPERATOR_SERVER_KEY` flag with fail-closed wiring.
  - 37 new tests + 6 no-regress; four pre-existing assertions found to have pinned the hole as intended behavior, amended with inline notes.
- **#1810** (setup flow double-writing every user's key into a global, last-writer-wins slot): ruled by Arch (no legitimate consumer, delete the write), closed, deployed v107, then v108.
  - Clearing condition required a live observed setup flow, not a test pin — delivered by direct HTTP-route testing against a prod-matching backend, corroborated at the storage layer (exactly 5 rows, all user-prefixed).
- **#1812** (should the product own any LLM key at all): PM ruled no — "the server key is not a real concept and will not be supported in any sense."
  - Recorded verbatim in `docs/internal/architecture/decisions/decisions.log` (entries 15:57 PT, 16:4x PT ×2, 17:30 PT) with a falsifiable clearing condition ("unless someone can describe some sort of minimal bootstrap situation").
- Web shipped a Source/Split/Preview body-editing toggle for the admin composer (website `bb579b5`), preserving caret and scroll position across an unmounting textarea via `onSelect`/`onScroll` capture and a pre-paint `useLayoutEffect` restore.
  - The quality-banked item discharged in its named trigger session, browser-verified against a live 7157-char draft on an isolated temp product root.

### Impact Measurement

- Issues closed today (sampled from logs): #1777, #1792, #1802, #1788, #1785, #1807, #1810, #1801 (weekly docs audit).
- Issues filed: #1800, #1799, #1808, #1811, #1809, #1812, #1813, plus Docs' #1803–#1806.
- MVP board moved from 51 → 54 not-done over the day, tracking active discovery and triage rather than net stagnation; unmilestoned count spiked to 7 mid-day and returned to 0 by evening.
- Epic count: created (epic 12), then retired same day on PM's ruling; net epics 6 → 11 (up from PM's last-known 6), with the growth traced honestly to cause-based re-partitioning plus two genuine new-discovery epics, not scope invention.
- Four deploys shipped in sequence to close the security chain: v104, v105, v106, v107, v108 — all health-checked 200 post-deploy.
- Docs' Weekly Audit found GitHub issue hygiene holding fleet-wide (0 of 336 open issues without a milestone, confirming PM's 09-12 filing-convention ruling holds) but doc staleness worsening (216/336 issues stale >30 days, up from 168/322 the prior week); 75 pattern files matched the README exactly, 0 broken ADR links.
- Exec's concentration analysis: 1,257 commits in the measurement window, 205 via mail (16%), 48 subagent dispatches (30 on Saturday alone) against 10 in the preceding nine days — the dispatch line, not the seat line, carried the real concentration.

### Session Learnings

- **HOST's own end-of-day framing captures the day's shape better than any single event does**: "a false alarm caught and corrected by its own author within two hours, one resource externality traced to a root cause and fixed at the behavioral level, and one real credential-safety incident that ran its full course — found, held, verified, and closed."
- **"Silence is not a diagnosis."** Three distinct causes produced identical belt silence in four days (a signed-out session, a sustained classifier outage, and today's model-tier ceiling) — the remedies differ per cause even though the symptom looks the same; now catalogued durably in `duty-cycle-freeze-check.sh`'s own header.
- **A dispatcher's model tier is inherited by its fan-out by default, invisibly.** Lead Dev's 48 weekend subagent dispatches silently spent a shared account-level ceiling that two uninvolved seats then paid for.
  - The fix adopted was explicit per-dispatch model pinning, not "dispatch less" — CIO and Lead Dev both separately checked and disclosed their own exposure rather than treating it as someone else's incident.
- **A check's position in its specified sequence is part of the check** — CXO's self-verify reported a false positive purely from running before the heartbeat it depends on existed, in a form that would have been easy to report outward as a real finding.
- **"Described is not running" (m-49) needs an enforced observation, not a good-faith report** — the #1810 clearing bar was deliberately written to require a live setup flow.
  - Exec and HOST both declined easier substitutions (a test pin, a source-level LIFT recommendation) that would have technically closed the ticket faster.
- **The person who sets a bar is the worst-placed person to decide it can be skipped** — Arch named this about its own conduct three hours after doing it, on the record, rather than let the near-miss go unremarked: "the reasoning that justifies the exception is the same reasoning that would have set a lower bar originally, and it arrives feeling like pragmatism."
- **Optimizing for "the record stays clean" is a different goal than optimizing for truth**, and both Lead Dev and PPM separately owned exactly this mistake in the epic-12 reversal: protecting "epic 2 is closed" as a page-fact rather than asking whether it was actually true.
- **A correct-looking comment can hide a defect for an entire security epic** — #1810's global write carried a plausible-sounding justification ("so LLMClient can find keys during server startup") that Arch had to trace, not just read, to find had no actual consumer.
- **Even a closing memo can overclaim, and the discipline holds when someone checks it anyway** — CXO corrected Lead Dev's "satisfied by the same run" claim about its own unrelated tracker row at 22:17, the last substantive act of the day, rather than let a convenient-sounding closure stand unverified.

---

## Sources

All 17 source session logs for 2026-09-14 were read in full:

- `dev/2026/09/14/2026-09-14-0629-lead-code-log.md` (Lead Dev)
- `dev/2026/09/14/2026-09-14-0630-prog-code-log.md` (prog — #1777 sweep)
- `dev/2026/09/14/2026-09-14-0642-comms-code-log.md` (Communications)
- `dev/2026/09/14/2026-09-14-0700-pa-code-log.md` (Piper Alpha)
- `dev/2026/09/14/2026-09-14-0707-host-code-log.md` (HOST)
- `dev/2026/09/14/2026-09-14-0708-exec-code-log.md` (Chief of Staff/Exec)
- `dev/2026/09/14/2026-09-14-0717-cxo-code-log.md` (CXO)
- `dev/2026/09/14/2026-09-14-0722-ppm-code-log.md` (PPM)
- `dev/2026/09/14/2026-09-14-0727-docs-code-log.md` (Documentation Management)
- `dev/2026/09/14/2026-09-14-0932-arch-code-log.md` (Chief Architect)
- `dev/2026/09/14/2026-09-14-0932-web-code-log.md` (Web)
- `dev/2026/09/14/2026-09-14-0935-prog-code-log.md` (prog — #1792 fix)
- `dev/2026/09/14/2026-09-14-1037-cio-code-log.md` (CIO)
- `dev/2026/09/14/2026-09-14-1256-prog-code-log.md` (prog — #1802 fix)
- `dev/2026/09/14/2026-09-14-1305-prog-code-log.md` (prog — #1807 fix)
- `dev/2026/09/14/2026-09-14-1730-prog-code-log.md` (prog — #1810 global-write removal)
- `dev/2026/09/14/2026-09-14-2148-prog-code-log.md` (prog — #1810 clearing-condition observation)

**Cross-reference gate (Step 2.5)**: no cohort role (Lead Dev, Docs, Chief Architect, Chief of Staff/Exec, HOST, Communications, CXO, CIO, PPM, PA, Web) was mentioned by name in any source log without also having its own log in this source set. All five `prog` sessions were confirmed via worktree/branch (`piper-morgan-worktrees/lead`, `claude/lead-cycle`) and issue-number alignment against Lead Dev's own log as Lead Dev's dispatches, not independent agent sessions. Cross-project agents mentioned (Janus, Pard) are correctly excluded from this gate per instruction.

**Cross-role mentions verification (Step 2.6)**: the two highest-stakes cross-role claims were checked against their referenced logs and found consistent: Arch's #1810 ruling (decisions.log, 15:57 PT) matches Lead Dev's, HOST's, and Exec's independent accounts of the same event; Lead Dev's closing claim that "CXO's rider is satisfied by the same run" was checked by CXO itself at 22:17 and found **not** consistent with the evidence (no FTUX-turn observation exists in the #1810 issue thread) — this discrepancy is preserved in the Phase 6 timeline rather than resolved in either direction, since CXO's own correction is the record of it.

**Canonical references (Step 7)**: no PDR, ADR, Pattern, or methodology document was newly ratified today. The consequential rulings quoted in this omnibus (the #1810 architecture ruling, the PM server-key deletion ruling, and its business-model rationale) are quoted verbatim from `docs/internal/architecture/decisions/decisions.log` (entries timestamped 2026-09-14 15:57 PT, 16:4x PT, and 17:30 PT), not paraphrased from any session log's summary of them.

**No same-day `dev/active/` artifacts** were found outside the session logs themselves (`find dev/active/ -maxdepth 1 -name "*2026-09-14*" -type f` returned empty).
