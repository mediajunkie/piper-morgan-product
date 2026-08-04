"""#1482 delete-copy honesty pins (CXO spec 2026-08-03, applied 2026-08-04).

Soft deletes must not claim permanence; the one hard delete says so honestly
(fact-corrected: we destroy OUR copy; no provider-side revocation exists —
verified against delete_user_key, which touches keychain+DB only).
"""
import pytest

SOFT_SURFACES = (
    "templates/home.html",
    "templates/insights.html",
    "templates/components/insight_controls.html",
    "templates/components/insight_card.html",
)


@pytest.mark.smoke
def test_no_soft_delete_claims_permanence():
    for path in SOFT_SURFACES:
        src = open(path).read()
        assert "cannot be undone" not in src, (
            f"{path} still claims permanence on a SOFT delete (#1482)"
        )
        assert "This cannot be undone" not in src


@pytest.mark.smoke
def test_soft_deletes_carry_the_honest_keeper_line():
    for path in SOFT_SURFACES:
        src = open(path).read()
        assert "for a while" in src, (
            f"{path} lost the honest retention line — the set ships together (#1482)"
        )


@pytest.mark.smoke
def test_hard_delete_key_copy_is_honest_and_does_not_overclaim():
    src = open("templates/settings_llm_keys.html").read()
    assert "really is gone" in src, "the one TRUE permanence claim went missing"
    assert "destroy our copy" in src
    # The overclaim that must never ship: Piper cannot revoke at the provider
    # (delete_user_key = keychain + DB only; verified 2026-08-04).
    assert "revoke it at the provider" not in src
    assert "until you revoke it there" in src, "the residual-validity fact went missing"
