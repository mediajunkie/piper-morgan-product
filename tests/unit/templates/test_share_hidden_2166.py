"""#2166 (PPM 10-24 18:36): Share is hidden on todos, lists and projects until its repair.

Todo sharing has no column, no route lists shares, and the typed email resolves to
nothing, so the dialog can't succeed and its "Not shared with anyone yet" is a false
absence. One flag, ``SHARING_ENABLED = false`` in permissions.js, gates every Share
button and the chat share intent.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def test_the_flag_is_off():
    src = (ROOT / "web/static/js/permissions.js").read_text()
    assert re.search(r"^const SHARING_ENABLED = false;$", src, re.M)


@pytest.mark.parametrize(
    "page,var", [("todos", "todo"), ("lists", "list"), ("projects", "project")]
)
def test_every_share_button_is_behind_the_flag(page, var):
    src = (ROOT / f"templates/{page}.html").read_text()
    assert f"if (SHARING_ENABLED && canShare({var})) {{" in src
    # no other render path for the button
    assert src.count('class="share-btn"') == 1


def test_the_chat_share_intent_checks_the_flag_first():
    src = (ROOT / "web/static/js/permission-intents.js").read_text()
    flag_at = src.index("if (!SHARING_ENABLED)")
    assert flag_at < src.index("openShareModal(resourceType")
