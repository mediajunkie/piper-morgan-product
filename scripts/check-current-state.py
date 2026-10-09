#!/usr/bin/env python3
"""check-current-state.py — keep BRIEFING-CURRENT-STATE.md a short, honestly dated "Now" page.

R6 step 3 (PM-approved 2026-10-04; built 2026-10-08, CIO). The page was 169 KB of accreted narrative and its
front matter said 09-28 while its footer said 10-05 (the evaluation's L-4: a false-clear date). Two checks:

  1. Size: the file must not exceed `size_cap_bytes` from its own front matter (default 12000).
  2. Honest date: front-matter `last_updated` must not be older than the newest YYYY-MM-DD date that
     appears in an attestation (the "*(Role, YYYY-MM-DD ...)*" parentheticals in the Now section).

It does NOT fail on age: a stale page is the session-start hook's warning to raise, not a red main.
Exit 0 = pass; 1 = a check failed (message says which); 3 = could not measure (file or front matter missing).

Cost: one file read per Code Quality run. Benefit: none yet: measuring. Review: 2026-12-01. Owner: CIO.
"""

import re
import sys
from pathlib import Path

PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/briefing/BRIEFING-CURRENT-STATE.md")
ATTEST = re.compile(r"\*\([^)]*?(\d{4}-\d{2}-\d{2})")


def main():
    if not PATH.exists():
        print(f"check-current-state: NOT MEASURED, {PATH} missing")
        return 3
    raw = PATH.read_bytes()
    text = raw.decode("utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        print("check-current-state: NOT MEASURED, no front matter")
        return 3
    fm = dict(
        (k.strip(), v.strip().strip('"'))
        for k, _, v in (line.partition(":") for line in m.group(1).splitlines())
        if k.strip()
    )
    cap = int(fm.get("size_cap_bytes", "12000"))
    last = fm.get("last_updated", "")
    dates = sorted(ATTEST.findall(text))
    newest = dates[-1] if dates else None
    rc = 0
    if len(raw) > cap:
        print(
            f"FAIL size: {len(raw)} bytes > cap {cap}. Move narrative to the omnibus or "
            "docs/internal/architecture/decisions/briefing-current-state-history.log; replace lines, don't append."
        )
        rc = 1
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", last):
        print(f"FAIL date: front-matter last_updated {last!r} is not YYYY-MM-DD")
        rc = 1
    elif newest and last < newest:
        print(
            f"FAIL date: last_updated {last} is older than the newest attested line ({newest}); bump it."
        )
        rc = 1
    print(
        f"check-current-state: {len(raw)}/{cap} bytes; last_updated {last}; "
        f"{len(dates)} attested lines, newest {newest or 'none'} — {'PASS' if rc == 0 else 'FAIL'}"
    )
    return rc


if __name__ == "__main__":
    sys.exit(main())
