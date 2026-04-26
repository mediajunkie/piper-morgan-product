#!/usr/bin/env python3
"""
Phase E Standalone Server Launcher
==================================

Starts a fresh uvicorn instance of `web.app:app` on port 8002 with
ENABLE_ETHICS_ENFORCEMENT=true, isolated from the long-running PID 98441
(started Apr 16, predates Phases A-D).

This exists so we can run the Phase E gate scenarios against the actual
post-#992 floor/redirect/denial code without disturbing the stale shared
server. After scenarios complete, kill this process.

Usage:
    cd /Users/xian/Development/piper-morgan/piper-morgan-product/.trees/992-ethics-activate
    /Users/xian/Development/piper-morgan/piper-morgan-product/venv/bin/python \\
        dev/2026/04/25/phase-e-transcripts/launch-server-8002.py

Then in a separate shell:
    PHASE_E_SERVER=http://localhost:8002 \\
        bash dev/2026/04/25/phase-e-transcripts/run-scenarios.sh
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the worktree root (5 levels up: phase-e-transcripts/25/04/2026/dev/{root})
# to sys.path so `services.*` and `web.*` resolve when running from any cwd.
_WORKTREE_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(_WORKTREE_ROOT))

# Force the gate flag on regardless of inherited env
os.environ["ENABLE_ETHICS_ENFORCEMENT"] = "true"

from dotenv import load_dotenv

load_dotenv()
# Re-assert after load_dotenv in case .env had it as false
os.environ["ENABLE_ETHICS_ENFORCEMENT"] = "true"


async def main() -> None:
    from services.container import ServiceContainer

    print("[phase-e launcher] Initializing ServiceContainer...", flush=True)
    container = ServiceContainer()
    await container.initialize()
    print(
        f"[phase-e launcher] Services initialized: {len(container.list_services())} services",
        flush=True,
    )
    print(
        f"[phase-e launcher] ENABLE_ETHICS_ENFORCEMENT={os.environ['ENABLE_ETHICS_ENFORCEMENT']}",
        flush=True,
    )

    import uvicorn

    config = uvicorn.Config(
        "web.app:app",
        host="127.0.0.1",
        port=8002,
        reload=False,
        log_level="info",
    )
    server = uvicorn.Server(config)
    print("[phase-e launcher] Starting uvicorn on port 8002...", flush=True)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[phase-e launcher] Shutdown via KeyboardInterrupt", flush=True)
        sys.exit(0)
