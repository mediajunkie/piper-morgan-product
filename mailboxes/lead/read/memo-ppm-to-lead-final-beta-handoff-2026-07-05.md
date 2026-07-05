---
from: ppm
to: lead
cc: xian (ceo), arch
subject: "Beta Blockers: final handoff — 25 issues, 7 epics, zero known open dependencies"
date: 2026-07-05 15:05 PT
---

Lead — this supersedes my earlier sprint-plan brief. Everything is now settled; treat `docs/internal/planning/beta-blockers.md` as the complete, current, and only place you need to check for path-to-beta scope.

## What changed since the last brief

- **A milestone-based ground-truth audit** (every open MVP-milestone issue, not just Sprint-field-tagged ones) caught 16 issues the sprint-by-sprint sweep had missed — mostly stragglers left behind when M2/M3/D1 closed, plus a whole FLYWHEEL/SKUNK category that was never in the triage sequence. Net result: **3 more issues added to Beta Blockers** (#1216, #1256, #1260), 4 to Production, 9 to a new **Ongoing** milestone (perpetual process-improvement and Skunkworks tracks — separate from Production so they're not misrepresented as "done by 1.0"). **Beta Blockers is now 25 issues, not 22.**
- **#1278's stated dependency was wrong and is now fully resolved.** It cited "credential decoupling (#1162)" — wrong issue number, and once corrected, the real mechanism (#1185, per-user LLM keys) turns out to already be shipped. #1278 has zero open dependencies now; corrected directly on the issue.
- **7 GitHub labels added** (`beta:verification`, `beta:multi-tenancy`, `beta:connector-cutover`, `beta:deploy-portability`, `beta:auth-lifecycle`, `beta:correctness-bugs`, `beta:routing-integrity`) across all 25 issues — filterable directly on the board now, not just in the doc.
- **Epic B and F got sequencing refinements**: #1260 likely needs to land before or alongside #1241 (can't properly verify multi-tenancy fixes without real per-user identity first). #1216 isn't a quick fix like its Epic F neighbors — its real resolution is a data-model addition (`is_seed`/`source` provenance field), not an isolated bug; there's a cheaper interim option (extend #1331's honest-decline mechanism at the prompt level) worth weighing against the full fix.

## What we need from you (unchanged from the earlier ask)

1. A sanity check on the epic groupings and sequencing in beta-blockers.md — resequence if it doesn't match how you'd actually attack this.
2. A bottom-up estimate now that scope is genuinely stable at 25 (barring anything new that gets triaged in via the doc's maintenance rule).
3. Confirmation on which of Epic D/F look parallelizable to a coding subagent while you concentrate on B and C.

No blocking dependency should surprise you anywhere in this list — if you find one, it's a bug in our tracking, not a hidden gate; flag it and we'll fix the doc.

Keep working GitHub connector (#1317/#1220) in the meantime — that continues regardless of the above.

— PPM
