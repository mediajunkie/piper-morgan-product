---
type: pattern
number: "075"
title: "Load-Bearing Work Crowded Out by Commodity Work"
status: "Emerging"
valid_from: "2026-10-13"
last_updated: "2026-10-13"
---

# Pattern-075: Load-Bearing Work Crowded Out by Commodity Work

## Status

**Emerging.** Elevated 2026-10-13 by CIO under Emerging self-approval (`methodology-audit-policy-updates-2026-03-16.md`) from PP-002, "Critical vs. Commodity Work in a Role", tracked in `PROTO-PATTERNS.md` since 2026-04-27. PM keeps upgrade, revision and removal authority.

## Problem

Every role has a small core of **load-bearing** work, where its distinctive judgement lives (a methodology audit, a voice-quality read, an ADR audit, a product-shadow observation). Around that core is **commodity** work the role also owns: mail, CI checks, logs, deploy steps, trackers. Commodity work gets mechanized (a script, a skill step, a hook, a duty-cycle step) and then runs on schedule. Judgement work can't become a hook. Unless it has a trigger, it silently stops, and the role still looks busy and healthy from outside.

## Evidence

**April (PP-002, by reflection):** seven retiring leadership roles independently drew the same load-bearing versus commodity split in their Agent 360 v0.2 section 6 (HOST, CIO, Comms, CXO, PPM, Arch, Exec). The full per-role table is kept in PP-002's history in `PROTO-PATTERNS.md` (git log).

**October (by measurement, the elevation evidence):** `docs/internal/research/role-duties-operational-vs-official-2026-10-13.md`. That is 11 roles, 164 written duties and 30 days of logs, measured six months after migration.
- 13 duties had moved into a mechanism; **none of the 13 had lapsed**.
- 37 duties were not seen at all, clustered in each role's specialist judgement work.
- Where it could be measured, roles spent 20 to 35% of a week's entries on their own priorities. CIO spent 0%.

**PP-002's three elevation criteria, each checked:**
1. *Holds across a full post-migration sprint:* yes, 30 days and all 11 roles.
2. *Lead and Docs validated, not inferred:* their duty rows were measured (Lead 14 of 15 operational, Docs 12 of 14 operational). Their focus share couldn't be measured because their log headings are templates. **Partly met.**
3. *Behaviour change, not just nomenclature:* the same day, three roles (Web, Arch, CXO) found judgement duties that had really stopped and gave each a trigger. All 10 replying roles sorted their unseen duties into keep, move or retire.

## Solution

- **Name the load-bearing core per role.** The role cards (`<!-- ROLE-CARD -->` blocks in each briefing, printed by the SessionStart hook since 2026-10-13) list priority 1 and name the commodity work to keep small.
- **Give judgement work a trigger with a visible miss.** It can't have a mechanism. The first trigger is the daily `Drift:` line in duty-cycle-tick v1.51.
- **Measure, don't assert.** Re-run the duty count with each 360 round. The next run is due 2026-10-27 (CIO standing item 8r). If the specialist share hasn't moved, the trigger is being written but not acted on, and it needs a cost when missed.

## Recognition cue

A role's log for a week is all mail, fixes and fire bookkeeping, every entry is correct, and nothing in it is the work the role card names first.

## Related

- **Methodology-36, corollary of 2026-10-13** ("work that cannot be mechanized gets crowded out by work that has been") is the mechanism behind this pattern. m-36 explains why the crowding happens; this pattern names what it looks like in a role.
- **Pattern-045 (Green Tests, Red User):** commodity work passing doesn't mean the role is succeeding.
- **Pattern-062 (Assembly Assumption):** role-correct work that doesn't add up to team-correct work, here at the level of how a role spends its time.
- **Pattern-074 (Visibility Loss After Premature Retirement):** the duty disappears from view without anyone deciding to retire it.

## Graduation to Proven

This needs one independent instance outside the 10-13 measurement: the 10-27 re-run, or another project's team (Klatch was named in PP-002). It also needs evidence that a trigger moved the specialist share, not only that roles acknowledged the gap.
