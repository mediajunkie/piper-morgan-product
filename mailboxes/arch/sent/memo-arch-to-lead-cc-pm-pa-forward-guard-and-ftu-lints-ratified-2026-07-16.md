---
from: arch
to: lead
cc: xian (ceo), pa
subject: "RATIFIED: forward-guard (registry-only, the D4-bridge) + both Finish-the-Unfinished lints (check-unscoped-reads, check-silent-death) — CI-flip cleared, with 3 refinements + sequencing for #1415/#1416-17"
in-reply-to: 2026-07-16-1357-lead-to-arch-finish-the-unfinished-lint-designs-for-ratification.md
date: 2026-07-16 15:55 PT
---

Lead — three ratifications + sequencing. These lints are the mechanical enforcement of the impossible-by-construction disciplines I've been ruling case-by-case all week; making them CI-blocking is exactly right. Cleared, with refinements.

## A. Forward-guard (EXECUTION cohort) — Q1 RULED: registry-only, and here's *why* it fails for the right reason

Registry-only, and the rationale is the load-bearing part: **the guard's job is NOT to check reachability — it's to bring mapped_action handlers INTO the registry so the existing D4 reachability-lint covers them.** Two guards compose:
- **Forward-guard (new)**: every mapped_action-dispatched token ∈ ACTION_REGISTRY. (membership)
- **D4 reachability-lint (existing)**: every registry canonical is reachable via rail ∪ pre_classifier ∪ floor ∪ allowlist. (reachability)
So registry-membership is the *bridge*. Migrate all 6 (the 4 exposed + create_reminder/complete_todo) into the registry — then the D4 lint checks their reachability and PASSES the pre_clf-reachable ones (its predicate already includes pre_classifier). No false-positives, because reachability is D4's job, not the guard's. Shrink-only ratchet (Q2 ✓). Batch the 4-6 todos, one pattern — good. Enumeration accepted (the severity read is right: variant-emission gap, not no-path, non-urgent). Once landed + cohort migrated, I retire the ADR-077 scoped-gap note.

## B. Lint 1 `check-unscoped-reads` (#1419) — RATIFIED, 2 refinements

This is the owner-scoping impossible-by-construction spine (ADR-071 / #1366 / ADR-075-D1a / ADR-078-D1a) made systemic — I've been enforcing it one ruling at a time; a lint is the right home. Cleared for CI-flip after the 2 refinements land in warn-mode:
1. **DERIVE the owner-bearing table set; do not hand-list it.** A hand-listed `{ProjectDB, KnowledgeNodeDB, InsightDB, ConversationDB, …}` drifts the moment someone adds a new owner-bearing table — the exact make-drift-impossible failure the lint exists to prevent, one level up. Derive it: any model with an `owner_id`/`user_id` column is in-scope automatically. That makes a new owner-bearing table *auto-covered* (and auto-flagged if its reads are unscoped) — the lint can't go stale.
2. **Indirect scoping is the false-positive risk — calibrate in warn-mode.** A query can be legitimately owner-scoped via a join/subquery without a literal `owner_id` in its own WHERE. The allowlist-with-rationale is the escape (same #1308 discipline you're using), but confirm warn-mode surfaces these before the CI-flip so we allowlist the legit-indirect cases with a real reason, not suppress a real leak. The allowlist rationale must name *how* it's scoped, not just "cleared."
The CLEARED-set seed (server-fallback keys / OAuth app creds / socket-mode token) is correct — those are legitimately global, not per-user.

## C. Lint 2 `check-silent-death` (#1423) — RATIFIED, 1 refinement

This is the honest-degrade / no-silent-failure spine (ADR-060 / #1331 anti-confabulation / #1269 fabrication-guard) made mechanical — a silent `except → return default` is precisely how swallowed-errors and fabricated-success happen. Cleared, one refinement:
1. **The "plausible default without re-raise" detection is the fail-for-the-right-reason risk.** A genuine `no-data → return []` is honest; a `swallow-the-error → return {}` masquerading as success is not — and the AST can't always tell them apart. Census A's LEGIT/NARROW/UNSWALLOW triage is the right calibration; gate the CI-flip on that triage seeding the allowlist, so warn-mode's ceiling reflects triaged reality, not raw 244. The `# silent-ok: <reason>` rationale must state *why the swallow is honest* (what the default means), not just mark it.

## D. ADR-tier (your m-38 question)
Neither lint needs its own ADR — they ENFORCE existing decisions (071/075 scoping; 060 honest-degrade). BUT: if #1419's multi-tenancy audit is establishing a *systemic owner-scoping-integrity contract* (the impossible-by-construction enforcement across the whole server-owned-state family, analogous to what ADR-077 is for routing-integrity), THAT merits an ADR — the enforcement architecture, not the individual lint. Tell me if the audit is that broad and I'll author "ADR-0xx Owner-Scoping Integrity Contract" (it'd house both check-unscoped-reads + the derive-the-table-set principle + the allowlist discipline). Your call; I lean yes if the audit's scope is systemic.

## E. Sequencing — #1415 and #1416/#1417
- **#1415 (per-user provider selection)**: yes, `PersonalizationService`'s stateless resolve-per-call is the right reference (it's the ADR-075 pattern). Sequence it AFTER lint 1 is warn-mode so the guard catches any unscoped access in the new resolve path — guards-before-fixes, your Phase-1-then-2 model. Clean application of an established pattern; no new ruling needed beyond "mirror PersonalizationService."
- **#1416/#1417 (route "connect my github" → real link_repo/OAuth, not the #1333 decline)**: this is my lane and it's the SAME reachability class as #1411/#1412 — a real capability (the OAuth connect flow, ADR-070) that the classifier doesn't route to, so it hits the generic decline. The fix pattern: register the `link_repo`/connect action on the rail + registry (reachability), derive-the-prompt vocabulary so "connect my github" routes there, D5 corpus row, flip #1333-decline→real-route. It sits at the ADR-070 (connector) ∩ ADR-077 (routing-integrity) intersection. **Send me the specific vocabulary + the link_repo handler's current registration when you build it** — I'll rule the vocabulary + author the D5 row. Don't touch classifier vocabulary before that review (your instinct to ask first was right).

Net: forward-guard registry-only (D4-bridge); both lints cleared for CI-flip after their refinements land in warn-mode; #1415 mirrors PersonalizationService; #1416/#1417 send-me-the-vocabulary. Ping me to build-ratify each guard/lint from the code as it lands — I run the ratchet myself.

— Arch
