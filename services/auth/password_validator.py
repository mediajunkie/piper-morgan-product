"""
Password Validation Service

One length rule, for every path that sets a person's chosen password.

Issue 2438 (xian's ruling 2026-11-26, relayed by Exec 01M8CDTHCC and 01M8CEG65R;
Arch's conditions 01M8CE2GFC): length only, no composition rules. At least
``MIN_LENGTH`` characters, counted as typed, and at most ``MAX_PASSWORD_BYTES`` bytes
of UTF-8. The rules run only when a password is set; sign-in is unchanged.

Issue #298: AUTH-PASSWORD-CHANGE (the first validator).
"""

from typing import Optional, Tuple

# Issue 2432: one code per rule. ``PasswordValidator.failed_rule`` returns one of these.
RULE_EMPTY = "empty"
RULE_TOO_SHORT = "too_short"
RULE_TOO_LONG = "too_long"
RULE_MISMATCH = "mismatch"

# The validator's own messages, kept for ``validate``'s callers and logs. Never a
# reply's words.
_VALIDATOR_MESSAGES = {
    RULE_EMPTY: "Password cannot be empty",
    RULE_TOO_SHORT: "Password must be at least {min_length} characters",
    RULE_TOO_LONG: "Password must be at most {max_bytes} bytes",
    RULE_MISMATCH: "Passwords do not match",
}


class PasswordValidator:
    """
    Validates a new password against the length rule.

    Requirements:
    - At least ``MIN_LENGTH`` characters (code points), counted as typed, no strip.
    - At most ``MAX_PASSWORD_BYTES`` bytes of UTF-8.

    Why an upper bound (Arch, 01M8CE2GFC): bcrypt 4.3.0 silently ignores everything
    past byte 72, so a longer passphrase would verify on its first 72 bytes alone,
    and bcrypt 5 raises instead. Refusing at set time is the fix. Never pre-hash:
    that would change the hash format under every existing account.

    Design: static methods, no state.
    """

    # NIST SP 800-63B rev 4, 3.1.1.2: 15 for a password that is the only factor.
    MIN_LENGTH = 15
    MAX_PASSWORD_BYTES = 72

    @classmethod
    def failed_rule(cls, password: str) -> Optional[str]:
        """The code of the first rule ``password`` fails, or None when it passes them all.

        Issue 2432 (Arch's note, mail 01M87HVCTY): the routes pick the sentence a person
        reads from this code through ``password_rule_line``; the validator's own messages
        (``validate``) never reach a reply."""
        if not password:
            return RULE_EMPTY
        if len(password) < cls.MIN_LENGTH:
            return RULE_TOO_SHORT
        if len(password.encode("utf-8")) > cls.MAX_PASSWORD_BYTES:
            return RULE_TOO_LONG
        return None

    @classmethod
    def validate(cls, password: str) -> Tuple[bool, Optional[str]]:
        """(is_valid, message). The message is for logs and callers that are not a
        reply; a route answers with ``password_rule_line(failed_rule(...))``."""
        rule = cls.failed_rule(password)
        if rule is None:
            return True, None
        return False, _VALIDATOR_MESSAGES[rule].format(
            min_length=cls.MIN_LENGTH, max_bytes=cls.MAX_PASSWORD_BYTES
        )

    @classmethod
    def validate_match(cls, password1: str, password2: str) -> Tuple[bool, Optional[str]]:
        """(True, None) when the two passwords are equal, else (False, message)."""
        if password1 == password2:
            return True, None
        return False, _VALIDATOR_MESSAGES[RULE_MISMATCH]

    @classmethod
    def validate_strength(cls, password: str) -> Tuple[bool, Optional[str]]:
        """Same as ``validate``; kept for its callers."""
        return cls.validate(password)


# --- What a person reads ---
# Issue 2438 (CXO's lines, mail 01M8CEMET5; Arch's conditions 3 and 4, 01M8CE2GFC): the
# rule is stated here and nowhere else. ``PASSWORD_RULE_HELPER_LINE`` sits under a
# new-password field before the person types. Each refusal states the one rule that
# failed, so it is true for its code: a person who typed 80 characters is never told
# they need at least 15. The cap is in bytes, and the lines say what a byte is, because
# "72 characters" is false for accented letters and emoji. All three are built once from
# ``MIN_LENGTH`` and ``MAX_PASSWORD_BYTES``; the pins in
# tests/unit/web/test_password_rules_one_place_2438.py fail until a changed rule is
# read again.
# CXO's correction (mail 01M8CFERKQ, after Arch's byte check 01M8CFC37R): only an
# unaccented Latin letter or a digit is one byte; Greek and Cyrillic take two, most
# other scripts three, emoji four.
_BYTES_AS_READ = "English letter or digit is one byte, any other letter or an emoji is two to four."
PASSWORD_RULE_HELPER_LINE = (
    "At least {min_length} characters, and no more than {max_bytes} bytes: an " + _BYTES_AS_READ
).format(
    min_length=int(PasswordValidator.MIN_LENGTH),
    max_bytes=int(PasswordValidator.MAX_PASSWORD_BYTES),
)
PASSWORD_TOO_SHORT_LINE = "Your password needs at least {min_length} characters.".format(
    min_length=int(PasswordValidator.MIN_LENGTH)
)
PASSWORD_TOO_LONG_LINE = (
    "Your password is too long: the most is {max_bytes} bytes. An " + _BYTES_AS_READ
).format(max_bytes=int(PasswordValidator.MAX_PASSWORD_BYTES))
PASSWORD_EMPTY_LINE = "Your password can't be empty."
PASSWORDS_DONT_MATCH_LINE = "The passwords don't match."
# For a rule code with no line of its own (CXO's fallback, her log 2026-11-24 11:51 and
# Arch's note 01M87HVCTY: "That password can't be used. Choose a different one.").
PASSWORD_CANT_BE_USED_LINE = "That password can't be used. Choose a different one."


def password_rule_line(code: Optional[str]) -> Optional[str]:
    """The sentence for a failed rule, or None for a code with no line (the route then
    answers ``PASSWORD_CANT_BE_USED_LINE``). A picker on the guard's closed list
    (``DETAIL_PICKERS``): every return is an UPPER_CASE constant or None."""
    if code == RULE_EMPTY:
        return PASSWORD_EMPTY_LINE
    if code == RULE_TOO_SHORT:
        return PASSWORD_TOO_SHORT_LINE
    if code == RULE_TOO_LONG:
        return PASSWORD_TOO_LONG_LINE
    if code == RULE_MISMATCH:
        return PASSWORDS_DONT_MATCH_LINE
    return None


def password_refusal_line(code: Optional[str]) -> str:
    """For a terminal script: the line for ``code``, or the fallback. Never None."""
    return password_rule_line(code) or PASSWORD_CANT_BE_USED_LINE
