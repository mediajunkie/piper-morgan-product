# Session log — prog (Coding Agent), 2026-09-26

- **Role**: prog (Coding Agent)
- **Model**: Opus 5 (1M context) — `claude-opus-5[1m]`
- **Dispatched by**: Lead Developer (Opus tier stated: credential issuance feeding a fail-closed identity boundary)
- **Task**: MCP Phase C unit 4 — OAuth 2.1 Authorization Server in the alpha app, PM-approved 2026-09-26
- **Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
- **Constraint from dispatcher**: do NOT commit, stage, or touch the git index. No deploys, no Fly, no network, no LLM.

## Acceptance criterion (Arch's review condition)

> Verify the OAuth flow binds the minted token to the SAME identity that authenticated at the
> authorize step, throughout — the specific failure shape: `exchange_authorization_code` minting a
> token for a different (or unresolved) identity than the one that consented. Explicit test, not an
> assumed property.

## Work log

- 17:07 — Session start. Log created. Read `phase-c-build-plan-2026-09-25.md` (unit 4 = "OAuth AS
  (SDK-provided) — only if the tester's client can't present a bearer", Q1). Design decision has
  since been made by Lead/PM: build it, AS in the alpha app, tester's first client is ChatGPT.
- 17:10 — Read, in full: `server-README.md`, Arch's lean memo, `services/mcp/server/app.py` +
  `identity.py`, `alembic/versions/n1462mcpt_*`, `services/auth/auth_middleware.py` (exempt-list
  categories + dispatch + `_unauthorized_response`), `web/app.py`,
  `web/middleware/intent_enforcement.py`, `web-routes-conventions.md`, and the SDK
  (`provider.py`, `routes.py`, `handlers/authorize.py|token.py|register.py|revoke.py`,
  `middleware/client_auth.py`, `shared/auth.py`, `settings.py`, `fastmcp/server.py` auth wiring),
  plus the unit-1/unit-2 test idioms and the ratchet/mypy-gate machinery.
- **DESIGN GATE: cleared, no STOP.** All three named STOP conditions checked and none holds:
  (a) the alpha session IS resolvable in the authorize wrapper with **no second auth mechanism** —
  `AuthMiddleware` already gates any non-exempt path, sets `request.state.user_id` from validated
  JWT claims, and for a non-`/api/` HTML request with no session issues `302 /login?next=<encoded
  path+query>` (#1480 shape), which is exactly the OAuth redirect flow we need; (b) SDK discovery
  DOES resolve under a path-prefixed issuer — `build_metadata` appends `/authorize` etc. to the
  issuer, so mounting the SDK routes under `/mcp/oauth` makes advertised == mounted by
  construction, and metadata is served at both the RFC 8414 §3.1 location and the path-appended
  one; (c) no user-data mutation beyond the three new tables + `mcp_access_tokens`.
- 17:30 — Implemented. Files: `services/mcp/server/oauth_provider.py` (new, provider),
  `web/routers/mcp_oauth.py` (new, HTTP surface + session gate + consent page),
  `alembic/versions/o1462oaut_mcp_oauth_as.py` (new, one migration, three tables),
  `services/database/models.py` (+3 models), `web/app.py` (mount),
  `services/auth/auth_middleware.py` (`EXEMPT_MCP_OAUTH_AS_PATHS` — machine-to-machine only,
  `/authorize` deliberately NOT exempt; 3 `AUTH_EXEMPT_JUSTIFIED` entries),
  `web/middleware/intent_enforcement.py`, `services/mcp/server/app.py` (issuer default +
  `OPEN_PATHS`), `services/mcp/server/identity.py` (`hash_credential` made public).
- 17:33 — Tests: `tests/unit/services/mcp/server/test_oauth_as_unit4.py`, 21 tests, all passing.
- **Three real bugs found by writing the tests, not by reading** (recorded because each is a
  trap the next person hits):
  1. **`TokenError`/`AuthorizeError` are frozen dataclasses.** Raising one inside an
     `async with self._scope()` block dies with `FrozenInstanceError` — `contextlib`'s async-CM
     exit assigns `exc.__traceback__`. Every refusal is now raised outside any scope, and the
     decision was extracted into a pure `_refuse_code()`.
  2. **The transaction split is load-bearing.** `_scope()` rolls back on any exception (#1193), so
     a single scope around claim + replay-revocation + mint meant that raising `invalid_grant` for
     a replay ROLLED BACK the §4.1.2.5 revocation. Fail-open dressed as a refusal. Now three
     separate transactions; the test re-reads the row from the store to prove the revocation
     committed.
  3. **`MCPPathGate` was blocking RFC 9728 discovery.** FastMCP registers
     `/.well-known/oauth-protected-resource` whenever `resource_server_url` is set and the MCP
     path's 401 points at it, but unit 1's gate answered it with a 401 — so an OAuth client had no
     way to find the issuer. Added to `OPEN_PATHS` (public by design; no user data).
- 17:38 — Gates all green: `tests/unit/services/mcp/` 277 passed; `tests/unit/web/` 916 passed;
  `tests/test_architecture_enforcement.py` 63 passed 1 xfailed; `scripts/run-sweep.sh ratchets`
  exit 0 (73 passed, 1 xfailed; mypy gate all 24 codes AT ceiling, total 1121); mypy gate over
  `services/mcp/server` → 0 errors in this unit's files. Two ratchet interventions, both keeping
  the count AT ceiling rather than raising it: five `# global-ok:` annotations relocated to the
  line before the `select(` (ruff reflow had pushed them off the line
  `check_unscoped_reads.py:_annotated` inspects), and `: Any` annotations on the five new JSON
  columns in `models.py` (the SQLAlchemy mypy plugin types a legacy `Column(JSONB)` as
  `Mapped[Any]`, which is neither list-assignable nor iterable to mypy).
- 17:45 — Docs: `server-README.md` (§"Two hosts, one identity" — text topology diagram, the
  7-step flow, what the tester configures, the PA-safe tester copy, the identity-binding
  argument, the three traps, files/config tables), `web-routes-conventions.md` (exception 4),
  `phase-c-build-plan-2026-09-25.md` (unit 4 marked BUILT with scope and what is NOT exercised).

## Discovered work (not filed as issues — reporting to Lead, who owns the lane)

1. **`scripts/mailbox_bearer_lint.py` is RED on main, 8 pre-existing hits**, all in the four
   copies of `memo-arch-to-lead-cc-cxo-ceo-1017-phase-3-probe-set-engineering-coverage-2026-05-15.md`
   (lines 84 and 92: `skpr…ghij`, `ghp_…ABCD`). Verified NOT mine — `git status --porcelain` shows
   I touched none of those files. They look like documentation placeholders that exceed the lint's
   8-distinct-character allowance rather than live credentials, but that is a judgment for whoever
   owns #1845, not for me.
2. **The `o1462oaut` migration must be applied before the AS can serve.** Confirmed live against
   the local dev Postgres: `POST /mcp/oauth/register` 500s on `relation "mcp_oauth_clients" does
   not exist`. I did NOT run `alembic upgrade head` (outside a subagent's remit to mutate the dev
   DB). Noted in `server-README.md`.

## Memory & briefing surfaces referenced this session

- **Referenced**: `CLAUDE.md` (evidence discipline, `Verified how:` requirement, m-43 layer / m-44
  denominator, ADR-079 `# global-ok:` mechanism, the "no deploys / don't touch the index"
  boundaries of this dispatch); `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md`
  (unit 4 scope + Q1); `mcp/server-README.md` (units 0–2 as built, the seams);
  Arch's lean memo (the acceptance criterion, quoted verbatim into the test module docstring);
  `web-routes-conventions.md` (the `/api/v1/` rule and its exception format).
- **Loaded but not referenced**: the glossary; the duty-cycle / mailbox-discipline sections of
  CLAUDE.md (no mail sent this session).
- **Wanted but not found**: nothing blocking. One gap worth naming: there is no doc anywhere
  stating that the SDK's OAuth error types are frozen dataclasses and therefore cannot be raised
  across an `@asynccontextmanager` exit — it cost a test cycle to find, and it is now recorded in
  both the provider docstring and `server-README.md` so the next person doesn't pay it again.
