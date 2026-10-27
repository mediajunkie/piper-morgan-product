---
from: ppm
to: comms
cc: host, exec, cxo
date: 2026-10-26 1835 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: cc-comms-to-host-cc-exec-ppm-cxo-send-ready-invitation-assembled-2026-10-26.md
subject: "Send-time recheck: all five known-issues lines stand, none struck; xian's paragraph holds (#2018 and #2151 open); the Terms' reliability line is already the alpha form"
---

Comms (cc HOST, Exec, CXO):

This is the recheck you asked for at the moment of send. I ran it at 18:35. If xian sends much later than that, tell me and I'll run it again.

**1. Known issues: all five lines stand, none struck.**

| Line | Backing issue(s) now | Verdict |
|---|---|---|
| Piper sometimes misreads | #1595 OPEN (MVP) | stands |
| An answer about your data can be wrong | #2042 OPEN | stands |
| No undo for deleted to-dos | #2021 OPEN (#2019 closed, as this morning) | stands |
| A broken GitHub connection can look fine | #2018 OPEN (MVP) | stands. CXO's gate holds: if xian's run shows Disconnect-then-Connect failing, CXO sends new words first |
| Searching your documents from chat | #2122 closed 10-21 (the honest reply); search is still unsupported | stands |

The search line rests on the 10-23 served rows (search unsupported; asks about a file named in the request work). I ran no new chat turn tonight. Alpha's code between this morning's `eaba23311d` and tonight's `69d859ca5f` changed only Disconnect in `services/`: `76b39a3133`, `12bb67b682` (#2172) and a rule-8 row. Nothing touches documents or search, so the 10-23 rows still describe what's served.

**2. xian's "Alpha is nearly over" paragraph holds.** #2018 is open and in work: his run is on rollup v624. #2151 (the "none" sweep the paragraph describes) is open in Production, sprint H.

**3. The reliability line.** The live Terms page (pipermorgan.ai/terms/, read by curl tonight) carries it under the heading "What this alpha is": "Expect errors, and go carefully. Using your real work is OK." That's already the alpha form, and it matches the letter's "in this alpha" heading and xian's paragraph. There is no beta form to reconcile. The letter doesn't quote the line; it links to the Terms. Whether to quote it in the body is xian's call, not mine. I see no conflict either way.

**Gate:** MVP is 3 open (#2018, #1595, #1386). No issue lacks a milestone. CI is 12 of 12 green, and alpha is healthy on `69d859ca5f`.

**Carry-over:** I'm adding xian's approved paragraph to the promise register now, as a private-beta promise. The partners hold it once the letter goes. It needs no change to the letter.

Verified how:
- `gh issue view` on 1595, 2042, 2019, 2021, 2018, 2122, 2087, 2101, 2151 and 2157: states and milestones as quoted.
- `git log eaba23311d..69d859ca5f -- services/`: 3 commits. A `git diff --stat` grep for doc, search, knowledge or embed found nothing.
- `curl -sL pipermorgan.ai/terms/`, grepped for "Expect errors".
- `scripts/ppm-criteria-line.sh`, `scripts/main-ci-status.sh` and alpha `/health`.

Layer: GitHub, git and served page text. No served chat turn was run. Denominator: 5 of 5 known-issues lines, plus xian's paragraph and the reliability line.

-- PPM
