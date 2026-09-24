"""Runtime-shape tests for cli/commands/*.py (#1873).

#1700's import-smoke test (test_cli_commands_import_1700.py) proves every
cli/commands/*.py module IMPORTS cleanly -- constructor-time dependency
resolution only. It explicitly does not exercise any command's runtime
behavior (m-43: name the layer). #1873 is exactly the runtime class that
leaves uncovered: cli/commands/notion.py imported fine (post-#1700) but 4 of
its 5 subcommands raised AttributeError on `self.adapter`, which nothing
ever assigned.

This file adds two instruments, run BEFORE any fix in the same investigation
so the findings are real (not narrated):

1. **Entry-shape construction** -- for each of the 8 cli/commands/*.py
   modules, exercise its actual argparse/click entry point far enough to
   prove the parser/group constructs (a `--help` invocation reaches
   `parser.exit()`/click's help path *after* every subparser, subcommand,
   and argument has been registered, but *before* any command object is
   constructed or any service call is made -- verified by reading each
   module's `main()`: `parser.parse_args()` always precedes
   `SomeCommand()` construction). keys.py has no argparse/click entry point
   at all (it exposes bare async functions invoked directly from
   `main.py`); its "entry shape" is checked via signature binding instead
   (see #2), and that substitution is stated explicitly rather than silently
   skipped.

2. **Unassigned self.attr detection** -- an AST walk over every top-level
   class in each module: collect every `self.X` LOAD (a read) anywhere in
   the class body, and every `self.X` STORE (an assignment) anywhere in the
   class body (not just `__init__` -- some commands legitimately assign in
   a later setup call, e.g. publish.py's `self.publisher = Publisher()`
   inside `cmd_publish`; collecting stores class-wide avoids flagging that
   legitimate pattern as a false positive while still catching an attribute
   that is NEVER assigned anywhere, which is the actual #1873 defect shape).
   The set difference (loads - stores) is the unassigned-attribute finding.
   Denominator: every top-level class with an `__init__` across all 8
   modules (modules with no such class -- documents.py, keys.py --
   contribute 0 handler classes and are counted, not silently omitted).

3. **Signature-bind check** -- for the two commands #1873 named as having
   signature drift (keys.py's calls into UserAPIKeyService; notion.py's
   calls into NotionDomainService), an AST walk over the call sites feeding
   each named receiver object, matched against `inspect.signature(...)` of
   the live method. A call whose positional/keyword shape does not bind
   against the live signature is the exact "test_key kwarg doesn't exist"
   class of defect, caught mechanically instead of by inspection.

Layer: (1) proves argparse/click parser construction only -- not that any
subcommand's body runs correctly end-to-end (no network/DB seam is
exercised). (2) proves attribute-assignment shape via static AST analysis --
not that the assigned value is the RIGHT object, only that something is
assigned before it's read. (3) proves call-site arity/keyword-name binding
against the live method signature -- not that the semantics are correct
(e.g. it cannot know that `validate_user_key`'s STORED-key semantics differ
from "test this candidate key"). All three are necessary, not sufficient,
for "the command works" -- see m-43.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import sys
from pathlib import Path
from typing import Callable

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
COMMANDS_DIR = REPO_ROOT / "cli" / "commands"


def _discover_command_modules() -> list[str]:
    modules = []
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        modules.append(f"cli.commands.{path.stem}")
    return modules


COMMAND_MODULES = _discover_command_modules()

assert COMMAND_MODULES, (
    f"No cli.commands.* modules discovered under {COMMANDS_DIR} -- "
    "the discovery glob is broken, not the codebase empty."
)


# ---------------------------------------------------------------------------
# 1. Entry-shape construction
# ---------------------------------------------------------------------------


def _run_argparse_help(module_name: str, is_async: bool, argv_prog: str) -> None:
    """Exercise a module's argparse `main()` with --help and confirm it
    reaches parser.exit(0) -- i.e. every subparser/argument registered
    without raising, and NOT past the point where a command object would be
    constructed (confirmed by reading each module: parse_args() always
    precedes construction)."""
    sys.modules.pop(module_name, None)
    module = importlib.import_module(module_name)

    old_argv = sys.argv
    sys.argv = [argv_prog, "--help"]
    try:
        with pytest.raises(SystemExit) as exc_info:
            if is_async:
                import asyncio

                asyncio.run(module.main())
            else:
                module.main()
        assert exc_info.value.code == 0, (
            f"{module_name}.main() --help exited with code "
            f"{exc_info.value.code!r}, expected 0 (argparse's own help exit)"
        )
    finally:
        sys.argv = old_argv


def _run_click_help(module_name: str, group_attr: str) -> None:
    """Exercise a module's click group with --help via CliRunner -- proves
    every @<group>.command() registered without raising, without invoking
    any command's callback."""
    from click.testing import CliRunner

    sys.modules.pop(module_name, None)
    module = importlib.import_module(module_name)
    group = getattr(module, group_attr)

    result = CliRunner().invoke(group, ["--help"])
    assert result.exit_code == 0, (
        f"{module_name}.{group_attr} --help exited {result.exit_code}, " f"output: {result.output}"
    )


