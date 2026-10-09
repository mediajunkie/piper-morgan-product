#!/usr/bin/env python3
"""burn_invite_tokens.py — DELETE exposed-but-unused alpha invite tokens, by mask.

Split out of mint_invite_tokens.py (Arch, 2026-10-09, ADR-080 D3 applied to
grants): under CIO's option 3 the deployed payload IS the permission grant, so
one payload carries one effect class. The mint CREATES rows; this one DELETES
them. No seat holds a rule for this payload unless PM names it.

The predicate is ``left(token,4)||right(token,4)`` so the operator names a token
the way memos are allowed to (masked), never in full. ``used_at IS NULL`` is in
the WHERE — a consumed token is a tester's account and is never touched. Output
is masked forms only. DRY-RUN unless --apply.

Usage (as deployed):
  python /app/scripts/burn_invite_tokens.py ZVHW8B35[,QGQPKJGP...]           # dry-run
  python /app/scripts/burn_invite_tokens.py ZVHW8B35[,QGQPKJGP...] --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# No shell to set PYTHONPATH: file-relative root (/app in the image).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

MAX_MASKS = 20
_MASK = re.compile(r"[0-9A-Z]{8}")  # first4+last4 of a Crockford Base32 token


def parse_masks(masks_csv: str) -> list[str]:
    """1..MAX_MASKS comma-separated masks, each exactly 8 of [0-9A-Z]; refused
    before any DB connection otherwise."""
    masks = [m.strip().upper() for m in masks_csv.split(",") if m.strip()]
    if not masks or len(masks) > MAX_MASKS or any(not _MASK.fullmatch(m) for m in masks):
        raise SystemExit(
            f"refusing: want 1..{MAX_MASKS} comma-separated 8-char masks [0-9A-Z] (first4+last4)"
        )
    return masks


def burn(masks: list[str], *, apply: bool) -> None:
    from prod_db import _database_url, _redacted
    from sqlalchemy import create_engine, text

    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== #1885 burn {mode}: {len(masks)} mask(s) ===")
    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    where = "used_at IS NULL AND (left(token,4)||right(token,4)) = ANY(:masks)"
    masked = "left(token,4)||chr(8230)||right(token,4)"
    eng = create_engine(url)
    with eng.begin() as c:
        rows = c.execute(
            text(f"SELECT {masked} AS m FROM invite_tokens WHERE {where}"), {"masks": masks}
        ).all()
        print(f"--- matched unused rows: {[r[0] for r in rows]}")
        if apply:
            gone = c.execute(
                text(f"DELETE FROM invite_tokens WHERE {where} RETURNING {masked}"),
                {"masks": masks},
            ).all()
            print(f"--- burned: {[r[0] for r in gone]}")
    if not apply:
        print("DRY-RUN complete — no writes. Re-run with --apply to burn the rows listed above.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="#1885 burn unused invite tokens by mask")
    ap.add_argument("masks", help="comma-separated first4+last4 masks")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args(argv)
    burn(parse_masks(args.masks), apply=args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
