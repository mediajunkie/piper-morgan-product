"""Import-smoke for cli/commands/*.py (#1700).

cli/ is now a live operator surface (Lead ruling, decisions.log 2026-09-24): it
joins the delete-module-safely sweep roots and every census denominator, and a
cli command whose backing module is gone must be fixed to the live path or
disposed WITH a record -- never left importing a deleted module.

pytest does NOT collect cli/ (testpaths=tests), so a broken import there was
previously invisible to CI for a month (#1700: cli/commands/notion.py imported
a Batch-1-deleted spatial module). This test is the instrument that closes
that blind spot: every module under cli/commands/*.py is discovered from the
FILESYSTEM (not a hand-kept list, so a new command is covered automatically)
and import_module'd. An ImportError here fails the build loudly.

Layer: this proves the module IMPORTS cleanly (constructor-time dependency
resolution). It does not exercise any command's runtime behavior -- name the
layer (m-43): import-clean is necessary, not sufficient, for "the command
works."
"""

import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
COMMANDS_DIR = REPO_ROOT / "cli" / "commands"


def _discover_command_modules() -> list[str]:
    """Enumerate cli.commands.* from the filesystem -- never a hand-kept list,
    so a newly added command is covered automatically (same discipline as
    scripts/reachability-map.py's filesystem-driven scan)."""
    modules = []
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        modules.append(f"cli.commands.{path.stem}")
    return modules


COMMAND_MODULES = _discover_command_modules()

# The instrument states its own denominator (methodology-44: state the
# denominator on any aggregate) rather than silently collecting zero tests
# if the discovery glob ever comes up empty.
assert COMMAND_MODULES, (
    f"No cli.commands.* modules discovered under {COMMANDS_DIR} -- "
    "the discovery glob is broken, not the codebase empty."
)


@pytest.mark.smoke
@pytest.mark.parametrize("module_name", COMMAND_MODULES)
def test_cli_command_module_imports_cleanly(module_name: str) -> None:
    """Every cli/commands/*.py module must import without raising.

    A command whose backing module is gone (the exact #1700 defect) raises
    ImportError/ModuleNotFoundError here instead of hiding until someone
    runs the command by hand.
    """
    # Ensure a stale prior import (e.g. from another test file that has already
    # loaded a same-named module under a different sys.path insert trick some
    # of these scripts perform) doesn't mask a real failure.
    sys.modules.pop(module_name, None)
    importlib.import_module(module_name)


def test_cli_command_denominator_matches_filesystem() -> None:
    """State the denominator explicitly: the parametrized set above must equal
    the current filesystem listing, so a module added between collection and
    a later re-run is never silently dropped from the count."""
    on_disk = {
        f"cli.commands.{p.stem}" for p in COMMANDS_DIR.glob("*.py") if p.name != "__init__.py"
    }
    assert set(COMMAND_MODULES) == on_disk
