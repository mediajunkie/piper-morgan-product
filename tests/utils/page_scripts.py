"""What the app shell loads before any page's own script, for tests that run a page's
script under node.

``templates/layouts/app_shell.html`` loads ``/static/js/escape.js`` shell-wide (#1582), so
a page script may call ``escapeHtml`` without defining it. A test that cuts a page's
script out and runs it alone has to load the same file first, as the browser does.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_SOURCE = (ROOT / "web" / "static" / "js" / "escape.js").read_text(encoding="utf-8")
_EXPORTS = "if (typeof window !== 'undefined') {"
assert _EXPORTS in _SOURCE, "escape.js changed shape; update tests/utils/page_scripts.py"
# The two function definitions only. The file's last lines copy them onto ``window``,
# which a harness declares itself (with ``const``, so touching it earlier is an error).
SHARED_ESCAPE_JS = _SOURCE[: _SOURCE.index(_EXPORTS)] + "\n"
