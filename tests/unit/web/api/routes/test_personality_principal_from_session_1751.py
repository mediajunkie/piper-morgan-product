"""#1751 — the personality routes must derive the principal from the SESSION,
never from the client.

Before this change the client named the principal on every personality route:
`GET /api/v1/personality/profile/{user_id}` (no auth dependency at all),
`PUT /api/v1/personality/profile/{user_id}`, and `POST /api/v1/personality/enhance`
reading `user_id` out of the request body. The canonical template
(`templates/personality-preferences.html:439/571/617`) hardcoded `"default"` into
all three. #1733 fixed the same hardcoding in a stale static twin by deleting the
twin; the real page kept it.

Fix shape: the `{user_id}` path segment and the body's `user_id` key are REMOVED.
The routes are `/api/v1/personality/profile` (GET/PUT) and the principal comes from
`Depends(get_current_user)` / `Depends(require_admin)`. A caller cannot address
another principal because there is no longer anywhere to write one down.

LAYER (m-43, named honestly): every test drives the REAL ASGI app
(`from web.app import app`) through a real TestClient — real AuthMiddleware, real
JWT crypto (tokens signed by the same AuthContainer JWTService singleton the
middleware validates with), the real route, the real `PiperConfigParser`, and a
real file on disk. Named stubs, exactly two, both startup/infra boundaries outside
the layer under test:
  1. `app.state.config_parser` / `app.state.templates` — the bare TestClient skips
     the startup lifespan, so these are seeded the way `web/startup.py` does.
  2. `services.auth.auth_middleware._user_is_admin` — the live `users.is_admin` DB
     read. The unit suite has no database; patching this one-line boundary is the
     established #1598/#1734 idiom and leaves `require_admin`'s own refuse/allow
     logic, the middleware, the route, and the file write all running for real.

DENOMINATOR (m-44): this file covers the three `/api/v1/personality/*` routes and
the canonical template's three fetch call sites. As of #1751 alone, it did NOT
cover per-user DATA isolation — `PiperConfigParser` ignored `user_id` entirely
and read/wrote one instance-wide file, so two authenticated users saw the same
bytes; #1751 closed only the client-supplied-principal hole.

#1791 (2026-09-24) closed the store gap named above: `PiperConfigParser` now
reads/writes each user's own row (`users.preferences["upm"]`, #1574's store)
and falls back to the instance-wide file ONLY for a user who has never saved a
profile. `TestKnownLimitationDataIsInstanceWide` below is REWRITTEN (not
deleted, per its own original instruction) to pin the new property instead of
the old limitation, and `TestAdminGateOnThePutSurvives` is likewise rewritten:
#1734's `require_admin` gate on the PUT is REMOVED in the same change, because
a per-user write no longer has the global blast radius that gate existed to
hold back.

File-system layer: `PiperConfigParser` resolves `config/PIPER.user.md` relative to
CWD, so each test chdirs into `tmp_path` with a sentinel overlay — the repo's real
overlay (legitimately absent, ADR-075 D4) is never in play.
"""

import hashlib
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth import auth_middleware
from services.auth.container import AuthContainer
from web.app import app
from web.personality_integration import PersonalityResponseEnhancer, PiperConfigParser

REPO_ROOT = Path(__file__).resolve().parents[5]

PROFILE_PATH = "/api/v1/personality/profile"
ENHANCE_PATH = "/api/v1/personality/enhance"
PAGE_PATH = "/personality-preferences"

# The principal the session belongs to, and a DIFFERENT principal the caller
# will try to name. Fixed so failure messages are readable.
USER_A = uuid.UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")

SENTINEL_OVERLAY = """# Piper Morgan User Configuration

```yaml
personality:
  warmth_level: 0.31
  confidence_style: numeric
  action_orientation: low
  technical_depth: detailed
```

## Hands off

If a refused or misaddressed write rewrites this file, #1751's fix has failed.
"""

