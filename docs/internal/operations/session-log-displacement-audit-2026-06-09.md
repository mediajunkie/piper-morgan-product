# Session-Log Displacement Audit — 2026-06-09

**Author**: Docs (Documentation Management)
**Trigger**: PM flag 2026-06-09 16:48 PT — *"This error of writing in an ephemeral cycle log and not the session log needs to stop now. It risks our entire memory and learning process and makes me concerned we may be leaking knowledge already."* Arch's displacement-analysis memo + CIO's disposition assigned the cohort-wide audit to Docs.

## Question

Is session-log displacement (substantive work logged only in the ephemeral `dev/active/` cycle log while the durable `dev/YYYY/MM/DD/` session log is left a stub) isolated to a couple of agents/days, or systemic?

## Method

For each role-day June 1–8, compared session-log line count vs. cycle-log line count (on `origin/main`). Heuristic flag: cycle log substantial (>40 lines) AND session log < half the cycle log — i.e., the cycle log is carrying the day while the session log is a stub. This is a **risk signal, not confirmed loss** (a short session-*summary* alongside a detailed cycle log is the correct pattern; the flag catches stub-not-summary). Heuristic has known false negatives (CIO's own 6/9 was displaced at 45 vs 66, below the /2 trip) — refinement noted below.

## Finding: SYSTEMIC

Displacement appeared in **6 of 9 cycling roles across ~15 role-days**, concentrated in the June 3–8 window — exactly tracking duty-cycle maturation. This confirms Arch's "structural displacement, not individual error" thesis.

| Role | Displaced role-days (June 3–8) |
|---|---|
| **CIO** | 06-03, 06-04, 06-05, 06-06, 06-07, 06-08 — **every day** |
| **Exec** | 06-03, 06-04, 06-05, 06-06 (4) |
| **Arch** | 06-03, 06-07, 06-08 (3) |
| **PPM** | 06-03, 06-08 (2) |
| **Lead** | 06-04 (1) |
| **CXO** | 06-06 (1) |

**Not displaced**: PA (always wrote a substantial session log; no cycle log or session ≥ cycle), and on cycle-log-absent days Lead/PA/PPM write session-log-only (correct). The displacement is specific to roles running a mature cycle-log fire loop.

## Mitigant already in place (the reassuring half)

**The June 3–8 omnibi captured the displaced roles' work** — Docs read the cycle logs (not just session logs) when synthesizing each day, and the omnibi live in the permanent `docs/omnibus-logs/`. So for June 3–8, the knowledge is **not lost** — it is preserved in the omnibus chain. BUT this depended on Docs manually reading cycle logs during synthesis; it is a fragile reactive backstop, not a guarantee, and it does nothing for days that go un-omnibused before their cycle logs are cleaned.

## Dispositions

1. **Source fix (DONE, CIO-lane)**: `duty-cycle-tick` v1.5 — Step 5 dual-surface; cycle-log-full-session-log-empty now impossible-by-construction. methodology-31 amended with the composition discipline.
2. **CLAUDE.md amendment (DONE, Docs-lane)**: "Cycle log lives ALONGSIDE the session log" subsection added to Session Log Maintenance, with the durability-asymmetry table + the displacement-trap framing + the per-fire one-line rule. Cross-references m-31.
3. **Protect cycle logs from premature cleanup (Docs-lane, ACTION)**: `cleanup-dev-active` must NOT archive/remove a role-day cycle log until that day has been omnibused (the omnibus is the durable capture). Add an omnibus-coverage check to the cleanup skill. **Filed as follow-up.**
4. **Detector hook (Lead-lane)**: a session-start net detecting a prior-day session log lacking growth across N substantive commits (CIO's refined heuristic — "no session-log growth across N commits," not a line ratio). Composes with `precompact-signoff-warning` + START step-0 (Comms's prior-day-STOP check). Docs concurs; routes to Lead.
5. **Meta-shape (CIO, candidate)**: "a matured mechanism silently displaces an older discipline it was meant to compose with, because the mechanism's loop doesn't reference the older surface." Ratify-on-this-audit: the systemic finding (6 roles) is the multi-instance evidence — **promotable** beyond candidate. Sibling of methodology-35.

## Heuristic refinement (for the detector)

Line-ratio (`session < cycle/2`) has false negatives. The robust signal is **"no session-log growth across N substantive same-day commits by that role"** — a session log that opens in the morning and never grows while the agent commits work all day is displaced regardless of the cycle log's size. Recommend the detector key on commit-correlated growth, not a static line ratio.
