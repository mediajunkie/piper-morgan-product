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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-07-31 PM.)*

- ✅ **OpenAI verification — RESOLVED 7/31. DO NOTHING. It was the wrong verification entirely.**
  ~~"The only item with an external clock"~~ — **withdrawn.** There are **two** OpenAI verifications:
  **API org verification** (advanced model access; one org per ID per 90 days) — **not on the ratified
  path, not required for a directory listing either**; and **verified developer/business identity**,
  which is what submission actually requires and is *explicitly distinct*. PA pushed the former for
  twelve days. **Arch asked whether it was required at all; PPM confirmed against the ratified text.**
  PDR-006 §Decision item 3 is *BYOC user adds the MCP URL manually* — **the user is OpenAI's customer;
  no org of ours is in that path.** Full answer in **PDR-006 Open Question 3**, not a memo.
  🔴 **New prerequisite recorded there**: MCP connector submission needs **domain-ownership verification
  for `mcp.pipermorgan.ai`** — which doesn't exist yet. Phase-2 dependency.
  ⚠️ **Deliberately unresolved**: whether the developer/identity flow has its own rate limit. Do not
  transfer the 90-day rule without evidence.

- ⚠️ **KEYS ARE PROVISIONED (17:27 PDT 8/1, confirmed by keychain query) — but an unauthorized read
  HANGS INSTEAD OF FAILING.** `piper-morgan/anthropic_api_key` and `openai_api_key` both exist. PA's
  probe-venv Python blocked >2 min, twice, **unresponsive to SIGALRM** → the block is inside the macOS
  Security framework, i.e. a **GUI authorization dialog** nobody is answering. Keychain items are ACL'd
  to the binary that wrote them; every other binary asks.
  🔴 **The operational finding, which outlasts this incident: on an unattended agent seat an
  unauthorized keychain read HANGS, not errors.** Two days of "absent" were loud and got fixed in
  hours; a hang burns a fire silently and looks like a slow task. **Any agent reading the keychain
  needs this in view.**
  ⚠️ **UNANSWERED and more important than PA's probe: does the SERVER's Python hit the same dialog?**
  If so the first LLM call after a restart hangs rather than fails — with beta on **Aug 8**. PA cannot
  test it (no venv in either Piper checkout; homebrew `python3` lacks `keyring`). **One restart answers
  it.** Asked, not asserted.
  **PA has stopped probing** — each attempt may queue another dialog at PM's seat. Unblocks on: PM
  clicking "Always Allow", or naming the binary they used so PA runs from the authorized one.

- ✅ **PDR-006 RATIFIED — PM, 2026-07-31**, *"And yes I do ratify PDR 006."* Recorded by Arch in the
  corpus + `decisions.log`; the three Architect conditions are written **into** the PDR so the
  implementation epic inherits them. **No PA action; no PM action.** ⚠️ **Ratified ≠ shippable** —
  #1458 and the recomposition rubric branch are both open pre-user gates.

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

## Active state — 2026-07-31 STOP (next wake 06:42 Sat 8/1)

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` (Model A) · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/07/31/2026-07-31-0711-pa-code-log.md` — **DAY-CLOSED 2026-07-31**
- **Handoff/lessons doc**: `dev/active/handoff-pa-2026-07-31.md` — **keep current, don't rewrite at departure**
- **Cron**: ARMED at STOP via delete-then-create. **Job id is in the registry row — read it there.**

  🔴 **FIRST ACTION ON ANY NEW SESSION: `CronList`.** Empty = **you are not cycling**, whatever the
  registry says. Jobs are **session-only** and **auto-expire after 7 days** — this generation lapses
  **~2026-08-07**. Both deaths silent, both look like a quiet day. *Approval to run a cadence and arming
  it are two separate acts.*
- **Inbox**: 0 at close.
- ⚠️ **Weekend note**: per `feedback_weekends_are_piper_morgan_prime_time`, Sat/Sun are PM-active. Beta
  target is **Aug 8** — one week out.

## ▶️ First items tomorrow

1. **`CronList`**, then check the keys — `keyring.get_password('piper-morgan','anthropic_api_key')`.
   **If present, run Probe A immediately**: it is green-lit by CXO (A) and PPM (B), the harness is
   committed and runnable at `dev/active/probes/`, and PM authorized the spend 7/31. ⚠️ Keep tool schemas
   identical across B's arms; run A against **both** Claude and GPT.
2. **If keys are still absent**, do not re-escalate — it is in PM Attention, CXO has withheld sign-off on
   #1386 with reasoning posted, and repeating it adds noise rather than pressure. Pick unblocked work and
   say plainly in the fire report that four lanes remain blocked on one step.
3. **Do NOT build ChatGPT submission test cases or a directory-listing checklist.** The listing is not
   beta-blocking, OQ3 is open, and it now additionally depends on `mcp.pipermorgan.ai` existing. That is
   bucket-A spend on an undecided channel.

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
