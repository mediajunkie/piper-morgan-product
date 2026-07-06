# Sprint Recovery — PM Decisions Log

**Owner**: PPM
**Status**: DURABLE — canonical record of PM's direct, memory-based sprint reconciliation decisions
**Purpose**: These decisions came from PM's own recollection, not from any document, session log, or automated method. They're the most fragile category in the whole recovery effort — nothing else will reconstruct them if this file is lost. Companion to `sprint-history-recovery-plan.md` (the method) and `dev/snapshots/project-board-*.tsv` (the mechanical current-state snapshot).

---

## Methodological corrections PM made during review (2026-07-06)

These apply going forward, not just to this session's issues:

1. **The old "M5 (MVP Polish)" planning label was refactored into the current "M5 - Distribution + Polish" sprint at some point.** Most issues carrying the old label are genuinely the current M5 — but not all; verify each one rather than blanket-applying (see #146/147/148/465 below, which turned out to be FLYWHEEL, not M5, despite carrying the old M5 label).
2. **Scope correction**: sprint-reassignment work should only concern the MVP milestone and earlier (i.e., milestones representing already-planned-or-completed work: MVP, Alpha, Production). Fast Follow / Enterprise / Dot-Releases (Post-MVP) issues are intentionally not yet planned at sprint granularity — a missing Sprint value there is expected, not a gap to recover.
3. **Heuristic**: any issue on the "Alpha" milestone is almost certainly in one of the A1–A31 (or T1/T2/S1/S2/Q1/B1/MUX-cluster) sprints — though PM notes some may have been ongoing/cross-cutting work rather than a single clean sprint.
4. **Sprint calendars matter for this kind of review** — PM asked for start/end dates on closed sprints specifically to support this reconciliation process; that calendar already exists (`sprint-history-recovery-plan.md`'s Tier 2 method) and should be kept current.

## Specific issue decisions (from PM's direct memory, 2026-07-06)

Grouped by destination sprint. Each of these overrode either no available evidence or a stale/ambiguous automated signal — PM's own recollection was the deciding input.

**FLYWHEEL - Process improvement** (Ongoing milestone unless noted):
#146, #147, #148 (milestone also moved MVP→Ongoing — these carried a stale "M5 (MVP Polish)" label but are FLYWHEEL work, not M5), #463 (PM assigned directly; also routed to CIO for closure review — problem likely solved by the 2026-06-12 worktree-discipline ratification), #465 (PM assigned directly), #1206 (PM assigned directly), #1243, #1248, #1267, #1274, #1276, #1180, #1204, #1222, #481, #164, #1141

**D1 - Beta design quality**: #1169, #1170, #1171, #1172, #1173, #1225, #1234, #1236, #1251, #1252, #1254, #1255, #1262, #1263, #1264, #1265, #1266, #1268, #1269, #1271, #1280 (21 issues — PM: "most of the [D1/RECONNECT overlap] group is indeed D1")

**RECONNECT - Connector Refactor**: #1273, #1334, #1339

**A12 - Alpha Setup**: #518, #519, #520, #521, #522, #523, #525 (the "Canonical Queries Phase A/B" series)

**Q - Recurring Audits**: #524 ("Pattern Sweep 2.0"), #938 ("Quarterly Maintenance Sweep - Q2 2026"), #1341 ("Quarterly Maintenance Sweep - Q3 2026" — confirmed by PM as an oversight in the original sweep, not a real exception).

**M1 - MVP Foundation**: #241 (closed the same day M1's own gate closed), #926 (the M1 gate issue itself), #945

**M3 - Artifact Persistence**: #1221

**A4 (Standup Epic)**: #105, #160, #178

**A9 (Alpha Tidy)**: #270 (closed the exact single day A9 ran), #357

**W (Quick Wins)**: #356, #368, #369

**C1 (Craft Pride - CRAFT)**: #231 — notable: this wasn't even one of the two candidate sprints the closedAt-calendar method had offered (A2 or A6); PM's memory identified a third option entirely.

**I1 - MUX Interaction**: #539 — notable: title text alone ("Integration Test button uses MCP instead of OAuth token") superficially resembles an unrelated A12-era issue; PM's memory disambiguated correctly where a title-matching approach would likely have guessed wrong. #639 also I1.

**PROD-INFRA - Infra & Security Hardening**: #1291 (closed as a duplicate of #1257, which is itself in PROD-INFRA; assigned for record-completeness rather than left blank, per PM's call)

## Process correction (2026-07-06, same session)

The first artifact refresh after this round of decisions used a hand-typed list of "resolved today" issue numbers to filter the remaining pool, rather than checking the live board directly. That list was incomplete (missed #1141, #1206, #164, #146, #147, #148, #1180, #1204, #1222, #481, #270 — all of which were genuinely already applied and verified, just not included in the removal list), so the refreshed artifact incorrectly still showed 35 remaining when the true number was 22. PM caught this by noticing already-reported issues still appearing as unresolved. Fixed by rebuilding the remaining-issue list from a fresh live query against the board instead of a manually maintained set — the artifact-refresh process now checks ground truth directly rather than tracking its own memory of past mutations, which can't drift the same way.

**Confirmed correctly sprint-less (Fast Follow milestone, future work, not a gap)**: #244, #272, #338, #104, #546, #568

---

*Log started 2026-07-06 during the Group 1 + Group 2 reconciliation pass. Append further decisions here as remaining groups are reviewed — do not start a new file.*
