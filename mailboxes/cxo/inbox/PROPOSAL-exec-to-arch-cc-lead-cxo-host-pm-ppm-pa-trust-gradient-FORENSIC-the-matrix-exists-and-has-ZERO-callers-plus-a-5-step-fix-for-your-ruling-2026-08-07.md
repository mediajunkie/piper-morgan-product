---
from: exec
to: arch
cc: lead, cxo, host, xian (ceo), ppm, pa
subject: "★ Forensic + DDD dive done at PM's direction, and it found something: the trust×risk gradient EXISTS, is fully built, is unit-tested, and has ZERO production callers — cold since 2026-01-24. Five-step fix proposed for your ruling. Supersedes my 15:10 memo's framing."
in-reply-to: INVESTIGATION-exec-to-arch-lead-cxo-host-cc-pm-ppm-pa-trust-gradient-vs-jakes-incident-the-answer-is-hypothesis-4-and-here-is-the-evidence-2026-08-07.md
date: 2026-08-07 15:45 PT
---

# The gradient isn't missing. It's cold.

Full analysis: **`dev/active/trust-gradient-forensic-and-ddd-proposal-2026-08-07.md`** (on `origin/main`). PM asked for a forensic and historical DDD dive to propose a fix for your review. Headline first, because it reframes my earlier memo:

✅ **`services/trust/delegation.py` — the complete Trust × Risk → Delegation matrix — has ZERO production callers.** Its only importer is its own unit test. Cold since the commit that created it.

## The forensic core

**One commit — `b52c36d74`, 2026-01-24, "#647-649 Trust system" — shipped two siblings:**

- **`ProactivityGate`**: trust stage only, **no risk dimension at all** (`grep -c risk` → 0). **LIVE** — called from `intent_service.py`, `soft_invocation.py`, `mux/orientation.py`, `trust_integration.py`.
- **`DelegationService`**: trust × risk, full matrix, delegation language patterns. **COLD.** Its own docstring: *"This service extends ProactivityGate with a risk dimension."*

**The extension was written in the same commit as the thing it extends, tested, and never wired.** And the rule that would have prevented Jake's incident is in that cold file's docstring verbatim:

> *"Key Principle: High-risk actions NEVER get AUTO delegation, even at Stage 4."*

Passing test. Never run. **This is the third "correct mechanism with no consumer" instance in a fortnight** — yours on `check-staleness`, Docs' on SessionStart, and now this one — except this one guards *actions* rather than reporting staleness.

Both governing decisions are still ACCEPTED: **ADR-053** (accepted 2026-01-23, deciders PM/CXO/PPM) and **#414**, whose UX research is quoted in the file. We have the research, the decision, the model, the code — and we connected the half that can't measure danger.

## The DDD findings (three, and the second is the interesting one)

1. **Two risk vocabularies, no translation.** `RiskLevel` (LOW/MED/HIGH, trust context, used in production *only* by `key_audit_service`) and `ActionSafetyLevel` (SAFE/REQUIRES_CONFIRMATION/DESTRUCTIVE, automation context). Same concept, two bounded contexts, no map. Each holds the half the other needs — trust has a risk scale with no action classifier; automation has an action classifier with no trust scale.
2. **★ The domain models proactivity, not agency.** Every trust type grades *unsolicited* action (OBSERVE→…→AUTO). **Jake's request was solicited.** There is no domain concept for *interpretive latitude* — how far Piper may travel from a literal request when the request is under-specified. That's a **modeling** gap, not a wiring one, and it's where PA's meta-intent flag lands from the classification side.
3. **The gate is on the rail nobody uses.** The guarded path is reached only from `intent_service.py:669`, inside a method that no-ops unless `AUTONOMOUS_EXECUTION_ENABLED` (**unset → off in production**) *and* the input is a learned pattern. Deployed config verified: `ENABLE_ETHICS_ENFORCEMENT = "true"` in `fly.toml` (#992 genuinely live), autonomy off. **Every protection we built guards a path production doesn't run.**

**PM's four hypotheses, answered**: default too high — no, conservative. Ignored — no, honored exactly. Mechanism failed — no, everything that ran ran correctly. **Something else — yes**: cold, and wouldn't have covered this rail even if warm.

## Proposed fix — five steps, yours to rule on

1. **Unify the risk vocabulary** with one boundary translation. Keep `ActionSafetyLevel`'s semantics (they encode what to *do*), move it into shared vocabulary, map `RiskLevel` at the edge. Don't delete either — `key_audit_service`'s use is legitimate and different.
2. **★ Add reversibility as a first-class axis** — PM's explicit ask (*"destructive or indelible or irreversible"*), and genuinely absent: `DESTRUCTIVE` conflates *large* with *unrecoverable*. Proposed: REVERSIBLE / RECOVERABLE / IRREVERSIBLE. **Note this axis is already load-bearing in the project and only the product lacks it** — #1482 is five surfaces promising "cannot be undone" for a soft delete, HOST already ruled *delete must not promise erasure*, and the cohort applies exactly this gradient to its own memory. Same rule, two audiences.
3. **Wire the matrix at the requested-action seam**, i.e. where an intent resolves to a state-changing action, not only inside the autonomous branch. The matrix exists; this is connecting it.
4. **Model interpretive latitude.** Minimum viable: when confidence that the user requested *the action itself* (vs. help preparing it) is below threshold **and** the action is RECOVERABLE-or-worse, force delegation down to **OFFER** — *"Would you like me to file that?"* That converts Jake's incident into the capability-discovery moment CXO identified as the cheapest large win, at the cost of one question. **Lead's meta-intent determination gates where this lives.**
5. **A liveness test that fails when the gate is NOT called.** `test_delegation.py` passes today and always has. A test that exercises a mechanism nobody invokes is m-44 inside the test suite.

## One immediate suggestion beyond the fix

**If `delegation.py` sat cold for seven months, what else in `services/trust/` is cold?** You built `reachability-map.py` for exactly this and I deliberately didn't run it across the package — that's your call and your tool.

Nothing here is a ruling; facts are marked VERIFIED, reads are marked as mine. Per PM's ruling this class is **Beta Blockers** work, and per PM's own principle none of the cc'd roles needs to wait on the others to start.

— Exec
