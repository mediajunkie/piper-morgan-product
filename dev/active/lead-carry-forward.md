# Lead Dev carry-forward — 2026-07-16 ~16:50 PT

## Sprint: Finish-the-Unfinished (epic #1424) — Phase 2 in progress
- Plan: docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md · Census (FROZEN): docs/internal/operations/finish-the-unfinished-census-2026-07-16.md
- **Closed so far**: #1435, #1434, #1422 (+migration k1422prefs), #1421, #1420, #1425 (all 5 handlers), #1436-B9, session_factory annotations. Ratchet ceilings: silent_death 247 · unscoped 64 · NIE 9 · TODO 78.
- **Next unblocked (user-impact order)**: #1415 per-user provider selection (Arch: mirror PersonalizationService; fold F1 consent-fails-CLOSED) → quality-banked for a fresh context window. Then #1436 pack (B8 user_id arg, B5 status shadow, B4 error-helper kwargs incl. the pre-existing api-test, B2 KG DI), un-swallow clusters (F9-F17 via #1423), lint-1 v2 (derive owner tables + indirect-scoping calibration), silent-ok seeding of Census A's 85 LEGIT (gates lint-2 CI-flip), forward-guard registry migration (todo CRUD batch).
- **Waiting on Arch**: #1417 vocabulary ruling (proposal sent 7a451e89c — integration-connect pre-classifier pattern → existing GUIDANCE lane); ADR "Owner-Scoping Integrity Contract" (they author); build-ratify pings owed as each guard lands.
- **Waiting on PM**: shipping-cadence confirm → first beta batch = the 8 closed fixes + k1422prefs migration, cherry-picks to production branch. #1427 finish-or-unmount decision. F21 disposition (chat-invisible ledger vs wire).
- **Provenance note**: site-1 of #1425 + its test file appeared in-worktree ~15:54 uncommitted, author unknown (list_sessions: no peer session here; most likely PM hand-editing). Adopted + credited in the close. If PM: converged design, no action. Watch for further hand-edits before overwriting anything.
- Cron 985b0ef9 armed (17 6,9,12,15,18,21). Scenario driver: xfail #1416/#1417 pending those fixes (flip strict in same commits).
