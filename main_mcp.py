#!/usr/bin/env python3
"""Piper Morgan MCP server — entrypoint (Phase C unit 0, #1462).

Separate process/entrypoint from main.py's alpha web app, on the SAME image
(see Dockerfile) — fly.mcp.toml overrides the container CMD to run this file
instead. Alpha's process, DB, and bindings are untouched; a bad MCP deploy
cannot take alpha down. Deployable dark: unit 0 ships no resources and fails
closed on all MCP traffic — see services/mcp/server/app.py for the real logic.
Keep this file thin.
"""

import os

import structlog
import uvicorn

# Side effect: configures structlog (JSON, correlation-ready) the same way
# every other Piper entrypoint does — reused, not reimplemented here.
import services.infrastructure.logging.config  # noqa: F401
from services.infrastructure.logging.url_redaction import (
    RedactionAtStartup,
    install_handler_redaction_filter,
    install_root_redaction_filter,
    install_url_redaction_filter,
)
from services.mcp.server.app import build_asgi_app, refuse_master_key

logger = structlog.get_logger(__name__)

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("PIPER_MCP_HOST", "0.0.0.0")


def main() -> None:
    refuse_master_key()  # #1982: the one place the guard lives (see its docstring)
    app = build_asgi_app()
    logger.info("mcp_server_starting", host=HOST, port=PORT, service="piper-morgan-mcp")
    # #2362: the same URL redaction the main app installs, on this process too. The
    # HTTP client loggers and the root first; then, once uvicorn.Config() has built the
    # uvicorn and uvicorn.access handlers (which do not propagate to the root), every
    # handler that exists.
    install_url_redaction_filter()
    install_root_redaction_filter()
    # RedactionAtStartup runs the install once more when startup has finished, for any
    # handler created during it.
    config = uvicorn.Config(RedactionAtStartup(app), host=HOST, port=PORT, log_level="info")
    install_handler_redaction_filter()
    uvicorn.Server(config).run()


if __name__ == "__main__":
    main()
