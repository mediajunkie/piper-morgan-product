"""Every direct child of docs/internal/ and docs/internal/architecture/ is excluded from the site, or
is one of the two folders published on purpose.

xian's "part 1 please" (2026-11-22, relayed by Docs 01M8291B1R) put the ADRs and the patterns catalog
on pmorgan.tech, so `docs/_config.yml` now excludes `internal/` child by child. Its own comment says a
new child is PUBLIC BY DEFAULT until someone adds it. This test turns that into a failing check: a new
file or folder at either level fails here until it is added to `exclude:` or, by a ruling, to PUBLISHED.
"""

import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
PUBLISHED = {"internal/architecture/adrs", "internal/architecture/patterns"}


def direct_children():
    out = subprocess.run(
        ["git", "ls-files", "docs/internal"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    kids = set()
    for path in filter(None, out.split("\n")):
        parts = path[len("docs/") :].split("/")
        kids.add("/".join(parts[:2]))
        if parts[1] == "architecture" and len(parts) >= 3:
            kids.add("/".join(parts[:3]))
    kids.discard("internal/architecture")
    return kids


def test_every_internal_child_is_excluded_or_published_on_purpose():
    config = yaml.safe_load((ROOT / "docs" / "_config.yml").read_text(encoding="utf-8"))
    excluded = set(config.get("exclude") or [])
    kids = direct_children()
    assert len(kids) > 10, "found too few children; the walk or the folder layout moved"
    assert PUBLISHED <= kids, "a published folder is gone; update PUBLISHED"
    unreviewed = sorted(k for k in kids if k not in excluded and k not in PUBLISHED)
    assert not unreviewed, (
        "public on pmorgan.tech by default, not yet reviewed: "
        f"{unreviewed}. Add each to docs/_config.yml exclude:, or publish it by a ruling."
    )
