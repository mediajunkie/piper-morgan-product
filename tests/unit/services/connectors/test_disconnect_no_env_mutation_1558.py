"""#1558: the user-scoped GitHub disconnect ran `os.environ.pop("GITHUB_TOKEN")`
(+ GITHUB_API_TOKEN / GH_TOKEN) — a process-wide ambient-credential mutation,
the mirror image of #1507 (whose env WRITE in github/save was deleted). One
user's disconnect deleted the SYSTEM/deployment credential for every
env-reading path in the process, and since #1461(a) the env fallback is
system-only anyway (GitHubConfigService gates it on `not is_real_user`), so
the pop protected no user path. Pin: the disconnect module must never mutate
the process environment — user disconnect touches only user-scoped stores.
"""

import ast


class TestDisconnectNoEnvMutation:
    def test_no_os_environ_mutation_anywhere_in_disconnect_module(self):
        """AST-level pin, not a string grep: no Subscript-assignment, `del`,
        or setdefault/update/pop/popitem/clear call on os.environ anywhere in
        the module — the class is banned, not the one line (same shape as the
        #1507 pin). Denominator: the module must parse and contain the GitHub
        disconnect impl (guards against the file moving)."""
        path = "services/connectors/disconnect.py"
        with open(path) as f:
            tree = ast.parse(f.read(), filename=path)

        source_has_github_disconnect = any(
            isinstance(node, ast.AsyncFunctionDef) and "github" in node.name.lower()
            for node in ast.walk(tree)
        )
        assert source_has_github_disconnect, (
            "disconnect.py no longer defines a github disconnect — "
            "relocate this pin to wherever _disconnect_github moved"
        )

        def is_os_environ(node) -> bool:
            return (
                isinstance(node, ast.Attribute)
                and node.attr == "environ"
                and isinstance(node.value, ast.Name)
                and node.value.id == "os"
            )

        violations = []
        for node in ast.walk(tree):
            # os.environ["X"] = ... (direct or via tuple-unpack targets)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Subscript) and is_os_environ(target.value):
                        violations.append(f"line {node.lineno}: os.environ[...] assignment")
            # del os.environ["X"] — the pop-equivalent this module's bug class uses
            if isinstance(node, ast.Delete):
                for target in node.targets:
                    if isinstance(target, ast.Subscript) and is_os_environ(target.value):
                        violations.append(f"line {node.lineno}: del os.environ[...]")
            # os.environ.pop/setdefault/update/popitem/clear(...)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in (
                    "pop",
                    "setdefault",
                    "update",
                    "popitem",
                    "clear",
                ) and is_os_environ(node.func.value):
                    violations.append(f"line {node.lineno}: os.environ.{node.func.attr}(...)")

        assert not violations, (
            "process-wide env mutation in disconnect.py (#1558, #1507 class): "
            + "; ".join(violations)
        )
