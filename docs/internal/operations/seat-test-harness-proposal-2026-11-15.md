# How seats run and test Piper without xian's hands

**Status:** PROPOSAL, first draft (Exec, 2026-11-15 19:13 PT). Not ruled. Arch owns the mechanism, CIO the harness and permission side, HOST custody. Corrections go to Exec by mail; Arch turns the agreed shape into one ADR.

**Draft 2 (19:24 PT):** section 7 holds the seats' corrections so far. Where section 7 and the text above differ, section 7 wins. Arch writes this up as ADR-084 after CIO's two dummy-value tests and HOST's custody answers.

**Why:** xian, 2026-11-15, in conversation (relayed verbatim in mail 01M7H5DC…): "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution." and "We keep changing how provider keys are used, how github is used, how piper morgan is used by our agents and it's become a tangled mess that keeps becoming my problem to manually navigate."

## 1. What went wrong

Between 11-11 and 11-15 four sound rules landed one at a time:

| Rule | Date | Sound because |
|---|---|---|
| Nothing a seat runs reads xian's login keychain | 11-11 | It holds his personal credentials |
| A seat doesn't read a credential file; a classifier refusal is final | 11-10 to 11-13 | The harness can't tell a test password from a real one |
| No seat runs `fly`; live reads and secret changes are xian's | standing | Production access |
| GitHub connect moves to the App; "your issues" follows the install | 11-12, 11-15 | Least reach |

Nobody owned their sum. Together they removed every way a seat had to spend on a model, sign in to beta, or read a production fact, and each loss was patched with "xian does it once". The patches are now a queue. On 11-15 alone it held: store a key, run a 26-call gate, run a 1,700-call screen, read four screens for CXO, read a provider count, grep a log, sign in as a test account, tick a flag.

The missing idea is a class of resource the rules never named: **things made for seats to use.** Every rule above protects xian's own state. None of them should apply to a capped test key, a test account or a test repository that exists only so agents can test.

## 2. The principle

**Seat resources are separate from xian's resources, granted once, bounded by a cap, and then used by seats without asking.**

1. **Separate.** A seat resource is never one xian uses himself. His keychain, his accounts, his production console and his personal GitHub stay off-limits exactly as now.
2. **Granted once, through the harness's own means.** xian (or Pard at his word) installs the grant: an environment variable at seat launch, or a named permission rule. A seat never works around a refusal; the grant removes the refusal.
3. **Bounded.** Each resource has a hard limit that holds even if a seat misbehaves: a workspace spend cap, a test account with no admin flag, an App installed only on test repositories, endpoints that return counts and never values.
4. **Standing.** Inside the bound, a seat acts and reports afterward. Asking first is for anything outside the bound.
5. **Stable.** One ADR records this. A later ruling that would put a step back on xian's hands must name the standing access that would remove it, and Exec checks for that line.

## 3. The three capabilities

### A. Paid model calls from a seat's own runs (screens, gates, evals)

