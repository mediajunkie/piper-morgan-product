# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-04 fire 3.)*

**Beta is Sat 2026-08-08** (verified at `decisions.log:303` — PM's own entry, ISO format). **4 days.**

- ⏱️ **TEN SECONDS: open `https://pipermorgan.ai/privacy` in a browser** and say whether a real policy
  renders. URL returns **200**; **server-rendered text is 29 characters.** PA cannot execute JS, so this
  is undecidable from an agent seat. Matters because Anthropic rejects *"missing or incomplete"* policies
  and review may fetch without JS.
- 🟡 **Three privacy items left for you**: **sub-processor completeness** (which LLM provider is actually
  in production?), **retention practice** (none exists in code), **contact address**.
- 🔵 **One word for Arch: is Slack inbound a beta surface?** Arch's #1481 ruling assumes **no** and
  everything in it follows from that. Yes → **#1484 flips to default-on and a fix lands on a 4-day clock**
  (Arch advises against). It's your scope condition to amend.
- ❓ **Is a Saturday beta deliberate?** Aug 8 is a Saturday. Given weekends are your active window it may
  well be — worth being deliberate rather than inherited. One word.
- 🟡 **Architecture diagram** — redrawn at your request, still awaiting a time to discuss. No urgency named.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED** (2026-07-31); epic **#1462**; gates **#1458**, **#1463**.
- ✅ **Probe A complete and stood down** — refusals survive as **failure-shaped payloads** (6/6 both
  providers); structured fields help but are **not sufficient** on GPT. ⚠️ API-layer only; deployed-host
  retest before booking.
- ⚠️ **"Delete" means SOFT delete** — five live *"cannot be undone"* claims on reversible paths
  (**#1482**, CXO owns copy, HOST owns the trust ruling).

## Active state — 2026-08-04 fire 3

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Session log**: `dev/2026/08/04/2026-08-04-0712-pa-code-log.md`
- **Handoff/lessons**: `dev/active/handoff-pa-2026-07-31.md` — keep current, don't rewrite at departure
- **Cron**: `42 6,9,12,15,18,21`. Session-only; expires ~2026-08-10. 🔴 **First action any new session:
  `CronList`.** Empty = not cycling.
- **Inbox**: 0.

⚠️ **KEYCHAIN**: use `/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — any other
binary **HANGS** on a GUI dialog rather than failing; `SIGALRM` will not save you.

⚠️ **SEARCH PREDICATES** — CXO's `grep "Aug 8"` against a log storing **ISO**; PA searching
**`web/templates`** (1 file) instead of **`templates/`** (63). **The search that finds NOTHING is the one
that most needs its predicate audited.** Real template root is `templates/`.

⛔ **SOURCE VOCABULARY IS NOT SOURCE VERIFICATION** *(new 8/4, cost two false claims — one in a legal
document)*. `disconnect.py`'s docstring says *"#358 grant **revoke**"* for what is a **local** grant-store
row deletion. I carried that verb into two artifacts. **A comment using a strong verb for a weak operation
hands you the strong verb, and the audit trail looks clean because you can cite the file.** Citing a file
proves you read it, not that you read what it does.

## Open threads PA owns

1. 🔵 **Phase 0 distribution work — PA's active lane, nothing blocked.** Plan + per-item state:
   `dev/active/distribution-submission-tiers-resolved-2026-07-26.md`.
   ⬜ **next**: tool-annotation spec — **carries product weight, not just `readOnlyHint`/`destructiveHint`**,
   because PPM established the catalog is where opinionation lives · `claude plugin validate` dry-run ·
   public docs page · ChatGPT 5-positive/3-negative test cases.
2. 🟢 **Probe B — not started, unblocked, PA's to run.** PPM: *"take it… one rig, two questions, Phase 0."*
   Spec: `dev/active/phase0-client-llm-probe-spec-2026-07-30.md`. **Do situation-shaped tool names route
   worse than object-shaped?** (PPM + Lead/Arch read it.) Doesn't need the server. ⚠️ **Keep schemas
   identical across arms.** Result changes what the tool layer emits, so it precedes Phase 2.
   ⚠️ **Rescore by hand, not by tally** — the Probe A scorer was wrong 4× across 5 arms and every error was
   caught by hand-reading.
3. **#1458** — pre-live cross-caller state isolation; blocks multi-tenant serving. Not started; belongs
   with the implementation epic. PPM: don't let epic optimism compress it — the failure is silent and
   cross-tenant.
4. 🟡 **Privacy draft (`docs/legal/privacy-policy-DRAFT.md`)** — 3 🔍 markers left, all PM's (above).
   ⛔ **Corrected 8/4**: it had asserted provider-side OAuth revoke for **GitHub**, which is false. Do not
   restore the aggregate sentence; the per-connector table is the honest form.
5. **Architecture-diagram discussion** — PM-requested, awaiting a time. `pa-standing-items.md` #2.
   Prep, don't pre-empt: PM asked to discuss, not for a revision.
6. **#1485** — filed 8/4 (global `slack_app_token` writable by any authenticated user). **Not PA's to
   implement.** Watch that its audit AC isn't trimmed — the finding was incidental, so the class is
   unexhausted.
