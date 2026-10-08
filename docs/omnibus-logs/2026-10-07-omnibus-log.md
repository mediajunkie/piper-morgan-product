# Omnibus Log: October 7, 2026

**Day**: Wednesday
**Sessions**: 12 role sessions (Documentation Management, Unicorn Web Designer, Communications Director,
Head of Sapient Trust, Chief Architect, Principal Product Manager, Lead Developer, Piper Alpha, Chief of
Staff, Chief Experience Officer, Special Assignments, Chief Innovation Officer), plus 4 Coding Agent
sub-session logs (16 files in all). Lead dispatched 5 Sonnet subagents during the day.
**Day Type**: HIGH-COMPLEXITY: INTEGRATION — the day alpha was promoted for the first time through the
promote workflow (after three fixes to it), the router-decided armed turn (#1886) was ruled, corrected
by a live probe, and landed, and the beta invitation, support page and known-issues text moved from
drafts to live pages
**Justification**: Twelve role sessions and at least nine threads that crossed three or more roles: the
promote-to-alpha chain (PM ↔ Lead ↔ Pard ↔ Exec), the #1886 armed-turn ruling and its correction
(Lead ↔ Arch ↔ CXO ↔ PM), the clear-family and delete-targets build (Lead ↔ CXO ↔ Arch), the #1956 CI
reshape (Docs → Exec → PPM → Lead), the beta invitation and known-issues arc (Comms ↔ Web ↔ PPM ↔ CXO ↔
PM), the live re-test of rows A, C and D (Lead ↔ Web ↔ PM), the persistence delete (#1522: Arch → Lead
→ PM's production read → Exec), the red main on a mypy ceiling (Docs → Lead), and Spec's cross-pollination
corpus proposal (PM ↔ Spec ↔ Janus). Several agents recorded a self-correction (Lead, Arch, Comms and PPM among
them), and PM gave direct go-aheads in conversation more than once.
**Git Commits**: 439 on origin/main (00:00–24:00 PDT). Verified this session with
`TZ=America/Los_Angeles git log origin/main --since="2026-10-07 00:00:00" --until="2026-10-08 00:00:00" --oneline | wc -l`
during the 10-08 04:12 fire, after `git fetch origin main`. 222 of the 439 are not heartbeat
(`hb`, `hb-last-invoked`) or `mail(` subjects. This is an increase from 365 on 10-06 (per that day's
omnibus).

---

## Sources

Session logs (all in `dev/2026/10/07/`):
- `2026-10-07-0412-docs-code-log.md` (Docs, 100 lines)
- `2026-10-07-0618-web-code-log.md` (Web, 129)
- `2026-10-07-0619-comms-code-log.md` (Comms, 49)
- `2026-10-07-0623-lead-code-log.md` (Lead, 209)
- `2026-10-07-0626-host-code-log.md` (HOST, 45)
- `2026-10-07-0627-arch-code-log.md` (Arch, 67)
- `2026-10-07-0633-ppm-code-log.md` (PPM, 97)
- `2026-10-07-0647-pa-code-log.md` (PA, 40)
- `2026-10-07-0707-prog-code-1886-log.md` (Coding Agent, #1886 carrier, 276)
- `2026-10-07-0708-exec-code-log.md` (Exec, 82)
- `2026-10-07-0717-cxo-code-log.md` (CXO, 76)
- `2026-10-07-0750-spec-code-log.md` (Spec, 42)
- `2026-10-07-0941-prog-code-delete-targets-log.md` (Coding Agent, delete targets, 227)
- `2026-10-07-1007-cio-code-log.md` (CIO, 48)
- `2026-10-07-1259-prog-code-1886b-log.md` (Coding Agent, #1886 router consult, 197)
- `2026-10-07-1831-prog-code-1522-persistence-log.md` (Coding Agent, #1522 persistence delete, 45)

Working material: `1386-criterion-3-scenario-refresh-2026-10-07.md` (CXO),
`clear-family-resolver-build-plan-2026-10-07.md` (Lead), and the `spec-xpoll/` directory (Spec:
`proposal-xpoll-corpus.md`, `layer0-screen.md`, `metrics/`).

**Day-close status**: 11 of the 16 files carry a `DAY-CLOSED` marker (Docs, Web, Comms, HOST, Arch, PPM,
PA, Exec, CXO, CIO, Lead). The five unmarked files are Spec's (paused for the evening, with a 10-08
pointer stub) and the four Coding Agent sub-session logs, which are subagent logs and do not write a
marker. Comms was unmarked at the start-of-fire check on 10-08 and was marked by the time this omnibus
was assembled. Lead was nudged about the four prog logs.

---

## Executive Summary

### Core Themes

1. **Alpha was promoted through the promote workflow for the first time, and it took three fixes to get
   there.** PM approved the promotion run at about 10:22 and it failed safely at its first step (nothing
   deployed): `flyctl status --json` has no top-level `ImageRef` on this platform, and the image lives in
   each machine's `config.image`. A fresh dispatch at 10:55 failed correctly at the content-parity gate
   because staging lacked `e598c56e78`, caused by a third stale gate read that had skipped the staging
   deploy. A third run at 16:15 failed at "Promote that exact image" because alpha's app-scoped token
   cannot deploy another app's image. The fix was a copy step using each app's own token. Run 37701277327
   succeeded at 16:20 and alpha's `/health` reads `99289b6690` (was v169 `36b11f3b2c`). Every failure was
   a safe refusal, and each fix was verified against the live platform before the next dispatch.

2. **The #1886 armed-turn design was ruled, then corrected by a live probe, and landed.** Lead's first
   subagent build bound any plausible text as a project name while the name question was armed, so "show
   my projects" or "close issue 108" would have created a project (held, not landed). Arch ruled a
   stateless router consult on the armed turn. PM approved a 10-call live probe: nine of ten phrasings
   behaved, and "delete my project Klatch" drew CLARIFY, which would have been created as a project
   under Arch's first rule. Arch corrected their own ruling at 15:27 (only NONE binds, and CLARIFY,
   low confidence, error or no key go to CXO's confirm) and said so plainly. Landed at 18:27 as
   `7dbc801fc1` and `26b138ecb5`.

3. **A premature close was caught by PM, reopened and fixed.** Lead closed #1941, #1942 and #1944 on
   live evidence at 17:03, but the #1944 test had passed only because Lead had registered the repo over
   REST first. PM had picked the default in Settings → GitHub, and the bare repo name still drew the
   nudge. #1944 was reopened and fixed by matching the current default and the connected account's
   repositories as well as the registry. Lead restored the test account's state afterwards.

4. **Main went red on an arithmetic ceiling, in the same shape as the day before.** The #1522 persistence
   delete removed five mypy errors and the ceiling was not lowered, so Architecture Enforcement failed
   at `mypy_arg_type: 357 < ceiling 362` (run 37714395419). Docs noticed at the 19:12 START-cycle check
   and sent Lead a notice (`3e1768578`), PPM noticed at 21:33, and Lead fixed it at 21:36–21:37
   (`895ad6dcf0`, merged as `4236f1de44`). Docs's 22:12 check read 12 of 12 green.

5. **The CI cost question closed on PM's 10-05 ruling.** Docs found the nightly E2E job red on an empty
   Anthropic CI key and filed #1956. Exec put the ruling that Piper pays for no LLM use in front of
   Lead, PPM and Arch, and Lead reshaped the workflow so no schedule can spend a Piper key (nightly runs
   `-m "not llm"` with every key blank, and the LLM, canonical and AAXT jobs are dispatch-only).

6. **The beta invitation, support page and known-issues text went from drafts to live pages.** Web
   adopted CIO's plugin wording on `/try/alpha`, shipped the invite button on PM's direct "ship" and
   closed website #45, then shipped `/support` to Production at about 16:20. The personality known-issue
   (#1735) was struck by PPM, then reinstated after CXO read the source and found the Warmth setting
   cannot change a chat reply. Privacy Section A was built but is not live, and Row F (#1913) is waiting
   on a PM-minted invite.

7. **PM's production read unblocked a table drop.** PM ran a psql query that returned
   `action_humanizations = 0` rows, with users 7 and setup_complete 5. Lead dispatched the #1522 delete,
   which removed `services/persistence/` and added migration `p1522drop` with a reversible downgrade.

### Technical Details

1. **Promote workflow, three fixes plus a docs entry.** (a) `fly-deploy.yml` reads the image from
   `config.image` across all started machines and refuses on disagreement. (b) The staging gate sorts
   rows by `created_at` in the job and treats a newest-completed run older than 48 hours as an
   unmeasured read (warn and deploy). (c) A copy step pulls staging's image with the staging token and
   pushes it to `registry.fly.io/piper-morgan:promote-<sha12>` with alpha's token. (d) The gotchas doc
   gained the stale-read lesson (a `decisions.log` edit did not trigger a deploy, because `**/*.log` is in
   `paths-ignore`).
2. **`armed_turn_consult.py` (new).** One helper for both carriers (the add-project name question and
   the reminder-task question). Outcomes are RELEASE (operation at or above 0.8, never dispatched by the
   consult), BIND (NONE only) and CONFIRM. The dead onboarding chain (`_check_portfolio_onboarding`,
   `offer_onboarding`, `start_onboarding`) was deleted and the starter census went from 8 to 4, all live.
3. **`handle_delete_todo_targets` (new).** The delete path now consumes router targets and always
   confirms, with CXO's strings D1 to D6 and three additions, ids code-written at resolution and deleted
   exactly at "yes" (a test makes `list_todos` raise during the confirmed re-entry). CXO's single-target
   fix (`4ea71650df`) removed the Leaving line when the target list is one item with no exclude.
4. **`clear_todos` resolver, built and held.** The subagent build (`0707c78bf8`, branch
   `claude/lead-clear-todos-resolver-held`) needs rework per Arch (a code-written
   `clear_family_resolved` marker instead of blanking `original_message`, and the #1886 helper
   generalized with a per-carrier answering set) and waits on the full-corpus run.
5. **Persistence delete.** Migration `p1522drop` (down_revision `o1462oaut`) drops
   `action_humanizations`, and the downgrade recreates the live schema exactly (unbounded varchar,
   timestamptz columns, PK, unique index `ix_action_humanizations_action`). The subagent ran upgrade,
   downgrade and upgrade on local Postgres 5433 and compared `\d` output. It runs as alpha's
   release_command at the next promotion.
6. **CI shape for #1956.** `e2e-aaxt.yml` runs the E2E job nightly with `-m "not llm"` and blank keys
   (measured locally: 8 passed, 1 deselected), and the Monday cron is gone.
7. **Ratchet ceiling.** `ratchet_ceilings.json` mypy arg-type ceiling lowered from 362 to 357 with a dated
   note, measured in the CI-pinned venv.
8. **Last-PM-scan markers untracked.** CIO ruled yes on Pard's proposal and shipped `92b941ee27`:
   `.gitignore` line, `git rm --cached` on nine markers. The markers had cost 111 commits in seven days.
9. **Cross-pollination corpus.** Spec's `xpoll_extract.py` hardening (P1) parses 242 of 242 brief files
   with 0 unparsed: 631 insights, 8 distinct letters (70 appearance rows), and a confidentiality screen of
   review 3, mention 9, clear 619.

### Impact Measurement

- **Commits**: 439 on origin/main for the day (222 not heartbeat or mail), up from 365.
- **Gate**: the MVP gate went from 14 to 13 (#1942 closed). Closed on live evidence: #1941, #1942, #1944
  (#1944 later reopened and fixed), #1848 (Docs), website #45 (Web).
- **CI**: main was 11 of 12 at 04:12 (E2E & AAXT red), 12 of 12 after Lead's 09:3x cut, red again from
  about 18:44 to 21:37 on Architecture Enforcement, and 12 of 12 at 22:12.
- **Tests**: #1886 landed on 5443 passed (intent_service, onboarding, conversation, enforcement and
  ratchets). The #1522 subagent ran 10472 passed, 231 skipped, 0 failed, and 15656 tests collected with
  no collection errors.
- **Cost**: roughly 10 router calls (the #1886 probe, PM-approved) and about 16 chat turns on the
  `web-agent` test account (about $0.45 to $0.50, inside PM's $1 approval). Web's funded-key rerun is
  separate. Spec's assignment ceiling was raised from $50 to $75 by PM.
- **Alpha**: `99289b6690` (was `36b11f3b2c`, v169). Rows A, C and D pass live. Row F is not yet run.
  The Revoke fix `87e8bc9c49` is in the build and has not yet been seen working.
- **Publishing**: Weekly Ship #063 "Check Before You Leap" published at 07:30 (LinkedIn leg recorded
  07:45, status distributed). "Three Failures Inspire One Law" published at 04:1x on 10-08 (see the
  timeline's final note), with the Medium crosspost still owed.

### Session Learnings

1. **A fix that lowers a ceiling must lower the ceiling.** Lead's own summary says the whole-suite and
   gate run was skipped on the last merge before pushing, for the second day running (census floor 10-06,
   mypy ceiling 10-07). Lead extended the 10-06 memory pin to "after any deleting merge, run the pinned
   mypy gate too."
2. **A test is only as good as its precondition.** Lead's #1944 close measured Lead's setup (a repo
   registered over REST), not the user's path (a default chosen in Settings). PM caught it.
3. **Rule 8 earns its keep on rulings, not only on code.** Arch's first #1886 ruling grouped CLARIFY with
   NONE, and the 10-call probe on the real router showed the grouping was wrong. Arch's correction named
   the error and the probe that caught it.
4. **Platform tokens have scopes the platform's read path does not show.** Pard's raw registry read of
   staging's image returned 200, but the deploy API refused the same image for alpha's app-scoped token.
5. **Described is not running, again, at the workflow layer.** The promote job had only ever run as drills
   that skip the failing steps, so three bugs sat in it until the first real run.
6. **An assigned fix reads source when the test cannot.** CXO resolved #1735 from the code (the saved
   personality setting writes `personality_profile`, whose only reader is the page's own `/enhance`
   preview) rather than by repeating a noisy live pair.
7. **Disclose the thing you saw.** HOST reported that one already-burned full invite code had been printed
   in its own tool output (nothing committed), consistent with the bearer-credentials rule.

---

## Timeline (PDT)

### Pre-dawn and early morning (04:00–08:00)

**04:12** **Docs** START. Main read 11 of 12 green: Scheduled E2E & AAXT red (run 37586735961, the
nightly E2E job with an empty Anthropic CI key). Filed #1956 and mailed Exec cc Lead (`8175f695c1`,
`e0e2d569e`). Wrote the 10-06 omnibus (498 lines, 365 commits, 11 sessions).

**06:18** **Web** START. Adopted CIO's plugin wording on `/try/alpha` (website `22f687e`) and replied
by mail (`0782139c5`).

**06:19** **Comms** START. Caught its own false "200" check on the invitation link (the site returns
200 for any path) and created `docs/internal/planning/beta-invitation-copy-2026-10-07.md`.

**06:23** **Lead** START. Main 11 of 12, alpha still v169, the promote run waiting on PM. Inbox read.
Dispatched a Sonnet subagent for #1886: the name ask becomes a per-turn carrier mirroring the reminder
carrier, the dead onboarding chain is deleted, and the starter census is flipped. Wrote the clear-family
build plan, having found that `delete_todo` does not consume router targets.

**06:26** **HOST** START.

**06:27** **Arch** restated the destructive condition as "ids shown equals ids changed" (memo
`629fc0bd3`).

**06:33** **PPM** placed #1956 in Ongoing and corrected the "funded key" framing in its first comment.

**06:47** **PA** START.

**07:08** **Exec** rollup v58. Put the E2E-red policy question to PM's standing 10-05 ruling (Piper pays
for no LLM use) and mailed it (`568db75a1`).

**07:11** **Lead** The #1886 subagent returned (`4f8ecd6df0`, 17 files, 5386 passed, greps empty). Review
found the blocking defect (an immediate project create from a regex-level guess at meaning for any text
that looks plausible as a name). Held on `claude/lead-1886-carrier-held`. Asked Arch and CXO.

**07:17** **CXO** START. Seven memos at start.

**07:30** **Docs** Weekly Ship #063 "Check Before You Leap" published (website `531cd77`, product
`7395802b6a`). A first live poll showed "Ship Not Found" (build lag) and the live check at 07:29 passed.

**07:45** **Docs** Recorded Ship #063's LinkedIn leg (PM cross-posted) and set status distributed.

**07:50** **CXO** Ruled Lead's plain-delete strings D1 to D6 plus three additions (a partial-failure line,
a decline that names what it will not delete, and no undo claim in either direction). Replied to Arch on
#1886, preferring a router consult with a confirm fallback because the alternative eats the user's
original command on "no." Confirmed #1386 criterion 3 at one working day plus a held half day, and found
the scenario scripts stale. **Spec** PM assigned the cross-pollination corpus assignment at 07:50 and
switched Spec to Fable.

### Morning (08:00–12:00)

**08:0x** **Web** A relayed go-ahead for the invite button was denied by the classifier. (Resolved at
about 10:40 on PM's direct "ship.")

**08:0x** **Spec** Read 27 memos from follow-through on assignment 1 and oriented on the corpus: 199 dated
briefs in this repo's slice, about 223k words and 444 numbered insights. PM answered the open questions
(full archive of 234 briefs, the interface lives under `/internal/`, a $50 ceiling).

**08:3x** **Spec** Dispatched two Sonnet research subagents (corpus extraction, prior-work map) and pushed
a Janus notice to the designinproduct repo (`932518a`).

**09:19** **Comms** Verified Ship #063 at the data layer.

**09:25** **Lead** Reshaped #1956: nightly E2E runs only `-m "not llm"` with blank keys, and the LLM,
canonical and AAXT jobs are dispatch-only. Dispatch run 37651896838 passed with E2E success and the
others skipped, and main read 12 of 12. Sized #1889 at about a day.

**09:27** **Arch** Ruled #1886: the router decides answer-versus-new-ask on armed turns, with a confirm
fallback and one helper for both carriers (memo `19276a70b`).

**09:29** **Lead** Dispatched a Sonnet subagent for delete-targets (clear-family piece 1).

**09:33** **PPM** Closed the sizing deadlines (#1889 about a working day, #1386 criterion 3 a working day
plus a held half day) and reshaped #1956 (`140a606928`).

**09:46** **Lead** Delete-targets landed after review (`e598c56e78`, merged `6083677204`): always
confirms, CXO's D1 to D6, no description or catalog change so no corpus run needed. Dispatched piece 2
(`clear_todos` resolver, built to be held).

**10:12** **Docs** Closed #1848. Restored five orphaned 2025-09-20 session logs from `858f10201`
(commit `541e647662`).

**10:22** **Lead** PM's promotion of run 37513074619 failed safely at its first step ("Could not read
ImageRef from piper-morgan-staging"). Root cause: no top-level `ImageRef` in `flyctl status --json`, the
image is each machine's `config.image`. Fixed in `fly-deploy.yml`, verified by running the extraction live
against staging.

**10:35** **Lead** The clear-family piece 2 build returned (`0707c78bf8`) and was held for deviations to
review.

**10:40** **Web** After PM's direct "ship," the invite button shipped to website main (`a08efac`) and
website #45 was closed. A credential read was denied again, and at about 10:45 xian ran it. Alpha checks
were then blocked by an out-of-quota LLM key.

**10:55** **Lead** PM's fresh promote (run 37662093227) failed at the content-parity gate, correctly:
staging `fa3fa1f` lacked `e598c56e78`. Fixed the stale-read gate, then added the gotchas-doc entry at
11:00 when a `decisions.log` edit alone did not trigger a deploy. Staging deployed `580e8186ff` (run
37662980278).

**11:08** **Exec** Rollup v61: the first promote run had failed on ImageRef and the second failed at
content parity. Alpha was still v169 (mail `b8e86fb80`).

**11:18** **Web** Funded-key rerun: #1735 inconclusive, #1955 not reproduced literally, and Reset to
Defaults did not reset Warmth (filed as #1957). Filled the `/support` content on
`claude/web-support-page` (`37bf522`).

### Midday and afternoon (12:00–18:00)

**12:19** **Comms** Revised the invitation (#1886 now under Gate), commit `ee251c18b3`.

**12:25** **Lead** Applied CXO's single-target fix (`4ea71650df`). Pushed at 12:31 so main reached
`8c8082c200` and staging deployed through the fixed gate (the first deploy to pass on its own).

**12:27** **Arch** Ruled the three landing points for `clear_todos` (memo `0b7c5c993`).

**12:33** **PPM** Keep or strike: #1735 struck, #1955 kept, #1957 kept. #1886 got `Gate class: 4`.

**12:47** **Comms** PM reviewed "Three Failures Inspire One Law" directly. By 13:0x the fixes were applied,
the retitles for 10-11, 10-13 and 10-15 synced, the draft files renamed, and the row set to
ready-for-docs. At 13:2x PM ruled that the Sep 6 beat (Tue 11-03) is a scaffold and the first trial of
"AI prompts human."

**13:06** **Lead** The #1886 router-consult build returned (`00a7c364ca`, 5438 passed) and was held for
Arch's live probe, because the build adds a create path alpha does not have.

**13:12** **Docs** Committed the `docs-last-pm-scan` marker (`479a4584dd`) and the mail move (`8e9c612b3`).
Received Comms's publish-ready memo for "Three Failures." Out of band, PM asked for a proofread: all 16
template-audit checks passed and the claims were fact-checked against the 08-11 and 08-12 omnibi.

**13:30** **CXO** Answered #1735 from source: the slider's Save writes `personality_profile`, whose only
reader is the page's own `/enhance` preview, so a saved Warmth cannot change a chat reply. Web's 0.0
versus 0.7 pair was run variation. Asked Web for the literal "next Friday" wording rather than filing.

**14:09** **Lead** PM approved the 10-call router probe and it ran: 7 of 7 command phrasings released at
0.8 or above, Klatch bound (NONE), and "delete my project Klatch" and "Piper Morgan Website" drew
CLARIFY. Tightened the held branch (`71693dd849`) so only NONE binds.

**15:08** **Exec** Rollup v62. The next promote run (37687899847) was waiting on PM.

**15:18** **Web** Answered CXO's literal-wording ask: only the Friday "next" wording is wrong.

**15:27** **Arch** Corrected their own ruling after Lead's probe (9 of 10, CLARIFY on a delete-project
phrasing): only the answering set binds, and CLARIFY, low confidence or error confirms. Memo `0ece35153`.

**15:33** **PPM** Reinstated #1735 after CXO's source read, re-verified by grep (`99289b6690`).

**16:15** **Lead** PM approved run 37687899847 and it failed at "Promote that exact image": Fly's deploy
API refused alpha's app-scoped token for another app's image. Fix: the copy step above.

**16:20** **Lead** ALPHA PROMOTED. Run 37701277327 succeeded and `/health` reads `99289b6690`. The flag
read on alpha shows the 12 prior tokens plus `complete_todo`. **Web** shipped `/support` to Production on
PM's direct go (desktop render checked).

**16:28** **Lead** Row C passed live on the `web-agent` account (seven chat turns): the numbered list
renders, "Mark the first three complete and leave the fourth one pending" confirms, "yes" completes
three, and the REST API shows three `completed` and one `pending`. **Exec** v63 and v64 (support page
live) and v65 followed PM's database check (users 7, setup_complete 5, humanizations 0).

**17:03** **Lead** Rows A and D passed live after PM connected the test account to GitHub. Closed #1941,
#1942 and #1944 and filed #1959 and #1960.

**17:09** **Lead** PM caught the premature #1944 close. Reopened and fixed (bare repo name now matches
the default and the account's repos), with three new pins. At 17:44 Lead deactivated the repo registration
it had created so the live re-test runs on the account's real state.

**17:14** **CXO** Seat restarted onto Claude Code 2.1.280 per Pard's handoff, with the cron re-armed.

### Evening and night (18:00–24:00)

**18:18** **Web** Built privacy Section A on `claude/web-privacy-section-a` (`2a24a37`), not live. Row F
(#1913) needs a PM-minted invite and key. Pushed `c9a8d58f7f` for the scan marker.

**18:26** **HOST** Answered Exec on the roster: sachio222 is not on it, recruiting names were given, Rebecca
Refoy is in, and Janne Lammi and Savanna Booth Enoch are reissue-pending (mail `1580bc755`).

**18:27** **Lead** #1886 landed (`7dbc801fc1`, main `26b138ecb5` after a push race) on 5443 passed.
**Arch** ruled #1958 (memo follows CXO's filing).

**18:31** **Lead** Dispatched a Sonnet subagent for #1522.

**18:33** **PPM** MVP gate 14 to 13 (#1942 closed) and the invitation approved by PM. Slip logged: PPM
re-armed a session cron on a LaunchAgent seat and deleted it the same fire.

**18:43** **Lead** #1522 landed (subagent `b79e0466c5`, merged `e26d6b1b4e`) with migration `p1522drop`.

**18:47** **PA** Told Web and Comms to keep the interim paragraph on the invitation.

**19:08** **Exec** Rollup v66.

**19:12** **Docs** Main read red on Architecture Enforcement (`mypy_arg_type: 357 < ceiling 362`, run
37714395419, 01:44Z). Sent Lead a notice (`3e1768578`).

**19:17** **CXO** Verified `71693dd849` in source: only `none` binds, and every other outcome confirms.

**21:19** **Comms** Drafted the widened privacy scope sentence and flagged that the policy does not cover
Piper accounts.

**21:26** **HOST** No spare unused invite exists for Row F (mail `2c7baf2a2`), and disclosed the
burned-code print in its own tool output.

**21:33** **PPM** Noticed main red on the ratchet. **Lead** fixed it at 21:36 (`895ad6dcf0`).

**22:07** **CIO** Ruled yes on untracking the `last-pm-scan` markers and shipped `92b941ee27` after
testing the migration in a throwaway worktree. A `pard` cc was refused by `mail-send` because Pard is
cross-project with no inbox here, so CIO resent to Exec.

**22:12** **Docs** STOP. CI read 12 of 12 green after Lead's `4236f1de44` (21:37 PDT).

**22:17** **CXO** STOP (day-close). **Lead** STOP, with the carry-forward rewritten (cron `1224eddf`, rotate
by Sun 10-11 START).

**23:08** **Exec** Rollup v67.

**18:0x–18:5x (Spec)** Proposal v0.3 written with all eight §7 decisions resolved
(layer 0 screen then publish, Klatch read-only, a periodic sweep review, six topics plus a free-text tag,
a pilot of 40 of the 116 "what became of it" items, E1 and E2 funded at about $6, Janus pre-labelling 100
gold items, the eight pre-unification briefs kept). Janus review request pushed (`7c1fa39`), Layer 0
screen run (235 files, 11 with hits, 3 substantive), and P1 returned. Spec paused for the evening with a
self check-in armed for 08:30 PDT on 10-08.

**Note on timestamps**: Spec's log carries one UTC cross-reference ("01:09 UTC 10-08") and created
`dev/2026/10/08/2026-10-08-0001-spec-code-log.md` by mistake at 17:02 PDT, after a bare `date` read the
UTC rollover. The 10-08 file is a pointer stub and was not renamed.

---

## Cross-Role Coordination Notes

1. **The promote chain** (PM → Lead → Pard → Exec): PM approved three runs across the day, Lead fixed the
   first-step failure (ImageRef), the parity failure (stale gate) and the scope failure (copy step), and
   Pard measured that the app-scoped token could read staging's image (HTTP 200) before the deploy API
   refused it. Exec relayed PM's questions and Lead's answers through the rollups. Pard's PR #1952 (the
   stale-read gate fix) overlapped Lead's on main, so Lead asked Pard to rebase over Lead's version.

2. **The #1886 chain** (Lead → Arch → CXO → PM → Arch): Lead held the first build, Arch and CXO ruled for
   a router consult with a confirm fallback, PM approved the probe, the probe broke one rule, Arch
   corrected it, and CXO verified the corrected behavior in source after it merged (`71693dd849`, then
   again at 19:17 on origin/main).

3. **The #1956 chain** (Docs → Exec → PPM → Arch → Lead): found in the Docs START check, routed to Exec
   cc Lead, put in the context of PM's 10-05 ruling by Exec, placed in Ongoing by PPM (with the funded-key
   framing corrected), and reshaped by Lead at 09:25. Closes after the nightly run confirms the
   schedule path.

4. **The #1735 reversal** (Web → PPM → CXO → PPM): Web's run pair was inconclusive, PPM struck the
   known-issues line, CXO answered from source that a saved Warmth cannot change a chat reply, PPM
   reinstated it at 15:33 with its own grep.

5. **The persistence delete** (Arch → PM → Exec → Lead): Arch's 10-05 GO required the production count.
   PM ran the psql query on piper-morgan-db at about 16:3x, Exec relayed it, and Lead dispatched the
   delete with the count in the commit and the migration docstring.

6. **The invitation copy** (CIO → Exec → Comms → Web → PA): CIO's plugin line was adopted by Exec,
   written into one file by Comms, put on `/try/alpha` by Web on PM's go, and kept as the interim
   paragraph by PA's call at 18:47.

7. **The red main** (Docs → Lead → PPM): Docs's 19:12 check found it and mailed Lead, PPM saw it again at
   21:33, and Lead's fix landed at 21:36.

8. **The marker untracking** (Pard → Exec → CIO → Exec): Pard proposed gitignoring the `last-pm-scan`
   markers, Exec routed it, CIO ruled and shipped it, and a cross-project cc had to go back through Exec.

Verified how: read all 16 session logs in `dev/2026/10/07/` in full or by heading (the Lead, CXO, CIO and
Spec logs re-read this session before writing), with commit hashes and run ids copied from those logs and
not re-queried. Layer: the logs' own claims, not GitHub or Fly state. Denominator: 16 of 16 log files
read. Commit counts were taken from `git log origin/main` as stated in the header.

---

## Discovered Work Filed

- #1956 E2E & AAXT red on an empty CI Anthropic key (Docs, from the START main-CI check)
- #1957 Reset to Defaults does not reset Warmth (Web, from the funded-key rerun)
- #1958 "next Friday" label on a same-week reminder (CXO, UX, low)
- #1959 close and reopen confirm before checking that the issue exists (Lead)
- #1960 the consent copy says set-default-repo writes to connected tools, when it writes Piper's own
  preference store (Lead)

**Closed**: #1848 (Docs), #1941, #1942 and #1944 (Lead, with #1944 reopened at 17:09 and fixed), website
#45 (Web). #1956 closes after tonight's nightly run confirms the schedule path.

---

## Notable Process Findings

1. **The promote path had never been exercised end to end.** The first real runs exposed three bugs across three
   dispatches (10:22, 10:55 and 16:15). Drills that skip the failing steps are not a test of those steps.
2. **A relayed go and a direct go are different to the permission layer.** Web's relayed go-ahead on the
   invite button was denied by the classifier and PM's direct "ship" was not. Credential reads needed
   xian's own run both times.
3. **Closing on a self-built precondition.** Lead's #1944 close is the sharpest instance of the day. It was
   caught by PM because PM had done the user action in the UI, which Lead's REST setup had bypassed.
4. **Two same-shape reds in two days.** The census floor on 10-06 and the mypy ceiling on 10-07 both
   came from merging a deletion without running the whole gate. Lead's pin was extended.
5. **A cross-project seat has no inbox here.** CIO's `mail-send` refused a cc to Pard, which is correct,
   and CIO's "wanted but not found" is a note saying Pard is cross-project in the DIRECTORY-adjacent docs.
6. **A cron re-armed on a LaunchAgent seat.** PPM re-armed a session cron on a LaunchAgent seat and
   deleted it the same fire. The gate in `duty-cycle-tick` says to skip all cron content there, and the
   slip was self-caught.
7. **Subagent tier is being logged.** Lead's log notes the model tier at every dispatch ("Sonnet,
   isolated worktree"), and the Coding Agent sub-session logs record the observed model
   (`claude-sonnet-5`).
8. **The 10-08 UTC rollover.** Spec's stub file for 10-08 came from a bare `date` after the UTC rollover,
   the failure the CLAUDE.md Pacific-time rule warns about. The file was not renamed, per that rule.

---

## Logging Continuity Note

- 16 log files for 10-07: 12 role logs and 4 Coding Agent sub-session logs. 11 are day-closed.
- Spec's log was paused for the evening and carries a sign-off check (`git status` tracked changes 0,
  `origin/main..HEAD` 0). It is expected to continue on 10-08 from the pointer stub.
- The four prog logs are subagent logs, and none writes a `DAY-CLOSED` marker. Lead (the dispatcher) was
  nudged at the 10-08 START check about these.
- Spec's model changed mid-day (Opus 5.5 to Fable at 07:50, sourced from the `/model` output) and the
  log header records it.
- Spec's entries use "17:xx" and "18:xx" for several decisions, so within-hour order is by sequence in
  the log, not by minute.

Verified how: `ls dev/2026/10/07/` (16 files plus working material), `grep -c DAY-CLOSED` over the 16
files (11 matches), and `wc -l` on each (counts above). Layer: file contents on the Docs worktree at
origin/main on 10-08. Denominator: 16 of 16 files.

---

## Open to PM at day close

🔒 **Held on PM**
- **Row F (#1913)**: needs a PM-minted fresh invite and key. HOST reports no spare unused invite exists.
- **Section A ship go** and **Revoke press** on the privacy and Revoke work Web and PA built.
- **Privacy scope sentence**: Comms's widened sentence flags that the policy does not cover Piper accounts.
- **Recruiting names** and the **HOST yes or no** on the roster answers (sachio222 is not on the
  roster and needs identifying).
- **Calendar secrets**: carried from earlier days.
- **Medium crosspost for "Three Failures Inspire One Law"**: owed after the 10-08 blog-first publish. Once
  PM supplies the Medium URL, Docs sets `mediumURL`, status distributed and `canonicalSite` distributed.

**Flag**
- Stale `roadmap.md` "fold due 10-09" for the Monday 10-12 Docs audit.
- R6 step 3 page review after the 10-08 21:59 PDT quota reset (CIO will mail Docs).
- `clear_todos` is held until the full-corpus run, and the cost of that run is PM's call.

Verified how: the open items copied from the day's logs (Web, HOST, Comms, Exec, Docs), not re-checked against
GitHub or the mailboxes at the time of writing. Layer: the logs' own statements. Denominator: the
role logs that name PM-gated items (6 of 12).
