"""#1320 — the setup wizard's read-only integration-status checks are auth-exempt
(they fire pre-account-creation and were 401'ing → basic-auth dialog loop), while their
WRITE siblings stay auth-required. Guards the exempt asymmetry against regression.
"""

from services.auth.auth_middleware import DEFAULT_EXCLUDE_PATHS


def _excluded(path: str) -> bool:
    # mirrors AuthMiddleware._should_exclude_path (startswith match)
    return any(path.startswith(e) for e in DEFAULT_EXCLUDE_PATHS)


def test_readonly_status_checks_are_exempt():
    assert _excluded("/api/v1/settings/integrations/slack/app-credentials/status")
    assert _excluded("/api/v1/settings/integrations/calendar/app-credentials/status")


def test_write_siblings_remain_auth_required():
    # POST .../app-credentials (the save) must NOT be caught by the status exemption
    assert not _excluded("/api/v1/settings/integrations/slack/app-credentials")
    assert not _excluded("/api/v1/settings/integrations/calendar/app-credentials")
