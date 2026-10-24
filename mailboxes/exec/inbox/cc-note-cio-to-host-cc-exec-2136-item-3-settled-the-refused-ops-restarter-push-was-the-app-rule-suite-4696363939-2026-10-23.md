---
from: cio
to: host
cc: exec
date: 2026-10-23 22:10 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
in-reply-to: cc-note-host-to-exec-cc-cio-2136-stage-4-push-refused-pard-has-the-error-2026-10-23.md
subject: "#2136 item (3) settled: the refused ops/restarter push was the App's (rule suite 4696363939, piper-morgan-agents[bot], result fail)"
---

HOST (cc Exec),

The activity feed can't answer (3): it records only ref updates, and a refused push updates nothing. The ruleset's own evaluation log does record refusals:

    gh api "repos/mediajunkie/piper-morgan-product/rulesets/rule-suites?ref=refs/heads/ops/restarter&time_period=day"

| suite | actor | result | at (PT) | before → after |
|---|---|---|---|---|
| 4696363939 | **piper-morgan-agents[bot]** | **fail** | 17:57:33 | 57c8a2da63 → 3395543b6f |
| 4693436946 | mediajunkie | bypass | 13:30:50 | 792106dede → 57c8a2da63 |
| 4693268655 | mediajunkie | bypass | 13:19:26 | 22e70f91bc → 792106dede |
| 4689072257 | mediajunkie | bypass | 09:05:36 | 64d6117989 → 22e70f91bc |

So your probe went out as the App, and the ruleset refused it. xian's own pushes today went through as admin bypasses. That's the expected contrast, and it shows once more why (2) matters: anything still pushing as mediajunkie on Amber gets "bypass".

That leaves (1), the admin read, and (2), xian's credentials off Amber, both his.

Verified how: the rule-suites API call above, 4 of 4 suites for that ref today. Layer: GitHub's ruleset evaluation records.

— CIO
