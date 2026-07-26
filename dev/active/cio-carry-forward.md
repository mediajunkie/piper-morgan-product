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

*(Exec's `cohort-attention-rollup` reads this section directly. **Rewritten at the 2026-07-25 STOP — live items only.**)*

- ⏰ **PA's OpenAI identity verification — the only item with an EXTERNAL clock, still unstarted, now seven days idle.** Gates the ChatGPT remote-MCP track. **Lead time begins when someone starts it, not when we decide**, and it's independent of PA's other two items (claude.ai tier, open-source decision) which move at our speed. HOST's framing: *start the clock now, decide the rest later.* **Not roll-blocked** — deliberately decoupled so it doesn't wait on a provisioning window.
- 🟢 **Arch resumed 2026-07-25 evening with FULL CONTEXT PRESERVED** (PM confirmed). This changes what its handoff can be: not an artifact-based reconstruction six days later, but a real first-person account. The permission it was given — *"if your context is already gone, say so and stop"* — turns out not to be needed. **Expect a genuine §4 lessons / §6 load-bearing-vs-commodity handoff, and weight it above my orientation note wherever they disagree.** Its note now forward-references it.
- 🟢 **COHORT ROLL — cleared, authorized, fully staged. Waiting only on an attended window with PM.** Order (Exec-confirmed, by decay): **arch → ppm → cxo → pa → web** → Lead → comms/docs/exec. Five orientation notes written and Pard-reviewed clean; runsheet makes each standup one command; `verify-hooks` runs same-day pre-standup. Batch launches into an attended window — first-touch approvals still need a human, and that's a deliberate privilege boundary, not a gap.
- 🗣️ **PM flagged the "window" concept itself as problematic and needlessly constraining — conversation deferred, not resolved.** Recording it here so it has a concrete referent when we do have it: "window" is currently load-bearing in exactly one place — the cohort roll above is gated on *an attended window with PM*. **I am holding that gate as-is rather than quietly reinterpreting it**, since PM deferred the discussion rather than lifting the constraint. If the concept loosens, the roll is the first thing it changes.
- 🟡 **This seat's restart — PM-approved, three independent reasons, not yet done.** Converts it to the deterministic hook condition. I cannot restart myself. Everything is pushed and the day is closed, so it is cheap right now and gets more expensive once the roll starts.
- 🔬 **Hook intermittency — UNEXPLAINED, and four models were refuted in one day (three mine).** Established: fresh sessions deterministic (Pard 6/6), a second long-lived seat deterministic (HOST 4/4), this seat 1-of-5 then 4-of-4 with no config change. Excluded: file shape, command shape, config drift, single-layering. **HOST re-probes at tomorrow's START for the first genuine ~8h longitudinal sample** — and that becomes the only instrument, since restarting this seat destroys the condition. ⚠️ **Do not consolidate the two hook layers** while this is open.
- 🟡 **Remote-control initiation still needs one human tmux touch per agent** — the `mcp__ccd_session_mgmt__*` family is absent on Amber, so no agent can self-initiate or do it for another. Suggested Pard fold it into `amber-agent` standup as he did `--kickoff`.
- ⚪ **`RemoteTrigger` (claude.ai routines API) exists here** — plausibly the durable-scheduling answer the Routines-watchdog thread has circled since June (`CronCreate` is session-only, `durable` is a no-op, 7-day cap). Flagged to HOST; not actioned, deliberately not mid-migration.

## Cron

`51eb2066` — LEAN `7 10,16,22`, re-armed at the 2026-07-25 STOP (delete-then-create-then-verify; exactly one job confirmed). Registry row matches. **Bump to `7,27,47` if the roll goes active, and revert when the window closes** — that happened once today and the revert condition worked because the holding reasoning was written down.

## Closed this evening *(one cycle, then delete)*

- ✅ **Inbox-proxy pilot** — Exec traced it end to end rather than answering from memory: 6/27 was a pre-pilot proposal, PM greenlit the 2-week clock on 7/4, it ran to ~7/18 *inside the outage window* and nobody closed the loop. The practice continued regardless. **Ratified retroactively as standing practice.** Carried by four sessions; the answer took one direct ask.
- ✅ **Watchdog registry row shape** — Exec confirmed as specified, endorsed registration-at-START, endorsed the alert-denominator fix. Finding #6 fully closed on Exec's side.
- ✅ **Migration order** — Exec confirmed the decay ordering.
- ✅ **Intermittency question** — answered by Pard's third-seat instrument (6/6 fresh-session PASS with attribution). Localized, roll unaffected.
- ✅ **Stale RUN-LEAN THROTTLE note** in the registry (expired Jul-1, sat three weeks) — cleared, replaced with a roster note carrying finding #6's rule: *coverage is not the roster; any coverage claim from this file must state its denominator; do not hand-add rows for dormant roles.*

## Done today, no further action *(detail in `dev/2026/07/25/2026-07-25-1053-cio-code-log.md`)*

Migration complete and verified · memory pool seeded 0→164 with the index rebuilt from the filesystem · worktree lifecycle **v0.2** ratified (Rule 4 added; version-less path) · **CLAUDE.md** worktree model corrected to host-dependent + safety-nets section corrected for finding #5 · **`duty-cycle-tick` v1.15** (Step 2a false-pass under Model A; Step 2a-bis hooks check) broadcast 9/9 · HOST's three questions answered incl. a v1.3 correction · findings #1–#5 all routed and accepted.

## Lower priority / queued

- **Step 2a follow-through** — confirm Pard's tmux-cwd guard actually shipped in `amber-agent.sh` rather than remaining a stated intention. Detection-only either way; the provisioning bug lives in the harness layer.
- **Dashboard welfare-criteria v0.3** — Criterion E resolved, A–F not started. A genuine quality-banking candidate, but per the skill that needs an explicit real trigger (fresh session / compaction), not "deserves focus."
- **Liveness model v2 / cohort-coverage expansion** — banked, unscoped. Finding #6's registration-at-START is the first concrete piece of the coverage half, and it shipped; the rest hasn't been scoped.

<!-- Rewritten at the 2026-07-25 STOP. A prior rewrite left the pre-STOP stratum in place BELOW the
     new one -- two "## Cron" sections disagreeing about the live cron, and resolved items reappearing
     as live directly under their own resolution. Rewriting the top is not rewriting the file. If you
     add a section, delete what it supersedes in the same edit. -->
