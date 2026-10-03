<!-- PROPOSAL ONLY (spec-eval workstream D-propose, 2026-10-03). Not in force. A sample rewrite of
CLAUDE.md at a191856 for PM review; see dev/2026/10/03/spec-eval/D-propose-ruleset.md for the
disposition of every removed line. Delete this comment on adoption. -->
# CLAUDE.md

Instructions for Claude Code agents in this repo. History and rationale for these rules live in
`docs/internal/architecture/decisions/claude-md-history.log`; this file holds only the rules.

## Role and session log

If PM assigns a role, read its briefing in `docs/briefing/` and use its log slug. If no role is assigned, you are a general agent (slug `code`); ask PM if the task needs a role.

| Role | Briefing | Slug |
|---|---|---|
| Lead Developer | BRIEFING-ESSENTIAL-LEAD-DEV.md | lead-code |
| Piper Alpha | BRIEFING-piper-alpha.md | pa-code |
| Chief Architect | BRIEFING-ESSENTIAL-ARCHITECT.md | arch-code |
| Chief of Staff | BRIEFING-ESSENTIAL-CHIEF-STAFF.md | exec-code |
| CXO | BRIEFING-ESSENTIAL-CXO.md | cxo-code |
| CIO | BRIEFING-ESSENTIAL-CIO.md | cio-code |
| PPM | BRIEFING-ESSENTIAL-PPM.md | ppm-code |
| HOST | BRIEFING-ESSENTIAL-HOST.md | host-code |
| Comms | BRIEFING-ESSENTIAL-COMMS.md | comms-code |
| Docs | BRIEFING-ESSENTIAL-DOCS.md | docs-code |
| Coding Agent | BRIEFING-ESSENTIAL-AGENT.md | prog-code |
| Web | BRIEFING-ESSENTIAL-WEB.md | web-code |
| ETA (dormant) | BRIEFING-ESSENTIAL-ETA.md | test-code |

Tiers and lanes: `docs/briefing/ROSTER.md`.

Session log: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{slug}-log.md`. It is the only durable log (a cycle log in `dev/active/` is optional scratch). One log per role per day; record the model in its header. Create it (skill `create-session-log`) before any other work, even for a greeting. After compaction, resume that log; it is how you recover your role. If you can't find it, stop and ask PM.

State you don't remember creating (commits, a changed cron, file edits) is most likely your own work from before a context gap. Check your session log first; use `list_sessions` only if doubt remains.

## Session start

1. Create or resume the session log.
2. Read `mailboxes/{role}/inbox/` (skill `check-mailbox`).
3. Read the "Now" section of `docs/briefing/BRIEFING-CURRENT-STATE.md` (not the history below it).
4. Read `docs/briefs/cross-pollination/current.md`.
5. Confirm you're in your worktree and on your branch, not `main` in the shared checkout.

The SessionStart hook prints a short status (log, mail, briefing freshness, role). If it says `BRIEFING: STALE`, or the briefing is visibly behind recent logs and commits, refresh what you can attest with skill `update-current-state` before other work. A partial refresh is better than none.

Before reading git or file state to answer a question or start work, `git fetch` and fast-forward if more than a few minutes have passed. A sync from earlier in the session is stale.

## Worktrees

- Amber (cohort host): your stable worktree `~/Development/piper-morgan-worktrees/{role}` on `claude/{role}-cycle`, reused every session (Claude Code keys state to the path). Check `git rev-list --count HEAD..origin/main` is 0 before working.
- Claude Desktop: the ephemeral worktree Desktop creates.
- Never work in the shared checkout `~/Development/piper-morgan-product`.

Lifecycle: `docs/internal/operations/amber-worktree-lifecycle.md`.

## Hard rules (data loss, exposure, irreversible changes)

1. The shared checkout `~/Development/piper-morgan-product` (on Amber and PM's Mac: `/Users/xian/Development/piper-morgan-product`) is PM's live workspace with uncommitted edits. Never run there: `git checkout -- <path>` or `.`, `git reset --hard`, `git stash`, `git clean`, or anything else that discards working-tree changes. If a merge or rebase there is blocked by unstaged changes, stop and push from your own worktree instead.
2. Before any `git checkout <ref> -- <path>` anywhere, run `git diff HEAD -- <path>`. If it is non-empty you are about to discard uncommitted work; read it and decide which side is stale. Clear MANIFEST noise only by your own role's explicit path.
3. Never write a bearer credential (invite code, API key, token) in full in any committed file. This repo is public. Use the masked form `ABCD…WXYZ`. A credential that reached git history must be rotated.
4. Projects v2: never send `updateProjectV2Field` with a partial `singleSelectOptions` list; it replaces the whole list and wipes assignments. Use skill `assign-sprint-safely`.
5. A commit message that pairs close/fix/resolve with `#N` closes issue N, whatever the surrounding words. Write the number without `#`, or add the trailer `Auto-Close: intentional` when closing is intended.
6. Memory in `~/.claude-pm/` is shared and has no git history. Export it to a tracked file before any prune or delete.
7. For any action with no undo (volume delete, `rm -rf`, force-push, bulk update), first check whether the narrow reversible step still works, and whether an API call is additive or full-replace.

