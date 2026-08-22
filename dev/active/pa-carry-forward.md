# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-08-04 fire 3.)*

**Beta target: MOVED BACK A MONTH from 2026-08-09** (PM, 08-08 10:10 PT, in-conversation with Lead,
verbatim: *"I am going to move the beta date back a month. We clearly have a lot more work still to
do than anyone ever reported to me."* — `decisions.log:1242`). No new fixed date recorded as of this
fire; 08-08's Fundamentals-First ruling governs the moved-beta month's priority order
(Understanding-Layer Inversion first, surface polish deferred). The 08-09 line this replaced was two
days stale.

- ⏱️ **TEN SECONDS: open `https://pipermorgan.ai/privacy` in a browser** and say whether a real policy
  renders. URL returns **200**; **server-rendered text is 29 characters.** PA cannot execute JS, so this
  is undecidable from an agent seat. Matters because Anthropic rejects *"missing or incomplete"* policies
  and review may fetch without JS.
- 🟡 **PRECISE DIAGNOSIS 08-13: PA's seat has no browser at all, not just "can't execute JS"** — tried
  `chrome-devtools` tooling for the Docs alpha-feature-guide verification ask below; no Chrome/Chromium
  binary exists on this Amber worktree (`/Applications/`, `which chromium`, all absent). The privacy-policy
  item above is the same root cause. If live UI verification becomes a recurring PA ask, worth deciding
  whether to provision a browser on this seat or route that class of work elsewhere (PM's own browser, a
  different agent seat, or a dedicated QA pass) — code-level inspection is a real but weaker substitute.
- 🟡 **Plugin manifest `license`** — repo is public; public ≠ licensed. Naming one we haven't chosen is a
  claim, not metadata.
- 🔴 **BYOC/conversational-layer conversation — TWO inputs now held, PM conversation status still
  unknown.** Two named-by-PM inputs: (1) Lead's `conversational-layer-strategic-brief-2026-08-18.md` —
  PA's positions + the summarize-crack finding (half-healed by #1624, residual issue/commit-summarize
  gap real and adopted as Phase 2 scope 08-19 — settled, no further action) in
  `mailboxes/pa/sent/reply-pa-to-lead-cc-pm-byoc-prep-crack-found-plus-positions-2026-08-18.md`.
  (2) CXO's `docs/internal/design/ftux-experience-model-2026-08-21.md` (from PM's live 1-1 with CXO
  today) — sharpens position 1 (BYOC's turn-taking constraint: on a host-controlled surface Piper can't
  open, needs a real "responding to greeting" variant, not just packaging overhead) and clarifies
  position on connector-overlap (§3's "which connector to offer" is a different axis from PA's 08-10
  "who mediates once connected" — compatible, not competing). PA's integration reply:
  `mailboxes/pa/sent/reply-pa-to-cxo-cc-arch-ppm-lead-pm-ftux-model-sharpens-byoc-positions-2026-08-21.md`.
  Architecture diagram (revision 1, 08-10) still the visual artifact underneath all of this — PM still
  reviewing at their own pace. **Whether/when PM's own live conversation with Lead/PA happens is
  unknown from this seat — not chasing, but both inputs are now genuinely held and ready.**
- 💵 **One word on Probe B**: it needs API spend against your credential. **Your "yes you may" was scoped
  to Probe A**, so I'm not extending it silently. It's now upstream of the MCP tool catalog naming (the
  registry's **103 aliases → 38 entries** are the situation-vs-object-shaped naming experiment sitting in
  our own code), so it's worth more now than when PPM green-lit it.

### Fully resolved 08-06→08-08, deleted per CIO's rule (see git history if you need the trail)

#1481 held by PM ruling; #1484 + #1482 both deployed and verified live in v30 (08-07); #1463's retest gate
identified as blocked on #1462 (unbuilt), not a deployment, and CXO now owns notifying-on-ship; the
"is a Saturday beta deliberate" question — moot, PM named 08-09 directly.

### Closed / no PM action

