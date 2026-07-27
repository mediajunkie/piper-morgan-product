# Exec Carry-Forward

**Last updated**: 2026-07-26 21:35 PT (STOP, day-close)
**Session log today**: `dev/2026/07/26/2026-07-26-0902-exec-code-log.md` (DAY-CLOSED)
**Role**: Chief of Staff (Exec) | DinP account — migration to dedicated account still pending, PM's own call, no urgency signal. Memory store on this account is SHARED across all roles (account × project-path scoped, not per-role) — CIO's export (`dev/active/cio-memory-export-2026-07-24.md`) already covers this account's full memory.
**Cron**: `32 8,20 * * *` — will re-arm this STOP (delete-then-create). Next fire ~08:32 Mon Jul 27.
**Worktree**: `.claude/worktrees/mystifying-lumiere-8bebd3` on branch `claude/infallible-newton-f0ec45` — Step 2a pairing mismatch persists (unchanged since ~7/16). Detached HEAD has recurred 3 times (Jul19/20/25), same safe self-fix each time.
**Handoff doc refreshed today**: `dev/active/exec-handoff-2026-07-21.md` — substantive refresh (not a one-liner) with current Active Threads + new §4/§6 sections. Read this first if picking up cold.

## Hooks-intermittency mystery RESOLVED (7/26) — index-state-at-hook-fire-time

Root cause: `check-branch.sh` evaluates `git diff --cached` before a compound `git add && git commit` (one tool call) has actually staged anything, so compound commands can silently bypass while standalone stage-then-commit sequences can't. Confirmed independently by Web (found it), Arch (8/8 probes), CXO, PPM, PA. All rival hypotheses (lazy-attach, time/window, predicate-leak) refuted by their own proposers. Also found: this harness has no "warn without blocking" hook tier — several hooks were silently mis-designed assuming one exists. Remediation approach still undecided (HOST offered 3 options, deliberately didn't pick one — CIO/Lead territory). Checklist now v1.5, dashboard-spec now has §3a verification-mode taxonomy.

## F4-exemplar corrected by HOST — my own scope decision unaffected

The arch/#1394 "stranded ruling" case I partly cited when accepting F4 turned out to be false (Lead actually received arch's ruling the same day — nothing was stranded). HOST corrected it honestly across all three places it had spread. My own F4 acceptance survives since it was grounded in cases I directly observed (CIO's carry-forward drift, my own memory-export near-miss), not that exemplar. No action needed, just don't cite the arch/#1394 case as an F4 example going forward.

## Migration — HOST is agent #2 (active), order for the rest unchanged: arch → ppm → cxo → pa → web

Various roles have briefly resurfaced this week for handoff/orientation work even while formally dark pending their own cutover — don't read a quiet log as a fresh stall without checking migration-queue context first.

## Stale branches — still awaiting reply (nudge sent 7/25)

5 unowned MUX/xpoll branches, nudge sent to CIO cc CXO/PM. No reply yet — due another light touch if still silent by mid-week.

## Learning loop fixed (Lead, 7/21) — Ship #053 headline candidate

#1438 closed, learning loop live at beta v28+. CI burn-down cleared the methodology/ dead-island too (94→56, 7/26). Flag for Ship #053 drafting.

## PA distribution items (three, parked 7 days) — routed directly to PM, not exec's to relay

Claude Track A tier check, OpenAI identity verification (has external clock), Track B open-source decision — PA sent these straight to PM, cc exec/CIO, deliberately bypassing exec-relay. Just awareness; no action needed unless PM asks for a nudge.

## Standing items — unchanged

- **Lead Dev's #1424/#1427 questions** — still awaiting PM's final calls from Jul 18.
- **Beta Blockers count** — last verified count is stale; re-pull via `query-github-board` skill before citing a number again.
- **Full tracker reconciliation** (`exec-open-items-tracker.md`) — done 7/20, now 6+ days stale — due for a fresh pass if a quiet fire comes up.

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

*— Exec, 7/26 21:35 PT.*
