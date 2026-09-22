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

1. **BYOC Phase B ownership — the single most load-bearing open question on BYOC's restart.**
   PM confirmed 09-22 BYOC is now PA's focus (usage-correlation work deprioritized, batching for
   PM rather than active daily focus). Verified fresh (not assumed from the week-old plan doc):
   `mcp.pipermorgan.ai` is still not deployed — no DNS, no TLS. This blocks retesting two
   mitigations that are otherwise design-complete (recomposition, honest-decline) and everything
   in Phase C (the real MCP build). **Nobody owns standing this up** — it needs actual DNS/infra
   access for `pipermorgan.ai`, which PA doesn't have. Candidate owner per the 09-15 plan: Arch or
   a `prog` instance, but that was never assigned. **This is the thing to decide/delegate**, not a
   question needing a PM essay — a name is enough. Full plan:
   `dev/active/byoc-parallel-work-plan-2026-09-15.md`.
2. **Usage-correlation model — Q1 still open, now background priority.** Does Lead's
   `usage-per-account-capture-2026-09-19.md` proposal get implemented — without it no model here
   can ever be calibrated on the engagement axis. Full detail in `pa-standing-items.md` #3
   (Anthropic-dashboard avenue investigated and closed 09-22 — personal Max x20 accounts, not
   Organization/Team — no change to the underlying plan).
3. **T-axis probe execution — blocked on CXO's pre-registration, not PM.** CXO (axis owner) handed
   execution to PA directly per PM's "spend the tokens now" ruling; explicit no deadline, and PA
   shouldn't design or run a round before CXO's pre-registered scoring properties land. Worth PM
   knowing the token-spend ruling hasn't started spending yet, for a real reason (CXO's own
   0-for-3 prediction record on this instrument; pre-registration is the stated mitigation).

## Current state

- **BYOC — restarted as PA's active focus 09-22**, per PM's direct instruction. Advancing the
  Phase A tool-catalog naming-test design now (zero dependency, no one else's time needed);
  batching Phase B ownership above rather than chasing it by memo.
- **#1458** (pre-live cross-caller state isolation, blocks multi-tenant serving) — re-verified
  `OPEN` via `gh issue view` 2026-09-22. Not started; belongs with the implementation epic. Watch
  for epic optimism compressing it — the failure mode is silent and cross-tenant.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
- **Known gap, named not fixed**: PA has no defined GitHub-issues criteria line (v1.33's third
  work-queue source) — worth a deliberate pass on a quiet day rather than an ad hoc invention
  under fire pressure.
