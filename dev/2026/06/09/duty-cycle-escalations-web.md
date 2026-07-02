# Web Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per Duty Cycle (escalations reframed as attention doc).

**Owner**: Unicorn Web Designer (Web)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Last refresh**: 2026-06-09 (housekeeping pass — cycle stand-down + cohort discipline updates)

---

## Active escalations (for PM)

- **(none currently)** — the cycle-launch escalation that lived here since 2026-05-29 was resolved 2026-06-06 by PM directive to stand down. See "Recently resolved" below for the trail.

## Awaiting external resolution (not blocking web)

- **PM↔CIO discussion on canonical launch gesture** (open since 2026-06-06). CIO confirmed cycle agents are peer top-level sessions with self-registered crons but flagged a doc-vs-practice drift on the launch gesture itself. PM clarified usage of both methods (Desktop "New session" + terminal `claude`); the canonical choice + trade-offs is a PM↔CIO design question, not web action. Web's cycle remains stood down until this resolves (or until PM directs a different approach). The shelved cron prompt at `dev/active/web-cron-prompt-v0.7.md` can be revived under either gesture.

## Process observations (for cycle methodology + CIO research)

- **2026-06-07** — recipient-owns-MANIFEST cohort discipline rolled out (Lead, PM-directed, CIO-endorsed; #1106). Originated from web's 2026-06-06 contention near-miss + PM's "who updates which when" instinct. Methodology-36 Class-1 exemplar per CIO; structural endgame is derive (regenerate MANIFEST from `ls inbox/` + frontmatter `subject:`).
- **2026-06-06** — cycle launch stood down. PM's "I have not had to set up doppleganger sessions for any other agents" surfaced a mental-model mismatch on cohort session-launch mechanism. CIO honestly split confirm-vs-don't-confabulate, flagged the drift, kept the variant ratified but launch deferred. Lesson: when PM intuition pushes back on an inferred model, the inference is what's likely wrong, not the intuition.
- **2026-06-05** — main-direct 2×/day shape with 11:57pm STOP fire RATIFIED by CIO (`cron-shape-experiments.md` row 5; explicit-paths-only named as load-bearing condition / falsification tripwire). Variant remains valid if cycle ever launches; shape design is preserved.
- **2026-06-02 → 06-05** — work-shape-fit assessment (CIO ask → web middle-path response → CIO 6/3 overnight-continuity update → web 2×/day STOP-shape proposal → CIO ratification). Captured how a separate-repo + intermittent + handoff-driven lane composes with the cohort cron pattern.
- **2026-05-29** — initial adoption prep at offset `:57` (worktree-Model-A version, since superseded by main-direct variant + then shelved).

## Recently resolved (rolling, ~14 days)

- **2026-06-09** — `claude/web-cycle` worktree + branch cleaned up (cycle stand-down housekeeping); standing-items + this file refreshed.
- **2026-06-06** — cycle launch stand-down ratified; substrate shelved (variant remains registered).
- **2026-05-29 → 06-06** — cycle adoption arc: substrate prep → variant design → CIO ratification → mental-model-mismatch surfaced → stand-down. Net: design value preserved (5th registered shape on cohort registry); operational launch deferred.

---

*Escalations-as-attention-doc per Duty Cycle architectural decision. Append during fires when items need PM-attention surfacing.*
