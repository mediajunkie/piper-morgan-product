"""One source for Settings sub-path places (Arch 01M8371T0C, 2026-11-22).

Every code-written "Settings → Integrations → X" in ``services/`` must name an X on
``capability_legibility.SETTINGS_SUBPATH_PLACES``. The pinned sentences stay literal;
this guard keeps them from pointing at a place the list doesn't know.
"""

import re
from pathlib import Path

from services.intent_service.capability_legibility import SETTINGS_SUBPATH_PLACES

SERVICES = Path(__file__).resolve().parents[4] / "services"
# The name after the second arrow: capitalised words, up to the first character that
# can't be part of a display name.
SUBPATH = re.compile(r"Settings → Integrations → ((?:[A-Z][A-Za-z]*)(?: [A-Z][A-Za-z]*)*)")


def _found():
    hits = []
    for path in sorted(SERVICES.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for match in SUBPATH.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append((f"{path.relative_to(SERVICES.parent)}:{line}", match.group(1)))
    return hits


def test_the_scan_finds_the_known_literals():
    """The guard is only worth something if it sees the sentences it guards."""
    names = {name for _, name in _found()}
    assert {"GitHub", "Google Calendar"} <= names


def test_every_code_written_sub_path_is_on_the_place_list():
    off_list = [(where, name) for where, name in _found() if name not in SETTINGS_SUBPATH_PLACES]
    assert off_list == []
