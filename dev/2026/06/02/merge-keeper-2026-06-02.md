# Merge-Keeper Sweep — 2026-06-02 10:44 PDT

**Mode**: DRY-RUN
**Branches considered**: 11

## Summary

| Action | Count |
|---|---|
| escalate | 6 |
| merged | 4 |
| skip-active | 1 |

## Per-branch detail

### claude/comms-cycle

- **Action**: merged
- **Reason**: wrapped (39.4h since last commit), 2 files / +55 -0, no escalation patterns, no conflicts
- **Last commit**: 39.4h ago
- **Diff**: 2 files, +55 -0

### claude/comms-may-24

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 220.1h ago
- **Diff**: 3 files, +32 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/comms-mux-voice-pass

- **Action**: merged
- **Reason**: wrapped (214.5h since last commit), 1 files / +73 -1, no escalation patterns, no conflicts
- **Last commit**: 214.5h ago
- **Diff**: 1 files, +73 -1

### claude/comms-narratives-may-23

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 230.1h ago
- **Diff**: 5 files, +242 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/continue-previous-session-DuHsl

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 380.4h ago
- **Diff**: 4 files, +71 -1
- **Conflict**: merge-tree reports conflicts against main

### claude/fix-docker-migration-setup

- **Action**: escalate
- **Reason**: diff contains files matching escalation patterns
- **Last commit**: 1505.3h ago
- **Diff**: 58 files, +4836 -63
- **Blob/pattern warnings**:
  - escalation pattern matched: mailboxes/.DS_Store
  - escalation pattern matched: mailboxes/cio/.DS_Store
  - escalation pattern matched: mailboxes/lead/.DS_Store
  - escalation pattern matched: mailboxes/pa/.DS_Store
  - escalation pattern matched: mailboxes/pa/inbox/.DS_Store

### claude/host-cycle

- **Action**: skip-active
- **Reason**: last commit 16.5h ago (< 24h threshold) — likely active session
- **Last commit**: 16.5h ago

### claude/interesting-goodall-c5535c

- **Action**: merged
- **Reason**: wrapped (214.7h since last commit), 4 files / +474 -0, no escalation patterns, no conflicts
- **Last commit**: 214.7h ago
- **Diff**: 4 files, +474 -0

### claude/manifest-regen-2026-05-17

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 400.5h ago
- **Diff**: 20 files, +161 -128
- **Conflict**: merge-tree reports conflicts against main

### claude/new-docs-log-1XXym

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 1539.3h ago
- **Diff**: 1 files, +53 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/suspend-compaction-hook-emUDP

- **Action**: merged
- **Reason**: wrapped (400.5h since last commit), 1 files / +1 -10, no escalation patterns, no conflicts
- **Last commit**: 400.5h ago
- **Diff**: 1 files, +1 -10

## Escalation queue (Docs to review)

- `claude/comms-may-24` — merge would conflict against main
- `claude/comms-narratives-may-23` — merge would conflict against main
- `claude/continue-previous-session-DuHsl` — merge would conflict against main
- `claude/fix-docker-migration-setup` — diff contains files matching escalation patterns
- `claude/manifest-regen-2026-05-17` — merge would conflict against main
- `claude/new-docs-log-1XXym` — merge would conflict against main
