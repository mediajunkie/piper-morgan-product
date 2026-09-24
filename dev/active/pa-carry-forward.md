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

1. **T-axis probe execution — blocked on CXO's pre-registration, not PM (re-verified 09-24:
   nothing from CXO since 09-20, #1468 untouched since 08-07).** CXO (axis owner) handed execution
   to PA per PM's "spend the tokens now" ruling; no deadline; PA won't design or run a round before
   the pre-registered scoring properties land (CXO's own 0-for-3 prediction record on this
   instrument; pre-registration is the stated mitigation). **Asked CXO 09-24 07:3x** whether the
   T-own/T-MCP split proposal has gone to PM and supersedes the pre-registration — if so this row's
   blocker becomes *PM's split ruling*, and it will be re-labelled the moment CXO answers.

*(Resolved 09-23, removed per CIO's rule: **BYOC Phase B** — PM approved the recommendation
directly; execution notice sent to Exec/Pard, nothing further PM-gated here. **Registry gaps**
(Loom, Vergil/OpenLaws) — PM is discussing directly with Janus, not waiting on PA. **Usage-
correlation model's two blockers** — Pard's 09-23 answer closed BOTH, including the seat→account
mapping PM had been asked for: it's a function of `CLAUDE_CONFIG_DIR`, all 11 PM seats on one
account. PM needn't answer that question now. Build dispatched, #1862.)*

## Current state

- **Usage-per-account capture — LIVE and already earning its keep.** LaunchAgent
  `com.xian.usage-capture` (Pard), every 3h at :23; 14 rows by 09-24 06:23. **First real
  SHAPE-CHANGED caught 09-24 00:23** — the unpublished endpoint served a 200 with an unrelated
  document for DinP, back to normal by 03:07; the keys-in-the-note idea made it distinguishable
  from the 18:23 transient. Writer fixed 09-24 07:2x (`33a0e200b2`) to pass any reader mode label
  through instead of flattening to UNMEASURABLE; driver picks it up via `--ff-only` at 09:23.
  Fallback (manual paste) stays. **Next for PA, trigger = data volume**: first *calibrated*
  correlation-model pass once ~a week of rows exist (~09-30).
- **Model drift on this seat, 09-23**: silently Sonnet 5 → Fable 5.1 at 13:01 PDT (rate-limit
  window; Exec's 11-seat instrument found comms/exec/pa all moved). Observed and logged at the
  time; still Fable 5.1 at 09-24 07:12 START, so not self-reverting. Allocation is PM's call (Exec put it to
  PM directly — not duplicated in PM Attention above); relaunch-restores-Sonnet is Pard's to test.
  Keep the co-author trailer honest so the drift stays visible in `git log`.
- **Fire lag, +30 min, cohort-wide**: PA/CIO/Exec all exactly +30 on every fire since ~09-23
  midday, across different expressions and re-arm histories (re-arm crossed out). PA's 09-24
  06:42→07:12 makes four. Thread is CIO's/Pard's; PA contributes fire-open `date` only.

- **BYOC — active focus.** Phase A: naming-test **four passes run** (09-22 ×2, 09-23 ×2) —
  finding, recorded as a comment on #1462 (UQ-14): situation-shaped naming helps specifically for
  purpose-ambiguous phrasing, shows no advantage where the distinguishing feature is concrete
  (time-cue pair: 6/6 both ways); supports a *mixed* catalog, not a rename-everything. Further
  passes (GPT arm, more pairs) are a PM cost/value call, not self-evidently worthwhile. **Phase B:
  APPROVED 09-23, notice delivered direct to Pard, decisions.log entry landed** — watch for
  execution. **Phase C**: the real build track is PPM's "MCP-path increment 1–8" series
  (#1701–1707, Production milestone) — reconcile with it before any prog dispatch; not PA's to
  re-sequence. Checklist: `dev/active/byoc-hosted-alpha-readiness-checklist-2026-09-15.md`.
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
## GitHub-criteria line (third work-queue source, v1.33) — DEFINED 2026-09-23

Two cheap queries, matching the two halves of PA's lane (ROSTER: skunkworks PoC coordination +
PM-bandwidth extension). **Open every hit with `gh issue view N` before writing a row anywhere**
— a list is a fragment (CXO's finding).

1. **Skunkworks/BYOC**: open issues referencing the hosted-MCP epic —
   `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+%221462%22"`.
   Denominator 2026-09-23: **12** (epic + increments #1701–1707 + #1514/#1509/#1632). Action on a
   NEW number: read it; update the readiness checklist / parallel-work plan if it changes
   sequencing or ownership; add to PM Attention only if it's genuinely PM-gated.
2. **PM-bandwidth**: `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+label:awaiting-decision"`.
   Denominator 2026-09-23: **0** — the label exists but nobody applies it; an empty source is a
   fact, not a failure. Action on a hit: verify it's PM-gated, then PM Attention above.

Seen-set lives in `dev/state/pa-gh-criteria-seen` (not sprint-cleaned); "newly observed" = in
today's query, absent from the file. Rejected alternatives, so nobody re-derives them:
`label:mcp` (5 stale pre-PDR-006 DIST issues — wrong era), free-text `byoc OR mcp` (24 hits,
half unrelated).
