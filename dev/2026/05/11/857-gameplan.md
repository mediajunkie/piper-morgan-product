# Gameplan: #857 — Token refresh mechanism (Option A)

**Issue**: INFRA: Token refresh mechanism for seamless session continuity
**PM Disposition (2026-05-11)**: Option A — full implementation
**Auditor**: Lead Developer
**Date**: 2026-05-11 ~09:30
**Phase**: 2 of 3 (Gameplan) — pre-implementation gate
**Audit-cascade reference**: `dev/2026/05/11/857-issue-audit.md`
**Branch / worktree**: `claude/857-token-refresh` at `../piper-morgan-product-857`

---

## Phase -1: Infrastructure verification

**Work characteristics**: Backend (auth route + JWT service) + frontend (api-wrapper.js) + tests. Pre-release dev env. Phase 0.5/0.6/0.7/0.8 N/A per the M2f Group A precedent (no UI design changes, no data flow new shape, no conversation, no completion side effects).

**Phase -1 verification**:
- ✅ Phase 0 audit complete; PM disposition (A) recorded
- ✅ Worktree isolated; no cross-agent collision risk
- ✅ `JWTService.refresh_access_token` exists (line 411); `generate_refresh_token` exists (line 210) but unused
- ✅ Existing cookie-based auth pattern at `/login` (sets `auth_token` cookie, 24h max-age)
- ✅ Existing #840 C2 redirect fallback in `chat.js:535-545`

---

## Phase 1: Modify /login to issue refresh token (~45 min)

### Changes to `web/api/routes/auth.py` login endpoint

After existing access-token generation, also generate refresh token:

```python
# Generate refresh token (Issue #857)
refresh_token = jwt_service.generate_refresh_token(
    user_id=user_id,
    user_email=user_email,
    session_id=None,
    workspace_id=None,
)

# Set refresh token cookie (separate from access token cookie)
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,
    secure=is_https,
    samesite="lax",
    max_age=7 * 86400,  # 7 days (matches JWT refresh_token_expire_days default)
)
```

The refresh-token cookie has a longer max-age than the access-token cookie. Both are httponly (not JS-readable).

### LoginResponse model — no shape change

Refresh token NOT returned in body — cookie-only. Frontend doesn't need to handle the refresh token directly; it lives in the cookie that the browser sends automatically.

---

## Phase 2: /api/v1/auth/refresh endpoint (~45 min)

### Add new route to `web/api/routes/auth.py`

```python
@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request: Request,
    response: Response,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Generate a new access token from a valid refresh token.

    Issue #857: INFRA token refresh mechanism.
    Reads refresh_token from cookie; generates new access_token + rotates refresh_token.
    """
    # Read refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, detail="No refresh token")

    # Get new access token from JWTService
    audit_context = build_audit_context(request)
    async with AsyncSessionFactory.session_scope_fresh() as db_session:
        new_access_token = await jwt_service.refresh_access_token(
            refresh_token=refresh_token,
            session=db_session,
            audit_context=audit_context,
        )

    if not new_access_token:
        # Invalid/expired refresh token — clear cookies + 401
        response.delete_cookie("auth_token")
        response.delete_cookie("refresh_token")
        raise HTTPException(401, detail="Refresh token invalid or expired")

    # Decode the new access token to get user info for the response
    claims = await jwt_service.validate_token(new_access_token)

    # Generate a NEW refresh token (rotation per AC)
    new_refresh_token = jwt_service.generate_refresh_token(
        user_id=claims.user_id,
        user_email=claims.user_email,
        session_id=claims.session_id,
        workspace_id=claims.workspace_id,
    )

    # Set both cookies
    is_https = request.url.scheme == "https"
    response.set_cookie(
        key="auth_token",
        value=new_access_token,
        httponly=True,
        secure=is_https,
        samesite="lax",
        max_age=86400,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=is_https,
        samesite="lax",
        max_age=7 * 86400,
    )

    return LoginResponse(
        token=new_access_token,
        user_id=claims.user_id,
        username=claims.username if hasattr(claims, "username") else claims.user_email,
    )
```

### Decision: token rotation strategy

**Decision**: rotate refresh token on every use (AC explicit). The old refresh token is naturally invalidated by being replaced in the cookie; we don't add it to a blacklist (the existing TokenBlacklist is for explicit revocations, not natural rotation). If a stolen refresh token is used in parallel with the legitimate user's refresh, the parallel use would generate a different access+refresh pair; the user's next session-aware operation would notice the inconsistency. For alpha, this rotation-without-blacklist is sufficient.

(Could add blacklist-on-rotation in a future enhancement if a stolen-token scenario becomes a real concern.)

### Auth middleware exclude list

`/api/v1/auth/refresh` needs to be in the exempt list so it can be hit with an expired access token. Add to `auth_middleware.py` EXEMPT_AUTH_ENDPOINTS list.

