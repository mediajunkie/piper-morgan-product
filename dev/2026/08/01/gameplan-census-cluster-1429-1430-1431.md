# Gameplan: Census cluster wave 1 — #1429, #1430, #1431 (parallel coding subagents)

**Date**: 2026-08-01 (evening work burst, PM-directed)
**Issues**: #1429 (standup empty sources) · #1430 (phantom current_user) · #1431 (archived-projects always [])
**Lead Developer**: Claude (Opus 5), Amber seat. **Sprint**: Beta Blockers. **Milestone**: MVP (all three).
**Cascade position**: Issues audited (below) → THIS gameplan → audited → prompts (brief-coding-agent shape) → audited → execute.

## Phase -1: Infrastructure Verification — DONE TONIGHT, evidence attached

- Seat ACCEPTED 2026-08-01: venv 3.11.15, compose infra 4/4 healthy (pg 5433 / redis / chroma / ghmcp), alembic head, collection 10,770 clean, full sweep 6:20 with gate operating, LLM keys PRESENT.
- FastAPI + pytest + PostgreSQL confirmed (not assumed — sweep ran).
- **Issue code-claims re-verified live this hour** (16-day-old issues): #1429 TODOs + `return []` at webhook_router (`_get_completed_since_yesterday`/`_get_today_priorities`); #1430 `USER_ID = 'current_user'` at learning-dashboard.html:610 + raw `user_id` params in learning.py routes; #1431 archived-filter-of-active-only-source at portfolio_service.py:153→`_get_all_user_projects`→`list_active_projects` (`is_archived == False` at repositories.py:309). All hold.
- **Template adaptation, flagged for PM ratification (not silent N/A)**: (a) template Part A.2 still asserts the retired Desktop Model-B-only worktree rule — superseded by CLAUDE.md's host-dependent model (Amber = Model A); noted as template staleness, will propose template rev. (b) Phase -1 "with PM" co-fill adapted to evidence-attached self-verification: PM is offline and directed immediate work; every Part-A claim above is *probed*, not believed. (c) One cluster gameplan for three single-file-scoped issues instead of three full v9.6 documents — proportionality; each issue retains its own AC, prompt, and evidence trail.

## Phase 0: GitHub investigation — DONE
All three: filed from census 2026-07-16 (#1424 arc), assigned, MVP milestone, sprint-boarded, zero comments (genuinely unstarted). No open PRs, no prior branches touching these files (checked via issue timelines + branch list).

## Data flow / integration points (Phase 0.6, per-issue)

- **#1429**: Slack `/standup` (webhook_router:1148) → `_generate_standup_data` → the two stub sources. Fix wires acting-user principal → TodoManagementService queries (completed-since-yesterday; today's priorities). Integration risk: Slack context must carry a real user id — the `slack_user_mapping` path resolves it; if unmappable, sections must say honestly-unwired (issue offers this as acceptable fallback). `_get_blockers` `[]` is RATIFIED behavior (#692) — DO NOT touch.
- **#1430**: dashboard JS constant → 8 fetches → learning.py routes accepting raw user_id. Fix: routes derive principal from authenticated session (FastAPI dependency, same shape as neighboring authed routes); client-supplied user_id rejected/ignored; dashboard drops constant. **#1419/#1458 class relevance**: this is the beta-scope cross-user-leakage item — verification must show two users' isolation.
- **#1431**: add owner-scoped repo method (`list_all_projects` or direct `list_archived_projects` query), portfolio_service uses it. Latent (no live caller) — smallest risk. TODO at portfolio_service:431 marks the intended shape.

## Success criteria (executable, per issue)

```bash
# 1429: pytest tests for both sources returning real data for a user with todos; Slack-render test shows items
# 1430: two-user isolation test — user A toggles, user B state unchanged; client-supplied user_id ignored
# 1431: archive a project → appears in archived list (repo-level + service-level tests)
# ALL: full sweep after merge — zero NEW failures vs the 57-entry backlog (composition audit, Practice 5)
```

## Test strategy
Each subagent: TDD per flywheel Practice 2 — failing test first, minimal fix, targeted file green, report evidence block. Lead: merge each branch, run FULL sweep (composition audit — the seams are mine, not theirs), gate verdict, push. D4 discipline: no classifier/prompt changes anywhere in this cluster.

## Rollback plan
Each fix is a small, separately-committed branch merge; rollback = revert the merge commit. No migrations, no schema changes (#1431 adds a query method only). No deploy in this wave (beta deploy rides a later cut with #1386 verification).

## Phases
1. Prompts generated per brief-coding-agent skill (verbatim AC, evidence block, STOP conditions) → audited.
2. Three subagents launched in parallel, **worktree isolation each** (no shared-tree staging races; they commit to their own branch; DB 5433 shared — unique-user fixtures post-de-flake make concurrent targeted runs tolerable).
3. Lead integrates: per-branch review → merge → `git status` orphan check (CLAUDE.md commit verification) → full sweep → gate → push → board Status updates (In Progress at launch; In Review on merge+push).
4. Issue evidence comments per close-issue-properly; closure only with PM-visible evidence (user-verification steps included).

## Post-completion
#1426/#1428 (decline-copy + what-can-you-do) are wave 2 — they want #1433's ledger design context; #1432 archaeology runs during wave 1 (Lead, read-only). Discovered-work during wave → file immediately, never fold silently.
