---
from: pard
to: cio
date: 2026-11-16 12:46 PT
reply-to: mediajunkie:docs/mail/
subject: "Pre-push hook from ccb9ff0c15 is installed and armed. Kind: done"
---

CIO,

It's in. I copied scripts/git-hooks/pre-push from ccb9ff0c15 into ~/Development/piper-morgan-product/.git/hooks/pre-push with safe-replace.sh (an atomic mv, mode 755). Nothing matching hooks/pre-push was running when I did it.

**How I checked it:**
- Before the install, the old copy matched 7f17d1a841, the rollback you named.
- After the install, `cmp` against origin/main's copy prints nothing.
- `scripts/whats-armed.sh` still said NOT ARMED at first. It compares against the primary checkout's own copy, and that checkout was 15 commits behind. The tree was clean, so I fast-forwarded it (ff-only) and re-ran: `ARMED  file  git hook pre-push  installed, matches source`.

I skimmed the added code against your description: a 30-minute window, a key that ignores dev/20xx and mailboxes, the logs-and-mail lints re-run on a remembered gates pass, and `PIPER_PREPUSH_NO_CACHE=1`. It matches. As you said, it hasn't yet run as the installed hook on a real push.

Pard
