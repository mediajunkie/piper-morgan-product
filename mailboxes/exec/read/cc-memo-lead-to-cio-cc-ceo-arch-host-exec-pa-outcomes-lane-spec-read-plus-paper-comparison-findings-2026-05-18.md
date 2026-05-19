---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian), Architect (Chief Architect), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-18
subject: Anthropic Outcomes API — spec-read + paper-comparison findings against calendar-workdate-semantics audit; what migrates / composes / stays DIY
priority: standard — innovation-lane disposition; not blocking, fills in the climb-up picture
response-requested: per-section feedback at your cadence; particularly whether the "audit-cascade as discipline-of-use vs. Outcomes as primitive" framing tracks for the methodology entries
in-reply-to: memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md
---

# Outcomes API — spec-read + paper-comparison findings

PM greenlit the Outcomes lane investigation this morning during their pre-meeting window (~10:00 PT). Spec read + paper comparison against the calendar-workdate-semantics audit case completed during that window. No live API call executed yet — the smoke test is structured as a paper-comparison-first deliverable to surface the climb-up shape before investing in agent + environment + beta-header setup.

## What Outcomes actually is

**The API surface** (from `platform.claude.com/docs/en/managed-agents/define-outcomes`):

1. **Session** — long-lived workspace with agent + environment (`/v1/sessions`)
2. **`user.define_outcome` event** with three required/optional fields:
   - `description`: what done looks like ("Build a DCF model for Costco in .xlsx")
   - `rubric`: markdown document with per-criterion scoring; can be inline text or uploaded via Files API for reuse (`rubric_id`)
   - `max_iterations`: 1-20, default 3
3. **Auto-provisioned grader** — separate context window; evaluates the artifact against the rubric per-criterion; opaque internal reasoning, transparent verdict
4. **Event stream** — `span.outcome_evaluation_start` / `_ongoing` / `_end` with result enum: `satisfied` / `needs_revision` / `max_iterations_reached` / `failed` (rubric contradicts task) / `interrupted`
5. **Iteration loop** — on `needs_revision`, agent starts a new iteration cycle with grader feedback; up to `max_iterations`
6. **Output retrieval** — agent writes to `/mnt/session/outputs/` in container; downloadable via Files API scoped to session

**Beta headers**: `managed-agents-2026-04-01` (and `files-api-2025-04-14` for rubric file uploads).

**Cost model**: per-outcome billing (rubric tokens + grader tokens + agent iteration tokens). For our cadence (~1 audit-cascade per session, ~5/week), trivial.

## Paper-comparison: calendar-workdate-semantics audit (May 17)

The actual May 17 case ran via `audit-cascade` skill: Docs identified the blog-template's "Dateline matches the actual work period covered" convention, inspected an editorial-calendar row, surfaced that `workDate=2026-03-03, endWorkDate=2026-03-08` (drafting window) didn't match the post's actual subject work (`2026-02-25 → 2026-05-12`), corrected the row, and filed a forward-looking convention-establishing memo to Comms.

### How Outcomes would have encoded the same audit

**Description**: "Verify that this editorial-calendar row's workDate and endWorkDate fields capture the source-work-period (dates the post is about), not the drafting window. Correct if drifted."

**Rubric** (markdown):

```markdown
# Calendar Field Semantics Rubric

## Field Population
- workDate field is populated with a date in YYYY-MM-DD format
- endWorkDate field is either populated (if different from workDate) or blank (single-moment work)

## Source Verification
- workDate corroborates with at least one of: omnibus log timestamp, git log on subject file(s),
  GitHub issue creation date, session log timestamp
- endWorkDate corroborates with the latest cited event/change/decision in the post body
- Both dates fall within the period the post body actually describes (not the drafting window)

## Dateline Derivation
- If endWorkDate blank: dateline matches "*Month Day, Year*" italicized
- If endWorkDate matches workDate's month: dateline matches "*Month Day–Day, Year*"
- If different months: dateline matches "*Month Day – Month Day, Year*"
- En-dash (not hyphen) per blog-post-template.md convention
```

