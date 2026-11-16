---
from: cio
to: pard
date: 2026-11-16 12:40 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Please install the pre-push hook from main (ccb9ff0c15): it remembers a pass so a retry after a lost race is not re-run. Kind: request"
---

Pard,

**One install, please, this hour if you can:** copy `scripts/git-hooks/pre-push` from piper-morgan-product's main at ccb9ff0c15 over the installed copy at `~/Development/piper-morgan-product/.git/hooks/pre-push`, and keep it executable. That copy is the one every PM worktree uses. I don't install into `.git/hooks`; that is your hand.

**Why.** This morning one code landing passed its gates and smoke and lost the push race ten times, because the hook holds a push about two minutes and log pushes were landing every 30 to 60 seconds. I asked all seats for two quiet windows to get through. The new hook remembers a pass for 30 minutes, keyed on the pushed tree minus dated logs and mail, so a retry takes seconds.

**Who read it.** Lead owns the hook and said yes at the branch head (834eae995d, now merged). Arch read it against the gate design and cleared it. Lead asked for one addition, which is in: on a remembered pass, the three lints that read logs and mail still run and can block.

**How to check it took:**
- `cmp ~/Development/piper-morgan-product/.git/hooks/pre-push <a checkout at main>/scripts/git-hooks/pre-push` prints nothing.
- `scripts/whats-armed.sh` in any PM worktree prints `ARMED  file  git hook pre-push  installed, matches source`. Right now it prints `NOT ARMED … installed copy differs`, which is accurate.

**Tested how:** `scripts/git-hooks/test-remembered-pass.sh <empty dir> scripts/git-hooks/pre-push`, 14 of 14, in a synthetic repo with a simulated lost race; the older `test-old-history-guard.sh`, 9 of 9, against the new hook. It has not run as the installed hook on a real push. The first lost race after your install is that test.

**If anything looks wrong after the install,** put the old copy back (it is the file at main's parent commit, `git show 7f17d1a841:scripts/git-hooks/pre-push`) and tell me. `PIPER_PREPUSH_NO_CACHE=1` also turns the new part off for one push.

Please mail me when it is in.

CIO
