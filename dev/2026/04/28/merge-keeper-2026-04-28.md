# Merge-Keeper Sweep — 2026-04-28 09:27 PDT

**Mode**: DRY-RUN
**Branches considered**: 4

## Summary

| Action | Count |
|---|---|
| escalate | 2 |
| merged | 1 |
| skip-active | 1 |

## Per-branch detail

### claude/evaluate-context-hub-7CBKi

- **Action**: merged
- **Reason**: wrapped (1143.8h since last commit), 1 files / +102 -0, no escalation patterns, no conflicts
- **Last commit**: 1143.8h ago
- **Diff**: 1 files, +102 -0

### claude/fix-docker-migration-setup

- **Action**: escalate
- **Reason**: diff contains files matching escalation patterns
- **Last commit**: 664.0h ago
- **Diff**: 58 files, +4836 -63
- **Blob/pattern warnings**:
  - escalation pattern matched: mailboxes/.DS_Store
  - escalation pattern matched: mailboxes/cio/.DS_Store
  - escalation pattern matched: mailboxes/lead/.DS_Store
  - escalation pattern matched: mailboxes/pa/.DS_Store
  - escalation pattern matched: mailboxes/pa/inbox/.DS_Store

### claude/new-docs-log-1XXym

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 698.0h ago
- **Diff**: 1 files, +53 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/phase-f-flag-flip

- **Action**: skip-active
- **Reason**: last commit 0.5h ago (< 24h threshold) — likely active session
- **Last commit**: 0.5h ago

## Escalation queue (Docs to review)

- `claude/fix-docker-migration-setup` — diff contains files matching escalation patterns
- `claude/new-docs-log-1XXym` — merge would conflict against main