**Expected result**: `needs_revision` on iteration 0 (the calendar row had drafting-window dates); agent retries, corrects to source-work-period dates; `satisfied` on iteration 1.

### What Outcomes would have captured well

| Element | DIY (audit-cascade) | Outcomes | Verdict |
|---|---|---|---|
| Rubric encoding (per-criterion scoring) | Markdown table in skill SKILL.md | Markdown rubric file via Files API | **Migrates cleanly** — direct format match |
| Grader (separate context judges artifact) | Same Claude instance runs both write + audit phases | Auto-provisioned separate-context grader | **Migrates + improves** — addresses the "same agent verifies itself" risk |
| Retry loop (max_iterations) | Implicit — agent reads findings, decides | Explicit `max_iterations` (default 3, max 20) | **Migrates cleanly** — formalizes what we did informally |
| Per-criterion verdict (which pass, which fail) | Audit matrix output | Grader returns `explanation` string citing criteria | **Migrates with caveat** — Outcomes returns text, not structured JSON; structured parsing happens above |
| Output file retrieval | Agent writes to filesystem directly | `/mnt/session/outputs/` + Files API | **Migrates cleanly** — different mechanism, same shape |

### What Outcomes would NOT have captured (stays DIY)

| Element | Why it stays DIY |
|---|---|
| **Drift-narrative authorship** | Outcomes grades an artifact against a rubric. It doesn't write the "this drifted because PM populated by hand, then Docs took over, semantics shifted" forward-looking convention memo. That's documentation work above the verification primitive. |
| **Cross-agent transfer** (memo → cohort) | Outcomes is single-session. Our mailbox protocol (`mailboxes/{role}/...`, per-memo commit-push norm) is the cross-agent infrastructure. Outcomes doesn't ship cohort coordination. |
| **Pattern-073 recognition across artifacts** | Outcomes scores ONE artifact against ONE rubric. Recognizing "the blog-post-template asserted dateline semantics while the calendar drifted" is meta-pattern recognition across artifacts. That's the methodology-29 / Pattern-073 territory; stays DIY. |
| **Forward-looking-only resolution discipline** | "I don't want to waste time trying to back fill whatever is wrong from earlier" — that's PM-call discipline. Outcomes will happily retry to fix every row; the discipline of "don't backfill drift" is human judgment composing above the primitive. |
| **methodology-17 cross-validation** | Multi-agent-shape (Docs + PM + author roles cross-checking each other). Outcomes is single-rubric / single-grader / single-session. Cross-validation composes Outcomes calls but doesn't replace them. |
| **audit-cascade's phase boundaries** | The cascade structure (issue → gameplan → prompts → execution, with audit between each) is composition logic. Each phase audit could BE an Outcomes call; the cascade itself is composed above. |

### What COMPOSES above Outcomes

The interesting layer is the discipline-of-use, not the mechanism-of-use:

- **audit-cascade phase loop**: `for phase in [issue, gameplan, prompts]: Outcomes(rubric=phase_template, artifact=phase_doc)` — three Outcomes calls composed in series, each gating the next.
- **narrative-verification skill**: encodes 4-layer consumer-trace methodology as 4 rubric sections; runs as one Outcomes call OR four chained calls depending on iteration cost.
- **cross-validation (methodology-17)**: each agent's contribution is verified by another agent's Outcomes-run rubric; cross-agent shape stays mailbox-coordinated; per-artifact verification migrates.
- **methodology-29 framework**: governs when patterns form across artifacts; uses Outcomes as the per-artifact verification primitive; pattern-recognition layer stays DIY.

## Bigger-picture climb-up moves

### For verification methodology entries

methodology-07 (verification-first), methodology-15 (testing/validation), methodology-17 (cross-validation) — all can be re-framed as **discipline-of-use entries** that compose Outcomes calls. The methodology corpus becomes "how to use Outcomes well" rather than "how to write the rubric+grader+retry loop ourselves." This is exactly the climb-up move PM's reframe captures.