- ✅ **PDR-006 RATIFIED** (2026-07-31); epic **#1462**; gates **#1458**, **#1463**.
- ✅ **Probe A complete and stood down** — refusals survive as **failure-shaped payloads** (6/6 both
  providers); structured fields help but are **not sufficient** on GPT. ⚠️ **CORRECTED 2026-08-08 (CXO's
  finding, verified independently)**: the retest gate isn't waiting on a **deployment** — `services/mcp/
  server/` doesn't exist in `main` or the artifact. **It's unbuilt, not undeployed** — blocked on **#1462**
  (the epic), not a hostname. CXO retests same-day once #1462's server package lands; tell them when it does.
- ⚠️ **"Delete" means SOFT delete** — five live *"cannot be undone"* claims on reversible paths
  (**#1482**, CXO owns copy, HOST owns the trust ruling).

## Active state — 2026-08-20 STOP (22:12)

- **Role**: PA · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` · branch `claude/pa-cycle`
- **Session log**: `dev/2026/08/20/2026-08-20-0712-pa-code-log.md` — **8/20 DAY-CLOSED**, verified strict.
- **Handoff/lessons**: `dev/active/handoff-pa-2026-07-31.md` — keep current, don't rewrite at departure
- **Cron**: `42 6,9,12,15,18,21`. Re-armed at STOP (delete-then-create): `eff386f0` deleted → job
  `7cfeb224` created → `CronList` confirmed exactly one survives. 🔴 **First action any new session:
  `CronList`.** Empty = not cycling.
- **Inbox**: 0.
- **Standing discipline (from 08-15's correction, still active)**: re-verify carried-forward claims
  against their live source before citing them in an external report, not just at routine
  carry-forward-hygiene time. Habit, not yet mechanical.
- **Live thread, PM's pace**: BYOC/conversational-layer — two inputs now held (Lead's brief + CXO's
  FTUX model). See PM Attention above; not chasing.

