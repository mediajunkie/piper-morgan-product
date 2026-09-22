# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

> **Spring-cleaned 2026-09-22** per PM's context-floor-reduction directive (item 4a,
> `docs/internal/operations/context-floor-reduction-plan-2026-09-21.md`) — cut from 538 lines to
> this. Everything removed was resolved, superseded, or duplicated in a session log / memory /
> `pa-standing-items.md` already; nothing here was live state. Full prior history: git log on this
> file, or the dated session logs it references.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only.)*

🔴 **PM-GATED, genuinely open:**

1. **Usage-correlation model — Q1 still open.** PM tasked PA (via Exec, no deadline) to build a
   real model of what correlates with usage instead of hand-waving, prior art first. Prior-art
   pass + first empirical pass both done
   (`dev/active/usage-correlation-model-prior-art-2026-09-20.md`,
   `dev/active/usage-correlation-model-first-pass-2026-09-21.md`). **Q1, sent 09-20 19:21, still
   open**: does Lead's `usage-per-account-capture-2026-09-19.md` proposal (the calibration
   mechanism for the engagement axis, zero rows captured) get implemented — without it no model
   here can ever be calibrated on that axis, only internally consistent. Full memo:
   `mailboxes/pa/sent/question-pa-to-exec-cc-pm-calibration-shape-for-usage-model-and-leads-
   unimplemented-proposal-2026-09-20.md`.
2. **T-axis probe execution — blocked on CXO's pre-registration, not PM.** CXO (axis owner) handed
   execution to PA directly per PM's "spend the tokens now" ruling; explicit no deadline, and PA
   shouldn't design or run a round before CXO's pre-registered scoring properties land. Worth PM
   knowing the token-spend ruling hasn't started spending yet, for a real reason (CXO's own
   0-for-3 prediction record on this instrument; pre-registration is the stated mitigation).

## Current state

- **BYOC Phase B (`mcp.pipermorgan.ai` DNS/TLS)** — still not deployed, corroborated two
  independent ways (PA's own DNS/TLS check; CXO's code-side check that `services/mcp/` is
  consumer-only). No false deadline on the recomposition/honest-decline retest.
- **#1458** (pre-live cross-caller state isolation, blocks multi-tenant serving) — re-verified
  `OPEN` via `gh issue view` 2026-09-22. Not started; belongs with the implementation epic. Watch
  for epic optimism compressing it — the failure mode is silent and cross-tenant.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
- **Known gap, named not fixed**: PA has no defined GitHub-issues criteria line (v1.33's third
  work-queue source) — worth a deliberate pass on a quiet day rather than an ad hoc invention
  under fire pressure.
