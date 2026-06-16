"""#1252 P6 / ADR-071 D5 — principal-threading lint gate tests.

The D5 anti-pattern is *principal degradation*: pulling the user principal
out of a loose context dict with a silent ``... if ctx else None`` fallback
(``user_id = context.get("user_id") if context else None``) instead of
threading it as a required parameter from the host boundary. When the key is
absent the principal silently becomes ``None`` — which downstream reads then
treat as "unscoped", the exact failure ADR-071 exists to stop.

This guard (AST-based, ratchet pattern — mirrors scripts/token_lint.py +
scripts/native_dialog_lint.py) snapshots the current sites and fails CI on
NEW ones, ratcheting to zero as D4 threading replaces each site.
"""

from __future__ import annotations

from collections import Counter

from scripts.principal_threading_lint import find_principal_degradations, new_against_baseline


class TestDetector:
    def test_flags_assignment_degradation(self):
        src = "def f(context):\n    user_id = context.get('user_id') if context else None\n"
        vs = find_principal_degradations(src)
        assert len(vs) == 1
        assert "user_id" in vs[0].snippet

    def test_flags_kwarg_degradation_with_attribute_chain(self):
        src = (
            "def f(intent):\n"
            "    return g(user_id=intent.context.get('user_id') if intent.context else None)\n"
        )
        vs = find_principal_degradations(src)
        assert len(vs) == 1

    def test_flags_double_quoted_key(self):
        src = 'def f(ctx):\n    u = ctx.get("user_id") if ctx else None\n'
        assert len(find_principal_degradations(src)) == 1

    def test_does_not_flag_plain_get_without_else_none(self):
        # A bare read with no silent-None degradation is not the anti-pattern.
        src = "def f(ctx):\n    user_id = ctx.get('user_id')\n"
        assert find_principal_degradations(src) == []

    def test_does_not_flag_context_construction(self):
        # Building a context to PASS the principal down is legitimate.
        src = "def f(slack_ctx):\n    return h(context={'user_id': slack_ctx.get('user_id')})\n"
        assert find_principal_degradations(src) == []

    def test_does_not_flag_different_key(self):
        src = "def f(ctx):\n    x = ctx.get('session_id') if ctx else None\n"
        assert find_principal_degradations(src) == []

    def test_does_not_flag_else_non_none(self):
        # Degradation is specifically the silent-None fallback.
        src = "def f(ctx):\n    u = ctx.get('user_id') if ctx else 'anon'\n"
        assert find_principal_degradations(src) == []

    def test_syntax_error_file_yields_no_violations(self):
        # Robust to unparseable files (don't crash the whole lint run).
        assert find_principal_degradations("def (:\n  oops") == []


class TestRatchet:
    def test_new_against_baseline_is_multiset_difference(self):
        current = Counter({"a|x": 2, "b|y": 1})
        baseline = Counter({"a|x": 1})
        new = new_against_baseline(current, baseline)
        assert new == Counter({"a|x": 1, "b|y": 1})

    def test_no_new_when_within_baseline(self):
        current = Counter({"a|x": 1})
        baseline = Counter({"a|x": 1, "b|y": 1})
        assert new_against_baseline(current, baseline) == Counter()
