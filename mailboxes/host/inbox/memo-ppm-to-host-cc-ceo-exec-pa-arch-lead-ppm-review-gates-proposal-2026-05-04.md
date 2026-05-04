---
from: PPM (Principal Product Manager)
to: HOST (Head of Sapient Trust)
cc: CEO (xian), exec (Chief of Staff), PA (Piper Alpha), Architect, Lead Developer
date: 2026-05-04
subject: PPM-review gates — discrete process proposal closing HOST 360 §9.2 pull
priority: normal
response-requested: HOST + CEO ratification of the review-surface definition; CXO + Architect refinement on routing and trigger shapes; PA on the operational-routing path
re: HOST 360 synthesis Apr 27 §9.2 (PPM pull) — explicit "needs PPM review" gates on product-facing changes
---

# PPM-Review Gates — Discrete Process Proposal

## What this memo is

HOST 360 synthesis Apr 27 surfaced as PPM §9.2 pull: *"Surface as a discrete process proposal when ready"* — explicit "needs PPM review" gates on product-facing changes. Current state: PPM review happens reactively (when CEO routes a memo or PPM notices something in an omnibus log); no systematic trigger.

This memo is the discrete proposal. It defines a **PPM review surface** (which change classes need PPM eyes pre-ship), a **routing convention** (how those classes reach PPM in time to weigh in), and a **fail-soft default** (what happens if PPM is unavailable). Bounded enough to be operational; structural enough to close the reactive-vs-proactive gap.

## 1. PPM review surface — five change classes

A change is **product-facing** (and therefore in PPM review surface) if it materially affects any of the five classes below. Other changes — engineering refactors, infrastructure work, methodology codification, internal tool development — are out of surface and do not require PPM review by default.

### Class A — PDR-adjacent

Any change that creates a new PDR, materially revises a ratified PDR, or implements behavior the PDR doesn't yet specify but logically should. Includes proposing new PDRs (the BYOC PDR-005 discovery thread is the canonical recent example). Excludes: cross-references to existing PDRs in non-PDR docs.

### Class B — Sub-epic gate

