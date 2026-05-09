# Audit: #936 against feature.md template

**Issue**: TECH-DEBT: UserService stores all user data in in-memory dicts
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~11:10
**Phase**: 1 of 3 (Issue audit) — pre-gameplan gate

---

## TL;DR

**Verdict: ⚠️ Issue body is partially WRONG.** The body claims "All user session data lost on restart" and "Multi-tenancy isolation depends on in-memory state." Investigation suggests **UserService's in-memory dicts are dead state** — nothing populates them in production. The acceptance criteria parenthetical ("or explicitly documented as auth-gateway pattern") may be the correct path; the migration-to-DB framing is the wrong one.

**1 PM question + 1 architect-routing recommendation** before gameplan.

---

## What the body claims

> *"`services/auth/user_service.py:116` uses plain Python dicts (`_users`, `_sessions`, `_email_to_user_id`) for all user data. Users and sessions are lost on server restart. **All user session data lost on restart. Multi-tenancy isolation depends on in-memory state.**"*

## What investigation found

### `UserService` IS instantiated in production

- `web/app.py:58`: `user_service = UserService()` instantiated at startup
- `web/app.py:60`: passed to `AuthMiddleware` as constructor arg
- `services/auth/auth_middleware.py:177`: `session = self.user_service.get_session(claims.session_id)` called per request

### But nothing populates `_sessions` or `_users`

```bash
$ grep -rn "user_service\.create_session\|user_service\.create_user" services/ web/
# ZERO production callsites for create_session
# ZERO production callsites for create_user
```

The class defines `create_session()` at line 250 and `create_user()` at line 123. Neither is called anywhere in production code. Tests call them (in `tests/security/test_user_api_key_service.py` and similar) — but production code never does.

### What's actually doing user/session work

Real production auth flow (verified via the `/api/v1/auth/login` endpoint we used during canonical retest this morning):

1. `users` table in PostgreSQL — actual user records (we have a `canonical-test` user with UUID `b4696a1f-a091-4913-9466-43b4e8bbbaed`)
2. `AuthService` (separate from `UserService`) handles login via `users` table + bcrypt password hash
3. Returns a JWT containing claims (`user_id`, `username`, `email`, `scopes`, etc.)
4. `AuthMiddleware` validates JWT and reads claims
5. `request.state.user_id = claims.user_id` set from JWT claims directly (line 174)
6. **`UserService.get_session()` is then called (line 177) but returns None because `_sessions` is empty.** The `if session:` guard at line 178 means the next line `request.state.session = session` never fires in production.

So:
- `request.state.user_id` IS set (from JWT)
- `request.state.session` is NEVER set in production (UserService doesn't have any sessions)
- Multi-tenancy ISOLATION is enforced via `request.state.user_id` (set from JWT), NOT via `_users` / `_sessions`

### Conclusion

**`UserService.get_session()` always returns None in production.** It's a no-op codepath. The `_sessions` / `_users` dicts are not "lost on restart" because they were never populated to begin with.

The body's framing ("user data lost on restart") is misleading. The actual situation is: **a parallel session-management codepath that nobody uses**.

---

## The 1 PM question

### Which path do we want?

**Option A — Remove UserService entirely** (dead-code cleanup):
- Delete `services/auth/user_service.py`
- Remove the `user_service` constructor arg from `AuthMiddleware`
- Remove the `get_session()` call from middleware (line 177-179)
- Update `web/app.py:58` to not instantiate it
- **Risk**: tests that exercise UserService directly will break — need to either delete those tests or ratify as migration cleanup
- **Effort**: ~2-3 hr including test impact

**Option B — Wire UserService to the real `users` DB table**:
- Replace in-memory dicts with SQLAlchemy queries against `users` + a new `user_sessions` table
- Hook `create_user` / `create_session` to the auth flow (login emits `create_session`; logout cleans up)
- Update tests to use real DB or mock the DB-backed UserService
- **Risk**: actually CHANGES production behavior — `request.state.session` would now sometimes be set, downstream code may not be ready for that
- **Effort**: ~6-10 hr; substantial work; needs Architect review (data model decisions, session-vs-JWT scope)

**Option C — Document as legacy / phase-out path**:
- Replace TODO with a "DEPRECATED — see #936 / new-issue" comment
- Note that `UserService` is intentionally a no-op compatibility shim awaiting full removal
- File a new issue for actual removal at a future milestone (post-MVP)
- **Risk**: leaves dead code in place; future agents may misunderstand and try to "fix" it
- **Effort**: ~30 min

### My recommendation: Option A (delete it)

Reasoning:
- We're in pre-release dev env. Dead code that's wired into production but does nothing is worse than no code — it confuses readers + invites accidental "fixes."
- The acceptance criteria already authorizes a non-DB path: *"or explicitly documented as auth-gateway pattern."* But the gateway-pattern framing presumes UserService is functional; investigation shows it's not.
- Real auth-gateway / session-management is shared between AuthService + JWT + (potentially) a future `user_sessions` table. None of those need UserService.
- Removing it now means future agents working in `services/auth/` see only the active codepaths. That's better hygiene.

Option B (DB migration) seems wrong: we'd be implementing a feature (real session management via UserService) that no production callsite needs.

Option C (document and defer) is acceptable but kicks the can. The cleanup is small enough to do now.

---

## Architect-routing recommendation

This issue probably needs a 5-min Architect review before commitment to Option A. UserService might be reserved for a planned future feature (e.g., OAuth federation per #470 RBAC epic, or multi-tenant workspace isolation). I see references to OAuth in the file but no production wiring. Worth Architect's eyes.

Surfacing in this audit so PM can route to Architect if they want a second opinion before approving Option A.

---

## Audit matrix (abbreviated)

| Template Requirement | Status |
|---|---|
| Title + LABEL | ✅ |
| Priority | ⚠️ "P:medium" stated — possibly wrong if dead code ⇒ much smaller scope |
| Problem Statement — Current State | ❌ **factually inaccurate** ("user data lost on restart" — not actually lost because never stored to begin with) |
| Problem Statement — Impact | ❌ **factually inaccurate** ("multi-tenancy isolation depends on in-memory state" — actual isolation is via JWT claims) |
| Goal | ⚠️ acceptance criteria leaves it open ("backed by DB OR documented") |
| What Already Exists | ❌ Body doesn't acknowledge `users` table + `AuthService` + JWT do the real work |
| Phases / Effort | ❌ Missing |
| STOP Conditions | ❌ Missing |
| Dependencies | ⚠️ Mentions #470 (RBAC) and #817 (closed); should also reference current AuthService + JWT-based auth |

---

## Action

Surfacing **Q1 (Option A vs B vs C)** plus the **Architect-routing recommendation** for PM disposition. I should not proceed to gameplan with the body's premise (DB migration) because investigation indicates the premise is wrong.

Once Q1 is answered, gameplan will be small (Option A: ~30 min gameplan; Option C: trivial; Option B: would need full audit-cascade re-run with proper scope).

— Lead Developer, 2026-05-09 ~11:20
