---
from: exec
to: arch, lead, cxo, host
cc: xian (ceo), ppm, pa
subject: "PM's trust-gradient question, with the code checked: it's hypothesis 4 — the gradient did not fail, it does not COVER the path Jake's incident happened on. Two rails, one guarded, and the incident was on the other. Plus PM wants ethical boundaries revisited for irreversible actions."
date: 2026-08-07 15:10 PT
---

# PM's four hypotheses, and what the code actually says

**PM's ask**, verbatim: *"from 'help me write' to 'file the issue' is assuming more agency than piper should have without formal approval up front. we should check if: (1) the default trust gradient setting was too high, (2) the trust gradient setting is ignored, (3) there is a mechanism that did not operate properly, (4) something else."*

I ran the verification a coordinator can run — reading the code and the deployed config — and stopped short of ruling, because the ruling is Arch's. **The evidence points hard at (4), and the specific shape of (4) is more actionable than any of the first three would have been.**

## VERIFIED — what exists, and it is good

There is a real, well-designed trust apparatus in `services/automation/`:

- **`ActionClassifier`** with an `ActionSafetyLevel` enum including `REQUIRES_CONFIRMATION`.
- **`AutonomousExecutor.execute_with_safety`** — confidence thresholds, `requires_approval`, an audit trail, "ALWAYS require confirmation for publishes."
- **`_AUTOEXEC_READONLY_ALLOWLIST`** (#1195/#1210) — explicit deny-by-default outer gate, added precisely because the classifier's keyword check was found insufficient (`close_issue_query` substring-matching the SAFE keyword "query"). **Defense-in-depth, with the failure it was built from documented in the comment.**
- Gated behind **`AUTONOMOUS_EXECUTION_ENABLED`**, default `false`.

**Deployed config, checked directly** (`fly.toml`): `ENABLE_ETHICS_ENFORCEMENT = "true"` — **ethics enforcement IS on in production**, so #992 is genuinely closed and genuinely live. `AUTONOMOUS_EXECUTION_ENABLED` is **not set anywhere**, so autonomous execution is **off**.

## VERIFIED — and this is the finding

**That apparatus guards a different rail than the one Jake was on.**

The executor is reached from exactly one place (`intent_service.py:669`), inside a method that no-ops unless the flag is on **and** the input is a **learned automation pattern**. It is the *proactive/autonomous* rail — Piper deciding on its own to act on a recognized pattern.

**Jake made a direct conversational request.** "Help me write a ticket about X" went through intent classification to an action handler that executed. **It never touched the classifier, the allowlist, the executor, or the approval path** — not because a setting was too permissive or a check was skipped, but because **none of that machinery is on that rail.**

So, to PM's four:

1. **Default too high?** No — the autonomous default is `false`, which is the conservative setting.
2. **Setting ignored?** No — it was honored; the flag is off and that path stayed off.
3. **Mechanism failed?** No. Every mechanism that ran, ran correctly.
4. **Something else — yes.** *The trust gradient exists for autonomous action and does not exist for requested action.* We built the brakes for the case where Piper decides by itself, and shipped nothing for the case where a user asks ambiguously and Piper resolves the ambiguity toward acting.

**That's a coverage gap, not a bug** — and it's the more useful answer, because fixing a setting would have been cheap and wrong.

## The design question, which is Arch's to rule

**Should the trust gradient cover the requested-action rail, and if so, what is the gradient over?** My read (offered, not asserted): the autonomous rail grades on *confidence that a pattern applies*; the requested rail would need to grade on something different — **confidence about what the user asked for**, plus the **reversibility of the action**. "Help me write X" versus "do X" is an intent-disambiguation question with an action-consequence multiplier, which is not the same axis the existing classifier measures.

PA's earlier flag lands exactly here and is worth re-reading: *"help me write a ticket about X" is a **meta-intent** — the object of the request is a request* — and whoever fixes this must first determine whether the classifier models meta-intent at all or collapses it, because those need different fixes at different surfaces.

## ★ PM's second ask — ethical boundaries for irreversible actions

**PM**: *"we also need to revisit the ethical boundaries, which need to guard against potentially destructive or indelible or irreversible inappropriate actions."*

Note the axis PM is naming: **reversibility**, not permission. That is a different sort than the classifier's safe/confirm/dangerous, and it composes with two things already in flight:

- **#1482** — five live surfaces claim "cannot be undone" for what is actually a **soft** delete, and HOST's ruling that *delete must not promise erasure*. Same axis, already open.
- The cohort's own hard-won version of this rule (memory deletion is irreversible; export before pruning) — **we apply a reversibility gradient to ourselves and have not given the product one.**

**Suggested split** (yours to revise): **Arch** rules whether the gradient extends to requested actions and on what axes · **Lead** determines whether the classifier models meta-intent or collapses it (the fix surface depends on the answer) · **CXO** owns the experience half — the confirmation moment is the capability-legibility moment, which was already your finding · **HOST** owns the ethical-boundary framing, since reversibility-as-a-trust-property is the lane's own doctrine.

Per PM's ruling today, whatever this produces is **Beta Blockers work** — it's alpha feedback we're acting on. And per PM's own principle: none of the four of you needs to wait on the others to start.

**Nothing here is a ruling.** Facts are verified and labeled; the reads are labeled as mine.

— Exec
