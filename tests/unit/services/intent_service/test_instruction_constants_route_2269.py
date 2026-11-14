"""#2269 3a: a phrasing Piper's code tells a person to type is a corpus row.

Beta session 11-04: Piper told a tester to type "link repo", then did not recognise
it. Arch's rule (11-04): any phrasing code tells a person to type is a corpus row that
routes to its handler, with a pin per instruction constant; an instruction that does
not route is a false capability claim. The fix is a corpus row, never a regex.

The rows went in on 11-06 (corpus 622 to 624). This is the pin per constant: the
instruction's own words, filled with the row's values, must BE a corpus row with the
expected operation. Change the constant's wording and this fails until the corpus has
the new phrasing (which the next router screen then scores).

LAYER: the constants against the corpus file. It does not run a router; whether the
row routes as expected is the corpus run's measurement.
DENOMINATOR: the two repo instruction constants (link, unlink) by exact phrase, and
the three project how-to lines (archive, add, restore) by the instruction's shape.
"""

import re
from pathlib import Path

import pytest
import yaml

from services.intent_service import adopted_category_reads_only as lines

ROOT = Path(__file__).resolve().parents[4]
CORPUS = ROOT / "tests/fixtures/inversion_corpus_phase0.yaml"
REPO = "octocat/hello-world"
PROJECT = "Mobile Redesign"


def _rows():
    return {row["phrase"]: row for row in yaml.safe_load(CORPUS.read_text())["corpus"]}


def _instruction(template: str) -> str:
    """The words inside the single quotes: what the person is told to type."""
    quoted = re.findall(r"'([^']+)'", template)
    assert len(quoted) == 1, f"expected one quoted instruction in {template!r}"
    return quoted[0].format(repo=REPO).replace("<project name>", PROJECT)


@pytest.mark.parametrize(
    "template,expected",
    [
        (lines.ADOPTED_REPO_LINK_LINE, "action:link_repo"),
        (lines.ADOPTED_REPO_UNLINK_LINE, "action:unlink_repo"),
    ],
    ids=["link", "unlink"],
)
def test_the_repo_instruction_is_a_corpus_row_for_its_operation(template, expected):
    phrase = _instruction(template)
    rows = _rows()
    assert phrase in rows, (
        f"Piper tells people to type {phrase!r}, and the corpus has no such row. Add the "
        "row (never a pattern) so the next screen scores it."
    )
    assert rows[phrase]["expected"] == expected


def test_the_instructions_read_as_written():
    assert _instruction(lines.ADOPTED_REPO_LINK_LINE) == (
        "link repo octocat/hello-world to Mobile Redesign"
    )
    assert _instruction(lines.ADOPTED_REPO_UNLINK_LINE) == (
        "unlink repo octocat/hello-world from Mobile Redesign"
    )


@pytest.mark.parametrize(
    "verb,expected",
    [
        ("archive", "action:archive_project"),
        ("add", "action:add_project"),
        ("restore", "action:restore_project"),
    ],
)
def test_each_project_how_to_instruction_has_a_corpus_row_of_its_shape(verb, expected):
    """The project how-to lines say "say '<verb> project {name}'". Each has a corpus
    row of exactly that shape (archive's was added 2026-11-14 on Arch's yes)."""
    template = lines.ADOPTED_WRITE_HOW_TO_LINES[verb]
    assert f"'{verb} project {{name}}'" in template
    matching = [
        row
        for phrase, row in _rows().items()
        if phrase.lower().startswith(f"{verb} project ") and row["expected"] == expected
    ]
    assert matching, f"no corpus row of the shape '{verb} project <name>' expecting {expected}"
