"""#1507: github/save wrote os.environ["GITHUB_TOKEN"] process-wide — any
authenticated user's save changed the ambient token every env-reading GitHub
path used (cross-tenant bleed), and refilled the env fallback that #1461(a)
gates off for real users. Pin: the save route must never mutate the process
environment.
"""

import ast


class TestGitHubSaveNoEnvMutation:
    def test_no_os_environ_writes_anywhere_in_settings_integrations(self):
        """AST-level pin, not a string grep: no Subscript-assignment or
        setdefault/update on os.environ in the whole route module — the class
        is banned, not the one line. Denominator: the module must parse and
        contain the github save route (guards against the file moving)."""
        path = "web/api/routes/settings_integrations.py"
        with open(path) as f:
            tree = ast.parse(f.read(), filename=path)

        source_has_github_save = any(
            isinstance(node, ast.AsyncFunctionDef) and "github" in node.name.lower()
            for node in ast.walk(tree)
        )
        assert source_has_github_save, (
            "settings_integrations.py no longer defines a github route — "
            "relocate this pin to wherever github/save moved"
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
            # os.environ.setdefault(...) / os.environ.update(...) / pop with default write intent
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ("setdefault", "update", "pop") and is_os_environ(
                    node.func.value
                ):
                    violations.append(
                        f"line {node.lineno}: os.environ.{node.func.attr}(...)"
                    )

        assert not violations, (
            "process-wide env mutation in settings_integrations.py (#1507 class): "
            + "; ".join(violations)
        )
