# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live **here**, in the section immediately below.

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction links/ideas drop file. Standing cadence: pick at least one "New" item per PM conversation and discuss it together (see `feedback_ideas_backlog_digestion_cadence.md`).

> **Rewritten 2026-07-25 ~14:05** (not appended). The pre-migration version had accreted into a day-by-day archive with `(superseded)` markers stacked on resolved items — the exact drift my predecessor flagged in the handoff ("needs periodic *rewriting*, not just appending"). Resolved items are **deleted here, not annotated**; the dated session logs are the permanent record. If you find yourself adding a third `(superseded)` marker, rewrite instead.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly per its SKILL.md Step 1.)*

- ⏰ **PA's OpenAI identity verification — the only item here with an EXTERNAL clock, and it hasn't started.** Six days idle. Getting Piper Morgan into ChatGPT (remote MCP) depends on it, the lead time begins when someone *starts* it rather than when we decide, and it's **independent of the other two PA items** (claude.ai tier check, open-source decision) which gate the Claude tracks but move at our speed. **Framing (HOST's): "start the clock now, decide the rest later."** Deliberately NOT coupled to the migration window — it would read as one more roll-blocked item and it isn't.
- 🟡 **RESTART TIMING — a refinement worth PM's 10 seconds, based on the reasoning PM already approved.** PM ruled *ride to day-close* on the grounds that restarting mid-provisioning would kill the session-scoped cron at the worst moment. **We are now in a quiet gap** — the roll hasn't started, both Pard and I are idle, everything is pushed and the carry-forward is current. That same reasoning now argues for restarting **during this gap rather than after the roll begins**: a restart is cheapest now and most expensive mid-roll, and if the window opens tonight I'd otherwise coordinate the whole roll unenforced. **I cannot restart myself** — it needs PM or Pard. Not urgent; day-close still works if the roll doesn't start tonight. Flagging because the *condition* PM reasoned about has changed, not the decision.
- ✅ **BOTH PM DECISIONS RECEIVED (15:50)** — (1) **no restart**, ride to day-close *(so: restart at STOP, and the new session must re-arm the cron immediately — it is session-scoped and dies with this one)*; (2) **CIO + Pard run HOST's cutover**, PM escalation-only. Go given, cutover executing.
- 🟢 **HOST CUTOVER IN FLIGHT** — worktree provisioned and **current** (the currency-assert caught a stale `claude/host-cycle` and auto-ff'd it — it fired for real on its first run, contra my prediction that it would catch nothing). HOST has the **reviewed** prompt (worktree at `c22c6ad50`, verified by hash). Session live, orienting autonomously. **Gate = HOST's hooks behavioral check; a block is the pass. CIO makes the call.**
- 🔴 **HOST IS CURRENTLY UNWATCHED** — no row in `dev/active/duty-cycle-registry.tsv`. Pard correctly declined to guess-edit and deferred. **Finding #6 recurring on agent #2, four hours after I flagged it.** Fixed as mechanism: `duty-cycle-tick` **v1.17** makes START verify-or-write your own row. **This also corrected my own proposal to Exec** — provisioner-writes-the-row *cannot* work, because the row's load-bearing field is the cron expr and that's unknown until the agent arms it. Exec: row shape still yours to confirm.
- 🟡 **PM asked when to archive emeritus-HOST. Recommendation: NOT until the gate passes and HOST completes a substantive fire.** Precedent is my own cutover — the old CIO session stayed alive until it had verified the successor across 7 fires, then retired. The gate is the branch where rollback matters; keep the fallback until it's cleared.
- ⚪ *(superseded — both answered)* **TWO ONE-LINE DECISIONS FOR PM — both have recommendations attached; approve or override, don't re-derive.**
  1. **"Go" on HOST's cutover, and who drives it. Recommendation: Pard and I run it; you say go once.** You drove mine because it was first, unproven, and half the decisions were open. None of that holds now — the package is proven, provisioning is scripted and safe-by-construction, the gate is a defined behavioral check with an unambiguous pass, and both governance questions are ruled. Making you drive the second one spends the attention we spent all day trying to give back. We escalate immediately if the gate fails — that's the branch where your judgment actually matters.
  2. **Whether I restart this session now to pick up hook enforcement. Recommendation: NO — ride to day-close.** My cron is session-scoped so a restart kills it mid-provisioning, and my actual mitigation is structural rather than vigilance: every mail op is `push origin HEAD:main` + **verified by content on origin/main**, which achieves the hook's goal (mail reaches main) by another route. Nothing has been stranded all day. At STOP everything is pushed by definition and the re-arm is already ritual, so the restart costs ~nothing there and the overnight session gets real enforcement. Easy override if you'd rather it be sooner.
  *(Both were Pard's calls to route to you rather than settle between us — correct, they have a human in them.)*

- 🟡 **COHORT MIGRATION — gate is the behavioral hooks check at agent #2 (HOST).** Pard has wired user-level hooks in `~/.claude-pm/settings.json` (incl. the finding-#5 PreCompact restore), landed the tracked mirror with the atomic-update rule, and verified the script cannot wedge a session. **My own behavioral check came back NOT-blocked — AMBIGUOUS, not a fail**: my session predates the wiring, so it cannot distinguish startup-only loading from a bad fix. **Gate stays CLOSED.** HOST's fresh session is the real test — *a block is the pass; anything else, including silence, stops the roll.* Order: **HOST → idle-since-Sunday → Lead → rest.**
- ⚠️ **Live sessions are unprotected even though the host is configured.** If hook loading is startup-scoped (consistent with my ambiguous result), the fix does **not** retroactively protect any session already running — including this one. Proposed to Pard that *"restart live sessions after a hooks change"* become a standing rollout step. **Meanwhile I am enforcing mailbox discipline and log maintenance manually and saying so in fire entries** rather than assuming coverage.
- ⚪ **`RemoteTrigger` (claude.ai routines API) exists in this environment.** Possibly the durable-scheduling answer the "Routines watchdog" thread has circled since June — `CronCreate` is session-only, `durable:true` is a documented no-op, 7-day cap. Flagged to HOST; **not actioned, deliberately not mid-migration work.**
- 🔴 **FINDING #6 — the stall watchdog covers 4 of 10 roles and reports its subset as the total.** Registry rows: `cio`, `exec`, `arch`, `lead`. **Five roles dark six days** (no session log since 7/19 AND zero commits since 7/20, verified independently): **arch, cxo, pa, ppm, web** — only `arch` is watched, so four are structurally invisible. The 14:01 alert said *"all currently stale: arch"*, which reads as "the cohort is fine except arch." Opt-in registration was the design; it drifted from the roster when the outage + migration changed it. **Proposed to Exec** (their design): couple registration to *provisioning* rather than adding rows now — adding them alerts on intentionally-dormant roles → noise → the belt gets ignored, which is worse than the gap. Also: make the alert name its denominator; clear the stale "through Wed Jul-1" throttle block.
- 🟢 **The idle-since-Sunday migration batch is now concrete: arch, cxo, pa, ppm, web.** Also corrects the alert's advice for arch — it needs a **migration**, not a re-prod; prodding a dormant session on the laptop being decommissioned is wasted work.
- ✅ **Old-machine session + cron `d854c9be` — RETIRED 15:29** (`a63219564`). The laptop CIO session stood down cleanly, deleting its cron, and **verified the successor was live and working across 7 fires before doing so** rather than taking the cutover on faith. Cutover is fully complete; nothing left on the old machine.
- 🟢 **HOST's three-piece package is COMPLETE** — handoff + Pard's reviewer pass + first-session prompt (`80466a948`). I gave the prompt a reviewer pass (`4ff7b9221`) and added a **branch-currency check**, which it lacked: Pard's new provisioning assert should make it a non-event, but HOST is the first agent it ever runs on, and an upstream assert with no downstream verification is the same believed-to-work-never-seen-fire shape as findings #4/#5/#6. Also flagged that Pard's channel is a separate repo needing its own fetch, that `/hooks` isn't agent-invokable, and that PreCompact's silence at compaction would be a second datapoint. **Everything is staged and waiting on PM's single go.**

## Done today, no further action *(detail in `dev/2026/07/25/2026-07-25-1053-cio-code-log.md`)*

Migration complete and verified · memory pool seeded 0→164 with the index rebuilt from the filesystem · worktree lifecycle **v0.2** ratified (Rule 4 added; version-less path) · **CLAUDE.md** worktree model corrected to host-dependent + safety-nets section corrected for finding #5 · **`duty-cycle-tick` v1.15** (Step 2a false-pass under Model A; Step 2a-bis hooks check) broadcast 9/9 · HOST's three questions answered incl. a v1.3 correction · findings #1–#5 all routed and accepted.

## Live threads needing a next action

- **Migration roll** — blocked only on HOST's fresh-session check. Nothing for me until it passes or fails.
- **Checklist v1.3** — HOST holding it for my proposed correction: Amber-bound migrants should **verify the memory pool is populated**, not export/read an export. Confirm it landed before Exec review.
- **Step 2a follow-through** — skill says Pard's tmux-cwd guard is the real gate; confirm it ships in `amber-agent.sh` rather than staying a stated intention.
- **Exec's inbox-proxy pilot** — unresolved 6/27-vs-7/4 framing discrepancy, aging since June. Just ask Exec directly; carried forward too long.

## Lower priority / queued

- **Dashboard welfare-criteria v0.3** — Criterion E resolved, A–F not started; needs a dedicated build session. *(Genuine quality-banking candidate, but per the skill that needs an explicit real trigger — a fresh session or compaction — not "deserves focus." Not started mid-migration-coordination on purpose.)*
- **Belt-4 non-spawn during the July dormancy** — likely moot (Amber has no auto-respawn watchdog at all; the detect-and-alert belt does exist and fired correctly today — see finding #6).
- **Liveness model v2 / cohort-coverage expansion** — banked, unscoped. Finding #6's registration-at-provisioning proposal is arguably the first concrete piece of the coverage half.

## Recently closed *(one cycle, then delete)*

- ✅ **Stray memory-path file** (aging since 7/7) — **resolved by migration**, verified 7/25. It was a local artifact on the old laptop; no such path exists on Amber, and the memory itself is present in the seeded pool. Three sessions carried it forward without spending 60 seconds to look.
- ✅ **#973 / #1277** — re-verified live 7/25, both genuinely OPEN. Left a Model-A scope note on #1277, whose "ephemeral-worktree" premise shifted today.
- 🟡 **Exec inbox-proxy pilot** (aging since June) — **asked** 7/25 with a four-option multiple choice; awaiting a one-line answer. Was carried by four sessions without anyone asking.

## Cron

`a645461c` — `7,27,47 * * * *` (20-min **COLLABORATION** cadence, temporarily bumped from LEAN for the active Pard window).
**REVERT to LEAN `7 10,16,22` when the migration collaboration closes** — hooks verified, v0.2 landed, cohort migrated or the work quiet for a full day. A 20-min cadence is for an active two-party window, not a steady state; letting it persist by inertia is the create-rule-without-cleanup-rule trap this whole lifecycle spec exists to prevent.

Registry row `cio`: needs updating to `7,27,47` — currently reads `7 10,16,22`.
