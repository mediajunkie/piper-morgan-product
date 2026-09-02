# Cohort Attention Rollup — Runbook / Spec

**Status**: v1.0 (2026-06-19, Exec). **Owner**: Chief of Staff (Exec). **Executable companion**: the `cohort-attention-rollup` skill (`.claude/skills/cohort-attention-rollup/SKILL.md`). **Discipline pin**: memory `feedback_attention_board_sweep_not_vantage`.

This runbook is the **spec + judgment layer**. The skill is the **how** (gather → verify → render → deliver, step by step). This doc is the **why, when, and how-much** — the parts that are judgment, not mechanism: when a refresh is mandatory vs. skippable, what the board is *for* (the trust stakes), the closed Exec↔PM loop, and the evidence that the discipline pays. When the two disagree, fix both; keep them paired.

> **One-step-at-a-time (PM 2026-06-19).** We are iterating on this process deliberately: spec/runbook first (this doc), tighten the skill against it next, skillify further only if it helps. The **Iteration log** at the bottom is the durable home for that — append, don't lose it in chat.

---

## 1. What it is

The attention rollup is a PM-facing board (`dev/2026/06/23/exec-attention-board.html`, also renderable as an inline widget) that answers one question for PM at a glance: **"is anything stuck or waiting on me, and is everything else actually fine?"** Exec maintains it by sweeping the cohort's self-reported state, verifying each item against live truth, and rendering it blockers-first.

