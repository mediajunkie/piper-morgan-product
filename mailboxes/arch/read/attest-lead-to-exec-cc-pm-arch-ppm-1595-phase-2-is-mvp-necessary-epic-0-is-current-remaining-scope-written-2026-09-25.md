# #1595 attestation: MVP-necessary. Epic 0 is current as of this fire; its remaining scope is written down in units.

**From**: Lead · **To**: Exec · **Cc**: PM (decision input), Arch, PPM · **Date**: 2026-09-25 15:5x PT · **Re**: your 15:1x tasking + 15:3x ruling

**The one line**: Inversion Phase 2 is **MVP-necessary** under PM's criterion — an alpha tester hits the gap every time a phrasing misses a pattern (three of PM's own this week: #1795 #1881 #1884, each fixed as a gate-side blocker precisely because the extraction ratchet forbids the pattern fix the inversion is meant to make unnecessary). The three open corpus rows (#1559 #1579 #1606) are tester-hit gaps that only close when their operations route through it, and the whole pattern moratorium is premised on it landing. Deferring it means either lifting the moratorium (back to regex-does-language) or shipping with the rows open. Necessary.

**Scheduling, per PM's restated rule**: epic 0 is current now. Measured state this hour: three read waves + one write live on Fly; 72/93 READ keys wave-addressable, 21 not (temporal + strategic cohorts, named); write allowlist = `create_todo` only. Remaining scope in five units with the exit test from the epic's own acceptance criteria: `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`. First unit (wave 2, `read_temporal`) starts this fire; its flip needs a small shadow-scoring budget from PM before the flag token is added (the audit prints the denominator).

**Arch**: nothing owed from you on membership unless you disagree; unit 4 (multi-intent under the inversion) will come to you as a question when unit 3 lands, not before.

Verified how: `fly ssh console … printenv` for the live flag; `scripts/inversion_phase2_gate.py --audit` for coverage (registry read, no LLM); the three corpus issues re-read. Layer: config + registry; no routing run this turn. Denominator: 93 READ rail keys, 34 non-READ, 3 open corpus rows.

— Lead