def _check_keys_entry_shape() -> None:
    """keys.py has no argparse/click parser -- its entry point is the bare
    async function `rotate_key_interactive`, invoked directly from
    main.py's `rotate-key` command (verified: main.py:376-386). Its "entry
    shape" is that this callable exists, is a coroutine function, and has
    the (provider, user_id=None) signature main.py's call site depends on.
    This substitutes for the argparse/click check the other 7 modules get;
    stated explicitly per the module's docstring note (m-44: state what a
    check covers, never let a substitution pass as the same check)."""
    sys.modules.pop("cli.commands.keys", None)
    module = importlib.import_module("cli.commands.keys")

    assert hasattr(module, "rotate_key_interactive"), (
        "cli.commands.keys lost its main.py-invoked entry point " "rotate_key_interactive"
    )
    assert inspect.iscoroutinefunction(module.rotate_key_interactive)
    sig = inspect.signature(module.rotate_key_interactive)
    # main.py:386 calls rotate_key_interactive(provider) positionally.
    sig.bind("openai")


ENTRY_SHAPE_CHECKS: dict[str, Callable[[], None]] = {
    "cli.commands.cal": lambda: _run_argparse_help(
        "cli.commands.cal", is_async=True, argv_prog="cal.py"
    ),
    "cli.commands.documents": lambda: _run_click_help("cli.commands.documents", "documents"),
    "cli.commands.issues": lambda: _run_click_help("cli.commands.issues", "issues"),
    "cli.commands.keys": _check_keys_entry_shape,
    "cli.commands.notion": lambda: _run_argparse_help(
        "cli.commands.notion", is_async=True, argv_prog="notion.py"
    ),
    "cli.commands.personality": lambda: _run_argparse_help(
        "cli.commands.personality", is_async=False, argv_prog="personality.py"
    ),
    "cli.commands.publish": lambda: _run_argparse_help(
        "cli.commands.publish", is_async=True, argv_prog="publish.py"
    ),
    "cli.commands.standup": lambda: _run_argparse_help(
        "cli.commands.standup", is_async=False, argv_prog="standup.py"
    ),
}


def test_entry_shape_denominator_matches_filesystem() -> None:
    """State the denominator (m-44): every discovered module must have an
    entry-shape check registered, even if (like keys.py) that check is a
    stated substitution rather than an argparse/click invocation."""
    assert set(ENTRY_SHAPE_CHECKS) == set(COMMAND_MODULES)


@pytest.mark.smoke
@pytest.mark.parametrize("module_name", COMMAND_MODULES)
def test_command_entry_shape_constructs(module_name: str) -> None:
    """Every cli/commands/*.py module's argparse/click entry point must
    construct cleanly (every subparser/subcommand/argument registers), or
    (keys.py only) its substitute signature check must pass."""
    ENTRY_SHAPE_CHECKS[module_name]()


# ---------------------------------------------------------------------------
# 2. Unassigned self.attr detection
# ---------------------------------------------------------------------------


class _SelfAttrVisitor(ast.NodeVisitor):
    """Collects every `self.X` Load (read) and Store (assignment) anywhere
    in a class body, across ALL methods -- not just __init__ -- so a
    legitimate later-setup assignment (e.g. publish.py's
    `self.publisher = Publisher()` inside cmd_publish, not __init__) is not
    a false positive. What matters is: is X EVER assigned anywhere in this
    class before this class is usable, not just structurally, but at all."""

    def __init__(self) -> None:
        self.loads: set[str] = set()
        self.stores: set[str] = set()

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            if isinstance(node.ctx, ast.Load):
                self.loads.add(node.attr)
            elif isinstance(node.ctx, ast.Store):
                self.stores.add(node.attr)
        self.generic_visit(node)


