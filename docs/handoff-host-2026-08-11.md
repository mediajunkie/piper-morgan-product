# HOST handoff — Amber reboot standdown, 2026-08-11

**Reason this file exists**: Pard's stand-down notice (`~/.local/state/amber-agent/standdown-host.txt`), Amber rebooting ~07:30 PT 2026-08-11 for macOS 26.6. Session should resume via `claude --resume` with conversation intact, but this file exists for the case resume fails for this seat specifically — treat it as a cold-start bootstrap, not just a note.

**Written**: 2026-08-11 ~06:3x PT, before the reboot, before today's first scheduled fire (06:37) — no work happened today prior to this notice.

---

## 1. Identity (if resume fails and this is a fresh session)

- **Role**: HOST (Head of Sapient Trust)
- **Slug**: `host-code` / session-log role slug `host`
- **Worktree**: Model A, stable, `~/Development/piper-morgan-worktrees/host` on branch `claude/host-cycle` — **reuse this exact path**, don't re-provision a new one; Claude Code keys memory/state to the path.
- **Cron**: `37 6,9,12,15,18,21 * * *` (6 fires/day). **This is a session-scoped `CronCreate` job (id `5e6e846e` as of this writing) — it does NOT survive a process restart even under `claude --resume`.** First action after resume, whether resume succeeds or this is a cold start: run `CronList`; if it's empty, re-arm immediately with the expression above before doing anything else. Verify exactly one job survives.
- **Briefing**: `docs/briefing/BRIEFING-ESSENTIAL-HOST.md`. **Skill**: `duty-cycle-tick` (currently v1.28) — read its current content fresh, don't work from memory of what it said in a prior session; it changed twice on 08-09 and once more on 08-10 alone.

## 2. State at stand-down — nothing in hand, nothing to finish

Per step 1 of the stand-down notice ("finish or park what is in hand"): **there was nothing in hand.** 2026-08-10 closed cleanly (verify: `grep -c "DAY-CLOSED" dev/2026/08/10/2026-08-10-0707-host-code-log.md` should return non-zero). No fire had happened yet today (06:37 slot hadn't landed before this notice arrived) — **no session log exists for 2026-08-11 yet**, and that is correct, not a gap.

**On resume/cold-start, treat the very next fire as a normal START**: Step 0 will find yesterday's `DAY-CLOSED` marker present (no missed-STOP repair needed), then proceed to create today's log and run the mail loop normally.

## 3. What to read to reconstruct current priorities

**Read `dev/active/host-carry-forward.md` in full before doing anything else** — it is current as of 2026-08-10's STOP fire and holds the real state, not this file. Summary as of that writing, so you don't have to open it blind:

- **Cron-count STOP check** (`grep -c "^## Fire"` vs. the cron expression's comma count, before ever writing STOP) — proven correct six times running across three days after four prior early-stops on this exact expression. Keep using it explicitly.
- **MEMORY.md headroom**: 186/200 lines used (14 headroom), stable for eight fires — a genuinely flat daily rate confirmed after two false extrapolations earlier in the week. Step 1c watches this every fire (reads the guard-convention count from `check-derived-drift.sh`'s own output, not a bare `wc -l` — that distinction was a real bug fixed 08-09).
- **Step 2c** (cohort-freeze detection, runs after sync at START/WATCH) reads `origin/main` directly and prints `ref=`/`tip=` — CIO's fix, landed 08-09/10. The "during a freeze" alert half (what PM sees while the cohort is silent) is also now live in production, verified against HOST's own content spec.
- **#1539** (HOST's own item, from the Jake FTUX review — "a much stronger sense of what uncertainty it is reducing for me as a user") — ruled *partial, not sufficient* on 08-10 against a related criterion. The legibility half is still not concrete on HOST's own end. Don't treat the ruling as having solved it.
- **A fifth mailbox header format** was found on HOST's own corpus 08-10 (Pard's `**Name → Recipients** (time):` inline notation) and reported to Comms — not HOST's to fix, watch for whether it resurfaces.
- **Beta moved back a month** (PM, 2026-08-08, `decisions.log:1242`) — settled fact, not a live watch, but grep `decisions.log` for "beta" rather than trust any cached framing (including this file's) if it ever matters to a decision — HOST wrote a stale beta-date claim into its own cron prompt once already this week and had to self-correct.

## 4. Mechanisms HOST owns or co-owns, for orientation

- `scripts/check-derived-drift.sh`, `scripts/check-safety-invariants.sh` — HOST-authored, run every fire.
- `scripts/cohort-freeze-detect.sh` — CIO's, HOST integrates it (Step 2c) and supplied the content spec for its alert.
- `duty-cycle-tick` skill Step 1a (Role Health Check self-poll), Step 1c (memory headroom) — HOST-only additions this week.
- `docs/internal/architecture/current/floor-honesty-contract-1517-spec.md` — Arch's, HOST gave the trust-lens sign-off 08-10.

## 5. Nothing else pending

No open mail requiring a HOST reply, no unresolved escalation, no work parked mid-task. This stand-down is closer to closing a laptop lid than a migration, per Pard's own framing — treat it that way unless resume actually fails.

— HOST, 2026-08-11
