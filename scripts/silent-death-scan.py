#!/usr/bin/env python3
"""
silent-death-scan.py — inventory the `except Exception → return <default>` shape (#1423).

WHY THIS EXISTS (2026-08-09, Arch)
----------------------------------
#1423's ask #1 is an INVENTORY of broad exception handlers on the core path. The
pattern is:

    except Exception:
        logger.warning(...)
        return <plausible default>

Intended as resilience. Actual effect: a broken feature produces no user-visible
failure and no test failure — it returns defaults, for months. #1420 and #1422 were
each found by accident, not by a check.

This is the same family as `assertion-vacuity-check.py`: **a failure that emits the
same observable output as success.** There, an assertion couldn't distinguish
measured-clean from didn't-measure. Here, a caller can't distinguish "no results"
from "the call raised and we swallowed it."

WHAT IT FLAGS
-------------
An `except` handler is SILENT-DEATH-SHAPED when it is broad (`except Exception`,
`except BaseException`, or bare `except:`) AND its body returns a *plausible default*
rather than re-raising or returning an error signal:
  return None / [] / {} / () / "" / 0 / False / <literal>
  return SomeClass.get_default() / <name>_default(...) / DEFAULT_<X>

NOT flagged (these are the good shapes):
  handlers that `raise` / `raise ... from e`
  handlers that return an explicit error object or a Result/Either
  narrow handlers (`except KeyError`, `except (ValueError, TypeError)`)

USAGE
    scripts/silent-death-scan.py                 # core-path defaults from #1423
    scripts/silent-death-scan.py services/foo    # explicit roots

LIMITS (stated, per this repo's habit)
  - Syntactic only. It cannot tell a *genuinely expected* Exception from an
    unexpected one; a flag is a QUESTION, not a defect.
  - It does not know whether the default is user-visible. A swallowed error behind
    a feature nobody reaches is lower-priority than one on the intent path.
  - It cannot see swallowing done via a decorator or a context manager.
"""

import argparse
import ast
import os
import sys

# The core-path roots #1423 names.
# EXACTLY the surfaces #1423 names. NOTE: this list is the ISSUE'S scope, and it
# does NOT contain services/todo — where #1420, one of the issue's own two
# confirmed instances, actually lives. Pass roots explicitly to widen.
DEFAULT_ROOTS = [
    "services/intent",
    "services/intent_service",
    "services/personality",
    "services/knowledge",
    "services/consciousness",
    "web/api/routes/intent.py",
]

EMPTY_DEFAULTS = (None, [], {}, (), "", 0, False)


def _is_broad(handler):
    """Bare `except:`, `except Exception`, or `except BaseException`."""
    t = handler.type
    if t is None:
        return True
    names = []
    if isinstance(t, ast.Name):
        names = [t.id]
    elif isinstance(t, ast.Tuple):
        names = [e.id for e in t.elts if isinstance(e, ast.Name)]
    return any(n in ("Exception", "BaseException") for n in names)


def _returns_plausible_default(handler):
    """Return (True, description) if the handler returns a default instead of raising."""
    for node in ast.walk(handler):
        if isinstance(node, ast.Raise):
            return (False, None)  # re-raises somewhere → not silent
    for node in ast.walk(handler):
        if not isinstance(node, ast.Return):
            continue
        v = node.value
        if v is None:
            return (True, "bare `return`")
        if isinstance(v, ast.Constant):
            return (True, f"return {v.value!r}")
        if isinstance(v, (ast.List, ast.Dict, ast.Tuple, ast.Set)) and not getattr(v, "elts", getattr(v, "keys", [1])):
            return (True, "return empty collection")
        if isinstance(v, ast.Call):
            fn = v.func
            nm = getattr(fn, "attr", None) or getattr(fn, "id", "")
            if "default" in nm.lower() or "fallback" in nm.lower() or "empty" in nm.lower():
                return (True, f"return {nm}(...)")
        if isinstance(v, ast.Name) and ("default" in v.id.lower() or "fallback" in v.id.lower()):
            return (True, f"return {v.id}")
    return (False, None)


def scan_file(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except Exception:
        return []
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if not _is_broad(node):
            continue
        hit, why = _returns_plausible_default(node)
        if hit:
            logs = any(
                isinstance(n, ast.Call)
                and getattr(getattr(n, "func", None), "attr", "") in ("warning", "error", "exception", "debug", "info")
                for n in ast.walk(node)
            )
            out.append((node.lineno, why, logs))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*", default=None)
    args = ap.parse_args()
    roots = args.roots or [r for r in DEFAULT_ROOTS if os.path.exists(r)]

    if not roots:
        print("⛔ SCAN ITSELF VACUOUS: none of the core-path roots exist. Not reporting a result.")
        return 2

    files = 0
    findings = []
    for root in roots:
        if os.path.isfile(root):
            files += 1
            for lineno, why, logs in scan_file(root):
                findings.append((root, lineno, why, logs))
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                p = os.path.join(dirpath, fn)
                files += 1
                for lineno, why, logs in scan_file(p):
                    findings.append((p, lineno, why, logs))

    if files == 0:
        print("⛔ SCAN ITSELF VACUOUS: roots exist but contain no .py files.")
        return 2

    print(f"SCOPE: {files} file(s) under {', '.join(roots)}")
    print("Flagged = broad `except` whose handler RETURNS A DEFAULT instead of raising.\n")

    if not findings:
        print(f"✅ 0 silent-death-shaped handlers in {files} files.")
    else:
        by_file = {}
        for p, lineno, why, logs in findings:
            by_file.setdefault(p, []).append((lineno, why, logs))
        for p in sorted(by_file):
            print(f"⚠️  {p}")
            for lineno, why, logs in sorted(by_file[p]):
                tag = "logs+swallows" if logs else "SWALLOWS SILENTLY"
                print(f"      L{lineno:<5} {why:<32} [{tag}]")
        print(f"\n⚠️  {len(findings)} handler(s) across {len(by_file)} file(s).")

    print(
        "\nNOTE: a flag is a QUESTION, not a defect. Some broad handlers are correct —\n"
        "      the finding is that the caller cannot distinguish 'no result' from\n"
        "      'this raised and we hid it'. Triage by whether the default is USER-VISIBLE.\n"
        "LIMITS: syntactic only; cannot see decorator/context-manager swallowing; cannot\n"
        "        judge whether the caught Exception was genuinely expected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
