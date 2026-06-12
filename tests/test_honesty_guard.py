"""Honesty guard (#1196/#1197/#1198, m-41): banned robot-script phrases must not
reappear in user-facing source strings.

The 2026-06-12 audit found hardcoded responses claiming actions Piper didn't
take ("took a look at your calendar" while unconnected), promising behavior it
can't deliver ("I'll keep an eye on things", "I'll keep trying"), and
surveillance-shaped phrasing. The strings were fixed; this guard fails the
build if the class returns. Comment lines are exempt (explanatory references
to the banned phrases are how the fixes are documented).
"""

import os
import glob

# Substrings banned from NON-COMMENT source lines in services/ and web/.
BANNED = [
    # First-person monitoring claims only — "keep an eye on X" as ADVICE to the
    # user is honest; Piper claiming to watch is not.
    "I'll keep an eye",
    "I've been keeping an eye",
    "I'm keeping an eye",
    "thing I'm watching",
    "but I'll keep trying",
    "I'll keep track of that for you",
    "I'll remember that you prefer",
    "I'll remember this for next time",
    "You're absolutely right",
    "took a look at looking",
]

ROOTS = ("services", "web")


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
        if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "tests" else "."


def test_no_banned_robot_script_phrases():
    root = _repo_root()
    violations = []
    for top in ROOTS:
        for path in glob.glob(os.path.join(root, top, "**", "*.py"), recursive=True):
            if "test" in os.path.basename(path):
                continue
            with open(path, errors="ignore") as f:
                for lineno, line in enumerate(f, 1):
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        continue  # explanatory comments may reference the phrases
                    if "NEVER" in line or "Do NOT" in line:
                        continue  # prompt-constraint lines QUOTE phrases to ban them
                    for phrase in BANNED:
                        if phrase in line:
                            violations.append(f"{path}:{lineno}: {phrase!r}")
    assert not violations, (
        "Banned robot-script phrase(s) reintroduced (see #1196/#1197/#1198 — "
        "false action/monitoring/retry/memory claims or sycophancy):\n"
        + "\n".join(violations)
    )