def _discover_handler_classes(module_name: str) -> dict[str, tuple[set[str], set[str]]]:
    """Return {class_name: (loads, stores)} for every top-level class in the
    module's source that defines __init__ (the handler-class shape this
    codebase's cli/commands/*.py files use: NotionCommand, StandupCommand,
    IssuesCommand, CalendarCommand, PersonalityCLI, PublishCommand). A
    module with no such class (documents.py's bare click functions,
    keys.py's bare async functions) contributes an empty dict -- counted in
    the denominator, not silently skipped."""
    stem = module_name.rsplit(".", 1)[-1]
    source_path = COMMANDS_DIR / f"{stem}.py"
    tree = ast.parse(source_path.read_text(), filename=str(source_path))

    classes: dict[str, tuple[set[str], set[str]]] = {}
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        has_init = any(
            isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "__init__"
            for item in node.body
        )
        if not has_init:
            continue
        visitor = _SelfAttrVisitor()
        visitor.visit(node)

        # Two more legitimate "assignment" shapes that are NOT `self.X = ...`
        # but make `self.X` a real attribute at runtime via normal Python
        # attribute lookup (instance -> class -> MRO): a method defined in
        # the class body (self.print_colored resolves through the class),
        # and a class-level attribute assigned directly in the class body
        # (self.COLORS resolves through the class, e.g. `COLORS = {...}`
        # at class scope, not inside __init__). Without these, every
        # class's own methods and class-level constants would be flagged as
        # "read but never assigned" -- a false positive this AST walk must
        # not produce.
        class_scope_names: set[str] = set()
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                class_scope_names.add(item.name)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_scope_names.add(target.id)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                class_scope_names.add(item.target.id)

        classes[node.name] = (visitor.loads, visitor.stores | class_scope_names)
    return classes


def _all_handler_classes() -> list[tuple[str, str, set[str], set[str]]]:
    """Flatten to (module_name, class_name, loads, stores) across all 8
    modules -- the denominator for the unassigned-attr finding."""
    rows = []
    for module_name in COMMAND_MODULES:
        for class_name, (loads, stores) in _discover_handler_classes(module_name).items():
            rows.append((module_name, class_name, loads, stores))
    return rows


HANDLER_CLASSES = _all_handler_classes()


def test_handler_class_denominator_nonzero() -> None:
    """State the denominator (m-44): at least the known handler classes
    (NotionCommand, StandupCommand, IssuesCommand, CalendarCommand,
    PersonalityCLI, PublishCommand) must be discovered, or the AST
    discovery itself is broken rather than the codebase having no classes."""
    discovered = {name for _, name, _, _ in HANDLER_CLASSES}
    expected_minimum = {
        "NotionCommand",
        "StandupCommand",
        "IssuesCommand",
        "CalendarCommand",
        "PersonalityCLI",
        "PublishCommand",
    }
    assert expected_minimum <= discovered, (
        f"Expected handler classes missing from AST discovery: "
        f"{expected_minimum - discovered}. Denominator: {len(HANDLER_CLASSES)} "
        f"classes found across {len(COMMAND_MODULES)} modules."
    )


@pytest.mark.smoke
@pytest.mark.parametrize(
    "module_name,class_name",
    [(m, c) for m, c, _, _ in HANDLER_CLASSES],
    ids=[f"{m.rsplit('.', 1)[-1]}.{c}" for m, c, _, _ in HANDLER_CLASSES],
)
def test_no_unassigned_self_attrs(module_name: str, class_name: str) -> None:
    """Every self.X read anywhere in this class must be assigned
    SOMEWHERE in the class (any method) -- the #1873 defect shape
    (self.adapter read in 4 methods, assigned nowhere) fails this loudly
    instead of raising AttributeError only when a user runs the command."""
    classes = _discover_handler_classes(module_name)
    loads, stores = classes[class_name]
    unassigned = loads - stores
    assert not unassigned, (
        f"{module_name}.{class_name}: self.{{{', '.join(sorted(unassigned))}}} "
        f"read but never assigned anywhere in the class -- AttributeError on use."
    )


