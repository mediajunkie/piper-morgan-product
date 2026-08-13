---
from: exec
to: host
cc: xian (ceo)
subject: "PM wants a data-retention policy drafted, and named it your remit — ground truth + open questions + a verified trust claim to build around"
date: 2026-08-13 11:35 PT
---

PM's ask, verbatim in substance: **"We have a strong ethos that should help guide a reasonable scaffolded draft I could review and bless."** I suggested this belongs with trust/safety rather than product or design — PM agreed and named it your remit. This is that handoff.

## The ground truth (verified against the code, not assumed — commit `a75166499`)

**No retention or expiry logic exists anywhere for conversation or message data.** Checked `services/database/`, `services/domain/`, and the product's own background-job scheduler (`services/scheduler/`, plain asyncio). The only automated cleanup job anywhere is `EthicsAuditCleanupJob` (`web/startup.py:451-452`, 90-day retention), and it purges only the `ethics_audit_log` table — decision metadata, unrelated to conversations.

Combined with what was already known (deletion is soft-delete only, `services/database/repositories.py` — the row stays, just gets marked; there is no account-deletion path anywhere in `web/api/routes/`): **today, conversation data is retained indefinitely, with no automatic expiry and no way for a user to fully remove it themselves.**

This is already written into `docs/legal/privacy-policy-DRAFT.md`'s retention section as fact. What's missing is the actual policy — what the practice *should* be, which is your call to scaffold, not something derivable from the code.

## PM's specific framing to build from

1. **Self-hosted deployment changes the whole picture.** When Piper Morgan runs self-hosted, the user is retaining *their own* data indefinitely, with no provider involved at all. The policy needs to distinguish hosted (us as a party to the retention question) from self-hosted (not our data to have a retention stance on) — these are different claims, not one policy with a footnote.
2. **Open question, PM's lean stated but genuinely open**: should there be a default offer to limit retention of data? PM doesn't currently think so, but wants your read if you see it differently — worth actually weighing, not just recording the lean as the answer.
3. **Open question, undecided**: should Piper Morgan provide user-facing data-retention preferences/settings (configurable, not just a fixed policy)?
4. **The part PM called out as potentially more important than the timing question**: **Piper does not apply what it learns from one user to any other user, and does not apply it to Piper Morgan's own core/shared functionality.** Piper isn't designed to learn in a way that's extractive across users, intrusive, or that violates the confidence of what a user has shared. PM wants this stated clearly and prominently — it's a *scope* claim about learning, not just a *duration* claim about storage, and it may be the more load-bearing trust signal of the two.

## What I verified before handing this to you, so you're not drafting on an assumption

**The no-cross-user-learning claim holds for the live production path**, and it's structurally enforced, not just conventional:
- `services/personality/repository.py` and `services/learning/learning_handler.py` (the actual production learning path — confirmed live-called from `services/intent/intent_service.py:1501-1507`) filter every read/write by `user_id`.
- **ADR-079** (owner-scoping integrity contract) makes this CI-blocking, not just a convention someone could quietly break — `scripts/check_unscoped_reads.py` fails the build on an unscoped read against any owner-bearing table, and it generalizes **ADR-075**, which specifically rules on personalization ownership.
- **One real precedent worth citing in the policy itself, honestly**: `#1366` (2026-07-06) was a genuine violation of exactly this claim — an unscoped instance file leaked one user's personalization to every user on a shared alpha instance. Fixed within a day (#1373), and ADR-079's lint now makes the class structurally harder to reintroduce. I'd rather the policy language survive contact with "has this ever actually happened" than assert a purity that isn't quite true — being honest that it happened once and was fixed with a structural guard is a *stronger* trust claim than pretending it never could.
- **One loose end I filed rather than let sit**: dead code (`QueryLearningLoop`/`PredictiveAssistant`) implements the exact cross-user pooling this claim disclaims — unreachable in production today (test-only entry point, HTTP routes commented out and marked deprecated), but present in the repo with nothing guarding against it being reconnected later. Filed as **#1613** so it doesn't become a silent policy violation if someone re-wires it without checking. Worth a line in your draft's methodology, not the user-facing text.

## What I'd suggest, not deciding

A scaffold that (a) states the no-cross-user-learning claim as the headline trust property, with the #1366-and-fixed honesty as a footnote if you want the receipts available, (b) splits hosted vs. self-hosted retention as genuinely separate claims, (c) states current hosted-retention practice as fact (indefinite, no self-service deletion) while PM decides whether that's the practice going forward, and (d) leaves the two open questions above as open questions in the draft rather than pre-deciding them for PM.

No deadline attached — PM wants to review and bless a scaffold, not approve something already locked in.

— Exec
