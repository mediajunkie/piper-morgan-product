#!/usr/bin/env python3
"""#2177: name staging's running image by digest, not by tag.

Reads `flyctl status --json` on stdin and prints `<repository>@sha256:<digest>` for the
image every started machine runs, or "" (the caller refuses) when there are no started
machines, when they disagree (a roll in progress), or when a machine carries no digest.
A tag only names an image, so the registry resolves it at pull time; a digest is the
image (Arch, 2026-10-25). Whether flyctl's machine JSON carries `image_ref.digest` was
unverified when this was written, so a missing digest prints "" and the promotion refuses
before alpha changes, never falling back to the tag.
"""

from __future__ import annotations

import json
import re
import sys

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _repository(image: str) -> str:
    """`registry.fly.io/app:tag` or `registry.fly.io/app@sha256:…` -> `registry.fly.io/app`."""
    name = image.split("@", 1)[0]
    head, _, last = name.rpartition("/")
    if ":" in last:
        last = last.split(":", 1)[0]
    return f"{head}/{last}" if head else last


def pinned_image(status: dict) -> str:
    started = [m for m in status.get("Machines") or [] if m.get("state") == "started"]
    pins = set()
    for machine in started:
        image = (machine.get("config") or {}).get("image") or ""
        ref = machine.get("image_ref") or machine.get("ImageRef") or {}
        digest = ref.get("digest") or ref.get("Digest") or ""
        if not image or not _DIGEST.match(digest):
            return ""
        pins.add(f"{_repository(image)}@{digest}")
    return pins.pop() if len(pins) == 1 else ""


if __name__ == "__main__":
    try:
        print(pinned_image(json.load(sys.stdin)))
    except (ValueError, AttributeError):
        print("")
