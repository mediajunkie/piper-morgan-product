# Audit: #857 against feature.md template

**Issue**: INFRA: Token refresh mechanism for seamless session continuity
**Auditor**: Lead Developer
**Date**: 2026-05-11 ~09:05
**Phase**: 1 of 3 (Issue audit) — pre-gameplan gate

---

## TL;DR

**Verdict: ⚠️ Issue body's premise is wrong (Pattern-067 firing).** The body claims *"JWT refresh tokens: 7-day expiry (already issued, `jwt_service.py:101`)"* — but investigation shows refresh tokens are **never actually issued in production**. `generate_refresh_token()` is defined in `jwt_service.py:210` but has **zero production callers**. Login generates only access tokens, no refresh cookie/storage exists.

This means #857's actual scope is materially larger than the body framed:
- **Body framed scope**: add a `/refresh` endpoint + frontend wiring (~2-3 hr)
- **Real scope**: also modify login to issue+store refresh tokens, design the storage shape (cookie? header? body?), add refresh token rotation, plus the endpoint + frontend (~5-6 hr)

PM disposition needed before proceeding.

---

## Phase 0 findings

### What I checked

**Backend** (`services/auth/jwt_service.py`):
- ✅ `access_token_expire_minutes = 30` (default, line 100)
- ✅ `refresh_token_expire_days = 7` (default, line 101)
- ✅ `generate_refresh_token` method exists (line 210)
- ✅ `refresh_access_token` method exists (line 411) — accepts refresh token, returns new access token; audit-logged
- ❌ **`generate_refresh_token` has zero production callers** (grep across services/ + web/ excluding tests/__pycache__)

**Web routes** (`web/api/routes/auth.py`):
- Existing endpoints: `/login` (line 77), `/logout` (line 245), `/me` (line 359), `/change-password` (line 414)
- ❌ **No `/refresh` endpoint exists**
- Login issues access token, sets `auth_token` cookie (max-age 86400 = 24h, but JWT inside expires in 30 min — a separate UX paper-cut)
- **No refresh token is generated or stored anywhere** in the login flow

**Frontend** (`web/static/js/`):
- `auth.js`: simple login form; uses cookie-based auth (`credentials: 'include'`); doesn't handle tokens directly
- `api-wrapper.js`: fetch wrapper with error handling; **doesn't handle 401 → refresh** flow
- `chat.js:535-545`: #840 C2 redirect — detects `auth_expired` flag from intent endpoint, shows message, redirects to /login after 2s. **This is the current fallback behavior.**

**`refresh_token` references found in `web/api/routes/settings_integrations.py`** are all about OAuth refresh tokens for **external integrations** (Google Calendar, Slack) — NOT our own JWT refresh tokens. Different domain.

### Pattern-067 instance

Same shape as #936 (UserService dead code) + #935 (analytics unreachable) + #921 (issue body understated upgrade scope) + #1041 (2-of-6 WIRE-* superseded) + the #983 label-convention thread. Issue body claims state ("already issued") that doesn't match reality (zero callers, no storage).

Issue was filed Feb 25 2026; codebase has evolved substantially since (~2.5 months). The body may have been accurate at filing time and drifted, OR was inaccurate at filing time and never caught. Either way, audit-cascade Phase 0 caught it before scoping work to a phantom premise.

---

## The disposition question for PM

Three options surface:

### Option A — Full refresh implementation (~5-6 hr)

What the body's AC ask amounts to, expanded for the real state:

1. Modify `/login` to also issue a refresh token; set as separate cookie (`refresh_token` httponly + appropriate flags)
2. Add `/api/v1/auth/refresh` endpoint; consume refresh token from cookie; call `JWTService.refresh_access_token`; also generate NEW refresh token (rotation per AC); set both cookies in response
3. Frontend: modify `api-wrapper.js` (or a new auth wrapper) to intercept 401 → attempt refresh → retry original request on success → fall back to existing #840 C2 redirect on refresh failure
4. Refresh token rotation (NEW refresh token on each use; old token blacklisted)
5. Tests: unit for endpoint + integration for the full refresh flow

**Effort**: ~5-6 hr Lead Dev + subagent for tests. Worktree-isolated.

**Risk**: medium — touches the auth flow on both sides. Existing 30-min UX paper-cut would become invisible. Real value.

### Option B — Scope down: lock 30-min expiry as alpha UX, file as post-MVP

Per the issue body's own framing: *"Not blocking M0 — C2 redirect is functional. Improves UX for longer sessions."*

We're now post-M2 (M2f tail). The C2 redirect still works. Refresh-token UX is a nice-to-have, not a blocker. The PM "don't pre-build for hypothetical futures" framing applies — we don't have production users hitting the 30-min expiry; we have alpha testers who can re-login.

**Disposition**: close #857 as "deferred to post-MVP / pre-beta"; the implementation work waits until we have a real UX signal (beta user complaints about re-login friction).

**Effort**: ~30 min — close with framing memo + add to deferred list in BRIEFING.

### Option C — Hybrid: simple-but-not-seamless refresh (~2-3 hr)

Build just the `/refresh` endpoint + frontend retry logic, but DON'T modify login to issue refresh tokens. The endpoint can only be hit if a refresh token exists — which it doesn't, today. So this is essentially building scaffolding for a future shape without changing current behavior.

**This is anti-pattern** — building scaffolding nobody uses, exactly the dead-code shape we just deleted in #935/#936. Reject.

---

## My recommendation: Option B (defer)

Same logic as Group B deletions (#935/#936 reasoning carried forward):
1. Pre-release dev env, no production users with 30-min session friction
2. Existing C2 redirect (#840) works correctly — graceful degradation when token expires
3. Refresh-token UX is beta-readiness shape, not MVP
4. "Don't pre-build for hypothetical futures" applies cleanly here
5. The disposition would be: defer to post-MVP; if/when beta surfaces the friction, file a new issue with concrete scope informed by actual user signal

Option A is also reasonable if PM wants to ship the proper UX now — the work is real and bounded (~5-6 hr). My lean is B because we already have a working fallback and the work cost is real.

---

## Cohort impact

If B: **M2f Group C is effectively complete with #921 alone** — #857 becomes the next deferred item alongside #1074 (full-suite verification). Group C done; M2f move on to E.

If A: Group C wraps with #857 fully shipped. ~5-6 hr Lead Dev work today.

---

## Cross-references

- Pattern-067 Issue-Body Reality Mismatch (this is the 6th instance in 2 weeks)
- #840 C2 redirect (current fallback, working)
- #854 Cross-Turn State Continuity (parent epic)
- JWTService.refresh_access_token (`jwt_service.py:411`) — the backend half exists
- generate_refresh_token (`jwt_service.py:210`) — defined but unused

---

## Action

Surfacing **Option A vs B** for PM disposition before any implementation. Phase 0 work durable in this memo; Phase 1+ contingent on decision.

— Lead Developer, 2026-05-11 ~09:15 PT
