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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-01 STOP.)*

**Nothing is blocked on PM tonight.** Beta is **Aug 8**.

- 🟡 **One optional convenience, not a blocker: click "Always Allow"** if a macOS keychain dialog is
  sitting on your screen. PA's 19:12 probe queued one or two before diagnosing the cause and stopping.
  **Already worked around** — Lead identified the authorized interpreter
  (`~/Development/piper-morgan-worktrees/lead/venv/bin/python`, which PM stored the keys through), and
  PA ran the probe from it successfully. So this is tidiness, not need.
- ✅ **Keys provisioned 17:27 8/1 — confirmed, and the four blocked lanes are unblocked.**
- ✅ **PDR-006 RATIFIED** 7/31; two pre-user gates tracked as **#1458** and **#1463**.
- ✅ **Architecture diagram redrawn** at PM's request — https://claude.ai/code/artifact/92ce8bc9-23d4-4590-b121-dacc0ab72e17
  (source in git at `dev/active/pdr-006-architecture-2026-08-01.html`, because the July one vanished
  with an account). **PM still owes a time to discuss it** — no urgency named.

### 🔴 The operational finding PM should know, even though it needs nothing tonight

**On an unattended agent seat, an unauthorized keychain read HANGS rather than ERRORS.** Worse than
"absent": absent was loud and got fixed in two days; a hang burns a fire silently and looks like a slow
task. ⚠️ **A Python `SIGALRM` cannot interrupt it** — the block is inside the macOS Security framework,
so any guard must be a **subprocess with a hard kill**, not an in-process alarm. HOST has routed a
bounded-timeout suggestion to CIO. **Server is NOT exposed** on the Anthropic path (HOST static trace:
it reads env, not keychain); **BYOC/user-key features are.**

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

## Active state — 2026-08-01 STOP (next wake 06:42 Sun 8/2)

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/08/01/2026-08-01-0712-pa-code-log.md` — **DAY-CLOSED 2026-08-01**
- **Handoff/lessons**: `dev/active/handoff-pa-2026-07-31.md` — keep current, don't rewrite at departure
- **Cron**: ARMED at STOP, delete-then-create. **Job id in the registry row.** 🔴 **First action any new
  session: `CronList`.** Empty = not cycling. Jobs are session-only and expire ~7d (this one ~2026-08-08).
- **Inbox**: 0 at close.

⚠️ **KEYCHAIN — read this before any probe.** Use the **authorized interpreter**
`/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` (PM stored the items through it).
**Any other binary HANGS on a GUI dialog rather than failing**, and `SIGALRM` will not save you.

## ▶️ First items tomorrow

1. **Probe A arm 2 — the prose-hedge arm.** Arm 1 (5/5 survived) tested caveats in *named structured
   fields*, which is the mitigation, not the risk. **Same five cases with hedges in narrative prose, no
   named field.** That is the arm that answers CXO's question.
2. **Probe A GPT arm.** PDR-006 ships to both; a Claude/GPT divergence is itself a ChatGPT-lane finding.
   `openai_api_key` is provisioned. Arm 1 is half an experiment until this runs.
3. **Probe B** (tool-naming vs selection accuracy) — PPM's verdict. Keep schemas identical across arms.

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
5. ✅ **Recomposition rubric gate — now [#1463](https://github.com/mediajunkie/piper-morgan-product/issues/1463)**
   (filed by PA 8/1 as a **tracking artifact**; CXO had confirmed the branch decision 7/30, PPM asked who
   would file it, and the question went unanswered through ratification + the credential blocker).
   **Design remains CXO's — not pre-empted.** PDR-006's two pre-user gates are now symmetric.
   ⛔ Blocked on the same Amber keys as everything else.
6. **Architecture-diagram discussion** — PM-requested, awaiting a time. `pa-standing-items.md` #2. Prep,
   don't pre-empt: PM asked to discuss, not for a revision.
7. ✅ **PA's lessons / load-bearing-vs-commodity write-up — WRITTEN 7/31**:
   `dev/active/handoff-pa-2026-07-31.md`. Closes the gap CIO's orientation note named. **Written live
   rather than at a handoff, deliberately** — CXO diagnosed 7/30 that a handoff composed under context
   pressure mis-states the author's own finished work. **Keep it current rather than rewriting it at
   departure.**

## Inbox

7 unread at session start. Triaged: the Exec handoff-prep ask (7/21), Arch's PDR-006 ack, CIO's
duty-cycle-tick v1.15 memo, PPM's spatial-lane accept, three WS-052 submissions (context-only), plus
CXO's and PPM's hook memos which arrived mid-session and were answered in the synthesis.
