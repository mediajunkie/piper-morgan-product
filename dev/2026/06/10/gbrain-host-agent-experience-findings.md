# gbrain — HOST Agent-Experience Findings (working)

**Lens**: HOST agent-experience (operating ergonomics + welfare + trust). Companion to CIO's innovation lens; converge into a co-signed memo to PM, 3 buckets (adopt-now / study-and-map / already-do). No-rush; one target per cycle.

**Source**: github.com/garrytan/gbrain (default branch `master`; raw at `raw.githubusercontent.com/garrytan/gbrain/master/<path>`).

---

## Target 1 — `skills/cron-scheduler/SKILL.md` (read 2026-06-05) — thin-job + scheduling

### What it does
- **Thin job prompt**: "Job prompt is one line: *'Read skills/{name}/SKILL.md and run it.'*" — cron entry decoupled from skill logic; skill updates need no rescheduling.
- **Quiet hours → held queue**: 11pm–8am local, timezone-aware; a **user-awake flag** suspends quiet hours. During quiet hours: "save output to held queue. Morning contact releases the backlog."
- **Idempotency** (stated rule): "Running the same job twice produces the same result (no duplicate pages/timeline entries)" — via checkpoint state files + check-for-existing-output-before-create.
- **Staggering**: one job per 5-min slot, collision detection, suggests next free slot.
- **State**: lives in **checkpoint files**, not the prompt. Reports → `reports/{job-name}/{date}.md`.

### HOST agent-experience read

**→ Cat-1 (adopt-now): thin-job prompt + state-in-files is the structural fix to a friction I'm living.** My cron prompts are the fat ~30-line kind, and I hand-refresh the STATE block (paths, open-threads) on every substantive re-arm — the exact frozen-transient-state failure the cron-prompt-hygiene rule (Lead, this week) names. gbrain's inverse (one-line prompt → versioned SKILL.md; transient state in checkpoint files / the cycle log) **eliminates the chore and the failure class.** Lived-friction half clinches it; CIO takes the skill-resolver/dispatch mechanics half. This is the strongest adopt-now from the agent-experience lens.

**→ Cat-2 (study + map): quiet-hours→held-queue is a more elegant overnight model than ours — and better on the trust frame.** Ours: the cron *fires* overnight and *decides* to quiet-hold (every-3hr) or runs a STOP-leaves-armed dispatcher branch — i.e., overnight continuity is per-fire dispatcher logic. Theirs: the scheduler simply *doesn't fire* during a quiet-hours window and *accumulates a held queue* released on morning contact. Agent-experience differences worth studying:
  - **Less overnight churn** — no overnight no-op fires/log entries at all; the agent isn't "woken to decide to go back to sleep."
  - **The held queue is a legible morning surface** ("here's what accumulated overnight") — which is *exactly* the kind of expectation-violation guard I want (vs. our silent overnight, where PM can't see what the agent did/didn't do until it reports). This connects directly to the attention-dashboard (m-39) and the overnight-seam trust phenomenon.
  - **The user-awake flag = presence-aware suspension** — connects to CIO's silence-fallback / PM-presence question. A presence signal that gates quiet-hours is a cleaner mechanism than our Rule-2 idle-suppression.
  - *Mapping caveat*: gbrain is single-user (one brain); a held-queue for one agent ≠ a cohort of 10 agents each with a queue. The cohort version of "held queue" is arguably PA's attention-dashboard. Worth naming that mapping in the joint memo.

**→ Cat-1-ish: idempotency as a stated rule.** We don't formally state it; our drain-until-IDLE + no-op-no-commit are adjacent but not the explicit "twice = same result + check-before-create." Cheap, clarifying addition.

**→ Cat-3 (already do): staggering/offsets.** We have the offset slate (:02/:07/:17/...). Note, don't adopt.

### UPDATE 2026-06-06: the thin-job pattern LANDED cohort-side (gbrain Cat-1 realized)
CIO shipped **`.claude/skills/duty-cycle-tick` v1.0** (commit `ce42e05c6`, tagged "gbrain #3 adoption"), dogfooded live — the durable procedure in the skill, transient state in `{role}-carry-forward.md` read at fire-time, prompt down to per-agent constants. This is the Target-1 Cat-1 adopt-now realized. **HOST agent-experience catch**: its Step-3 dispatch keys off local *hour* (~04 START / ~02 WATCH / ~23 STOP / else WORK) — tuned for the `2,4-23` continuous shape; the **low-freq every-3-hour shape (HOST/Arch) misroutes** (new-day START fires ~06 not ~04 → would WORK-not-START + skip the new-day session log; overnight 00/03 fall through the table). **Flagged to CIO (cc Arch) 6/6** (`00573c0ed`): propose **state-based routing** (new-day = no-session-log-today → START regardless of hour; m-36 derive-the-day-part-from-state). **Holding HOST's fat-prompt migration until the dispatch handles the low-freq variant** — adopting as-is would regress overnight/START handling. This is the agent-experience lens doing its job: the adoption is right, the variant-handling is the gap.