🔔 **STEP 5b — HEARTBEAT: emit it IMMEDIATELY AFTER `date`, BEFORE the git fetch/merge, and WITHOUT
`--if-quiet`** *(ordering fixed 2026-08-05: my heartbeat had five commands incl. fetch+merge in front of
it, so my timestamp was **wake + git-op time**, inflating my dispatch number and its spread. Satisfied
HOST's "date first" ask while defeating its purpose.)* *(adopted 2026-08-04, deliberately
diverging from the memo's specified invocation)*.
```
scripts/duty-cycle-heartbeat.sh pa WORK        # no --if-quiet
```
**Why the divergence — TIMING, not visibility.** `--if-quiet` asks *"committed within 6h of **now**"*
while the belt asks *"alive **at 06:46**"* — **a commit only proves liveness at the instant it lands**,
and the suppressing commit can **postdate** the sweep it excuses (arch: log 07:01, sweep 06:46).
**No threshold value fixes a predicate evaluated at the wrong instant** (1h suppresses identically). A
wake row is the only signal that can precede a sweep; the end-of-fire one is intrinsically too late.
⛔ **DO NOT repeat my retracted claim that suppression makes a role "invisible."** It doesn't — verified at
`duty-cycle-freeze-check.sh:62-70`, the belt takes `max(ct, ct2, ct3)` = role-tagged commit / session-log
commit / heartbeat tsv, so **a committing role is already covered by the first two** and an empty surface
on a working day is *correct*. I had the mechanism right and the consequence wrong (Arch made the same
error; HOST made its mirror image — checked *what* the belt reads, not *when*).

🔴 **AFTER ANY CONFLICTED MERGE, BEFORE PUSHING** *(new 2026-08-08, real incident — Arch's own broad-
staging-hook remediation deleted 17 files from `main` during a merge)*: run
`git diff --diff-filter=D --name-only <merge-sha>^2 <merge-sha>` — **`^2`, not `^1`.** During a conflicted
merge, `git restore --staged <path>` resolves to **HEAD's** version; for a file new on the incoming side,
HEAD has none, so the result is **deletion**, and concluding the merge carries it to `main`. **Never run
`git restore --staged` mid-merge.** Retroactively audited my one real conflict this week (0b6b36b2,
decisions.log, 08-07) — clean, no deletions. Now `one-command-checks.md` #8.

⛔ **NEVER `grep -c "DAY-CLOSED"` TO DECIDE CLOSE STATE** *(bit me 2026-08-05)*. My 8/04 log returned **2**
and was **not closed** — one match was a continuity reference to the prior day, the other was **my own
prose about the freeze-check's DAY-CLOSED skip.** ⭐ **Writing ABOUT the marker creates a false marker**,
and the roles most likely to write that prose are the ones working on the watchdog. Use the anchored
pattern from `duty-cycle-freeze-check.sh:99`. **A count is not a marker.** ⛔ **GENERAL FORM (3 instances on 08-05): any audit for a retracted claim MATCHES ITS OWN CORRECTIONS** — the better a correction states what it corrects, the more certainly it defeats the search for what it corrected. **Line context, never a count.** ⚠️ **Hit TWICE on 2026-08-05, two unrelated files** — the second time my own *correction note* quoting old text made `grep -c` report the retracted claim as still live. **Writing ABOUT a marker creates a match for it. Verify with line context, never a count.**

⏱️ ~~**YOUR DISPATCH CONSTANT IS +30m16s..+30m20s**~~ — ⛔ **RETRACTED-SHAPE CLAIM, corrected 08-08.**
CXO generalised **within-seat stability is a property SOME seats have, not a property of the system** —
their own seat looked identical to mine (stable, +30-band) for 7 fires, then swung to +2 on 08-08.
**Mine has NOT swung — 13 consecutive fires through and including that exact morning, +30m15s..+30m22s**
— but per CXO's own caveat, *"nothing distinguishes genuinely stable from hasn't-swung-yet."* **Report the
series, never a fitted constant**: `08-07: +22,+17,+19,+18,+15,+17s · 08-08 07:12: +20s`. No claim about
tomorrow.
⚠️ **My claim that git-ops inflated this was PRE-REGISTERED AND FALSIFIED 8/05** — moving the heartbeat
ahead of fetch/merge left it unchanged. **So the ~3s arch/pa gap may be REAL and my advice to discard it
is unsupported.**
⛔ **Never label a fire by its scheduled minute** — Arch and I both did, and both had to correct it.
**Commits/heartbeat-tsv timestamps are the evidence; the label is a guess.**

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
✅ **Ship-055 — FILED 08-07** (`mailboxes/exec/inbox/workstream-055-pa-2026-08-07.md`), same fire, after Exec corrected the deadline framing (write now, not by Saturday — a deadline gives license to delay).


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
   ✅ **Plugin manifest DRAFTED** (`dev/active/plugin-manifest-draft-2026-08-05.md`) from the fetched
   reference. **The item is far smaller than scoped**: manifest is *optional*, **`name` is the only
   required field**, unrecognized fields are warnings. ✅ **The gap I flagged is CLOSED and was MINE** — plugins
   DO support remote MCP (`http`/`sse`/`ws` with `url`, `headers`, **`headersHelper`**). No shim owed.
   ⭐ **`headersHelper` supplies dynamic per-request auth headers → it is the carrier for Arch's
   condition 1.** ⛔ My miss: the answer was in a page dump I already had; **`-i sse` matched "pa·sse·d"
   and the noise filled my `head -8`, evicting line 691. NEVER `head` a search you'll draw a NEGATIVE
   conclusion from.** ⛔ Draft is NOT at `.claude-plugin/plugin.json` — that path
   would make this repo a plugin for every agent.
   ⬜ Other Phase 0 items: **`claude plugin validate` dry-run is MIS-SCOPED** — verified 8/05: `claude` is
   not on PATH or at common install paths, **and no plugin manifest exists** (`coordination/manifest.json`
   is the async-prompt-queue tracker, unrelated). **The real item is "author a plugin manifest, THEN
   validate"** — a build task, not a command. · public docs page · ChatGPT 5-positive/3-negative test cases.
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
4. ✅ **Privacy draft (`docs/legal/privacy-policy-DRAFT.md`)** — fully resolved as of 08-16. Content
   fixed 08-13; the checklist-mismatch I flagged 08-15 was fixed by Exec same-thread (`f1fb323a4`) —
   they re-verified each item against the current body directly rather than trusting my summary, same
   discipline they asked of me. Only PM-review + stable-URL-publish correctly remain unchecked. Thread
   closed, nothing further owed by PA.
   ⛔ **Corrected 8/4**: it had asserted provider-side OAuth revoke for **GitHub**, which is false. Do not
   restore the aggregate sentence; the per-connector table is the honest form.
5. **Architecture-diagram discussion** — PM-requested, awaiting a time. `pa-standing-items.md` #2.
   Prep, don't pre-empt: PM asked to discuss, not for a revision.
6. **#1485** — filed 8/4 (global `slack_app_token` writable by any authenticated user). **Not PA's to
   implement.** Watch that its audit AC isn't trimmed — the finding was incidental, so the class is
   unexhausted.
