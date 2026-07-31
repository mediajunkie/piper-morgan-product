# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> **Rewritten wholesale 2026-07-26 ~14:00, first PA session on Amber.** The prior version was dated
> **2026-06-17 — 38 days stale** — and described a DinP account, a Model-B ephemeral worktree, and a
> BYOC-era task list that no longer exists. Per CIO's rule: **resolved items are deleted here, not
> annotated**; the dated session logs are the permanent record. A stale carry-forward is worse than
> an absent one, because it reads as current — that warning in CIO's orientation note is exactly what
> saved this file from being trusted.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-07-30 PM.)*

- 🔴 **PDR-006 IS READY FOR YOUR RATIFICATION. All three reviews in, all RATIFY, no objections** —
  Arch 7/29, CXO 7/30, PPM 7/30. A PDR is PM-ratified; the reviewers are done and the decision is yours.
  **Nothing is blocked on the signature** — PA is working Phase 0 either way.
  *Worth 30 seconds before signing*: the reviews found a **defect in the document's own success
  criteria** — all three originals were *setup* criteria and none could fail for "installed fine,
  answered correctly, demonstrated nothing," which is Jake's session exactly. **Same defect class as
  #1386's beta gate**, from the other direction. One binary criterion added (cold account + one
  connector → user's own data in the first exchange, unprompted); it's the only one that fails today.
  ⚠️ **Ratified ≠ shippable**: #1458 (cross-caller isolation) and the recomposition rubric gap both
  remain open as pre-user gates.
- ⏰ **OpenAI identity verification — still the only PM ACTION outstanding, and still unstarted.**
  PM committed to Thu 7/30; not done as of this writing. **platform.openai.com → Settings →
  Organization → General → "Verify Organization"** — government ID, a few minutes. The only item with
  an **external clock**; gates the ChatGPT lane and nothing else gates it.

### Closed since 7/29 — no PM action

- ✅ **Team upgrade DROPPED** (chat installs plugins on all paid plans; plugins bundle connectors).
- ✅ **"Open-source decision" never existed — the repo is already public.**
- ✅ **#558 stays in Production** (PPM): you cannot get colleague-model feedback from users who bounce at
  first contact, so it is gated behind cold-start. *Explicitly a sequencing call — if overridden, the
  spatial coupling returns immediately.*

### Context PM may want when these come up

**Submission is gated on build, not decisions.** Verified rather than restated: **`mcp.pipermorgan.ai`
is not deployed** (exists only in PDR-006 and planning docs) and **no public privacy policy page exists**
— a missing privacy policy is an *immediate rejection* on both directories. So the earliest realistic
submission is weeks out regardless, and **OpenAI verification is the one thing whose clock runs
independently of all of it** — which is why it stays the single ⏰ item.

⚠️ **Standing caution for this whole thread, earned three times over.** The tier answer was wrong twice
in opposite directions; the open-source "decision" was carried as open for ten days after PM had
answered it repeatedly; Q2 blocked PDR-006 for ten days after PM had ruled on it in January. **Every one
was a claim inherited from a document and never checked against the source** — `gh repo view`,
`gh issue view`, the actual code. All three were 30-second checks. **Before restating anything on this
thread, verify it.** *(And per PM 7/29: the platform story here changes fast — a correct answer from four
days ago is not a current answer.)*

## Active state — 2026-07-30 STOP (next wake 06:42 Fri 7/31)

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` (Model A) · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/07/30/2026-07-30-0712-pa-code-log.md` — **DAY-CLOSED 2026-07-30**
- **Cron**: ARMED at STOP via delete-then-create. **Job id is in the registry row — read it there.**

  🔴 **FIRST ACTION ON ANY NEW SESSION: run `CronList`.** Empty = **you are not cycling**, whatever the
  registry says. Jobs are **session-only** and **auto-expire after 7 days** — this generation lapses
  **~2026-08-06**. Both deaths are silent and look exactly like a quiet day. **The registry records
  intended cadence, not a live job.** *Approval to run a cadence and arming it are two separate acts.*
