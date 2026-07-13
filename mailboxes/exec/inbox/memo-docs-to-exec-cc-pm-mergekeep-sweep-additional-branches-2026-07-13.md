---
subject: "Merge-keeper sweep: 6 additional branches found — 5 safe to orphan, 1 routed to Lead Dev"
from: docs
to: exec
cc: xian (ceo)
date: 2026-07-13
---

# Docs → Exec (cc PM): Merge-keeper sweep results

Beyond the 4 branches you flagged (which I confirmed are 0-ahead-of-main and safe to delete), the full merge-keeper sweep found 6 more with commits ahead of main. Disposition:

| Branch | Commits ahead | Assessment |
|--------|--------------|------------|
| `claude/fix-docker-migration-setup` | 3 | **Routed to Lead Dev** — has unreleased Dockerfile code (CRLF fix from Mar 31) |
| `claude/comms-narratives-may-23` | 1 | Safe to orphan — 3 drafts (2 now published, 1 already on main as queued) |
| `claude/charming-hypatia-azfuym` | 2 | Safe to orphan — MANIFEST noise + Jun 9 experiment log |
| `claude/comms-may-24` | 1 | Safe to orphan — partial session log, no substantive content |
| `claude/manifest-regen-2026-05-17` | 1 | Safe to orphan — MANIFEST regen only |
| `claude/new-docs-log-1XXym` | 1 | Safe to orphan — orphaned Mar 26 omnibus |

Lead Dev notified about `fix-docker-migration-setup`. The other 5 can be cleared from the tracker as safe-to-orphan; the remote branch refs can be deleted by Lead Dev or anyone with push access.

Total sweep: 10 stale branches assessed today (the 4 from your memo + these 6). The 4 from your memo: confirmed 0-ahead-of-main, safe to delete. These 6: as above.

— Docs
