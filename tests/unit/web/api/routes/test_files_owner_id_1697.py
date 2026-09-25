"""#1697 — GET /api/v1/files/list's file-kind (`kind: "file"`) projection
carried no `owner_id`, so templates/files.html rendered "Uploaded by: " with
nothing after the colon on every file card (isOwner(file) reads
`file.owner_id === window.currentUser.user_id`, which is always false when
`owner_id` is missing — so the ownerIndicator branch fired for the caller's
OWN files, which the owner-scoped query never should have let through).

Root cause + fix, confirmed by reading the route: `list_files` queries
`UploadedFileDB WHERE owner_id == current_user.sub` — every returned
file-kind row IS the caller's own, with no admin/cross-owner path (unlike
get_file/download_file/preview_file, which do support an admin bypass). The
artifact-kind projection in the SAME response already carries `owner_id`
(82d8b56, #1165 slice 3) specifically because "files.html isOwner/delete
permission needs it" — the file-kind entries were the missed twin. Fix:
mirror that field onto file-kind entries too.

Decision explicitly considered and rejected: dropping the "Uploaded by"
label from the template instead of adding the field. Rejected because
`owner_id` is not merely a display value here — it is what isOwner() (and,
through it, canDeleteFile()/the tag-edit button) uses to decide whether the
CALLER's own delete/edit-tag controls render at all. Omitting owner_id left
those controls silently hidden for every non-admin caller on their own
uploaded files, not just the reported blank label. Adding the field (like
the artifact projection already does) fixes both the display and the
permission-gating bug from a single root cause, and — because the query is
owner-scoped — has the side effect of making the "Uploaded by" branch never
fire in practice (isOwner() is now correctly always true for a returned
row), with no template change needed for this half of the fix. (The
template ALSO got a small defense-in-depth guard — see
tests/frontend/unit/files-page-owner-indicator-1697.test.js — so a future
gap in this API contract can never reproduce a dangling label either.)

LAYER (m-43, named honestly): a real ASGI app (`from web.app import app`)
through a real TestClient, the real AuthMiddleware/get_current_user
dependency chain, and a real JWT minted by the same AuthContainer
JWTService singleton instance the app registered (the #1480/#1640 pattern —
not a mocked request.state). The seeded row is a real Postgres row (DB-
backed per the #1401/B15 house pattern), not a mocked session — this is the
layer that answers "what does the live endpoint actually send", which is
exactly what #1697 was filed against (a live API-response inspection).

Denominator (m-44): covers GET /api/v1/files/list's file-kind (`kind:
"file"`) projection only, for #1697. The artifact-kind projection already
carried owner_id before this fix; one canary test below re-asserts it
unchanged rather than re-deriving its own coverage.
"""

import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.auth.container import AuthContainer
from web.app import app

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
def client():
    # Bare TestClient (no `with`) skips the startup lifespan — list_files()
    # initializes the DB itself (`if not db._initialized: await
    # db.initialize()`), so no extra app.state wiring is needed for this route
    # (unlike a Jinja-rendered page, which would need app.state.templates).
    return TestClient(app, follow_redirects=False)


def _auth_cookie(user_id: uuid.UUID, email: str) -> str:
    """A real token signed by the SAME JWTService instance the app's
    AuthMiddleware/get_current_user validates with (AuthContainer is a
    singleton provider) — real crypto, not a mocked request.state."""
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=user_id,
        user_email=email,
        scopes=["user"],
    )


@pytest.fixture
async def file_owner():
    """One real user row + one real uploaded_files row; cleans up both."""
    engine = create_async_engine(_DB_URL, echo=False)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    uid = uuid.uuid4()
    uid_s = str(uid)
    email = f"f1697_{uid_s[:8]}@test.example.com"
    now = datetime.now(timezone.utc)
    file_id = f"file_{uuid.uuid4().hex[:12]}"
    async with factory() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {"id": uid_s, "u": f"f1697_{uid_s[:8]}", "e": email, "now": now},
        )
        await s.execute(
            text(
                "INSERT INTO uploaded_files (id, owner_id, filename, file_type, "
                "file_size, storage_path, upload_time) "
                "VALUES (:id, CAST(:o AS uuid), :fn, 'text/plain', 12, :sp, :now)"
            ),
            {
                "id": file_id,
                "o": uid_s,
                "fn": "owner-id-probe.txt",
                "sp": "/does/not/need/to/exist.txt",
                "now": now,
            },
        )
        await s.commit()
    try:
        yield uid, uid_s, email, file_id
    finally:
        async with factory() as s:
            await s.execute(
                text("DELETE FROM uploaded_files WHERE owner_id = CAST(:u AS uuid)"),
                {"u": uid_s},
            )
            await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid_s})
            await s.commit()
        await engine.dispose()


class TestFileListOwnerId:
    def test_file_kind_entry_carries_owner_id_matching_caller(self, client, file_owner):
        uid, uid_s, email, file_id = file_owner
        client.cookies.set("auth_token", _auth_cookie(uid, email))
        try:
            r = client.get("/api/v1/files/list")
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 200, r.text
        body = r.json()
        entries = [f for f in body["files"] if f["file_id"] == file_id]
        assert len(entries) == 1, f"seeded file not found in response: {body['files']}"
        entry = entries[0]
        assert entry["kind"] == "file"
        assert "owner_id" in entry, "file-kind entries must carry owner_id (#1697)"
        assert entry["owner_id"] == uid_s, (
            "owner_id must equal the caller's own id: GET /list is "
            "owner-scoped (WHERE owner_id == current_user.sub), so every "
            "returned file-kind row IS the caller's own"
        )

    def test_unauthenticated_request_is_401_not_leaked(self, client):
        """Canary: the fix must not have loosened the route's auth gate."""
        r = client.get("/api/v1/files/list")
        assert r.status_code in (401, 403), r.text
