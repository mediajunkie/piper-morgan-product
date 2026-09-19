# Docs Standing Items (Task List per v0.6 Duty Cycle)

**Purpose**: durable task list per v0.6 Duty Cycle architecture (reframed standing-items = task
list, per Architectural Decision 1). This is the slow-moving durable list — for fast-moving
session-to-session state, read `dev/active/docs-carry-forward.md` first; it's the higher-fidelity
source and is rewritten every substantive fire.

**Owner**: Documentation Management (Docs)
**Last touched**: 2026-09-19 ~09:57 PT — Watch surfaces reconciled against `docs-carry-forward.md`
(the fresher source), which had drifted 18 days ahead of this file without a corresponding refresh
here. No new action items found; this is a sync pass, not new work discovered.
**Last full rewrite**: 2026-08-19 13:0x PT. The prior version (unrefreshed since 2026-05-27, with
checkbox items dated through 06-15) had gone stale to the point of being misleading: 6 of its
cited GitHub issues (#1058, #974, #972, #1127, #1128, #1206) were all CLOSED (verified live via
`gh issue view` that fire). Kept only what's still genuinely open, verified live.

---

## Architectural Review 2026 — B3 corpus-disposition pass — COMPLETE, ratified, executed
**Added**: 2026-08-29. **Closed**: 2026-09-01 (3 days against a 1-week estimate).

My lane (**workstream B3**, patterns corpus, 81 files) is fully done: all 81 dispositioned
(75 EFFECTIVE / 2 HISTORICAL / 1 LIKELY HISTORICAL / 3 ABSORBED), Arch ratified all 145
dispositions across both corpora (patterns + CIO's methodology-core, 64 files) in one synthesis
motion 2026-09-01, and every directed marking action is executed: P-006 absorbed into m-07,
P-059 absorbed into m-22 (Docs+CIO joint pick, m-22 canonical), and CIO's two Docs-lane findings
(the doubly-stale multi-agent guides, the gameplan-template.md fork) both fixed. Full trace:
`docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`.
B4 (derived cross-corpus index, #1455) is Arch's, starts next fire — nothing owed here.

## B2 living-core-doc set — glossary is now a Docs-owned living core doc (new, 2026-08-30)
**Added**: 2026-08-30

Six documents now carry "current law" status per Arch's `living-core-docs.md` v0.1
(`docs/internal/architecture/reviews/2026-08-architectural-review/`): ESSENCE.md, SYSTEM.md (new),
intent-routing-stack.md, data-model.md, CONNECTORS.md (new), and **`knowledge/piper-morgan-glossary-v1.1.md`
— mine**. 60-day staleness contract; needs CXO's tracked-state frontmatter
(`last_updated`/`currency_claim`/`max_age_days`) added at first substantive touch, per the plan's
own sequencing — not urgent today, current header is prose-only (v1.4, dated 2026-06-27). Joins
the same machine-read staleness checker the other 5 docs use once frontmatter lands.

---

## Active items

### PreCompact hook — locality differentiation (owed since May, CIO re-flagged 2026-08-23)
**Added**: 2026-08-23 (row); underlying obligation dates to a May second-incident memo — older
than this row, per CIO's audit anchor-date question, see the reply on that.

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
**Added**: 2026-05-28 — **95 days as of 2026-08-31, per CIO's audit. Real candidate, not
neglect-by-omission: the item's own text already names its trigger ("flag at next PM
engagement"), it's just that a natural PM-engagement moment for THIS item specifically hasn't
landed yet. Surfacing plainly rather than let the honest deferral condition become a silent one.**

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

*Reconciled 2026-09-19 against `docs-carry-forward.md`'s "Watch surfaces" section (the fresher,
continuously-updated source). Items below carry the carry-forward's own dates where they've moved
since this file's last full rewrite; anything not re-confirmed there in the last few weeks is
marked accordingly rather than silently dropped.*

- [x] **BRIEFING-CURRENT-STATE engineering/CI/backlog staleness** — flagged 2026-08-17 (#1643),
  escalated directly to Lead Dev 2026-08-24, fixed same-day. Resolved, dropping from watch.
- [ ] **Time-handling audit cluster (#1493, closed) → 6 F-slice children** —
  #1556/1574/1575/1576/1577/1588, filed 08-09/08-10, root cause "no per-user timezone exists
  anywhere in the system." **New to this file 2026-09-19** (was tracked only in carry-forward since
  09-13). Proposed to PM 09-13 as one project routed to Lead Dev; offer to draft the routing memo
  still not confirmed by PM as of 09-19 — watching, not chasing. (09-19: Lead asked where this offer
  went, since it was never mailed to them — clarified it was a PM-facing offer, not a Lead-facing
  one; see `mailboxes/docs/sent/reply-docs-to-lead-cc-exec-the-0913-offer-...-2026-09-19.md`.)
- [ ] **Three PM-directed audits, early August, zero follow-through** — #1499 (route-surface),
  #1522 (false-trails), #1533 (principal-dropping). **New to this file 2026-09-19**, same
  PM-answer-pending status as the cluster above.
- [ ] **`last_verified` bulk-stamp cluster** — **superseded numbers**: this file's 09-01 figure
  (20/38) is stale; carry-forward's 09-07 audit (#1725) read 24/38, unchanged from 09-03. Structural
  fix now filed as **#1726**, CIO's lane — no longer a re-escalate-each-audit item. Check again at
  the 09-21 Weekly Docs Audit.
- [ ] **`universal-list-architecture-guide.md` duplicate** — GH #1585, two paths, diverged content,
  Sept 2025 reorg artifact. Confirmed 2026-08-30 as a genuine judgment call, not mechanical. Still
  unowned/unclaimed as of last check (2026-08-30) — not re-verified this pass, due for a live check.
- [ ] **#1644** — full v19 historical fold of roadmap.md still owed (PPM's lane). Header-date
  symptom fixed 2026-08-24; narrative content still frozen at July 16 state as of last check
  (2026-08-30). Not mine to force.
- [ ] **#1683** — 145 editorial-calendar rows genuinely syndicated but `status`/`canonicalSite`
  never bumped (2026-07-19 migration root cause). Independently corroborated 2026-08-30 by
  Dispatch-PM. Needs a scripted per-row day-of-week-routing reconstruction before any bulk fix.
- [ ] **#1720/#1721** — filed by Docs (missing onboarding screenshots), already triaged by PPM into
  FLYWHEEL — watch for progress. **New to this file 2026-09-19** (carried in carry-forward only).
- [ ] **CXO's marker-provenance-field finding** — no observed/derived flag on the heartbeat marker,
  found 2026-09-05. CIO's lane, not mine. Watch for the fix landing. **New to this file 2026-09-19.**
- [ ] **Feature-guide 4-item PM click-through** — PM commitment cited 2026-08-16, PA's code-level
  verification done 2026-08-19. **Status unknown — dropped out of carry-forward's watch list at
  some point without an explicit resolution note.** Not re-verified this pass; flagging the gap
  rather than assuming either "done" or "still open." Worth a direct PM check next engagement.

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
