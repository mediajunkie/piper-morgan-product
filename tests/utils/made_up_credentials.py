"""Made-up, credential-shaped test values, built at run time (issue 2397).

This repo is public and its commit hook, push gate and CI refuse a credential shape in a
tracked file (issue 2392). A test that needs a value shaped like a key therefore builds
it here, from a prefix and a body joined when the test runs, so no file holds a
matching run.

Rules:
- Every value is made up. A body is either plain words that say so, or generated from a
  label by ``body``; nothing here was ever issued by a provider.
- Never paste a real or once-real value, whole or in pieces. Splitting a real value
  across string parts keeps it in the file.
- The same label always gives the same body, so a failing test is repeatable.
"""

from __future__ import annotations

import hashlib
import string

BASE62 = string.digits + string.ascii_letters
# The invite-code alphabet (Crockford base32: no I, L, O or U).
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def joined(*parts: str) -> str:
    """The parts as one string. Use it so a prefix and its body never sit together in a
    source line."""
    return "".join(parts)


def body(label: str, length: int, alphabet: str = BASE62) -> str:
    """``length`` characters of ``alphabet``, derived from ``label`` alone."""
    out: list[str] = []
    counter = 0
    usable = 256 - 256 % len(alphabet)  # reject the tail so every symbol is equally likely
    while len(out) < length:
        for byte in hashlib.sha256(f"{label}:{counter}".encode("utf-8")).digest():
            if byte < usable:
                out.append(alphabet[byte % len(alphabet)])
        counter += 1
    return "".join(out[:length])


def openai_key(label: str, length: int = 48, project: bool = False) -> str:
    """An OpenAI-shaped key: the provider prefix, then ``length`` generated characters."""
    return joined("sk", "-", "proj-" if project else "", body(label, length))


def anthropic_key(label: str, length: int = 95) -> str:
    """An Anthropic-shaped key."""
    return joined("sk", "-ant-", "api03-", body(label, length))


def github_pat(label: str, length: int = 36) -> str:
    """A GitHub personal-token-shaped value."""
    return joined("gh", "p_", body(label, length))


def invite_code(label: str) -> str:
    """A 24-character invite-code-shaped value that the bearer lint counts as a code:
    upper case, a digit and a letter, eight or more distinct characters, not all hex."""
    attempt = 0
    while True:
        code = body(f"{label}:{attempt}", 24, CROCKFORD)
        if (
            any(c.isdigit() for c in code)
            and any(c in "GHJKMNPQRSTVWXYZ" for c in code)
            and len(set(code)) >= 8
        ):
            return code
        attempt += 1


# Two keys that pass the app's real validators: format, strength, and the quick leak
# checks (which answer "unknown", because nothing lists them). Checked by
# tests/unit/utils/test_made_up_credentials.py.
GOOD_OPENAI_KEY = openai_key("a made-up key that passes format, strength and the quick leak checks")
GOOD_ANTHROPIC_KEY = anthropic_key(
    "a made-up key that passes format, strength and the quick leak checks"
)
