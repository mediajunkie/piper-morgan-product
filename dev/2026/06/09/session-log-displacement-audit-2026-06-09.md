# Cohort Session-Log Displacement Audit — 2026-06-09

**Author**: Documentation Management (Docs) · **Trigger**: PM's "are we leaking already?" + CIO Rec 1 (the gate for whether the displacement meta-shape earns a methodology slot) + Arch's structural-displacement analysis.
**Method**: per cycling-role × day (June 4–9): session-log lines (SL), cycle-log lines (CL), **session-log commits that day (SLc)**, cycle-log commits (CLc). The load-bearing signal is **SLc** — did the session log *accrete as work happened* — per CIO's refinement (line-ratio alone misses mid-day displacement). Candidates spot-verified by reading, not trusted from counts.

## Verdict: displacement is **SYSTEMIC**, not localized to Docs + CIO

The discriminator is stark. **PA runs SLc 4–13** (session log accretes through the day, cycle log near-empty) — the gold standard, proving per-fire session-logging is fully achievable inside the duty cycle. The displacers run **SLc 0–1** (session log written once) while the cycle log carries 80–350 lines of the day's actual substance.

| Role | Pattern | Evidence |
|------|---------|----------|
| **PA** | ✅ **Gold standard** | SLc 4–13; 18 in-day entries (6/6); cycle logs ~0. Session log IS the record. |
| **Docs** | ⛔ **Total displacement** | No session log at all June 4–8 (cycle-log-only); CLc 16–23/day. Fixed 6/9 (reconstructed + resumed). |
| **CIO** | ⛔ **Heavy displacement** | SLc=1 June 4–7 (write-once) while CL 79–168, CLc 9–25. Self-admitted 6/9 (session stopped 11:45). Worse than admitted — 4+ days. |
| **Exec** | ⛔ **Heavy displacement** | June 5–7 SLc 0–1 while CL 56–207. Substantive work (cohort-rollup etc.) lived in cycle logs. |
| **Arch** | ⚠️ **Intermittent** | Good session logs 6/6–6/7 (SL 116/83, SLc 2); displaced 6/8–6/9 (SL thin, CL 348/217, SLc 1). |
| **PPM** | ⚠️ **Structural / stub** | Session log is a stub ("## Work Log — per-fire detail in cycle log"); SLc=1; day-detail + STOP in cycle log. |
| **HOST** | ⚠️ **Summary-at-close** | Real EOD summary but written once (SLc=1); granular day-work in cycle log (CL 25–70). Milder. |
| **CXO** | 🟡 **Improving** | Displaced 6/4–6/7 (SLc 1–2) → healthy 6/8–6/9 (SLc 5, accreting). |
| **Comms** | ✅ **Low concern** | Cycle logs thin (CL 9–30, quiet lane); session logs comparable. Not displacing. |

**~6 of 9 cycling roles** show displacement to some degree. This decisively clears CIO's gate ("multiple independent instances → the meta-shape earns a slot"). PA is the existence-proof that it's avoidable; the gap is discipline-not-feasibility.

## The clean detector (for the Rec-2 hook, Lead's build)

**SLc (session-log commits per day) is the discriminator**, exactly as CIO predicted — not the SL/CL line-ratio (which would have missed CIO's own 45-vs-66 day). Operational signal:

> **On day-close or per-fire: if the role has ≥N substantive commits today but its session log was committed ≤1 time (no mid-day accretion) while a cycle log accreted, flag displacement.**

This catches all the cases above and would NOT false-flag PA (SLc tracks CLc) or Comms (no substantial cycle log). It's a "growth across N commits" check, not a snapshot ratio.

## Conclusion → routes
1. **Meta-shape earns a slot** (CIO's gate met): *"a matured mechanism silently displaces an older discipline it was meant to compose with, because the mechanism's procedure loop doesn't reference the older surface."* The duty cycle (mechanism) displaced session-log discipline (older surface) across 6 roles. → CIO to mint as the methodology entry; cross-references m-35 (asymmetric-discipline sibling).
2. **The v1.5 dual-surface skill fix is correctly targeted** — it forces SLc to track CLc (every substantive fire writes a session-log line), making displacement impossible-by-construction for every role on the skill.
3. **Rec-2 hook** (Lead): implement the SLc-based detector above as the reactive net for roles not on the skill.
4. **Docs Rec-4** (CLAUDE.md): amend the Session Log Maintenance section to name the discipline + cross-ref m-31's new section. **Also found**: CLAUDE.md line 31 says *"Session logs: `dev/active/YYYY-MM-DD-…`"* — WRONG path (should be `dev/YYYY/MM/DD/`); the `dev/active/` instruction is itself a contributing factor to the cycle-log confusion. Fix in the Rec-4 amendment.

*Forensic basis: git history on origin/main, June 4–9; spot-reads of HOST/PA/PPM/CIO logs.*