These are backed by guards where noted in `docs/internal/operations/github-and-tooling-gotchas.md`; guards are advisory and bypassable, so the rule still applies.

## Git, push, sign-off

- Commit from your worktree and push finished units to main as you go: `git push origin HEAD:main`. Work not on `origin/main` is invisible to other agents.
- Commit the session-log entry for a unit with that unit.
- At idle points, run `scripts/sync-pm-local.sh` to fast-forward PM's checkout (it never touches PM's prose edits).
- After subagent work, run `git status` and stage or explain any modified files left in `services/`, `tests/`, `web/`.
- Stage in one call, commit in the next: the mailbox hook reads the index before a compound `git add && git commit` runs.

Sign-off (paste the output in your log):

```bash
git status
git fetch origin main
git rev-parse --verify -q origin/main >/dev/null || echo "STOP: origin/main did not resolve; the check below did not run"
git log --oneline origin/main..HEAD   # must be empty
```

If it is not empty: push with `git push origin HEAD:main`, or leave a NOTICE memo saying why the work is held, or ask PM. While the #974 pilot runs, add the memory-eval section described in `docs/internal/operations/memory-eval-pilot.md`. Before going dark on purpose (migration, stand-down), park your row in `dev/active/duty-cycle-registry.tsv` with a checkable clearing condition.

## Mail

- Write memo, cc copies and sent mirror under `mailboxes/`, then send with `scripts/mail-send.sh "mail({role}): {subject}" <every changed path>`. Don't `git add` or commit mailbox files yourself. Details: `docs/internal/operations/branch-worktree-mailbox-discipline.md`.
- Routing: `mailboxes/DIRECTORY.md` (PM is `mailboxes/xian (ceo)/`).
- Cc PM only when the memo (a) needs a decision only PM can make, (b) relays a PM ruling, or (c) says something PM would want to contradict. Everything else reaches PM through the attention rollup.
- Mail asks another agent to act; a GitHub comment records something about the work.

## Working rules

