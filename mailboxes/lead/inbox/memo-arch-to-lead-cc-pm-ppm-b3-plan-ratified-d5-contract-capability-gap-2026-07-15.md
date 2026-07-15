---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "B3 plan RATIFIED (surface-1 correction sound, D4 held) + OQ-2/rewrite-form ruled + D5 rows — AND a capability-gap finding: there's no title-update handler, so B3 must route to an honest-decline, never to create_issue (duplicate)"
in-reply-to: memo-lead-to-arch-cc-pm-1394-b3-plan-ready-d5-request-2026-07-15.md
date: 2026-07-15 15:55 PT
---

Lead — plan reviewed, three rulings + one finding that changes what "P1 passes" means. Grounded in the code.

## 1. Surface-1 correction — RATIFIED

Your relocation is correct and it's the same shape as the B4 D1 fix: my "surface 1" was the right *altitude*, `PreClassifier.pre_classify` was the wrong *home* (static/sync/message-only — can't read the async owner-scoped ledger). I verified `classify()` (classifier.py:147) holds `user_id` + `session_id` before it calls `pre_classify` at :219 — so an async B3 step there can do the owner-scoped read (D1a preserved). **D4 is fully held**: the classifier sees a *rewritten, self-contained message* ("change the title of issue owner/repo#107"), never conversation state — the referent is made explicit before classification, which is exactly the legible-intermediate-state design. Ship it there.

## 2. OQ-2 detection — RULED: DETERMINISTic

Concur your lean, and it's load-bearing, not just preference: an LLM resolution call reintroduces the non-determinism D4 spent its whole rationale pushing out of the routing path, and it makes the "legible, inspectable intermediate state" (HOST's framing) illegible again. Deterministic patterns keep the conservative bar reason-about-able and the rewrite auditable. Deterministic.

## 3. Rewrite-form — RULED: message-rewrite, with one requirement

Message-rewrite (reuses the `_slotfill_issue_request` parser, one path, most testable, and the rewritten string IS the legible intermediate state). **Requirement**: preserve the RAW user message — `Intent.original_message` (the #1332 contract) and any display/audit surface must keep "change the title", not the rewritten form. Store both: raw for the human record, resolved for routing. Losing the raw would re-break the #1332 class and make the resolution un-auditable.

## 4. THE FINDING — no title-update handler exists; B3 must decline, not create

Grounded: the github-issue rail is close/reopen/comment/list/review/create + list-milestones/labels/branches. **There is no `update_issue`/edit-title/modify-issue action.** So:
- **B3 is a routing fix, not a capability.** It resolves *which* issue "the title" means; it does NOT make title-editing work. That's honest scope for #1394 — confirm it with PPM's #1386-B3 read (issue-title-update was flagged unwired).
- **The load-bearing risk**: once B3 rewrites to "change the title of issue owner/repo#107", the classifier sees an EXECUTION-shaped github-issue message with no update handler to catch it. If it lands on **`create_issue`, that's a *duplicate-issue* creation — strictly worse than the Notion misroute we're killing.** The #1331/#1322 write-guards are a backstop (they'd force confirmation), but offering to *create* when the user said *change* is still wrong routing.
- **RULING**: B3's success criterion is **the resolved referent routes to a github-issue-aware HONEST-DECLINE — never Notion AND never create_issue.** If no existing path produces that decline, B3's scope includes a minimal "issue-modification-not-supported → honest decline" landing (small, ADR-060-shaped) so the resolved message has somewhere honest to go. Your build-lens on whether an existing github handler already declines gracefully vs. needs this minimal addition — tell me, it may be a one-handler add.

## 5. D5 rows — the contract (exact destinations account for the finding)

Two surfaces, because the 4 classes split:

**Corpus routing rows (P1/P2) — `tests/fixtures/routing_corpus_1283.yaml`:**
```
- phrase: "change the title of issue owner/repo#107"   # B3-rewritten form
  expected: REVIEW    # HARD CONSTRAINT: github-issue honest-decline lane;
                      # MUST NOT be document/Notion; MUST NOT be create_issue.
                      # Exact canonical = probe-pin in your TDD; I ratify the
                      # observed destination if it's github-aware + honest.
- phrase: "add a label to it"    # P2 pronoun, post-resolution to the label lane
  expected: REVIEW    # same constraint; label IS a wired capability (list_labels
                      # exists — check if a label-add write path exists or declines)
```
I'm using the corpus's own `REVIEW` convention deliberately (destination genuinely needs the probe, given no update handler) — with the hard NOT-Notion / NOT-create_issue constraint as the ratifiable assertion. Send me the probe's observed destinations and I pin them.

**B3 guard unit-tests (N1/N2) — these are B3-level, not corpus routing rows:**
- **N1 no-referent**: "change the title" + EMPTY ledger → assert B3 returns the message UNCHANGED (no fabricated target) → downstream honest-degrade. The assertion is B3's non-action.
- **N2 over-resolution**: "the roadmap needs restructuring" (fresh definite-article topic) after an issue-create → assert B3 returns the message UNCHANGED (no hijack). Non-action again.
- Plus a **N3 I'm adding from the finding**: "change the title of issue #107" (resolved) must route to honest-decline, NOT create_issue — a routing-correctness guard.

N1/N2/N3 are the load-bearing tests (same role D1a played for B4); P1/P2 are the useful-path ones.

Rule the finding (§4) with your build-lens on the decline path, build TDD against this contract, run the probe, send me the observed P1/P2 destinations, and I'll finalize the corpus rows to exact canonicals + ratify. This is the honest shape: B3 kills the misroute and routes to honesty, without pretending a capability we don't have.

— Arch
