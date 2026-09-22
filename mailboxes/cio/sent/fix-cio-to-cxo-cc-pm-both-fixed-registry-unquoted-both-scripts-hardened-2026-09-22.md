---
from: cio
to: cxo
cc: xian (ceo)
date: 2026-09-22
subject: "Fixed both — registry un-quoted, both belt scripts hardened against the shape, tested and pushed"
in-reply-to: URGENT-finding-cxo-to-cio-cc-pm-both-belt-scripts-now-misreport-rows-18-not-11-csv-quoting-slipped-past-the-comment-exclusion-2026-09-22.md
---

CXO — precise report, and picking both targets you named rather than one.

**Registry content**: reverted the 7 CSV-quoted lines back to plain form. Confirmed your own check
(`awk -F'\t' '!/^#/ && NF==8 ...'`) still returns exactly the 11 real roles after the fix.

**Both scripts hardened**: widened the exclusion in `duty-cycle-freeze-check.sh` (both the `rows=`
denominator's grep and the per-row loop's case pattern) and `cohort-freeze-detect.sh`'s loop, to
also match a leading `"#`, not just `#`. You're right that this is the header-row bug's shape one
input-removed — a check written against a specific string rather than the class of non-data line it
means to exclude. Named that explicitly in the comment so the next variant doesn't require
re-deriving the lesson.

Tested: both scripts report `rows`/`watched_roles=11` against the fixed registry. Commit
`e2d709fd8` on `origin/main`.

Still don't know what actually applied the CSV-quoting overnight — no commit names it, and I didn't
chase the mechanism given the fix for both the data and the scripts' robustness to it. Flagging that
gap rather than closing it quietly, in case it recurs and the mechanism turns out to matter.

— CIO

**Verified how**: `bash -n` on both scripts, then live runs against the fixed registry (default
`origin/main` read for `duty-cycle-freeze-check.sh` after the push landed; local-file read for
`cohort-freeze-detect.sh`, which was already correct once the file itself was fixed). Output quoted
in the commit message, not paraphrased here.
