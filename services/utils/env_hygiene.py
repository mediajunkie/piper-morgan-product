"""#1258 — launch-environment hygiene.

A Claude Code shell exports ``ANTHROPIC_API_KEY=""`` (empty) plus
``ANTHROPIC_BASE_URL`` / ``ANTHROPIC_AUTH_TOKEN`` / ``ANTHROPIC_CUSTOM_HEADERS``
for its own use. ``python-dotenv`` never overrides an already-set var, so an
inherited EMPTY key silently shadows the real key in ``.env`` — every LLM call
then fails with a connection/auth error that masquerades as an outage
(diagnosed 2026-06-04; documented in CLAUDE.md's launch incantation).

``strip_empty_anthropic_vars()`` deletes only vars that are present-but-EMPTY,
so dotenv can fill in the real values. Deliberately narrow: a NON-empty
``ANTHROPIC_BASE_URL``/``AUTH_TOKEN`` may be legitimate configuration (an LLM
gateway on a hosted deployment) — stripping those unconditionally would break
real setups. The residual local-dev nuance (a Claude Code shell's NON-empty
proxy vars) remains covered by CLAUDE.md's ``env -u`` launch procedure.
"""

import os

ANTHROPIC_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_CUSTOM_HEADERS",
)


def strip_empty_anthropic_vars() -> list[str]:
    """Delete present-but-empty Anthropic env vars. Returns what was stripped."""
    stripped = []
    for var in ANTHROPIC_ENV_VARS:
        if var in os.environ and not os.environ[var]:
            del os.environ[var]
            stripped.append(var)
    return stripped


_DEV_DEFAULT_PASSWORD = "dev_changeme_in_production"


def warn_if_prod_uses_dev_password() -> bool:
    """#1324: the Postgres dev default must never silently reach production.

    Returns True (and logs CRITICAL) when PIPER_ENVIRONMENT/ENVIRONMENT says production
    and POSTGRES_PASSWORD is unset-or-the-dev-default. A warning, not a crash —
    the alpha droplet's compose may inject the real password at the container
    layer where this check can't see the final value; a hard exit on a false
    positive would take the service down. The CRITICAL log is unmissable in
    the deploy's startup output (runbook Phase 4 checks it).
    """
    import logging

    # PIPER_ENVIRONMENT is canonical, ENVIRONMENT secondary — the same pair
    # (and read order) as services/auth/jwt_service.py's production guard.
    env = (
        os.environ.get("PIPER_ENVIRONMENT") or os.environ.get("ENVIRONMENT") or ""
    ).lower()
    if env not in ("production", "prod"):
        return False
    password = os.environ.get("POSTGRES_PASSWORD", _DEV_DEFAULT_PASSWORD)
    if password == _DEV_DEFAULT_PASSWORD:
        logging.getLogger(__name__).critical(
            "POSTGRES_PASSWORD is the dev default in a production environment "
            "(#1324) — set a real password before exposing this instance."
        )
        return True
    return False
