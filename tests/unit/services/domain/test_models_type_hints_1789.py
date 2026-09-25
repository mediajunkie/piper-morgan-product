"""
Regression test for #1789: `class List` in services/domain/models.py shadowed
`typing.List`, breaking `typing.get_type_hints()` for 24 of 55 domain
dataclasses (any annotation written as `List[...]` resolved to the dataclass,
not typing.List, since the module uses `from __future__ import annotations`).

Fixed by converting every `List[...]` annotation in models.py to the builtin
`list[...]` and dropping `List` from the module's `typing` import -- no
rename of the `List` domain dataclass, zero blast radius on consumers.

This test discovers every dataclass in services.domain.models (not a hand
list) and asserts get_type_hints() succeeds for all of them, so the
collision cannot silently return.
"""

import dataclasses
import typing

import services.domain.models as domain_models


def _domain_dataclasses():
    """Every dataclass defined in services.domain.models, discovered via

    dataclasses.is_dataclass() over vars(module) -- not a hand-maintained
    list, so newly added dataclasses are automatically covered.
    """
    return [
        obj
        for obj in vars(domain_models).values()
        if isinstance(obj, type) and dataclasses.is_dataclass(obj)
    ]


class TestDomainModelsTypeHintsResolve:
    """get_type_hints() must succeed for every domain dataclass (#1789)."""

    def test_discovers_the_expected_number_of_dataclasses(self):
        """Sanity check on discovery itself: the issue's own count was 55."""
        found = _domain_dataclasses()
        assert len(found) == 55, (
            f"Expected 55 domain dataclasses (per #1789's baseline count), found "
            f"{len(found)}. If this is an intentional addition/removal, update "
            f"this count -- it exists so a silent count drift is visible."
        )

    def test_get_type_hints_succeeds_for_every_domain_dataclass(self):
        """The actual regression guard: no dataclass in the module may fail

        typing.get_type_hints() resolution. A failure here means the List/
        typing.List collision (or an equivalent shadowing bug) has returned.
        """
        found = _domain_dataclasses()
        assert found, "No dataclasses discovered in services.domain.models -- discovery broke"

        failures = []
        for cls in found:
            try:
                typing.get_type_hints(cls)
            except Exception as e:  # noqa: BLE001 - collecting all failures, not just first
                failures.append((cls.__name__, type(e).__name__, str(e)))

        assert not failures, (
            f"get_type_hints() failed for {len(failures)} of {len(found)} domain "
            f"dataclasses:\n"
            + "\n".join(f"  {name}: {err_type}: {msg}" for name, err_type, msg in failures)
        )

    def test_the_list_domain_dataclass_itself_resolves(self):
        """Specifically confirm the dataclass literally named `List` (the

        source of the shadowing) resolves its own annotations correctly,
        e.g. `tags: list[str]` resolves to `list[str]`, not something
        referencing the dataclass itself.
        """
        hints = typing.get_type_hints(domain_models.List)
        assert hints["tags"] == list[str]