**Today:** the key sits encrypted in the local database; only a process that loads the lead folder's `.env` can decrypt it; the classifier refused that (Lead, 18:51). The binder's database route (Arch's 11-11 ruling) was never run end to end.

**Proposed:**
- A **seat key** per provider lives in a capped workspace (Anthropic: `lead-scoring`, limit $150; OpenAI: one capped project key).
- It reaches a seat as an **environment variable set when the seat's session launches** (for example `PIPER_SEAT_ANTHROPIC_KEY`), installed by xian or Pard in the launch configuration. The name differs from `ANTHROPIC_API_KEY` so Claude Code's own credentials are untouched.
- A run names it on the command line, which `scripts/dev_key_binding.py` already supports (source 2 in its docstring): `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags, with `PIPER_CREDENTIAL_STORE=db`. No file is read, no keychain, no `.env`.
- **Budget rule replaces per-run asking:** a seat may spend up to a set amount per run and per week from the seat key without asking (proposed: $10 a run, $40 a week across seats), states the planned calls in its log before the run and the actual cost after, and stops at the in-code cap. Above the per-run figure it asks through Exec.
- `scripts/local_key_setup.py` stays what it was built for: a self-hoster's own key on their own install. Seats stop using it. The key stored tonight in the lead folder can be removed.

**Open, for Arch and CIO:** does the harness let a seat use a key present in its own session environment (CIO to test with a dummy value before any real key moves)? Which launch surface carries it (the LaunchAgent, or the worktree's git-ignored settings file)? Does every seat get it, or only Lead, CIO and PA?

### B. Using served Piper as a signed-in person

**Today:** no seat can sign in to beta. The test account's password file is refused by the classifier. CXO judges screens from xian's screenshots. PA reads the connector on xian's own account.

**Proposed:**
- **Two seat accounts on beta**, neither an admin: the existing plain test account, and one **GitHub-connected** account whose GitHub side is a dedicated test identity that belongs to the `pipermorgan` org and can see only its test repositories.
- **Their credentials are seat resources.** They live in one folder made for the purpose, and a named permission rule installed by xian or Pard lets seats read that folder and nothing beside it. The repo never holds them (hard rule 3 unchanged).
- **Web owns served reads and a screen atlas:** after each promotion Web signs in as each seat account, captures every settings and integrations page in each state that matters, and files them where CXO reads. CXO judges from the atlas. xian's screen is asked for only when the question is about his own account.
- **PA's connector** authorizes as the GitHub-connected seat account, not as xian.

**Open, for HOST, Arch and CIO:** the test GitHub identity (a second account of xian's, or a machine account under GitHub's one-machine-user allowance; HOST's custody call). Whether the permission-rule route is honoured by the classifier for that folder (CIO tests with a dummy file first). Session lifetime and who re-signs in.

### C. Production facts

**Today:** every fact that lives in beta's logs or database is a command on xian's list (`fly logs | grep`, a count query, `fly storage list`).

**Proposed:** the #2327 pattern becomes the rule. A fact seats need more than once gets a **read-only endpoint behind `ops_reader`** that returns counts, names and booleans, never values: the floored-action counts (served), provider-key counts by provider, evidence and probe line counts by event name, the deployed secret names (not values), storage presence. The plain test account holds `ops_reader` (one tick, already designed). A one-off fact is asked of xian once and not built.

**Open, for Arch and HOST:** which of today's log reads are recurring (my count: the #2362 and #2350 probes, the provider count, the refresh pass). The threat model of each endpoint is HOST's.

### D. Local full runs

Seats that run a local server or the whole test tree use a **scratch database per seat** (Lead's idea, Arch has no objection), so one seat's stored key or migration state never collides with another's or with xian's. Docs' fresh-clone run on 11-16 is the first use of that shape.

## 4. What xian does, once

| # | Action | About | Unblocks |
|---|---|---|---|
| 1 | Say yes or no to the principle and the three capabilities | 1 minute | everything below |
| 2 | Put the Anthropic seat key into seat launch (with Pard; the key made tonight) | 5 minutes | #2364's gate, arm B, H1, later screens |
| 3 | Make one capped OpenAI key and add it the same way | 5 minutes | #2364's OpenAI half, with no count read |
| 4 | Create the test GitHub identity, add it to the org, connect it on the second seat account | 15 minutes | CXO's reads, PA's rows, the atlas, #2266's second-account box |
| 5 | Install the permission rule for the seat-accounts folder (Pard can) | 2 minutes | every signed-in read |
| 6 | Tick "Operations reader" on the plain test account | 1 minute | the counter read and capability C |

After that, these leave his list: the 26-call gate, the arm B run, CXO's on-screen checks, the test-account sign-in, the provider count read, the log grep, the planned-calls approvals inside budget.

## 5. Order and owners

1. **Tonight to Monday morning:** seats correct this draft (mail to Exec). Arch, CIO and HOST each rule their part.
2. **CIO tests the two harness questions with dummy values** (a session variable, a permitted folder), so we know the grant route works before xian touches a real secret.
3. **Arch writes the ADR;** PPM places the build items (the endpoints of C, the binder note, the atlas).
4. **Exec brings xian one card:** the yes or no of row 1 and the five one-time actions, each with exact steps.

Suggested for the design work: Arch and CIO on Fable 5.2 until the ADR lands (xian offered).

## 6. Not in this proposal

- Any change to what protects xian's own keychain, accounts or console.
- Any seat running `fly`.
- A way past a classifier refusal. If a tested grant route is still refused, that route is dropped and another is proposed.

## 7. Corrections merged (draft 2)

From Arch (01M7H5T9…, 01M7H5MF…), HOST (01M7H55B…), Web (01M7H5B9…), CXO (01M7H5PD…), PPM (01M7H5HJ…), Docs (01M7H5JB…) and Comms (01M7H5M8…).

**A. Paid calls**
- **The bound must be hard (Arch).** A weekly tally in the repo is a reporting line, not a bound. The seat key sits in a workspace whose monthly limit *is* the seat budget, and that workspace holds nothing else. Open with Arch: whether `lead-scoring` can serve as that workspace once the older `lead-scoring-2026-10` key is revoked and the limit is lowered to the budget, so xian makes no further key.
- **One cap enforcer (Arch).** `developer_keys_bound(providers=..., max_usd=...)` refuses to start without a cap; the spend chokepoint (`services/llm/clients.py`, #1809) adds each response's usage and stops before the cap is passed; batch submits check worst-case cost first. A build item for PPM to place and Lead to build. It is what makes "act, then report" safe.
- **No binder change for the key source.** The existing command-line source carries it; the shell expands the variable, so the command text never holds the value.
- **Who gets the key:** only seats that run screens (Lead, CIO, PA). Docs' guide run can use the same seat key in a fresh clone's scratch database, so that run stops needing xian's own key.
- The 11-11 database route is narrowed to self-hosters, with its defect recorded.

**B. Signed-in use**
- **Two bounds on the test GitHub identity (Arch):** org base permission "No permission" or a team limited to the test repositories; the App installed on those repositories only.
- **HOST's conditions for the GitHub-connected account:** a separate throwaway GitHub account preferred over xian's own; a seeded test account, never a tester's; images show no token, email or outside name; every image records sha and time; the connection is ended when the work pauses; no admin and no `ops_reader` on that account.
- **Open, HOST and Arch against xian's 19:11 ruling:** HOST's condition 2 keeps every sign-in in xian's hand (a seat-driven browser profile he signs into; no seat reads or stores a test password). That is one sitting per account, repeated whenever a session expires. The draft's alternative is a permitted folder of seeded-account credentials. HOST to say which bound it requires now that the ruling is in, and how long a session lasts.
- **The atlas (#2381):** CXO writes the state matrix per page and reads from the atlas; Web captures; the tracked atlas is a text index (page, state, sha, time, quoted labels, image name); images live in the private repo or a seat-held folder with a name-free pointer here. A navigation tree of record is generated from routes and templates.
- Connector reads retry once after an MCP deploy until #2382 (stateless MCP server) lands.

**C. Production facts**
- **An endpoint can't read logs (Arch).** A recurring log fact becomes a counter written where the event is emitted, as the floored counter is; the endpoint reads the counter. Each one is a small build item.
- **Endpoint rules:** fixed named queries in code; no parameter selecting a user, row or free text; counts, booleans and names from a fixed vocabulary; `ops_reader` checked per request; every read logged. HOST owns each threat model, including whether deployed secret names are listed at all.
- First three (Arch): active keys by provider, the floored-action counter, the routing-to-floor tally. Comms needs counts for public copy (testers, waiting list, invites used): counts only, no personal detail.

**D. Local runs**
- One database per seat on the shared Postgres server (`CREATE DATABASE piper_<seat>`), not per-seat containers. Docs' fresh-clone run keeps its own server through a compose override.

**Not access questions, left with xian by design:** syndication to Medium and LinkedIn (his byline, his accounts). Docs can hand him one paste-ready block per post if he wants it lighter.

**Changed already, without waiting:** PPM names on every new acceptance row who can read it, and no longer routes a served read to xian by default.

