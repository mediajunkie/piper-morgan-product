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

## Queue next (in order — TOMORROW'S FRESH SESSION, both quality-banked 8/1 22:00 with this explicit trigger)
1. **Judge-parity check** (#1395 quality half): reconstruct Run 15's judge config (model + PASS/MARGINAL counting — #1386 comments/logs), run parity or declare new baseline; tonight's 7/22-under-STRICT is non-comparable, NOT a quality answer. Then close #1395.
2. **#1432 delete** (GO in hand): delete-module-safely — pair + 3 test files + conftest ref + pm034 workflow; Phase-4 re-land as tracked step; backlog entries riding these tests come off in same commit.
3. #1460 instance fix (original_message backfill at detect_multiple + 6 reader sites to idiom B + 2 wrong-key Slack sites; runtime verification of setup flow in AC).
4. Census wave 2: #1426 + #1428 (want #1433 ledger design first — read census D §6).
5. #1464/#1465 fixes if PM adds to sprint (both small; 1465 is trivial import + regression test).

## Standing notes
- Beta target **Aug 8** (PM 7/30); scope growth needs PM approval. Multi-tenancy beta scope = #1430 (done) + #1458 traces + ratchet green (#1419 comment). #1458/#1457 → Production milestone.
- Board-status discipline ACTIVE (PM 7/30): In Progress at take-up, In Review at shipped-pending-verification, Done at close — same-work-block, per-item mutations only.
- decisions.log entries current through 8/1 (1461a). Design record amended per Arch second read (8/1).