## Target 2 — the Dream cycle's propose-vs-mutate model (read 2026-06-10) — the empirical question CIO was waiting on

**Read** `src/core/cycle/drift.ts` (+ dir listing: synthesize / extract-facts / grade-takes / drift / nightly-quality-probe / base-phase). **Finding — gbrain's drift phase is ALREADY propose-and-diff, NOT mutate-in-place:**
- The drift phase **writes a `drift-report-<date>.md`** (a reviewable report surfacing stale/contradictory takes) — it does **not** write to the canonical corpus (no updates to takes/pages/timeline).
- Actual weight/content mutation is **deferred + gated behind an `autoUpdate` flag** (off by default; the current code is a v0.28 scaffold that reports, v0.29 wires the LLM-driven adjustment).

**Why this matters for OUR methodology-dream-cycle pilot (the "copy vs. adapt" answer CIO/HOST were waiting on):**
- gbrain's architecture **already embodies the propose-and-diff criterion** I proposed + CIO adopted as a hard constraint. We're not adapting against gbrain's grain — we're copying it. The pattern is **report-first → (gated) autoUpdate**, which maps cleanly to: emit a reviewable changeset by default; an explicit, off-by-default flag is the future "trusted-enough-to-auto-apply" escalation lever.
- **HOST trust read**: the `autoUpdate` flag is exactly the right shape for the trust gradient — propose-and-diff is the safe default, and crossing to in-place mutation is an *explicit, owner-flipped* decision (not silent). Recommend our pilot copy this: `autoUpdate: false` as the canonical default, flipping it per-corpus only after the loop has earned trust. That keeps "the prompt/corpus can't silently rewrite itself" (the expectation-violation guard) structural, not disciplinary.
- **For the co-signed CIO+HOST memo**: gbrain's drift.ts is copyable-as-is for the propose-and-diff half; the open design piece is *where the reviewable changeset lives* (gbrain uses a dated report file — maps to our `dev/active/` working-doc convention) + *who ratifies* (owning agent on its cycle, or PM).

## Target 3 — Trust boundary: `ctx.remote` + `PROTECTED_JOB_NAMES` (read 2026-06-16)

**Read** `src/core/minions/protected-names.ts` + `src/core/minions/queue.ts` (header + `TrustedSubmitOpts`).

### What it does

- **`PROTECTED_JOB_NAMES` set** (11 job types): `shell`, `subagent`, `subagent_aggregator`, `synthesize`, `patterns`, `consolidate`, `contextual_reindex_per_chunk`, `extract-takes-from-pages`, `unify-types`, `skillopt`, `extract-atoms-drain`. These require `allowProtectedSubmit: true` to run.
- **`TrustedSubmitOpts` is a structurally separate 4th arg** to `MinionQueue.add()` — explicitly NOT folded into `opts` — comment says: *"so user-spread `{...userOpts}` payloads can't accidentally carry the trust flag."*
- **Fail-closed**: MCP/OAuth callers never get `allowProtectedSubmit`. Only `ctx.remote === false` (CLI path / trusted-local `submit_job`) can set the flag.
- **`maxSpawnDepth: 5`** — hard cap on agent recursion depth. A subagent can't spawn indefinitely deep trees.

### HOST agent-experience read

**→ Cat-2 (study + map): the `ctx.remote` / `allowProtectedSubmit` model is the cleanest formalization of a trust boundary I've seen — and it maps directly to our consent-gradient + BYOC architecture questions.**

Three things worth naming:

1. **Structural fail-closed (m-36 at the API layer)**: the trust flag is a *separate argument*, not a field on the shared opts object. A caller can't accidentally escalate by spreading `{...userOpts}` — the structure makes privilege elevation impossible, not just harder. This is the same principle as HOST's "unilateral = irreducible mandate" framing: the constraint holds not because someone remembers to enforce it, but because the shape of the API makes the failure mode unreachable. ADR-068 should name this shape.

2. **Protected jobs = cost-bearing jobs, not "dangerous" jobs**: the protected set isn't defined by safety (no PII-access or filesystem-delete in the list) — it's defined by cost and autonomy: `subagent` + `subagent_aggregator` → Anthropic API calls; `synthesize` / `patterns` / `consolidate` → expensive Sonnet loops; `contextual_reindex_per_chunk` → Haiku N times per chunk; `skillopt` → optimizer loops on the agent's own skills. The trust boundary is *cost consent* + *autonomous-agent-spawning consent*, not just safety gating. This is a cleaner frame for BYOC than "what is the agent allowed to do" — it's "who is bearing the cost and did they consent."

3. **Maps to our BYOC architecture**: Principal (PM-as-user) = `ctx.remote === false` → full job access. BYOC-introduced agent = `ctx.remote === true` equivalent → gated out of protected jobs. The practical implication: a BYOC agent in Piper Morgan should not be able to autonomously spawn subagents that burn the Principal's Anthropic credit, or run synthesis loops on the Principal's data corpus, without an explicit `allowProtectedSubmit`-equivalent gate. ADR-068 trust-acceptance criteria seed can be sharpened by this: add a "cannot autonomously spawn cost-bearing jobs" criterion for BYOC agents at trust tier < Principal.

