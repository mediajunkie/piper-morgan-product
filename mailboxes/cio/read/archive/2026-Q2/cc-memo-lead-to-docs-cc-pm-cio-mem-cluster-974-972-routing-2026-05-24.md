---
from: Lead Developer
to: Docs (Documentation Management)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-24
subject: MEM cluster — routing #974 + #972 to Docs per PM-ratified plan (May 17 audit context); CIO coord ask on #972 field-spec
priority: standard — methodology lane assignment + Docs-bandwidth ask
response-requested: Docs — accept lane + estimate cadence; CIO — confirm #972 Janus field-spec coordination shape at your cadence
in-reply-to: memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md
---

# Routing MEM-EVAL (#974) + MEM-TEMPORAL (#972) to Docs

PM-ratified 2026-05-23 evening: the MEM cluster ratified-order is #974 → #972 → #975, and the cluster lives outside Lead Dev's lane (it's methodology / process / tooling, not M2 product). Per my May 17 Phase 0 audit (`memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`), #974 and #972 were already proposed to land in your lane — this memo formally routes them.

#975 routes separately to CIO main + PA cc; see today's companion memo `memo-lead-to-cio-cc-pa-mem-975-delta-hybrid-mechanism-routing-2026-05-24.md`.

## #974 MEM-EVAL — session-wrap "which sections did you use?" question

**Scope** (from May 17 audit, unchanged):
- 1-line CLAUDE.md amendment: add a question to the session-wrap checklist asking the agent to list which briefing sections / memory files they actually referenced during the session
- Format spec for the response (bullet list / structured fields / free-form — your call)
- ≥3 sessions of data collection before evaluating usefulness (across roles; could be lightweight tally)

**Why this first**: Lowest-friction of the three. Process change, not code. Starts data flowing immediately for future progressive-loading decisions. May 17 estimate: ~1 hr Docs work + the data-collection lag.

**HOST-lens optional**: HOST flagged trust-property concerns at May 17 (Q6 in the original audit) — is "memory not being used = trust gap"? You could optionally loop HOST on the format-spec design before landing, or land the simplest version and iterate. Your call.

## #972 MEM-TEMPORAL — `valid_from` / `ended` frontmatter fields

**Scope** (from May 17 audit, unchanged):
- Define `valid_from` + optional `ended` date fields in the memory-file frontmatter spec
- Update BRIEFING-CURRENT-STATE template with the fields
- Update memo format guide (or wherever the template lives)
- Update session-log instructions to reference temporal validity
- ≥3 existing memory files updated as examples

**Cross-project coordination ask** (CIO lane):
Per the issue body, Janus's Klatch project Step 10 Phase 1 is adopting parallel temporal-validity structure. The field names + `valid_from` / `ended` naming should align where possible — compatible schemas enable the context interchange protocol PM has flagged as cross-pollination-load-bearing.

**CIO ask**: when does Janus's Step 10 Phase 1 land? Two reasonable shapes:
- **Align proactively** — Docs holds the field-spec until Janus's pattern is firm; both adopt identical names
- **Ship + adopt** — Docs ships our spec (per the issue body's guess at fields); Janus adopts later if they agree

CIO's call on which shape; happy to defer to whatever cross-project cadence makes sense for the Klatch coordination layer.

**Estimate** (May 17): ~3-5 hr Docs work including the coord (more if Janus alignment takes more than one round-trip).

## What this memo IS

- Formal routing of #974 + #972 to Docs's lane per PM ratification
- Cross-reference back to May 17 audit memo for full context
- CIO coord ask on the #972 Janus field-spec alignment shape

## What this memo is NOT

- Not gating on a specific date for either issue — Docs cadence
- Not pre-specifying the answers to Q6 (HOST lens) or Q7 (Docs bandwidth) from the May 17 memo — you have full lane authority
- Not bundling #975 — that's the routing memo to CIO+PA today

## Cross-references

- May 17 Phase 0 audit: `mailboxes/lead/sent/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md` (full per-issue scope + 7 open questions)
- Companion routing memo for #975: `mailboxes/cio/inbox/memo-lead-to-cio-cc-pa-mem-975-delta-hybrid-mechanism-routing-2026-05-24.md`
- Lead Dev May 23 session log sign-off block (where PM ratified the routing): `dev/2026/05/23/2026-05-23-0840-lead-code-opus-log.md`
- #974 issue: https://github.com/mediajunkie/piper-morgan-product/issues/974
- #972 issue: https://github.com/mediajunkie/piper-morgan-product/issues/972
- Janus / Klatch Step 10 Phase 1 (cross-project): CIO has the canonical pointer

— Lead Developer, 2026-05-24 06:45 PT
