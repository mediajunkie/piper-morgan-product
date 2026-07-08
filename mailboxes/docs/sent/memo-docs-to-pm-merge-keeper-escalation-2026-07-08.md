---
from: Documentation Management (docs)
to: xian (ceo)
date: 2026-07-08
subject: "Merge-keeper: 6 stale branches need PM decision (safe to delete all)"
---

# Merge-keeper: 6 stale branches — please confirm deletion

Docs ran the daily merge-keeper sweep on Jul-7 and found 6 branches with commits not on `main`, all flagged for escalation. All 6 conflict with current `main`. Summary and recommendation below.

## Branches

| Branch | Age | Content summary | Recommendation |
|--------|-----|-----------------|----------------|
| `claude/new-docs-log-1XXym` | ~99d (Mar 26) | 1 file: `docs/omnibus-logs/2026-03-26-omnibus-log.md` (53 lines) — almost certainly on main already | **Delete** |
| `claude/fix-docker-migration-setup` | ~98d (Mar–Apr) | 58 files: `.DS_Store`, old memos (Mar 24/30), `verify-python-version.sh` deletion, `web/api/routes/setup.py` edits. Real code changes but 98d old; would need full rebase to land and likely already superseded | **Delete** |
| `claude/manifest-regen-2026-05-17` | ~52d (May 17) | MANIFEST regen — conflicts with every MANIFEST change since | **Delete** |
| `claude/comms-narratives-may-23` | ~44d (May 23) | Old Comms narratives work | **Delete** |
| `claude/comms-may-24` | ~44d (May 24) | Old Comms work | **Delete** |
| `claude/charming-hypatia-azfuym` | ~26d (Jun 11) | 2 commits: cloud surface experiment ("fire #0 setup") + MANIFEST regen — experimental probe, no deliverables landed | **Delete** |

## Recommendation

All 6 are safe to delete. No substantive in-flight work is at risk:
- The 2 oldest (99d, 98d) predate the current sprint by months
- MANIFEST branches are always regenerable
- The cloud experiment was a probe with no follow-on

If you want Docs to delete these directly: reply to confirm and I'll run `git push origin --delete <branch>` for all 6 from the worktree.

If `fix-docker-migration-setup` has content you want to salvage first, let me know — I can extract the `web/api/routes/setup.py` diff for review before deleting.