# ---------------------------------------------------------------------------
# 3. Signature-bind check: keys.py -> UserAPIKeyService, notion.py ->
#    NotionDomainService
# ---------------------------------------------------------------------------


def _extract_calls(source_path: Path, receiver: str) -> list[tuple[str, int, ast.Call]]:
    """Return (method_name, lineno, call_node) for every `<receiver>.method(...)`
    call site in the module's source, where <receiver> is either a bare
    Name (e.g. "key_service") or a "self.attr" dotted path (e.g.
    "self.notion_domain_service")."""
    tree = ast.parse(source_path.read_text(), filename=str(source_path))
    receiver_parts = receiver.split(".")

    def _receiver_matches(value: ast.expr) -> bool:
        if len(receiver_parts) == 1:
            return isinstance(value, ast.Name) and value.id == receiver_parts[0]
        # self.attr
        return (
            isinstance(value, ast.Attribute)
            and value.attr == receiver_parts[1]
            and isinstance(value.value, ast.Name)
            and value.value.id == receiver_parts[0]
        )

    calls = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and _receiver_matches(node.func.value)
        ):
            calls.append((node.func.attr, node.lineno, node))
    return calls


def _assert_calls_bind(source_path: Path, receiver: str, live_cls: type) -> list[str]:
    """For every <receiver>.method(...) call site, bind its extracted
    positional-arg count + keyword names against
    inspect.signature(live_cls.method) (skipping `self`). Returns a list of
    human-readable failure descriptions (empty = all bind)."""
    failures = []
    for method_name, lineno, call in _extract_calls(source_path, receiver):
        live_method = getattr(live_cls, method_name, None)
        if live_method is None:
            failures.append(
                f"{source_path.name}:{lineno}: {receiver}.{method_name}() -- "
                f"no such method on live {live_cls.__name__}"
            )
            continue
        sig = inspect.signature(live_method)
        # Drop `self` -- these are unbound function objects off the class.
        params = list(sig.parameters.values())
        if params and params[0].name == "self":
            sig = sig.replace(parameters=params[1:])

        n_positional = sum(1 for a in call.args if not isinstance(a, ast.Starred))
        has_star_args = any(isinstance(a, ast.Starred) for a in call.args)
        keywords = {kw.arg for kw in call.keywords if kw.arg is not None}
        has_star_kwargs = any(kw.arg is None for kw in call.keywords)

        if has_star_args or has_star_kwargs:
            # *args/**kwargs unpacking at the call site -- arity can't be
            # statically checked; not present in any call this test covers,
            # but don't silently pass it either.
            failures.append(
                f"{source_path.name}:{lineno}: {receiver}.{method_name}() uses "
                f"*args/**kwargs unpacking -- static bind check skipped, verify by hand"
            )
            continue

        placeholder_args = [object()] * n_positional
        placeholder_kwargs = {k: object() for k in keywords}
        try:
            sig.bind(*placeholder_args, **placeholder_kwargs)
        except TypeError as e:
            failures.append(
                f"{source_path.name}:{lineno}: {receiver}.{method_name}"
                f"({n_positional} positional, kwargs={sorted(keywords)}) does not "
                f"bind against live signature {live_method.__name__}{sig} -- {e}"
            )
    return failures


def test_keys_calls_bind_to_live_user_api_key_service() -> None:
    """Every key_service.<method>(...) call site in keys.py must bind
    against the live UserAPIKeyService's signature -- the exact class of
    defect #1873 named (test_key/skip_validation kwargs that don't exist)."""
    from services.security.user_api_key_service import UserAPIKeyService

    source_path = COMMANDS_DIR / "keys.py"
    failures = _assert_calls_bind(source_path, "key_service", UserAPIKeyService)
    assert not failures, "\n".join(failures)


def test_notion_calls_bind_to_live_notion_domain_service() -> None:
    """Every self.notion_domain_service.<method>(...) call site in
    notion.py must bind against the live NotionDomainService's signature."""
    from services.domain.notion_domain_service import NotionDomainService

    source_path = COMMANDS_DIR / "notion.py"
    failures = _assert_calls_bind(source_path, "self.notion_domain_service", NotionDomainService)
    assert not failures, "\n".join(failures)
