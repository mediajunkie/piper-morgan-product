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

- [x] **#1058 Template hygiene** — CLOSED 2026-06-15. Delivered via #1206: agent-prompt-template v10.4 + gameplan-template v9.5 (four-tier model reframe) + v9.6 (stale A.2 worktree block trim). Arch-ratified.
- [ ] **#974 MEM-EVAL pilot data collection** — runs from May 26 wrap onward. Aggregate ≥3 sessions per role, target ~early June for first evaluation. Tracker doc: `docs/internal/operations/memory-eval-pilot.md`.
- [ ] **#972 MEM-TEMPORAL field-spec work** — Spec at **v0.4** (`docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`, `c9dea12c8` 2026-06-15). Schema: `valid_from`+`last_verified` (expected) + `valid_until`+`superseded_by` (optional). Janus alignment incorporated. **P2 remaining**: (a) session-log-instructions disposition (PM ratification needed — recommend drop by point-in-time logic), (b) briefings `last_verified` stamp (as-touched, not bulk), (c) ADRs/patterns/methodology opportunistic YAML upgrade (ongoing), (d) `valid_until` vs `ended` pending PM bridge to Daedalus; (e) close issue once (a) resolves.

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

- Jun 15 — **#1206 all 3 items closed**: gameplan-template v9.5/v9.6 + agent-prompt-template v10.4 (four-tier model + A.2 trim); Arch-ratified
- Jun 15 — **#972 MEM-TEMPORAL spec v0.4** shipped (`c9dea12c8`); field-names reconciled with CIO schema
- Jun 15 — **Layer C pre-commit hook** (`pre-commit-reconcile-drafts.sh`, `fd6003a9d`); warn-first per Comms go-signal
- Jun 15 — **June 14 omnibus** (HIGH-COMPLEXITY: COORDINATION, 14 sessions, `c5104bf8d`)
- Jun 15 — cleanup-dev-active: ~200+ → 57 files in dev/active/
- Jun 15 — duty-cycle-tick v1.9: pre-staging discipline added to Step 6

---

*This file is task-list-as-standing-items per v0.6 architectural decision 1. Append/edit during cycle fires; durable across sessions; never deleted.*

### Agent 360 v0.3 response (HOST-requested 2026-06-03; backstop ~June 10)

Post-migration benchmark questionnaire. Respond via markdown memo to `mailboxes/host/inbox/agent-360-response-docs-2026-06-0X.md`.
- Questionnaire: `dev/active/agent-360-questionnaire-v0_3.md` (read Instructions first).
- Docs has NO v0.2 baseline (Docs/Lead/PA didn't field v0.2) → answer §7 from observed Code-era experience; skip prediction-comparison prompts.
- Answer the Docs-specific §8 section + §10 duty-cycle adopter block. Friction + tacit-knowledge answers valued over satisfaction.
- Time Lord: June 10 backstop, not pacing — fold into a cycle fire when it fits.

  **✅ DONE 2026-06-03**: Agent 360 v0.3 response filed to HOST (cc PM) — `mailboxes/host/inbox/agent-360-response-docs-2026-06-03.md` (main `c286d5330`). Answered §1-2/5-10 + Docs §8 + adopter §10; friction + tacit-knowledge focus. Ahead of the June 10 backstop.
