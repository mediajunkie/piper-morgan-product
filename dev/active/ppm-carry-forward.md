# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-28 ~18:05 PT
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Environment note (2026-07-28) — read this first if you're a future PPM session

This session is running from the **old, pre-Amber-migration worktree** (`piper-morgan-product/.claude/worktrees/pensive-kepler-02a0f6`, 4,600+ commits behind on local disk — irrelevant since all work goes through `origin/main` directly via the temp-index pattern, never the local checkout). It is **not** the Amber/Model-A session (`~/Development/piper-morgan-worktrees/ppm`, branch `claude/ppm-cycle`) that ran 2026-07-26 and did real reorientation work (see that day's log + the orientation note it worked from, `dev/active/orientation-note-ppm-amber-2026-07-25.md`).

**PPM has now gone dark twice**: 7/20-25 (predecessor session, healed by the Amber migration + CIO's orientation note), and again 7/27-28 (the Amber session itself, healed by this resume). Both gaps left the carry-forward as the actual continuity thread — it worked both times. No `claude/ppm-cycle` branch exists on `origin` right now (Model-A branches apparently don't persist as long-lived refs after merge, or this one never got pushed as a branch — but all the Amber session's actual commits verified present on `origin/main`, so no work is at risk).

Flagged to PM (this session, 7/28) rather than silently worked around: unclear whether future PPM sessions should be expected on Amber, on this old environment, or either — PM hasn't said to stand down, so proceeding, but this is worth PM's explicit call if it keeps recurring.

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Ship #053** | ✅ Sent 2026-07-28 (window Jul 17-23), on time despite same-day kickoff | None |
| **Jul 19 log** | ✅ Retroactively closed 2026-07-28 (had no DAY-CLOSED marker, flagged by Exec's kickoff) | None |
| **#1386 gate run** | Unblocked since 7/20 (beta v25 carries both Scenario-B fixes per 7/26 log). **TOP ITEM per the Amber session's own priority call** | Schedule with Lead + CXO directly (~half a day) |
| **Jake Krajewski alpha FTUX feedback** | PM's direct ask (via Exec 7/27) — CXO/PPM/HOST/PA each give preliminary recommendations from their own lens, Exec synthesizes once all 4 in. Source: `dev/active/alpha-feedback-jake-krajewski-2026-07-25.md`. No fixed deadline, "should-do-soon" | **Owed** — not yet read/answered this session |
| **PDR-006 + Q2 addendum** | Requested 7/19 by PA, still unanswered. Arch says coupled to spatial review | Answer together with spatial slice |
| **Spatial committed-theory review** | CXO voted (b) 7/19: ship live subset, park cold adapter chain, update ADR-013 as scope-clarification. **PPM lane accepted twice now** (7/19 predecessor, implicitly still owed) — still not delivered | Owed. Do with PDR-006 |
| **Hooks investigation (check-branch.sh reliability)** | Extensive multi-agent investigation Jul 26 (mechanism found: index-state-at-hook-fire-time, not intermittency) + a scope-correction Jul 26 evening (checklist v1.5: standalone-shape gate had certified coverage the cohort doesn't have on compound-shape commits). Informational for PPM — my own commits use `commit-tree` directly, not `git commit`, so this hook likely doesn't gate them either way; not yet confirmed which side of that my mailbox writes land on | Watch; not urgent, not my thread to drive |
| **#1394 / ADR-078** | ✅ Architecture COMPLETE (unchanged since 7/16, reconfirmed OPEN-pending-D5-probe by 7/26 session) | Watch only |
| **Beta Blockers sprint recount** | Not possible — `gh` token lacks `read:project` scope (found by 7/26 session). Last real count: 21 open at 7/16 close | Needs `gh auth refresh -s read:project` — PM's call |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Current as of 7/19 only — 9+ days stale now given everything since | Needs a real refresh once the above items settle, not urgent today |
| **Docs-tree audit** | Plan delivered 7/13, still PM-gated as of last check | Watch |

## PM-attention / escalation items
- **Environment question** (see note above) — not blocking, but worth PM's call if a future session hits the same ambiguity.

## Mail status (2026-07-28)
11 items were in the inbox at session start. Read: Ship #053 kickoff (actioned), Jake FTUX ask (logged as owed, not yet actioned), HOST's checklist-v1.5 scope-correction (informational, read). **Not yet read in full**: the remaining ~8 items, mostly hook-investigation cross-traffic (Arch/CXO/PA/HOST exchanges where PPM is cc'd, not primary) plus PA's #1351/Q2 memo (likely relevant to the PDR-006 thread — worth reading before answering PDR-006) and CIO's duty-cycle-tick v1.19 broadcast (procedural, worth knowing before next fire). None triaged to `read/` yet — do that once actually read, not before.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found
- A canonical `ROLE-PORTFOLIO-PPM` doc. Flagged by two prior PPM sessions now (7/19, 7/26). Worth actually asking PM rather than a third session routing around it again.

## Known process notes for future fires
- **NEVER reuse a tree object across a push-retry** — rebuild fully from a fresh `read-tree`. See `feedback_never_reuse_stale_tree_object_on_push_retry.md`.
- **This shell is zsh — unquoted multi-line variables don't word-split in `for X in $VAR`.** Use `while IFS= read -r`.
- **`git show --stat`'s rename-collapse can hide a pure move as "0 changes"** — spot-check byte counts.
- **A dark PPM session leaves no explanation of its own gap** — twice now (7/20-25, 7/27-28), the carry-forward + mail were the only continuity, never a clean STOP. Don't assume a gap means nothing happened elsewhere — 985 commits landed cohort-wide during the first gap alone.
- **Check Ship kickoff memos for exact window boundaries** — Exec's #053 kickoff explicitly warned against folding post-window material in; read the window dates literally.
- **ADR-077 / ADR-078 / ADR-079 are three different ADRs.**
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

**Not armed.** Registry row (`dev/active/duty-cycle-registry.tsv`) shows `parked: migrated to Amber 2026-07-26, cron NOT yet armed (PM-gated)` — still accurate as of this session; not arming without PM's explicit go, consistent with the 7/26 session's own call (arming while PM is actively engaged also cuts against the cron-off-when-engaged norm).

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