- **STOP and ask PM** when: infrastructure doesn't match the plan; tests fail; the thing you're building already exists (complete it); you can't produce evidence; the issue is missing; an ADR conflicts; user data is at risk; you want to defer work. PM decides what is critical.
- **Done** means a user can use it, tests exist and pass, evidence is on the issue, and your log is updated. Passing tests alone is not done.
- **Evidence.** Every completion claim (memo, issue closure, report) carries `Verified how:` with the method you ran this time, the layer it measured (a curl 200 is not a render test), and the denominator (what it covered out of what exists). Issue closures follow `docs/agent-protocols/issue-closure-protocol.md`.
- **Don't guess facts.** Look up names, credentials, config, counts and history, and quote the output in the same turn; otherwise say "unverified".
- **Investigate before extending.** Read the whole issue, memo or module before acting on part of it. GitHub is the source of truth for issue status.
- **Discovered work**: file it immediately with `bd create`; list filed issues at wrap-up.
- **Deferral** needs a named trigger (a fresh session or a compaction, with the reason). Rows in `dev/active/{role}-standing-items.md` carry a `Filed` column or a `**Filed**: YYYY-MM-DD` line so `scripts/aging-standing-items.sh` can read them.
- **Duty-cycle fires** wake you to check for work. Drain all unblocked work in priority order; commit at each unit but don't stop there. Procedure: skill `duty-cycle-tick`.
- **Honesty.** Give your actual assessment and call out mistakes, including PM's.
- **Decisions** other agents will need: an ADR in `docs/internal/architecture/adrs/` or a PDR in `docs/internal/product/pdr/`, or a line in `docs/internal/architecture/decisions/decisions.log`. Session logs are not the cross-session record.

## Subagents

- Brief with role, task, issue, acceptance criteria and expected evidence (skill `brief-coding-agent`).
- Set the `model` parameter explicitly and record the tier in your log entry: Haiku for fully specified mechanical work, Sonnet for bounded implementation, Opus for hard reasoning inside the unit.
- Quick search subagents report back; implementation subagents keep their own session log.

## Code conventions

- API routes use `/api/v1/` (exceptions: `docs/internal/architecture/current/web-routes-conventions.md`).
- New action handlers register a `WorkflowEntry(..., action_triggered=True)` in `services/intent_service/workflow_entries.py`; never add an `elif intent.action` branch. Lower `MAX_DISPATCH_SITES` when you migrate one.
- A new failing phrasing gets a corpus row, not a new extraction regex (`TestExtractionPatternRatchet`).
- Read `docs/internal/architecture/current/intent-routing-stack.md` before touching classification, dispatch or chat responses, and update it if your change makes it stale.
- Read `knowledge/piper-morgan-glossary-v1.1.md` before writing about Plugin, MCPB, Connector, Extension, Skills, Cowork or Claude Desktop.

## Quick reference

```bash
python main.py                    # server, port 8001 (entry point; not web/app.py)
python -m pytest tests/unit/ -v
docker compose up -d && alembic upgrade head   # Postgres 5433
./scripts/fix-newlines.sh         # before committing
```

Ports: server 8001, Postgres 5433, Redis 6379, ChromaDB 8000. Domain models `services/domain/models.py`; enums `services/shared_types.py`; config `config/PIPER.md` (`config/PIPER.user.md` is an optional, often absent overlay).

From a Claude Code shell, start the server with the inherited Anthropic vars stripped, or every LLM call fails:

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
```

Deploys come from `origin/main`; for what is live, check the running host's commit. Store app credentials with `KeychainService`, not the `security` CLI.

Repository: `https://github.com/mediajunkie/piper-morgan-product`.

## More detail when you need it

| Need | Read |
|---|---|
| Sprint position | `docs/briefing/BRIEFING-CURRENT-STATE.md` ("Now") |
| Project overview | `docs/briefing/PROJECT.md` |
| Debugging / E2E investigation | `docs/agent-protocols/debugging-protocol.md`, `e2e-investigation-protocol.md` |
| Git workflow, completion discipline | `docs/agent-protocols/git-workflow.md`, `completion-discipline.md` |
| Ops recipes, tooling gotchas | `docs/internal/operations/canonical-ops-recipes.md`, `github-and-tooling-gotchas.md` |
| Hooks on Amber | `docs/internal/operations/amber-hooks-investigation-2026-07.md` |
| Patterns, ADRs | `docs/internal/architecture/patterns/`, `adrs/` |
| Skills | `.claude/skills/` |
