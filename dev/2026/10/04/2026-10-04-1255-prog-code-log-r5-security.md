# 2026-10-04 12:55 — Coding Agent (prog), R5 security items 1–3

**Model**: Sonnet. **Dispatched by**: Lead Dev, via
`mailboxes/lead/read/ruling-relay-spec-to-lead-cc-host-pm-approves-r5-security-code-items-2026-10-04.md`
(PM-approved relay from Spec's `docs/internal/audits/2026-10-spec-project-evaluation.md` R5, evidence
`dev/2026/10/03/spec-eval/A-architecture-security.md`).

Scope: R5 items 1–3 only (item 4, the prod `setup_complete` read-only query, is explicitly not mine).
Worked in `/Users/xian/Development/piper-morgan-worktrees/lead` on `claude/lead-cycle`. Did not
touch `services/intent_service/*`, `canonical_handlers.py`, `todo_handlers.py`,
`workflow_entries.py`, `workflow_dispatcher.py`, `action_registry.py`, or
`scripts/inversion_phase3_deletion_gate.py` (other lanes). Made no commits — Lead reviews/commits.

## Item 1 — removed `?token=` query-param JWT acceptance

`services/auth/auth_middleware.py` `_extract_token` (was line ~468) dropped the
`request.query_params.get("token")` branch entirely; header (`Authorization: Bearer`) and
`auth_token` cookie paths unchanged.

