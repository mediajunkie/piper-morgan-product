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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-03 STOP.)*

**Beta is Sat 2026-08-08** (verified at `decisions.log:303` — PM's own entry, ISO format).

- ⏱️ **TEN SECONDS: open `https://pipermorgan.ai/privacy` in a browser** and say whether a real policy
  renders. URL returns **200**; **server-rendered text is 29 characters.** PA cannot execute JS, so this
  is undecidable from an agent seat. Matters because Anthropic rejects *"missing or incomplete"* policies
  and review may fetch without JS.
- 🟡 **Three privacy items left for you** (narrowed from five — the rest PA answered from code):
  **sub-processor completeness** (which LLM provider is actually in production?), **retention practice**
  (none exists in code), **contact address**.
- ❓ **Is a Saturday beta deliberate?** Aug 8 is a Saturday. Given weekends are your active window it may
  well be — worth being deliberate rather than inherited. One word.
- 🟡 **Architecture diagram** — redrawn at your request, still awaiting a time to discuss. No urgency named.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED**; epic **#1462**; gates **#1458**, **#1463**; delete-copy finding **#1482**;
  Jake welfare subset **#1476/#1477**.
- ✅ **Probe A complete and stood down** — refusals survive as **failure-shaped payloads** (6/6 both
  providers); structured fields help but are **not sufficient** on GPT. ⚠️ API-layer only; deployed-host
  retest before booking.
- ⚠️ **"Delete" means SOFT delete** — five live *"cannot be undone"* claims on reversible paths
  (**#1482**, CXO owns copy, HOST owns the trust ruling). Credentials are the one genuinely hard delete.

## Active state — 2026-08-03 STOP (next wake 06:42 Tue 8/4)

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/08/03/2026-08-03-0712-pa-code-log.md` — **DAY-CLOSED 2026-08-03**
- **Handoff/lessons**: `dev/active/handoff-pa-2026-07-31.md` — keep current, don't rewrite at departure
- **Cron**: ARMED at STOP, delete-then-create. **Job id in the registry row.** 🔴 **First action any new
  session: `CronList`.** Empty = not cycling. Session-only; expires ~2026-08-10.
- **Inbox**: 0 at close.

⚠️ **KEYCHAIN**: use `/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — any other
binary **HANGS** on a GUI dialog rather than failing; `SIGALRM` will not save you.

⚠️ **SEARCH PREDICATES — two false negatives on 8/3 alone**, from two roles, both nearly inverting a
report: CXO's `grep "Aug 8"` against a log storing **ISO**; PA searching **`web/templates`** (1 file)
instead of **`templates/`** (63). **The search that finds NOTHING is the one that most needs its
predicate audited** — a confident null is what nobody re-checks. Real template root is `templates/`.

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