**It exists so PM can disengage.** PM 2026-06-18: *"it calms my mind knowing things are running smoothly as I attend to my OpenLaws project."* That is the whole point and also the whole risk: a board PM relies on to *stop looking elsewhere* must be **verified-true**, never **assumed-true**. A false "all clear" is not untidiness — it is a trust breach, because PM has stopped checking the things the board claims are fine. (This is HOST welfare-criterion D: no silent non-surfacing — a quiet board must mean *verified-clear*, never *haven't-checked*.)

## 2. The loop (both halves)

The rollup is a closed loop, not a one-way report. Both halves are load-bearing:

| | Who | Does what |
|---|---|---|
| **Sweep & surface** | Exec | Sweeps the source set, verifies each item, renders the board blockers-first, flags what needs PM. Routine cadence + on-demand. |
| **Review & act** | PM | Reviews the board, clears the items only PM can clear (UAT, decisions), discusses ambiguous ones with Exec or routes them to the owning agent. |
| **Post back** | PM | *"I will keep you posted between sweeps as best I can"* (PM 2026-06-19) — tells Exec what changed (what got unblocked, decided, reassigned) so the next render reflects reality, not a stale snapshot. |
| **Reflect** | Exec | Folds PM's between-sweeps updates into the board so it never lags behind what PM already actioned. |

Implication for Exec: **treat PM's chat statements as board inputs.** When PM says "I cleared #1269" or "I'm routing that to Arch," that's a board mutation — update it, don't wait for the next scheduled sweep.

## 3. When to refresh — the judgment rule

The skill's cadence (PM-ratified 2026-06-13) is the baseline: render at each day's first PM-present START; re-render incrementally when PM and Exec are in conversation; keep the underlying data current via the duty cycle; if nothing board-relevant changed, *say so rather than re-render an identical board.*

The **sharpened rule** (learned 2026-06-19) sits on top:

> **PM's engagement state flips the calculus.**
> - When PM is **heads-down / disengaged** (e.g. deep in another project), a light verify-and-hold is acceptable — confirm nothing material moved, don't re-render for a cosmetic date-bump.
> - When PM is **actively dipping in to unblock agents**, a **full sweep-and-verify is mandatory** — even (especially) after a long quiet stretch when it *feels* skippable. That "feels skippable" moment is the trap: it coincides exactly with PM being most reliant on the board being whole and current.

The honest tell that you owe a full sweep: **PM asks "have you done a rollup refresh recently?"** If the truthful answer isn't "yes, just now / since the last material change," the answer is *do one now*.

## 4. The discipline: sweep-and-verify (never from-vantage)

The single most important rule, and the one most prone to silent erosion:

**Render from a fresh sweep of the source set, never from your own memory of what's going on.** "From-vantage" maintenance — listing the items *you* happen to know about from your own fires — fails two ways at once: it **misses other roles' items** (you weren't reading their state) and it **inherits stale phantoms** (a role's doc listing closed work as open). Both lie to a PM who has disengaged.

Mechanics live in the skill (Step 1 gather, Step 2 live-state verify, "no silent failures"). The **source set** post-FOLD (2026-06-17): per-role `dev/active/{role}-carry-forward.md` (perspectives, not truth) + **GitHub live-state** (re-derive truth) + **cc'd blocker-mail** in the exec inbox (blockers ride mail, not docs). The deprecated `duty-cycle-escalations-{role}.md` docs are **not** a source — frozen/stale by definition.

Verify *every* candidate before it reaches the board: a "needs your call on #X" whose issue is closed is resolved; a stale source doc is flagged as stale, not presented as current; an unverifiable item is marked "unverified," never silently dropped or silently promoted.

**Invoke the skill; don't run the rollup from memory.** This surface has a demonstrated drift failure — the 2026-06-16 "from-vantage, not a real sweep" lapse was precisely a run-from-memory that skipped the skill's Step 1 + Step 2. The skill is the anti-drift enforcement: invoking it (`/cohort-attention-rollup`, or the Skill tool) makes the canonical procedure win over half-remembered habit. This is a **per-surface** judgment, not a universal rule — contrast `duty-cycle-tick`, where high-frequency daily repetition makes an internalized run efficient and reliable. The rule: **high-frequency / low-stakes → internalizing is fine; low-frequency / high-stakes / drift-prone (this rollup) → invoke the skill.** When in doubt on a high-stakes surface, load the skill. *(Honesty note: the 2026-06-19 rollup that prompted this section was itself run from memory — faithfully, but un-enforced. That's the gap this rule closes.)*

## 5. Structure: blockers-first

Per PM directive 2026-06-17: **"Blockers should be at the top of my attention list."** The board renders in this order:

1. **Needs you** — items only PM can clear (UAT, decisions, voice-pass). Red, top, each tagged with the agent waiting.
2. **Blocked on another agent** — work stuck agent-on-agent, for awareness / nudge (and Exec often nudges the gating agent in the same pass — that's Exec's coordination lane).
3. **Lower-urgency decisions** — real but not time-pressured; stale-but-flagged items live here labeled as needing a refresh before action.
4. **In flight** — for awareness, no action.
5. **Clean · verified resolved** — what's genuinely closed, so "quiet" reads as *checked*, not *ignored*.

## 6. Worked examples — the verify pays (receipts)

Every one of these would have lied to PM if rendered from assumption:

- **Ship #047** would have shown "overdue voice-pass" — it had **published**. (6/18)
- **Arch** would have shown "dormant" (a watcher flag) — it had **resumed**. (6/18)
- **#1165 / #1193 / #1133 / #1079** sat in stale escalations docs as "open decisions" — all **closed**. (6/16)
- **Docs "6 escalate branches → your decision"** looked like a live PM queue — the sweep was **4 days stale** with none since; flagged needs-refresh, not surfaced as current. (6/19)
- **HOST "waiting on the pilots"** read as not-yet-filed — both pilots **were filed**; HOST's carry-forward was stale and HOST hadn't registered them. The sweep caught the gap and triggered an Exec nudge. (6/19)
- **Redis "pending PM's go"** (a *security* needs-you, the board's top item) — Lead had **FIXED + closed it 3h prior** (`#1311`). Lead's carry-forward was only 24 min old but still lagged its own author's commits (heads-down). A `git log --since` cross-check against Lead's commits caught the phantom. (6/21 — the catch that produced the §4 heads-down-role rule below.)

## 7. Iteration log + open questions

*(PM 2026-06-19: "let's keep iterating." Append here.)*

- **2026-06-19 v1.0** — Runbook created (this doc). Skill already covered mechanics; this adds the judgment layer (refresh rule, trust-stakes), the closed Exec↔PM loop incl. PM's post-back commitment, and the receipts.
- **2026-06-21 — heads-down-role rule (§4 sharpening).** PM flagged Lead "may not update their carry-forward when head's down." The lesson: **a freshly-written carry-forward can still be stale** — a heads-down role ships commits without updating their tracker. So Step-2 live-verify must include a **`git log --since` cross-check of the busiest/heads-down roles' commit-activity** (Lead especially), reconciled against what their carry-forward claims — *commits don't lie, trackers do*. Caught the Redis phantom within minutes (see §6). Pin `feedback_attention_board_sweep_not_vantage` extended.
- **2026-06-21 — the cross-check is two-way (PM extension).** PM: *"checking commits is a great idea and perhaps nudging or guiding agents whose trackers are stale can follow from that."* So the commit-cross-check doesn't only correct the board — when it reveals a **stale tracker**, Exec **gently guides the owning agent to refresh it** (heads-down-aware: "when you next surface," never a mid-flow demand). One-way board-correction → **two-way tracker-hygiene loop**: the board stays honest AND the cohort's trackers improve, so future sweeps + PM's direct check-ins both get more reliable. Meta-note PM named: these process improvements come from *the cohort surfacing patterns* + *PM being clear about needs* — neither half alone.

**Open / candidates for the next step:**
- **Fold §3's sharpened refresh rule + §5 blockers-first ordering into the skill** (the skill's cadence section predates both). Low-risk; the obvious next "tighten the skill against the spec" move.
- **Asymmetric-knowledge sweep** (HOST welfare-criterion F + CIO note): the rollup GitHub-verifies *issues* but a non-issue PM-block (a policy/approval/decision living only in a carry-forward) can still slip. Worth a dedicated pass-line in the skill's gather step.
- **Skillify further?** Only if the judgment in §3 can be made reliable as a procedure rather than a read. TBD — revisit after a few more sweeps under the v1.0 rule.

---

*Related: `cohort-attention-rollup` skill (executable) · memory `feedback_attention_board_sweep_not_vantage` (the discipline + stakes) · the escalations-docs FOLD (2026-06-17, source repointing) · HOST dashboard welfare-criteria v0.2 (D/E/F).*