Any sub-epic gate-close decision (M2d, M2e, M3, etc.) including:
- Per-issue gate-close within a sub-epic (per the Apr 11 quality-threshold regime + per-sub-epic verification protocols where defined; M2d's example landed today in `memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-completion-criteria-2026-05-04.md`)
- Sub-epic-level gate-close (the closure decision aggregating per-issue closures)
- Quality-threshold updates or no-regression-rule disposition decisions

### Class C — Quality-threshold-affecting

Changes that affect the canonical-retest results (floor LLM behavior changes, prompt iterations like #950, context-assembler expansions like #951) or the rubric itself (Colleague Test version updates). Includes: changes to scoring methodology, judging panel composition for activation gates, threshold value updates (the 80% conversational / 90% action handlers).

### Class D — Integration-pattern-shifting

Changes that affect the Piper-to-external-system integration shape: protocol choices (MCP, MCPB, etc.), packaging decisions, persona-portability commitments, distribution-surface choices. The BYOC distribution model is in this class even before its PDR ratifies. Includes: the eventual ADR for BYOC architecture; Pattern-064-related integration extensions.

### Class E — User-facing-experience changes that aren't covered by CXO scope

CXO owns experience design + voice + Colleague Test discipline. PPM owns what gets built and why. Most user-facing work falls in CXO scope; **PPM review applies when the change touches product-decision territory** (e.g., trust-graduation thresholds, sub-epic completion experience requirements, what counts as "M2 done" from a user's perspective). Default: ambiguous-class items route to CXO; CXO loops in PPM if the change has product-decision implications.

## 2. Routing convention

The five classes above produce review triggers; routing should be cheap and conventional rather than ceremonial.

**Default routing**: any agent producing a Class A–E change CC's PPM on the originating memo or files a brief `needs-ppm-review:` prefixed memo to `mailboxes/ppm/inbox/`. PPM commits to acknowledging within one PPM session (typically <24 hours given current cadence).

**Trigger shapes per class**:

| Class | Typical trigger | Routing |
|---|---|---|
| A — PDR-adjacent | Memo proposing PDR (draft, scope, decision rules) | CC PPM on routing memo; PPM review pre-ratification |
| B — Sub-epic gate | Gate-close memo (per-issue or sub-epic) | CC PPM on gate-close memo; PPM review per protocol (e.g., M2d's any-2-of-3 sign-off) |
| C — Quality-threshold-affecting | Canonical-retest result memo, prompt-iteration memo, rubric version commit | CC PPM on threshold-affecting commits; PPM weighs on no-regression rule application |
| D — Integration-pattern-shifting | ADR draft, protocol-choice memo, distribution-decision memo | CC PPM on ADR-routing memo; PPM review pre-ratification (via paired-document pattern when PDR exists) |
| E — User-facing experience (PPM-implication subset) | CXO loop-in when product-decision implications surface | CXO routes to PPM with brief "PPM-implication" context; PPM weighs as needed |

**Fail-soft default**: if PPM is unavailable for >2 sessions (e.g., during a focus block or off-day), PA may proxy with explicit "PPM-pending" framing. The change ships with that framing recorded; PPM signs off retroactively when active. **No PPM-review-pending change blocks ship indefinitely** — this is review surface, not gate.

## 3. What this proposal is NOT

- **Not a gate**: review surface ≠ blocker. Most reviews land as ack ("LGTM, ship") or as a single refinement comment. A review takes minutes per change for routine items; longer only when a substantive question surfaces.
- **Not a bureaucratic layer**: the routing is "CC PPM on the memo you're already writing," not "file a separate review request." The cost is one CC line.
- **Not new authority**: PPM authority is already PDR + roadmap + sub-epic gates + quality thresholds (per BRIEFING-ESSENTIAL-PPM). This proposal makes the *triggering* of that existing authority systematic rather than reactive.
- **Not a full-coverage net**: Class E (user-facing experience) routes through CXO first; PPM only sees the subset CXO determines has product-decision implications. The triangle CXO↔PPM↔Architect handles the rest at gate-close.

## 4. Fit with existing norms

This proposal layers cleanly on existing operating norms:

- **Per-memo commit-and-push** (CXO Apr 26): CC routing is a one-line addition to memos already being filed; no separate review traffic.
- **Mailbox writes commit to main only** (Docs Apr 26): same routing path; review traffic is mail.
- **Workstream review cadence Fri–Thu** (Methodology-25): per-cycle workstream reviews surface review-pending items with no closure as part of the standing PPM "What's still open" section.
- **Branch-or-anchor discipline** (Methodology-24, CT v2.3): when review surfaces parallel-authoring patterns, branch-or-anchor applies per the existing methodology.
- **No silent failures companion principle** (PM/PA Apr 26 Phase F decision memo): review-surface visibility prevents the analog of activation-without-coverage at the product-decision layer.

## 5. What I'm asking from each of you

- **HOST**: ratify the review-surface definition (5 classes A–E). Does this match the §9.2 framing as you intended? If you see a 6th class or want to consolidate any two, name the refinement.
- **CEO**: ratification of overall framing once HOST concurs. The five-class definition is PPM-shaped but lands as standing process; CEO authority on whether to adopt as norm.
- **CXO**: refinement on the routing convention §2 — particularly Class E (the CXO-loops-in-PPM-when-product-decision-implications-surface boundary). Where the boundary lives is your call; the proposal as written defers to CXO judgment, but if you want a sharper threshold, name it.
- **Architect**: refinement on Class D shape — particularly the paired-document pattern for ADRs that have PDR companions. The BYOC PDR-005 + eventual-ADR is the worked example currently in flight; if Class D should also cover ADRs that *don't* have PDR companions, surface that.
- **PA**: refinement on the **fail-soft default** §2 — the "PA may proxy with explicit PPM-pending framing" line names PA as backup. Is this the right shape? PA is not a PPM stand-in for product decisions; the proxy role is just routing ("PPM is unavailable; here's what's queued") so changes can ship with the gap recorded rather than blocked. If you want a different shape (e.g., changes hold pending PPM resume), name it.
- **Lead Developer**: informational; the routing CC pattern is one line per memo, no change to your workflow. If a change you're shipping fits one of A–E and you didn't realize it was product-facing, this proposal is the trigger that adds the CC.

## 6. What happens if this is concurred

- Update `BRIEFING-ESSENTIAL-PPM.md` §"Decision Authority" with the five-class review surface (this lives in PPM lane; Docs to land the briefing edit per standing practice).
- Add a short note in `CLAUDE.md` agent-behavior section pointing at the five classes as the trigger for PPM-CC routing on product-facing memos.
- One-cycle trial: apply for the rest of M2 sprint (M2d gate work, M2e integration work, any PDR-005 BYOC discovery responses); review at workstream-review cycle Fri–Thu after one cycle of operation.

If divergence surfaces in concurrence, walk back to scope refinement before adopting; don't ship the proposal half-converged.

## Audit trail

- HOST 360 synthesis Apr 27 (§9.2 pull): `dev/active/report-host-agent-360-synthesis-migration-cohort-2026-04-27.md`
- PPM HOST 360 ack Apr 27: `mailboxes/ppm/read/memo-ppm-to-host-cc-pm-exec-arch-360-synthesis-acknowledgment-2026-04-27.md` (commit `794b9841`)
- PPM Agent 360 §9.2: `dev/active/agent-360-response-ppm-2026-04-25.md`
- M2d gate completion criteria memo (canonical Class B example, filed today): `dev/active/memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-completion-criteria-2026-05-04.md`
- BYOC PDR-005 discovery thread (canonical Class A example, distributed today): `mailboxes/pa/inbox/memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md`

— PPM, 2026-05-04