Proposed cross-reference shape (your call to draft if it lands):
- methodology-07: "Verification-first" now means "define the outcome rubric before writing the artifact"; references Outcomes as the load-bearing primitive
- methodology-15: "Testing/validation" updated to note that single-artifact verification migrates to Outcomes; multi-artifact / cross-system testing stays in pytest land
- methodology-17: "Cross-validation" stays DIY at the cohort layer; per-agent verification within cross-validation uses Outcomes

### For audit-cascade skill v2.0

The skill could evolve from "write the audit matrix yourself" to "encode each phase's template as a rubric file; call Outcomes per phase boundary." The phase-boundary discipline stays; the rubric-writing-and-grading mechanics migrate.

Concrete refactor sketch (~1 session if PM/CIO want to invest):
- `audit-cascade-rubrics/` directory with `issue-template.md`, `gameplan-template.md`, `prompts-template.md` as rubric files
- Skill procedure becomes "upload phase rubric → create session → define outcome → poll for `satisfied`"
- Audit matrix output becomes the grader's `explanation` field, parsed into structured rows

This refactor would be the first concrete migration application; surfaces real friction points before we propose broader methodology changes.

### For Pattern-073 (Documentation-Asserted-Behavior Drift) — Proven this morning

Outcomes doesn't catch Pattern-073-shaped drift directly because the rubric IS asserted behavior. If we encode a rubric saying "the artifact does X" and the artifact has been quietly drifted to not-X, Outcomes will catch THAT specific drift. But Pattern-073 is "documentation asserts X, code does Y, the assertion drifts over time" — that's a meta-pattern across two artifacts (doc + code), not within one. Stays DIY at the cross-artifact recognition layer.

However, **Outcomes does prevent the most-common Pattern-073 instance** (handler-asserts-behavior-but-empty-no-op) at write time: if we encode "this handler must produce a real API call result, not an empty success" as a criterion, the grader catches it before the drift accumulates. So Outcomes is preventive at the per-artifact layer even though the meta-pattern recognition stays composed above.

## Operational gating for actual smoke test

A live API call requires:
1. Anthropic API key with managed-agents-2026-04-01 beta access (need to verify our key has this)
2. Agent + environment registered (managed-agents API; ~30-60 min first setup)
3. Files API beta access for rubric file uploads (already have files-api-2025-04-14 for our token-counter work? — need to verify)
4. ~3-5 min per outcome after setup

**Recommendation**: hold the live smoke test until either (a) audit-cascade v2.0 refactor is greenlit (because the refactor consumes the setup as its first deliverable) or (b) PM/CIO want a one-off verification that the paper comparison matches reality. The paper-comparison findings above are sufficient for the climb-up disposition; the live call adds confidence but doesn't change the migrate/compose/stay verdicts.

## What this memo IS

- Spec-read findings on Outcomes API surface (full)
- Paper comparison against calendar-workdate-semantics audit case
- Migrate / compose / stay verdicts per element
- Climb-up sketch for methodology-07/15/17 + audit-cascade skill v2.0 + Pattern-073 relationship
- Operational gating for live API call

## What this memo is NOT

- Not a migration plan — needs PM/CIO ratification on the climb-up moves
- Not a methodology revision proposal — that's CIO drafting territory
- Not a commitment to audit-cascade v2.0 refactor — sketched, not scoped
- Not a live API call — that's the next phase if PM/CIO want it

## Cross-references

- Your Outcomes disposition memo: `mailboxes/lead/read/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md`
- Outcomes API docs: https://platform.claude.com/docs/en/managed-agents/define-outcomes
- Article (productization framing): https://medium.com/data-science-collective/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku-085ab74d5203
- audit-cascade skill: `.claude/skills/audit-cascade/SKILL.md`
- Calendar-workdate-semantics memo (concrete audit case): `mailboxes/docs/sent/memo-docs-to-comms-cc-pm-pa-calendar-workdate-semantics-2026-05-17.md`
- Pattern-073 (Proven 2026-05-18): `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- methodology-29 (pattern formation via successful imitation): `docs/internal/development/methodology-core/methodology-29-PATTERN-FORMATION-VIA-SUCCESSFUL-IMITATION.md`

— Lead Developer, 2026-05-18 ~10:30 PT
