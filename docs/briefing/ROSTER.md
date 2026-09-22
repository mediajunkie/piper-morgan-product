---
type: briefing
title: ROSTER.md — Piper Morgan Role Roster
valid_from: "2026-05-22"
last_updated: "2026-08-05"
last_verified: "2026-08-05"
---

# ROSTER.md — Piper Morgan Role Roster

**Status**: v1.0 (Docs-hosted, 2026-05-22). Codifies the implicit role-tiering that has lived in CLAUDE.md's "Your Role" table and the per-role briefings.
**Owner**: Docs (Documentation Management) — keeps roster current as roles are added, retired, or renamed.
**Canonical source for**: which roles are active, what tier each is in, and where each role's briefing lives.

---

## What this doc is

A canonical roster of Piper Morgan agent roles, organized by tier. Per-role lane summaries are one-line; full mission + responsibilities live in each role's `BRIEFING-ESSENTIAL-{ROLE}.md`. CLAUDE.md's "Your Role" table is the same set of pointers in a different shape (assignment-flow oriented); this doc is the org-shape view.

**When in doubt about a role's lane**: read the briefing, not this doc. ROSTER.md is the index; briefings are the substance.

---

## Tier 1 — Leadership (7 roles)

Standing leadership roles. Each owns a strategic lane + a methodology workstream + a defined relationship to PM. All seven on Claude Code as of 2026-04-26 (migration wave Apr 22–26).

| Role | Slug | Briefing | One-line lane |
|---|---|---|---|
| **Chief of Staff** (Exec) | `exec` | `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | Cross-role synthesis; sprint/epic progress tracking; weekly Ship coordination |
| **Chief Architect** (Architect) | `arch` | `BRIEFING-ESSENTIAL-ARCHITECT.md` | Architectural decisions (ADRs); pattern governance; technical strategy |
| **Chief Experience Officer** (CXO) | `cxo` | `BRIEFING-ESSENTIAL-CXO.md` | UX vision; MUX (Modeled User Experience) framework stewardship; interaction patterns |
| **Principal Product Manager** (PPM) | `ppm` | `BRIEFING-ESSENTIAL-PPM.md` | Product strategy; Product Decision Records (PDRs); roadmap + prioritization |
| **Chief Innovation Officer** (CIO) | `cio` | `BRIEFING-ESSENTIAL-CIO.md` | Methodology evolution; pattern capture; Excellence Flywheel custodian |
| **Head of Sapient Trust** (HOST) | `host` | `BRIEFING-ESSENTIAL-HOST.md` | Agent + human network health; role lifecycle; trust-property monitoring |
| **Communications Director** (Comms) | `comms` | `BRIEFING-ESSENTIAL-COMMS.md` | Public narrative; weekly Ship + building narratives + insights; voice + tone |

**Short-references**: "Exec" or "the Chief" (never "CoS" per PM directive May 15). Other titles use their full or abbreviated form interchangeably (e.g., "Architect" / "Chief Architect"; "PPM" / "Principal Product Manager").

---

## Tier 2 — Staff (4 roles)

Standing staff roles. Each owns operational infrastructure + a hands-on production lane. All four on Claude Code.

| Role | Slug | Briefing | One-line lane |
|---|---|---|---|
| **Lead Developer** (Lead Dev) | `lead` | `BRIEFING-ESSENTIAL-LEAD-DEV.md` | Multi-agent dev coordination; cathedral-quality completion; evidence-chain enforcement |
| **Piper Alpha** (PA) | `pa` | `BRIEFING-piper-alpha.md` | PM assistant; skunkworks PoC coordination; PM-bandwidth-extension lane |
| **Documentation Management** (Docs) | `docs` | `BRIEFING-ESSENTIAL-DOCS.md` | Omnibus logs; mailbox system; blog metadata pipeline; merge-keeper sweep |
| **Web** (Unicorn Web Designer) | `web` | `BRIEFING-ESSENTIAL-WEB.md` | pipermorgan.ai public site + publishing pipeline; a two-repo role (product-repo infra worktree + `piper-morgan-website` worktree) |

**Web is Tier 2** (retiered from Tier 3, 2026-08-05 — full rationale in
`docs/internal/architecture/decisions/claude-md-history.log`).

---

## Tier 3 — Specialized roles

Roles deployed for specific work shapes rather than continuous standing presence.

| Role | Slug | Briefing | Status | One-line lane |
|---|---|---|---|---|
| **Coding Agent** (subagent) | `prog-code` | `BRIEFING-ESSENTIAL-AGENT.md` | Active (deployed by Lead Dev / others as needed) | Subagent role for precise technical tasks; systematic verification + evidence |
| **Exploratory Testing Agent** (ETA) | `test` | `BRIEFING-ESSENTIAL-ETA.md` | Dormant (last session March 2026) | Agent-perspective testing of Piper Morgan's systems; friction + capability-gap surfacing |
| **Special Assignments** | `spec` | — | Active (activated as needed) | Specialist work outside the standing roles' scope; `mailboxes/spec/` exists, no dedicated briefing yet |

---

## Session log naming

Every role's session logs live at `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{slug}-{tool}-log.md`:

- **Slug** column above identifies the role
- **Tool**: `code` for Claude Code
- **Model**: NOT in the filename — recorded in the session log's own header instead (models vary
  by role and change over time; encoding one in the filename would go stale). See CLAUDE.md's
  Session Discipline section.
- **Historical logs** (pre-2026-06-29) do carry a `-opus` or `-sonnet` suffix — leave those as-is
  when you encounter them, don't rename to match the current convention.

Example (current convention):
- `2026-09-22-0632-docs-code-log.md` — Docs Code session, Sep 22 06:32 (model in the log header)

## General-purpose Code sessions

If no role is assigned, the agent is a **general-purpose Claude Code agent**. Use slug `code` (per CLAUDE.md's own Role section). Per CLAUDE.md: "Do not assume you are the Lead Developer — ask PM what role you should take if the task is ambiguous."

---

## Cross-references

- **CLAUDE.md** "Your Role" section: assignment-flow oriented version of this same set (briefing pointers + slugs)
- **Each role's briefing** at `docs/briefing/BRIEFING-ESSENTIAL-{ROLE}.md`: full mission + core responsibilities + relationship to PM + lane-specific protocols
- **`docs/internal/operations/branch-worktree-mailbox-discipline.md`**: cross-role operational discipline (worktree-default, mailbox-on-main, merge-keeper sweep, fold-on-handoff)
- **Mailbox routing**: `mailboxes/DIRECTORY.md` (canonical slug → role mapping; especially for the CEO mailbox at `mailboxes/xian (ceo)/`)
- **Agent activity log**: `docs/internal/operations/agent-activity-log.csv` (per-session record across all roles)
- **Briefing currency**: `docs/briefing/BRIEFING-CURRENT-STATE.md` (project state; refreshed regularly)

---

## How to use this doc

- **As a new role assignee**: find your row, follow the briefing pointer, read that doc first
- **As an active agent looking up another role's lane**: read the one-line summary here; if you need more depth, open the briefing
- **As PM or an agent thinking about cohort tiering**: this is the canonical view of who's in which tier and why
- **As a role rename or new-role proposal**: update this doc + CLAUDE.md role table + create the briefing + announce via cohort memo

---

## Status / change log

- **v1.0** (2026-05-22, Docs): initial codification of the 7+3+specialized tiering. Source-of-truth for what had been implicit in CLAUDE.md's role table and the BRIEFING-ESSENTIAL-* set. PM-blessed via the May 22 conversation thread.

---

*— Documentation Management, 2026-05-22*
