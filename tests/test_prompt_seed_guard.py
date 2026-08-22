"""Prompt seed guard (#1655, mechanism family of #1544/#1648): the known
fabrication-seed sentences must never reappear in any prompt surface.

Four incidents (2026-08-16 and 2026-08-18) trace to EXAMPLE REPLY SENTENCES
in prompt guidance being assembled into live replies — including two
fabricated action confirmations copied near-verbatim from the guidance's own
examples. The per-section pins (test_todo_scope_framing_1544,
test_floor_action_claims_1648, test_sibling_verified_empty_1639) guard the
floor addendum; this guard is the repo-wide backstop against the exact seed
strings being reintroduced ANYWHERE in services/, web/, or config/ by
copy-paste — the reintroduction path the incidents proved cheap.

Scope decisions, on the record:
- Banned strings are the DISTINCTIVE cores of the four incident seeds, chosen
  so no legitimate copy collides (verified at guard-creation: the real
  reminder confirmation is "Reminder saved:", never "Reminder set for";
  repo-wide grep found zero non-comment occurrences).
- #1544's second seed ("…in this conversation", the scoping fragment) is too
  generic for a repo-wide ban — it stays enforced at the section level by the
  #1544/#1639 pins ("this conversation" not in the fabrication section).
- Unlike test_honesty_guard.py, there is NO exemption for NEVER/"Do NOT"
  lines: #1570 proved the model imitates vocabulary its prompt teaches even
  when prohibited, so quoting a seed sentence to ban it re-seeds it. Rules
  must describe the banned shape without reciting it. Comment lines stay
  exempt (fix documentation legitimately references the incident strings).
"""

import glob
import os

# Distinctive cores of the four #1544/#1648 incident seed sentences.
SEED_STRINGS = [
    # #1544 instance: the floor prompt's own empty-data example became PM's
    # live reply, verbatim.
    "I don't see any todos",
    # #1648 instance 3: "On it — creating that now…" was a literal example
    # reply string in the guidance; the core is distinctive without the
    # (too-generic) "On it" opener.
    "creating that now",
    # #1648 instance 4: "Reminder set for 3pm tomorrow ✓" was a literal
    # example; real save copy is "Reminder saved:" (todo_handlers), so this
    # prefix has no legitimate use.
    "Reminder set for",
]

ROOTS_PY = ("services", "web")
CONFIG_GLOB = os.path.join("config", "*.md")  # PIPER.md is a prompt source


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here) if os.path.basename(here) == "tests" else "."


def test_no_incident_seed_strings_in_prompt_surfaces():
    root = _repo_root()
    violations = []

    def scan(path, exempt_comments):
        with open(path, errors="ignore") as f:
            for lineno, line in enumerate(f, 1):
                if exempt_comments and line.strip().startswith("#"):
                    continue  # fix documentation may reference the seeds
                for phrase in SEED_STRINGS:
                    if phrase in line:
                        violations.append(f"{path}:{lineno}: {phrase!r}")

    for top in ROOTS_PY:
        for path in glob.glob(os.path.join(root, top, "**", "*.py"), recursive=True):
            if "test" in os.path.basename(path):
                continue
            scan(path, exempt_comments=True)

    for path in glob.glob(os.path.join(root, CONFIG_GLOB)):
        scan(path, exempt_comments=False)

    assert not violations, (
        "Fabrication-seed sentence(s) reintroduced (see #1655; mechanism in "
        "#1544/#1648 — example reply strings in prompt guidance become live "
        "replies, including fabricated action confirmations). State the rule "
        "without reciting the sentence:\n" + "\n".join(violations)
    )
