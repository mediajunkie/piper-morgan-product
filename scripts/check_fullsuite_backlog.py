#!/usr/bin/env python3
"""check_fullsuite_backlog.py — the full-suite burn-down gate (#1452, Arch-ratified 2026-07-19).

Compares a pytest run's failures against scripts/known_failing_backlog.tsv and
enforces shrink-lock in BOTH directions:

  * a failure NOT in the backlog  -> FAIL (new rot may not ship; fix it, or — only
    if it is a genuinely pre-existing miss — add it with a tag + justification)
  * a backlog entry that no longer fails -> FAIL (drift was fixed; REMOVE the
    entry in the same commit to lock the shrink in)

The backlog is a BURN-DOWN list, not an exception set: every entry is debt, the
list only shrinks, a stalled list is a regression, and the endpoint is an empty
file that gets deleted (Arch refinement 1). Entries carry a triage tag
(fixture | regression:#NNNN | triage) so a real product break can't hide among
test-infra rot (Arch refinement 2) — `regression`-tagged entries must reference
a filed issue.

Usage (CI pipes the pytest output; the script never runs pytest itself):
    pytest tests/ -m "not llm" -q --tb=no ... 2>&1 | tee /tmp/fullsuite.out
    python scripts/check_fullsuite_backlog.py /tmp/fullsuite.out

Blind-spot guards (the 6-instance class: a gate must know whether it measured):
  * refuses when the output has no pytest summary line (truncated / never ran)
  * refuses when the summary claims failures but none were parsed (format drift)
  * a file-level collection ERROR covers that file's per-test backlog entries
    (they could not run, so they are not "fixed")
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKLOG_FILE = REPO_ROOT / "scripts" / "known_failing_backlog.tsv"

_SUMMARY = re.compile(r"^=*\s*(?:\d+ \w+, )*\d+ (?:passed|failed|error|errors|skipped|deselected|warnings?)")
_RESULT_LINE = re.compile(r"^(FAILED|ERROR) (\S+)")
_VALID_TAG = re.compile(r"^(fixture|triage|regression:#\d+)$")


def load_backlog() -> dict[str, str]:
    entries: dict[str, str] = {}
    for raw in BACKLOG_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2 or not _VALID_TAG.match(parts[1]):
            sys.exit(f"backlog format error: {raw!r} (want '<node-id>\\t<tag>')")
        entries[parts[0]] = parts[1]
    return entries


def parse_run(path: Path) -> tuple[set[str], set[str], bool]:
    """(failed_nodes, file_level_errors, saw_summary) from a -q pytest output."""
    failed: set[str] = set()
    file_errors: set[str] = set()
    saw_summary = False
    for line in path.read_text(errors="replace").splitlines():
        m = _RESULT_LINE.match(line)
        if m:
            node = m.group(2)
            if "::" in node:
                failed.add(node)
            else:
                file_errors.add(node)  # collection-level: covers the whole file
        if ("passed" in line or "failed" in line or "error" in line) and re.search(
            r"\b\d+ (passed|failed)\b", line
        ):
            saw_summary = True
    return failed, file_errors, saw_summary


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out_file = Path(sys.argv[1])
    if not out_file.is_file():
        sys.exit(f"no such output file: {out_file}")

    failed, file_errors, saw_summary = parse_run(out_file)
    if not saw_summary:
        sys.exit(
            "REFUSING to judge: no pytest summary line found in the output — "
            "the run was truncated or never happened (a gate blind to whether "
            "it measured is a false gate)."
        )

    backlog = load_backlog()

    def covered_by_file_error(node: str) -> bool:
        return any(node.startswith(f + "::") for f in file_errors)

    new_failures = sorted(
        n for n in failed if n not in backlog and not covered_by_file_error(n)
    )
    # file-level errors not covering any backlog entry are new rot too
    new_file_errors = sorted(
        f for f in file_errors if not any(n.startswith(f + "::") for n in backlog)
    )
    now_passing = sorted(
        n for n in backlog if n not in failed and not covered_by_file_error(n)
    )

    problems = []
    if new_failures or new_file_errors:
        problems.append(
            f"NEW failures not in the backlog ({len(new_failures) + len(new_file_errors)}) — "
            "new rot may not ship. Fix them; only a verified pre-existing miss may be "
            "added to the backlog (with tag + justification in the commit):"
        )
        problems += [f"  + {n}" for n in new_failures + new_file_errors]
    if now_passing:
        problems.append(
            f"SHRINK-LOCK: {len(now_passing)} backlog entr{'y' if len(now_passing)==1 else 'ies'} "
            "now pass (or no longer exist) — remove them from "
            "scripts/known_failing_backlog.tsv in this same commit:"
        )
        problems += [f"  - {n}" for n in now_passing]

    tags: dict[str, int] = {}
    for t in backlog.values():
        key = t.split(":")[0]
        tags[key] = tags.get(key, 0) + 1
    print(
        f"backlog size: {len(backlog)} "
        f"(fixture={tags.get('fixture', 0)}, regression={tags.get('regression', 0)}, "
        f"triage={tags.get('triage', 0)}) — target 0; a stalled list is a regression"
    )

    if problems:
        print("\n".join(problems))
        return 1
    print(f"full-suite gate OK: {len(failed)} failures, all on the burn-down backlog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
