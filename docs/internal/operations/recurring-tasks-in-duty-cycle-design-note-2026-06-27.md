# Design note — role-recurring tasks in the duty-cycle structure

**STATUS: DISCUSSION INPUT** (PM idea 2026-06-27; for the upcoming Exec↔CIO↔PM discussion — not ratified, not being built). Author: Exec.

## The idea (PM, 2026-06-27)

Each duty-cycle agent maintains three surfaces: a **session log**, a **durable task list** (open + closed-not-yet-pruned), and an **attention document** (anything blocking a task that needs PM). The task list should *also* carry **recurring tasks at role-specific cadences** — above the baseline daily work — e.g. Docs omnibus (daily), Exec weekly-review kickoff (Fri), Docs audit (weekly), HOST 360 questionnaire (quarterly). Some of these already have GitHub Action workflows that mint recurring tickets, "but I still need to tell the agents about them." Cron may be better. The need: **operationalize role-specific non-daily recurring obligations** in the process.

## Inventory findings (actual state, 2026-06-27)

**The three surfaces are NOT standardized — PM's suspicion confirmed:**

| Surface | Reality |
|---|---|
| Session log | Standardized, skill-governed (`dev/.../{role}-log.md` + DAY-CLOSED). Solid. |
| Durable task list = `{role}-standing-items.md` | 10/11 roles have it — **Exec is the gap** (keeps it folded in carry-forward). |
| "Attention document" | **Supposedly** folded into the carry-forward 2026-06-17 (escalations docs deprecated). **REALITY (verified 6/27): the fold was declared but never fully executed — the cohort is SPLIT across two conventions.** |

**⚠️ The attention-surface convention is split (the real Step-0 blocker, found 6/27):**
- **Lead + Docs still actively run on `duty-cycle-escalations-{role}.md`** as their live attention surface — Lead reconciled its escalations doc at the 6/25 STOP; it holds all of Lead's current Open items. These files are **live, not stale** (a near-miss: a "delete the deprecated files" sweep would have destroyed live attention items — caught by per-file inspection; cf. "investigate before deleting / never sweep up others' work").
- **Other roles** (arch/cio/host/web/pa/exec) moved PM-attention items into the **carry-forward** (escalations docs old + untouched since ~the fold → content likely migrated, but each needs per-file verification before removal).
- **CXO has NEITHER** an escalations doc nor a carry-forward — genuinely missing an attention surface.
- **PPM** runs on its escalations doc (6/6), no carry-forward.

So Step-0 is **not** mechanical cleanup — it's: **(1) decide the canonical attention surface** (carry-forward vs escalations-doc — one wins), **(2) have each role reconcile its OWN live items into it** (not Exec bulk-editing others' files), **(3) then** retire the losing surface + give CXO the canonical one + give Exec a standing-items. The 6/17 fold's lesson repeats: a convention declared but not mechanically enforced silently doesn't happen.

**Prior art exists** — this isn't net-new: `memo-host-to-cio-...-recurring-workflow-owner-routing-2026-06-08` → folded into **methodology m-36 class-2** ("recurring-workflow owner routing"). CIO should bring m-36 to the discussion.

**Recurring triggers already exist as GH Actions** (the "tickets I have to tell agents about"): `weekly-docs-audit.yml`, `quarterly-maintenance.yml`, `role-health-check.yml`, `dependency-health.yml`, `pattern-sweep.yml`. Several map directly to PM's examples.

## GitHub Actions survey (the existing trigger layer)

Of 18 workflows, **7 are scheduled (cron); the other 11 are CI** (push/PR — not recurring tasks). The scheduled set IS the recurring-task trigger layer that already exists:

