#!/usr/bin/env python3
"""#2342 (ADR-081 D3): move existing GitHub connections off the classic OAuth App.

Run by xian, in the container, in the same sitting as setting the GitHub App's secrets
(Arch 2026-11-12 06:51): until it runs, the classic tokens stay live at GitHub.

For every stored GitHub grant that the published App did not mint, it tries to revoke it
at GitHub with the classic app's credentials, marks the account's GitHub connection
stale with the reason ``cutover`` (the person then sees CXO's "GitHub now connects
through the Piper GitHub app" line and reconnects), and deletes the stored token. It
does not touch a personal access token, a saved repository choice, or a connection
already made through the App. It prints counts only.

Dry run by default:

    python scripts/github_app_cutover.py            # counts what it would do
    python scripts/github_app_cutover.py --apply    # does it

``--apply`` is refused unless GITHUB_APP_CLIENT_ID and GITHUB_APP_CLIENT_SECRET are both
set. Run it twice: the second run should find no classic grant. A failed revoke is
counted and does not stop the run; put the count on issue 2342.

Exit codes: 0 done; 2 refused (nothing changed); 1 an error.

Concept: docs/internal/architecture/adrs/adr-081-github-identity-one-app-whose-token-serves-a-request.md
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="make the changes (default: dry run)")
    args = parser.parse_args(argv)

    from services.connectors.github_app_cutover import (
        CutoverRefused,
        format_counts,
        run_cutover,
    )

    try:
        counts = asyncio.run(run_cutover(apply=args.apply))
    except CutoverRefused as e:
        print(f"github app cutover: REFUSED. {e}")
        return 2
    except Exception as e:  # counts only: never a traceback that could carry a value
        print(f"github app cutover: ERROR ({type(e).__name__}). Nothing further was done.")
        return 1
    print(format_counts(counts, applied=args.apply))
    return 0


if __name__ == "__main__":
    sys.exit(main())
