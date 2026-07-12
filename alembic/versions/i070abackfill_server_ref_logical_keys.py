"""ADR-070 Amendment A (A5) — backfill managed mcp_server_ref literals → logical keys.

Data-only (no DDL — the #1312 autogen-empty invariant is untouched). Maps the
KNOWN managed-deployment literals to the logical key ``github``; anything else
(a genuine BYOC literal) is deliberately left verbatim per A3 — that URL is
the user's own server.

The known-managed set is explicit and closed (deterministic, reviewable):
- http://github-mcp:8082/mcp                       (droplet docker-compose)
- http://piper-morgan-gh-mcp.internal:8082/mcp     (Fly private network)
- http://localhost:9100/mcp                        (the pre-A1 code default)

Revision ID: i070abackfill
Revises: h1312recon
Create Date: 2026-07-12
"""

from alembic import op

revision = "i070abackfill"
down_revision = "h1312recon"
branch_labels = None
depends_on = None

_MANAGED_LITERALS = (
    "http://github-mcp:8082/mcp",
    "http://piper-morgan-gh-mcp.internal:8082/mcp",
    "http://localhost:9100/mcp",
)


def upgrade() -> None:
    literals = ", ".join(f"'{u}'" for u in _MANAGED_LITERALS)
    op.execute(
        "UPDATE connector_bindings SET mcp_server_ref = 'github' "
        f"WHERE connector = 'github' AND mcp_server_ref IN ({literals})"
    )


def downgrade() -> None:
    # The literal each environment used is a deployment fact the DB no longer
    # carries; restoring 'github' rows to the CURRENT deployment's URL keeps
    # the pre-A1 read path working on downgrade.
    op.execute(
        "UPDATE connector_bindings SET mcp_server_ref = 'http://github-mcp:8082/mcp' "
        "WHERE connector = 'github' AND mcp_server_ref = 'github'"
    )