| Workflow | Cron | Cadence | Maps to |
|---|---|---|---|
| `weekly-docs-audit.yml` | `0 16 * * 1` | Mon weekly | **Docs audit** (PM's example) |
| `link-checker.yml` | `0 2 * * 0` | Sun weekly | Docs (link integrity) — mints issue |
| `role-health-check.yml` | `0 16 * * 1` | Mon weekly | HOST/role health |
| `pattern-sweep.yml` | `0 17 * * 2` | Tue weekly | CIO pattern sweep |
| `dependency-health.yml` | `0 9 * * 1` | Mon weekly | Lead/infra — mints issue |
| `quarterly-maintenance.yml` | `0 9 1 1,4,7,10 *` | Quarterly | **HOST quarterly** (PM's example) |
| `e2e-aaxt.yml` | `0 6 * * *` | Daily | (CI test run — NOT a role task) |

**The diagnosis of PM's "I still have to tell them":** the trigger layer *already exists* (6 recurring role/maintenance reminders), but it's **disconnected from the agents two ways** — (1) most mint a **GitHub issue**, and per cohort norm agents do NOT autonomously watch GH issues (mail is the signaling surface, issues are passive artifacts) → a reminder fires into a forest no agent walks; (2) the recurring task is **not declared in the agent's own task list**, so the agent doesn't proactively own it. PM becomes the human bridge between trigger and agent. *(Mixed today: a couple — quarterly-maintenance, role-health-check — appear to reference mailboxes, so a partial mail-bridge exists; weekly-docs-audit / pattern-sweep / link-checker / dependency-health mint issues only. The bridge is inconsistent, not absent.)*

So the trigger side is **80% built** — the gap is the **binding** (trigger → agent-owned task), not the triggers themselves.

## The core design insight

A recurring task has **two separable parts** that are currently conflated/scattered:
1. **Declaration** — where the obligation + its cadence live durably (→ the task list / standing-items).
2. **Trigger** — what makes the agent act on cadence. Today this is scattered across: GH Actions (fire on cron, but the agent doesn't *see* the ticket → the "I have to tell them" gap), ad-hoc per-task crons (fragile — session-scoped; e.g. the Friday-kickoff cron I hand-rolled today dies with the session), and tribal knowledge.

**Proposal to put to CIO: the duty-cycle fire becomes the universal scheduler.** Each role's standing-items gets a **recurring-tasks registry**: `task | cadence | last-completed | trigger`. At each fire, the agent checks "what's due?" (cadence vs. last-completed) — exactly how a crontab is read. This:
- Uses the mechanism that **already runs daily for every cycling role** (no per-task cron sprawl, no GH-Action-awareness gap).
- Makes the agent **proactively own** its recurring obligations instead of waiting to be told.
- Needs **last-completed state** per entry (a weekly task must know when it last ran), updated when the agent completes it.
- Gives a natural **cohort view**: Exec/the attention board can surface "what's due across the cohort today."

**Worked example (today):** the Friday weekly-review kickoff = declaration in methodology-25 + trigger via cron. That's the dual structure in miniature — and its hand-rolled fragility (session-scoped cron) is precisely the problem the generalized fire-as-scheduler design removes.

## Open questions for the CIO discussion
1. Registry home: extend `{role}-standing-items.md` with a recurring section, or a separate `{role}-recurring.md`?
2. Trigger unification: the trigger layer is ~80% built (7 scheduled GH Actions). The real gap is the **binding** (trigger → agent-owned task). Two candidate bindings: **(a) GH Action → mail** (the workflow signals the agent's inbox, which it DOES watch — minimal change, keeps GH Actions as triggers), or **(b) fire-as-scheduler** (agent's registry is the source of truth; fire computes what's due; GH Actions feed or retire). Or both (Action mails + registry owns). Decide one source of truth — no double-fire.
3. How does m-36 class-2 already frame recurring-workflow routing — does this extend it or supersede it?
4. **Step-0 is a convention decision, not cleanup** (revised 6/27 after the survey found the split): pick the canonical attention surface, have each role reconcile its OWN items into it, enforce it in the fire — *then* layer recurring tasks. See below.

## Recommended first step (revised 6/27 — survey found a split base, not just an uneven one)
1. **CIO/PM decide the canonical attention surface** (carry-forward vs escalations-doc — one wins). Carry-forward is better-defended (the 6/17 fold already chose it; the cohort-attention rollup reads it) — but it must be **enforced in the fire**, not just declared.
2. **Each role reconciles its OWN live items** into the canonical surface (Lead/Docs/PPM migrate escalations-doc → carry-forward; CXO creates one; Exec adds a standing-items). Exec coordinates + tracks; Exec does **not** edit others' surfaces.
3. **Then** retire the losing surface per-role (after that role confirms migration) and build the recurring-tasks registry + fire-as-scheduler on the uniform base (with CIO, m-36 owner).

**Meta-lesson:** the 6/17 fold proves a convention declared without a mechanical enforcement point silently doesn't happen — 10 days later the cohort was still split and nobody noticed until this survey. Whatever Step-0 decides, enforcement must live in the fire (checked every cycle), not in a memo.
