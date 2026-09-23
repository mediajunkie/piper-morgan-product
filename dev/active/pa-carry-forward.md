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

1. **BYOC Phase B ownership — PA's recommendation sent 09-22, Exec agrees, awaiting PM's decision.**
   PM asked for an actual proposal (Exec relayed, floating "Arch supervising" as one option, not a
   ruling). Checked this week's real hosting-migration mechanics before recommending (the 09-15
   plan's "Arch or prog" framing predates it): Fly.io access is grant-gated, not standing; DNS
   control is PM's directly by a 2026-07-10 standing rule; Pard was this week's sole hands-on
   Fly/DNS executor, with fresh proven context on this exact stack. **Recommendation**: reuse that
   pattern (PM-granted scoped Fly access to Pard) rather than onboard Arch+a fresh prog instance.
   Exec replied agreeing with the reasoning, relayed to PM directly. Full memo:
   `mailboxes/pa/sent/proposal-pa-to-exec-cc-pm-mcp-dns-tls-assignment-recommendation-2026-09-22.md`.
2. **Two small cross-project registry gaps, sent 09-22, low priority.** Janus checked PM's
   from-memory agent list against their canonical registry (`docs/agents/registry.md`,
   `mediajunkie/designinproduct`) — confirmed nearly everything. Two open: **(a)** where is Loom's
   ("Layers of Meta") repo — neither Janus nor PA has a pointer; **(b)** Vergil/OpenLaws — PM's own
   09-12 ("retired") and 09-21 ("in scope for activity record") rulings read as in tension, Janus's
   call for PM to resolve. No urgency stated. Full memo:
   `mailboxes/pa/sent/question-pa-to-pm-cc-janus-loom-repo-and-vergil-status-2026-09-22.md`.
3. **Usage-correlation model — Q1 still open, background priority.** Does Lead's
   `usage-per-account-capture-2026-09-19.md` proposal get implemented — without it no model here
   can ever be calibrated on the engagement axis. Full detail in `pa-standing-items.md` #3
   (Anthropic-dashboard avenue investigated and closed 09-22 — personal Max x20 accounts, not
   Organization/Team — no change to the underlying plan).
4. **T-axis probe execution — blocked on CXO's pre-registration, not PM.** CXO (axis owner) handed
   execution to PA directly per PM's "spend the tokens now" ruling; explicit no deadline, and PA
   shouldn't design or run a round before CXO's pre-registered scoring properties land. Worth PM
   knowing the token-spend ruling hasn't started spending yet, for a real reason (CXO's own
   0-for-3 prediction record on this instrument; pre-registration is the stated mitigation).

## Current state

- **BYOC — active focus.** Phase A: naming-test **two passes run 09-22** — pass 1 found
  situation-shaped 12/12, object-shaped 10/12 with a real same-author confound flagged; pass 2
  (independent-author control, run once PM's usage-directive lifted the cost-caution that had
  deferred it) confirmed one failure was the confound (fixed by better authorship) but the other
  persisted even under a good independent description — net a real, small, honestly-uncertain
  1-point residual gap. See `dev/active/probes/RESULTS-naming-test-first-pass-2026-09-22.md` and
  `dev/active/probes/RESULTS-naming-test-control-2026-09-22.md`. Phase B: recommendation sent, see
  PM Attention item 1 above.
- **PA's own briefing refreshed 09-22** (`docs/briefing/BRIEFING-piper-alpha.md`) — Docs flagged
  it 6 weeks stale, fixed same-day with live-verified facts (version, GitHub milestone counts, Fly
  hosting migration, team/account structure).
- **#1458** (pre-live cross-caller state isolation, blocks multi-tenant serving) — re-verified
  `OPEN` via `gh issue view` 2026-09-22. Not started; belongs with the implementation epic. Watch
  for epic optimism compressing it — the failure mode is silent and cross-tenant.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
- **Known gap, named not fixed**: PA has no defined GitHub-issues criteria line (v1.33's third
  work-queue source) — worth a deliberate pass on a quiet day rather than an ad hoc invention
  under fire pressure.
