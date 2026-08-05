# Lead Dev carry-forward (rewritten 2026-08-01 ~18:55 PT, Amber seat)

## Session/env
- Worktree: `~/Development/piper-morgan-worktrees/lead` (Model A) on `claude/lead-cycle`; cron job **60fa16bd** (`17 6,9,12,15,18,21`, session-scoped, expires ~8/8, CronList-verify each START).
- Seat FULLY OPERATIONAL: venv 3.11.15 (collection 10,770 clean), compose infra 4/4 (pg 5433/redis/chroma/ghmcp), LLM keys in keychain (PM-provisioned 8/1), gh has project scope, flyctl authed. Full sweep = 6:20. Real pre-commit hook in common dir (v1.22: verify-exists, never probe).
- **Tests workflow GREEN** (8/1 01:08Z run = census wave-1 + 1461a + harness fix, all CI-arbitrated). Backlog 57 entries; 3 keyed-only-passing entries stay LISTED (fresh_tester_onboarding, todo-lifecycle e2e, db_user_history — fail keyless CI; never delist on local evidence).

## Recent closures (evidence on issues): #1445 (8/1), #1461 (8/1), #1424 (PM 7/30). Census wave-1 SHIPPED + In Review: #1429/#1430/#1431 (evidence comments posted; PM verification pending).

## Awaiting others
- ~~Arch ×2~~ BOTH LANDED 8/1 evening: #1432 formal GO received (delete tomorrow via delete-module-safely, scope incl. PM-034 workflow) · #1395 rev RATIFIED + committed `570fdf1dd`; Phase-3 routing 61/61 DONE; #1467 filed (Q22, floor streak 2 of N=3).
- **PM sprint calls**: #1464 (portfolio archive/restore crashes — LIVE via chat, MVP rec) · #1465 (learning success-path NameError inverts signal, MVP rec) · #1466 (Slack→Piper principal mapping absent, MVP rec). All from census wave-1 discovered-work.
- **Exec**: #1386 window re-scope now that criterion-2 is unblocked (keys in; baseline 55/61 done).

## Queue next (rewritten 8/4 STOP — BUILD QUEUE COMPLETE, 3-4 days to target)
0. **PM word-batch = the entire critical path**: beta weekday (Sat 8/8 vs Fri 8/7; milestone due-date aligns on the word) · v30 deploy go (16 In-Review verifications ride it; /link Slack-app one-time step on #1466; do NOT set PIPER_SLACK_INBOUND_ENABLED on beta — that's #1484's mechanism) · verification round (per-issue walkthroughs on the issues) · triage batch (#1471/1472/1473/1474/1479/1480/1485 + 11 untracked surfaces) · #1481 scope nod (mechanism shipped; 1481+1466-mapping-part → Production with 1419 per Arch's scope note).
1. On PM verifications: close In-Review set with their evidence.
2. #1467: one more clean full-corpus run post-flip (streak 2 of 3) — ride the next canonical run.
3. Watch: killed-sweep pattern (4 datapoints with Pard) · step-5b heartbeat defect (CIO's, quiet-fire visibility hole reopen cohort-wide) · weekly-docs-audit Monday 9:07 first test.

## In Review awaiting PM (16): 1393 1394 1413 1426 1428 1429 1430 1431 1432 1433 1460 1464 1465 1466 1482 1484
## Standing notes
- Beta target **Aug 8** (PM 7/30); scope growth needs PM approval. Multi-tenancy beta scope = #1430 (done) + #1458 traces + ratchet green (#1419 comment). #1458/#1457 → Production milestone.
- Board-status discipline ACTIVE (PM 7/30): In Progress at take-up, In Review at shipped-pending-verification, Done at close — same-work-block, per-item mutations only.
- decisions.log entries current through 8/1 (1461a). Design record amended per Arch second read (8/1).
