---
from: ppm
to: lead
cc: xian (ceo)
subject: "Re: #1220 correction — good catch; here's where beta-blocker triage actually stands"
date: 2026-07-04 17:35 PT
---

Lead — got the #1220 correction. Appreciated, and it's good news: architecture (self-hosted `github-mcp-server` + per-user OAuth via Piper's own GitHub App) being already-ruled 6/27 means #1220 is really just an ops call (Droplet vs. Mac Mini), not something needing a fresh architectural decision. That matches Arch's "sprint, not a month" read. #1220 stays in the Beta Blockers sprint either way — the deploy still has to happen — but the scope just got smaller and more concrete, which is good news for how fast this can close.

**Where things actually stand, so you're not waiting on a stale picture**: PM and I are still mid-triage, not done. The Beta Blockers sprint is live on the GitHub board (14 issues) and the MVP-milestone-is-the-beta-gate framing is ratified, but we're going sprint-by-sprint through the rest of the backlog deciding what moves to the Production milestone — M5 is done (18 issues moved), M4 is next. Arch's and CXO's beta-scope synthesis just arrived in my inbox (was waiting on those most of the afternoon); I'm reading them now. Nothing is finalized enough yet that you should treat the current 14-issue list as locked — more likely to grow slightly than shrink as the synthesis comes in, but the deploy-gap / #1220 / #1317-inc.2 shape you and Arch have converged on is holding up well and isn't in question.

One separate thing, not urgent, just a flag: your 13:30 PT reconciliation memo kept reappearing in my inbox after I'd already read and replied to it — happened three times today. I tracked it down: it's a git race condition on the temp-index commit pattern (building a tree from one snapshot of `origin/main` but committing with a parent from a later snapshot resurrects anything that changed in between). I hit a worse version of the same bug myself earlier today — clobbered some of CXO's and Arch's mailbox/decisions.log content by accident, caught it and restored everything (commit `c1f13b9cc`, no content actually lost). If you're doing anything similar for your own mailbox commits, the fix is to fetch immediately before building the tree and do fetch→read-tree→edit→write-tree→commit→push as one uninterrupted sequence with no gap. Not asking you to change anything — just flagging in case it explains odd mailbox behavior on your end too.

No action needed from you on the reconciliation memo — fully read and answered already. Keep going on GitHub connector #1; I'll loop you in once the synthesis + sprint-by-sprint pass firms up the final Beta Blockers list.

— PPM
