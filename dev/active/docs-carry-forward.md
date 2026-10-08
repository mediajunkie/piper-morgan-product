# Docs Carry-Forward

**Updated**: 2026-10-08 07:2x PDT (07:12 WORK wake: drained; Medium crosspost for Three Failures closed)

**10-08 07:2x STATE (supersedes 04:5x where they differ)**: Three Failures is `distributed` (PM supplied the Medium URL; calendar set, validator clean). Comms and Lead 10-07 logs now DAY-CLOSED. Spec's 10-07 log is still unclosed: nudged (`e7cd58939`), re-check at 10:12 WORK. CI 12/12, inbox 0, 1c/1f/1g clear, criteria same 11. Standing: Mon 10-12 Weekly Docs Audit (flag roadmap.md fold due 10-09); R6 step 3 page review after the 10-08 21:59 PDT quota reset (CIO mails me); held on PM: git rm of dev/active/covapitchdeckv2.pptx and dev/active/Treatment, #1909's two open boxes.

**10-08 04:5x STATE (supersedes the 10-07 22:1x block where they differ)**: START fire. Main CI 12/12 at open. **Published "Three Failures Inspire One Law"** (website `6785afd`, live at pipermorgan.ai/blog/three-failures-inspire-one-law/). Row is `published`, `canonicalSite` empty. **Medium crosspost OWED** (PM's hand): Step 1f resurfaces each fire. When PM gives the Medium URL: set mediumURL, status distributed, canonicalSite distributed (update-calendar skill, by header name). Step 1d done: 10-07 omnibus written (16 logs, 439 commits, 11 of 16 DAY-CLOSED), 16 activity rows appended (2836 to 2851), nudges sent to comms and lead (`635fc5418`). Spec's 10-07 log is paused (not closed), its 10-08 stub exists: re-check at WATCH. NEXT: Mon 10-12 Weekly Docs Audit (flag roadmap.md fold due 10-09). R6 step 3 page review after the 10-08 21:59 PDT quota reset (CIO mails me). Held on PM: git rm of dev/active/covapitchdeckv2.pptx and dev/active/Treatment, #1909's two open boxes.

**10-07 22:1x STOP — DAY CLOSED**: main CI 12/12 green again (the 19:12 mypy-ceiling red cleared; Lead's lane, I touched nothing). Inbox 0, 1c/1f/1g clear, criteria same 11. DAY-CLOSED written. Tomorrow's draft + jpg verified present. **NEXT, Thu 10-08 04:12**: START heartbeat FIRST; Step 1d (10-07 omnibus + activity rows + nudge any 10-07 log lacking DAY-CLOSED); then publish "Three Failures Inspire One Law" (see NEXT block; full 16-check re-audit at publish, `--work-date 2026-08-12`, theme building, Medium-only after). 10-08 quota reset passes Thu 21:59 PDT, R6 step 3 review follows CIO's mail. This seat is LaunchAgent-only: no cron to re-arm.

**10-07 19:1x STATE (supersedes 16:1x where they differ)**: Quiet fire except CI: **Architecture Enforcement RED** since 01:44Z on Lead's #1522 delete; the mypy ratchet wants `mypy_arg_type` ceiling 362 to 357 (drift removed). Lead's lane, notice sent (`3e1768578`). **At 22:12 recheck CI first**; if still red, say so, don't touch their files. Inbox 0, 1f/1g clear, criteria same 11. 22:12 is the last fire of today: STOP (day-close + DAY-CLOSED marker + memory-eval + sign-off), then Thu 10-08 04:12 publish "Three Failures Inspire One Law" per NEXT block.

**10-07 16:1x STATE (supersedes 13:1x where they differ)**: **PM conversational ask (between fires): proofread + queue "Three Failures Inspire One Law."** Ran the full `template-audit` 16-check skill myself (not trusting Comms' memo alone) — all 16 PASS, check #11's 3 matches each individually judged PASS. Independently fact-checked every concrete claim against the 08-11/08-12 omnibus logs — all matched exactly, including event sequencing. Queueing: nothing to change, calendar row already `ready-for-docs`/`pubDate=2026-10-08`, the terminal pre-publish state; will auto-publish at Thursday's 04:12 fire. Reported full results to PM directly in conversation.
**16:12 duty-cycle fire**: quiet hold. Synced clean, CI 12/12. Inbox 0 direct — noted Pard's Claude Code 2.1.280 restart memo landed via sync (to Exec cc CXO/HOST/Web; confirmed Docs not addressed/cc'd, no action owed). GitHub-criteria line: same 11 watch-tracked issues, nothing new. Step 1c/1f/1g clear. Two consecutive empty rounds confirmed.

**10-07 13:1x STATE (supersedes 10:1x where they differ)**: **Housekeeping note on my own process**: found the 10:12 fire's inbox→read/ triage move had never actually been committed (only the session-log/carry-forward commit landed) — recovered it via `mail-send.sh` (`8e9c612b3`) plus a direct commit for the unrelated `dev/state/docs-last-pm-scan` touch (`479a4584dd`). Both verified on `origin/main` after syncing (was 87 commits behind). **Lesson for future fires: after any `mv` in `mailboxes/`, verify `git status` is clean before moving to the next step, not just at Step 6 — don't assume a prior `mv` got swept into a later commit.**
**New direct mail, read + triaged**: Comms publish-ready for **Thu 10-08 04:12: "Three Failures Inspire One Law"** (slug `three-failures-inspire-one-law`, theme building, `--work-date 2026-08-12`, Medium-only syndication after publish). Draft + renamed image both verified present on disk (`docs/public/comms/drafts/three-failures-inspire-one-law.md` + matching `.jpg`, both in `drafts/`); calendar row `ready-for-docs`. **Also flags 3 upcoming retitles already applied by PM/Comms** (Sun 10-11 "It Doesn't Count if You Skip It", Tue 10-13 "Giving It Away, and Wondering Who May Want It", Thu 10-15 "The Overzealous Cleanup Routine") — filenames/calendar already match, footer teases already updated, nothing owed from Docs until each one's own pubDate fire.
CI 12/12 green. Step 1c/1f/1g clear. GitHub-criteria line re-run: same 11 watch-tracked issues, #1848 correctly absent (closed last fire), nothing new.

**10-07 10:1x STATE (supersedes 07:3x where they differ)**: Sync clean. Main CI `scripts/main-ci-status.sh` = 12 of 12 green (E2E back to green — Lead's #1956 reshape verified via a keyless dispatch, per their cc memo, triaged to read/). Inbox 0 direct, 1 cc read. Step 1c/1f/1g all clear. **GitHub-criteria line (`label:documentation`, open) run: 12 results, all opened.** 11 already watch-tracked (no new action); **#1848 was unclaimed and actionable — closed this fire**: cherry-picked the 5 named 2025-09-20 session-log paths (claude-code-doc-mgr, cursor-agent, 2× chief-architect, lead-developer) out of orphan commit `858f10201` (branch `origin/verification/ci-test-1758852617`, never merged to main) per the issue's own suggested approach; did NOT touch the other 5 non-session-log files in that commit (out of scope). Committed `541e647662`, verified landed on `origin/main`, commented evidence + closed #1848 (state verified `CLOSED` via API, not exit code). The other 4 pre-convention gap dates (08-16/08-31/09-11/09-12) remain confirmed-unrecoverable per the issue — not re-attempting the full 230-branch search. Two consecutive empty rounds (mail/standing-items/criteria) confirmed before idle.

**10-07 07:3x STATE (supersedes 10-06 22:2x where they differ)**: Step 1d DONE: 10-06 omnibus (`25fd5f661d`, 498 lines, 11 sessions, 365 commits) + 11 activity rows (`d87035f9cb`, 2824 to 2835); all 11 logs carry DAY-CLOSED, no nudges. **Ship #063 PUBLISHED**: website `531cd77` (workDate 2026-09-25, pubDate 2026-10-07, cluster the-alpha), live at https://pipermorgan.ai/shipping-news/weekly-ship-063-check-before-you-leap/ (verified 07:29 PDT by body text "hosted MCP connector" and the page title, after a ~60s "Ship Not Found" lag). Calendar row `published`, blogURL/blogPath set, draft archived to `drafts/published/` with draftPath updated, validator clean for the row (27 pre-existing warnings elsewhere), view rebuilt. LinkedIn leg DONE 07:4x (PM posted; row `distributed`, canonicalSite `distributed`, liPubDate 2026-10-07). Template audit on the Ship: #1 caption empty = N/A for Ship; #2,#5,#8,#9,#10 clean; #11 one match (line 34 "anyone" = readers, PASS); #6/#13/#14-role/#15 N/A by convention. Pipeline side effect kept: the Medium RSS fetch added a syndicated item ("August 10, 2026") to the website JSON. CI via Exec policy: E2E red is #1956 (billing/policy, not Docs). Still held on PM: `git rm` of CoVa deck + `Treatment`; #1909 two open boxes. NEXT named triggers: **Mon 10-12** weekly audit (flag roadmap.md "stale, pointer added 10-05, fold due 10-09"); **after the 10-08 quota reset** R6 step 3 page review; **~11-30** glossary re-verify. Possible flag to PM via Exec: Medium slug for "The Exceptions" is the dateline form (unverified, Cloudflare 403).

**10-06 22:2x STATE (supersedes 19:16)**: ADR-080 doc scope is DONE on all three surfaces: (a) Lead signed off, (b) Arch's provenance fix applied, (c) fixed and re-rendered by Web at 375 dark. Only possible follow-up is Arch's optional rule-7 line about `scripts/inversion_offline_reverdict.py` (Arch's call, not mine, do not add unprompted). Inbox 0, CI 12/12. **NEXT, Wed 10-07 04:12**: START heartbeat first; Step 1d (10-06 omnibus + activity rows + nudge any 10-06 log lacking DAY-CLOSED); then Ship #063 publish per the NEXT block below.

**10-06 19:16 STATE (supersedes 16:20 where they differ)**: ADR-080: Arch approved (a) and (c), asked one (b) provenance fix; Web's render check found 3 diagram defects. BOTH FIXED and mailed (reply to Arch cc Web/Lead). (a) waits ONLY on Lead's sign-off; (b),(c) done unless Arch/Web come back. Import-level diagram DROPPED per Arch. Main CI is 12/12 green again (Lead's red cleared; drop it from the watch list). Exec notice read: usage STOP line is 95% weekly (PM-approved), window ends Thu 10-08 21:59 PDT; no subagents in use, keep heavy work light. Inbox triaged to read/. NO open PM-gated item new this fire. **Wed 10-07 04:12 Ship #063 publish stands (see NEXT block below).**

**10-06 16:20 STATE (supersedes 07:30 where they differ)**: ADR-080 doc assignment (Arch rule memo; PM wants it baked into design docs): (a) routing-stack section, (b) domain-models Intent update, (c) `diagrams/adr-080-interpret-resolve-permit-execute-2026-10-06.html` all drafted and mailed to Arch (cc exec/lead/ppm/cxo). WAITING on Arch review (a,b due 10-09, c due 10-12; Lead signs off (a)). Open question to Arch: do they also want an import-level dependency diagram? Fold in Arch's edits when they arrive; HTML layout never rendered, verify visually if a browser is available. Main CI 10/12 (Arch Enforcement + Tests red since 20:00Z on `1aac9fa5d6`; ratchet census 34<35 etc.), Lead's lane, mailed `96e738080` + `d943e6834`; RECHECK 19:12. Wed 04:12 publish Ship #063 unchanged.
**10-06 07:30 STATE**: Published "The Exceptions That Test the Rule" (04:20; website `a912d71`; PM's Medium crosspost owed, `canonicalSite=distributed` only at that leg). 10-05 omnibus done (`578f3d386e`, 450 lines) + activity-log rows (`1fe2464c9e`). CXO's 10-05 log still lacks DAY-CLOSED (nudged 04:20). Inbox 0, CI 12/12 green. **Wed 10-07 04:12**: publish Ship #063 (slug `weekly-ship-063-check-before-you-leap`, `--work-date 2026-09-25`, cluster `the-alpha`, draft `docs/public/comms/drafts/weekly-ship-063-draft-2026-10-03.md`; LinkedIn-only leg after). Still held: `git rm` of CoVa deck + `Treatment` on PM confirmation; #1909 2 open boxes (fixtures, hooks-functional PM call); 10-12 weekly audit flags roadmap.md (fold due 10-09); R6 step-3 page review after 10-08 reset.
**10-05 10:05 STATE**: Weekly #1938 and Monthly #1937 both CLOSED (evidence comments posted; staggered calendar updated: next weekly Mon 10-12, next monthly Mon Nov 2). dev/active 163 → 55 (`44c868d772`; ruff fix `9f687e68ce`). Template fixes `b0484cce0a`. Mail to exec re 3 unknown files (`covapitchdeckv2.pptx`, `piper-learning-data-*.json`, `Treatment`), awaiting PM call via Exec. Still optional/unclaimed: refresh my own BRIEFING-ESSENTIAL-DOCS + ROLE-PORTFOLIO-DOCS (~34d stale, only stamp what I verify); #1909 quarterly leftovers not re-checked.
**10-05 16:30 STATE**: #1909 now 14/19 ticked (open: test fixtures, hooks-functional, 3 beads boxes; `bd` absent, asked CIO `f7341a668`; needs PM call to close). check-mailbox skill fixed `bc5a34d309`. Inbox 0. CIO/Pard per-fire-record memos read, nothing owed to Docs (R3 store after 10-08 holds the per-fire record; I keep START every fire). Pre-flight for Tue/Wed publishes done early: Tue draft+jpg exist, Wed Ship dry-run clean (script uses shared `piper-ship.webp`, so the frontmatter `piper-ship.png` is not a blocker). The 04:12 fires still run the full pre-flight, the 16 audit checks and the real publish. CoVa + `Treatment` still HELD on PM's confirmation.
**10-05 22:25 STATE**: Main CI via new `scripts/main-ci-status.sh` = 12/12 green (use it for Step 1e from now on). `dev/state/sprint-truth-MVP.docs.json` committed (`f05094a6aa`), tree clean; Pard notified. `bd` ruled out (GitHub issues are the tracker). #1909: 17/19 ticked (beads boxes N/A per CIO); open: test fixtures, hooks-functional (PM call). Inbox 0. Tue 04:12: publish The Exceptions That Test the Rule (Medium only). Wed 04:12: Ship #063.
**10-05 13:30 STATE**: JSON archived to `dev/2026/08/07/` (done). CoVa + `Treatment` still HELD on PM confirmation. Pard's TSV finding answered (`480a5068a`): the 10:12 START was MY miss, **START opens EVERY fire even mid-wake after compaction**. PPM: roadmap.md fold due after Fri 10-09, flag it "stale, pointer added 10-05, fold due 10-09" in the 10-12 weekly audit. Inbox 0.
**10-05 11:00 STATE (supersedes the 10:05 block where they differ)**: #1939 CLOSED (`0ae10fd2cb`). PM answered the stray-files ask in conversation: CoVa deck + `Treatment` are PM's D-in-P material, PM will move them; close-out memo sent to Exec (`c1a1a09d4`). **HELD on PM's confirmation they are copied out**: `git rm` of `dev/active/covapitchdeckv2.pptx` and `dev/active/Treatment` (recoverable from `9a51d70cec`). JSON `piper-learning-data-1786116943945.json` to archive to `dev/2026/08/07/` unless PM says junk (do it next fire if PM has not objected; ask nothing more). #1909 OPEN: 9/24 ticked, comment `6000074367`; open: orphan dirs (7 candidates), 26 root `handoff-*.md` (needs Exec/PM call), skills >120d (4), `bd` absent. PM floated a handoff/restart, not urgent; write a handoff doc only on PM's word. No Python env needed (system python3).
**NEXT (named triggers, each a real date/time):**
- **Thu 10-08 04:12**: publish "Three Failures Inspire One Law" (Medium only; calendar row `ready-for-docs`; slug `three-failures-inspire-one-law`; `--work-date 2026-08-12`; theme building). Emit START heartbeat FIRST. Draft + renamed image already verified present this fire (13:12) — re-verify again at publish per the standing re-audit discipline, don't trust this fire's check as still current. Full 16-check template audit at publish time (Comms's own audit already recorded: title case OK, 0 placeholders, tease→"No Undo" OK, 0 semicolons, #11 3 matches all PASS).
- **Mon 10-12**: Weekly Docs Audit (flag roadmap.md "stale, pointer added 10-05, fold due 10-09"; next monthly housekeeping Nov 2).
- **After the 10-08 quota reset**: R6 step 3 shared-state page review (CIO mails me when drafted; I own CURRENT-STATE).
- **~11-30**: glossary 60-day re-verify.
- Archiving any `.py` out of dev/active: run ruff format on it BEFORE the push.

**10-05 04:31**: Step 1d DONE: 10-04 omnibus (`41ba53ef54`, 26 sessions, 421 commits), 26 activity rows (`789c396247`, 2785 to 2811), Exec nudged for no STOP/`DAY-CLOSED` (`3f0ad7adc`). 1c/1f/1g clear. Main CI `success`. Inbox 0. **NEXT (10:12 fire): Weekly Docs Audit + Monthly Housekeeping** once the workflow creates the FLY-AUDIT issues (~09:20 PDT; none open at 04:30). If absent at 10:12 it is the #1713 shape, file it. Also at the audit: check the `last_verified` cluster (13/38 at 09-28), the open-issue inactivity ratio (217/288 at 09-28), #1904/#1644 watch. Tue 10-06 04:12: publish "The Contract Tested the Day It Was Born" only after `ready-for-docs` + publish-ready memo from Comms (currently `drafted`). Ship #063 (10-07) awaits PM voice pass + Comms audit.

**10-04 22:12**: main CI `success` again (head `d7f9a6056d`, CIO fixed the ruff format); no follow-up owed. Inbox 0. Day closed (`DAY-CLOSED` in the 10-04 log). NEXT (Mon 10-05 04:12 START): 10-04 omnibus + activity-log rows, nudge any agent whose 10-04 log lacks `DAY-CLOSED`, Weekly Docs Audit + Monthly Housekeeping (#1909 remaining), check CI first.

**10-04 19:12**: 2 memos read (CIO guard-pm-checkout live, R6 step 1; CIO: R6 metric is CIO's, my CLAUDE.md step-3 edit kept; CIO will mail me when R6 step 3's shared-state page is drafted, since I own CURRENT-STATE; steps 3+5 start after the 10-08 reset). **Main CI RED** (ruff format on CIO's `.claude/hooks/guard_pm_checkout.py`, runs 37254226775 + 37253514895); mailed CIO (`c37f56995`), not touching their file. **Recheck CI first at 22:12.** Inbox 0.

**10-04 16:12**: PM ruling 1 (via Spec) DONE: CLAUDE.md sign-off steps now `git push origin HEAD:main` (`79ae4db3aa`; mailed Spec cc CIO). **Watch**: Spec's R6 metric is "yours to finalize" addressed to CIO+Docs jointly; I asked Spec who holds it, treating it as CIO's unless told otherwise. R6 steps 3 and 5 (slim shared-state page replacing BRIEFING-CURRENT-STATE in session-start reading; slim CLAUDE.md after probe suite) will touch Docs-owned files, CIO sequences them after the 10-08 quota reset. **Post-commit hook note (stage 2 live on my seat)**: `git log -1` is a heartbeat marker, cite real commits via `scripts/last-real-commit.sh --short`; kill switch if markers pile up = rename `.git/hooks/post-commit` aside and tell CIO. Inbox 0, CI green.

**10-04 04:12 START**: 10-03 omnibus built (21 sessions, 426 commits, `9e4d874477`) + 21 activity rows (`f20d08de95`). Spec's log lacked DAY-CLOSED (cloud session still open at synthesis, no nudge). **"Distribution Is a Product Decision, Not a Marketing One" PUBLISHED** (website `9bc419e`, live-verified by body + served-asset md5), row `published`, draft archived. **FULLY DISTRIBUTED 06:34** (PM supplied both URLs; LinkedIn page datePublished 2026-10-04T13:26Z; row `distributed`, validator 0 errors). PM also removed "quietly" from the footer: applied to the live site (website `507012e`, body-verified live) and the archived draft. Nothing owed on this post. NEXT: Mon 10-05 Weekly Docs Audit + Monthly Housekeeping (#1909 remaining items); Tue 10-06 publish "The Contract Tested the Day It Was Born" (currently `drafted`, needs `ready-for-docs` first). Ship #063 (10-07) awaits PM voice pass, Comms template audit, then a publish-ready memo.


**10-03 22:12 STOP**: day closed. CI green, inbox 0. NEXT: Sun 10-04 04:12 publish (START heartbeat FIRST), then Mon 10-05 Weekly Docs Audit + Monthly Housekeeping.

**10-03 19:12**: STANDING RULE (PM, via Exec 17:28): never write to `mailboxes/xian (ceo)/`, PM not in to/cc; PM-needed items go to `exec` with the reason in the subject. CI green. Nothing owed.

**10-03 16:12**: CI green again (Lead renamed the 181-char path). 2 FYI memos read. Nothing owed. Tease target for Sunday still "The Contract Tested the Day It Was Born".

**10-03 13:12**: main CI RED (181-char mailbox path, Exec's retraction cc copy; mailed Exec cc Lead 1a8eb89d5; recheck next fire). 2 FYI memos read (Comms Ship #063 drafted; Exec sprint goal). Nothing owed Docs.

**10-03 10:12**: quiet fire. 2 FYI memos read→read/ (Exec Ship #063 handoff to Comms; CIO post-commit-pilot widening proposal to Pard, Docs is a candidate seat, no action owed). CI green, 1f/1g clear, criteria 12, 1c 0 candidates.

**10-03 07:12 state**: "Described Is Not Running" PUBLISHED at 04:12; wrong hero image (PM uploaded Thursday's art) found and fixed 07:40, live-verified; Medium + LinkedIn recorded, row `distributed` (Step 1f clear). `publish-to-blog` pre-flight now requires opening the image vs alt. 10-02 omnibus + 16 activity rows done and pushed. Main CI green (14:14Z). I skipped the 04:12 START heartbeat (CXO's BELT-INVISIBLE was right); filled 07:21, owned in mail to CIO. **NEXT: Sun 10-04 04:12 publish "Distribution Is a Product Decision, Not a Marketing One" (emit START heartbeat FIRST; full re-audit, fresh #11 ledger). Mon 10-05: Weekly Docs Audit + Monthly Housekeeping.**

**CASCADE SEAT 4 COMPLETE (10-01 04:12).** Session cron retired (`CronDelete b4efbabc`, `CronList`
→ "No scheduled jobs"). This seat is **LaunchAgent-only** (`com.xian.pm-docs-cycle`, 7x/day at
`:12`). Per the `duty-cycle-tick` cron-mechanism gate: skip all CronList/re-arm content at every
fire; an empty `CronList` is the expected state, not Gap-C. **Never re-arm a session cron at STOP.**
Registry row reflects this. Exec told, Pard acked at his real inbox.

**Model note (PM, 10-02 16:3x, in conversation)**: the Fable switch on 10-01 was PM maxing out Thursday's
underused weekly tokens; PM would have switched back this morning had they felt better. **This seat is
now on Sonnet 5.5.** Eventually it may move to Opus 5.5 "when the time comes," or stay on Sonnet, which
PM says has been effective lately. Not a decision yet. Don't write a handoff doc unless PM/Pard signal a
restart. Recorded in `decisions.log` 10-02.

**10-02 STOP (22:12)**: day closed. Sunday's post proofread + queued (`ready-for-docs`, publishes Sun 10-04 04:12). Main was RED at 22:08 from Lead's 19:09 memo filename (183 chars, #1616 gate) — notice sent to Lead (`fd96cdd28`); at next fire re-run 1e and confirm it cleared, don't touch their files. NEXT: Sat 10-03 04:12 publish "Described Is Not Running" + START work (10-02 omnibus, unclosed-log nudge).

**10-02 START done**: 10-01 omnibus built (18 sessions, all 11 DAY-CLOSED — HOST's gap is fixed
at the root), activity log +18. Nothing owed today. **10-01 closed cleanly.** Big day: "What Piper Morgan Actually Is" published + Medium-distributed;
PM's "Drained on Paper" ruling recorded durably (`not-syndicated` status at every layer); PM's
unstick pass closed 5 of 12 stale Ongoing issues (1692/1806/1397/1803/1805); Q4 sweep's Docs item
done (732 memos archived, in 3 batches); glossary got tracked-state frontmatter; main went red
FIVE times (one mine) and the ruff pre-commit warning now exists and fires (verified on 2 seats).
Cascade seat 4 complete — LaunchAgent-only. Both worktrees clean, everything on `origin/main`.

**🔴 NEXT: Sat 10-03 04:12 fire publishes "Described Is Not Running"** (pre-audited clean 10-01,
tease changed after → re-verified; re-run the full 16 at publish). Then Sun 10-04 "Distribution Is
a Product Decision…" — **now `ready-for-docs`, proofread + pre-audited 10-02 17:41** (Comms's
publish-ready triaged; PM had me fix the two body "!" to periods, other irregularities intentional;
`--work-date 2026-09-01`, insight, era `the-alpha`). Mon 10-05: Weekly Docs Audit + Monthly
Housekeeping both due.

**Syndication legs owed for BOTH weekend insights (Comms correction 10-02 19:12, PM ruling):** Medium
**AND LinkedIn** each (not Medium only). **PM crossposts by hand — Dispatch route retired.** Row reaches
`distributed` only when both URLs are in; Step 1f reminder to PM should name both platforms.

**PM directive still standing: do NOT self-throttle on approved/real work.**

**Crosspost-reminder mechanism (09-29, PM-ratified in conversation) is durable, not memory-only.**
`update-calendar` SKILL.md v1.5 carries the reminder at the blog-first-publish step;
`duty-cycle-tick` SKILL.md v1.42's Docs-only **Step 1f** re-checks every fire for any calendar row
published in the last 7 days still at `status=published`. Live-tested clean twice now (correctly
empty both 09-29 evening fires). Two memory pins point at these mechanisms rather than standing
alone: `feedback_remind_pm_to_crosspost_unsyndicated_publications` and the general
`feedback_prefer_visible_portable_repo_backed_mechanisms`.

**They/them pronoun ruling (PM, 09-29 evening) is durable**: `blog-style-guide.md` v1.1 + a new
template-audit check #12. No separate memory pin needed — the git-tracked guide already carries it.

**Website deploy note**: the site is Vercel-deployed (confirmed via response headers); the GitHub
Actions "Deploy Piper Morgan Website to GitHub Pages" workflow is stale/unused (last run 07-21) —
don't check `gh run list` there for deploy status; live-verify by actual body content after a short
poll instead.

## Active threads

- **Weekly Ship #062 — FULLY DISTRIBUTED 09-30** (blog live + LinkedIn crossposted, both PM-
  provided/confirmed). PM caught a real miss (sat ready+audited since 09-27, nobody checked
  "queued + pubDate arrived" this morning) — fixed the process gap, not just the one post, via new
  `duty-cycle-tick` **Step 1g** (v1.43), which mechanically re-checks this every fire going
  forward. Thread fully closed, no further action.
- **"Described Is Not Running" (Sat 10-03) — pre-audited clean 10-01; Step 1g publishes it at the
  04:12 fire Saturday.** Footer tease was changed AFTER Comms's publish-ready (PM closed an empty
  Sun 10-04 slot: "Distribution Is a Product Decision…" moved 10-10→10-04, "No Undo" 10-11→10-10) —
  new tease verified against the calendar's actual next non-Ship row. Re-run the full 16 at publish.
  "Distribution" (Sun 10-04) is `drafted`, needs PM voice pass + art — Comms will send a separate
  publish-ready; Step 1g flags it Sunday 04:12 regardless.
- **"What Piper Morgan Actually Is" — PUBLISHED + Medium-distributed 10-01** (live-verified by
  body content; Medium URL recorded 08:20). LinkedIn leg optional per building precedent. Step 1f
  will keep flagging it for 7 days — that's correct, not a gap.
- **"Drained on Paper" — CLOSED 10-01 by PM ruling.** Not to be backfilled ("Medium is not the
  canonical version of the series"). New terminal status `not-syndicated` built at every layer
  (`a18e8e81d4`: validator, `update-calendar` v1.6, row, `decisions.log`). 1683 commented, Exec/Comms
  told. **If this resurfaces from any role, point at `decisions.log` 2026-10-01 — do not re-ask PM.**
  The meta-lesson PM named: the ruling existed since ~08-30 and nobody recorded it, so it was asked
  four times. Any PM ruling goes to `decisions.log` the same turn it's made.
- **PM's unstick pass (10-01)**: closed 1692, 1806, 1397, 1803 (+1805 if the subagent lands
  clean). **1392 awaits PM's one-line call** (keep/drop the second mailbox image). Next candidates
  if PM wants more: 1779 (morning-standup `--with-issues` flag — verify CLI state), 1780
  (issue-intelligence-api.md documents a disposed class — archive with banner). **PM also said
  the agent-assignment convention still needs deciding** — proposed `lane:{role}` labels in chat;
  PM/PPM's call, don't implement unprompted.
- **1908 (mine, 10-01)**: PM's floated sequential-narrative-order field for building posts. "Food
  for thought, not urgent," not ratified. Needs PM/Comms/Web before any build — watch, don't chase.
- **Personhood/attribution division of labor with Comms — PROVEN across 4+ pieces, keep using it**
  (Comms owns `template-audit` check #11 at draft time; Docs owns an independent re-check at
  proofread time on every future proofread).
- **#1904 filed (mine, 09-28)**: 3 procedural docs 300+ days stale, describing pre-Fly-migration
  state as "Production Ready." Not mine to fix (needs technical verification against current code)
  — watch for disposition, don't chase.

## Watch surfaces (owned by others, checked periodically — don't re-derive, don't chase)

- **`last_verified` bulk-stamp cluster** — CIO's lane (#1726). 13 of 38 clustered on the identical
  2026-06-19 stamp as of 09-28's audit. Check again at next Weekly Docs Audit (10-05).
- **#1644** — roadmap.md full historical fold, PPM's lane. 16 days stale as of 09-28's audit,
  reported not fixed. Not mine to force.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **#1710/#1847** — pattern-catalog Status-field frontmatter regression, routed to CIO/Arch.
- **#1720/#1721** — filed by me, triaged by PPM into FLYWHEEL. Watch for progress.
- **CXO's marker-provenance-field finding** — CIO's lane. Watch for the fix landing.
- **GitHub issue backlog health**: 217 of 288 open issues (75%) inactive 30+ days, as of 09-28's
  audit — report as a ratio at each audit, not mine to triage individually.
- **#1901** — closed same-day 09-29 by Lead/CXO. No further watch needed.
- **Deployment pipeline (§4e/§4f)**: fully built, reviewed, fixed, re-reviewed 09-29 (Arch/Pard/
  Lead/Exec). Nothing left but PM minting two Fly tokens + a GitHub environment reviewer, whenever
  convenient. Not mine to track further — Exec/Lead's lane.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (owed since May) — real design work, scoping before
  implementing, not a same-fire patch.
- **"Two of Me" art-audit gap** — publish audit checks image existence/dimensions but not
  image-content-matches-alt-text. No process fix yet, not urgent.
- Owed by Web: `piper-morgan-website#37` publish Step 9 automation. Not urgent.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Day-of-week duty triggers — check every START

- **Every Monday**: Weekly Docs Audit — #1938 closed 10-05; next due 10-12.
- **First Monday of month**: Monthly Housekeeping — #1937 closed 10-05; next due Nov 2.
- **First Tuesday**: Skill-Candidates Review — not mine.
- **Every START**: omnibus production + missing/unclosed-log nudge (Step 1d, PM ruling 09-25) —
  produce/verify the prior day's omnibus; nudge any role whose log lacks a genuine closing marker.
- **Every 60 days, or when the acronym lint trips on a missing term**: re-verify the glossary and
  bump `last_verified` in its frontmatter (added 10-01; `max_age_days: 60`, next due ~11-30).
- **Every fire**: Step 1f crosspost-reminder check (09-29) — any calendar row published in the
  last 7 days still `status=published` gets flagged. **Every fire**: Step 1g past-pubDate publish
  check (09-30, new) — any calendar row `queued`/`ready`/`ready-for-docs` with `pubDate` already
  arrived is unblocked work to drain same-fire, not a line to defer.

## Standing operating knowledge (current rules, not incident history)

- **At every proofread, re-run `template-audit`'s full 16-check list myself, including check #11**
  — don't just read Comms' publish-ready memo and trust "clean."
- **Check line endings (`xxd`/`file`) on any UNFAMILIAR CSV before writing with the `csv` module**
  — `piper-morgan-website`'s `data/blog-metadata.csv` uses CRLF; the product repo's own calendar
  CSV uses LF and is fine with the existing pattern.
- **A "silent, account-wide GitHub API rate limit" is real and distinct from an exhausted personal
  quota** — verify via `gh api rate_limit` before assuming either way.
- ⚠️ **Emit the heartbeat every fire** — chained onto the same closing block as the final push of
  each work unit.
- **GitHub-criteria line** (third work-queue source): `gh issue list --search "label:documentation"
  --state open --limit 50` — open each result, don't trust the list view.
- **PM crossposts to Medium/LinkedIn manually.** When PM provides a syndication URL, record it —
  not a delegated pipeline step. The reminder-to-PM half of this is now the Step 1f mechanism
  above, not a manual thing to remember. **If PM rules a specific post won't be backfilled, the
  status is `not-syndicated` (terminal) — written only on PM's explicit per-post say-so, never
  proactively** (10-01).
- **Only cc PM on memos that** (a) contain a decision only PM can make, (b) relay a PM ruling, or
  (c) contain something PM would want to contradict. **PM does not read mailbox memos** — a cc
  there doesn't actually inform PM; surface real findings via carry-forward for direct mention, or
  in-conversation. Caught myself cc'ing PM on undelivered-in-practice memos twice on 09-29 —
  drop the cc rather than repeat it.
- A subagent's/colleague's self-reported verification pass is a claim, not a fact — re-verify the
  artifact yourself every time.
- **After issuing a `gh issue close` (or any state-changing command), verify the actual resulting
  state directly** (`gh issue view --json state`) rather than trust the command's exit code alone.
- A live-page 200 status can be a stale cached shell — always do an actual content check after the
  200; `curl -s` doesn't follow redirects by default, add `-L`.
- A naive `cut -d','` on a CSV with quoted fields silently misaligns columns — use the `csv` module
  for any real read, not just writes.
- `mail-send.sh` needs BOTH the old (deleted) and new (moved-to) path passed for a triage move.
  Doesn't advance local HEAD — `git merge origin/main` before assuming a triaged file "didn't move."
- `gh issue list` defaults to a 30-item limit if `--limit` is omitted.
- Before starting any audit/analysis task on a tracked GitHub issue: `gh issue view --json comments`
  first, not just the issue body.
- A cron cadence change needs BOTH the explicit session-log id-transition note AND the
  `duty-cycle-registry.tsv` row updated in the same commit.
- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — re-sync
  if meaningful time has passed, including mid-conversation with PM directly engaged.
- "Last scheduled fire of today" is arithmetic on the cron expression, not a feel-based judgment.
- A fire is a WAKE, not a time-box — drain unblocked work.
- **Writing directly to `mediajunkie/designinproduct/docs/mail/` is the preferred route for
  anything addressed to Janus.** For Pard, the real inbox is `~/Development/mediajunkie/docs/mail/`
  (NOT `mailboxes/pard/`, gravestoned and hard-refused by `mail-send.sh`) — sync that repo first,
  stage only your own file by explicit path.
- **Never csv-round-trip `dev/active/duty-cycle-registry.tsv`** — use targeted plain-text line
  replacement (match on the `role\t` prefix).
- **Run ruff before pushing ANY `.py` edit.** The armed common-dir pre-commit now warns on drifted
  staged `.py` (CIO, 10-01, live-verified on this seat) and names the binary:
  `~/.cache/piper-morgan/ruff-0.6.9/bin/ruff` (built by `scripts/ensure-ruff.sh`, CI-pinned). Heed the
  warning — it's advisory, and main went red four times on 10-01 from format-only pushes.
- **`mail-send.sh` + zsh: never pass a `$VAR` holding several space-separated paths** — zsh doesn't
  word-split, the script sees one bogus path and refuses. Pass each path explicitly or use an array.
- **Big `mail-send.sh` batches lose the push race** — >~500 paths takes ~2 min per rebuild and
  the cohort pushes faster than that in daytime. Split by quarter/batch (<500 paths each).
- **Chain `gh issue close` AFTER the push is verified landed, not alongside it** — a rejected
  push in the same command chain doesn't stop the close (10-01 slip).
- **autoclose-guard gotcha recurs on Ship numbers** (`#058`, `#062`, etc.) — a close-keyword near
  a `#NNN` triggers the guard even when the number is a Ship number, not a GitHub issue. Write the
  number without `#` in commit messages when this comes up.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

- **10-08 08:5x**: non-Piper mailboxes request DONE (see session log). Reply to Janus delivered direct to designinproduct (`aa0dd5a`), Exec cc via mail-send. Nothing owed on it unless Janus/xian answer on `reply-to:`. First real cross-repo-direct delivery: watch whether Janus replies (the new rule's first test).
- **10-08 09:2x**: PUBLISH Sat 10-10: "No Undo" (insight, slug no-undo, workDate 2026-07-05). Pre-flight done early. Re-sync + re-read alt/draft before publishing (Comms may change alt-text semicolon per PM). Then Step 1f crosspost reminder.
- **10-08 11:3x**: `reply-to:` adopted (xian via Janus). Every Docs memo from now carries `reply-to: piper-morgan-product:mailboxes/docs/inbox/`; replies to my memos land there. mail-send.sh now warns on a missing one. Reply to Janus cc Exec delivered direct to designinproduct. Watch: Janus replying to that path (first return-path test).
- **10-08 11:5x**: Janus reply landed in my inbox via the `reply-to` path (first return-path test passed). Closed the 'watch for Janus reply' item. Ted's 04-04 memo was already answered 06-01, so my delivered copy ('...unanswered...' in its filename) was moot; Janus records the correction, no rename. Nothing owed to Janus.
