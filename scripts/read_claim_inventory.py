#!/usr/bin/env python3
"""#2151 step 1: the read-claim inventory.

Every user-facing reply built from a read of the user's data takes one of five
states, each with its own honest wording: verified, failed, narrowed, not
performed, substituted. This script computes the LIVE set of surfaces that can
make such a claim from code (never from a hand list), joins it with the
classification in ``docs/internal/architecture/current/read-claim-inventory.yaml``
and prints the table.

Live surfaces (the denominator):

- ``rail``   one canonical name per unique action-triggered ``WorkflowEntry`` in
             ``WORKFLOW_REGISTRY`` after ``register_default_workflows()``: the same
             walk as ``workflow_dispatcher.wired_chat_actions`` part 1.
- ``legacy`` ``set(ActionMapper.ACTION_MAPPING.values()) - {"unknown_intent"}``
             not already on the rail.
- ``floor``  the floor's ``SOURCE_FAILED_FLAGS`` (``floor:<flag>``) plus every
             ``ContextAssembler._gather_*`` source (``floor:assembler.<method>``),
             registered there or not.
- ``route``  every route decorator in the integration settings, setup and
             integration test/health route modules (``route:<METHOD> <path>``),
             parsed with ``ast``.

Exit codes: 0 ok; 1 the YAML is missing a live surface or holds a stale row
(ids listed); 2 the live count is 0 (refuse to report on zero: the #1423
lesson, a ceiling passes when detection breaks).

Run (no LLM or network calls are made):

    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \\
        venv/bin/python scripts/read_claim_inventory.py [--json]

Concept: docs/internal/architecture/current/intent-routing-stack.md
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "docs" / "internal" / "architecture" / "current" / "read-claim-inventory.yaml"

ROUTE_FILES = (
    "web/api/routes/settings_integrations.py",
    "web/api/routes/setup.py",
    # The Settings "Test" button and the integration health probe (#2125's
    # surface): the status probes the two files above point users at.
    "web/api/routes/integrations.py",
)

STATES = ("verified", "failed", "narrowed", "not_performed", "substituted")
VERDICTS = ("green", "red", "exempt", "unknown")
KINDS = ("rail", "legacy", "floor", "route")
_HTTP_METHODS = {"get", "post", "put", "delete", "patch"}


def _ensure_repo_on_path() -> None:
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))


def rail_surfaces() -> Dict[str, str]:
    """``{canonical_name: effect}`` for the registry rail (wired_chat_actions part 1)."""
    _ensure_repo_on_path()
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent
    out: Dict[str, str] = {}
    seen: set = set()
    for key, entry in WORKFLOW_REGISTRY.items():
        if not entry.action_triggered:
            continue
        if id(entry) in seen:
            continue
        seen.add(id(entry))
        out[key] = getattr(entry.effect, "name", str(entry.effect))
    return out


def legacy_surfaces(rail: Dict[str, str]) -> List[str]:
    _ensure_repo_on_path()
    from services.intent_service.action_mapper import ActionMapper

    targets = set(ActionMapper.ACTION_MAPPING.values()) - {"unknown_intent"}
    return sorted(t for t in targets if t not in rail)


def floor_surfaces() -> List[str]:
    _ensure_repo_on_path()
    from services.intent_service.context_assembler import ContextAssembler
    from services.intent_service.conversational_floor import SOURCE_FAILED_FLAGS

    ids = [f"floor:{entry.flag}" for entry in SOURCE_FAILED_FLAGS]
    ids += [
        f"floor:assembler.{name}"
        for name in sorted(vars(ContextAssembler))
        if name.startswith("_gather_") and callable(getattr(ContextAssembler, name))
    ]
    return ids


def _router_prefix(tree: ast.Module) -> str:
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
            if name != "APIRouter":
                continue
            if not any(isinstance(t, ast.Name) and t.id == "router" for t in node.targets):
                continue
            for kw in node.value.keywords:
                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                    return str(kw.value.value)
    return ""


def route_surfaces() -> List[Tuple[str, str]]:
    """``[(id, "file.py:function")]`` for every ``@router.<method>(path)`` decorator."""
    out: List[Tuple[str, str]] = []
    for rel in ROUTE_FILES:
        tree = ast.parse((REPO / rel).read_text(), filename=rel)
        prefix = _router_prefix(tree)
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)):
                    continue
                if dec.func.attr not in _HTTP_METHODS:
                    continue
                if not (isinstance(dec.func.value, ast.Name) and dec.func.value.id == "router"):
                    continue
                if not dec.args or not isinstance(dec.args[0], ast.Constant):
                    continue
                path = prefix + str(dec.args[0].value)
                out.append((f"route:{dec.func.attr.upper()} {path}", f"{rel}:{node.name}"))
    return out


def live_surfaces() -> Dict[str, Dict[str, str]]:
    """``{id: {"kind", "effect"}}`` for the whole live set. Module import and
    registration log to stdout, so that noise goes to stderr here."""
    with contextlib.redirect_stdout(sys.stderr):
        rail = rail_surfaces()
        legacy = legacy_surfaces(rail)
        floor = floor_surfaces()
    routes = route_surfaces()
    live: Dict[str, Dict[str, str]] = {}
    for name, effect in rail.items():
        live[name] = {"kind": "rail", "effect": effect}
    for name in legacy:
        live[f"legacy:{name}"] = {"kind": "legacy", "effect": "EXECUTION"}
    for fid in floor:
        live[fid] = {"kind": "floor", "effect": "READ"}
    for rid, _handler in routes:
        live[rid] = {"kind": "route", "effect": "READ"}
    return live


def load_inventory(path: Path = YAML_PATH) -> List[Dict[str, Any]]:
    import yaml

    data = yaml.safe_load(path.read_text())
    rows = data.get("surfaces", []) if isinstance(data, dict) else data
    return list(rows or [])


def join(
    live: Dict[str, Dict[str, str]], rows: List[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    """``(missing, stale)``: live ids with no row, and rows with no live surface."""
    row_ids = [r.get("id") for r in rows]
    missing = sorted(set(live) - set(row_ids))
    stale = sorted(set(row_ids) - set(live))
    return missing, stale


def conflations(row: Dict[str, Any]) -> List[str]:
    states = row.get("states") or {}
    return [
        f"{s}->{str(states[s]).split(':', 1)[1]}"
        for s in STATES
        if str(states.get(s, "")).startswith("conflated:")
    ]


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    verdicts = Counter(str(r.get("verdict", "unknown")) for r in rows)
    per_kind: Dict[str, Counter] = {k: Counter() for k in KINDS}
    for r in rows:
        per_kind.setdefault(str(r.get("kind")), Counter())[str(r.get("verdict", "unknown"))] += 1
    return {
        "total": len(rows),
        "verdicts": {v: verdicts.get(v, 0) for v in VERDICTS},
        "per_kind": {
            k: {"total": sum(c.values()), **{v: c.get(v, 0) for v in VERDICTS}}
            for k, c in per_kind.items()
        },
    }


def footer(summary: Dict[str, Any]) -> str:
    v = summary["verdicts"]
    line = (
        f"{summary['total']} surfaces: {v['green']} green, {v['red']} red, "
        f"{v['exempt']} exempt, {v['unknown']} unknown"
    )
    kinds = "; ".join(
        f"{k} {c['total']} ({c['green']}g/{c['red']}r/{c['exempt']}e/{c['unknown']}u)"
        for k, c in summary["per_kind"].items()
    )
    return f"{line}\nper kind: {kinds}"


def _cell(text: Any) -> str:
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


def markdown(rows: List[Dict[str, Any]]) -> str:
    out = ["| id | reads | verdict | conflated states |", "|---|---|---|---|"]
    for r in rows:
        out.append(
            f"| `{_cell(r.get('id'))}` | {_cell(r.get('reads'))} | {_cell(r.get('verdict'))} | "
            f"{_cell(', '.join(conflations(r)) or '-')} |"
        )
    return "\n".join(out)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    live = live_surfaces()
    if not live:
        print("REFUSED: the live surface count is 0; detection is broken (#1423).", file=sys.stderr)
        return 2

    rows = load_inventory()
    missing, stale = join(live, rows)
    if missing or stale:
        for rid in missing:
            print(f"MISSING from YAML: {rid}", file=sys.stderr)
        for rid in stale:
            print(f"STALE in YAML (no live surface): {rid}", file=sys.stderr)
        return 1

    order = {rid: i for i, rid in enumerate(live)}
    rows = sorted(rows, key=lambda r: order.get(r.get("id"), len(order)))
    summary = summarize(rows)
    if args.json:
        payload = {
            "summary": summary,
            "surfaces": [{**r, "conflated": conflations(r)} for r in rows],
        }
        print(json.dumps(payload, indent=2, default=str))
    else:
        print(markdown(rows))
        print()
        print(footer(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
