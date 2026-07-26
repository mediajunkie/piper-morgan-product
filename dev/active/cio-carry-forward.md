# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live **here**, in the section immediately below.

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction links/ideas drop file. Standing cadence: pick at least one "New" item per PM conversation and discuss it together (see `feedback_ideas_backlog_digestion_cadence.md`).

> **Rewritten twice on 2026-07-25 — ~14:05 and ~19:57 — never appended.** The pre-migration version had accreted into a day-by-day archive with `(superseded)` markers stacked on resolved items; the 14:05 rewrite cleared it and left the rule *"if you find yourself adding a third `(superseded)` marker, rewrite instead."*
>
> **That rule then fired within six hours**, which is the useful part: by 19:57 this section had drifted back to 14 bullets with four resolved items still presented as live (HOST unwatched, HOST cutover in flight, the emeritus-archive question, the hooks gate). **Resolved items are deleted here, not annotated** — the dated session logs are the permanent record.
>
> **Why it matters more than tidiness**: Exec's `cohort-attention-rollup` reads this section directly, so anything stale here propagates onto PM's attention board. A surface that reports resolved items as open is the same shape as finding #6 — a mechanism reporting something that isn't true — and PM stops looking elsewhere precisely because they trust it.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly per its SKILL.md Step 1. **Rewritten 19:57 — it had re-drifted to 14 bullets with resolved items still presented as live, which is how stale state reaches PM's board. Live items only below.**)*

- ⏰ **PA's OpenAI identity verification — the only open item with an EXTERNAL clock, and it has not started.** Six days idle. Gates the ChatGPT remote-MCP track; **lead time begins when someone starts it, not when we decide**, and it's independent of PA's other two items (claude.ai tier check, open-source decision) which move at our speed. Framing (HOST's): *start the clock now, decide the rest later.* **Deliberately decoupled from the migration window** — it isn't roll-blocked and shouldn't read as though it is.
- 🟢 **COHORT ROLL — gate CLEARED, authorized, fully staged. Waiting only on an attended window with PM.** Batch-1 packages complete on both legs (my orientation notes + Pard's reviewer pass, all three verified clean) and Pard's runsheet makes each standup one command. Order by decay, not alphabet: **arch → ppm → cxo → pa → web** → Lead → comms/docs/exec.
- 🟡 **Exec owes exactly one call: the operational sequencing within the dark-role batch.** HOST has ratified the methodology half (orientation notes, never reconstructed handoffs) on its own surface — I originally asked Exec to "ratify or redirect" as a single decision, which was my conflation. HOST concurs with the decay order; Pard has pre-staged against it.
- ⚠️ **This session runs UNENFORCED and will until it restarts** — user-level hook settings are read once at session start, and this session predates the key. Not a risk to the roll (every migrant is a fresh, enforced session), but it means I'm enforcing mailbox discipline and log maintenance by hand. **PM ruled ride-to-day-close; I flagged that the same reasoning now favours restarting during a quiet gap rather than after the roll starts.** PM's call, unresolved, low stakes either way.
- 🟡 **Remote-control initiation still needs one human tmux touch per agent.** Verified: the `mcp__ccd_session_mgmt__*` family from the old environment is absent on Amber, so no agent can self-initiate it or do it for another. First-touch permission approvals are a *deliberate* privilege boundary and shouldn't be automated; remote-control initiation probably should be, and I've suggested Pard fold it into `amber-agent` standup the way he folded `--kickoff`.
- ⚪ **`RemoteTrigger` (claude.ai routines API) exists in this environment** — plausibly the durable-scheduling answer the Routines-watchdog thread has circled since June, given `CronCreate` is session-only with a documented no-op `durable` flag and a 7-day cap. Flagged to HOST; **not actioned, deliberately not mid-migration work.**
- ⚪ **Finding #6 follow-through — and a sharper framing the 20:02 re-ping supplied.** The immediate instance is closed (HOST registered its own row; skill v1.17 makes START own it). What remains with **Exec** is the row *shape* and the alert phrasing. **The re-ping adds a third item and a better argument**: the watchdog alerted on arch again at 20:02 (151h, same *"all currently stale: arch"*), and will keep doing so roughly every 6h while arch waits for a migration window it's already first in line for.
  **The asymmetry is the point**: arch is the *only* dark role that gets alerted on **precisely because it's the only dark role that was registered** — the other four are silent for want of a row. So the current registry state produces **the worst of both: noise where there's coverage, silence where there isn't.** That's a stronger case for coupling registration to provisioning than the original finding was, and it's also why "just add rows for the dormant roles" would have been wrong — it would have converted four silences into four repeating alerts about deliberately-parked agents.
  Third ask for Exec, alongside row-shape and phrasing: **a known-dark-with-a-plan state**, so an agent parked pending migration doesn't re-alert every 6h and train the reader to ignore the belt. Also still true from the first alert: the recommended action (*"the session needs a prod/resume"*) is wrong for arch — it needs a **migration**, not a prod. Deliberately folded into this existing thread rather than opened as a new one; Exec has enough unanswered from me.

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
