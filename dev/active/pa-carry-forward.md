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
- 💵 **One word on Probe B**: it needs API spend against your credential. **Your "yes you may" was scoped
  to Probe A**, so I'm not extending it silently. B just became *upstream* of the MCP tool catalog (the
  registry's 31 aliases are the situation-vs-object-shaped naming experiment sitting in our own code), so
  it's worth more now than when PPM green-lit it.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED** (2026-07-31); epic **#1462**; gates **#1458**, **#1463**.
- ✅ **Probe A complete and stood down** — refusals survive as **failure-shaped payloads** (6/6 both
  providers); structured fields help but are **not sufficient** on GPT. ⚠️ API-layer only; deployed-host
  retest before booking.
- ⚠️ **"Delete" means SOFT delete** — five live *"cannot be undone"* claims on reversible paths
  (**#1482**, CXO owns copy, HOST owns the trust ruling).

## Active state — 2026-08-04 fire 4 (13:12)

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

1. 🟢 **Tool-annotation spec — UNBLOCKED, complete enough to hand to Lead.**
   `dev/active/tool-annotation-spec-2026-08-04.md`. **Next actor is Lead, not PA.**
   ✅ **Arch ruled**: condition 3 does **NOT** reach the workflow registry — **nothing leaves the catalog,
   build ONCE**. `readOnly` ≠ `resource` (orthogonal axes: *addressable context vs invoked operation* is
   not *does it mutate*). ✅ A defaultless registry field satisfies condition 2, and Arch flagged
   **"don't let defaultless get softened in review — it's the whole thing"** (4 of 5 `WorkflowEntry`
   fields are already defaulted).
   ✅ PPM: `close_issue` = `WRITE` — **DESTRUCTIVE = destroys information unrecoverable through the product**.
   ✅ CXO: **the irreversible part of a reversible operation goes in the same sentence as the reversibility
   claim** (a recomposing client LLM drops trailing caveats, and keeps the *reassuring* one).
   ✅ **Registry alias count CORRECTED**: not 31→12 (that's the literal dict, **one of five writers**) but
   **103 aliases → 38 entries**, 2.71 names/op — re-derived independently, matches Arch exactly.
   **Catalog must dedupe by entry identity; aliases are classifier surface and must not leak outward.**
   ✅ All **26 cohort handlers screened → all READ** (3 ambiguous hand-checked). ⚠️ **A screen, not an
   audit**; `_handle_learn_pattern` is the one to re-check first.
   ⬜ **Open for Lead**: the ~15-site breaking change. ⬜ Unscreened: `meeting` (offer-only),
   `run_todo_query_workflow` (separate module).
   ⬜ Other Phase 0 items untouched: `claude plugin validate` dry-run · public docs page · ChatGPT
   5-positive/3-negative test cases.
2. 🟡 **Probe B — now UPSTREAM of the catalog, and PM-gated on API spend.**
   Spec: `dev/active/phase0-client-llm-probe-spec-2026-07-30.md`. **Do situation-shaped tool names route
   worse than object-shaped?** ⭐ **The alias set is that experiment sitting in the codebase** —
   `what_changed`/`show_changes`/`changes_since` (situation) vs `changes_query` (object). **B's answer
   decides which of the 12 canonical tool names we pick**, so it precedes the catalog rather than sitting
   beside it.
   ⛔ **PM's "yes you may" was scoped to Probe A. B is new API spend — do not extend it silently; ask.**
   ✅ **CXO's two-audience worry is RESOLVED and does not constrain B**: MCP Tool carries **`name`**
   (*"Unique identifier"*) **and `title`** (*"human-readable… for display purposes"*) as **separate
   fields** — verified against the 2025-06-18 spec. B decides `name`; `title` is legibility (CXO's copy).
   **Still state B's denominator** in the probe: *measures routing for `name`, not legibility of `title`*.
   ⭐ **Arch's suggestion worth weighing**: the 103 aliases are a **naturally-occurring sample across both
   name shapes** — B may be answerable partly *from the registry* rather than only in front of it, which
   would cut the API spend.
   ⚠️ **Keep schemas identical across arms.** ⚠️ **Rescore by hand, not by tally** — the Probe A scorer was
   wrong 4× across 5 arms and every error was caught by hand-reading, never by the tally.
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