ATTACK_PAYLOAD = {
    "warmth_level": 0.93,
    "confidence_style": "descriptive",
    "action_orientation": "medium",
    "technical_depth": "simplified",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _token(user_id: uuid.UUID) -> str:
    """A real token signed by the SAME JWTService instance the app's
    AuthMiddleware validates with (AuthContainer is a singleton provider) —
    real crypto, not a mocked request.state (the #1480/#1640 lesson)."""
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


@pytest.fixture
def overlay(tmp_path, monkeypatch) -> Path:
    """Chdir into an isolated tree seeded with a sentinel instance overlay."""
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    overlay_path = config_dir / "PIPER.user.md"
    overlay_path.write_text(SENTINEL_OVERLAY)
    return overlay_path


@pytest.fixture
def client(overlay, monkeypatch):
    """Real app; seed only the startup wiring the bare TestClient skips."""
    from fastapi.templating import Jinja2Templates

    monkeypatch.setattr(app.state, "config_parser", PiperConfigParser(), raising=False)
    monkeypatch.setattr(
        app.state, "personality_enhancer", PersonalityResponseEnhancer(), raising=False
    )
    if getattr(app.state, "templates", None) is None:
        app.state.templates = Jinja2Templates(directory=str(REPO_ROOT / "templates"))
    return TestClient(app, follow_redirects=False)


@pytest.fixture
def as_user_a(client):
    client.cookies.set("auth_token", _token(USER_A))
    try:
        yield client
    finally:
        client.cookies.delete("auth_token")


@pytest.fixture
def as_admin(monkeypatch):
    async def _is_admin(user_id):
        return True

    monkeypatch.setattr(auth_middleware, "_user_is_admin", _is_admin)


@pytest.fixture
def as_non_admin(monkeypatch):
    async def _not_admin(user_id):
        return False

    monkeypatch.setattr(auth_middleware, "_user_is_admin", _not_admin)


class TestPrincipalComesFromTheSession:
    def test_get_profile_reports_the_session_principal(self, as_user_a):
        """The caller supplies no id anywhere; the response names the session's
        own principal. This is the property #1751 exists to create."""
        r = as_user_a.get(PROFILE_PATH)
        assert r.status_code == 200, f"GET {PROFILE_PATH} → {r.status_code}: {r.text[:200]}"
        assert r.json()["user_id"] == str(USER_A), (
            "the profile response does not name the authenticated principal — "
            "the id source is still something other than the session"
        )

    def test_get_profile_requires_authentication(self, client):
        """Unauthenticated → 401 from the real AuthMiddleware. Pins that the new
        address is inside the auth perimeter (the old GET had no gate at all)."""
        r = client.get(PROFILE_PATH)
        assert r.status_code == 401, f"unauthenticated GET {PROFILE_PATH} → {r.status_code}"

    def test_enhance_ignores_a_client_supplied_user_id(self, as_user_a):
        """The body key is not merely unused — supplying another principal's id
        cannot change whose principal the route reports acting as."""
        r = as_user_a.post(
            ENHANCE_PATH,
            json={
                "content": "Task completed successfully",
                "user_id": str(USER_B),
                "confidence": 0.8,
            },
        )
        assert r.status_code == 200, f"POST {ENHANCE_PATH} → {r.status_code}: {r.text[:200]}"
        assert r.json()["data"]["user_id"] == str(USER_A), (
            "a client-supplied body user_id changed the acting principal — "
            "the /enhance route still trusts the client"
        )


class TestCrossUserAddressingIsStructurallyImpossible:
    """User A cannot read or write user B's config, through the real route with
    real auth middleware: the address that used to name B no longer exists."""

    def test_user_a_cannot_read_user_bs_profile(self, as_user_a):
        r = as_user_a.get(f"{PROFILE_PATH}/{USER_B}")
        assert r.status_code == 404, (
            f"GET {PROFILE_PATH}/<other-user> → {r.status_code}; the id-in-path "
            "address must be gone, not merely ignored"
        )

    def test_user_a_cannot_write_user_bs_profile_even_as_admin(self, as_user_a, as_admin, overlay):
        """The strongest form: A is an ADMIN — post-#1791 an admin's OWN PUT is
        unremarkable (TestAdminGateIsRemovedFromThePut), but A still cannot aim
        a write at B, because the `{user_id}` address does not exist at all —
        and the instance overlay is provably untouched either way. Pre-#1751
        this returned 200 and rewrote the (then-global) file."""
        before = _sha256(overlay)
        r = as_user_a.put(f"{PROFILE_PATH}/{USER_B}", json=ATTACK_PAYLOAD)
        assert r.status_code == 404, (
            f"PUT {PROFILE_PATH}/<other-user> → {r.status_code}; there must be no "
            "address a caller (admin or not) can use to aim a write at another principal"
        )
        assert _sha256(overlay) == before, "a misaddressed PUT still wrote the overlay"

    def test_no_route_in_the_app_takes_a_personality_user_id_segment(self):
        """Wiring layer, stated as such: no `{user_id}` personality address may
        survive anywhere in the mounted route table — a second copy of the old
        route would make the two behavioral tests above true and useless."""
        offenders = [
            route.path
            for route in app.routes
            if getattr(route, "path", "").startswith("/api/v1/personality")
            and "{user_id}" in getattr(route, "path", "")
        ]
        assert not offenders, f"client-supplied principal still addressable at: {offenders}"


class TestAdminGateIsRemovedFromThePut:
    """#1791: the store is now per-user, so a write can no longer clobber the
    shared instance file — #1734's admin gate is REMOVED from the PUT in this
    same change (its own filing named this as the exit condition). What used
    to be 403-for-non-admin is now 200, landing in the caller's OWN row, never
    the overlay file. Supersedes the retired
    test_authenticated_non_admin_put_403_and_overlay_untouched /
    test_admin_put_still_works_and_persists pair (renamed+rewritten, not
    deleted, per this file's own precedent)."""

    def test_authenticated_non_admin_put_200_persists_own_row_overlay_untouched(
        self, as_user_a, as_non_admin, overlay
    ):
        before = _sha256(overlay)
        r = as_user_a.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 200, (
            f"non-admin PUT {PROFILE_PATH} → {r.status_code}; the #1734 admin gate "
            "should be gone as of #1791"
        )
        body = r.json()
        assert body["data"]["warmth_level"] == 0.93
        assert body["scope"] == "user", f"expected scope='user', got {body['scope']!r}"
        assert _sha256(overlay) == before, "a per-user PUT must not touch the shared overlay"

    def test_unauthenticated_put_401_before_any_admin_lookup(self, client, overlay, monkeypatch):
        called = []

        async def _should_not_run(user_id):  # pragma: no cover - asserted absent
            called.append(user_id)
            return True

        monkeypatch.setattr(auth_middleware, "_user_is_admin", _should_not_run)
        before = _sha256(overlay)
        r = client.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 401, f"unauthenticated PUT {PROFILE_PATH} → {r.status_code}"
        assert not called, "an admin DB read ran even though require_admin was removed"
        assert _sha256(overlay) == before

    def test_admin_put_behaves_identically_to_non_admin(self, as_user_a, as_admin, overlay):
        """Admin status must no longer change this route's behavior at all —
        not merely 'also still works', but the SAME outcome as a non-admin."""
        before = _sha256(overlay)
        r = as_user_a.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 200, f"admin PUT {PROFILE_PATH} → {r.status_code}: {r.text[:200]}"
        body = r.json()
        assert body["data"]["warmth_level"] == 0.93
        assert body["scope"] == "user"
        assert (
            _sha256(overlay) == before
        ), "even an admin's per-user write must not touch the shared overlay"


class TestCanonicalTemplateSendsNoUserId:
    """#1751 AC 3: a render-layer pin on the id source, not a curl-200. Renders the
    real template through the real auth-gated route with a real cookie."""

    def test_rendered_page_has_no_hardcoded_default_user_id(self, as_user_a):
        r = as_user_a.get(PAGE_PATH)
        assert r.status_code == 200, f"{PAGE_PATH} → {r.status_code} with a valid cookie"
        body = r.text
        assert "/api/v1/personality/profile/default" not in body, (
            "the rendered page still fetches the hardcoded 'default' profile "
            "(#1751 lines 439/571)"
        )
        assert 'user_id: "default"' not in body, (
            "the rendered page still sends a hardcoded user_id in the /enhance "
            "body (#1751 line 617)"
        )

    def test_rendered_page_calls_the_session_scoped_address(self, as_user_a):
        """Not just absence of the old string — the page must actually call the
        id-free address, or 'no hardcoded default' would pass on a broken page."""
        body = as_user_a.get(PAGE_PATH).text
        assert f'fetch("{PROFILE_PATH}"' in body, (
            f"the page does not call {PROFILE_PATH}; the previous assertion could "
            "pass on a page that calls nothing at all"
        )


class TestPerUserDataSeparationNowExists:
    """#1791 pin, REWRITTEN from the retired TestKnownLimitationDataIsInstanceWide
    per that class's own instruction ("update this file's DENOMINATOR note,
    which currently documents the opposite" — now done, see the module
    docstring). If any assertion here ever fails, the store has regressed to
    instance-wide and #1791 needs re-opening."""

    def test_a_users_own_saved_profile_is_invisible_to_a_different_user(self, client):
        """User A saves a profile; user B's read is untouched by it — the
        opposite of the pre-#1791 behavior this class used to pin."""
        client.cookies.set("auth_token", _token(USER_A))
        client.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        a = client.get(PROFILE_PATH).json()
        client.cookies.delete("auth_token")

        client.cookies.set("auth_token", _token(USER_B))
        b = client.get(PROFILE_PATH).json()
        client.cookies.delete("auth_token")

        assert a["user_id"] == str(USER_A) and b["user_id"] == str(USER_B)
        assert (
            a["data"]["warmth_level"] == 0.93 and a["scope"] == "user"
        ), "user A's own saved profile did not read back as scope='user'"
        assert b["data"] != a["data"], (
            "user B's read picked up user A's saved profile — the store is "
            "still instance-wide, not per-user"
        )
        assert b["scope"] == "instance", (
            "user B has never saved a profile and must read the instance "
            "default, not user A's saved one"
        )

    def test_a_user_with_no_saved_profile_gets_the_instance_default_not_emptiness(
        self, as_user_a, overlay
    ):
        """A fresh user gets the generic voice (the instance default file), not
        an empty/zeroed profile — the AC's explicit requirement."""
        r = as_user_a.get(PROFILE_PATH).json()
        assert r["scope"] == "instance"
        assert r["data"]["warmth_level"] == 0.31, (
            "a user with nothing saved must read the instance-wide default "
            "file's actual values, not a hardcoded/empty fallback"
        )

    def test_response_scope_reflects_which_store_actually_served_the_read(self, as_user_a, overlay):
        """scope is now a real, observable fact about the response — not the
        hardcoded literal #1751 shipped — so a client can tell the two apart:
        'instance' before any save, 'user' after one."""
        before = as_user_a.get(PROFILE_PATH).json()
        assert before["scope"] == "instance"

        as_user_a.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        after = as_user_a.get(PROFILE_PATH).json()
        assert after["scope"] == "user"
