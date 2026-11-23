"""One source for Settings sub-path places (Arch 01M8371T0C, 2026-11-22).

Every code-written "Settings → Integrations → X" in ``services/`` must name an X on
``capability_legibility.SETTINGS_SUBPATH_PLACES``. The pinned sentences stay literal;
this guard keeps them from pointing at a place the list doesn't know.
"""

import ast
import re
from pathlib import Path

from services.intent_service.capability_legibility import SETTINGS_SUBPATH_PLACES

ROOT = Path(__file__).resolve().parents[4]
SERVICES = ROOT / "services"
# The name after the second arrow: capitalised words, up to the first character that
# can't be part of a display name.
SUBPATH = re.compile(r"Settings → Integrations → ((?:[A-Z][A-Za-z]*)(?: [A-Z][A-Za-z]*)*)")

# Named exceptions (Arch 01M838A0KA, CXO 01M8389WFK, 2026-11-22), keyed by the constant
# that holds the sentence, never by line number: (file, constant) -> (place, reason).
EXCEPTIONS = {
    ("services/integrations/slack/link_copy.py", "ALREADY_LINKED_DECLINE"): (
        "Slack",
        "said only through Slack; Slack paths are gated by connector_offered('slack'), "
        "so the Slack row exists wherever this is said. CLEARING CONDITION: when Slack "
        "joins any host's offered set, add Slack to SETTINGS_SUBPATH_PLACES and delete "
        "this exception.",
    ),
}


def _module_constants(path: Path):
    """Module-level ``NAME = <expr>`` -> (first line, last line), for locating a hit."""
    spans = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    spans[target.id] = (node.lineno, node.end_lineno or node.lineno)
    return spans


def _found():
    """Every sub-path literal: (relative file, line, place, enclosing constant or None)."""
    hits = []
    for path in sorted(SERVICES.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        matches = list(SUBPATH.finditer(text))
        if not matches:
            continue
        spans = _module_constants(path)
        for match in matches:
            line = text.count("\n", 0, match.start()) + 1
            constant = next((n for n, (a, b) in spans.items() if a <= line <= b), None)
            hits.append((str(path.relative_to(ROOT)), line, match.group(1), constant))
    return hits


def test_the_scan_finds_the_known_literals():
    """The guard is only worth something if it sees the sentences it guards."""
    places = {place for _, _, place, _ in _found()}
    assert {"GitHub", "Google Calendar"} <= places


def test_every_code_written_sub_path_is_on_the_place_list():
    off_list = [
        (f"{file}:{line}", place)
        for file, line, place, constant in _found()
        if place not in SETTINGS_SUBPATH_PLACES
        and EXCEPTIONS.get((file, constant), (None,))[0] != place
    ]
    assert off_list == []


def test_each_exception_still_names_a_live_off_list_sentence():
    """An exception is deleted with its sentence, or when its place joins the list."""
    found = {(file, constant): place for file, _, place, constant in _found()}
    for key, (place, reason) in EXCEPTIONS.items():
        assert found.get(key) == place, f"exception {key} no longer matches a sentence"
        assert place not in SETTINGS_SUBPATH_PLACES, f"{place} is on the list: delete {key}"
        assert "CLEARING CONDITION" in reason
