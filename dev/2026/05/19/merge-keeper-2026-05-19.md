# Merge-Keeper Sweep — 2026-05-19 20:57 PDT

**Mode**: DRY-RUN
**Branches considered**: 17

## Summary

| Action | Count |
|---|---|
| escalate | 5 |
| merged | 6 |
| skip-active | 6 |

## Per-branch detail

### claude/cio-duty-cycle-2026-05-17

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 47.8h ago
- **Diff**: 7 files, +550 -132
- **Conflict**: merge-tree reports conflicts against main

### claude/cio-duty-cycle-2026-05-18

- **Action**: skip-active
- **Reason**: last commit 23.4h ago (< 24h threshold) — likely active session
- **Last commit**: 23.4h ago

### claude/comms-draft-blog-post-skill

- **Action**: merged
- **Reason**: wrapped (104.6h since last commit), 3 files / +308 -1, no escalation patterns, no conflicts
- **Last commit**: 104.6h ago
- **Diff**: 3 files, +308 -1

### claude/comms-editorial-may-17

- **Action**: merged
- **Reason**: wrapped (36.6h since last commit), 11 files / +133 -0, no escalation patterns, no conflicts
- **Last commit**: 36.6h ago
- **Diff**: 11 files, +133 -0

### claude/comms-family-resemblance-prep

- **Action**: merged
- **Reason**: wrapped (70.9h since last commit), 3 files / +181 -12, no escalation patterns, no conflicts
- **Last commit**: 70.9h ago
- **Diff**: 3 files, +181 -12

### claude/comms-may-18

- **Action**: skip-active
- **Reason**: last commit 13.6h ago (< 24h threshold) — likely active session
- **Last commit**: 13.6h ago

### claude/comms-narratives-may-19

- **Action**: skip-active
- **Reason**: last commit 13.5h ago (< 24h threshold) — likely active session
- **Last commit**: 13.5h ago

### claude/continue-previous-session-DuHsl

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 54.6h ago
- **Diff**: 4 files, +71 -1
- **Conflict**: merge-tree reports conflicts against main

### claude/docs-duty-cycle-2026-05-18

- **Action**: skip-active
- **Reason**: last commit 20.9h ago (< 24h threshold) — likely active session
- **Last commit**: 20.9h ago

### claude/fix-docker-migration-setup

- **Action**: escalate
- **Reason**: diff contains files matching escalation patterns
- **Last commit**: 1179.5h ago
- **Diff**: 58 files, +4836 -63
- **Blob/pattern warnings**:
  - escalation pattern matched: mailboxes/.DS_Store
  - escalation pattern matched: mailboxes/cio/.DS_Store
  - escalation pattern matched: mailboxes/lead/.DS_Store
  - escalation pattern matched: mailboxes/pa/.DS_Store
  - escalation pattern matched: mailboxes/pa/inbox/.DS_Store

### claude/host-duty-cycle-2026-05-18

- **Action**: skip-active
- **Reason**: last commit 14.4h ago (< 24h threshold) — likely active session
- **Last commit**: 14.4h ago

### claude/interesting-goodall-c5535c

- **Action**: merged
- **Reason**: wrapped (205.9h since last commit), 2 files / +239 -0, no escalation patterns, no conflicts
- **Last commit**: 205.9h ago
- **Diff**: 2 files, +239 -0

### claude/manifest-regen-2026-05-17

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 74.7h ago
- **Diff**: 20 files, +161 -128
- **Conflict**: merge-tree reports conflicts against main

### claude/new-docs-log-1XXym

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 1213.5h ago
- **Diff**: 1 files, +53 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/skunkworks-byoc-coordination

- **Action**: merged
- **Reason**: wrapped (61.2h since last commit), 1 files / +261 -0, no escalation patterns, no conflicts
- **Last commit**: 61.2h ago
- **Diff**: 1 files, +261 -0

### claude/suspend-compaction-hook-emUDP

- **Action**: merged
- **Reason**: wrapped (74.7h since last commit), 1 files / +1 -10, no escalation patterns, no conflicts
- **Last commit**: 74.7h ago
- **Diff**: 1 files, +1 -10

### claude/tender-aryabhata-2aab8b

- **Action**: skip-active
- **Reason**: last commit 13.5h ago (< 24h threshold) — likely active session
- **Last commit**: 13.5h ago

## Escalation queue (Docs to review)

- `claude/cio-duty-cycle-2026-05-17` — merge would conflict against main
- `claude/continue-previous-session-DuHsl` — merge would conflict against main
- `claude/fix-docker-migration-setup` — diff contains files matching escalation patterns
- `claude/manifest-regen-2026-05-17` — merge would conflict against main
- `claude/new-docs-log-1XXym` — merge would conflict against main
