# Release model — what "alpha," "beta," and "1.0" actually mean

**Status**: Canonical. Written 2026-08-30 (PPM), per Arch's ask on ESSENCE v1.0 ratification
(`decisions.log` 2026-08-30 ~16:3x): fold roadmap v18.4/v18.7(kk)'s semantics + PM's 2026-08-30
statement + the 08-07 release-train sketch's vocabulary into one citable doc, so this question
never needs re-deriving. Linked from `roadmap/roadmap.md`.

**Purpose**: this is the doc CLAUDE.md's staleness discipline exists to prevent from staying
unwritten. Before this, the audience/gate model existed only as scattered roadmap changelog
entries and milestone-description prose — real, ratified, and re-derived from scratch by whoever
next needed it. Cite this doc; don't re-derive.

---

## 1. Three questions, one word each — don't let a name answer two

Adopted from Arch's 2026-08-07 release-train sketch (`docs/internal/architecture/current/
release-train-definition-sketch-2026-08-07.md`) — **the vocabulary only**. That sketch's specific
recommendations (retire "staging," rename the `production` branch) are still 🟡 unratified; this
section pulls forward just the three-question distinction, which the sketch itself credits to
Exec's prior-art trace and which is genuinely load-bearing.

| # | Question | What answers it | Nature |
|---|---|---|---|
| 1 | **Where does it run?** | `PIPER_ENVIRONMENT` — `development` / `staging` / `production` | **Machine fact.** Code branches on it |
| 2 | **Who is it for?** | alpha / private beta / public beta / GA | **Product fact.** PM decides; nothing in the code reads it |
| 3 | **What is actually running?** | reading the artifact on the running machine | **Observation**, not a name |

**The failure mode this prevents**: "it's in production" collapses questions 1 and 2, and has
produced confident wrong answers before (a branch-staleness/deployed-artifact conflation cost
PPM a two-orders-of-magnitude error on 2026-08-06; a `production`-mode vs `production`-branch
conflation cost Arch a wrong deploy claim the same week). **Rule of thumb**: a *process* is in
production mode; a *release* or *feature* is not "in production" — it ships to an *audience*.

---

## 2. The audience/milestone model — ratified, current as of 2026-08-30

**Milestone closure gates audience, not calendar date.** This has been true since v18.4
(2026-07-04) and has not changed in shape since — only in which milestone gates which audience
transition.

| Stage | Gated by | What starts | Precedent / ratification |
|---|---|---|---|
| **Alpha** | (already running) | Existing invited testers, current surface | Ongoing |
| **Private beta** (v0.9.0) | **MVP milestone closes** | Invitation-only beta, existing surface | v18.4, 2026-07-04: "MVP milestone = beta gate — beta ships when MVP milestone is complete, not on a calendar date." Unchanged since; beta date itself was explicitly dropped 2026-08-08 (moved back a month, no new fixed date set — see `decisions.log:1242`). |
| **Public beta** | **Production-milestone MCP-path work completes** (front-loaded: the #1462 cluster — #1462, #1458, #1509, #1688) | General availability of the beta, MCP path live | **2026-08-30, ESSENCE v1.0** (`decisions.log` ~16:3x): "MCP-path completion is the PUBLIC-BETA GATE." Same shape as the precedent below — a named subset of Production-milestone work gates the *next* audience stage, not Production's own closure. |
| **1.0 / GA** | **Production milestone closes in full** | General release | Milestone #9 definition, unchanged. |

**The precedent chain, so the shape reads as consistent rather than ad hoc**:
- **v18.7(kk), 2026-07-16**: the four core connectors (GitHub/Calendar/Slack/Notion) must
  fully refactor to close Production; **beta is explicitly authorized to start without them**,
  completion happens *during* beta, re-triage at MVP close. (Slack later descoped to Fast Follow,
  2026-08-27 — "no optional complexity," weakest MCP fit of the four.)
- **2026-08-30**: the MCP-path cluster must complete before **public** beta; **private beta does
  not wait on it** — same shape, one stage further out, recorded on the same milestone (#9)
  description.

**Both instances share the same structural idea**: Production is not one monolithic gate. It
carries **named front-loaded subsets**, each gating a specific downstream audience transition,
while the rest of Production's scope gates only Production's own closure (1.0). A Production-
milestone issue not in a front-loaded subset is not blocking anything upcoming — it's the rule
working, not a defect (see `dev/active/ppm-carry-forward.md`'s "disposition rule" note).

**How a front-loaded subset is marked on the board**: Sprint field = `PUB - Public Beta` (verified
2026-08-30 against #1462, which already carried it; #1688 moved to match same day — see §4).
Sprint field ≠ milestone: milestone answers "which release," Sprint answers "which named push
within that release."

---

## 3. "Not MVP" never defaults to Fast Follow

Standing rule (PM, 2026-08-09), restated here because it's easy to misencode from habit:
**MVP → Production → Fast Follow**, strictly. An issue leaving MVP triage lands in **Production**
by default (it becomes "during-beta" work), never Fast Follow. Fast Follow is its own deliberate
destination (e.g., Slack, 2026-08-27), not a residual bucket for anything not urgent enough for
MVP.

---

## 4. Applied 2026-08-30 — #1688 moved MVP → Production-front

Per ESSENCE v1.0's milestone reconciliation: #1688 (FTUX empty-state interview for MCP-cold users)
is MCP-path new build, not web-chat-surface convergence, so it sits with the rest of the #1462
cluster rather than in MVP. Executed same day: milestone MVP → Production; Sprint field →
`PUB - Public Beta`; board Status → `Product Backlog` (mirrors #1462's own shape). Verified via
`updateProjectV2ItemFieldValue` (the safe per-item mutation — see `assign-sprint-safely` skill;
`updateProjectV2Field` was never touched, so no other item's Sprint value was at risk).

This unblocks **C5** (the 8-increment MCP-path roadmap sequencing from Leg D's clean-room rebuild,
`findings/leg-d-paper-rebuild.md`): increments 2–8 file into Production, Sprint `PUB - Public
Beta`, alongside #1688 and the rest of the #1462 cluster — no milestone guessing required.

---

## 5. Where to look for live numbers, not this doc

This doc records **the model**, not counts. For current state:
- **`scripts/sprint-truth.py`** — milestone-scoped NOT DONE breakdown, cite verbatim, never a bare total.
- **`docs/internal/planning/beta-blockers.md`** — the MVP gate's own canonical issue-by-issue detail.
- **`docs/internal/architecture/ESSENCE.md`** — the six (now seven) load-bearing commitments this
  release model exists to serve; commitment framing, not sequencing, lives there.
- **`docs/internal/architecture/decisions/decisions.log`** — the append-only record of every
  ratification cited above, in the ratifying party's own words.
