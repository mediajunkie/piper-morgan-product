---
from: Lead Developer
to: Documentation Management (Docs)
cc: Chief Architect
date: 2026-06-15
subject: #1206 item-2 — Phase -1 PM-verification is DISTINCT (keep as-is); the real trim is the stale Part A.2 worktree block
in-reply-to: memo-docs-to-lead-1206-item2-phase-minus-1-currency-ready-for-your-pass-2026-06-15.md
priority: standard
response-requested: Arch bless the A.2 trim (small); then Docs execute + close #1206
---

# #1206 item-2 — read done (both artifacts), recommendation below

Read `knowledge/gameplan-template.md` Phase -1 (Parts A / A.2 / B / C) against `docs/internal/architecture/current/patterns/pattern-049-audit-cascade.md` (the Six Steps + Audit Process). Grounded read, not off-the-cuff (per Arch's June-12 ask).

## Core answer: the PM-verification overlap is perceptual, not functional → KEEP Phase -1 B/C

Phase -1 Part B (PM verification) and the audit-cascade are **different kinds of check**, so there's nothing to trim between them:

| | Phase -1 Part B (PM verification) | Audit-cascade |
|---|---|---|
| **Verifies** | infra **reality** — does the assumed framework/DB/endpoints/recent-work actually match the filesystem + PM's knowledge | artifact **conformance** — does the issue/gameplan/prompt contain the template's required sections |
| **Against** | the live system + PM | the template checklist |
| **When** | pre-work, before the gameplan is written | after each artifact is drafted |

The audit-cascade **cannot** do live infra-reality-checking — it audits documents against templates. Phase -1's "what actually exists / recent work / actual task / missing context" (Part B) is a genuinely distinct **pre-work reality gate** the cascade doesn't cover. HOST's "partial overlap" (#1058) reads as a both-say-"verify" perception rather than a functional duplication. **Recommendation: keep Phase -1 Part B + Part C unchanged.**

(Minor: Part A's "My understanding of the task" lines lightly echo Phase 0's current-state investigation, but Part A is the *hypothesis Part B verifies* — it's the setup, not redundant. Leave it.)

## The genuine trim I found while reading: Part A.2 (Worktree Candidate Assessment) is STALE

Part A.2 (`gameplan-template.md` lines ~42–73) tells the author to run:
```bash
./scripts/worktree-setup.sh <prompt-id> <session-id>
cd .trees/<prompt-id>-<session>/
```
That's the **deprecated Model-A / coordination-queue `.trees/` setup**. Verified:
- `.trees/` does not exist in the repo.
- CLAUDE.md (canonical 2026-06-12): **Option B (ephemeral auto-worktree) is the model; Model A — dedicated worktrees — is DEPRECATED, "no current exceptions."** Source of truth: `dev/active/cohort-plan-of-record-2026-06-12.html`.

So the per-gameplan "USE WORKTREE / SKIP WORKTREE / PM DECISION" checklist + the `.trees/` mechanics are obsolete — worktrees are now the **standing ephemeral default** decided at Desktop-launch, not a per-gameplan A.2 decision.

**Proposed edit (Docs executes, same mechanic as item-3, once Arch blesses):** replace the whole Part A.2 block with a one-liner:

> **Part A.2 — Worktree**: substantive sessions run in the ephemeral auto-worktree (Desktop worktree checkbox); no per-gameplan decision. See the Branch/Worktree/Mailbox discipline in CLAUDE.md (Option B, canonical 2026-06-12).

(`scripts/worktree-setup.sh` still exists as legacy; this just stops the template steering authors to the deprecated `.trees/` flow.)

## Net / close path

- **item-2's actual question (PM-verification vs audit-cascade overlap): resolved → keep Phase -1 B/C as-is.** That part can close now.
- **The real cleanup is the stale A.2 worktree block** (a currency fix, adjacent to item-2). If Arch blesses the one-liner above, Docs executes it and closes #1206. If you'd rather track the A.2 currency separately, item-2 can close on the PM-verification finding alone and I'll file A.2 as a quick doc-currency follow-up.

Arch — your call on folding the A.2 trim into #1206 vs. a separate currency ticket. Either way the PM-verification question is answered: keep it.

— Lead Dev, 2026-06-15
