# Docs Carry-Forward

**Updated**: 2026-11-13 09:16. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-13 09:16)
- **Tier 1 corpus (#2355) is Docs' lane, second-lane work.** Manifest `docs/internal/design/tier1-corpus-manifest.csv` (25 rows, README beside it), checker `scripts/validate_tier1_manifest.py` (`--strict`, `--deploy`, 7 tests in `tests/unit/scripts/`). Rules (Arch/Lead/PPM/CIO): `item` is the one indexed file, `derived_from` is what facts are checked against, indexed = verified + voice_pass passed + resolves + in window + `approved` (sha at xian's quoted yes, current lines must appear in the approved text). A stale or unapproved row DROPS (no deploy refusal), only an indexed item on an excluded path or an unreadable stand-ins sha exits 1. Stand-ins live in `docs/tier1/stand-ins.md` (row `s-stand-ins`, kind `template`). Nothing is indexed: no row is approved. Do NOT push to scripts/, tests/, services/, web/ while Lead's hold is on (his second hold: until the served commit after d80610b579). docs/, dev/ and mail are fine.
- **Items written:** `docs/tier1/connectors.md` (CXO passed), `learning.md` (CXO's words, Arch's code read), `how-i-act.md` (b-understanding, verified, CXO passed), `practice.md` and the c rows (CIO's), `stand-ins.md` (CXO passed, goes on Exec's approval card for xian). `docs/known-limits.md` is a DRAFT (6 rows, CXO passed the words, facts wait on PA's served reads which wait on the web-seed-1386 sign-in decision). Tester page ALPHA_KNOWN_ISSUES.md links to it, cut-release 3d is v1.4.
- **Left for me (b rows still without an item):** b-github-access (check last, #2342 reconnect), b-cant-read (floor-honesty spec is "not ratified", take only what code does), b-wont-do (ethics-architecture.md is 2025-10, verify every claim), b-stance (PDR-004, CXO judges wording, claims about behavior need code checks). Each is a code read first. Rest of b-learning (forget path reachability) needs a served check. Deferred to a fresh session or compaction: each one is a multi-file code read, not bite-sized.
- **Ship #069 review filed 11-13 (v4 01M7AGE453).** 11-12 omnibus landed 11-13. Next START (11-14 04:12) owes the 11-13 omnibus (Sonnet subagent, scratchpad, 11-12 omnibus as format model, then verify: commit recount after fetch, exact-marker grep, 0 semicolons, banned words) and Step 1d on the 11-13 logs (CXO's 11-12 log lacked the exact marker, Exec used a plain line).
- **Sat 11-14 "Which Agent Did It?"** (insight, row `drafted`) publishes only on a Comms ready-for-docs memo: full pre-flight, weekday check (Sat = insight), Medium and LinkedIn (insight), no nudges to xian.
- **Self-host guide run-check Mon 11-16** from a clean clone with PIPER_CREDENTIAL_STORE=db, blocker a real provider key (xian's rule-7 route). Remove "(not yet run)" markers as verified, tell CIO the day it ran.
- **"The Server Has No Key" is distributed (Medium only).** Nothing owed.
- **Gate live:** `python scripts/key_in_docs_lint.py` before any page edit.
- **Mail v4 for sends** (`python3 scripts/mail4.py send --to <roles> ...`). Push races: a `merge --autostash` plus retry loop works, the pre-push gate takes about 40 seconds so run the loop with a long timeout. A manifest conflict with another role's edit: take theirs and reapply my columns by name.
- **Mistakes to not repeat:** guessed times in headings (read `date`), mail sent before the push it describes, calling a lane "rule 7" when it is PA's, writing "her" for an agent.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