**Caller search before removing** (so a genuine need wouldn't get silently broken): grepped
`templates/`, `static/`, `web/` and `tests/` for `?token=`, `EventSource`, `new WebSocket`,
`ws://`. Findings:
- No `EventSource`/SSE anywhere in the repo.
- No WebSocket route registered in the app at all (`grep -rn "@router.websocket\|websocket_route"`
  → nothing). `socket_mode_runner.py` is Slack's own socket, unrelated to this JWT middleware.
- The one `?token=` hit outside docs/prose is `templates/settings_github.html:656`, which is a
  request **body** (`token=${...}`), not a URL query param — unrelated.
- No test exercises the query-param path (`grep -rn "query_params.*token\|token_param"` →
  nothing in `tests/`; `tests/test_security_framework.py`'s `query_params = {"token": ...}` is a
  plain dict-construction assertion with no HTTP call against the app).

Conclusion: no caller, no STOP needed. Removed outright rather than scoping to a route.

## Item 2 — removed the hardcoded fallback JWT secret (fail closed in every env)

`services/auth/jwt_service.py` `_get_secret_key`: removed the `PIPER_ENVIRONMENT`/`ENVIRONMENT
== "production"` conditional and the `"dev-secret-key-change-in-production"` fallback string
entirely. Now: `JWT_SECRET_KEY` set → use it; unset → `RuntimeError` naming the var and giving the
one-line fix, **regardless of env name**. (Previously: only `production` literally triggered the
guard; dev/staging/alpha/unset all silently signed with the public hardcoded string.)

**How tests get their secret now**: `tests/conftest.py` — added
`os.environ.setdefault("JWT_SECRET_KEY", "test-only-jwt-secret-not-for-real-use-32chars-min")`
right after the `sys.path` insert, before any fixture/import that could construct a `JWTService()`.
conftest.py loads before any test module under `tests/` is imported (pytest's hierarchy), so this
covers all ~46 call sites across the suite that call `JWTService()` with no explicit secret — and
`setdefault` means a real env override still wins. Verified by grep: `tests/auth/test_jwt_service.py`
is the only file that references `JWT_SECRET_KEY` directly (its own monkeypatch tests), so it was
the only test file needing updates for the behavior change itself.

Updated `tests/auth/test_jwt_service.py`:
- `test_secret_key_production_unset_raises` / `test_secret_key_production_via_environment_var_also_raises`:
  same scenario, match string updated from `"JWT_SECRET_KEY must be set in production"` to
  `"JWT_SECRET_KEY is not set"` (the message is now env-independent).
- `test_secret_key_dev_unset_keeps_fallback` → replaced with
  `test_secret_key_dev_unset_also_raises` (dev env, unset key, now raises — this is the exact,
  approved behavior change, not a weakening).
- Added `test_secret_key_unset_entirely_also_raises` (no env name set at all — the common local-shell
  case) for coverage the old suite didn't have.
- `test_secret_key_from_environment` / `test_secret_key_not_hardcoded_in_code`: docstring/comment
  updated to note there's no more default; behavior unaffected since conftest now supplies a value.
- `test_secret_key_production_with_key_set_works`: untouched, unaffected.

**Discovered risk, fixed** (`web/app.py`): `AuthMiddleware` registration was wrapped in the same
`try: ... except Exception as e: logger.error(...)` pattern as the other optional middlewares in
that file — which would have **swallowed** the new `RuntimeError` and booted the server with
**no auth middleware registered at all** (every route open) whenever `JWT_SECRET_KEY` is unset.
That failure mode got strictly more likely once the dev fallback was removed, and is worse than the
problem item 2 fixes. Changed that one `except` block to re-raise after logging — the server now
refuses to start rather than starting unauthenticated. Did not touch the other middlewares' (still
fail-open-and-continue) blocks around it — out of scope, and they're not the app's perimeter the way
auth is.

**Local dev / docs**: `main.py` has no direct `JWTService`/`JWT_SECRET_KEY` reference — it launches
`uvicorn.Config("web.app:app", ...)`, so an unset key now surfaces as an import-time `RuntimeError`
with the actionable message at `uvicorn` startup. `scripts/validate_install.py` already flags a
missing/empty `JWT_SECRET_KEY` in `.env` as required — no change needed there. Added a new
`## Authentication` section to `docs/internal/operations/environment-variables.md` (before `## Server
Configuration`) documenting the new fail-closed behavior, the local-dev generation one-liner, how
tests get it, and a note that staging/prod must carry it in the deploy secrets store.

**Could not edit**: `.env.example` — this sandbox's permission settings deny Read/Bash access to any
`.env*`-matching path outright (confirmed: both `Read` and a bare `ls .env.example` were denied, not
just a `cat` of contents). I could not confirm or change its `JWT_SECRET_KEY` line. **Lead: please
check `.env.example` has a `JWT_SECRET_KEY=` line with a comment pointing at the generation one-liner
above (or remove it if a placeholder value there would mislead someone into thinking it's set).**

**Deploy config (Fly secrets) — report only, no fly/ssh run**: the OLD guard already raised
`RuntimeError` whenever `PIPER_ENVIRONMENT=production` and `JWT_SECRET_KEY` was unset. If the Fly
deploy is up and issuing sessions today, that means `JWT_SECRET_KEY` is **already** set as a Fly
secret — the new, broader guard doesn't change prod's requirement, only dev/staging's. I did not run
`fly secrets list` or anything else against Fly; this is inferred from the old code path's behavior,
not independently verified against the live deploy.

## Item 3 — extended the bearer-credential check to commit/mail messages

`scripts/mailbox_bearer_lint.py` scans **files**; it has no view of the commit/mail **message**
itself, which is how a tester's name and a full invite token sat in commit subject `7941ae4b97`
on main. `scripts/check_autoclose_keywords.py` already extracts "the message, however it arrived"
for both doorways (mail-send.sh's commit-tree `-` stdin path, and `autoclose-guard.sh`'s
`--bash-tool-input` PreToolUse hook on `git commit`), so it was the natural place to add the same
check rather than building a second message-extraction path.

**Shared detector, not duplicated**: added
```python
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mailbox_bearer_lint import mask, scan_line  # noqa: E402

def bearer_hits_in_message(message: str) -> list[str]:
    hits = []
    for line in message.splitlines():
        hits.extend(scan_line(line))
    return hits
```
`main()` now runs both checks on the same extracted `message` and refuses (exit 1) if either fires.
**The `Auto-Close: intentional` opt-in waives only the auto-close concern — it does not and cannot
waive a bearer hit** (tested explicitly: a message with both the opt-in trailer and a token is still
refused, for the bearer reason). Bearer hits are printed **masked only** (`mask(cred)`, e.g.
`ZVHW…8B35`) — the raw credential never reaches stdout/stderr.

Updated both wrapper scripts' generic refusal text (the detailed reason was already printed by the
Python script above the wrapper's line; only the wrapper's own generic sentence was now
inaccurate for a bearer-only refusal) — `scripts/mail-send.sh` and
`.claude/hooks/autoclose-guard.sh` — plus their header comments. No change to either script's
control flow or exit codes; existing #1691-only tests (`test_check_autoclose_keywords_1691.py`)
still pass unchanged.

**New test file** `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py`:
- `bearer_hits_in_message` detects a synthetic Crockford token, an `sk-ant-...` key, a `ghp_...`
  token, and the lowercased-paste form of the token, embedded in realistic commit-subject-shaped
  messages.
- **False positives tested and confirmed clean**: a masked form (`ZVHW…8B35`) in prose; a real
  10-char git sha (`7941ae4b97`, the actual incident sha, used as a negative control); a 40-char
  full hex sha; plain `#1845`/`#1691` issue references; a mixed-case base62-shaped id (rejected by
  the same `_is_token_run` logic the existing lint test already pins).
- CLI-level test (actual subprocess against `check_autoclose_keywords.py -`): refuses, masked form
  only in stderr, raw token never appears in stdout or stderr.
- `autoclose-guard.sh` doorway: `git commit -m` with a token in the message → blocked (exit 2,
  masked only); the same message with the credential pre-masked → passes.
- `mail-send.sh` doorway: a mail subject carrying a token → refused before any push (exit 1,
  "Nothing was sent", masked only) — this is the exact doorway the real 2026-07-09 incident went
  through, since the leak was in a commit **subject**, not a memo body.
- Opt-in-does-not-waive-bearer test, described above.

## Tests

Targeted run (auth + script suites):
```
tests/auth/test_jwt_service.py tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py
tests/unit/scripts/test_check_autoclose_keywords_1691.py tests/unit/scripts/test_mailbox_bearer_lint_1845.py
→ 88 passed, 1 skipped
```
Broader auth/web sweep:
```
tests/auth/ tests/unit/services/auth/ tests/unit/web/ tests/integration/auth/ tests/security/
→ 1203 passed, 6 skipped, 110 warnings
```
Full prescribed suite:
```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py tests/scripts \
  -q -p no:cacheprovider -m "not llm" -o addopts="--ignore=tests/archive --ignore=*/archive/* \
  --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ \
  --tb=short --import-mode=importlib"
→ 4 failed, 12350 passed, 228 skipped, 3 deselected, 1 xfailed, 166 warnings in 258.92s
```
(`tests/scripts` as given doesn't exist — actual dir is `tests/unit/scripts/`; included in `tests/unit`
already collected, so coverage is unaffected.)

**The 4 failures — not mine, confirmed by inspection, none touch any file I edited:**
- `tests/unit/test_inversion_phase3_deletion_1595.py::TestDeletedPatternListsLedger::test_real_ledger_entries_pass_non_regression`
  and `::test_calendar_entry_fails_non_regression_without_the_live_flag` — explicitly named in the
  dispatch instructions as another lane's territory (`scripts/inversion_phase3_deletion_gate.py`).
- `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py::TestDefaultEmpty::test_flag_on_but_no_sibling_routed_is_the_same_turn`
  — same `services/intent_service/*` territory, off-limits per dispatch.
- `tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet::test_every_pointer_resolves_deterministically`
  — failure is pre-classifier/intent-routing (`'give me my standup'` and `'what time is it?'` not
  resolving deterministically via `services/intent/intent_service.py` / `ratchet_ceilings.json`),
  same conceptual territory as the excluded intent lane, and no file this test reads was touched by
  this work.

## Quality gates

```
ruff check  services/auth/auth_middleware.py services/auth/jwt_service.py tests/conftest.py \
  tests/auth/test_jwt_service.py web/app.py scripts/check_autoclose_keywords.py \
  tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py
→ All checks passed!

ruff format --check <same files> → 7 files already formatted
bash -n scripts/mail-send.sh && bash -n .claude/hooks/autoclose-guard.sh → both OK
```

## Files changed

- `services/auth/auth_middleware.py` — removed `?token=` extraction
- `services/auth/jwt_service.py` — removed fallback secret; fail-closed unconditionally
- `web/app.py` — `AuthMiddleware` registration re-raises instead of swallowing
- `tests/conftest.py` — sets a fixed test `JWT_SECRET_KEY` via `os.environ.setdefault`
- `tests/auth/test_jwt_service.py` — updated/added tests for the new fail-closed behavior
- `scripts/check_autoclose_keywords.py` — added `bearer_hits_in_message` (imports
  `mailbox_bearer_lint.scan_line`/`mask`); `main()` checks both rules
- `scripts/mail-send.sh` — wrapper refusal text/comments generalized to cover both guards
- `.claude/hooks/autoclose-guard.sh` — same
- `docs/internal/operations/environment-variables.md` — new `## Authentication` section
- `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py` — new test file

**Not changed, flagged for Lead**: `.env.example` (sandbox denies me read/write access to any
`.env*` path — could not confirm or update its `JWT_SECRET_KEY` line).

## Discovered work

- The `web/app.py` fail-open-on-auth-registration-failure pattern (see above) — fixed inline as a
  direct, minimal consequence of item 2; not filed as a separate issue since it was fixed in this
  same pass and reported here with full evidence.
- No other issues discovered beyond what's already tracked in the R5 evaluation.

## Memory & briefing surfaces referenced this session

- **Referenced**: the ruling-relay memo (authority + scope); `A-architecture-security.md` (A-S8/A-S9
  findings, exact line numbers); CLAUDE.md bearer-credential rule (masked-form convention, `ZVHW…8B35`
  shape) — informed test fixture design and refusal-message wording.
- **Loaded but not referenced**: most of CLAUDE.md's worktree/mailbox/sign-off sections (not
  applicable — I don't commit/push).
- **Wanted but not found**: none.

— prog (Sonnet), dispatched by Lead
