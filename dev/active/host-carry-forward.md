---
last_updated: 2026-10-10
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-10-09 14:2x PDT (restart refresh, day 77 on Amber; 10-08 06:3x block below is older; the frontmatter above is the checkable claim, this prose line is not). · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

**Cadence**: LaunchAgent seat 7 (`com.xian.pm-host-cycle`, `26 6,9,12,15,18,21`). There is no session cron; `CronList` always reads empty and that is expected. The registry row (`dev/active/duty-cycle-registry.tsv`, host row, col 2) is the cadence source of truth.

OWED[key: host-pm-attention-count; to: cio; by: trigger: xian or Exec asks for it, or the next 360 round (v0.6) asks what HOST measures]: propose or build the per-fire count of rollup 'waiting on PM' items and their age; read from the rollup, not the carry-forwards. Filed 2026-10-13.
OWED[key: host-360-v05-owner-lines; to: exec; by: trigger: owners of candidates 1-7 reply, or xian asks for status]: collect one line each from owners of the seven candidates (cohort memo 10-13); report agree/change/no per candidate to Exec cc CIO. Filed 2026-10-13.
DONE-1015 (minted X1NZ…WBHA, file to Web) OWED[key: host-oauth-invite-mint; to: exec; by: trigger: xian adds the mint rule on the HOST seat and is present in the pane]: mint ONE alpha invite for Web's OAuth-only test account (dry run, then `--apply` once); write only to `~/.piper-shared/host-mint-credential-oauth-test-<date>.txt` (0600); masked form to Web, Exec, CIO; tell Web the file name. Asked via Exec 2026-10-15; not done, blockers: no `mint_prod_invite` rule on seat, no fly in wake fires. Filed 2026-10-15.
DONE-1014 (reset to 25d96342a1, replied; unfrozen 09:02 10-14) OWED[key: host-history-rewrite-reset; to: exec; by: trigger: Exec freeze mail 22:30 PDT 10-13 (runbook v2) and step 6 mail]: reply ONCE by 22:45 with `git status --short | wc -l` (expect 1: untracked settings.local.json.bak-20261012T170337, not mine) and unpushed count (0), then do NOTHING (no commit, push, mail-send, heartbeat, clean, stash) until step 6; on step 6: fetch, confirm status empty, `git reset --keep origin/main` on claude/host-cycle (--hard is denied), reply 'reset to <sha>'; wait for 'unfrozen' before any push. Filed 2026-10-13.
DONE-1013 OWED[key: host-fly-attended-check; to: exec; by: trigger: xian is in HOST's pane; xian chose B 10-13 so the installed file stands and deploy is expected refused]: run `fly status -a piper-morgan` (expect no prompt), `fly logs` (expect prompt, decline), `fly deploy` (expect per the revised file); report to Exec cc CIO. Read-only parts may run earlier if xian says so. Filed 2026-10-12.
OWED[key: host-pat-invite-mint; to: pa; by: trigger: xian re-adds Bash(scripts/mint_prod_invite.sh:*) on HOST's seat]: dry run, mint ONE (--apply), raw in 0600 roster only, mail PA cc Exec the masked form; PM's go relayed via PA and Lead 10-11
OWED[key: host-alpha-inbox; to: exec; by: trigger: xian grants read-only Gmail on HOST's seat and confirms which account receives alpha@]: start watching alpha@ each fire; report sender first name, date, subject, gist to Exec only; never send. ROUTE (xian via Janus 10-11): alpha@ is an alias of xian's pipermorgan.ai address, forwarded to a designinproduct.com address and delivered by catch-all to his designinproduct.com inbox; my connector must be signed into THAT Google account (unknown until the first read). Interim: Janus checks at 05:07, 14:07, 20:07 and relays; stops when my seat can read.

**10-10 15:26 wake**: e2e lookup check is RIPE (both commits in deployed `dd5b7c702e`, file (A) installed); blocker = needs a person in conversation for the ask click; notice sent to Exec. Whether the ~15:00 reboot happened is unverified by me; this fire ran normally.

**10-10 14:0x PRE-REBOOT (day 78)**: Amber reboots ~15:00 PT (Pard). State: the ask rule DID fire (my 10-09 evening `fly secrets list` froze the seat until someone cleared it ~12:55 on 10-10); **my standing rule now: no fly commands in scheduled or mail-wake fires, only with a person in the conversation** (CIO recommends keeping the ask file, xian's yes/no on keep-ask vs file (B) still his). Answered Exec's OpenAI ask (no server OpenAI key on prod; stored user keys and 429 history UNMEASURED) and Lead's Anthropic-workspace ask (unmeasured by me; xian says the limit was raised). Sev O. added to the gitignored roster as recruiting-list only, no invite, no code (Exec: none until xian says). 10-09 log closed (DAY-CLOSED); 10-10 log is `dev/2026/10/10/2026-10-10-1300-host-code-log.md`. Inbox empty. Still gated on others: post-deploy e2e lookup check (needs a person present for the fly click), Janne and Savanna sends, roster flips, fielding 1b on Agent 360 v0.6. First post-reboot fire is 15:26: expect it to find a quiet inbox, no fly.

**10-09 14:2x RESTART (day 77)**: Pard restarted this seat at Janus's request so xian's `.claude/settings.local.json` loads (four `ask` lines for `fly`/`flyctl` forms, one `deny` for a retargeting `-` flag after the quoted `-C` command; valid JSON, read by me). The restart also cleared my one-session mint-wrapper approval, so `scripts/mint_prod_invite.sh` may be classifier-denied again. **I have not run any fly command since the restart; whether the ask rule fires is untested, and my first fly command (the post-deploy e2e) is the live test, with xian clicking.** Do not write rules myself.
**What happened 10-09 (all in the session log)**: Row F mint for Web done (`65G9…2BPV`); Janne `C048…Z3JW` and Savanna `EHAB…JWF2` reissues minted, UNUSED, sends are PM's hand; lookup payloads approved from the trust side; both shell probes on xian's "HOST, go" CLEAN (no remote shell on `fly ssh console -C`; not measured for `|`, `&&`, backticks, redirects, newlines); Agent 360 v0.5 synthesis sent (11 of 11); #1967 owed-scanner marker accepted by CIO, `scripts/owed-scan.py` built, pilot HOST+Exec 10-09 to 10-16.
**OWED markers (pilot; same text as the log)**:
DONE-1012 OWED[key: host-e2e-lookup; to: arch; by: trigger: a deploy carrying b4dbf72025 and 9e1fa372cb, and permission file (A) installed]: post-deploy end-to-end lookup check, run once, paste output (`prod_user_lookup.py a; echo SHELL_RAN`, expect a "refusing" line and no `SHELL_RAN`)
OWED[key: host-roster-flip; to: exec; by: trigger: Exec says the day xian sends the Janne and Savanna codes or either is used]: flip both roster lines the same day
OWED[key: host-fielding-1b; to: exec; by: trigger: Agent 360 v0.6 is fielded]: fielding memo asks for a dated row on receipt, plus a mid-window reminder ALSO (10-13, CIO): drop the per-seat hook question from v0.6 and point at scripts/whats-armed.sh.
**Next wake**: 15:26 PDT LaunchAgent.

**10-08 evening**: Themis's sent-mail read is IN and folded (see log); (b) below is resolved except ONE yes/no pending: did Janne get a working code after 09-22? Savanna reissue still owed. 5 recipients unnamed. Profile refresh filed as standing item.
**10-08 ~17:5x wake (supersedes the 09:26 block's blocker)**: xian relay says roster/files/logs FIRST, then a short Gmail search. DONE: list built and sent to Exec (cc Lead, Web) with two Gmail searches for xian (`b223894f1`). **OPEN: (a) Row F mint: approved by xian but `scripts/mint_prod_invite.sh` dry run is classifier-denied on HOST and Lead seats `[Secret-Store Writes]`; PM must add `Bash(scripts/mint_prod_invite.sh:*)` to ONE seat (awaiting which). When allowed: dry run, `--apply` one code, output to 0600 file in `~/.piper-shared/`, record masked form on roster, give Web/Exec masked only. (b) xian pastes recipient names/dates from the two searches, then fold into roster. (c) outside-account match pending PM's lookup result.** Reply memos need `reply-to:` frontmatter.
**10-08 09:26 wake**: PM said YES (via Exec 07:05) to my reading his sent mail; sent Exec the recruiting list's roster half, but the Gmail read itself was **denied by the permission classifier (PII Data Handling)** and so was a roster re-read. **OPEN, blocker named: PM adds a read-only Gmail permission for HOST's seat, or pastes the names; then I run ONE sent-folder search (alpha/beta/invite, since 06-01, subjects and recipient names only) and send Exec names and status only (no emails, no text, no codes).** Do not route around the denial via other Gmail tools. Also unverified: whether Savanna's original invite was ever sent (the sent-mail read answers it).

**10-08 START (day 76)**: Exec acked my no-spare-invite answer (mint on PM's board, rollup v67 item 4); nothing owed. Architecture Enforcement green again (12 of 12 workflows green at 06:26). Re-verified: Agent 360 still 8 of 11 by proxy, no new rulings on invites/usage in `decisions.log` since 10-07. Still waiting on: mint's masked form for Web (record on roster same day), outside-account identification result, Exec's word on PM's yes/no for reading his sent mail.

**10-07 (day 75)**: all six fires on slot. Two roster answers for Exec: outside-account is not on the roster (PM's identification query pending, nothing owed until relayed); recruiting status list sent (R. in, L. and B. reissue-pending); **no spare unused invite exists for Web's row F (#1913), a mint is needed, PM's hand** (sent 21:3x to Exec cc Lead). **Watch for**: Exec relaying PM's identification query result for outside-account (match against roster, no action before), the mint's masked form for Web (record on roster same day), and Exec's word on whether PM said yes to my reading his sent mail 07-12 onward (do not start before). I printed one full burned invite code into my own tool output while grepping the roster; disclosed in the memo; mask in the first command next time. Architecture Enforcement was red on main at 21:26 (not my lane, cause not investigated). Agent 360 still 8 of 11. Mail empty at STOP.

**10-06 (day 74)**: all six fires on slot, all quiet holds. One Exec cc triaged (PM-approved 95% weekly-usage stop line; at 95% of the meter stop non-essential work and tell Exec; window ends Thu 10-08 21:59 PDT). Agent 360 still 8 of 11. Mail empty twice at STOP; nothing owed.

**10-05 (day 73)**: all six fires on slot. Re-probed #1934's shipped fix (14 of 14 shapes block). PM's burn ruling for `ZVHW…8B35` relayed by Exec; my seat was classifier-denied, Exec ran the dry-run on Fly (`matched unused rows: []`), I marked the roster and told Exec at the 15:26 wake. Redeemed-vs-deleted stays unexamined. Agent 360 still 8 of 11 (no new response all day). Mail empty twice at STOP; nothing owed.

**10-04 (day 72)**: all six fires on slot. Delivered the trust read of the commit-message bearer guard (#1934 filed, Lead's lane). Caught and owned one error of mine: I repeated "synthetic, never minted" about a fixture that was Janne's real `ZVHW…8B35`, without checking the roster. Answered Lead's roster question from the roster (sent 09-21, never redeemable, void since 09-21; burn is PM's hand). Agent 360 stayed 8/11. STOP: one Exec cc triaged, mail empty twice after.

**10-03 (day 71)**: quiet apart from two Exec broadcasts (sprint goal locked, PM mailbox retired) and a peer-row finding mailed to Web/CIO (registry CSV-quote artifact, not HOST's row).

**10-02**: Ship #063 workstream review filed same-day as kickoff (window Fri 09-25 → Thu
10-01) — `mailboxes/exec/inbox/workstream-063-host-2026-10-02.md`. Writing it surfaced a real,
separate finding: `ROLE-PORTFOLIO-HOST.md` §2 had gone **three weeks stale** (last touched 09-11,
untouched across workstream reviews #060/#061/#062) despite the doc's own 2-week staleness rule and
a mechanical check that evidently isn't gating this file. Refreshed it same-fire, flagged the
mechanism gap to Exec/PM in the review itself rather than silently catching up without comment.
**Exec then bounced the review back, correctly**: no `Verified how:` line (the one requirement
HOST itself holds other roles to), and no explicit answer to PM's product-delta frame (silence
instead of a stated "none," when four other roles gave exactly that honest answer). Fixing it
surfaced a **third, self-found error**: the review claimed CIO's Agent 360 response landed 10-02,
outside the window — checking the actual commit/frontmatter timestamp showed it landed 10-01 at
16:11 PDT, inside the window, making the correct window-close count 8/11 not 7/11. Sent a single
addendum covering all three rather than silently edit the delivered review.

**Day before (10-01)**: Docs caught the `DAY-CLOSED` marker gap on my own logs two days running
(09-29, 09-30); root-caused and fixed (the STOP-entry habit was stopping one line early). CIO's new
NO-DAY-CLOSE detector then found the real gap was six days, not two — see standing hazards below.
PM engaged directly on Agent 360 v0.5, corrected my approach twice in one exchange (start the
analysis sooner; then hold the finished synthesis for completeness) and directed HOST complete the
questionnaire too, as an 11th response. Full detail in 10-01's session log and `#1895`.

## Standing hazards (durable behavioral guidance, not time-bound)

- **The STOP entry's LAST line, every time, with nothing after it: `<!-- DAY-CLOSED: {date} -->`.**
  Missed two days running (09-29, 09-30) because the habit stops at "Cron: armed... next fire
  HH:MM" and treats that as the natural end — it isn't; the marker is one more line after it, not
  part of the cron sentence. Check this specifically before considering any STOP fire done.
- **Step 0's "verified DAY-CLOSED" means actually grepping the anchored marker, not reading the
  prior day's STOP prose and judging it sounds closed.** CIO's NO-DAY-CLOSE detector (10-01) found
  six real days (09-23→09-28) where every morning's Step 0 line read as verified while the marker
  was simply absent — the self-heal had never once checked the thing it exists to check. Fixed
  going forward (five correct days since 09-29), but the lapse was structural, not a typo.
- **Verify at the mechanism, not the announcement** — especially when the announcement points at
  *less* work.
- **Re-verify carried claims, don't restate them.** An item marked "unconfirmed" or "watching" is
  a claim to re-check against its actual source, not a status to keep copying forward.
- **Match your measurement's scope to the question** — before quoting a number, say what the
  denominator is and what it structurally cannot contain.
- **A predicate is a derived artifact** — enumerate the real corpus before writing one; don't
  hand-write a pattern against an imagined format.
- **PM mailbox retired (Exec broadcast 10-03 17:28).** Never write to `mailboxes/xian (ceo)/`; PM is
  not in `to:`/`cc:` of any new memo. Anything needing PM goes **to `exec`**, subject names which of
  the three: PM-only decision / relayed PM ruling / something PM would contradict. The 09-11
  three-condition cc rule is retired. Mail already in flight that cc's PM is sent as written.
- **Never delete a memory to fit the index.** Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**
- **Never write your own cadence from memory** — read the registry row live (not `CronList`
  anymore — see below, `CronList` is now expected to always read empty).

## Cron

**Mechanism changed 10-02: LaunchAgent only, no session cron.** `com.xian.pm-host-cycle`,
`26 6,9,12,15,18,21` (6x/day), boot-persistent, external to this session. `CronList` will now
always correctly read "No scheduled jobs" — that is NOT a gap, do not re-arm a session cron on
seeing it. The registry row (`dev/active/duty-cycle-registry.tsv`, `host` row, col 2) IS the
cadence source of truth going forward; there is no `CronDelete`/`CronCreate` rotation to do at
STOP anymore. If the prompt's `cron=` constant ever disagrees with the registry row, that's a
real finding (the generator reading a stale registry), not something to silently paper over.

## Standing cadence work

- **Role Health Check** — 4-weekly, self-polling via GH Actions (`label:sapient-trust`). **Closed
  today** (`#1902`) — 9 Low, 1 Medium, 0 High/Critical. Calendar updated same-fire. **Next due
  ~10-26.**
- **Role briefing** (`docs/briefing/BRIEFING-ESSENTIAL-HOST.md`) — refreshed 09-22 (Docs's
  staleness flag; caught a real operating-model error, not just a dated section). Has
  `last_verified` frontmatter now; keep it moving when it drifts rather than let it sit another
  3 months.

## Open threads

- **10-08 close state (21:26 STOP), all blockers outside HOST:**
  - **Row F mint for Web (#1913) — DONE 10-09 09:33 PDT**: xian added `Bash(scripts/mint_prod_invite.sh:*)` on HOST's seat; dry run clean, `--apply` 1 token (prod rows 12 -> 13), masked `65G9…2BPV`, raw only in `~/.piper-shared/web-row-f-invite-2026-10-09.txt` (0600). Roster recorded; memo sent to Exec cc Web, Lead (`76a390a3d`). **Watch for**: Web saying the code is consumed, then flip the roster line to used the same day. Unverified: that the code redeems (not tested by me).
  - **Janne** (he/him; my earlier "her" was wrong): no prod account (xian's read 09:49 10-09). Fresh code minted 10-09 ~10:0x PDT, masked `C048…Z3JW`, UNUSED, raw in `~/.piper-shared/janne-savanna-reissue-2026-10-09.txt` line 2 (0600). **Send is PM's hand**; flip the roster line to used when Exec relays that he signed up.
  - **Savanna**: owed reissue minted 10-09 ~10:0x PDT, masked `EHAB…JWF2`, UNUSED, same file line 4. Original 07-13 send never verified. **Send is PM's hand.**
  - **Lookup payload review — DONE 10-09 ~11:5x PDT**: approved from the trust side (`23debc3be`); `--all` OK with conditions; flags sent: (1) probe 'no remote shell' with a benign `; echo SHELL_RAN` after deploy, (2) `--burn-unused` widens the mint grant vs the old wrapper. **Watch for**: Lead/Exec reply on flag 2; xian adding the fly-form rules on my seat (do not write them myself); deploy carrying `b4dbf72025` + `c2adbd926d`; run prod commands from a default-mode session after the swap.
  - **outside-account — RESOLVED 10-09**: = an outside alpha tester xian identified (name and email stay out of this public repo: private memo in designinproduct, mapping only in the gitignored roster). Used `3MTN…BN12`, the code PM emailed him 07-12; not a HOST mint (roster starts 09-13). Exec's "unissued code" question closes as no. Prod users: 7 (2 outside humans).
  - Roster (gitignored) carries Themis's names for the 07-12 sends; tester profiles refreshed 10-08 (done).
  - Usage window ended 10-08 21:59 PDT; read the next meter figure before any heavy work.
- **`#1885` burn + reissue** (09-24, timeline updated 09-25) — burn is live this sprint week (PM-
  authorized, Lead's to execute); **reissues (Savanna, Janne) explicitly deferred to next week** by
  PM ruling ("not urgent... wait til they try and fail"). **HOST re-records both on the roster the
  same day they're minted** — not before, don't chase it, watch for Lead's mint memo.
- **R5(1) answered 10-04** (to Exec, cc Lead): commit-subject token `QGQP…KJGP` burned 09-26 by PM, Google key deleted 09-25; nothing left on it. Still open adjacent: Savanna/Janne reissues (HOST re-records the roster same day minted; check Savanna's original send-status first). Spec's R5 items are Lead's. **Trust read of the commit-message bearer check DELIVERED 10-04 15:32** (to Lead, cc Exec): sound on `-m`, misses `-am`/`--message`/`-F`/`git -C` and a block shows no reason. Filed **#1934**, priority is Lead's and Exec's. Also told them the R5 landing sha in their memos (`7ba6415ec4`) is a heartbeat commit; the change is `23e4cefcbd`. **Correction 10-04 18:35**: my 'synthetic, never minted' claim in #1934 and that memo was WRONG (the fixture was Janne's real `ZVHW…8B35`, void on the roster since 09-21); corrected by comment and memo. Answer sent to Exec cc Lead: sent 09-21, never redeemable (wrong DB), current Fly row unverified, burn is PM's hand — **watch for PM's burn, then mark the roster line the same day**. **#1934 CLOSED 10-04 15:53 PDT by Lead (`786bbda020`); HOST re-probed the shipped fix 10-05 06:3x: 14 of 14 shapes now block, reason on stderr, live harness probe blocked (comment `#issuecomment-5995450364`). No `commit-msg` git hook exists in the common dir, so the guard stays PreToolUse-only and advisory. Nothing owed.** CIO's guard-pm-checkout notice read, nothing owed.
- **Burn of `ZVHW…8B35` — CLOSED 10-05.** PM ruled burn (Exec relay 08:58); my seat was classifier-denied; Exec ran the `--burn-unused` dry-run on Fly (target `piper-morgan-db.flycast:5432/piper_morgan`): `matched unused rows: []`, `--apply` not run, nothing to delete. HOST marked the roster 10-05 ("no live unused row", masked only) at the 15:26 wake and told Exec. **Still unexamined**: whether the row was redeemed or already deleted (script matches unused rows only). Do not chase; PM's ruling was that we'd hear if anyone used it in good faith.
- **Agent 360 v0.5** (fielded 09-25) — **11 of 11 in, synthesis DONE 10-09** and sent to Exec
  (`mailboxes/host/sent/memo-host-to-exec-agent-360-v0.5-synthesis-2026-10-09.md`, pushed `9653df733`,
  kind: needs-PM decisions (a) PM-hands queue/mint delegation, (b) briefings maintain-or-retire,
  (c) cohort-share go). #1895 commented. Follow-on issues: #1967 (owed-item scanner, HOST+CIO),
  #1968 (tooling follow-ons for CIO). **Watch for**: PM's answers via Exec, then the
  what's-worth-changing step. **HOST-owned, not yet done**: fielding process change (dated row on
  receipt + mid-window reminder) goes into the questionnaire/fielding procedure before v0.6;
  route PPM's three implicit PDR candidates to Arch and CIO's probe/venv items to Lead/Pard (via #1968
  for now). Cohort-share waits on PM's framing clearance. The 10-01 working notes are superseded.
- **Classifier bucket-split** (the `auth` error bucket, `_classify_llm_error`) — ruled and copy
  drafted as of 09-15, status of the build still unknown. Not HOST's to build; check for movement
  if it comes up.
- **`#1731`** — CLOSED 09-25 (mechanism reproduced, send-side guard `fe92cd9aaa`). Dropped from watching.
- **ESSENCE.md v0.1 trust-lens** — given 08-29. Watch for Lead's watched round adding the
  inversion-path test.
- **Weekly reflection section** (Exec's proposal, CIO-ratified 09-18) — a ~150-word subjective
  reflection rides the sprint-closeout template now. Include it in HOST's next closeout.

## Watching, not owed

- **#1539 ruled partial, not sufficient** (08-10) — the legibility half (what uncertainty a reply
  is answering) is still not concrete on HOST's own end. If it comes up again, that's still true.
- **A fifth mailbox header format found on HOST's own corpus** (08-10, Pard's inline-arrow
  notation) — reported to Comms, not HOST's to fix.
- **PM's 10-05 BYO-key ruling** (`decisions.log` ~17:20, Exec relay): Piper provides no LLM service, users bring their own key for web GUI and hosted-LLM features. Nobody asked HOST. A user-supplied key is a stored bearer credential, so key custody (where it lives, who can read it, redaction in logs and errors) is a trust property in HOST's lane. Not owed; if it comes up, or when the BYO-key feature is built, read how keys are stored before anyone calls it safe.
- **Usage stop line (Exec cc 10-06 17:26, PM-approved)**: at 95% of the weekly meter, stop non-essential work and tell Exec. Meter read 71% with the week about 68% elapsed; window ends Thu 10-08 21:59 PDT. HOST fires are quiet holds on a mid tier; keep stated dispatch tiers and no fan-out without a reason.

- **10-09 ~12:1x — Lookup-rule install is ON HOLD (Arch).** Pard does NOT install until the no-remote-shell probe result (`fly ssh console -a piper-morgan -C "echo a; echo SHELL_RAN"`) is on main. I offered to run it on Exec's go (not on my own authority). Burn split (option b) is Lead's to schedule; mint swap memo to xian waits for it.
- **10-09 ~12:2x — Updates.** Probe: waits for xian's one word (HOST go / Pard runs / xian runs) via Exec; I do NOT run before it. Flag 2 (burn) RESOLVED by Lead `9e1fa372cb`. Remaining before rules land: probe result on main, then a deploy carrying the payloads. Arch suggests an `ask: Bash(fly *)` rule instead of a mode change (xian/CIO/Pard decide).
- **10-09 ~12:3x — Grant locations.** Mint-wrapper allow lives in the PRIMARY checkout's `.claude/settings.local.json` (line 14), not my worktree; applicability to my seat unverified. CIO: wrapper grant goes before the `ask: Bash(fly *)` rule. Janus's order: xian's probe go -> result on main -> CIO sends one paste-ready file -> xian pastes + restarts HOST. I write no rules.
- **10-09 11:58 — Shell probe DONE, CLEAN** (both forms, no remote shell; mailed `af5c386a5` + designinproduct). Install of the ask-plus-deny file is CIO/Pard + xian's paste/restart. Still open: post-deploy end-to-end check with the real payload (`prod_user_lookup.py a; echo SHELL_RAN`), and the mint-wrapper grant removal before relying on the ask rule. Earlier "~12:xx" log clock labels today were estimates (corrected in the log).
- **10-09 ~12:0x — Arch approval now unconditional.** HOST owes only the post-deploy e2e (`prod_user_lookup.py a; echo SHELL_RAN`), after a deploy carries the payloads and file (A) is installed; xian approves the command by sight.
- **10-09 12:3x — #1967 BLOCKED on marker convention** (no OWED line exists to scan; 3 of 64 logs' lines are a labeled form, none matching). Proposal `OWED[to:; by:]: ...` sent to CIO cc Exec (`e2e41a1a9`), #1967 commented. Unblocks on CIO's accept/amend. Then HOST adds the convention to the log/fielding procedure.

## Open OWED rows (pilot #1967; owed-scan.py matches `key:`; aging-standing-items.sh reads `Filed`)

| key | Item | Filed | Blocked on |
|---|---|---|---|
| key: host-e2e-lookup | Post-deploy end-to-end check, once: `prod_user_lookup.py a; echo SHELL_RAN` expects a "refusing" line and no `SHELL_RAN`; to Arch | 2026-10-09 | A deploy carrying the payloads (`b4dbf72025`, `9e1fa372cb`) and file (A) installed; xian approves the command by sight |
| key: host-roster-flip | Flip the roster lines for Janne and Savanna the day xian sends their codes or either is used; to Exec | 2026-10-09 | Exec telling me the send day (xian's hand) |
| key: host-fielding-1b | Fielding memos ask for a dated row on receipt, plus a mid-window reminder; to Exec | 2026-10-09 | v0.6 being fielded (briefing line added 10-09) |
| key: host-v30-tester-privacy-line | One line pointing to pipermorgan.ai/privacy in the next note the 09-21 tester gets (xian 10-16: no separate email); to Exec | 2026-10-16 | The reissue send (xian's hand) |
| key: host-design-partner-list | Who xian counts as a design partner (#2063: no invite beyond them until counsel review); HOST mints/flips nobody else; to Exec | 2026-10-16 | xian naming the list |
| key: host-scaffold-4-and-7 | Check Terms scaffold sections 4 and 7 (tell-me-when-broken; a code is yours); to Comms | 2026-10-16 | DONE-1016 (checked, reply sent) |

**10-18 07:1x**: xian ruled (via Lead relay) 10-23 = checkpoint to approve inviting partners, 10-30 stays target; outreach order: interest list first, then newsletters, very few at first. Partners still not named. A4 fresh mint for #2078 denied again on HOST's seat; xian's hand.

### 10-19 13:1x
- host-2088-interim: invites and tester instructions say the wizard asks for the code at step 3 of 5 (PPM #2088; clears when Lead moves the field). Goes in the held-send template. PPM reads today as the beta form; PPM sends Comms the line the morning of any invite. #2089 (hosted system check, Temporal line fails) is PPM's question to xian.
- host-2081-close: my word given (pass); Lead's refresh fix in flight.
- 10-19 14:5x host-2085: started. Off-Fly health watch proposed to Lead (GitHub scheduled probe of /health services.database). Owed: read-only fly command card for xian (pg check, machine status, restart policy, memory, Postgres log around 05:25), run only with xian present. #2089 now BEFORE partners (xian 14:13, supersedes 13:20); known-issue wording not needed once it lands; #2088 interim (code at step 3) holds until Lead's lane lands (CXO: code becomes step 1).
- 10-19 15:0x host-2085-acceptance: posted on #2085 (comment 6278206729). Lead builds the Actions probe after the five admitted fixes (#2091 #2092 #2094 #2095 #2096), then #2089+#2088. When it lands: check items 1-3 (forced failure email via Gmail metadata, one blip silent, healthy quiet).
- host-1386-cred: ruled yes with conditions for the warm run (sent to PA cc PPM Web Exec). Scenario A code: record masked form as spent once xian names it.
- 10-19 15:1x host-2085-flap: Exec measured /health database flapping 14:53-14:57. Read-only fly card sent to Exec for xian's rollup. #1386 canonical run is HELD by PPM until Lead or HOST says the DB is steady; do not lift it on a single /health read. Owed: read the card output when xian pastes it; Lead's pool-settings answer.
- 10-19 15:2x host-1386-hold: hold lifts on Lead's 30-read count; I asked for a stop rule (>3s or db unhealthy). host-web-1386-code: file web-1386-credential-invite-2026-10-19.txt exists; record masked form when xian gives it, mark spent when Web's run redeems. #2085 acceptance addendum posted (watch covers sustained outage, not intermittent flap).
- 10-19 15:4x host-send-gate: before releasing any held send: (1) /privacy Google paragraph live and quoted back by Web, (2) Terms text vs #2064/#2057/#2021 state that morning, (3) wizard step order served that morning. Told Comms. E8EJ…RYSG allocated to Web's scenario A (roster). Lead flips pool_pre_ping tonight after #2094; watch gets a 3-of-6 rate rule (my acceptance line stands).
- 10-19 16:0x host-stall: PPM asks xian (via Exec) whether "alpha stalls under light load" goes on the gate; HOST leans admit, close on a load re-measure. Asked PA to delete raw fly-log streams at its 21:47 STOP (confirm in its entry). /privacy live read still blocked by Vercel bot check; xian's 30-second look or Web retry; send check 1 waits on it.
- 10-19 17:2x host-tests-recheck: Tests on main in progress at fc17eab244 (earlier failures at 6c0f84dcba, 99d2ba2a53); recheck, mail Lead only if red. host-2085-watch: told Lead Actions schedules floor at 5 min; loop 5 probes inside a run. host-pard-key: answered Pard (none read pm-web-anthropic-key; three unknowns: Fly secret, Actions secret, other accounts' stored keys). #2101 admitted Class 4; Lead's bounds (5 s connect timeout, 60 s cache) ride Tuesday's promotion; scenario A and criterion 2 Tuesday.
- 10-19 17:4x host-health-watch: landed 66c3050358; forced run failed as designed; EMAIL to xian is the acceptance (Exec asking him; my Gmail search inconclusive). Still to see: first scheduled runs quiet; one-miss-in-five silent. host-pard-fly-date: asked PA (or Exec's card) for the ANTHROPIC_API_KEY secret date on piper-morgan; I run no fly. host-tests: Tests red at fc17eab244 attributed by Lead to shrink-lock fixed 3a837f20fa; recheck on a run at or after it. Arch ruled #2101 async surface via to_thread (tomorrow); Lead's process-wide cache 2acf8af82d for Tuesday.
- 10-19 18:0x host-watch-accept: NOT accepted (xian: no email for run 39347484450). Sent Exec a settings checklist and proposed an assigned-issue alert path (Lead's build, no secret). Track 2 stays open on #2085 until a forced failure reaches xian by some path. host-key-revoke: Web-key-for-testing last used 10-17 (xian); consumer unnamed; my read: (b) acceptable; xian's call. #2100 admitted (Class 3).
- 10-19 18:1x: Web-key-for-testing NOT revoked (xian: his own test key; decisions.log supersedes the 16:56 revoke step); host-key-revoke closed. Watch: Lead builds the assigned-issue backup after #2100 and tomorrow's thread surface; track 2 not accepted until a forced failure reaches xian. host-oauth-notices: Exec asked Web to count alpha OAuth authorizations since 10-15 (times only); if any is not ours, it is a security notice to HOST the same day; none received yet. Main CI 12 of 12 green at 18:10.
- 10-19 18:3x host-oauth-notices: Web (6, all dinp-machine), PA (none; lists xian's own windows) and HOST (none) answered. Open: xian's security-log match against PA's windows; any entry outside = same-day security notice to HOST (xian revokes app).
- 10-19 18:5x host-watch-accept: EMAIL leg met (run 39354889203, 18:46:35 PT, subject "Run failed: Alpha Health Watch"). Posted status on #2085. Open: one-blip-silent, assigned-issue backup (Tuesday) + its forced test. The gh default notification address is now xian's designinproduct address, which my Gmail connector reads: add a metadata-only search for "Run failed: Alpha Health Watch" to the fire routine.
- 10-20 18:1x host-test-key-print: CLOSED. Web printed the $20 test-workspace key to their own terminal; xian ruled no rotation (Exec relay 18:07). Pending, record each masked form the same hour: the Wed 10-21 alpha invite, a staging invite, and the throwaway OpenAI key ($10 cap, -credential- file for Web).
- 10-21 16:50 host-2088-interim: CLEARED. #2088 and #2089 closed (CXO 15:32, Web's five served rows on 76789a8988; code is step 1). The step-3 line and the Temporal known-issue are out of the held-send template. Send check stays: re-read the wizard order served the morning of any send.
OWED[key: host-restarter-token-expiry; to: xian; by: 2027-10-08]: restarter token `alpha-db-restarter` (Fly app `piper-morgan-db`, one-machine `rC` else `r`, 8760h) expires about 2027-10-22 13:38 PT. Two weeks before: xian mints a replacement by Arch's block and replaces secret `FLY_API_TOKEN_ALPHA_DB` on environment `alpha-db`; HOST records the new date.
- 10-22 15:5x host-restarter-token: RECORDED. Created 13:38 PT 10-22 by xian's hand on his Mac (secret on `alpha-db` at 20:38:41Z per Exec's gh api read); scope piper-morgan-db, machine 865105fe247158 `rC`, else `r`; expiry 8760h (about 2027-10-22). Caveats match (xian's report); one `checks list` read failed "unauthorized" (app-wide machine listing), handled by guard 1b on `ops/restarter` 64d611798e. No piece of the token in git or in HOST's reach. Revoke route if ever needed: `fly tokens list -a piper-morgan-db`, name `alpha-db-restarter`.
- 10-22 18:08 host-xian-away: xian away from desk, will do the App key move, and name who restarts the DB (interim line), when home tonight, worst case 10-23 morning. Until then no sends, no install. HOST checks names-only on the .pem when he says 'key stored'.
- 10-23 11:00 host-app-key-custody: RECORDED. GitHub App `piper-morgan-agents` (ID 5434481) private key at ~/.piper-shared/github-app-piper-morgan-agents-credential-2026-10-22.pem, 0600 owner xian, 1675 bytes, mtime 10-23 10:56 (names/mode/size only; contents never opened). Moved by xian's scp from faoilean; faoilean copy had sat in a gitignored repo checkout (never committed; .gitignore has *.pem); xian to confirm the faoilean rm ran. My check: no other .pem under ~/Development to depth 4; 0 tracked .pem in git. NOT YET: App installed on the repo, Pard's mint helper, xian's admin token/SSH key off Amber, acceptance bar (admin false from a seat; refused push to ops/restarter) — #2136 stays open.
- 10-23 11:00 host-2085: CLOSED by PPM 10:50 (test 3, run 39997651271, restart HTTP 200, verified healthy ~2m6s down end to end). Caveat to carry into sends: recovery waits on an approver's click on `alpha-db` (about 1 min in the test). Restarter token unchanged; rwC fallback not needed.

- host-send-checks 10-23 12:26: Calendar line is click-through plus tick-the-box until #2087 (data-access verification) is approved; the 10-22 'verified' was branding only. Check the restored wording and the 100-user cap on the send morning.
- host-xian-present-session 10-24 12:56: one session, three reads, all read-only and shown to xian first: Draft 1 (names in secure_credentials), Draft 2 only if Draft 1 has a row (with Arch's 09-21 14:08Z bound), and the served refusal check (one chat turn, an account with no key, expect refusal; Arch: that settles ANTHROPIC_API_KEY, whose only reader is a 1-token Haiku startup check). Plus the stored-key count. Blocker: xian present. Removing the ANTHROPIC_API_KEY secret is hygiene, xian's call with Lead.
