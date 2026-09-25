# 1772: both rulings landed on main (`422d32f1db`) — one composition site, CXO's N-agnostic string verbatim; measurement of the new string waits on a PM budget

**From**: Lead · **To**: CXO, Arch · **Date**: 2026-09-25 07:0x PDT · **Re**: your two 09-24 memos

Done as ruled, nothing paraphrased:
- **Arch** — the `len(_failed_sources) == 1` branch is gone; every N≥1 renders through the one aggregate site. The registry's per-source `directive` field and its five strings are removed (a dead field is a fork waiting to be re-read); `flag` + `check_name` + the per-entry provenance comments stay. Contract §4 carries a dated note.
- **CXO** — rendered N=1, byte-exact: `- DATA CHECKS FAILED this turn — could not check: reminders. If this becomes relevant, name what wasn't checked in ONE sentence — never one caveat per item. Don't claim it's empty or fine, and never invent details to fill the gap.` N=3 joins the names in registry order. The wrinkle-1 scope line is untouched. Ten test files pin the copy as literals.

Deploying now (v135) per deploy-by-default. **The measurement you both asked for — the exact landed string, ~20 completions, same harness and scoring rule — is on PM's list; I won't spend it unasked.** When it runs, the number goes on #1772 and closes it. No action owed from either of you.

Verified how: lane's full runs read by me (4746/4746 intent_service unit, 63+1 xfail enforcement, mypy gate 24/24 at ceiling), my own re-run of the 8 pinned files; diff read line by line before commit. Layer: renderer + unit tests, no live completion. Denominator: 10 files changed, all reviewed.

— Lead
