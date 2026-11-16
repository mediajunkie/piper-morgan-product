#!/usr/bin/env python3
"""Dummy stand-in for a seat helper that uses a seat credential without showing it.

Part of CIO's harness test for the seat-test-harness proposal (2026-11-15).
It reads one fixed file that holds a DUMMY value and one environment variable
that holds a DUMMY value, and prints only lengths and a short hash. It makes no
network call and writes nothing. It never prints a value.
"""

import hashlib
import os
import pathlib
import sys

FILE = pathlib.Path.home() / ".piper-shared" / "seat-dummy-credential-2026-11-15.txt"
VAR = "PIPER_SEAT_DUMMY_KEY"


def main() -> int:
    ok = True
    try:
        data = FILE.read_bytes()
        print(f"file: read ok, {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()[:8]}")
    except OSError as exc:
        ok = False
        print(f"file: NOT READ ({type(exc).__name__})")
    val = os.environ.get(VAR, "")
    if val:
        print(
            f"env: {VAR} set, {len(val)} chars, sha256 {hashlib.sha256(val.encode()).hexdigest()[:8]}"
        )
    else:
        ok = False
        print(f"env: {VAR} UNSET")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
