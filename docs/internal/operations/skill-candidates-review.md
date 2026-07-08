# Skill candidates review — standing PM+Exec surface

**STATUS: PROPOSED** (Exec draft, 2026-07-08, from PM's suggestion during the Ship #050 window-error discussion — *"We can consider the question of what to skillify maybe as a routine thing that we do on a regular cadence... a very good thing for you and I to talk about."*) Cadence, shape, and the current candidate dispositions below are all pending that conversation — nothing here is ratified.

## Purpose

A recurring, lightweight PM+Exec review of what deserves to become a skill, what should fold into an existing one, and — just as deliberately — what should *not* be built. The don't-build column exists because of PM's don't-overlearn principle (2026-07-08): a process with a long clean track record that failed once under compound exogenous disruption usually needs repair-readiness, not new machinery.

## Proposed cadence

**Monthly**, PM+Exec, ~20 minutes, opportunistically sooner if something hot lands. (Weekly would compete with the Ship rhythm and overproduce; quarterly would let candidates go stale.) Exec maintains this doc between reviews; PM disposes at review time.

## Signal feeds (all already being collected — no new collection needed)

1. **Memory-eval "wanted but not found" buckets** — every role already writes this section at session wrap (per #974). A recurring "wanted but not found" across roles is a skill candidate by definition.
2. **Incident docs** (`docs/internal/operations/*-2026-*.md`) — each one ends with a fix-disposition that is often a skillify-or-not question.
3. **Omnibus "Session Learnings"** — Docs already surfaces repeated improvised procedures.
4. **Exec's synthesis vantage** — repeated ad-hoc patterns visible across role logs during weekly Ship work.

## Triage columns

Every candidate gets exactly one disposition, with reason recorded (so we don't re-litigate):
- **BUILD** — new skill warranted
- **FOLD** — belongs inside an existing skill/procedure; name which
- **DON'T-BUILD** — explicitly declined, with the reason and (where useful) an escalation trigger that would reopen it

## A taxonomy worth applying at creation time (PM, 2026-07-08)

Two distinctions, orthogonal:
- **Generally-usable vs. role-tailored** — some skills any agent could run; others encode one role's specific lane.
- **Who owns it vs. who can run it cold** (the bus-factor axis) — PM's example: Docs wrote the publish skill to formalize a process Docs and PM do together, but any agent could run it in a pinch. This week supplied two live proofs of the value: Exec ran `draft-weekly-ship` when Comms went dark (Ship #049), and again for Ship #050. Skills written for coverage — "who runs this cold if the owner is unavailable?" — earned their keep twice in one week.

Proposed cheap discipline: skill creation asks the bus-factor question at birth, and the frontmatter `scope:` field (already exists — cf. `create-session-log`'s `scope: cross-role`) gets set deliberately rather than by default.

## Current candidates (first-pass triage, PENDING PM review)

| Candidate | Origin | Exec's lean | Reason |
|---|---|---|---|
| Ship-kickoff window mechanism | Ship #050 window error (7/8) | **FOLD** (into Exec's existing Friday kickoff procedure) | The fix is three lines — compute window from prior Ship +7d, assert Fri/Thu day-of-week, verify push landed. A skill is more surface than the fix warrants; the failure needed a compound outage to occur at all. |
| Workstream-§0 report-writing skill | PM floated it, same discussion | **Two honest options — PM's call** | *Light*: the kickoff memo template carries the computed window verbatim and reports quote it rather than re-derive; add a one-line date-bleed self-audit reminder (the process guide already names date-bleed as the #1 recurring error). Gets ~90% of the value with almost no new surface. *Full*: a thin cross-role `write-workstream-section` skill mechanizing the methodology-25 §0 format + window-quoting + self-audit. Worth it if we see one more windowing/date-bleed error under *normal* (non-outage) conditions — that's the escalation trigger. Five clean prior Ships argue the prose instructions mostly work. |
| Skill-scope/bus-factor audit | PM's taxonomy point | **FOLD** (one-time pass, then it's a creation-time discipline) | Inventory existing skills' `scope:` frontmatter vs. reality; make "who runs this cold?" a standard question in skill-creator guidance. |

## Review log

*(empty — first review not yet held)*
