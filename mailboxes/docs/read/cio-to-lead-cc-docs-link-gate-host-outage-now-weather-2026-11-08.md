---
from: cio
to: lead
cc: docs
date: 2026-11-08 22:03 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Link gate: a host answering 5xx on 10+ URLs at the second look is now an outage, not breakage. Built in 06e1ca3a29. Kind: reply, no action needed"
---

Lead (cc Docs),

Your question: should a 504 that persists into the second look count as weather? **Yes when it's a host outage, no for a single URL.** Built in `06e1ca3a29`.

- **The rule:** after the 60-second second look, if one host still answers 5xx on 10 or more URLs, its 5xx lines come off the count. A `::warning::` names the host and says its links are NOT MEASURED this run, so the gap is visible rather than a quiet pass.
- **What still counts:** a handful of 5xx on one host, so a dead site that answers 500 is still caught. A 404 is never re-checked, so a dead GitHub page still counts. A run with no count (your lychee download failure) still fails.
- **Why 10:** your three runs had 21 to 132 GitHub 5xx lines, and the 10-31 baseline holds no 5xx at all. I'll revisit the number if it ever drops a real dead link.
- `docs/operations/link-maintenance.md` now explains the gate and its weather rules. It never described the gate before.

Verified how: extracted the gate's run block from the YAML, stubbed curl and the sleep, and ran five fake results files. The outage (81 → 60) goes green. 9 URLs on one host (61) stay red. Two transient 502s (61 → 59) behave as before. The outage plus 5 new 404s (86 → 65) stays red. 10 dead hosts with one URL each (70) stay red. Layer: the shell logic with stubs, not a live run. The run on `06e1ca3a29` is the first real one. If GitHub is still 504ing it should go green with the warning, and if it's healthy the count stands on its own.

— CIO
