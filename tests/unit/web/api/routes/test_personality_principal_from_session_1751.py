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
the canonical template's three fetch call sites. It does NOT cover, and must not be
read as covering, per-user DATA isolation — see
`TestKnownLimitationDataIsInstanceWide` below. `PiperConfigParser` ignores `user_id`
entirely and reads/writes one instance-wide file (`config/PIPER.user.md`), so two
authenticated users still see the same bytes. What #1751 closes is the
client-supplied-principal hole; the store rewrite is tracked separately.

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
        """The strongest form: A is an ADMIN (so the #1734 gate admits) and still
        cannot aim a write at B — and the instance overlay is provably untouched.
        Pre-fix this returned 200 and rewrote the file."""
        before = _sha256(overlay)
        r = as_user_a.put(f"{PROFILE_PATH}/{USER_B}", json=ATTACK_PAYLOAD)
        assert r.status_code == 404, (
            f"PUT {PROFILE_PATH}/<other-user> → {r.status_code}; an admin must not "
            "be able to address another principal on a route whose store is global"
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


class TestAdminGateOnThePutSurvives:
    """#1734's gate is load-bearing for #1751's blast-radius assessment; pin that
    removing the path segment did not remove the gate."""

    def test_authenticated_non_admin_put_403_and_overlay_untouched(
        self, as_user_a, as_non_admin, overlay
    ):
        before = _sha256(overlay)
        r = as_user_a.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 403, (
            f"non-admin PUT {PROFILE_PATH} → {r.status_code}; the #1734 admin gate "
            "must survive the route rename"
        )
        assert _sha256(overlay) == before, "a refused PUT still wrote the overlay"

    def test_unauthenticated_put_401_before_any_admin_lookup(self, client, overlay, monkeypatch):
        called = []

        async def _should_not_run(user_id):  # pragma: no cover - asserted absent
            called.append(user_id)
            return True

        monkeypatch.setattr(auth_middleware, "_user_is_admin", _should_not_run)
        before = _sha256(overlay)
        r = client.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 401, f"unauthenticated PUT {PROFILE_PATH} → {r.status_code}"
        assert not called, "admin DB read ran for an unauthenticated caller"
        assert _sha256(overlay) == before

    def test_admin_put_still_works_and_persists(self, as_user_a, as_admin, overlay):
        """The gate must not break the route for the people it admits."""
        r = as_user_a.put(PROFILE_PATH, json=ATTACK_PAYLOAD)
        assert r.status_code == 200, f"admin PUT {PROFILE_PATH} → {r.status_code}: {r.text[:200]}"
        assert r.json()["data"]["warmth_level"] == 0.93
        assert "0.93" in overlay.read_text(), "admin save reported success but did not persist"


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


class TestKnownLimitationDataIsInstanceWide:
    """Honest scope statement, pinned so it cannot silently drift into a claim of
    per-user isolation. `PiperConfigParser` ignores user_id and reads/writes one
    instance-wide file, so #1751 closes the client-supplied-principal hole WITHOUT
    creating per-user data separation. If this test ever fails, per-user storage
    has arrived and this file's DENOMINATOR note needs rewriting (not deleting)."""

    def test_two_users_read_the_same_instance_config(self, client):
        client.cookies.set("auth_token", _token(USER_A))
        a = client.get(PROFILE_PATH).json()
        client.cookies.set("auth_token", _token(USER_B))
        b = client.get(PROFILE_PATH).json()
        client.cookies.delete("auth_token")

        assert a["user_id"] == str(USER_A) and b["user_id"] == str(USER_B)
        assert a["data"] == b["data"], (
            "profiles now differ per user — the store became per-user; update this "
            "file's DENOMINATOR note, which currently documents the opposite"
        )

    def test_response_declares_its_scope_honestly(self, as_user_a):
        """The payload says instance-wide, so a client cannot mistake the
        principal echo for evidence the data is private to that principal."""
        assert as_user_a.get(PROFILE_PATH).json()["scope"] == "instance"
