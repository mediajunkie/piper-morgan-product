# Docs Standing Items (Task List per v0.6 Duty Cycle)

**Purpose**: durable task list per v0.6 Duty Cycle architecture (reframed standing-items = task list, per Architectural Decision 1).

**Owner**: Documentation Management (Docs)
**Last refresh**: 2026-05-27 12:05 PT — initial creation at v0.6 cycle adoption

---

## Active items

### Critical-docs YAML-frontmatter upgrade (PM-directed 2026-05-28; systematic plan, supervised subagents)

PM directive: upgrade critical docs to proper YAML frontmatter; I prompt + supervise + validate subagents. **Validated pattern** (briefing pilot, commit `b40876b87`): subagent prepends frontmatter extracting existing metadata (type/title/valid_from/last_updated from body or git first-commit date), body untouched; I validate via `git diff --numstat` (must show 0 deletions) + spot-check + confirm all start with `---`.

Schema: `type:` (briefing|methodology|adr|pattern|memory) + `title:` (from H1) + `valid_from:` + class-specific (number/status for adr/pattern/methodology; last_updated for briefing/methodology). `valid_from` ties to #972 temporal-validity.

- [x] **Briefing (17)** — DONE, validated, committed `b40876b87`
- [ ] **ADRs (69)** — uniform header (# ADR-NNN: Title + Status/date); add type/number/title/status/date/valid_from. Supervised subagent + validate.
- [ ] **Patterns (80)** — # Pattern-NNN: Name + Status (emerging/proven); add type/number/name/status/valid_from.
- [ ] **Methodology (52)** — # Methodology NN: Title + Last-updated line; add type/number/title/valid_from/last_updated.
- [ ] **.serena/memories (29)** — plain markdown, varied; add type: memory + title + valid_from (git date). Lower priority (Serena tool memory, not the #972 institutional-memory target).

Each remaining class = one supervised work-block (cron Task Loop or PM-engaged). Same validation gate.

**Watch**: confirm no line-1 parser breaks from added frontmatter. BRIEFING-CURRENT-STATE freshness hook reads the body "Last Updated" line (still present) → unaffected. Verify ADR/pattern index generators + any tooling that greps line-1 `# ` before scaling.

### Lane work

- [ ] **#1058 Template hygiene** — stale Cursor refs + staleness in agent-prompt-template + gameplan-template. Templates = Docs domain. Idle-advanceable. (Accepted from CIO triage routing 2026-05-28.)
- [ ] **#974 MEM-EVAL pilot data collection** — runs from May 26 wrap onward. Aggregate ≥3 sessions per role, target ~early June for first evaluation. Tracker doc: `docs/internal/operations/memory-eval-pilot.md`.
- [ ] **#972 MEM-TEMPORAL field-spec work** — design questions resolved 2026-05-30 (Q1 add YAML block done via May 28 pilot `b40876b87`; Q2 drop memos from scope per PM "I never asked for that"). Spec at v0.3 (`docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`). ≥3-examples AC satisfied via 17-briefing pilot. **Remaining**: (a) session-log-instructions disposition (recommend dropping by point-in-time logic, same as memos — flag for PM ratification), (b) continue YAML-frontmatter upgrade across other standing-doc classes already queued (ADRs/patterns/methodology/serena), (c) Janus alignment ping to CIO once spec firms, (d) close issue once (a) lands.

### Cycle / daily ops

- [ ] **Daily merge-keeper sweep** — Docs-owned discipline catching stranded session logs and unmerged feature-branch work within 24h. Per Sign-Off Discipline.
- [ ] **MANIFEST regen across mailboxes** — typically after mail-discipline operations; script `scripts/regenerate-mailbox-manifests.py`.
- [ ] **Omnibus log cadence** — daily synthesis for prior day per `create-omnibus` skill.

### Watch surfaces

- [ ] **Comms process-tightening proposal** — outstanding from Sun May 24 + Mon May 25 memos on orphan drafts. Comms cadence.
- [ ] **Web publish-post.js bugs** — 2 memos filed: Tue 17:50 (edit-pass mirror bug) + today (inline-image conversion gap). Web cadence.
- [ ] **HOST trust-lens input on memory-eval pilot** — at HOST cadence after pilot data accumulates (~early June).
- [ ] **Pattern README catalog refresh (#1127)** — filed today; Lead Dev + Architect lane.
- [ ] **Roadmap refresh (#1128)** — filed today; PPM lane.
- [ ] **GitHub Actions operational refactor** — Lead Dev primary; memo filed today (Architect + CIO CCs).

## Blocked items

(none currently — #972 unblocked yesterday)

## Recently completed (rolling, ~7 days)

- May 28 — CIO triage routing answered: accepted #972/#974/#1058; **redirected #973 MEM-CACHE-AUDIT → Lead Dev** (code-shaped) + **PR #941 Ted→Janus → Comms** (cross-project relay). Pickup notices filed. Commit `ee9ddcbeb`.
- May 28 — **Docs vacated on-main cron** per ratified "do not register on main"; aligned with cohort (CIO/Exec/HOST/PA). Resume = operator relaunch in `claude/docs-cycle` worktree post-mechanism. See attention doc.
- May 27 — Weekly Docs Audit #1125 closed properly with completion matrix + 2 follow-ups filed
- May 27 — Weekly Ship #044 published (blog + LinkedIn syndicated)
- May 27 — `gh` CLI access restored (symlink to `/opt/homebrew/bin/gh`)
- May 27 — GitHub Actions cron-drop forensic audit + Lead Dev memo
- May 27 — Lead Dev #1126 close-discipline lapse caught + body fixed by Docs
- May 26 — Two Migrations in One Day published + edit-pass corrected
- May 26 + 25 + 24 omnibus logs filed
- May 25 — #974 MEM-EVAL amendment landed in CLAUDE.md + HOST trust-lens FYI memo
- May 25 — #972 MEM-TEMPORAL CIO unblock memo + ratification received

---

*This file is task-list-as-standing-items per v0.6 architectural decision 1. Append/edit during cycle fires; durable across sessions; never deleted.*
