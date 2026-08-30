"""#1232 P2/P3 — connector contract guard (m-41, ADR-070 D5) + github structural proof.

The guard enforces the four-method contract on adapters that **declare**
conformance (``IMPLEMENTS_CONNECTOR = True``), via pure AST (no import / no
instantiation). Declared-conformer scoping is deliberate: a not-yet-ported
adapter doesn't break the build, but a declared connector cannot silently skip
honest-degradation or status. Mirrors the TestSessionScopeCommitContract (#1193)
AST-enforcement pattern.

History: at creation there were 5 not-yet-ported adapters (and a companion test
asserting some adapters were unported). The 2026-08-29 spatial cold-island
disposal (PM-ruled 2026-08-15/16) deleted the four never-wired spatial adapters
(cicd/devenvironment/gitbook/linear), leaving every surviving adapter a declared
conformer, so that companion test's premise expired and it was removed. The
declared-conformer scoping stays: a future unported adapter still won't break
the build until it declares.
"""

import ast
import glob
import os

from services.mcp.consumer import connector

CONSUMER_DIR = os.path.dirname(connector.__file__)
REQUIRED = {"connect", "status", "resolve", "degrade"}


def _declaring_classes(path):
    """{class_name: {method_names}} for classes that declare IMPLEMENTS_CONNECTOR=True."""
    with open(path) as f:
        tree = ast.parse(f.read())
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            declares = any(
                isinstance(s, ast.Assign)
                and any(
                    isinstance(t, ast.Name) and t.id == "IMPLEMENTS_CONNECTOR" for t in s.targets
                )
                for s in node.body
            )
            if declares:
                out[node.name] = {
                    n.name
                    for n in node.body
                    if isinstance(n, (ast.AsyncFunctionDef, ast.FunctionDef))
                }
    return out


def _all_declaring():
    found = {}
    for path in glob.glob(os.path.join(CONSUMER_DIR, "*_adapter.py")):
        found.update(_declaring_classes(path))
    return found


def test_every_declared_connector_implements_all_four_methods():
    declaring = _all_declaring()
    assert declaring, "no Connector-declaring adapter found — the github proof should declare one"
    for cls, methods in declaring.items():
        missing = REQUIRED - methods
        assert not missing, (
            f"{cls} declares IMPLEMENTS_CONNECTOR but is missing {sorted(missing)} "
            f"(#1232 / ADR-070 D5: a declared connector must implement connect/status/resolve/degrade)"
        )


def test_github_adapter_is_a_declared_connector():
    assert "GitHubMCPSpatialAdapter" in _all_declaring()


def test_guard_helper_flags_declared_but_incomplete(tmp_path):
    bad = tmp_path / "bad_adapter.py"
    bad.write_text(
        "class Bad:\n"
        "    IMPLEMENTS_CONNECTOR = True\n"
        "    async def connect(self, u): ...\n"
        "    async def status(self, u): ...\n"
        "    async def resolve(self, u, r): ...\n"
        "    # missing degrade\n"
    )
    found = _declaring_classes(str(bad))
    assert "Bad" in found
    assert REQUIRED - found["Bad"] == {"degrade"}


def test_github_adapter_satisfies_runtime_connector_protocol():
    # Runtime isinstance via the runtime_checkable Protocol — real conformance, not just names.
    from services.mcp.consumer.connector import Connector
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    assert isinstance(GitHubMCPSpatialAdapter(), Connector)


def test_no_return_type_exposes_credential_material():
    """ADR-070 D3 + Arch #1232 constraint 5: no connector result/return type may carry raw
    token / refresh-token / secret. A type that *could* hold a credential violates D3
    structurally (the MCP server owns tokens; Piper stores bindings only). Auto-discovers
    every dataclass defined in connector.py, so new return types are checked by construction."""
    import dataclasses
    import inspect

    forbidden = (
        "token",
        "secret",
        "password",
        "credential",
        "api_key",
        "apikey",
        "access_key",
        "private_key",
        "refresh",
    )
    offenders = []
    for _, obj in inspect.getmembers(connector):
        if dataclasses.is_dataclass(obj) and getattr(obj, "__module__", "") == connector.__name__:
            for f in dataclasses.fields(obj):
                if any(sub in f.name.lower() for sub in forbidden):
                    offenders.append(f"{obj.__name__}.{f.name}")
    assert not offenders, (
        "#1232 D3 SECURITY BOUNDARY: connector return types must not carry credential material, "
        f"but found credential-named field(s): {offenders}. Per ADR-070 D3 the external MCP server "
        "owns OAuth/tokens; Piper stores bindings only. Store a binding_id, not a token."
    )
