"""#1845 — the bearer-credential lint's matcher, pinned.

HOST's second review (2026-09-24) tested these shapes by hand and found the
one gap (a lowercased invite token slipped through, the class was
uppercase-only). This makes those probes permanent, plus the two rejections
that keep the case-insensitive class from becoming noise: a MIXED-case
24-char run is a base62 id, not a token; a lowercase all-hex run is a
truncated sha; a lowercase run must be contiguous (hyphenated prose with a
digit matched 357 times on the first case-insensitive pass).

Layer: the matching functions in isolation, not the tracked-file walk.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "mailbox_bearer_lint",
    Path(__file__).resolve().parents[3] / "scripts" / "mailbox_bearer_lint.py",
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["mailbox_bearer_lint"] = _MOD
_SPEC.loader.exec_module(_MOD)
scan_line = _MOD.scan_line
mask = _MOD.mask

# A synthetic 24-char Crockford token (never minted; letters + digits, not hex).
TOKEN = "ZVHWT5408X2NFA6P0D838B35"


@pytest.mark.parametrize(
    "label, line, expected_hits",
    [
        ("as minted, uppercase", TOKEN, 1),
        ("uppercase, display-grouped", "ZVHW-T540-8X2N-FA6P-0D83-8B35", 1),
        ("lowercased paste (HOST's gap)", TOKEN.lower(), 1),
        ("lowercase AND grouped — prose shape, rejected", "zvhw-t540-8x2n-fa6p-0d83-8b35", 0),
        ("mixed case — a base62 id, not a token", "ZvHwT5408x2NfA6p0D838b35", 0),
        ("24 lowercase hex — a sha prefix", "a10301be5d9e0690e1234567", 0),
        ("24 uppercase hex", "A10301BE5D9E0690E1234567", 0),
        ("letters only, no digit", "ABCDEFGHJKMNPQRSTVWXYZAB", 0),
        ("hyphenated prose with a digit", "phase0-assessment-great-revised-x", 0),
        ("masked form, uppercase", "ZVHW…8B35", 0),
        ("masked form, lowercase", "zvhw…8b35", 0),
        ("masked form, three dots", "ZVHW...8B35", 0),
        ("anthropic key", "sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123", 1),
        ("openai-style key", "sk-abcdefghijklmnopqrstuvwxyz0123", 1),
        ("google key", "AIzaSyA1234567890abcdefghijklmnopqrstuvw", 1),
        ("slack bot token", "xoxb-1234567890-abcdefghij", 1),
        ("github pat", "ghp_abcdefghijklmnopqrstuvwxyz0123", 1),
        ("github fine-grained pat", "github_pat_abcdefghijklmnopqrstuvwxyz", 1),
        ("fly token", "fo1_abcdefghijklmnopqrstuvwxyz", 1),
    ],
)
def test_scan_line(label, line, expected_hits):
    assert len(scan_line(f"context {line} context")) == expected_hits, label


def test_mask_prints_first_and_last_four_only():
    assert mask(TOKEN) == "ZVHW…8B35"
    assert mask(TOKEN.lower()) == "zvhw…8b35"
    assert mask("ZVHW-T540-8X2N-FA6P-0D83-8B35") == "ZVHW…8B35"
    assert mask("short") == "…"


def test_lowercase_hit_is_the_same_credential_as_uppercase():
    # The reason the class went case-insensitive: one credential, two spellings.
    upper = scan_line(TOKEN)[0]
    lower = scan_line(TOKEN.lower())[0]
    assert upper.lower() == lower
