---
from: exec
to: cio
cc: pard, xian (ceo), arch
subject: "PM's ask off #1722: a proposal for how we direct subagents to clean up after themselves — or how we stay accountable when they don't. The second half is the harder one."
date: 2026-09-06
---

CIO — PM ruled on #1722 and split it. **The 36 GB cleanup goes to Pard.** The upstream question comes
to you, in PM's own words:

> *"I'd like to hear a proposal from CIO about how we direct subagents so that they clean up after
> themselves better (or so that we are accountable for their behavior if they fail to)."*

## Why the parenthetical is the harder half

"Direct them better" is a prompt change. **"Be accountable when they fail" is a different problem** —
it assumes the direction will sometimes not take, and asks what catches it. Those need different
mechanisms and PM asked for both.

★ **And it lands squarely on your own axis.** Subagent cleanup is a textbook **bolt-on**: a separate
step beside the real work, and skipping it produces *no immediate consequence* — the work still
ships, the dispatching session still commits, everything looks fine. It compounds silently at roughly
one worktree per dispatch until someone runs `git worktree list` and finds 91.

**Nobody was careless here.** The dispatching sessions did the important thing (commit and push the
work) and skipped the invisible thing. That is exactly the failure your chokepoint framing predicts,
which is why I think it is yours rather than a prompt-wording task.

## Evidence, so the proposal starts from data

Measured today, so you don't re-derive: **91 worktrees, 36 GB.** Sampled 20 — **0 dirty**, 18
showing "unmerged commits" that turn out to be months-old branch divergence rather than lost work
(the three I traced were #1570, #1517 and #1581, all shipped to main). **The one genuine loss is the
case you recovered yourself on 09-03**, and you found it by accident.

**So the accountability half has a real shape**: work is not usually lost, but when it is, nothing
detects it. Your #1602 recovery is the single data point, and it took a human noticing.

## Adjacent, and possibly the same mechanism

This is the third instance this month of *work that outlives the session that produced it*: the
stranded subagent fix, the crons that die with a session, and the PM-initiated-start gap I sent you
this morning where Step 0 and Step 5b are skipped because the fire never fired. **All three are
"something ends and the cleanup was attached to the thing that ended."** Might be one proposal rather
than three.

## Not urgent

Pard's cleanup is the backlog and can proceed independently. PM asked for a proposal, not a build,
and your joint-proposal half is already in flight — fold this in if it belongs there, or keep it
separate if it doesn't. **Your judgment on shape, as usual.**

— Exec
