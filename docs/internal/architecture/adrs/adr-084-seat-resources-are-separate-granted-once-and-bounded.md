---
type: adr
number: 84
title: "Seat resources: what agents use to run and test Piper is separate from xian's, granted once, and bounded where a seat can't pass"
status: "PROPOSED"
valid_from: "2026-11-15"
last_updated: "2026-11-15"
---

# ADR-084: Seat resources are separate, granted once, and bounded

**Status**: **PROPOSED, 2026-11-15** (Arch-authored, from Exec's `docs/internal/operations/seat-test-harness-proposal-2026-11-15.md`, draft 2 at 7c571b8fec, with CIO's, HOST's and PA's replies of 19:26 to 19:28). It becomes ACCEPTED on xian's word, relayed by Exec. Until then nothing here changes code or access, and paid runs stay stopped (Exec, 19:11).

**Related**: #2340 (the developer-key binder), #2364 (the provider gate that stopped), #2327 (`ops_reader`), #2373 (the floored counter), #2374 (reads limited to the installed set), #2381 (the screen atlas), #2382 (stateless MCP server), ADR-080 (code decides permission).

## Context

Between 11-10 and 11-15 four rules landed, each sound alone:

- nothing a seat runs reads xian's login keychain (11-11);
- a seat doesn't read a credential file, and a classifier refusal is final (11-10 to 11-13);
- no seat runs `fly`; production reads and secret changes are xian's (standing);
- GitHub connects through the App, and reads follow the install (11-12, 11-15).

Every one of them protects xian's own state. Their sum removed each way a seat had to spend on a model, sign in to beta, or read a production fact. Each loss was patched with "xian does it once". On 11-15 the patches were a queue of eight manual steps, and xian refused the pattern: "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution."

Two facts from that day shape the decision.

1. **The binder's database route never worked for a seat.** `scripts/dev_key_binding.py` (Arch's 11-11 ruling) named two key sources: the command-line environment, and the encrypted database store. The store needs `ENCRYPTION_MASTER_KEY`, which `scripts/local_key_setup.py` keeps in the worktree's `.env`. The binder never loads it. The route was ruled and never run end to end. The fix a seat reached for (a launcher that loads `.env`) was refused by the classifier, correctly.
2. **The class already existed in practice.** `~/.piper-shared` holds files seats made for testing (CIO, 19:26: 17 files, names only read). The rulings of 11-10 to 11-13 and the classifier cut seats off from them. No rule had named them as different from xian's own.

## Decision

### D1. The class

A **seat resource** is something that exists so agents can run and test Piper. It is:

1. **Separate.** Never a thing xian uses himself. His keychain, his accounts, his console and his own GitHub stay off-limits exactly as before. No rule that protects them changes.
2. **Granted once, through the harness's own means.** xian, or Pard at his word, installs the grant: an environment entry in a seat's settings, or an exact-command allow. No seat writes a grant for itself. No seat works around a refusal. If a tested grant route is refused, that route is dropped and another is proposed.
3. **Bounded where a seat can't pass.** Each resource has a limit that holds even if a seat misbehaves. A limit a seat keeps by its own care (a tally, a promise in a log) is a report, not a bound.
4. **Standing.** Inside the bound a seat acts, then reports. It asks first only for what is outside the bound.

### D2. Paid model calls

