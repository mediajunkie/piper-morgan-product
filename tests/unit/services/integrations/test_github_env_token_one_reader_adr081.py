"""ADR-081 D1/D2 (Arch 10-24): the deployment's GitHub env token is read in one place only.

``GitHubConfigService.get_authentication_token("system")`` is the one local-only reader of
the env token names; it answers None on a hosted deploy. Nothing else in ``services/`` or
``web/`` may read ``GITHUB_TOKEN``, ``GH_TOKEN``, ``GITHUB_ACCESS_TOKEN``,
``GITHUB_API_TOKEN`` or a ``GITHUB_TOKEN_*`` form from the environment, so a user's
request can't be served on the deployment's identity and a status can't claim GitHub from
the env. A caller acting for an account uses that account's resolved credential.
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NAMES = {"GITHUB_TOKEN", "GH_TOKEN", "GITHUB_ACCESS_TOKEN", "GITHUB_API_TOKEN"}
THE_ONE_READER = "services/integrations/github/config_service.py"


def _is_env_read(node: ast.AST) -> bool:
    """os.getenv(...), os.environ.get(...), environ.get(...), or os.environ[...]."""
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "getenv":
            return True
        if (
            isinstance(f, ast.Attribute)
            and f.attr in ("get", "pop", "setdefault")
            and isinstance(f.value, (ast.Attribute, ast.Name))
            and getattr(f.value, "attr", getattr(f.value, "id", None)) == "environ"
        ):
            return True
    if isinstance(node, ast.Subscript):
        v = node.value
        return getattr(v, "attr", getattr(v, "id", None)) == "environ"
    return False


def _key(node: ast.AST):
    arg = node.args[0] if isinstance(node, ast.Call) and node.args else getattr(node, "slice", None)
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    if isinstance(arg, ast.JoinedStr):
        head = arg.values[0] if arg.values else None
        if isinstance(head, ast.Constant) and isinstance(head.value, str):
            return head.value
    return None


def _github_env_reads(path: Path):
    tree = ast.parse(path.read_text())
    hits = []
    for node in ast.walk(tree):
        if _is_env_read(node):
            key = _key(node)
            if key and (key in NAMES or key.startswith("GITHUB_TOKEN_")):
                hits.append((node.lineno, key))
    return hits


def test_only_the_one_reader_reads_the_github_env_token():
    offenders = []
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == THE_ONE_READER:
                continue
            for line, key in _github_env_reads(path):
                offenders.append(f"{rel}:{line} reads {key}")
    assert not offenders, (
        "Direct GitHub env-token reads outside GitHubConfigService.get_authentication_token"
        '("system") (ADR-081): ' + "; ".join(offenders)
    )


def test_the_scan_sees_each_read_shape(tmp_path):
    sample = tmp_path / "s.py"
    sample.write_text(
        "import os\n"
        "a = os.getenv('GITHUB_TOKEN')\n"
        "b = os.environ.get('GH_TOKEN')\n"
        "c = os.environ['GITHUB_ACCESS_TOKEN']\n"
        "d = os.getenv(f'GITHUB_TOKEN_{x}')\n"
        "e = 'GITHUB_TOKEN is a string in a message'\n"
    )
    assert [k for _, k in _github_env_reads(sample)] == [
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "GITHUB_ACCESS_TOKEN",
        "GITHUB_TOKEN_",
    ]
