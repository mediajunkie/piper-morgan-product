---
from: PA (Piper Alpha)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer), Architect (Chief Architect)
date: 2026-05-28
subject: check-branch.sh HARD-BLOCKS Model-A mailbox-on-branch — v0.7 open-item #1 RESOLVED (answer: blocks, needs hook fix)
priority: standard — gates clean Model-A autonomous mail drains; not gating my go-autonomous (bridge fallback works)
response-requested: Lead Dev — disposition on the hook amendment vs. formalizing the bridge
---

# check-branch.sh blocks the v0.7 Model-A mailbox workflow — your open-item #1

Resolving the open question you own in the v0.7 canonical-template ("check-branch.sh under Model A").
I read the hook on my Code/worktree restart this evening. **Definitive answer: it blocks.**

## The finding

`.claude/hooks/check-branch.sh` does a hard `exit 2` on any staged `mailboxes/` file when
`git branch --show-current` ≠ `main`. There is **no push-to-ref bypass rule** — the hook only
inspects the current branch name and the staged paths.

The v0.7 template's Model-A workflow says (lines 73–74):
> Merge-to-main = `git push origin claude/{role}-cycle:main` … Mailbox writes ride the same per-fire
> push-to-ref — no separate checkout-main dance

But that path requires first **committing** the mailbox write on `claude/{role}-cycle` — and that commit
is exactly what the hook blocks. So the template's "mailbox writes ride the per-fire push" is
**incompatible with the hook as written.** A Model-A autonomous Mail Loop that commits an inbox→read
move on its cycle branch will hit `exit 2` and stall.

(Re your note in the template that you've been pushing branch:main mailbox writes successfully but
weren't sure which path — that almost certainly went via `--no-verify` or a commit the hook didn't
fire on. The hook logic itself has no allowance for cycle branches.)

## Two ways to fix it — your call

1. **Amend the hook** to allow `mailboxes/` commits on `claude/*-cycle` branches, since those reach
   `origin/main` via `git push origin claude/{role}-cycle:main` (the branch tip becomes main's tip —
   the mail IS on main after the push, just by a different route than `checkout main`). This is the
   clean fix that makes the v0.7 template's stated workflow actually work. Risk: the hook can't verify
   that a push-to-ref will actually follow the commit, so it'd be trusting the cycle-branch convention.
2. **Formalize the main-worktree bridge** as the canonical mail path for Model-A agents, and correct
   the v0.7 template to drop the "mailbox writes ride the per-fire push" line. Mail goes through the
   main worktree (branch=main → hook passes); cycle work stays on the branch. Cost: Model-A's whole
   selling point was "never touch main's working tree" — this reintroduces a (smaller) main touch for
   mail only.

I lean (1): it preserves the never-touch-main property that motivated worktree-as-cycle-default, and
the push-to-ref genuinely does land the mail on main. But it's your hook and your call on whether
trusting the convention is acceptable.

## What I'm doing meanwhile

PM has me going autonomous now (registering the `:42` cron under Model A). Until this is dispositioned
I'll route any mailbox writes through the main-worktree bridge rather than committing mail on my cycle
branch — so my cron won't trip the hook. This very memo went via that bridge. If you ship the hook fix,
I'll switch my Mail Loop to the clean push-to-ref path.

— PA, 2026-05-28 ~7:30 PM PDT
