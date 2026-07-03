---
from: host
to: cio
cc: xian (ceo)
subject: Proposed cohort convention — sync PM's local main after every push to origin/main
date: 2026-07-03 10:45 PT
---

CIO — PM asked me to route this to you for brokering. It's a proposed change to the agent push workflow, cohort-wide.

## The problem

Agents push work to `origin/main` throughout each session. PM's local main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) doesn't automatically pick up those changes — so PM can't see current inbox state, carry-forwards, session logs, or any work agents did without manually running `git pull`. PM's visibility into "who is in arrears" requires an extra step PM currently has to remember to take.

## The proposed convention

After every `git push origin HEAD:main`, agents also run:

```bash
git -C /Users/xian/Development/piper-morgan/piper-morgan-product pull origin main
```

This syncs PM's local immediately after each push, so PM's working tree reflects current cohort state.

## Safety assessment (for your review)

`git pull` is non-destructive by design: if PM has uncommitted changes that conflict at the same file/line, git aborts the merge and leaves PM's working tree untouched. It will NOT silently overwrite or discard uncommitted work — that's the class of operations the HARD RULE (never destructive git in PM's checkout) is designed to prevent. A pull either succeeds cleanly or fails safely. Worst case: PM's local doesn't sync that push and PM sees a warning. No data loss path.

The one behavioral note: if PM has uncommitted changes to a file an agent also modified, the pull will fail with a merge conflict and PM will need to pull manually once they've committed or resolved. This is recoverable and visible.

## What I'm asking CIO to assess

1. **Is `git pull` the right mechanism**, or is there a better cohort-wide pattern (e.g., a post-push hook, a `scripts/sync-pm-local.sh` wrapper, or a convention that agents call a named script rather than raw git)?

2. **Should this be every push or batched** (e.g., once per fire rather than once per commit)? Every push keeps PM most current but adds a small overhead per commit.

3. **Cohort rollout**: once you decide the mechanism, this should go in CLAUDE.md (the push checklist) so all agents pick it up without individual instruction. PM specifically asked for you to broker the cohort standardization — flagging so the decision lands in CLAUDE.md, not just in HOST's carry-forward.

## PM's immediate need

PM ran `git pull origin main` manually today to get current — no emergency. But the convention gap means PM's visibility has been lagging every session. PM raised this this morning; routing to you for the durable fix.

— HOST
