# Exec carry-forward

**Rewritten 2026-11-11 22:09 PST at STOP** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/11/2026-11-11-0601-exec-code-log.md` (closed).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake, plus v3 via `git log --since=<last> --name-only --format= origin/main -- mailboxes/exec/inbox/`. Last check 22:01 Wed 11-11. File v3 with plain `mv` + `scripts/mail-send.sh` (both paths); never `git mv` on the branch (M-3 guard).

## Rollup
v933, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus assert; for span cuts anchor both ends and assert neighbours survive. Steps for xian go in a card on the board, not in chat (his ask, 11-11).

## Where things stand (end of 11-11)
- **Main CI** 12/12 green at 22:01.
- **Ship #068** published 16:12, `distributed`. Done.
- **#2174 PASSED** 18:52 (xian, Amber). D3 governs (ADR-081, decisions.log). Build is **#2342**, placed by PPM 19:11 in PUB under #2261, Sprint PUB: (1) xian registers the published App and approves its secrets on hosts, (2) Arch rules the classic-grant cutover, (3) Lead builds with CXO's words, (4) served connect on alpha closes #2342 and #2261's code half. Lead starts the unit layer at 11-12 START in a fresh session. **#2341** script built, closes on xian's first run.
- **#2340** closed (screen scripts no longer read the keychain). Real screens wait on xian's key choice.
- **Budget:** memo to Themis in designinproduct only (f8185d229f). Never mirror business spending here.
- **Invite hold:** #2342 (xian's App registration first), #2282 (his word on Web's sign-in check), #2292 (his mail records; still only google-site-verification TXT when checked for the 19:05 reply).

## Waiting on xian (all on board v933)
1. #2292 email records (step card on board).
2. #2342 App registration + secrets word (when he is ready; no date).
3. Yes/no: #1423 Ongoing→Production move (PPM asks); #2340 key handover (rec: one capped lead-scoring key he puts in the local DB store); #2333 go (rec yes after Arch sequences); #2327 sprint (rec PPM Friday); CLAUDE.md v4 Mail line (CIO 01M760HBR0); start scripts keep-or-switch.
4. #2328 sign-in (key=value copy for PA, or sign in Web's Chrome); #2335 Fly log yes/no only; #2282 consent revoke; #2157 restore drill hour.
5. Optional: `FLY_NO_UPDATE_CHECK=1 fly image show -a piper-morgan-gh-mcp` Repository/Tag/Digest.
6. **Thu 11-12 post "The Server Has No Key"**: xian writes it Thursday morning; draft still scaffold, calendar `planned`. Check every fire.
7. Talk later: beta tester feedback (private file in designinproduct), self-hosted beta, skills, Piper self-knowledge.

## Reminders owed to xian
- #2282 step 5 around Thu 11-12 (standing item #183): remove alpha callbacks in GitHub and Google if a week passes with no hits.
- flyctl planned upgrade 11-16 (Pard upgrades, CIO regenerates fly rules).
- Thanksgiving week Mon 11-23: PPM's closing-review question. v4 review 11-23.
- Vercel downgrade once headroom exists (standing item #182).

## Mine
- Timestamps only from a `date` call in the same command (11-11: guessed twice, both caught).
- Review slot every START: re-read one claim from the last 24 hours against its source.
- Calendar check every fire. Run `scripts/aging-standing-items.sh exec` at START.
- Relay xian's rulings at once; decisions.log + mail the same hour.
- DAY-CLOSED in grep form as the log's last line.
- Keychain stays off-limits without xian's permission; secrets stay in his password manager.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. #1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
