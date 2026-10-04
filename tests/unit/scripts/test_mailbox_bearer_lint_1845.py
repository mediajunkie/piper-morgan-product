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
TOKEN = "9EA0V9VPHS9CFRTKH873EGJ6"


@pytest.mark.parametrize(
    "label, line, expected_hits",
    [
        ("as minted, uppercase", TOKEN, 1),
        ("uppercase, display-grouped", "9EA0-V9VP-HS9C-FRTK-H873-EGJ6", 1),
        ("lowercased paste (HOST's gap)", TOKEN.lower(), 1),
        ("lowercase AND grouped — prose shape, rejected", "9ea0-v9vp-hs9c-frtk-h873-egj6", 0),
        ("mixed case — a base62 id, not a token", "9eA0V9VpHs9cFrTkH873EgJ6", 0),
        ("24 lowercase hex — a sha prefix", "a10301be5d9e0690e1234567", 0),
        ("24 uppercase hex", "A10301BE5D9E0690E1234567", 0),
        ("letters only, no digit", "ABCDEFGHJKMNPQRSTVWXYZAB", 0),
        ("hyphenated prose with a digit", "phase0-assessment-great-revised-x", 0),
        (
            "uppercase prose with digits, space-grouped (registry note, 09-26)",
            "CADENCE CHANGED 2026-09-26 05:3x PDT",
            0,
        ),
        ("uppercase token space-grouped is NOT a display form", "9EA0 V9VP HS9C FRTK H873 EGJ6", 0),
        ("obviously-fake placeholder, two symbols", "XXXX0000XXXX0000XXXX0000", 0),
        ("obviously-fake placeholder, dash-grouped", "AAAA-1111-AAAA-1111-AAAA-1111", 0),
        (
            "low-entropy but not a placeholder shape — still rejected (<8 distinct)",
            "ABABABAB1212121234343434",
            0,
        ),
        ("masked form, uppercase", "9EA0…EGJ6", 0),
        ("masked form, lowercase", "9ea0…egj6", 0),
        ("masked form, three dots", "9EA0...EGJ6", 0),
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
    assert mask(TOKEN) == "9EA0…EGJ6"
    assert mask(TOKEN.lower()) == "9ea0…egj6"
    assert mask("9EA0-V9VP-HS9C-FRTK-H873-EGJ6") == "9EA0…EGJ6"
    assert mask("short") == "…"


def test_lowercase_hit_is_the_same_credential_as_uppercase():
    # The reason the class went case-insensitive: one credential, two spellings.
    upper = scan_line(TOKEN)[0]
    lower = scan_line(TOKEN.lower())[0]
    assert upper.lower() == lower
