# Release Notes — v0.8.11.0 "Finish the Unfinished"

**Date**: 2026-07-17 · **Cut from**: main (see tag `v0.8.11.0`) · **Milestone**: Finish-the-Unfinished sprint (#1424) + multi-tenancy audit (#1419)
**Quality posture**: smoke gate 565 passed / 1 skipped at cut; two DB migrations included (run automatically on deploy).

## Summary

This release ships the Finish-the-Unfinished sprint: a systematic census of half-done work (four parallel audits over the whole codebase), fixes for every P0 it found, and permanent enforcement so the same debt classes can't silently return. The visible theme for testers: **Piper stops lying** — about your data, about its capabilities, and about what went wrong.

## What's New

### Multi-user correctness (the #1419 audit)
- **Your LLM provider choice is yours** ([#1415](https://github.com/mediajunkie/piper-morgan-product/issues/1415)): provider *selection* (default + authorized list) now resolves per user; one user's setup can no longer pin the whole instance to their provider. Consent-list read failures now fail **closed** (server default) instead of silently disabling the consent filter.
- **Personality questionnaire works again** ([#1422](https://github.com/mediajunkie/piper-morgan-product/issues/1422)): the `users.preferences` column lost in the #262 migration is restored (migration `k1422prefs`); questionnaire answers now actually shape Piper's warmth/confidence/depth. Prior answers were unrecoverable — testers re-answer once.
- **Owner-scoping fixes** ([#1420](https://github.com/mediajunkie/piper-morgan-product/issues/1420), [#1421](https://github.com/mediajunkie/piper-morgan-product/issues/1421), [#1434](https://github.com/mediajunkie/piper-morgan-product/issues/1434)): knowledge-similarity search and default-project resolution are owner-scoped and fail closed; a missing `await` that silently defeated an auth check (falling back to a global key) is fixed.
- **List/todo metadata persists** ([#1435](https://github.com/mediajunkie/piper-morgan-product/issues/1435)): a permissive-constructor trap silently discarded metadata on every save.

### Honest conversation
- **Greetings don't swallow your question** ([#1416](https://github.com/mediajunkie/piper-morgan-product/issues/1416)): "Hi! How do I address you?" now gets the question answered — only pure pleasantries short-circuit.
- **"Connect my GitHub" gets real guidance** ([#1417](https://github.com/mediajunkie/piper-morgan-product/issues/1417)): natural connect/setup phrasings deterministically reach the integrations-setup answer (which links Settings → Integrations) instead of a wrong generic decline.
- **No more false "there is nothing" claims** ([#1425](https://github.com/mediajunkie/piper-morgan-product/issues/1425)): status/agenda/retrospective/priority answers distinguish "the source failed" from "genuinely empty" — you'll see "I couldn't check your todos just now" instead of a false "no pending tasks."
- **No more false capability denials** ([#1426](https://github.com/mediajunkie/piper-morgan-product/issues/1426)): stale copy claiming Piper can't accept file uploads / set reminders (both shipped long ago) is retired; declines point at Piper's own pages, not "(e.g. GitHub)."
- **Classification failures tell the truth** ([#1414](https://github.com/mediajunkie/piper-morgan-product/issues/1414)): LLM-key/quota problems surface the honest key message instead of "Something unexpected happened."
- **Session memory recall** ([#1394](https://github.com/mediajunkie/piper-morgan-product/issues/1394)): "what did we create this session?" reads the new session-activity ledger (ADR-078); "update the title" style follow-ups resolve to the issue you just created.

### Reliability + enforcement (mostly invisible, permanently load-bearing)
- Signature-drift fixes from the one-shot type-audit ([#1436](https://github.com/mediajunkie/piper-morgan-product/issues/1436) Tier-1): knowledge-graph routes construct the service correctly; learning routes return clean 422/404s instead of 500s; todo-status route no longer shadows the HTTP status module; todo knowledge-graph writes carry the acting user.
- The classifier's per-user personalization path had a latent crash (caught by this release's own gate) — fixed; primary classification no longer silently falls to the fallback ladder.
- **Completion ratchets now guard the codebase** (ADR-079): unscoped credential/repository reads, silent-death exception handlers, stub counts, and dispatch-vocabulary membership are all counted and can only go DOWN; new debt of these classes fails the build.

## Known limitations
- Conversation picker sometimes loads the most recent chat regardless of selection ([#1418](https://github.com/mediajunkie/piper-morgan-product/issues/1418)) — fix in progress.
- The `/api/v1/todos` REST surface is still mocked ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427)); chat todos are real.
- Slack `/standup` sections and the learning dashboard have known gaps ([#1429](https://github.com/mediajunkie/piper-morgan-product/issues/1429), [#1430](https://github.com/mediajunkie/piper-morgan-product/issues/1430)).
- Knowledge-graph accumulation is newly re-enabled; similarity features fill as new activity is indexed.

## Version mechanics
- Cut commit: tag `v0.8.11.0` on `main`; `production` fast-forwarded to the same commit (prior curated-cherry-pick stamps through v0.8.10.14 are superseded — all their content is on main).
- Migrations: `j1394ledger` (session_activity), `k1422prefs` (users.preferences) — applied automatically at deploy (`release_command: alembic upgrade head`).

## Upgrade instructions
- **Beta (Fly)**: `fly deploy` from the release commit; migrations run in the release command; verify `/health` and login.
- **Alpha (droplet)**: standard archive deploy from `origin/production` + `./deploy.sh` (migrations run in-script). Alpha parity scheduled at sprint end.
- Testers: re-answer the personality questionnaire once (prior answers were unrecoverable, see #1422).
