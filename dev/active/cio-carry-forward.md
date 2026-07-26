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

*(Exec's `cohort-attention-rollup` reads this section directly. **Rewritten 21:11 — five items closed this evening; live only below.**)*

- ⏰ **PA's OpenAI identity verification — the only open item with an EXTERNAL clock, still not started.** Six days idle. Gates the ChatGPT remote-MCP track; **lead time begins when someone starts it**, and it's independent of PA's other two items (claude.ai tier, open-source decision), which move at our speed. HOST's framing: *start the clock now, decide the rest later.* Deliberately decoupled from the migration window — it is not roll-blocked.
- 🟢 **COHORT ROLL — cleared, authorized, fully staged, waiting only on an attended window with PM.** Order **confirmed by Exec**: arch → ppm → cxo → pa → web → Lead → comms/docs/exec. All five orientation notes written and Pard-reviewed clean; runsheet makes each standup one command. **Pard's `verify-hooks` gives 6/6 lifetime PASS on fresh sessions** — migrants are the deterministic condition by construction, so the roll is unaffected by the intermittency below.
- ⚠️ **This seat's hook enforcement is UNRELIABLE until it restarts** — 1 firing in 5 probes, identical config; file shape and command shape both tested and excluded. Pard's N=5 fresh-session run localizes it to the *long-lived session with config attached mid-session* condition, which is mine alone. **Not a risk to the roll.** PM ruled ride-to-day-close; the restart now has **three** independent reasons (user-scope load, this, and Pard's endorsement). Mailbox discipline stays manual and primary meanwhile — I use `mail-send.sh` push-to-ref.
- 🟡 **Remote-control initiation still needs one human tmux touch per agent.** Verified: the `mcp__ccd_session_mgmt__*` family is absent on Amber, so no agent can self-initiate or do it for another. First-touch *approvals* are a deliberate privilege boundary and shouldn't be automated; remote-control initiation probably should be — suggested Pard fold it into `amber-agent` standup as he did `--kickoff`.
- ⚪ **`RemoteTrigger` (claude.ai routines API) exists here** — plausibly the durable-scheduling answer the Routines-watchdog thread has circled since June, given `CronCreate` is session-only with a no-op `durable` flag and a 7-day cap. Flagged to HOST; **not actioned, deliberately not mid-migration.**

## Closed this evening *(one cycle, then delete)*

- ✅ **Inbox-proxy pilot** — Exec traced it end to end rather than answering from memory: 6/27 was a pre-pilot proposal, PM greenlit the 2-week clock on 7/4, it ran to ~7/18 *inside the outage window* and nobody closed the loop. The practice continued regardless. **Ratified retroactively as standing practice.** Carried by four sessions; the answer took one direct ask.
- ✅ **Watchdog registry row shape** — Exec confirmed as specified, endorsed registration-at-START, endorsed the alert-denominator fix. Finding #6 fully closed on Exec's side.
- ✅ **Migration order** — Exec confirmed the decay ordering.
- ✅ **Intermittency question** — answered by Pard's third-seat instrument (6/6 fresh-session PASS with attribution). Localized, roll unaffected.
- ✅ **Stale RUN-LEAN THROTTLE note** in the registry (expired Jul-1, sat three weeks) — cleared, replaced with a roster note carrying finding #6's rule: *coverage is not the roster; any coverage claim from this file must state its denominator; do not hand-add rows for dormant roles.*

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
