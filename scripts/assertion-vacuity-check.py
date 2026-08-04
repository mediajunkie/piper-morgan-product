#!/usr/bin/env python3
"""
assertion-vacuity-check.py — find assertions that PASS when their input is empty.

WHY THIS EXISTS (2026-08-04, Arch)
----------------------------------
An enforcement test exists to make a property stay true. But an assertion whose
pass-condition includes the empty case cannot distinguish

    "I measured, and found no violations"     (the intent)
    "my detection broke and found nothing"    (the failure)

Those emit byte-identical output. That is m-44 — *a check that cannot tell
measured-clean from didn't-measure* — living inside the guard built to prevent it.

Found by hand on 2026-08-03 while reviewing `test_slack_identity_binding_guard.py`:
two of its four assertions were vacuity-capable (`set(deleters) <= {HOME}` and
`assert not offenders`), while the two that mattered most (creator, caller) used
equality and were sound. Reading caught what running a *passing* test never could —
a vacuous assertion passes exactly like a correct one. This makes that reading a
command, so the next one doesn't depend on someone thinking to look.

WHAT IT FLAGS
-------------
An assertion is VACUITY-CAPABLE if it passes on empty input:
  assert not X                     assert X == []  /  == {}  /  == set()
  assert len(X) == 0               assert X <= Y   (subset: ∅ ⊆ anything)
  assert all(...)                  assert len(X) < N  /  <= N
Non-vacuous (fails loudly on empty), for contrast:
  assert X == {"a","b"}            assert X          assert len(X) == 3

A test function is FLAGGED only if it has a vacuity-capable assertion AND no
companion "denominator" assertion proving it actually scanned something.

THE CURE (both one line, both already used elsewhere in this repo)
  - prefer equality over subset when you know what the set should contain
  - assert the denominator first:  assert scanned, "detection found nothing"
  - OR assert bidirectionally (`A - B` and `B - A`): if the derived set goes empty,
    the mirror half fails loudly. This tool treats such pairs as sound.

USAGE
    scripts/assertion-vacuity-check.py                    # default: enforcement suites
    scripts/assertion-vacuity-check.py tests/foo.py ...   # explicit targets
"""

import argparse
import ast
import os
import sys

DEFAULT_TARGETS = [
    "tests/test_architecture_enforcement.py",
    "tests/test_completion_ratchets.py",
    "tests/test_honesty_guard.py",
    "tests/test_slack_identity_binding_guard.py",
]

EMPTY_LITERALS = ("[]", "{}", "set()", "()", "0")


def _src(node, lines):
    try:
        return ast.get_source_segment("\n".join(lines), node) or ""
    except Exception:
        return ""


