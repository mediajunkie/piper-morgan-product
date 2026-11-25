"""
Password Validation Service

Validates password strength requirements for new passwords.
Used by password change endpoint (#298) and user creation flows.

Security Features:
- Enforces OWASP password complexity requirements
- Clear, specific error messages (not generic "invalid password")
- No information leakage about password requirements
- Helps prevent weak password selection

Issue #298: AUTH-PASSWORD-CHANGE
"""

import re
from typing import Optional, Tuple

# Issue 2432: one code per rule. ``PasswordValidator.failed_rule`` returns one of these.
RULE_EMPTY = "empty"
RULE_TOO_SHORT = "too_short"
RULE_NO_UPPERCASE = "no_uppercase"
RULE_NO_LOWERCASE = "no_lowercase"
RULE_NO_DIGIT = "no_digit"
RULE_NO_SPECIAL = "no_special"
RULE_MISMATCH = "mismatch"
# Issue 2438: the five strength rules, the ones ``PASSWORD_RULE_LINE`` states.
STRENGTH_RULES = (
    RULE_TOO_SHORT,
    RULE_NO_UPPERCASE,
    RULE_NO_LOWERCASE,
    RULE_NO_DIGIT,
    RULE_NO_SPECIAL,
)

# The validator's own messages, word for word as before issue 2432, kept for
# ``validate``'s callers and logs. Never a reply's words.
_VALIDATOR_MESSAGES = {
    RULE_EMPTY: "Password cannot be empty",
    RULE_TOO_SHORT: "Password must be at least {min_length} characters",
    RULE_NO_UPPERCASE: "Password must contain at least one uppercase letter",
    RULE_NO_LOWERCASE: "Password must contain at least one lowercase letter",
    RULE_NO_DIGIT: "Password must contain at least one digit",
    RULE_NO_SPECIAL: "Password must contain at least one special character ({special})",
    RULE_MISMATCH: "Passwords do not match",
}


class PasswordValidator:
    """
    Validates password strength against security requirements.

    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter (A-Z)
    - At least 1 lowercase letter (a-z)
    - At least 1 digit (0-9)
    - At least 1 special character (!@#$%^&*)

    Design:
    - Static methods, no state
    - Returns tuple: (is_valid, error_message)
    - Error messages specific for each requirement
    - Can be unit tested independently
    """

    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*()"

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
        if not re.search(r"[A-Z]", password):
            return RULE_NO_UPPERCASE
        if not re.search(r"[a-z]", password):
            return RULE_NO_LOWERCASE
        if not re.search(r"\d", password):
            return RULE_NO_DIGIT
        if not re.search(f"[{re.escape(cls.SPECIAL_CHARS)}]", password):
            return RULE_NO_SPECIAL
        return None

    @classmethod
    def validate(cls, password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength.

        Args:
            password: Password string to validate

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid=True: Password meets all requirements, error_message=None
            - is_valid=False: Password invalid, error_message describes requirement

        The shape is unchanged by issue 2432. The message is for logs and callers that
        are not a reply; a route answers with ``password_rule_line(failed_rule(...))``.

        Example:
            >>> PasswordValidator.validate("weak")
            (False, "Password must be at least 8 characters")

            >>> PasswordValidator.validate("WeakPass1")
            (False, "Password must contain at least one special character (!@#$%^&*())")

            >>> PasswordValidator.validate("Strong@Pass1")
            (True, None)
        """
        rule = cls.failed_rule(password)
        if rule is None:
            return True, None
        return False, _VALIDATOR_MESSAGES[rule].format(
            min_length=cls.MIN_LENGTH, special=cls.SPECIAL_CHARS
        )

    @classmethod
    def validate_match(cls, password1: str, password2: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that two passwords match.

        Args:
            password1: First password
            password2: Second password (confirmation)

        Returns:
            Tuple of (is_valid, error_message)

        Example:
            >>> PasswordValidator.validate_match("Pass123!", "Pass123!")
            (True, None)

            >>> PasswordValidator.validate_match("Pass123!", "Different!")
            (False, "Passwords do not match")
        """
        if password1 == password2:
            return True, None
        else:
            return False, _VALIDATOR_MESSAGES[RULE_MISMATCH]

    @classmethod
    def validate_strength(cls, password: str) -> Tuple[bool, Optional[str]]:
        """
        Comprehensive validation including strength and matching.

        Combines both validate() and internal strength checks.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)

        Note:
            This is the main method to use for password validation.
            Other methods (validate, validate_match) are available for specific checks.
        """
        return cls.validate(password)


# --- What a person reads ---
# Issue 2438 (CXO, mail 01M8A7MG8Q; Arch, mails 01M8A7N4F1 and 01M8A7PQQ6): the whole rule
# is stated twice and only here. ``PASSWORD_RULE_HELPER_LINE`` sits under a new-password
# field before the person types; ``PASSWORD_RULE_LINE`` is the one refusal for every
# strength rule. It states the rule, not which part failed, so it is true for each of the
# five codes and nobody is refused once per unstated rule. Both are built once from
# ``MIN_LENGTH`` and ``SPECIAL_CHARS``, so the sentences and the rule cannot drift; the
# pins in tests/unit/web/test_password_rules_one_place_2438.py fail until a changed rule
# is read again.
_SPECIALS_AS_READ = " ".join(PasswordValidator.SPECIAL_CHARS)
PASSWORD_RULE_HELPER_LINE = (
    "At least {min_length} characters, with an uppercase letter, a lowercase letter, "
    "a number and one of {specials}."
).format(min_length=int(PasswordValidator.MIN_LENGTH), specials=_SPECIALS_AS_READ)
PASSWORD_RULE_LINE = (
    "Your password needs at least {min_length} characters, an uppercase letter, "
    "a lowercase letter, a number and one of {specials}."
).format(min_length=int(PasswordValidator.MIN_LENGTH), specials=_SPECIALS_AS_READ)
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
    # Issue 2438: the five strength codes share the one line that states the whole rule.
    if code in STRENGTH_RULES:
        return PASSWORD_RULE_LINE
    if code == RULE_MISMATCH:
        return PASSWORDS_DONT_MATCH_LINE
    return None
