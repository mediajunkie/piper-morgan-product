#!/usr/bin/env python3
"""invite_redemption_read.py — READ-ONLY: which alpha invite codes have been redeemed.

HOST's redemption read (xian, 2026-11-04): has anyone signed up with a given
code? The operator names codes the way memos may (masked: first4+last4, eight
characters), never in full. Output is counts and masked forms only: for each
mask, ``unused`` or ``USED`` with the date, then totals. It prints no user id,
email or name, and it writes nothing: one SELECT, no --apply flag exists.

Usage (as deployed, run by xian with ``fly machine exec``):
  python /app/scripts/invite_redemption_read.py 4JAJ8WBG,D7TFY3M9,...

Sibling of burn_invite_tokens.py (same mask rule, same prod_db URL resolution).
Trust zone (#1344): this table knows tokens, never identities; the code-to-person
map stays in HOST's private roster.
"""

from __future__ import annotations

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


def read(masks: list[str]) -> None:
    from prod_db import _database_url, _redacted
    from sqlalchemy import create_engine, text

    print(f"=== redemption read (read-only): {len(masks)} mask(s) ===")
    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    sql = text(
        "SELECT left(token,4)||right(token,4) AS m, used_at FROM invite_tokens "
        "WHERE (left(token,4)||right(token,4)) = ANY(:masks)"
    )
    with create_engine(url).connect() as c:
        rows = {m: used_at for m, used_at in c.execute(sql, {"masks": masks}).all()}
    used = 0
    for m in masks:
        label = f"{m[:4]}…{m[4:]}"
        if m not in rows:
            print(f"{label}  NO ROW")
        elif rows[m] is None:
            print(f"{label}  unused")
        else:
            used += 1
            print(f"{label}  USED {rows[m]:%Y-%m-%d}")
    missing = sum(1 for m in masks if m not in rows)
    print(f"--- {len(masks)} asked: {used} used, {len(rows) - used} unused, {missing} no row")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: invite_redemption_read.py MASK[,MASK...]")
    read(parse_masks(sys.argv[1]))
