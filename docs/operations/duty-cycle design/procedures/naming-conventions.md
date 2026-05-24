# Naming Conventions — duty cycle artifacts

**Locked**: 2026-05-24 ~13:00 PT per PM directive ("define a convention now eventually for all agents, yes")
**Scope**: cohort-wide; applies to any role adopting the v0.5 duty cycle

---

## Per-agent docs

| Doc | Path | Notes |
|---|---|---|
| **Session log** (existing convention) | `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{role-slug}-log.md` | Detailed turn-by-turn record. One per role per session. Already cohort-canonical. |
| **Daily tracker** (Doc 1; new under v0.5) | `dev/YYYY/MM/DD/{role-slug}-tracker-YYYY-MM-DD.md` | At-a-glance current state + day's primary agenda. Renewed daily. NOT duplicative with session log. |
| **Task list** (Doc 2; reframed under v0.5) | `dev/active/{role-slug}-standing-items.md` | Per-agent task list of record. Persists across days. Reframes existing "standing-items tracker" pattern; no parallel new doc. |
| **Attention doc** (Doc 3; reframed under v0.5) | `dev/active/duty-cycle-escalations-{role-slug}.md` | Items for PM to scan during IDLE. Reframes existing "escalations" pattern; no parallel new doc. |

## Cycle / branch / worktree (post-V1-retirement)

| Surface | Convention | Notes |
|---|---|---|
| **Cycle branches** | NOT NEEDED under v0.5 | V3-era `claude/{role}-duty-cycle-YYYY-MM-DD` pattern retired. Cycle runs in agent's current session/branch. |
| **Substantive work worktrees** | Per existing CLAUDE.md "Worktree-default for substantive sessions" guidance | Cycle work IS substantive — uses normal worktree-default discipline. |

## Mailbox (existing; unchanged)

- Inbox: `mailboxes/{role-slug}/inbox/{memo-filename}.md`
- Read: `mailboxes/{role-slug}/read/{memo-filename}.md`
- Sent: `mailboxes/{role-slug}/sent/{memo-filename}.md`
- Memo filenames per existing convention: `memo-{from-slug}-to-{to-slug}-cc-{cc-slugs}-{subject-slug}-YYYY-MM-DD.md`

## Role-slug values (canonical)

Per `docs/briefing/ROSTER.md`:
- `cio`, `host`, `docs`, `exec`, `cxo`, `ppm`, `comms`, `pa`, `arch`, `lead`, `xian (ceo)`

Note: `xian (ceo)` has a literal space + parens in the directory name for PM's mailbox.

## Cross-references

- v0.5 design: `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md` (Three per-agent docs section)
- `start.md`: references this file for new-log + new-tracker creation paths
- `procedures/*.md`: all procedure docs reference these paths
- CLAUDE.md mailbox-discipline norms

---

*Conventions locked 2026-05-24 ~13:00 PT. Cohort-wide; applies at adoption time for any role.*
