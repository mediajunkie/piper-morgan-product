# Docs Standing Items (Task List per v0.6 Duty Cycle)

**Purpose**: durable task list per v0.6 Duty Cycle architecture (reframed standing-items = task
list, per Architectural Decision 1). This is the slow-moving durable list — for fast-moving
session-to-session state, read `dev/active/docs-carry-forward.md` first; it's the higher-fidelity
source and is rewritten every substantive fire.

**Owner**: Documentation Management (Docs)
**Last touched**: 2026-08-29 ~19:3x PT — added Architectural Review B3 workstream (below).
**Last full rewrite**: 2026-08-19 13:0x PT. The prior version (unrefreshed since 2026-05-27, with
checkbox items dated through 06-15) had gone stale to the point of being misleading: 6 of its
cited GitHub issues (#1058, #974, #972, #1127, #1128, #1206) were all CLOSED (verified live via
`gh issue view` that fire). Kept only what's still genuinely open, verified live.

---

## Architectural Review 2026 — B3 corpus-disposition pass (owed, kickoff ~09-01)

Arch ran a full architectural review with PM, ratified 2026-08-29. My lane: **workstream B3** —
corpus-disposition pass over patterns (81 files, my side) alongside CIO's methodology-core (64
files) and Arch's ADRs, owner Arch with CIO+Docs. Mechanical first axis (cited/uncited) already
done via `docs/internal/architecture/reviews/2026-08-architectural-review/
findings/citation-census-summary.md` — my job at kickoff is the second axis (effective/inert
judgment) for the cited patterns, working from that census rather than re-deriving from zero.
Target ~1 week from kickoff. Full plan: `reorientation-plan.md` in the same review directory.
No prep owed before 09-01 — acknowledged to Arch, ready.

---

---

## Active items

### PreCompact hook — locality differentiation (owed since May, CIO re-flagged 2026-08-23)

`.claude/hooks/precompact-signoff-warning.sh` — I'm the named owner (per the May 10 second-incident
memo). Of the 3 proposed refinement options, 2 are addressed (severity tiering, shipped May 10;
"safe to compact" self-serve path, was already substantively present via SOFT tier's option (c),
reworded 2026-08-23 to match the proposal's exact language — `298fd4f89`). **Option 1 (locality
differentiation) is the genuine remaining gap** — described as highest-leverage, lowest-effort at
the time, but requires real design: reliably detecting "local persistent Model-A worktree" vs.
"remote/sandbox/ephemeral session" isn't obviously solvable with an available signal (no confirmed
env var or session metadata to key off yet). Touches a hook that wedged 4 agents (PPM, Lead Dev,
CXO, CIO) in the May 10-17 incidents — needs proper behavioral testing before shipping any
control-flow change, not a same-fire patch. Scope the detection mechanism first, then implement +
watch it fire before trusting it, per CLAUDE.md's hook-verification discipline.

### Critical-docs YAML-frontmatter upgrade (PM-directed 2026-05-28; still genuinely incomplete)

PM directive: upgrade critical docs to proper YAML frontmatter; Docs prompts + supervises +
validates subagents. **Validated pattern** (briefing pilot, `b40876b87`): subagent prepends
frontmatter extracting existing metadata, body untouched; validate via `git diff --numstat`
(0 deletions) + spot-check + confirm `---` start.

Schema: `type:` (briefing|methodology|adr|pattern|memory) + `title:` + `valid_from:` +
class-specific fields (number/status for adr/pattern/methodology; last_updated for
briefing/methodology).

- [x] **Briefing (17)** — DONE, `b40876b87`.
- [ ] **ADRs (~78)** — spot-checked live this fire: still plain `# ADR-NNN: Title` headers, no
  frontmatter block. Genuinely not started beyond the pilot.
- [ ] **Patterns (~80)** — spot-checked live this fire: still `# Pattern-NNN: Name` + `## Status`,
  no frontmatter. Genuinely not started.
- [ ] **Methodology (~52)** — not verified this fire; assume not started absent evidence.
- [ ] **.serena/memories (~29)** — lower priority (Serena tool memory, not the institutional-
  memory target the directive was really aimed at).

Dormant since the briefing pilot (2.5+ months, no further progress logged). Worth a direct check
with PM on whether this is still wanted at this priority, rather than continuing to carry it
silently — flag at next PM engagement rather than resume unprompted.

