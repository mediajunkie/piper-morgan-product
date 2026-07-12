"""ADR-070 Amendment A — the ONE server-ref resolution authority.

The incident this kills (2026-07-12 Fly migration): ``connector_bindings.
mcp_server_ref`` stored literal URLs, so a host move silently invalidated
every binding — PM's GitHub binding said BOUND-and-healthy while resolving
against a docker-compose hostname that didn't exist on the new host, and the
failure surfaced as a server outage, not a config problem.

The amendment's shape (Arch-ruled 2026-07-10):

- **A1** — managed-connector bindings store a LOGICAL KEY (``github``), and
  the URL resolves from deployment config at connect-time. Topology is a
  deployment property; a host move is a config change, not a row migration.
- **A2** — every read-site routes through THIS function. If resolution logic
  spreads across adapters, we've rebuilt the same drift one level up (the
  #1283 one-resolver lesson).
- **A3** — BYOC is preserved by shape-discrimination, centralized HERE:
  a scheme-prefixed value (``http://…``/``https://…``) is a literal override
  (the user's OWN server, whose lifecycle they own — re-bind is the honest
  recovery if it goes stale); a bare token is a logical key.
- **A4** — an unknown key degrades honestly and NAMES the missing config;
  it must never read as "server down."
- **A5** — existing literal rows backfill to keys (migration i070aresolve);
  forward-compatible with a per-user server registry (the key becomes the
  registry lookup key when that lands).
"""

import os
from typing import Optional

# Logical key → the env var that holds this deployment's URL for it.
# Adding a connector = one line here + the env var in each deployment's
# config (fly.toml [env] / droplet .env) — never a new resolution path.
_KEY_TO_ENV = {
    "github": "GITHUB_MCP_SERVER_URL",
    "calendar": "CALENDAR_MCP_SERVER_URL",
    "notion": "NOTION_MCP_SERVER_URL",
    "slack": "SLACK_MCP_SERVER_URL",
}


class ServerRefResolutionError(LookupError):
    """A4: raised for an unresolvable ref — carries the config name so the
    degrade can point at the ACTUAL problem (missing deployment config),
    never masquerading as a server outage."""

    def __init__(self, ref: str, env_var: Optional[str]):
        self.ref = ref
        self.env_var = env_var
        if env_var:
            msg = (
                f"server ref '{ref}' resolves via {env_var}, which is unset "
                f"in this deployment — set it in the environment config"
            )
        else:
            msg = (
                f"server ref '{ref}' is not a known connector key "
                f"({', '.join(sorted(_KEY_TO_ENV))}) and not a literal URL"
            )
        super().__init__(msg)


def resolve_server_ref(ref: Optional[str], *, connector: Optional[str] = None) -> str:
    """Resolve a binding's ``mcp_server_ref`` to a connectable URL (A2 authority).

    Shape discrimination (A3): scheme-prefixed = BYOC/literal override, returned
    verbatim; bare token = logical key, resolved from deployment config (A1).
    Empty/None falls back to the ``connector`` argument's key when given (so
    legacy NULL-ref rows keep working through the same authority).

    Raises ServerRefResolutionError (A4) — callers translate it into their
    honest-degrade surface with the message intact.
    """
    value = (ref or "").strip()
    if value.startswith(("http://", "https://")):
        return value  # A3: literal/BYOC override — the user's own server
    key = value or (connector or "")
    if not key:
        raise ServerRefResolutionError(ref="", env_var=None)
    env_var = _KEY_TO_ENV.get(key)
    if env_var is None:
        raise ServerRefResolutionError(ref=key, env_var=None)
    url = os.getenv(env_var)
    if not url:
        raise ServerRefResolutionError(ref=key, env_var=env_var)
    return url
