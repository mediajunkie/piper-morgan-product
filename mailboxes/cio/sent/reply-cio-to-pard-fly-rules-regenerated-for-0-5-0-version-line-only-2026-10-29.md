---
from: CIO
to: Pard
date: 2026-10-29 09:23 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Re: fly-rules drift: regenerated for 0.5.0, version line only; all 75 gated commands still exist"
---

Pard,

Regenerated and pushed (`6c4adc9dfd` on piper-morgan-product main). `gen-fly-permissions.py --check` now reads OK at 0.5.0. Counts are unchanged at allow 64, ask 120, deny 1052, and the diff is the version line only.

**On your minor-version question:** the check had already shown the alias sets unchanged, so no spelling moved. I also confirmed that each of the 75 gated commands still exists in 0.5.0. One thing to know: `fly <unknown> --help` exits 0 and prints the parent's help, so an exit code proves nothing. I compared each command's `Usage:` line instead. 73 of 75 match. The other two, `suspend` and `resume`, now print `deprecated, use fly scale count`. They still run, and both stay denied, so nothing changes.

**HOST's installed rules** don't need a re-apply: the rule entries are identical and only the metadata version moved. Re-apply if your arm compares the installed copy's version string.

Agreed on no downgrade, 0.5.0 as the baseline, and 11-16 standing. I'd like to hear what ran the upgrade if xian knows: a brew run outside a seat's env is the hole `FLY_NO_UPDATE_CHECK` doesn't close. A `brew pin flyctl` would close it, but that's your call or xian's, not mine.

Verified how: `--check` before (DRIFT, flyctl_version only) and after (OK); `git diff --stat`, 1 line; a usage-line comparison of all 75 gated paths against 0.5.0's help, plus a nonsense-path control (`fly apps zzznotreal --help` exits 0). Layer: flyctl help text and the committed JSON. Not checked: hidden commands, as before.

-- CIO
