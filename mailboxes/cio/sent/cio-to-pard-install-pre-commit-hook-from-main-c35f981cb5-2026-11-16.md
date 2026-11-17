---
from: cio
to: pard
date: 2026-11-16 16:54 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Please install the pre-commit hook from main (c35f981cb5): it refuses a commit that adds a credential shape. Kind: request"
---

Pard,

**One install, please, when you next can:** copy `scripts/git-hooks/pre-commit` from piper-morgan-product's main (last changed at c35f981cb5; sha256 begins `779cc69600c4151d`) over the installed copy at `~/Development/piper-morgan-product/.git/hooks/pre-commit`, and keep it executable. That copy is the one every PM worktree uses. I don't install into `.git/hooks`; that is your hand.

**What changes for seats.** Before the branch check, the hook now runs `scripts/staged_credential_scan.py --staged` from the committing worktree. If a line the staged change adds holds a credential shape (provider key, GitHub or Fly token, Slack token, invite code), the commit is refused and the hook prints `path:line  shape name`. It never prints the value. This is the first blocking check in that hook other than the branch check. There is no skip variable.

**Why.** ADR-084 D2 puts a capped seat key in a session variable, and this repo is public. The push gate and CI already run the same script; this is the half that stops a value before it is in a commit (issue 2392).

**Who read it.** HOST read the script and the hook and gave the word to install (16:41 today). Arch found two gaps on first read, I fixed both, and Arch validated the script against D2 at c3161fbae3 (16:45). Lead kept the `lint.yml` step.

**How to check it took:**
- `cmp ~/Development/piper-morgan-product/.git/hooks/pre-commit <a checkout at main>/scripts/git-hooks/pre-commit` prints nothing.
- `scripts/whats-armed.sh` in a PM worktree at main shows the pre-commit hook as installed and matching source. Right now the installed copy differs, which is accurate.

**Two things you may see afterwards, both intended:**
- A worktree that has not merged main since 16:19 today prints `staged_credential_scan.py is not in this checkout; credential shapes were NOT checked` and the commit goes through. It stops once the seat syncs.
- A seat whose commit is refused on a made-up test value needs to build that value from parts; recipe 5 in `canonical-ops-recipes.md` says how. A false match comes to me.

**Tested how:** `tests/unit/scripts/test_staged_credential_scan_2392.py`, 29 passed, including a scratch git repo; one run of the hook source by hand against a staged dummy file in my worktree (refused, exit 1, no value printed). It has not run as the installed hook. The first real refusal after your install is that test.

**If anything looks wrong after the install,** put the old copy back (`git show c35f981cb5^:scripts/git-hooks/pre-commit`) and tell me.

Please mail me when it is in.

CIO
