"""#1581 [SECURITY] — stored XSS in templates/files.html client-side rendering.

Same class as #1578 (todos.html), same sweep, same pattern. renderFiles()
interpolated ``${file.owner_id}``, ``${file.content_type}``, ``${kind}`` and the
onclick id/kind arguments unescaped into ``container.innerHTML``; worse, the
page's ``escapeHtml()`` was the DOM-based (`div.textContent` -> `innerHTML`)
variant which does NOT escape quotes, so every ``value="..."``/``aria-label``
attribute site it "protected" was quote-breakable (attribute injection — e.g. a
filename planting a real ``onerror`` handler attribute). And renameArtifact
passed ``'${file.filename}'`` through the onclick JS-string context, which HTML
escaping cannot protect at all.

LAYER (named honestly): these tests verify the JS SOURCE escapes, not the
runtime DOM. The escaping happens client-side inside a JS template literal, so
a Jinja render proves only what the shipped script says — assertions here are
string/regex pins on the rendered page source. The runtime-DOM half lives in
the jsdom harness: tests/frontend/unit/files-page-xss.test.js renders hostile
files through the real extracted script and asserts no element/attribute
injection.

Two contexts, two rules pinned here (verbatim from #1578):
- HTML text/attribute contexts -> escapeHtml()/escapeAttr() on every
  interpolation (the sweep tests ratchet this: any future bare ``${...}`` in
  the render path fails).
- JS-string-inside-onclick context -> HTML-escaping CANNOT protect it (the
  HTML parser decodes entities before the JS engine parses the handler), so
  user-authored text must never appear there at all. The Rename button used to
  pass ``'${file.filename}'`` into onclick — the filename now travels via the
  window._allFiles state lookup and only server-generated ids cross that
  boundary (the #1578 shareTodo fix is the model).

Helpers are duplicated inline per-template (todos.html did the same) —
consolidation into a shared static asset is a flagged follow-on, not this fix.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parents[3]
TEMPLATES = REPO / "templates"

_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture(scope="module")
def rendered():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("files.html").render(trust_stage=1, user=_USER)


def _fn_body(rendered, signature):
    """Extract a top-level inline-script function body (this page's inline
    script is indented four spaces, unlike todos.html's two)."""
    m = re.search(rf"{re.escape(signature)}\(.*?\n    \}}\n", rendered, re.DOTALL)
    assert m, f"{signature}() not found in rendered page"
    return m.group(0)


# --- the helpers --------------------------------------------------------------


def test_escape_html_helper_covers_all_five_metacharacters(rendered):
    """The page's old DOM-based escapeHtml (div.textContent -> innerHTML) does
    NOT escape quotes, so it cannot protect attribute contexts. #1581 replaces
    it with the #1578 string-based single source of truth."""
    body = _fn_body(rendered, "function escapeHtml")
    for ch, entity in [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&#39;"),
    ]:
        assert entity in body, f"escapeHtml() does not escape {ch!r} -> {entity}"


def test_escape_attr_helper_exists(rendered):
    """escapeAttr() — the attribute-context variant (delegates to escapeHtml;
    the name documents the call-site context, per #1578)."""
    assert "function escapeAttr" in rendered, "escapeAttr() (attribute-context variant) is missing"


# --- the headline hole: filename through the onclick JS-string context ---------


def test_rename_button_no_longer_passes_filename_through_onclick_js_string(rendered):
    """HTML-escaping cannot protect a JS string inside onclick (entities are
    decoded before the JS parses), so the filename must not cross that boundary
    at all — only the server-generated id does."""
    assert not re.search(r"renameArtifact\('\$\{[^}]*\}',\s*'\$\{[^}]*\}'\)", rendered), (
        "Rename button still passes a second (filename) argument through the "
        "onclick JS-string context — unprotectable by HTML escaping"
    )
    assert (
        "renameArtifact('${escapeAttr(file.file_id)}')" in rendered
    ), "Rename button should pass only the escaped id"
    # and renameArtifact() resolves the filename from state instead
    body = _fn_body(rendered, "function renameArtifact")
    assert "window._allFiles" in body, (
        "renameArtifact() must resolve the filename from window._allFiles "
        "state, not from an onclick-interpolated argument"
    )


# --- the sweep: every interpolation in the render path -------------------------

# Composed sub-template variables whose leaves are escaped where they are built.
_ALLOWED_COMPOSED = {
    "actionButtons",
    "sourceBadge",
    "ownerIndicator",
}

_INNERMOST_INTERP = re.compile(r"\$\{([^{}]*)\}")


def _assert_all_escaped(body, fn_name, allowed=()):
    allowed = set(allowed)
    for expr in _INNERMOST_INTERP.findall(body):
        expr = expr.strip()
        ok = expr.startswith("escapeHtml(") or expr.startswith("escapeAttr(") or expr in allowed
        assert ok, (
            f"unescaped interpolation in {fn_name}(): ${{{expr}}} — every "
            "dynamic value in the render path goes through escapeHtml()/"
            "escapeAttr() (or is a composed, already-escaped fragment)"
        )


def test_every_interpolation_in_renderFiles_is_escaped_or_composed(rendered):
    """Ratchet: a future bare ``${...}`` added to renderFiles fails here.
    (Innermost interpolations only — outer conditional wrappers contain braces
    and are covered via their nested literals.)"""
    _assert_all_escaped(
        _fn_body(rendered, "function renderFiles"),
        "renderFiles",
        allowed=_ALLOWED_COMPOSED,
    )


def test_every_interpolation_in_applyFileFilter_is_escaped(rendered):
    """The no-match empty state is static today; the ratchet keeps it that way
    if anyone ever interpolates the search query into it."""
    _assert_all_escaped(
        _fn_body(rendered, "function applyFileFilter"),
        "applyFileFilter",
    )


def test_every_interpolation_in_showPreviewModal_is_escaped_or_composed(rendered):
    """The preview modal shell: title is escaped; innerHtml is a composed
    fragment whose leaves previewFile() escapes (pinned below)."""
    _assert_all_escaped(
        _fn_body(rendered, "function showPreviewModal"),
        "showPreviewModal",
        allowed={"innerHtml"},
    )


# --- named field sites (the sweep proves coverage; these name the fields) ------


@pytest.mark.parametrize(
    "site",
    [
        # onclick id/kind arguments — server-generated, but the HTML-attribute
        # layer still gets escaped (per #1578's completeTodo/editTodo handling)
        "editTags('${escapeAttr(file.file_id)}', '${escapeAttr(kind)}')",
        "previewFile('${escapeAttr(file.file_id)}', '${escapeAttr(kind)}')",
        "downloadFile('${escapeAttr(file.file_id)}', '${escapeAttr(kind)}')",
        "deleteFile('${escapeAttr(file.file_id)}', '${escapeAttr(kind)}')",
        # owner indicator (another account's id — hostile-capable on shared rows)
        "Uploaded by: ${escapeHtml(file.owner_id)}",
        # bulk-select checkbox: data attrs + the quote-breakable aria-label
        'data-id="${escapeAttr(file.file_id)}"',
        'data-kind="${escapeAttr(kind)}"',
        'aria-label="Select ${escapeAttr(file.filename)} for bulk download"',
        # card title (text context)
        "${escapeHtml(file.filename)}",
        # metadata line: size/date go through formatters whose fallback can be
        # the raw value (same reasoning as #1578's formatDueDate), and
        # content_type is attacker-supplied at upload (Content-Type header)
        "${escapeHtml(formatFileSize(file.size))}",
        "${escapeHtml(formatDate(file.uploaded_at))}",
        "${escapeHtml(file.content_type)}",
        # tag chips (user-authored freeform strings)
        '<span class="tag-chip">${escapeHtml(t)}</span>',
        # preview modal: message + content + title all escaped
        "${escapeHtml(data.message || ",
        "<pre class=\"file-preview-content\">${escapeHtml(data.content || '')}</pre>",
        '<h3 class="file-preview-title">${escapeHtml(title)}</h3>',
        # dialog form inputs (Dialog.show sets content via innerHTML —
        # dialog.js:84 — so value="" attributes need full attribute escaping;
        # the old quotes-only .replace() and quote-less escapeHtml both fail)
        'id="tagsInput" value="${escapeAttr(current)}"',
        'id="rename-title-input" value="${escapeAttr(current)}"',
    ],
)
def test_field_site_is_escaped(rendered, site):
    assert site in rendered, f"expected escaped interpolation site missing: {site}"


def test_old_quotes_only_tags_escape_is_gone(rendered):
    """editTags used ``current.replace(/"/g, '&quot;')`` — quotes-only escaping
    in a value="" attribute. Superseded by escapeAttr()."""
    assert "current.replace(/\"/g, '&quot;')" not in rendered


# --- sink-classified sites (verified-safe-by-sink, evidence pinned) ------------


def test_toast_body_sink_is_textcontent():
    """uploadOneFile/downloadSelected interpolate ``${file.name}`` and
    ``${error.detail}`` into ToastMessages bodies — safe BY SINK, not by
    escaping: Toast renders title/body via textContent. Pin the sink so this
    classification breaks loudly if toast.js ever switches to innerHTML."""
    toast = (REPO / "web" / "static" / "js" / "toast.js").read_text()
    assert "titleEl.textContent = title" in toast
    assert "messageEl.textContent = message" in toast


def test_dialog_title_sink_is_textcontent():
    """editTags/renameArtifact/openUploadDialog pass static titles today, but
    the classification 'Dialog titles are a textContent sink' (dialog.js:78,
    same evidence #1578 relied on for the Share modal) is load-bearing — pin it."""
    dialog = (REPO / "web" / "static" / "js" / "dialog.js").read_text()
    assert "title.textContent = config.title" in dialog


# --- canary: same-page features untouched --------------------------------------


def test_existing_page_features_untouched(rendered):
    """The fix must not disturb the page's features: tags (#313), preview
    (#313), rename (#1184), provenance badge (#1270), search filter (G64).
    (Their own suites pin details; this is a canary.)"""
    assert "function applyFileFilter" in rendered
    assert "function renameArtifact" in rendered
    assert "source-badge" in rendered
    assert "tag-chip" in rendered
    assert "function initDragDropUpload" in rendered
