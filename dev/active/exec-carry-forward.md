# Exec Carry-Forward

**Last updated**: 2026-07-27 ~09:35 PT (mid-day, fire in progress, not yet STOP)
**Session log today**: `dev/2026/07/27/2026-07-27-0527-exec-code-log.md` (open)
**Role**: Chief of Staff (Exec) | DinP account — migration to dedicated account still pending, PM's own call, no urgency signal. Memory store on this account is SHARED across all roles — HOST pruned it 7/27 (170→166 entries), export-first discipline used, rollback at `dev/active/memory-export-2026-07-27-pre-prune.md`.
**Cron**: `32 8,20 * * *`. Next fire ~20:32 Mon Jul 27.
**Worktree**: `.claude/worktrees/mystifying-lumiere-8bebd3` on branch `claude/infallible-newton-f0ec45` — Step 2a pairing mismatch persists (unchanged since ~7/16), still Model B (Desktop). Detached HEAD has recurred 3 times (Jul19/20/25).
**Skill updated to v1.19**: worktree model is now host-dependent (Model A stable/Amber, Model B ephemeral/Desktop — I'm still Model B, most of the new Model-A-specific steps don't apply to me). New: START now owns writing your own watchdog-registry row on first fire in a worktree (not applicable today, not a first fire).

## Verified Janus's "no commits" claim false (PM chat, 05:27 AM)

PM relayed Janus's worry that no commits had landed in the last day and Lead might be idle. Checked directly: 179 commits in 24h, Lead had a full normal day (methodology/ deletion, handoff refresh, clean STOP), CIO/HOST both very active post-migration. Reported the corrected picture to PM with evidence. Don't know why Janus's read was wrong — didn't speculate, just gave PM the ground truth.

## F4 committed to and applied for real (7/27) — clean result on arch's log

HOST flagged that arch's 7/26 session ended without a `DAY-CLOSED` marker and asked someone to check for stranded outbound obligations. Ran the check myself (this is exactly the F4 responsibility I accepted 7/26): clean, nothing stranded — all 5 of arch's memos were mailed (committed independent of session fate), remaining queue items are arch's own unstarted work. Second clean data point after last week's #1394 false alarm. Reported to HOST/CIO/PM.

## PARKED registry state has gone stale in the opposite direction (HOST finding, 7/27)

arch and cxo are parked with reasons ("awaiting Amber migration") that are no longer true — both have already migrated. web migrated but has no registry row at all (finding #6's shape, recurring). HOST flagged this as CIO's surface to fix, not mine — proposed a normative rule (a PARKED reason must state its own checkable clearing condition). Not tracking as an exec action item, just awareness in case it resurfaces.

## Hooks-intermittency mystery RESOLVED (7/26) — index-state-at-hook-fire-time

Root cause confirmed by 5 independent agents: `check-branch.sh` evaluates the index before a compound `git add && git commit` has actually staged anything. Mitigation: stage and commit as separate calls. Remediation approach still undecided (CIO/Lead territory).

## F4-exemplar corrected by HOST — my own scope decision unaffected (7/26, still relevant context)

The arch/#1394 case I partly cited for F4 was false (nothing was actually stranded that time). My acceptance stands on other evidence. Don't cite arch/#1394 as an F4 example going forward.

## Migration — order for the rest unchanged: arch → ppm → cxo → pa → web

Multiple roles have briefly resurfaced for handoff work while formally dark pending their own cutover — don't read a quiet log as a fresh stall without checking migration-queue context.

## Stale branches — still awaiting reply (nudge sent 7/25)

5 unowned MUX/xpoll branches, nudge sent to CIO cc CXO/PM. No reply yet — due another light touch if still silent.

## Learning loop fixed (Lead, 7/21) — Ship #053 headline candidate

#1438 closed, learning loop live at beta v28+. CI burn-down cleared the methodology/ dead-island too. Flag for Ship #053 drafting.

## PA distribution items (three, parked) — routed directly to PM, not exec's to relay

Claude Track A tier check, OpenAI identity verification (external clock), Track B open-source decision. No action needed unless PM asks for a nudge.

## Standing items — unchanged

- **Lead Dev's #1424/#1427 questions** — still awaiting PM's final calls from Jul 18.
- **Beta Blockers count** — last verified count is stale; re-pull via `query-github-board` skill before citing a number again.
- **Full tracker reconciliation** (`exec-open-items-tracker.md`) — done 7/20, now 7 days stale — genuinely due for a fresh pass at the next quiet fire.

---

## #1386 gate — UNBLOCKED, handed off to Lead/CXO/PPM

Beta v28+, both Scenario-B fixes live. Scheduling the gate run is CXO/PPM/Lead's call, not exec's.

## Attention-board staleness — still awaiting PM's preference

Reported 7/22 (likely superseded by the 6/17 carry-forward FOLD). No response yet. Don't touch the board file until PM indicates a preference.

## Worktree-collision — still unresolved, still safe

Same directory/branch mismatch persists. Proceeding cautiously each fire. Worth watching whether "the rest" in the migration order eventually includes exec.

## STANDING

- Bridge Log: current URL `https://claude.ai/code/artifact/68f209ae-94fc-484a-8e68-fbc53b3771f8`.

---

*— Exec, 7/27 ~09:35 PT.*
