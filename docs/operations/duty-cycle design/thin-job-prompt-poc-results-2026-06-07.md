# Thin-job-prompt PoC — results (day-1 dogfood, 2026-06-06→07)

**Owner**: CIO. **Status**: PoC PASSED on the CIO cron; ready to propose cohort rollout (co-authored w/ HOST). **Origin**: gbrain finding #3 (thin-job pattern) → PM-approved adopt 2026-06-05 → built + dogfooded 6/6–6/7.

---

## What the thin-job-prompt is

The fat ~40-line `DUTY CYCLE TICK` cron prompt is split into three:
1. **Durable procedure** → `.claude/skills/duty-cycle-tick/SKILL.md` (versioned, one place for the whole cohort).
2. **Transient carry-forward** → `dev/active/{role}-carry-forward.md`, read at fire-time (not frozen in the prompt).
3. **The cron prompt** → ~8 lines: role + worktree + cron-expr + "run the duty-cycle-tick skill" + carry-forward pointers + a fallback line.

Retires the hand-refresh-the-prompt-every-re-arm chore; versions the procedure once (no per-agent drift); shrinks the re-arm error surface.

## What the dogfood validated (CIO cron, 6/6–6/7)

| Risk being tested | Result |
|---|---|
| Does a one-line cron prompt reliably **trigger skill-load**? | ✅ PASS — every autonomous fire (~12 substantive + holds) loaded + followed the skill. |
| Does **carry-forward-from-file** work (vs frozen-in-prompt)? | ✅ PASS — state read cleanly from `cio-carry-forward.md` + cycle-log tail every fire; hand-refresh chore gone. |
| Does **keep-armed-through-conversation** (Rule 2) hold? | ✅ PASS — cron stayed armed through multiple PM exchanges; presence-aware, no clash. |
| Does it survive an **overnight self-wake** (STOP→WATCH→START)? | ✅ PASS — **3rd consecutive clean overnight**; STOP 6/6 23:37 → WATCH 02:28 → START 04:17, skill fired across the boundary. |

## Two bugs the dogfood caught + fixed (the value of dogfooding-before-rollout)

Both would have hit **every** cohort agent on rollout:
- **v1.1 (HOST cross-agent review, 6/6)**: Step-3 dispatched by clock-hour (tuned for `2,4-23`), so a low-freq `*/3` agent whose first morning fire is ~06:37 would fall through to WORK and **silently skip its new-day START**. Fix: route START by state ("no-session-log-today"), not hour.
- **v1.2 (CIO overnight dogfood, 6/7)**: pure-state was *almost* right — but the continuous shape's ~2am WATCH fire *also* has no-session-log-today, so the bare rule would **mis-START at 2am**. Fix: state+hour hybrid — overnight branch checked first + hour-gated; START rule gets a `≥~4` overnight-window guard. (HOST's low-freq fix preserved.)

**Net**: state gates START-vs-WORK; hour gates overnight-WATCH-vs-morning-START. The skill is now v1.2.

## Honest open items before/at rollout
- **Fresh-session skill-load after compaction** not yet explicitly tested (within-session it persists; a post-compaction fire should re-invoke the skill cleanly via the thin prompt, but worth confirming).
- **Per-shape coverage**: continuous (`2,4-23`) validated on CIO; low-freq (`*/3`) validated by *reasoning* + HOST's review but not yet *run* — HOST/Arch co-dogfood is the low-freq validation; Web's 2×/day variant separate.
- **Rule-2 keep-armed-default** rides with this rollout (bundled — one cohort touch).

## Recommendation
Rollout-ready pending: (a) HOST/Arch co-dogfood confirming the low-freq path live, (b) PM nod for the cohort broadcast. The cohort-rollout *proposal* (per-agent thin-prompt template + sequencing + Rule-2 bundle) to be co-authored with HOST (agent-experience half). This doc is the factual basis.

*Filed by CIO, 2026-06-07 (Fire 2). Companion: `.claude/skills/duty-cycle-tick/SKILL.md` (v1.2), `cron-shape-experiments.md`, `procedures/cron-lifecycle.md` (Rule 2).*
