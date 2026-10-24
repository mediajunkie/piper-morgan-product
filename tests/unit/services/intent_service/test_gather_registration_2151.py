"""#2151 step 2 (Arch's ruling, point 3): the floor is code. Every gather must be registered.

The #1717 family (test_source_failed_registry_1717.py, test_source_failed_composition_1717.py)
single-sourced the floor's failed-read directive in ``SOURCE_FAILED_FLAGS``. This file closes
the other end: every ``ContextAssembler._gather_*`` method, derived from the class (never a
hand list), must be REGISTERED, meaning its failed read can arm a ``SOURCE_FAILED_FLAGS``
flag. A gather that returns ``{}`` / ``None`` on error is FLOOR-ABSENT (the inventory header):
the floor renders the gap exactly like a verified empty.

How registration is read (source structure, the 1717 registry file's layer):

- A method EMITS a flag when its source writes a registered flag name as a dict-literal key
  (``{"pending_todos_source_failed": True}``) or as a subscript-store target
  (``context["pending_todos_source_failed"] = True``). A ``.get("<flag>")`` read is not an
  emission.
- A gather's reach is the transitive closure of the ``self.<method>`` references in its body
  (lambdas passed to the cache included) over ``ContextAssembler``'s own methods.
- A gather is REGISTERED when its reach emits at least one registered flag AND every other
  ``_gather_*`` it reaches is itself registered. So a composite gather (status/priority,
  temporal) is registered only once each gather it is built from is.

``UNREGISTERED_KNOWN`` lists today's unregistered gathers; its ceiling only falls, and a listed
gather that is now registered fails with "registered: remove it".

LAYER: source structure (``ast``), not rendered output; the rail forcing test
(test_read_claim_forcing_2151.py) measures the floor prompt under forced failures.
DENOMINATOR: every ``_gather_*`` callable on ``ContextAssembler``, asserted > 0.
"""

import ast
import inspect
import textwrap
from typing import Dict, Set

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import SOURCE_FAILED_FLAGS

# Each with why it is unregistered today (the inventory's floor rows).
UNREGISTERED_KNOWN: Dict[str, str] = {
    "_gather_calendar_connection": "a failed connection lookup reads as not connected",
    "_gather_temporal_context": "built from unregistered gathers (calendar, milestones, activity)",
}
UNREGISTERED_KNOWN_CEILING = 2

_FLAGS = {entry.flag for entry in SOURCE_FAILED_FLAGS}


def _gathers() -> list:
    return sorted(
        name
        for name in vars(ContextAssembler)
        if name.startswith("_gather_") and callable(getattr(ContextAssembler, name))
    )


def _tree(name: str) -> ast.AST:
    return ast.parse(textwrap.dedent(inspect.getsource(getattr(ContextAssembler, name))))


def _emits(tree: ast.AST) -> Set[str]:
    out: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            out |= {k.value for k in node.keys if isinstance(k, ast.Constant) and k.value in _FLAGS}
        elif isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Store):
            if isinstance(node.slice, ast.Constant) and node.slice.value in _FLAGS:
                out.add(node.slice.value)
    return out


def _self_refs(tree: ast.AST) -> Set[str]:
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
        and callable(getattr(ContextAssembler, node.attr, None))
    }


def _reach(name: str) -> Set[str]:
    seen: Set[str] = set()
    todo = [name]
    while todo:
        cur = todo.pop()
        if cur in seen:
            continue
        seen.add(cur)
        todo.extend(_self_refs(_tree(cur)) - seen)
    return seen


def registration() -> Dict[str, bool]:
    reach = {g: _reach(g) for g in _gathers()}
    emits = {g: set().union(*(_emits(_tree(m)) for m in r)) for g, r in reach.items()}
    registered: Dict[str, bool] = {}

    def is_registered(g: str, stack: frozenset = frozenset()) -> bool:
        if g in registered:
            return registered[g]
        subs = {m for m in reach[g] if m != g and m.startswith("_gather_") and m not in stack}
        ok = bool(emits[g]) and all(is_registered(s, stack | {g}) for s in subs)
        registered[g] = ok
        return ok

    for g in reach:
        is_registered(g)
    return registered


def test_the_denominator_is_derived_and_nonzero():
    gathers = _gathers()
    assert gathers, "no _gather_* methods found on ContextAssembler; detection broke (#1423)"
    stale = sorted(set(UNREGISTERED_KNOWN) - set(gathers))
    assert not stale, f"UNREGISTERED_KNOWN names no gather: {stale}"


def test_every_gather_is_registered_in_source_failed_flags():
    reg = registration()
    unregistered = sorted(g for g, ok in reg.items() if not ok)
    new = [g for g in unregistered if g not in UNREGISTERED_KNOWN]
    assert not new, (
        f"gather(s) that cannot arm a SOURCE_FAILED_FLAGS flag on a failed read: {new}. Return "
        "the failure sentinel and register its flag in SOURCE_FAILED_FLAGS (FLOOR-ABSENT)."
    )
    fixed = sorted(g for g in UNREGISTERED_KNOWN if reg.get(g))
    assert not fixed, f"registered: remove {fixed} from UNREGISTERED_KNOWN and lower the ceiling"


def test_unregistered_ceiling_only_falls():
    assert len(UNREGISTERED_KNOWN) <= UNREGISTERED_KNOWN_CEILING


def test_the_reader_sees_a_registered_gather():
    # The detector itself must find the one gather the floor already registers; a reader
    # that finds none would pass every gather off as "known" forever.
    assert registration().get("_gather_reminder_context") is True
