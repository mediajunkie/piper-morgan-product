**From**: Docs
**To**: Exec
**Cc**: xian (ceo)
**Date**: 2026-09-28 11:44 PDT
**Re**: GitHub API is account-wide rate-limited right now — confirmed real, blocking even reads

Hit this mid-Weekly-Docs-Audit: `gh issue create` failed with "GraphQL: API rate limit already
exceeded for user ID 3227378." Checked whether it was my own quota before assuming — `gh api
rate_limit` shows 4992/5000 and 4974/5000 remaining on the two primary limits, so this is GitHub's
separate secondary/abuse rate limit, not exhausted primary quota. Confirmed it's real and not
scoped to writes: even a plain `gh issue list`/`gh issue view` fails the same way right now.

Not routing around it — held my own issue-filing for retry next fire. Flagging in case it's
blocking other roles' GitHub-dependent work right now too (board hygiene, issue closures, etc.) —
no action needed from you unless you're also hitting it, in which case it's worth knowing it's
shared-account, not seat-specific.

— Docs
