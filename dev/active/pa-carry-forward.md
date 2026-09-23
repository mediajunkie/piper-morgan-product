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

1. **Usage-correlation model — PM confirmed 09-23 it should get built (PA+prog, not Arch);
   blocked on one fact now.** Lead's `usage-per-account-capture-2026-09-19.md` proposal.
   **(1) seat→account mapping — asked PM directly 09-22, still awaiting.**
   **(2) usage-readability/Dispatch question — RESENT DIRECTLY to Pard's real inbox 09-23** per
   PM's explicit instruction to deliver Pard's mail directly to `mediajunkie` rather than via
   Exec-relay (`mediajunkie` commit `26f4c03`, pushed). Full detail: `pa-standing-items.md` #3.
2. **T-axis probe execution — blocked on CXO's pre-registration, not PM.** CXO (axis owner) handed
   execution to PA directly per PM's "spend the tokens now" ruling; explicit no deadline, and PA
   shouldn't design or run a round before CXO's pre-registered scoring properties land. Worth PM
   knowing the token-spend ruling hasn't started spending yet, for a real reason (CXO's own
   0-for-3 prediction record on this instrument; pre-registration is the stated mitigation).

*(Resolved 09-23, removed per CIO's rule: **BYOC Phase B** — PM approved the recommendation
directly; execution notice sent to Exec/Pard, nothing further PM-gated here. **Registry gaps**
(Loom, Vergil/OpenLaws) — PM is discussing directly with Janus, not waiting on PA.)*

## Current state

- **BYOC — active focus.** Phase A: naming-test **three passes run** (09-22 first pass +
  independent-author control, 09-23 targeted follow-up, PM-approved) — sharpened finding:
  situation-shaped framing gives a real, replicated disambiguation benefit specifically for
  ambiguous user phrasing, not a general naming advantage. Full results:
  `dev/active/probes/RESULTS-naming-test-first-pass-2026-09-22.md`,
  `-control-2026-09-22.md`, `-followup-2026-09-23.md`. **Phase B: APPROVED by PM 09-23** —
  execution notice sent to Exec (relay to Pard), nothing further needed from PA.
- **PA's own briefing refreshed 09-22** (`docs/briefing/BRIEFING-piper-alpha.md`) — Docs flagged
  it 6 weeks stale, fixed same-day with live-verified facts (version, GitHub milestone counts, Fly
  hosting migration, team/account structure).
- **Mail-routing lesson, 09-23**: `mailboxes/pard/` in this repo is gravestoned (09-12) — Pard's
  real inbox is external (`mediajunkie/docs/mail/`). Default to Exec-as-relay per
  `docs/internal/operations/cross-project-mail-routing.md`, **except when PM explicitly directs
  direct delivery** — PM did so 09-23 (both the usage-readability question and the Phase B notice
  were then written and committed directly into `~/Development/mediajunkie` via `git -C`, matching
  that repo's own commit/frontmatter conventions, not `mail-send.sh`). Treat Exec-relay as the
  default, direct delivery as PM's to authorize case-by-case.
- **#1458** (pre-live cross-caller state isolation, blocks multi-tenant serving) — re-verified
  `OPEN` via `gh issue view` 2026-09-22. Not started; belongs with the implementation epic. Watch
  for epic optimism compressing it — the failure mode is silent and cross-tenant.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
- **Known gap, named not fixed**: PA has no defined GitHub-issues criteria line (v1.33's third
  work-queue source) — worth a deliberate pass on a quiet day rather than an ad hoc invention
  under fire pressure.
