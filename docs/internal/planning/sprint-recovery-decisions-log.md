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

**W (Quick Wins)**: #319, #320, #331
**S1 (Security and Critical Fixes)**: #323, #324, #333
**FLYWHEEL - Process improvement**: #334, #339, #340
**A10 - Alpha Testing**: #445, #454
**A11 - Alpha Polish**: #457, #475, #476, #478, #479
**P2 - MUX Document Management**: #677, #678, #679, #680, #681 (PM wrote "671" — confirmed via direct lookup that #671 is an unrelated MUX-WIRE issue and #681 is the "document_update_queries routing" issue actually in this cluster; treated as a typo)
**P1 - MUX Navigation Crisis**: #682

## Group 2 complete (2026-07-06)

All 85 issues in the original closedAt-calendar "overlapping candidates" pool are now resolved and verified against the live board. Group 3 (issues with zero evidence from any automated method — the ~99-issue true gap after the milestone-scoping correction) is next.

---

## MEDIUM-tier promotion to HIGH — 21 issues applied (2026-07-06)

Of the 93 MEDIUM-confidence issues, calendar cross-check produced two promotable buckets, both now applied and verified live:

- **17 CALENDAR_CONFIRMS_ALONE** (the calendar's own closedAt-window lookup agreed with the explicit-document proposal, no competing candidate): A7 (Testing & Bufferj) — #254, #255, #257, #258, #259, #260, #261; A20 - Alpha Testing (round 2) — #588, #596; M2 - Conscious Floor + Action Handlers — #100, #101, #946, #964, #970, #971, #1041; A6 (User Onboarding) — #237.
- **4 paren-formatting false alarms**, all genuinely A8 (Alpha Rolloutj [sic — the live option's own name is missing its closing paren]): #262, #283, #291, #294. These had been flagged CALENDAR_CONTRADICTS, but the contradiction was an artifact of my own inconsistent handling of that trailing-parenthesis typo across working files, not a real disagreement — normalizing (stripping parens) before comparing resolved all 4 as genuine A8 matches.

PM approved application of the full high-confidence set beforehand ("high confidence updates approved, yes").

## A9 four-issue cluster resolved by PM memory (2026-07-06)

#376, #377, #378, #379 — PM: "the first 4 are all A9." No calendar or document evidence pointed anywhere for this cluster; PM's direct recollection placed it in A9 (Alpha Tidy), alongside the already-established #270/#357 members. Content is consistent with that call — #376 FRONTEND-RBAC-AWARENESS, #377 ALPHA-DOCS-UPDATE, #378 ALPHA-DEPLOY-PROD, #379 ALPHA-UI-QUICK are all alpha-rollout/deployment-adjacent work. Applied and verified live.

## Methodological insight: cherry-picking and pre-sprint closure (2026-07-06)

PM, on reviewing the harder remaining cases: **"sometimes we cherrypick or things get closed before their sprint starts."** This is a distinct failure mode from calendar-boundary imprecision (the earlier-documented narrow-vs-broad distinction) — an issue can be closed *before* its true home sprint's calendar window even opens, because it was deliberately pulled forward and finished early rather than worked in sequence. The closedAt-vs-calendar method structurally can't detect this: it looks for the window containing the close date, and a cherry-picked issue's close date sits earlier than that window entirely, not inside a neighboring one. No automated fix proposed — this is now a documented reason a low-confidence or seemingly-contradictory case may still be correct, and a reason PM's direct memory is sometimes the only correct source even when the calendar looks like it disagrees.

---

## Three contradicting-tier resolutions, PM-confirmed 2026-07-06 (afternoon)

**#998 — correctly sprint-less, NOT FLYWHEEL.** My proposal (FLYWHEEL) was wrong on a more basic level than sprint choice: PM's own closing comment (missed on first pass because the \ call omitted \) says *"CLOSED. This is an error. The editing and admin UI is attached to pipermorgan.ai, not to the product, and the Web agent already built it."* The real editorial-compose-UI work happened in the **website repo** (Web's lane), not this product repo — #998 is a same-repo placeholder closed as a cross-repo duplicate/error. No sprint value applies; leave empty. PM: *"pro tip: if something seems off, read the comments!"*

**#234 — confirmed C1 (Craft Pride - CRAFT).** PM: *"C1 for sure. It may have not been 'closed properly' till after the work was done?"* — confirming the trailing-edge-slip theory (epic's own body states the work ran Oct 11-14, 2025, inside C1's Oct 10-14 window; the issue's closing comment just landed a day later, Oct 15, sliding the closedAt into A2's window). Already applied.

**#922 — resolved to M1 (MVP Foundation), not the originally-proposed M2.** PM context: *"The floor issue arose as a problem before we dedicated an entire sprint to cleaning it up."* The issue's own comment confirms this precisely: it's the ADR-059 (workflow-dispatcher/offer-consolidation) implementation, closed 2026-03-19 with PM smoke-tests dated 2026-03-20 — five weeks before M2's window even opens (Apr 11). This was the foundational fix that later motivated carving out a dedicated M2 sprint for the same domain ("Conscious Floor + Action Handlers") — thematically M2-adjacent, but chronologically and factually M1 work. Applied and verified live.

## Methodological note: the MVP sprint count changed mid-flight (2026-07-06)

PM: *"Remember, we refactored the MVP sprints at some point. We had six originally, and then we had five, so things changed."* Flagged as context for any remaining M0-M5 boundary judgment calls — a resequencing happened at some point during the MVP track, which may explain some otherwise-odd close-date-vs-window mismatches in that range beyond the already-documented old-M5-relabeling correction. No specific issue reattributed on this note alone; noting it so the pattern is recognized if it recurs in the 56-issue medium-tier artifact.

---

*Log started 2026-07-06 during the Group 1 + Group 2 reconciliation pass. Append further decisions here as remaining groups are reviewed — do not start a new file.*
