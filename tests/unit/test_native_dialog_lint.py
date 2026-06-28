"""F1 #1170 (Part C) — native-dialog lint gate.

Catches native browser `confirm()`/`alert()`/`prompt()` reachable in app code —
the design-floor F1 "Done = no native confirm/alert reachable" grep gate. Native
dialogs are off-brand + unstyleable; callers must use the `Dialog` component.
Mirrors the F3 token-lint (scripts/token_lint.py) baseline-ratchet pattern.
"""

from __future__ import annotations

from scripts.native_dialog_lint import find_native_dialogs


def _has(text):
    return bool(find_native_dialogs(text))


# --- native calls (flag) ----------------------------------------------------


def test_bare_confirm_flagged():
    assert _has("if (!confirm('Delete this?')) return;")


def test_bare_alert_flagged():
    assert _has("alert('Failed: ' + e.message);")


def test_bare_prompt_flagged():
    assert _has("const name = prompt('New name?');")


def test_window_prefixed_native_flagged():
    assert _has("window.confirm('sure?')")
    assert _has("window.alert('hi')")


def test_confirm_after_bang_or_paren_flagged():
    # `if (!confirm(...))` and `(confirm(...))` are the common shapes
    assert _has("  if (!confirm(msg)) { return; }")


# --- Dialog component + non-dialog calls (allow) ----------------------------


def test_dialog_component_methods_allowed():
    assert not _has("Dialog.confirm({ title: 'x', onConfirm: f });")
    assert not _has("Dialog.alert({ title: 'Done' });")
    assert not _has("Dialog.prompt({ title: 'Rename' });")


def test_toast_and_other_calls_allowed():
    assert not _has("ToastMessages.error('upload_error');")
    assert not _has("this.confirmCallback();")  # not confirm( — has chars between
    assert not _has("confirmBtn.addEventListener('click', f);")


def test_comments_allowed():
    assert not _has("// confirm this works later")
    assert not _has("/* alert the user via Toast */")


def test_allow_comment_suppresses():
    assert not _has("alert('legacy');  // native-dialog-allow: third-party embed")


def test_function_definition_not_flagged():
    # defining a function/method named confirm is not a native CALL
    assert not _has("function confirm(opts) { return Dialog.open(opts); }")


# --- snippet content --------------------------------------------------------


def test_violation_reports_the_call():
    v = find_native_dialogs("a();\nalert('boom');\nb();")
    assert len(v) == 1
    assert v[0].line_no == 2
    assert "alert" in v[0].snippet
