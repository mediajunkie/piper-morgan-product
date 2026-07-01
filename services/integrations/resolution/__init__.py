"""Connector-agnostic target-resolution seam (#1342, Arch-ruled 2026-07-01).

A separate resolution service (NOT a Connector-protocol method) that generalizes the
GitHub ``resolve_repo`` decision tree so the connector framework can share it. See
``target.py`` for the ``ResolvedTarget`` envelope + the promoted ``ResolutionSource``.
"""

from services.integrations.resolution.target import ResolutionSource, ResolvedTarget

__all__ = ["ResolutionSource", "ResolvedTarget"]
