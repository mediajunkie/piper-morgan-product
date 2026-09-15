"""#1807/#1812 — the generic error table's keyless + out-of-quota entries.

LAYER: the real UserFriendlyErrorService resolving a REAL exception instance
raised by services.llm.request_key, not a hand-written string. That matters:
CXO supplied copy and explicitly left the regex to us, so the thing worth
pinning is that the pattern matches what the code ACTUALLY raises.
"""

from services.llm.request_key import UserLLMKeyRequiredError
from services.ui_messages.user_friendly_errors import make_error_user_friendly


def test_real_keyless_exception_resolves_to_the_keyless_entry():
    exc = UserLLMKeyRequiredError(
        "Authenticated caller has no LLM key of their own and is not the "
        "designated operator — refusing to spend the server's key (#1807)."
    )
    r = make_error_user_friendly(exc)
    assert "LLM key of your own" in r["message"]
    assert "doesn't bill anyone else's account" in r["message"]
    assert r["category"] == "llm_key"


def test_keyless_entry_never_says_sign_in_or_try_again():
    # They ARE signed in (#1320's copy would be wrong), and retrying without a
    # key changes nothing — both pinned at the entry points, inherited here.
    exc = UserLLMKeyRequiredError("Authenticated caller has no LLM key of their own")
    r = make_error_user_friendly(exc)
    blob = (r["message"] + " " + r["recovery"]).lower()
    assert "sign in" not in blob
    assert "try again" not in blob


def test_keyless_entry_does_not_claim_nothing_was_charged():
    # CXO's §5b: a generic handler cannot cash that claim — only the entry
    # points know the refusal preceded any provider call.
    exc = UserLLMKeyRequiredError("Authenticated caller has no LLM key of their own")
    r = make_error_user_friendly(exc)
    assert "nothing was charged" not in (r["message"] + r["recovery"]).lower()


def test_out_of_quota_recovery_no_longer_routes_the_user_into_the_keyless_state():
    # THE TRAP (#1807 fallout, caught by CXO): the old recovery advised
    # "remove the current key to fall back to the built-in model" — a fallback
    # #1807 deleted. Following it deleted your key and landed you worse off.
    r = make_error_user_friendly(Exception("insufficient_quota: exceeded your current quota"))
    assert "fall back to the built-in model" not in r["recovery"]
    assert "remove the current key" not in r["recovery"]
    assert "Settings" in r["recovery"]
