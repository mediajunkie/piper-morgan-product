# Alpha promotion standing grant

**In force since 2026-10-16.** xian confirmed it ("Yes. I confirm the promotion grant.", via Janus; CIO received it at 08:10 PT). It succeeds decisions.log 2026-10-14 17:31, which made every promotion a dispatch on his explicit word. Record: decisions.log 2026-10-16. Text: Exec's draft with CIO's five changes and Lead's migration line, accepted by Exec, Lead and CIO, and shown to xian on Janus's card v368. Owner of this page: CIO, as the record. Lead holds Step 0 and dispatches.

## The grant, as confirmed

> **Alpha promotion standing grant.** The seat holding Step 0 (Lead; one dispatcher only, no one else dispatches) may promote to alpha without asking me, when all of these hold:
>
> 1. **Step 0 is READY.**
>    - Tests succeeded on the exact sha staging serves, or on its nearest tested ancestor when only untested paths changed since (what the promote gate itself accepts).
>    - `scripts/main-ci-status.sh` shows every gating workflow green.
>    - The promote gate accepts the build.
>    - No fly-deploy run is queued or in progress.
>    - `git diff --name-only <sha alpha /health reports> <sha staging serves> -- alembic/versions` lists nothing. If it lists anything, ask me, with the scratch-database round-trip and Arch's read attached.
> 2. **No hold is on.** That means no freeze (a history rewrite or a cohort freeze), no "hold promotions" from me, no open served-check failure on staging, and no NOTICE memo from PPM, CXO or Arch that names the build or an issue in it as held. It also means alpha's own `/health` reads `status: healthy`. The promote step refuses otherwise, including a body with no `status`; a forward fix under "If it goes wrong" goes with `quiet_override=true` on my word. *(2026-10-21: added after the 11:25 dispatch went out while alpha's database was unreachable (#2124); the step refused it only through an unrelated reader bug. CIO's proposal 11:37, built by Lead at 97f4dbda1d.)*
> 3. **Not while I'm testing alpha, nor into design partners' chats.**
>    - If a test session on alpha is announced as in progress (me, PA or Web on the test card), wait for it to end.
>    - **From Fri 2026-10-23, while design partners are invited:** a promotion waits until `services.chat_turns_last_30m.quiet` on alpha's `/health` is `true` (no account had a chat turn in the last 30 minutes, and no record attempt failed in that window), at any hour inside condition 4's. The promote step refuses on `quiet: false`, on `record_failed_in_window: true`, on `{"error": "unavailable"}`, and on an alpha it can't reach. /health serves no counts, since it is public; the counts go to the server log. The count restarts at zero whenever alpha restarts, and every promotion restarts it, so a promotion also waits until alpha has been up 30 minutes (`services.uptime_seconds` ≥ 1800 on the same `/health`). The promote step refuses on either reading; a build that doesn't serve a field falls back to the dispatcher reading it by hand. If alpha ever serves a build without the field, only 20:00-21:00 Pacific applies.
>    - A must-close fix may go outside this on my word, as on 10-20: dispatched with `quiet_override=true`.
>    - *(2026-10-20: xian delegated the window to Exec, PPM and CXO, since partners are spread worldwide and no single hour is quiet (relayed by Exec 17:42). Exec's proposal of 17:42, agreed by CXO 17:43 and PPM 17:45. decisions.log 2026-10-20 17:45 (exec). 2026-10-21: the count is served on alpha from 8e61423f1a (Lead, 07:35), and the promote step "Alpha must be quiet" refuses above zero, so the 20:00-21:00 window gave way to it before the partner window opened. The 30-minute wait after a restart is CIO's reading of Lead's stated limit: a restart resets the count; PPM raised no objection (08:04). `uptime_seconds` served from 95dea16f50 (08:14); the step's first served verdict was "Alpha is quiet: 0 accounts" on run 39623185812. The step holds the uptime wait from 8cdd2afbeb (Lead, 08:16), always on, with no partner-day input. Arch's review (09:27) found two fail-opens, both closed (52333d4bbc). The boolean shape replaced the counts at CIO's call (10:08) and is in the step from d09b7e0d86, served on alpha from the next promotion after b28d46a97f.)*
> 4. **Hours and spacing.** Between 07:00 and 21:00 Pacific, so someone is awake to see the result. No daily count: after a promotion, the next one waits until the Alpha Health Watch (`.github/workflows/alpha-health-watch.yml`) has run green once on it, so a break is pinned to one build before another lands on top. *(2026-10-20: replaced "at most two promotions a day". xian via Janus, relayed 11:08: "In this pre-beta period I am comfortable with a readiness based process and no limit to number of deploys per se." On CIO's recommendation of 10:54; the cap's original reason, CIO's 10-16 draft, had gone stale: it was used up every day 10-17 to 10-20 and held the #2101 fix. decisions.log 2026-10-20.)*
> 5. **What still needs my yes.** A build with a new database migration (see 1), or any change to production, beta or secrets. The grant covers alpha only.
>
> **After each promotion**, the seat:
> - logs the run id and sha;
> - confirms alpha's /health shows the new sha and its body `status` reads `healthy` (since #2083 the body carries `services.database`; a `degraded` body with the right sha means the image is live but the database is not answering, which is "If it goes wrong", not a promotion to report as done);
> - mails Web per the 10-14 procedure;
> - tells Exec.
>
> Exec puts one line on my board ("alpha moved to X at T"), so I learn after the fact instead of approving before.
>
> **If it goes wrong:** the fix goes forward through main, or a revert on main that staging redeploys and Tests passes, followed by one promotion under this grant. Then it stops, and the seat tells me.
>
> **A dispatch that leaves alpha unchanged is not a promotion and has not gone wrong.** That means alpha's /health still shows the previous sha, healthy, whether the gate refused it or Fly failed before the deploy. It isn't a promotion for the spacing rule. The seat fixes the cause or waits out the outage, then may dispatch again within the grant's hours, and mentions it in its line to Exec. *(2026-10-16: added at 11:44 as a gate-refusal-only line, confirmed by xian via Janus after a 10:51 gate refusal was read as the grant's stop; that reading came from wording in CIO's superseded first draft. Widened at 15:04 to any dispatch that leaves alpha unchanged, xian via Exec ("Yes, wider-version of grant is acceptable."), after Lead's 11:33 dispatch failed at Fly's image query during Fly's partial outage. A deploy that half-applied, leaving alpha changed or unhealthy, still falls under "If it goes wrong".)*
>
> **To stop it:** I say "hold promotions" to any seat, and it holds until I lift it. Any promotion I later say I would have refused ends the grant until I renew it.

## Why these conditions

- **Why a grant:** xian had approved every promotion request. A yes that never fails guards nothing (m-44's boundary: a gate that can only pass), so the grant keeps only what the Tests gate doesn't cover, which is migrations and timing.
- **Why no count (10-20):** a count holds back fixes as readily as features, and it batches changes so a break is harder to pin to one build. Each promotion already passes the Tests gate and reaches xian's board as "alpha moved to X at T". The spacing rule keeps one build per health-watch window. The watch checks liveness and the database only, not behaviour; served checks and testers cover that, as they did under the cap.
- **Expected next shape, not a rule (xian, 10-20):** "Once we enter beta and start to have users active on hosted system we'll probably move to something like nightly deploys from staging to production but will continue to allow relative free deployment to staging." Recorded as a direction to revisit at beta, not as a condition.
- **Why a partner window (10-20):** nobody has tested what a deploy does to a person's open chat (CXO, 12:32). A turn that fails mid-deploy reads to a partner as Piper being broken. No seat can see when a partner is online, and Rule 8 keeps partner names out of this repo, so the rule uses a fixed hour and then a name-free count, never a session list.
- **Open:** Web's staging row (does a deploy drop an open chat, and what the person sees) has not run. Its result goes to PPM and CXO, who decide whether condition 3's partner line can loosen. The invitation's restart line is CXO's and stays a draft until that row runs.
- **Migrations:** alpha runs `alembic upgrade head` on every release (`fly.toml`, app `piper-morgan`), and a migration is the one change a forward fix can't undo.
- **No rollback by sha:** the promote job copies the image staging runs now, and `workflow_dispatch` has no sha input (`.github/workflows/fly-deploy.yml`). That is why "if it goes wrong" says forward or revert.
- **Permission (corrected 2026-10-29):** this held while Lead's seat ran in bypass mode (the 10-15 15:31 dispatch). The seat now runs in auto mode, and the reviewer refused the dispatch on 10-28. The fix is one exact allow line on Lead's seat, added by xian: `prod-command-permissions.md` §2026-10-29. **Applied 2026-11-03** (decisions.log 17:36): xian ran `seat-permissions.py --apply --seat lead` (+allow 1, +deny 0), and Exec confirmed the line in Lead's `settings.local.json`. **The reviewer honours it (verified 2026-11-03):** Lead dispatched twice with no refusal. Both runs succeeded: run 41760826169 at 18:27 PT, which Lead reported at 18:32 as "worked first time, no refusal", and run 41770597383 at 20:01. CIO's 22:08 read of alpha's `/health` was healthy. The `alpha` GitHub environment has no required reviewers, only a branch policy.

## Procedure notes (do not change the grant's text)

- **"The sha staging serves" is read from staging's own `/health`**, never from the newest push in the fly-deploy run list. When Tests is red, the known-broken guard skips staging deploys, so staging can lag the run list by several pushes. On 10-16 10:51 a dispatch picked the run list's sha and the promote gate refused it (Tests on 0e30760c79 = failure; alpha untouched). Recipe corrected in `canonical-ops-recipes.md` (Lead, 6a91d56ec5).
- **Condition 2 covers a box that can't store keys (2026-10-22, CIO).** Since #2125 (Lead, `4fca5b1e9b`, `fd32d0febe`; served from the next promotion), `/health` serves `services.credential_store`, and `unavailable` degrades the body `status`, so the promote step's not-healthy refusal already covers it. No new wording: condition 2 already asks for `status: healthy`. A hosted box with no encryption key (`FLY_APP_NAME` set, no variable) now reads `unavailable` too and degrades (Lead, 48d06e12bd on main at fbd0206444, 10-22, Arch's point 3); scoped subkeys read healthy, a local box `not_configured`. Condition 2 covers it with no new wording.
- **A hold is a file, and the promote step refuses while it exists (2026-10-23, CIO).** On 10-23 a promotion landed inside the #2085 test-2 hold, which existed only in mail. Since `1f795adff1` (Lead; Arch's conditions), the promote job's first gate refuses while `ops/alpha-hold.md` exists on `origin/main`, read from main whatever branch dispatched it, and refuses if main can't be resolved. It prints the file, so the refusal names the holder. There is no override input; clearing a hold means removing the file. How to call and clear one: `ops/README.md`. This is condition 1's "xian's word" made visible, so the grant's text doesn't change. Validated by the pin test (5 passed); Arch's three real dispatches (hold from main, hold from another branch, no hold) wait for test 2's end and xian's word.
- **A second hold file stops promotions only (2026-11-20, CIO; Arch's written approval as a stricter-only change, mail 01M7Y8836V).** The promote job's first gate also refuses while `ops/promote-hold.md` exists on `origin/main`. The health watch does not read that file, so #2146's automatic database recovery stays on. Use it for a wording or review hold; use `ops/alpha-hold.md` when a deliberate stop must not be undone. The pre-check reads both. How to call and clear one: `ops/README.md`. The grant's text doesn't change.
- **A late green leaves staging on an older red sha; the remedy is a re-run, not a code push (2026-11-02, Lead).** The staging deploy's health gate reads the newest completed Tests verdict on main at deploy time. On 11-02 a one-line backlog push (`dfa3363d5b`) deployed while the previous sha's Tests were still red, so staging kept serving `fc31f4a` and the promote gate refused on the served sha. `gh run rerun <the push's Fly deploy run id>` after that push's own Tests went green re-ran the staging job against the green verdict and staging served `dfa3363d5b` four minutes later (run 41556514319 attempt 2). No `fly`, no `workflow_dispatch`, nothing on the deploy path changes.

- **Arch's part in a promotion, as practised (written 2026-11-27, Arch, at CIO's request; the grant's text doesn't change).** Alpha has redirected to beta since 11-05 (#2282), so "alpha" in the grant means beta. There are two Arch steps, and neither is a condition the dispatching seat waits on:
  1. **Before a change lands on main:** Arch reads the change's branch from source and records "conforms", or the conditions, in decisions.log. This is the ordinary landing rule, not a promotion step.
  2. **After a promotion:** Arch reads beta's `/health` `git_sha`, checks with `git merge-base --is-ancestor` that the commits Arch read are in it, checks that the served paths (`services/`, `web/`, `templates/`) don't differ from the read commits, and records "Promotion <sha> conforms" in decisions.log. A mismatch goes to Lead and Exec the same hour. It is a validation after the fact, not a gate.
  - **What it doesn't cover:** a migration or a deploy-path change is outside the grant and needs xian's word, as the grant says. Arch's read does not stand in for it.
  - **The 11-13 to 11-17 exception, kept for the record:** five decisions.log lines read "PROMOTION GRANTED" (11-13 16:13, 11-14 12:55, 11-17 07:53 and 09:53, plus the 08:27 conforms). Each lifted Arch's own temporary promotion hold, set during PA's reads for #2342 (Lead's 11-12 log: "his promotion hold lifted for one promotion, between PA's reads"), for one commit. That is condition 2 ("no NOTICE memo from PPM, CXO or Arch that names the build ... as held") working as written, not a separate layer. *(Corrected the same day: this line first said a one-per-day pacing, which was Arch's misreading; CIO 01M8F42S56 had it right.)* No such per-promotion grant has been given or needed since 11-17.
  - **Also true in practice (Lead, 11-27):** the window is 07:00 to 21:00 PT, and Lead does not dispatch during a xian sitting. Exec's "xian has not started (a)" line is how Lead knows.

- **Tests runs on main queue, so a late served push can cost the evening promotion (2026-11-27, CIO, after Lead's 11-26 20:22 landing).**
  - `test.yml` cancels superseded runs on pull requests only. A push to main waits behind every Tests run already queued or running, and the promote gate needs Tests green on the sha staging serves.
  - On 11-26, Lead landed the flip at 20:22 behind two runs. Its verdict was due at about 21:10, past the 21:00 limit, so the pleasantry skip waited until the morning.
  - Before a served push on a day when a promotion is still planned, run `scripts/tests-queue-eta.sh`. It is read-only and prints the runs ahead and an estimated verdict time. Exit 1 means after 20:50 PT, so promote first, then push.
  - The median green Tests run on main was 24 minutes over the last 40 runs, read 11-27.
  - **Every seat's push counts, not only the dispatcher's (11-27, Lead 01M8F8NHGZ).** The promote gate takes the nearest tested ancestor of what staging serves. So any push to a tested path (`scripts/`, `tests/`, `services/`, `web/`, `templates/`, `cli/`, `.github/workflows/`) moves staging and puts a new Tests run in front of a waiting promotion. On 11-27, promotion 4 waited behind two `scripts/` pushes, one of them this check's own. **While the dispatching seat has announced that a promotion is waiting, every seat holds tested-path pushes until its "beta moved" mail.** Logs, mail and docs are fine, because they don't start a gating run.

**Review:** 2026-12-29 (renewed 2026-11-27; see the outcome below the 28-day review), or after a promotion that leaves beta serving neither the promoted build nor the one before it, whichever comes first. A refusal by a condition is not a trigger. *(Replaced 2026-11-03 on xian's word, decisions.log 2026-11-03 17:30, from CIO's 10-30 review below. The first line, "after 14 days (2026-10-30) or after the first failed promotion", was met on 10-16 by a refusal and so couldn't tell the grant working from a deploy failure.)*

### 14-day review (CIO, 2026-10-30, STOP fire)

**Record, 10-16 to 10-30:** 67 promotion dispatches (`fly-deploy.yml`, `workflow_dispatch`), 51 promoted and 16 failed in `promote-alpha`. By the failing step:
- **7 were the gate refusing, as designed:** Tests not green on the served sha 4 times (10-16, 10-20, 10-23, 10-24), alpha not quiet once (10-21), the hold file once (10-23, the day the file gate landed), and the staging read once (10-23).
- **8 broke at the deploy step:** the promote step 5 times (10-16, 10-19, 10-24 twice, 10-29), the registry copy twice (10-26), and the flyctl setup once (10-29, the 0.5.0 upgrade). Each was followed by a successful promotion: within 35 minutes for 4 (10-24 twice, 10-29 twice), after about 4 to 5.5 hours for 2 (10-16, 10-19), and after about 12.5 hours for the 10-26 pair.
- **1 I couldn't classify** (10-23 18:13): no step reports failure.

**Findings:**
1. **The conditions did their job.** Every refusal stopped at a named condition, and the hold-file gate refused on its first day.
2. **The review trigger was missed.** "After the first failed promotion" was met on 10-16 at 18:33, the grant's first day, and nobody treated it as a review. The amendments above (10-22, 10-23, 10-29) were made incident by incident instead. The trigger as written also can't tell a refusal (the grant working) from a deploy failure.
3. **Deploy-step failures are the real risk, and they left alpha recoverable.** I didn't verify served state for each of the 8. "A successful promotion followed" is the evidence, not a `/health` read at the time.

**Recommendation to xian, via Exec:** keep the grant as it stands. Replace the review line with: *"Review: 2026-11-27, or after a promotion that leaves alpha serving neither the promoted build nor the one before it, whichever comes first. A refusal by a condition is not a trigger."* Whether to renew is xian's call. Until then the grant runs as is, under Exec's promotion freeze until the letters go.

**Outcome (2026-11-03 17:30, xian in session, via Exec):** the grant is kept, and the review line above is replaced as recommended (decisions.log 2026-11-03 17:30).

### 28-day review (CIO, 2026-11-27, START fire; standing row 9k)

**Record, 10-30 to 11-27 10:07 PT:** 103 dispatches of `fly-deploy.yml` by `workflow_dispatch`.
- **93 promoted.** In 94 runs the workflow succeeded; `promote-alpha` succeeded in 93 of them and was skipped in 1.
- **7 refused at a named condition, as designed:**
  - 6 times, Tests not green on the served code: 11-03, 11-05, 11-08, 11-13, 11-16, 11-23.
  - Once, alpha not quiet: 11-04.
- **2 broke at the deploy step.** Neither left alpha serving a third build, so neither met the early-review trigger:
  - **11-06 23:26** (run 42311939348): Fly's release-command machine failed to start, and the deployment aborted. Lead logged "alpha untouched".
  - **11-08 08:40 PT** (run 42501163035): a Fly machines-API stream error came after the machine had updated, so the verify step was skipped. Lead verified by hand that beta's `/health` read the promoted `7f9aa353fa`, healthy, 5 times, and did not re-dispatch.

**Findings:**
1. **The conditions did their job.** Every refusal stopped at a named condition. Most were the Tests condition.
2. **Deploy-step failures fell from 8 in 14 days to 2 in 28 days.** Both left a known build serving.
3. **This page no longer describes how promotions are given.**
   - Since 11-05, alpha 301s to beta (#2282), but the page still says alpha.
   - Since 11-13, each promotion has also carried a per-promotion grant from Arch in decisions.log. The first was 11-13 16:13 ("Granted for 81d149ac86, this commit only"). Lead's 11-13 log reads "the next promotion needs his word again".
   - xian's 11-26 rulings speak of "the standing grant with Arch validating and HOST reading".
   - None of that is written here. I have not found where the Arch layer was set or by whom. Unverified: I searched decisions.log for 11-06 to 11-13 and Lead's 11-13 log.
4. **No case of "a promotion I would have refused" was found.** I searched decisions.log only, not every card, so this is not an exhaustive check.

**Recommendation to xian, via Exec:**
- Keep the grant.
- Arch states the per-promotion layer, as he applies it, as a procedure note on this page, so the page says what a dispatch actually needs. The grant's text doesn't change.
- The page's own text renames alpha to beta where it means the hosted app. The app and workflow names stay `piper-morgan` and `promote-alpha`, because those are their real names.
- Next review: 2026-12-29, beside the methodology audit, or earlier if a promotion leaves beta serving neither the promoted build nor the one before it. A refusal by a condition is not a trigger.

Whether to renew is xian's call. Until he answers, the grant runs as is.

Verified how:
- **Dispatches:** `gh run list --workflow fly-deploy.yml --event workflow_dispatch --created ">=2026-10-30"` (103 runs). `gh run view` on each failure gave the failing step. `promote-alpha`'s conclusion was read on each of the 94 successful runs.
- **What the two deploy failures left serving:** Lead's 11-06 and 11-08 logs, as recorded on their days, not re-measured.
- **Health watch, 11-06 to 11-09:** 20 runs, 20 green.
- **Layer:** GitHub Actions records plus logs.
- **Denominator:** every dispatch in the window.

**Correction to finding 3 (CIO, 2026-11-27, after Lead 01M8F3P2J6 and Arch 01M8F3X402):**
- **The per-promotion grants were not a standing layer.** They were five "PROMOTION GRANTED" lines, 11-13 to 11-17. Each lifted Arch's temporary promotion hold for one promotion, during the reads for 2342. Lead's 11-12 log: "his promotion hold lifted for one promotion, between PA's reads".
- **That is condition 2 working.** A hold named by Arch stops promotions, so no gap in the grant follows from it.
- **None has been given or needed since 11-17.** Arch's part now is a read of each change before it lands and a validation after each promotion. Neither is a gate. He wrote it as the procedure note above.
- **Not traced:** where the hold was first called. It isn't in decisions.log, so it was probably in mail.

**One textual point the renewal should settle (xian's words, not mine to change):** condition 5 says "any change to production, beta or secrets" needs his yes, and "The grant covers alpha only". Since 11-05 the app the grant promotes to is served as beta. Practice since then, and xian's 11-26 rulings ("under the standing grant"), read the grant as covering that app. The renewal should say so in his words.

**Outcome (2026-11-27 11:36, xian in conversation, via Exec 01M8F85S17):** "Yes, please let Lead proceed with pushing to beta." The grant continues. It covers the app served as beta (condition 5's "alpha only" reads as that app), and the next review is 2026-12-29, or sooner after a promotion that leaves beta serving neither the promoted build nor the one before it. Record: decisions.log 2026-11-27 11:36. A hold in force now: Exec's "no promotion until I say he's clear" during the GitHub move (same mail), under condition 2.