### Cycle / daily ops (recurring, still current)

- [ ] **Daily merge-keeper sweep** — Docs-owned; catches stranded session logs / unmerged
  feature-branch work within 24h. Per Sign-Off Discipline.
- [ ] **MANIFEST regen across mailboxes** — after mail-discipline operations;
  `scripts/regenerate-mailbox-manifests.py --role docs`.
- [ ] **Omnibus log cadence** — daily synthesis for prior day, `create-omnibus` skill. **Note**:
  the cadence slipped twice this week (3-day gap 08-14/15/16, then a 2-day gap 08-17/18 — both
  found and closed same-week, not by external flag). Verify 08-19 gets its omnibus on 08-20
  without a third gap; if it slips again that's a pattern worth naming, not just re-fixing.

## Watch surfaces (things owned by others, checked periodically — don't re-derive, don't re-chase)

- [x] **BRIEFING-CURRENT-STATE engineering/CI/backlog staleness** — flagged 2026-08-17 (#1643),
  escalated directly to Lead Dev 2026-08-24 (a 2nd, name-addressed flag after the first sat a
  week), fixed same-day. Resolved, dropping from watch.
- [ ] **`last_verified: "2026-06-19"` bulk-stamp cluster** — flagged 2026-07-30 (Arch/CIO), 20 of
  26 still on the stamp as of 2026-08-24 (down from 23 a week prior — modest, ongoing). Cohort-
  wide, no single owner. Check at next Monday audit; escalate by name if still >75% stale.
- [ ] **`universal-list-architecture-guide.md` duplicate** — two paths, diverged content, Sept
  2025 reorg artifact. Lead Dev's lane, flagged 2026-08-17, unchanged as of 2026-08-24.
- [ ] **#1644** — full v19 historical fold of roadmap.md still owed (PPM's lane). The header-date
  symptom was fixed 2026-08-24; the underlying narrative content is still frozen at July 16 state.
- [ ] **#1683** (new, 2026-08-25) — 145 editorial-calendar rows genuinely syndicated but
  `status`/`canonicalSite` never bumped (root cause: 2026-07-19 migration used an unreliable
  selection field). Historical, not urgent. Needs a scripted per-row day-of-week-routing
  reconstruction before any bulk fix — not something to attempt casually.
- [ ] **Feature-guide 4-item PM click-through** — PA's code-level verification is done; 4 items
  need a live browser PM doesn't have on their Amber seat's normal path. PM said they'd take it
  directly (2026-08-16); status of completion still unconfirmed as of 2026-08-25 — surface at
  next PM engagement, don't chase.

## Blocked items

(none currently)

## Recently completed (rolling, ~7 days — see session logs / omnibus for full detail)

- 2026-08-19 — **Weekly Ship #056 "Fundamentals First"** published, live-verified, 2 real defects
  caught+fixed, 5 load-bearing claims fact-checked against primary logs, Exec notified.
- 2026-08-19 — **Omnibus backfill, 08-17 + 08-18** (2-day gap found+closed same-day, 27 session
  logs synthesized, 27 activity-log rows appended, 2 genuine cross-role discrepancies preserved).
- 2026-08-17 — **Weekly Docs Audit #1643 CLOSED** — 7 real fixes, 2 systemic findings surfaced
  (not swept under the rug), #1644 filed for residuals.
- 2026-08-17 — **Omnibus backfill, 08-14/15/16** (3-day gap found+closed, chain verified
  continuous 07-27→08-16).
- 2026-08-18 — **9-day duty-cycle-heartbeat gap found+fixed** (Exec found, HOST verified, Docs
  fixed same-fire, now a standing per-fire practice).
- 2026-08-13 through 08-16 — 4 blog posts published end-to-end (Alpha Launches, Confabulating a
  Peer's Unfinished Work, The Fabricating Standup, The Architect's Own Trap), zero rendering
  defects; website#31 publish-post.js rendering bug found, fixed, back-applied to 15 historical
  Ships.

---

*This file is task-list-as-standing-items per v0.6 architectural decision 1. Append/edit during
cycle fires; durable across sessions; never deleted — refresh instead of letting it drift, per
the 2026-08-19 rewrite that prompted this note.*