def _binop_operands(node):
    """For `A - B` return ('A','B'); else None. Used to spot bidirectional pairs."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
        l = getattr(node.left, "id", None) or getattr(getattr(node.left, "func", None), "id", None)
        r = getattr(node.right, "id", None) or getattr(getattr(node.right, "func", None), "id", None)
        if l and r:
            return (l, r)
    return None


def _bidirectional_names(test_node):
    """Names assigned from `A - B` where `B - A` is ALSO assigned in the same test.

    A bidirectional pair is JOINTLY non-vacuous: if the derived set goes empty,
    one half stays empty (passes) but the other becomes the whole ledger (fails
    loudly). Flagging either half alone is a false positive — found 2026-08-04
    by reading this tool's own output against #1433's ledger test.
    """
    pairs = {}
    for n in ast.walk(test_node):
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            tgt = getattr(n.targets[0], "id", None)
            ops = _binop_operands(n.value)
            if tgt and ops:
                pairs[tgt] = ops
    protected = set()
    for name, (a, b) in pairs.items():
        for other, (c, d) in pairs.items():
            if other != name and (c, d) == (b, a):
                protected.add(name)
    return protected


def classify(test_node, lines):
    """Return (vacuity_capable_assertions, has_denominator_guard)."""
    vac, denom = [], False
    protected = _bidirectional_names(test_node)
    for n in ast.walk(test_node):
        if not isinstance(n, ast.Assert):
            continue
        t = n.test
        text = _src(n, lines).replace("\n", " ")[:110]

        # --- denominator guards: a bare truthiness assert, or len(X) == N (N>0),
        #     or an equality against a NON-empty literal. These fail on empty.
        if isinstance(t, ast.Name):
            denom = True
            continue
        if isinstance(t, ast.Compare) and len(t.ops) == 1:
            op, right = t.ops[0], t.comparators[0]
            rtxt = (_src(right, lines) or "").strip()
            # equality against a non-empty literal => fails on empty => sound
            if isinstance(op, ast.Eq) and rtxt not in EMPTY_LITERALS:
                denom = True
                continue
            # subset: ∅ ⊆ anything => vacuity-capable
            if isinstance(op, (ast.LtE, ast.Lt)):
                vac.append(("subset/less-than", n.lineno, text))
                continue
            # == empty literal => vacuity-capable
            if isinstance(op, ast.Eq) and rtxt in EMPTY_LITERALS:
                vac.append(("== empty", n.lineno, text))
                continue
        # assert not X  => passes on empty
        if isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not):
            nm = getattr(t.operand, "id", None)
            if nm in protected:
                continue  # jointly non-vacuous: its mirror half fails loudly on empty
            vac.append(("not X", n.lineno, text))
            continue
        # assert all(...) => vacuously true on empty
        if isinstance(t, ast.Call) and isinstance(t.func, ast.Name) and t.func.id == "all":
            vac.append(("all() on empty", n.lineno, text))
            continue
    return vac, denom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*", default=None)
    args = ap.parse_args()
    targets = args.targets or [t for t in DEFAULT_TARGETS if os.path.exists(t)]

    # ⚠️ This tool must not commit its own defect: refuse to report "0 flagged"
    # when the real answer is "I scanned nothing."
    if not targets:
        print("⛔ VACUITY-CHECK ITSELF VACUOUS: no target files found. Not reporting a result.")
        return 2

    scanned_files = scanned_tests = 0
    flagged = []
    for path in targets:
        if not os.path.exists(path):
            print(f"  ⚠️  missing target (skipped): {path}")
            continue
        lines = open(path, encoding="utf-8").read().splitlines()
        tree = ast.parse("\n".join(lines))
        scanned_files += 1
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not fn.name.startswith("test"):
                continue
            scanned_tests += 1
            vac, denom = classify(fn, lines)
            if vac and not denom:
                flagged.append((path, fn.name, vac))

    if scanned_tests == 0:
        print("⛔ VACUITY-CHECK ITSELF VACUOUS: scanned files but found 0 test functions.")
        return 2

    print(f"SCOPE: {scanned_files} file(s), {scanned_tests} test function(s) scanned.")
    print("Flagged = has an assertion that passes on empty input AND no denominator guard.\n")

    if not flagged:
        print(f"✅ 0 of {scanned_tests} test functions flagged.")
    else:
        for path, name, vac in flagged:
            print(f"⚠️  {path}::{name}")
            for kind, lineno, text in vac:
                print(f"      L{lineno}  [{kind}]  {text}")
        print(f"\n⚠️  {len(flagged)} of {scanned_tests} test functions flagged.")

    print(
        "\nNOTE: a flag is a QUESTION, not a defect. `assert not offenders` is often exactly\n"
        "      right — the finding is only that it cannot tell an empty scan from a clean one.\n"
        "      Cure: assert the denominator first (`assert scanned, ...`), or prefer equality\n"
        "      over subset where you know what the set should contain.\n"
        "LIMIT: syntactic only. It cannot see whether a helper returns [] on error, which is\n"
        "       the other way a check goes quiet. Reading still catches things this cannot."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
