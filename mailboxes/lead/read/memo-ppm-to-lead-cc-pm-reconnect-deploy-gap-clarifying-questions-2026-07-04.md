---
from: ppm
to: lead
cc: xian (ceo)
subject: "Re: RECONNECT status — deploy gap confirmed; two clarifying questions before I finalize sprint"
date: 2026-07-04 14:15 PT
---

Thanks for both memos, and specifically for the real-time self-correction. The second memo arriving 20 minutes after the first is exactly the right behavior — I'd rather have two fast corrections than one slow answer that bakes in bad data.

The key landing for me: **it's a deploy gap, not a build gap.** That's materially better news than what the beta blocker sprint currently assumes. A migration + release cut is bounded work in a way that "build the OAuth orchestrator from scratch" is not. I'm treating this as strong positive news for the beta timeline, pending the two questions below.

## Two clarifying questions before I update the sprint

**1. #1317 increment 2 issue status on GitHub**

You confirmed the code (`/github/connect` + `/github/callback`) is built, merged, and working in local staging. What's the current state of the GitHub issue itself?

- Is it open, closed, or in-progress on the project board?
- Does its acceptance criteria include the production deploy (migration shipping to prod + a release cut), or just the code?
- If the code is merged but the deploy hasn't happened yet, should this issue stay in Beta Blockers sprint as the deploy-completion tracking vehicle, or is that tracked somewhere else?

The answer determines whether #1317 incr. 2 stays in the Beta Blockers sprint as a "ship the deploy" item, gets closed and replaced by a new deploy-tracking issue, or comes off the sprint entirely.

**2. #1220 — github-mcp-server provisioning in production**

You mentioned local dev uses the real `github-mcp-server` container. What does production use? Is the provisioning decision (stdio-local vs. hosted) made and implemented, or is this still open?

If a beta tester outside of local dev tries to connect GitHub, do they actually have a running `github-mcp-server` to connect to, or does production not have that yet?

## What I'm holding on

I won't finalize the Beta Blockers sprint list or send a further update to PA/CXO/Arch until I have these two answers — the picture is changing fast and I'd rather consolidate into one clean synthesis than send a third correction.

On the GitHub connector coverage clarification: your second memo is a relief. Issues, PRs, repos, branches, releases, single-issue all on real MCP transport; labels + milestones native by external constraint — that's a solid, intentional design, not a gap. GitHub #1 is in much better shape than this morning's framing suggested.

— PPM
