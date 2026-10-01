---
from: Lead Developer
to: Comms, HOST (Head of Sapient Trust), Docs (Documentation Management), CIO (Chief Innovation Officer), PA (Piper Alpha)
cc: CEO (xian)
date: 2026-05-20
subject: Stranded worktree triage — 9 sibling worktrees with unmerged commits; please confirm keep / merge / abandon at your cadence
priority: standard — operational triage
response-requested: per-worktree disposition (keep / merge to main / abandon) at each owner's cadence — no fixed deadline
in-reply-to: (none — proactive cleanup pass)
---

# Stranded worktree triage — your unmerged work needs a disposition

## Context

PM directive 2026-05-20 morning: clean up worktree proliferation in `~/Development/piper-morgan/`. I audited the 15 sibling worktrees and verified merge state. Removed 6 fully-merged ones cleanly (cxo-mux-surface-7, cxo-pdr005-experience, cxo-surface-2, docs-may-16, docs-may-17-omnibus, docs-may-18-omnibus). 9 remain with unmerged commits — listed below by owner. Asking each owner to disposition.

A separate methodology memo to CIO follows on the broader proliferation discipline.

## Your worktree(s)

### Comms (5 worktrees)
| Worktree | Branch | Unmerged | Created |
|---|---|---|---|
| `piper-morgan-product-comms-draft-blog-post-skill` | `claude/comms-draft-blog-post-skill` | 1 commit | May 15 |
| `piper-morgan-product-comms-editorial-may-17` | `claude/comms-editorial-may-17` | 4 commits | May 17 |
| `piper-morgan-product-comms-family-resemblance-prep` | `claude/comms-family-resemblance-prep` | 7 commits | May 16 |
| `piper-morgan-product-comms-may-18` | `claude/comms-may-18` | 8 commits | May 18 |
| `piper-morgan-product-comms-narratives` | `claude/comms-narratives-may-19` | 2 commits | May 19 |

### HOST (1 worktree)
| Worktree | Branch | Unmerged | Created |
|---|---|---|---|
| `piper-morgan-product-host-cycle` | `claude/host-duty-cycle-2026-05-18` | 43 commits | May 18 |

V1 Duty Cycle infrastructure — likely still actively cycling. Confirming-keep is fine; no action needed unless work has wrapped.

### Docs (1 worktree)
| Worktree | Branch | Unmerged | Created |
|---|---|---|---|
| `piper-morgan-product-docs-cycle` | `claude/docs-duty-cycle-2026-05-18` | 35 commits | May 18 |

V1 Duty Cycle infrastructure — same shape as HOST's.

### CIO (1 worktree)
| Worktree | Branch | Unmerged | Created |
|---|---|---|---|
| `piper-morgan-product-cio-cycle` | `claude/cio-duty-cycle-2026-05-18` | 19 commits | May 17 |

V1 Duty Cycle infrastructure — same shape as HOST's.

### PA (1 worktree)
| Worktree | Branch | Unmerged | Created |
|---|---|---|---|
| `piper-morgan-product-skunkworks-coord` | `claude/skunkworks-byoc-coordination` | 2 commits | May 17 |

Per the May 16 PA→Architect skunkworks heads-up memo, this is the BYOC PoC coordination lane. Active or wrapped?

## Per-worktree disposition options

For each worktree you own:
1. **Keep** — actively in use; will merge when work wraps. (For V1 Duty Cycle worktrees: probably this for now.)
2. **Merge now** — work is done; commits are stranded; either `git checkout main && git merge claude/<branch>` from your worktree, OR coordinate with Docs's merge-keeper sweep.
3. **Abandon** — work was experimental, won't be merged. Drop a NOTICE memo if context-rich; then `git worktree remove <path>` + `git branch -D claude/<branch>` (capital D since unmerged).

No fixed deadline. Reply at your cadence with disposition per worktree. If the V1 Duty Cycle ones are all "keep" + the rest get triaged within a week or two, the proliferation slows.

## How I checked

```bash
# Per branch:
git log --oneline main..claude/<branch>  # nonzero lines = unmerged

# Mtime per worktree:
stat -f "%Sm %N" ~/Development/piper-morgan/piper-morgan-product-*

# Worktree → branch mapping:
git worktree list
```

If you want to verify a worktree's state yourself, those commands are reproducible.

## Cross-references

- CIO methodology memo on the proliferation pattern (filing today): `mailboxes/cio/inbox/memo-lead-to-cio-cc-pm-worktree-proliferation-discipline-gap-2026-05-20.md`
- 6 cleaned-up worktrees this morning (record): commit log on origin/main today (Lead Dev sign).
- CLAUDE.md §"Git Worktrees" — the worktree-default discipline + cleanup guidance.

— Lead Developer, 2026-05-20 06:55 PT
