#!/usr/bin/env python3
"""
#1003 Diagnostic Server Launcher — flag=false variant
=====================================================

Sibling of `dev/2026/04/25/phase-e-transcripts/launch-server-8002.py`.
Difference: forces ENABLE_ETHICS_ENFORCEMENT=false so we can re-run the
S1 r2 input and compare the response to the flag=true r2 transcript.

Per #1003 acceptance criterion #1:
> Diagnostic comparison run: S1 r2 input with ENABLE_ETHICS_ENFORCEMENT=false;
> verify whether the response differs from the flag-on response in any
> observable way (intent classification, audit envelope, response content)

Usage:
    cd /Users/xian/Development/piper-morgan/piper-morgan-product/.trees/992-ethics-activate
    /Users/xian/Development/piper-morgan/piper-morgan-product/venv/bin/python \\
        dev/2026/04/26/phase-e-transcripts/run-1003-diagnostic/launch-server-8002-flag-off.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Worktree root: 6 levels up from this file
# (run-1003-diagnostic/phase-e-transcripts/26/04/2026/dev/{worktree-root})
_WORKTREE_ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(_WORKTREE_ROOT))

# Force the gate flag OFF regardless of inherited env
os.environ["ENABLE_ETHICS_ENFORCEMENT"] = "false"

from dotenv import load_dotenv

load_dotenv()
# Re-assert after load_dotenv in case .env had it as true
os.environ["ENABLE_ETHICS_ENFORCEMENT"] = "false"


async def main() -> None:
    from services.container import ServiceContainer

    print("[#1003 launcher] Initializing ServiceContainer...", flush=True)
    container = ServiceContainer()
    await container.initialize()
    print(
        f"[#1003 launcher] Services initialized: {len(container.list_services())} services",
        flush=True,
    )
    print(
        f"[#1003 launcher] ENABLE_ETHICS_ENFORCEMENT={os.environ['ENABLE_ETHICS_ENFORCEMENT']}",
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
    print("[#1003 launcher] Starting uvicorn on port 8002...", flush=True)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[#1003 launcher] Shutdown via KeyboardInterrupt", flush=True)
        sys.exit(0)