- **Inbox**: 0 at close.

## ▶️ First substantive item tomorrow (deferred with a named trigger, not drifting)

**Run the two client-LLM probes.** Both green-lit by their verdict-owners — CXO on A, PPM on B. Spec:
`dev/active/phase0-client-llm-probe-spec-2026-07-30.md`. Deferred from 7/30 STOP *because a designed
experiment started inside a day-close fire ends half-run, and a partial experiment invites its fragment
being read as a result.* Trigger named: **06:42 START.**
⚠️ Design constraints, carried from this week's own failures: **keep tool schemas identical across B's
arms** (vary only names/descriptions — otherwise the arms differ in more than the variable, the confound
that cost five seats and a week); **run A against both Claude and GPT** (a divergence is itself a
ChatGPT-lane finding).

**Second**: file the cron-mechanism gap to CIO. **Owed since 7/29 and dropped once already** — no durable
cohort record exists of *which* cron mechanism we use (session-scoped `CronCreate`) or its two silent
death modes. It has now appeared in two consecutive memory-evals. Don't re-promise it a third time.

## Open threads PA owns

1. 🟢 **PDR-006 — ALL THREE REVIEWS IN AND RATIFYING. Routed to PM 7/30; awaiting PM ratification.**
   Nothing is blocked on the signature. **Next PA action: none — do not chase PM.** If ratification lands,
   PPM drafts the implementation epic (theirs, offered).
2. 🔵 **Phase 0 distribution work — PA's active lane, nothing blocked.** Plan + per-item state:
   `dev/active/distribution-submission-tiers-resolved-2026-07-26.md`.
   ✅ privacy policy drafted (`docs/legal/privacy-policy-DRAFT.md`, 5 open 🔍 markers needing PM: contact
   address, deletion/export reality, retention, sub-processor completeness, security claims).
   ⬜ **next**: tool-annotation spec — **now carries product weight, not just `readOnlyHint`/`destructiveHint`**,
   because PPM established the catalog is where opinionation lives · `claude plugin validate` dry-run ·
   public docs page · ChatGPT 5-positive/3-negative test cases.
3. 🟢 **Client-LLM probes — GREEN-LIT BY BOTH VERDICT-OWNERS, unblocked, PA's to run.**
   CXO: *"PA — yes on Probe A."* PPM: *"take it… one rig, two questions, Phase 0."*
   Spec: `dev/active/phase0-client-llm-probe-spec-2026-07-30.md`. **A** = does our honesty survive
   recomposition by the client LLM (CXO reads the result). **B** = do situation-shaped tool names route
   worse than object-shaped (PPM + Lead/Arch read it). **Neither needs the server.** Both results change
   what the tool layer emits, so they precede Phase 2. ⚠️ Keep schemas identical across B's arms; run A on
   **both** Claude and GPT. **Not started.**
4. **#1458** — pre-live cross-caller state isolation; blocks multi-tenant serving. Not started; belongs
   with the implementation epic. PPM: don't let epic optimism compress it — the failure is silent and
   cross-tenant.
5. **Recomposition rubric gate** — the second pre-user gate, and **prose-only, unlike #1458 which has a
   number.** PPM asked CXO whether to file it; **a gate that isn't an issue isn't tracked.** Watch that it
   gets a number.
6. **Architecture-diagram discussion** — PM-requested, awaiting a time. `pa-standing-items.md` #2. Prep,
   don't pre-empt: PM asked to discuss, not for a revision.
7. **PA's lessons / load-bearing-vs-commodity write-up** — still owed; the gap CIO's orientation note
   named. Not written.

## Inbox

7 unread at session start. Triaged: the Exec handoff-prep ask (7/21), Arch's PDR-006 ack, CIO's
duty-cycle-tick v1.15 memo, PPM's spatial-lane accept, three WS-052 submissions (context-only), plus
CXO's and PPM's hook memos which arrived mid-session and were answered in the synthesis.
