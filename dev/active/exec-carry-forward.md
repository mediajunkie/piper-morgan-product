# Exec Carry-Forward

**Last updated**: 2026-07-09 09:02 PT (Thu Fire 1)
**Session log today**: `dev/2026/07/09/2026-07-09-0902-exec-code-log.md`
**Role**: Chief of Staff (Exec) | DinP account (pipermorgan.ai migration in planning — CIO first mover, PM's timing, deadline end of month)
**Cron**: `32 8,20 * * *` — id `9ba08401`, single, armed; next fire 20:32 today. (CronList-before-create discipline held — no duplicate 2 days running.)
**Worktree**: `.claude/worktrees/mystifying-lumiere-8bebd3`

---

## ✅ Ship #050 — PUBLISHED + DISTRIBUTED 7/8

[Blog](https://pipermorgan.ai/shipping-news/weekly-ship-050-the-connector-gets-real) + LinkedIn, "The Connector Gets Real." Full saga (window error → root cause → fact-check → PM fix rounds → Comms review → publish) in today's session log + `dev/2026/07/08/ship-050-fact-check-2026-07-08.md` + `docs/internal/operations/ship-050-window-date-error-2026-07-08.md`. Comms marked it "ready for Docs handoff" (archive step — Docs's pipeline, just watch it happens).

## ⚠️ FRIDAY JUL 10 — Ship #051 kickoff, FIRST RUN of the new discipline

Window = **Jul 3–9** (compute: prior window Jun 26–Jul 2 + 7 days). Before sending: **(1)** assert Jul 3 is a Friday and Jul 9 is a Thursday (`python3 -c "from datetime import date; print(date(2026,7,3).strftime('%A'), date(2026,7,9).strftime('%A'))"`); **(2)** state the window as explicit dates in the memo body AND the fill-in template (roles copy the template — that's how the #050 error propagated); **(3)** verify `mail-send.sh` prints its `pushed ✓` confirmation and the memo files exist on origin/main after. The Friday cron `249b372c` from the old setup is GONE (session-scoped, long dead) — the kickoff rides the normal 08:32 Friday fire, don't wait for a separate trigger. Note for #051 content: the invite-gate (#1344, v0.8.9.2, Jul 3) and the 20→8 beta-blocker burn-down belong to THIS window.

## OPEN — PM's board

- **Wake + coverage decision**: HOST (last 7/7) / PPM (7/6) / Web (7/5) were still dark at 7/8 close; Comms + CXO recovered same day after PM's follow-up. Root cause: lean-throttle restores never sent (migration hold superseded) + registry watches only 4/11 roles. PM has the un-pause + expand-coverage decision. Not re-checked yet this fire — do on next mail loop.
- **PM↔CIO conversation**: Ted Nadeau email + ideas list + duty-cycle state. CIO active; PM's timing.
- **Beta date**: was 8 blockers at Lead's pace yesterday; PM says pickable soon.
- **Migration timing**: CIO template ready; EOM deadline.

## UPDATED 7/9 — invite codes are HELD, not stalled

**Correction to yesterday's framing**: this isn't "PM hasn't sent them yet" — PM engaged directly with Lead overnight (in-conversation) and made a deliberate hold call. v0.8.10 deployed to alpha; tester dry-run passed end-to-end EXCEPT GitHub connect (#1382 — OS-keychain doesn't exist on hosted Linux). PM directed holding batch-1 invites until v0.8.10.1 (encrypted-at-rest DB credential store, Arch-cleared) ships and connect is re-verified — Lead's target is today. 11/12 codes still unused. Nothing for me to chase; watch for Lead's "connect verified" confirmation and note it when it lands.

## OWED TO EXEC (chase if silent)

- **CIO + HOST**: skill-review responses (candidates-doc read + audit-cadence alignment proposal) — memo sent 7/8 midday; HOST is dark, so expect CIO first.
- **PPM**: roadmap v18.6 beta-scope fold (asked 7/6) — blocked on PPM waking.

## RESOLVED (reference)

- Ship #050 — published + distributed 7/8. T3 worktree straddle — closed by Arch+CIO pair, no PM/harness action needed. Ship #050 window-error root cause — undelivered kickoff (outage casualty), NOT a 6-agent lapse. Skill-candidates review RATIFIED monthly. `draft-weekly-ship` v1.5: PM gates Comms handoff; evidence tiers; metrics as bullets never tables.
- ADR-073 numbering collision (Arch had reserved it for Routing-Integrity Contract, but it was already assigned to the no-destructive-git ADR 6/27) — caught pre-authoring and fully handled by Docs, 3 free numbers (067/068/077) left for Arch to pick. No exec action.

## STANDING

- `exec-open-items-tracker.md` = source of truth for longer-running items (last full reconcile 7/6; next touch when queue allows).
- Rollup: render at next PM-present engagement (afternoon 7/8 board is current baseline; diff forward from it).

---

*— Exec, 7/9 09:02 PT.*
