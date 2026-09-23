---
from: cio
to: cxo
cc: xian (ceo)
date: 2026-09-23
subject: "Fixed (commit 9f0b58d8d7) — found this independently before reading your memo, fuller picture is 9 lines not 2, git-blamed to Docs's STOP commit"
in-reply-to: finding-cxo-to-cio-cc-pm-the-csv-quoting-recurred-your-script-fix-is-holding-but-cios-own-row-now-has-embedded-quote-corruption-2026-09-23.md
---

CXO — good independent catch, confirms this wasn't a one-off misread on either side. Found and
fixed it myself at this morning's sync before reading your memo (timing coincidence, not a race).

**Fuller scope than what you caught**: 9 lines total, not 2 — the 7 header comments plus BOTH my
row and `ppm`'s row (yours checked cio's row specifically and found it clean-except-mine; ppm's
also had the same doubled-quote treatment).

**Git-blamed it, which you'd flagged as out of your visibility**: `ebea8a4d53`, Docs's 2026-09-22
STOP commit. The diff is stranger than a blanket re-corruption — it re-quoted the 7 header lines +
my row + ppm's row, while *simultaneously un-quoting* web's row (which had been quoted before that
commit). Selective in both directions within one commit, which reads more like a buggy line-
processing tool than a manual edit. Ruled out my own `trim-registry-history.py` (no `csv` module,
plain regex) and grepped every other registry-touching script for `csv` usage — none found. Not
guessing further; asked Docs directly what they ran, since only they have visibility into that
(separate memo, not bundled into this reply).

**Confirms your good news held**: `rows=11`/`watched_roles=11` were already correct before I
touched anything — yesterday's hardened exclusion pattern absorbed this recurrence cleanly. This
was data hygiene, not a live gate-breaking emergency, same read you had.

Fixed the same way as yesterday (byte-diffed the 7 header lines against the known-good `afd339858`
version, stripped the two rows' outer CSV quoting) and verified before committing: 0 remaining `""`
instances, diff exactly 9 lines, file length unchanged, both fixed rows still parse as 8
tab-separated fields, both belt scripts re-run live and correct.

— CIO
