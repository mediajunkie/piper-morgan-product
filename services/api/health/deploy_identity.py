"""Deploy identity (#1839) — what is actually running, answerable without SSH.

Extracted from ``services/api/health/staging_health.py`` (#1499 Class 2,
2026-09-23, Arch Rule-0 ruling) when that module's FastAPI router was deleted
as unmounted dead code. This helper is NOT dead: it is imported live by
``web/api/routes/admin.py`` at two call sites — the served ``/health``
(``:109``) and ``/api/v1/version`` (``:145``) — so it had to move out before
the shell around it could be removed. See the disposal record:
``docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md``.

DESIGN RULE, and it is the whole point: **never fabricate a plausible value.**
Each of these returns the literal string "unknown" when it cannot determine the
answer. That is deliberate and is the lesson of what it replaced — the fields
these succeed were hardcoded to "staging"/"PM-038-staging", so they were always
populated, always confident, and carried no information. A reader saw a filled-in
`version` and concluded the surface worked.

"unknown" is a measurement. A default that looks like an answer is not.
"""

import os
from pathlib import Path

_UNKNOWN = "unknown"


def _deployed_version() -> str:
    """The running build's version, read from the VERSION file shipped in the image.

    Falls back to PIPER_VERSION, then "unknown". Never guesses.
    """
    env = os.getenv("PIPER_VERSION", "").strip()
    if env:
        return env
    # VERSION sits at the repo/image root; this file is services/api/health/.
    candidate = Path(__file__).resolve().parents[3] / "VERSION"
    try:
        text = candidate.read_text(encoding="utf-8").strip()
        return text or _UNKNOWN
    except OSError:
        return _UNKNOWN


def deploy_identity() -> dict:
    """#1839: the three deploy-identity facts, as one reusable payload.

    Added 2026-09-21 when the v0.8.13.0 deploy verification found the first
    #1839 landing had put these fields ONLY on staging_health.py's router —
    which was mounted by no app (the live `/health` is web/api/routes/admin.py).
    The described surface wasn't the running one (m-49, caught by curling the
    droplet rather than reading the code). This helper is consumed by BOTH the
    live route and `/api/v1/version`, so the two can't drift again.

    Moved to this dedicated module 2026-09-23 (#1499 Class 2) when
    staging_health.py's dead router was deleted around it.
    """
    return {
        "environment": _deployed_environment(),
        "version": _deployed_version(),
        "git_sha": _deployed_git_sha(),
    }


def _deployed_git_sha() -> str:
    """The commit this image was built from.

    Populated by a build arg (see Dockerfile PIPER_GIT_SHA). Returns "unknown"
    when the build did not supply one — which is the honest answer for any image
    built before that wiring existed, and must NOT be replaced by reading the
    local .git of whatever host happens to be running: that would report the
    *host's* checkout, not the *image's* provenance, which is precisely the
    build-vs-release confusion this field exists to end.
    """
    return os.getenv("PIPER_GIT_SHA", "").strip() or _UNKNOWN


def _deployed_environment() -> str:
    """Which environment this process believes it is — REPORTED, never interpreted.

    🔴 ``PIPER_ENVIRONMENT`` IS NOT A FREE-TEXT LABEL. It is an existing, canonical
    variable with **security-gate consumers**, and its established vocabulary is
    ``development`` / ``production`` (see ``Environment`` in
    ``services/config/llm_config_service.py``, which warns and falls back to
    ``development`` on any value it doesn't recognise):

      - ``services/security/encrypted_types.py:57`` — ``== "production"`` makes an
        unset ``ENCRYPTION_MASTER_KEY`` **fatal on the write path** (#1387). Any
        other value silently restores warn-and-write-plaintext.
      - ``services/auth/jwt_service.py:177`` — fails loudly in production (#1087).
      - ``services/utils/env_hygiene.py:44`` — production hygiene CRITICAL.

    ⚠️ So setting this to a near-miss like ``prod`` does not merely mislabel the
    health output — **it silently disarms the gates above**, because they compare
    against the exact string ``"production"``. An earlier draft of this docstring
    said ``local | staging | prod``; that would have re-opened exactly the
    plaintext-PII hole #1387 was written to close. Fixed before it shipped anywhere.

    This function therefore **reports the raw value and interprets nothing** — it
    is a mirror, not a source of truth. If the deployment vocabulary is ever
    changed (plan v0.1 §2 proposes ``local``/``staging``/``prod`` as *environment
    names*), that is a **migration with security-gate consumers**, not a rename,
    and it must be done at those call sites first.
    """
    return os.getenv("PIPER_ENVIRONMENT", "").strip() or _UNKNOWN