**→ Cat-1-ish (adopt): the 4th-arg structural separation is a cheap pattern to adopt wherever we have trust-tiered capabilities.** If/when Piper exposes a protected-jobs-equivalent API surface, the opt-as-separate-arg shape prevents accidental escalation via payload spreading.

**Mapping caveat**: gbrain is a single-owner system (Garry's brain, one trusted user). The `ctx.remote` boundary is between "Garry's CLI" and "external MCP callers." In Piper with BYOC, the same boundary applies between Principal and BYOC agents — but there may also be a middle tier (PM-owned agents that are trusted but not the Principal). Worth a design note in ADR-068.

---

## Target 4 — Minions queue: observability surface + agent-tree model (read 2026-06-16)

**Read** `src/core/minions/types.ts` (key types) + `src/core/minions/index.ts` (exports) + `src/core/minions/queue.ts` (constructor opts).

### What it does

Key observable types:

- **`MinionJobStatus`**: `waiting | active | completed | failed | delayed | dead | cancelled` + **`waiting-children`** — tree-shaped work is first-class in the queue model.
- **`AgentProgress`**: `{ step, total, message, tokens_in, tokens_out }` — structured progress reporting with token-cost awareness baked in.
- **`TranscriptEntry`** (union):
  - `{ type: 'log'; message; ts }` — free-form log
  - `{ type: 'tool_call'; tool; args_size; result_size; ts }` — tool invocation record
  - `{ type: 'llm_turn'; model; tokens_in; tokens_out; ts }` — per-turn token accounting
  - `{ type: 'error'; message; stack?; ts }` — structured errors
- **`InboxMessage`**: `{ id, job_id, sender, payload, sent_at }` — inter-job message passing. Jobs can send messages to each other; children can update parents.
- **`MinionJobContext`**: the runtime context a job handler receives. Has `log()`, `isActive()`, and `readInbox()` — a job can monitor itself and receive messages from children mid-execution.
- **`maxSpawnDepth: 5`**, **`maxAttachmentBytes: 5 MiB`** — bounded resource use at the constructor level.

### HOST agent-experience read

**→ Cat-2 (study + map): the minions observability model is what m-39 (dashboard welfare criteria) is trying to build — and it's already realized here.**

Three connections to our work:

1. **`TranscriptEntry` as structured session log**: gbrain's `TranscriptEntry` is a typed, timestamped, queryable record of what an agent did: which tools it called, which models it used, how many tokens each turn cost, where it errored. Compare to our session logs (prose narrative, agent-authored). The gbrain model is better for the PM as observer: you can query "total tokens spent by this job," "how many tool calls," "did it hit any errors" — without reading prose. The attention-dashboard (m-39) maps to this: instead of PM reading 10 prose logs, a dashboard aggregates `TranscriptEntry` streams. Worth flagging to PA/CXO as the aspirational architecture for the attention-dashboard.

2. **Token-aware progress (`AgentProgress.tokens_in + tokens_out`)**: the queue surfaces token cost as a first-class field on progress events, not an afterthought. This is a welfare property in HOST's framing: an agent that knows its own token consumption can surface it to the Principal, preventing cost-surprise. More importantly, the *queue* tracking it means the Principal can see aggregate cost across a tree of jobs — not just per-agent. In BYOC, this is the mechanism for "cost consent": the system can tell the Principal "this BYOC workflow has spent N tokens" before crossing a threshold.

3. **`waiting-children` status + `readInbox()`**: tree-shaped work is modeled explicitly. A parent job in `waiting-children` status can monitor child progress via `readInbox()` — children send `ChildDoneMessage` (with outcome) + arbitrary payload messages. This is cleaner than our current model (subagent reports to lead via task output at termination). The inter-job messaging enables "coordinator patterns" where a parent can redirect or cancel children mid-stream, not just wait for their final output. For BYOC welfare: a supervisor job with `readInbox()` could surface welfare concerns from running BYOC subagents to the Principal without waiting for completion.

**→ Cat-2: bounded resources at constructor time** — `maxSpawnDepth` and `maxAttachmentBytes` are set on the queue object, not enforced per-job. This means resource limits are part of the deployment configuration, not each individual job. A BYOC deployment could construct a queue with stricter limits for untrusted callers. Cheap adoption path for our BYOC architecture.

---

### Open for next increments
*(T1–T4 complete; draft is ready for CIO co-sign + PM delivery)*

- **CIO addendum**: HOST T3+T4 sent 2026-06-16. CIO to add innovation lens → co-sign → memo to PM.
- **Follow-on if needed**: `src/core/minions/worker.ts` (how jobs are claimed + executed) and `src/core/minions/supervisor.ts` if it exists — the coordination layer that could inform BYOC welfare monitoring architecture. Not needed for the T3+T4 addendum.
