"""#1510 (inferred half) AC: REAL-DB round-trip for the verified-inference store.

Mocked-interface persistence tests are how #1548/#1603 shipped broken — this
file drives the REAL preference persistence (users.preferences JSONB via
collaboration_gate's seam) against dev Postgres. Requires live Postgres
(POSTGRES_PORT=5433, docker compose up -d).

Covers, against the real store:
- verified → stored with provenance; second read returns it (not re-inferred)
- the meta-preference lands under its OWN key and is visible in the store
- the acceptance entry point writes the real row end-to-end
- the declared working mode (the other tenant of the same JSONB) is untouched
  — one store, no clobbering between the declared and inferred surfaces
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text as _text

from services.database.session_factory import AsyncSessionFactory
from services.intent_service import verified_inference as vi
from services.intent_service.collaboration_gate import (
    WORKING_MODE_PREF_KEY,
    WorkingMode,
    get_working_mode,
    set_working_mode,
)
from services.intent_service.workflow_entries import run_verify_inference_workflow


async def _seed_user(prefix: str = "vi1510") -> str:
    """Seed a real users row (the #1472 idiom)."""
    uid = str(uuid4())
    now = datetime.now(timezone.utc)
    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(
            _text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": uid,
                "u": f"{prefix}_{uid[:8]}",
                "e": f"{prefix}_{uid[:8]}@test.example.com",
                "now": now,
            },
        )
        await s.commit()
    return uid


async def _delete_user(uid: str) -> None:
    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(_text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


async def _raw_preferences(uid: str) -> dict:
    """Read the JSONB straight off the row — the store as it actually is,
    not as any wrapper reports it (m-43: name the layer)."""
    async with AsyncSessionFactory.session_scope_fresh() as s:
        row = await s.execute(_text("SELECT preferences FROM users WHERE id = :u"), {"u": uid})
        return row.scalar_one() or {}


@pytest.fixture
async def seeded_user_id():
    uid = await _seed_user()
    yield uid
    await _delete_user(uid)


async def test_store_and_read_verified_inference_round_trip(seeded_user_id):
    """Once verified, it's stored — not re-inferred each time: the write
    lands in the real JSONB and the second turn's read returns it."""
    ok = await vi.store_verified_inference(
        seeded_user_id,
        "standup_format",
        "brief",
        source=vi.SOURCE_USER_VERIFIED,
        confidence=0.6,
    )
    assert ok is True

    record = await vi.get_verified_inference(seeded_user_id, "standup_format")
    assert record is not None
    assert record["value"] == "brief"
    assert record["source"] == vi.SOURCE_USER_VERIFIED
    assert record["confidence_at_verification"] == 0.6

    raw = await _raw_preferences(seeded_user_id)
    assert raw[vi.VERIFIED_INFERENCES_PREF_KEY]["standup_format"]["value"] == "brief"


async def test_meta_preference_lands_under_its_own_key(seeded_user_id):
    """The distinct-signal requirement, verified at the storage layer: the
    meta-preference is visible in the store, under its OWN key, separate
    from task preferences."""
    ok = await vi.set_meta_mode(seeded_user_id, vi.VerificationMetaMode.TRUST_INFERENCES)
    assert ok is True
    assert await vi.get_meta_mode(seeded_user_id) is vi.VerificationMetaMode.TRUST_INFERENCES

    raw = await _raw_preferences(seeded_user_id)
    assert raw[vi.VERIFICATION_META_PREF_KEY]["mode"] == "trust_inferences"
    assert vi.VERIFIED_INFERENCES_PREF_KEY not in raw  # nothing folded together


async def test_acceptance_entry_point_writes_the_real_row(seeded_user_id):
    """The 'yes'-turn entry point against the real store."""
    offer = vi.build_read_back_offer(
        seeded_user_id,
        "default_repo",
        "mediajunkie/piper-morgan-product",
        "that mediajunkie/piper-morgan-product is your default repo",
        confidence=0.55,
    )
    result = await run_verify_inference_workflow(
        session_id="int-1510",
        user_id=seeded_user_id,
        context={"pending_action": offer.offer["pending_action"]},
    )
    assert result["intent_data"]["persisted"] is True
    raw = await _raw_preferences(seeded_user_id)
    stored = raw[vi.VERIFIED_INFERENCES_PREF_KEY]["default_repo"]
    assert stored["value"] == "mediajunkie/piper-morgan-product"
    assert stored["source"] == vi.SOURCE_USER_VERIFIED


async def test_shared_store_tenants_do_not_clobber_each_other(seeded_user_id):
    """One preference persistence (PPM+CXO ruling) means multiple tenants in
    one JSONB: the declared working mode, the verified inferences, and the
    meta mode must coexist without overwriting one another."""
    assert await set_working_mode(seeded_user_id, WorkingMode.EXECUTE) is True
    assert await vi.store_verified_inference(seeded_user_id, "k1", "v1") is True
    assert await vi.set_meta_mode(seeded_user_id, vi.VerificationMetaMode.ALWAYS_ASK) is True

    raw = await _raw_preferences(seeded_user_id)
    assert raw[WORKING_MODE_PREF_KEY] == "execute"
    assert raw[vi.VERIFIED_INFERENCES_PREF_KEY]["k1"]["value"] == "v1"
    assert raw[vi.VERIFICATION_META_PREF_KEY]["mode"] == "always_ask"
    assert await get_working_mode(seeded_user_id) is WorkingMode.EXECUTE