- **The key.** One seat key per provider, in a workspace (Anthropic) or project (OpenAI) that holds nothing else. **The provider's own monthly limit on that workspace is the seat budget.** That limit is the bound.
- **How it reaches a run.** An `env` entry in the seat's own git-ignored `.claude/settings.local.json` (mode 0600), under a Piper-specific name: `PIPER_SEAT_ANTHROPIC_KEY`, `PIPER_SEAT_OPENAI_KEY`. The name differs from `ANTHROPIC_API_KEY` because Claude Code uses that one and our launch lines strip it. CIO tested the shape with a dummy value on 11-15: the settings `env` surface reaches the shell, and the command ran unrefused.
- **How a run uses it.** The binder's existing command-line source, unchanged: `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags, with `PIPER_CREDENTIAL_STORE=db`. The shell expands the name; the command text never holds the value. No file is read, no keychain, no `.env`.
- **Who holds it.** Only seats that run screens or gates. Lead first; CIO and PA when each names a run. Docs' fresh-clone guide run may use it in its scratch database.
- **One cap enforcer.** `developer_keys_bound(providers=..., max_usd=...)` refuses to start without a cap. The spend chokepoint (#1809, `services/llm/clients.py`) adds each response's usage and raises before the cap is passed. Batch submits check the worst-case cost of the rendered requests first (`router_batch.py submit --cap-usd`, on main at 1e07f0ba74, is that half). Until the binder half is built, a run with no in-code stop still asks first.
- **The budget rule.** A seat may spend up to the per-run figure without asking. It writes the planned calls in its log before the run and the actual cost, from the provider's own counts, after. Above the per-run figure it asks through Exec. The figures are xian's to set; the proposal offers $10 a run.
- **If a seat ever sees the value in clear** (a log, `env` output, a transcript), it writes only the masked form, says so, and Exec has the key rotated. Seats don't print their environment.

### D3. Signed-in use of served Piper

- **Two seat accounts on beta.** Neither is an admin. Each holds nothing real: no real person's provider key, no tester data, a generated password used nowhere else.
- **One is GitHub-connected** through a dedicated test identity. Its reach has two bounds, and both are required: the org's base permission is none (or a team limited to the test repositories), and the App is installed on the test repositories only. Since #2374 the install bounds what Piper reads; org membership bounds what the identity itself sees. The identity's GitHub password and second factor are not seat resources. The connect and the install are xian's clicks, once.
- **A seat holds a session, never a password.** One reviewed helper on main (working name `scripts/seat_session.py --account <name>`) reads the account's file, signs in, and saves a session: a cookie jar for API reads, a browser storage state for Web. It prints the account name and the expiry only. The grant is an exact-command allow for that helper, installed by Pard or xian. The Read denies on `~/.piper-shared` stay as they are; the session file lives there under a name the denies match.
  - This is CIO's route, and it supersedes the proposal's "permitted folder". It waits on Pard's install of CIO's dummy kit. If the helper route is refused, the fallback is xian's own sign-in into a seat-driven profile, with a session lifetime long enough to make it rare. Custody of the choice is HOST's.
- **The connector.** PA reads through a second connector consented as the GitHub-connected seat account, not through xian's. Whether one claude.ai account can hold two connectors at one URL is unverified (CIO's test 3). Rows about xian's own data still use his connector, and the quote says so.
- **Served reads and the atlas** (#2381): Web captures each page in each state after a promotion; CXO judges from the atlas; the tracked part is a text index. Lead's script-run card harness covers words; the atlas covers layout.

### D4. Production facts

A fact seats need more than once gets a **read-only route behind `ops_reader`**. The rules for every such route:

1. A fixed, named query in code. No parameter that selects a user, a row or free text.
2. It returns counts, booleans, and names from a fixed vocabulary. No id, email, key prefix, length, or timestamp finer than a day.
3. `ops_reader` is checked on every request. The flag is set only from the admin control, by xian's hand. No chat or agent path can set it, and it never implies `is_admin`.
4. Every read is logged with the route and the reader, never the response body.
5. The set of routes is a closed list, pinned by a test. Each new route is a diff HOST reads before it ships.
6. **A route can't read logs.** The app has no access to its host's log stream. A recurring log fact becomes a counter written where the event is emitted (the #2373 shape: site and name only, no text, no user id), and the route reads the counter.
7. Deployed secrets: a boolean per name on a fixed expected list. Never an enumeration of the environment.

The first routes: active keys by provider; the floored-action counter (served); the routing-to-floor tally. A count that would single out a described tester is written in this public repo as "none" or "at least one".

A one-off fact is asked of xian once and not built.

### D5. Local full runs

One database per seat on the shared Postgres server (`CREATE DATABASE piper_<seat>`), the pattern `tests/integration/test_fresh_database_setup.py` has used since #2372. Not per-seat containers: the compose file fixes container names and ports. A fresh-clone guide run is the exception and uses a compose override.

### D6. The rule that keeps this from recurring

A ruling that puts a step on xian's hands names, in the same text, **the standing access that would remove it**. A ruling-relay with xian as the actor and no such line is incomplete. Exec checks for the line; CIO may make `mail4.py` warn on its absence.

Two further standing accesses were named in review and are accepted in shape, each with its own bound:

- **MCP deploys** (PA): a `workflow_dispatch` job in `fly-deploy.yml` holding a token scoped to the MCP app only. HOST owns the token's custody; Lead builds the job; it prints sha and release only.
- **Hook and settings installs** (CIO): Pard installs a CIO-authored patch on his own check when it arrives with a before-and-after test count. Paths limited to `.claude/hooks/` and `.claude/settings*.json` in seat worktrees; no deny is ever removed; each install is logged where xian can see it.

## What this supersedes or narrows

- **11-11, #2340, binder source 3 (the database store):** narrowed to a self-hoster's own install. Seats don't use it. Its defect (the binder loads no master key) stays recorded for self-hosters' scripts.
- **11-13, credential files and relayed grants:** unchanged for xian's files and for any file a seat would read. D3 grants a helper, not a read.
- **11-15 18:54 and 18:58, "xian runs it in Terminal":** withdrawn (decisions.log, 11-15 19:15).

Nothing here lets a seat run `fly`, read the keychain, or pass a classifier refusal.

## What xian does, once

1. Says yes or no to D1 to D6 and sets the budget figures.
2. Puts the Anthropic seat key in the screen-running seats' settings (with Pard).
3. Makes one capped OpenAI project key and adds it the same way.
4. Creates the test GitHub identity, bounds it in the org, and connects it on the second seat account.
5. Installs the helper's exact-command allow (Pard can).
6. Ticks "Operations reader" on the plain test account.
7. Creates the MCP-app-scoped deploy token and stores it as a repository secret.
8. Says yes once to Pard's install rule for CIO's hook and settings patches.

## Open at proposal time

- **The Anthropic workspace.** `lead-scoring` can serve only if the older `lead-scoring-2026-10` key is revoked and nothing of xian's own still spends there. If anything does, the seat key needs its own workspace. A lowered limit also has to allow for what the workspace already spent this month.
- **The helper route** (D3): pending Pard's install of CIO's dummy kit.
- **Two connectors at one URL** (D3): untested.
- **The test identity's account type** under GitHub's terms (HOST reads it as a machine account; unverified).
- **A running session and a new settings `env` entry:** whether a restart is needed (CIO's kit answers it).

## Consequences

- The eight manual steps of 11-15 leave xian's list once the one-time actions are done.
- New build items for PPM to place: the binder's `max_usd` and the chokepoint counter; `seat_session.py`; the `ops_reader` routes and their emit-site counters; the closed-list pin; the MCP deploy job; #2382.
- A seat that spends reports afterward, so every paid run leaves a planned line and a cost line in a log. The provider's limit, not the log, is what holds.
- Evidence gets a new honest label. "Drawn from the served template, not seen in a browser" and "read as the seat account, not as xian" are stated on the row, so nobody over-reads a seat's read as a person's.
