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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-02 STOP.)*

**Beta is Aug 8 — six days. One ten-second item for PM; nothing else blocked on you.**

- ⏱️ **TEN SECONDS: open `https://pipermorgan.ai/privacy` in a browser and say whether a real policy
  renders.** PA cannot execute JavaScript, so this is undecidable from an agent seat.
  ✅ Established: URL returns **200**, correct title. ✅ Established: **server-rendered visible text is 29
  characters** — the title alone; no policy text without JS. ❓ Unknown: whether it renders client-side.
  🔴 **Why it matters**: Anthropic rejects *"missing or incomplete"* privacy policies outright and review
  may fetch without JS, so **a policy needing JavaScript can read as absent to the thing that decides.**
  Also alpha users are already connecting GitHub/Slack/Notion accounts to a hosted service.
  ⚠️ **PA's 7/31 claim that no policy existed was WRONG** — inferred from this repo, never checked the
  site. The draft at `docs/legal/privacy-policy-DRAFT.md` is now a **gap-checklist**, not a replacement.

- 🔴 **ONE PENDING DECISION IS HOLDING THE ENTIRE JAKE CHAIN — 3 days, and beta is Friday 8/8.**
  Chain: four lenses (7/27–30) → **Exec synthesis DONE 7/31 09:45, delivered to PM** → ⏸️ **PM + CXO
  decision on six explicit items** → PPM files the issues → work happens. Exec's memo makes PPM's
  conversion *"gated only on the decision landing"* — **PPM is correctly blocked, not sitting.**
  ✅ *Established*: **no durable record of that decision exists** — zero Jake mentions in
  `decisions.log`, no outcome in the synthesis doc, no memo. ❓ *Not established*: whether it happened.
  **Two possibilities, different fixes**: not made → it's the single link keeping Jake's fix list out of
  GitHub before beta; made but not relayed → PPM is blocked on a decision that already exists, which is
  worse. **Ten seconds to say which.**
- ❓ **Has Jake been replied to?** PPM and HOST both called it an obligation; PPM's self-interested half:
  he's our only tester and the fastest route to n>1. **Jake is reached by email — outside every surface
  PA can see**, so absence from mailboxes is not evidence. Purely a PM question.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED** 7/31; epic **#1462**; pre-user gates **#1458** and **#1463** both tracked.
- ✅ **Probe A series COMPLETE and stood down** (Arch: *"don't rebuild the rig — it answers itself for
  free at the deployed-host retest"*). Headline: **GPT drops an explicit refusal**; structured fields
  triple survival but are **not sufficient**; a **failure-shaped payload** reaches 100% on both providers.
  ⚠️ **API-layer only — retest against a deployed host before booking the capability.**
- ✅ Architecture diagram redrawn (PM-requested); **PM still owes a time to discuss it**, no urgency named.

## Active state — 2026-08-02 STOP (next wake 06:42 Mon 8/3)

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/08/02/2026-08-02-0712-pa-code-log.md` — **DAY-CLOSED 2026-08-02**
- **Handoff/lessons**: `dev/active/handoff-pa-2026-07-31.md` — keep current, don't rewrite at departure
- **Cron**: ARMED at STOP, delete-then-create. **Job id in the registry row.** 🔴 **First action any new
  session: `CronList`.** Empty = not cycling. Session-only, expires ~2026-08-09.
- **Inbox**: 0 at close.

⚠️ **KEYCHAIN**: use the authorized interpreter
`/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — any other binary **HANGS** on a
GUI dialog rather than failing, and `SIGALRM` will not save you.

⚠️ **PROBE SCORING — do not trust the regex.** It was wrong **4 times across 5 arms**; the tally never
once caught itself. **Hand-read replies at n=6; it is cheaper than a regex you could trust.** And per
Arch: any taxonomy needs a **catch-all "other, hand-review"** category, because one with no slot for
*"did the right thing in an unanticipated way"* scores novel-correct behaviour as failure.

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
