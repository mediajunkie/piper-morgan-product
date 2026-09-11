# Merge-Keeper Escalation — 6 stranded `claude/*` branches need a keep-or-delete call

**From**: Docs (Documentation Management)
**To**: PM (xian)
**CC**: Lead Dev
**Date**: 2026-07-08 ~05:35 PDT
**Priority**: Low / housekeeping — **no urgency**. These branches are old and stable; nothing is at risk. This is a "clear the backlog when convenient" ask, not a blocker.

---

## Why you're getting this

The daily merge-keeper sweep has flagged the **same 6 branches** every day for weeks. They persist not because they're hard, but because no one has been asked to make the one decision that clears them: **keep (and someone rebases/resolves) or delete.** This memo consolidates them into a single pass so they stop recurring in the sweep. Full sweep log: `dev/active/merge-keeper-2026-07-08.md`.

None auto-merges — each either conflicts against `main` or carries `.DS_Store` junk. So none can be swept in automatically; they need a human call.

## The 6 branches

| Branch | Age | Diff | Why stranded |
|---|---|---|---|
| `claude/charming-hypatia-azfuym` | ~27d | 19 files, +218/−45 | conflicts vs main |
| `claude/comms-may-24` | ~45d | 3 files, +32 | conflicts vs main |
| `claude/comms-narratives-may-23` | ~45d | 5 files, +242 | conflicts vs main |
| `claude/manifest-regen-2026-05-17` | ~52d | 20 files, +161/−128 | conflicts vs main |
| `claude/new-docs-log-1XXym` | ~99d | (docs-log) | conflicts vs main |
| `claude/fix-docker-migration-setup` | ~99d | 58 files, +4836/−63 | only `.DS_Store` escalation patterns — **content may be mergeable** once junk is stripped |

## Recommendation

- **Comms branches** (`comms-may-24`, `comms-narratives-may-23`): likely superseded narrative drafts — Comms would know if any content is still wanted; otherwise **delete**. (Prior stranded-comms triage exists from May; these may already be moot.)
- **`manifest-regen-2026-05-17`** and **`new-docs-log-1XXym`**: almost certainly obsolete mechanical/log branches (MANIFEST regen + a stray docs log) — **delete** unless you recognize unique content.
- **`charming-hypatia-azfuym`**: 27d, real code diff — worth a 2-minute look before deleting; if the work matters, Lead can rebase.
- **`fix-docker-migration-setup`**: the only one whose *content* might be worth salvaging (Docker/migration setup) — the escalation is purely `.DS_Store` noise. If the Docker work is still relevant, Lead can cherry-pick the real files minus the junk; otherwise delete.

**Backstop (not a deadline)**: whenever you have a spare few minutes. If I hear nothing, the sweep keeps logging them harmlessly and I'll re-surface once more only if the list changes.

— Docs
