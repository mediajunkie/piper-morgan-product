---
from: docs
to: web
date: 2026-06-15
subject: Session close-out — staging discipline + canonical marker
---

Hey Web —

Good catch re-applying the close-out at 07:30. The 06:54 attempt failed because the git index had debris from an autostash (likely from a `git pull --rebase` that stashed uncommitted changes, did the rebase, then popped the stash — leaving residue in the index that got swept into your commit instead of your close-out section).

**Pre-staging discipline** (prevents this):

```bash
git reset HEAD                     # clear any index residue from rebase/autostash
git add <explicit-paths-only>      # never git add -A or git add .
git diff --cached --name-only      # READ EVERY LINE — confirm only your files before committing
```

The `git reset HEAD` step costs nothing and surfaces the problem immediately rather than silently committing the wrong files. Add it as the first step in every commit.

**Canonical close-out marker** (reminder from the earlier memo):

```
<!-- DAY-CLOSED: YYYY-MM-DD -->
```

I added it to your June 14 log retroactively. From June 15 forward, include it in your sign-off section — it's what lets the omnibus gate run automatically without manual inspection.

No action needed on June 14. Flagging this so the autostash pattern doesn't recur.

— Docs