---

## Phase 3: Frontend retry-on-401 wrapper (~1 hr)

### Modify `web/static/js/api-wrapper.js`

Add a retry-on-401 path:

```javascript
async fetch(url, options = {}) {
  const controller = new AbortController();
  const timeout = options.timeout || this.defaultTimeout;

  const timeoutId = setTimeout(() => {
    controller.abort();
  }, timeout);

  try {
    let response = await fetch(url, {
      ...options,
      signal: controller.signal,
      credentials: 'include',  // Ensure cookies sent
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    // Issue #857: attempt refresh on 401, retry on success
    if (response.status === 401 && !options._retried) {
      const refreshResponse = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        credentials: 'include',
      });

      if (refreshResponse.ok) {
        // Refresh succeeded; retry original request
        response = await fetch(url, {
          ...options,
          signal: controller.signal,
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            ...options.headers
          },
          _retried: true,  // Prevent infinite retry loop
        });
      }
      // If refresh failed, fall through to handleHttpError → existing #840 C2 redirect via chat.js
    }

    clearTimeout(timeoutId);

    if (!response.ok) {
      await this.handleHttpError(response);
    }

    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    this.handleNetworkError(error);
    throw error;
  }
}
```

### Don't break existing #840 fallback

The chat.js `result.auth_expired` flag handling continues to work as the FALLBACK when refresh ALSO fails. The two layers compose:
- Layer 1 (new): api-wrapper attempts seamless refresh on 401
- Layer 2 (existing): if refresh fails, chat.js shows the message + redirects to /login

---

## Phase 4: Tests (subagent — ~1.5 hr)

### Backend unit tests

Add to `tests/auth/test_auth_endpoints.py` (or new file):

1. `test_refresh_endpoint_succeeds_with_valid_refresh_token` — generate a valid refresh token, POST to /refresh, assert 200 + new access_token in body + new refresh_token cookie set
2. `test_refresh_endpoint_fails_with_no_refresh_token` — POST to /refresh without cookie, assert 401
3. `test_refresh_endpoint_fails_with_expired_refresh_token` — generate an expired refresh token, POST, assert 401 + cookies cleared
4. `test_refresh_endpoint_rotates_refresh_token` — call refresh; assert the new refresh token in response cookie differs from the input refresh token
5. `test_login_now_issues_refresh_token_cookie` — POST /login, assert refresh_token cookie is set with appropriate max-age

### Frontend tests

ApiWrapper retry logic — verify via Jest-or-equivalent (or skip if no JS test infra; the integration testing via canonical retest is sufficient signal).

### Smoke test

Manual via dev server:
1. Login → verify both cookies set
2. Wait for access token expiry (or manually expire via dev tool)
3. Make a request → verify it transparently refreshes + succeeds
4. Manually delete refresh token cookie → make request → verify fallback to login redirect

---

## Phase Z: Verification + handoff (~30 min)

- Targeted test sweep on tests/auth/ + tests/integration/test_intent_wiring_integration.py
- Smoke test against running server
- Update issue evidence comment
- Merge to main

---

## Acceptance criteria (from issue body)

- [ ] Refresh endpoint exists and works
- [ ] Frontend automatically attempts refresh on token expiry
- [ ] Successful refresh is invisible to the user
- [ ] Failed refresh falls back to login redirect
- [ ] Refresh token rotation (new refresh token issued on use)

---

## STOP Conditions

- Login endpoint changes break existing login tests in unexpected ways → surface, may indicate scope re-think
- /refresh endpoint's session-handling for audit logging is fragile (the `session=db_session` param expects a real session) → may need to adapt or skip audit-on-refresh
- Frontend retry creates infinite loops in edge cases I didn't anticipate → STOP and investigate
- AuthMiddleware exclude list change breaks something else

---

## Effort estimate

**Total: ~4-5 hours**

- Phase 1 (login change): 45 min
- Phase 2 (/refresh endpoint): 45 min
- Phase 3 (frontend wrapper): 1 hr
- Phase 4 (tests via subagent): 1.5 hr
- Phase Z (verify + handoff): 30 min

---

## Dependencies

- `JWTService.refresh_access_token` exists (verified Phase 0)
- `generate_refresh_token` exists (verified Phase 0)
- TokenBlacklist exists for explicit revocations (separate; not used by natural rotation)

---

## Audit-cascade self-check

Phase 0.5/0.6/0.7/0.8 N/A per M2f Group A precedent. Lead Dev solo for Phases 1+2+3 (tightly coupled to design); subagent for Phase 4 tests (bias toward subagents for testing per PM May 9 directive). All paths documented; STOP conditions explicit.

— Lead Developer, 2026-05-11 ~09:35 PT
