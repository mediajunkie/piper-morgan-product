# Merge-Keeper Sweep — 2026-07-19 10:05 PDT

**Mode**: DRY-RUN
**Branches considered**: 6

## Summary

| Action | Count |
|---|---|
| escalate | 6 |

## Per-branch detail

### claude/charming-hypatia-azfuym

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 929.4h ago
- **Diff**: 19 files, +218 -45
- **Conflict**: merge-tree reports conflicts against main

### claude/comms-may-24

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 1347.5h ago
- **Diff**: 3 files, +32 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/comms-narratives-may-23

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 1357.5h ago
- **Diff**: 5 files, +242 -0
- **Conflict**: merge-tree reports conflicts against main

### claude/fix-docker-migration-setup

- **Action**: escalate
- **Reason**: diff contains files matching escalation patterns
- **Last commit**: 2632.7h ago
- **Diff**: 58 files, +4836 -63
- **Blob/pattern warnings**:
  - escalation pattern matched: mailboxes/.DS_Store
  - escalation pattern matched: mailboxes/cio/.DS_Store
  - escalation pattern matched: mailboxes/lead/.DS_Store
  - escalation pattern matched: mailboxes/pa/.DS_Store
  - escalation pattern matched: mailboxes/pa/inbox/.DS_Store

### claude/manifest-regen-2026-05-17

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 1527.8h ago
- **Diff**: 20 files, +161 -128
- **Conflict**: merge-tree reports conflicts against main

### claude/new-docs-log-1XXym

- **Action**: escalate
- **Reason**: merge would conflict against main
- **Last commit**: 2666.7h ago
- **Diff**: 1 files, +53 -0
- **Conflict**: merge-tree reports conflicts against main

## Escalation queue (Docs to review)

- `claude/charming-hypatia-azfuym` — merge would conflict against main
- `claude/comms-may-24` — merge would conflict against main
- `claude/comms-narratives-may-23` — merge would conflict against main
- `claude/fix-docker-migration-setup` — diff contains files matching escalation patterns
- `claude/manifest-regen-2026-05-17` — merge would conflict against main
- `claude/new-docs-log-1XXym` — merge would conflict against main

---

## Docs assessment (2026-07-19, ~13:30 PDT)

**7/13–7/16 window** (CIO-requested): **CLEAR.** No branches from that period in the escalation set. All work from that window is on `origin/main`. ✓

**Per-branch review**:

| Branch | Age | Content | In main? | Recommendation |
|--------|-----|---------|----------|----------------|
| `claude/new-docs-log-1XXym` | 111 days | `2026-03-26-omnibus-log.md` (1 file) | ✓ EXISTS on main | Safe to delete |
| `claude/manifest-regen-2026-05-17` | 64 days | MANIFESTs only | ✓ All superseded | Safe to delete |
| `claude/charming-hypatia-azfuym` | 38 days | Experiment log (Jun 9) + MANIFESTs | Superseded | Safe to delete |
| `claude/comms-may-24` | 56 days | May 24 comms session log stub (incomplete) + 1 cc memo | Not in main | Low value (stub); safe to delete |
| `claude/comms-narratives-may-23` | 56 days | May 23 session log, old calendar, 3 drafts | All in main (incl. critical-vs-commodity via published/) | Safe to delete |
| `claude/fix-docker-migration-setup` | 110 days | Dockerfile + 15+ March-30 session logs + .DS_Store | Partially unclear | **Needs PM review** — old content, .DS_Store blocker |

**Summary**: 5 branches can be safely deleted (content in main or low value). 1 needs PM attention (`fix-docker-migration-setup`). PM may authorize branch deletions via `git push origin --delete <branch>`.

**Action requested**: PM to confirm delete authorization for the 5 safe branches, and advise on `fix-docker-migration-setup` (delete or investigate Dockerfile contents first).
