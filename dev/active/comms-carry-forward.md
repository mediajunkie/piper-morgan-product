# Comms carry-forward — 2026-07-30 STOP (21:12) → for the Jul 31 START

**Host**: Amber.local · **Model A** `~/Development/piper-morgan-worktrees/comms` · `claude/comms-cycle`
**Session log**: `dev/2026/07/30/2026-07-30-0642-comms-code-log.md` — `DAY-CLOSED: 2026-07-30` ✓
**Cron**: re-armed at STOP by delete-then-create (see registry row for the id transition)

---

## Open for PM — 4 items, one with a date behind it

1. ⚠️ **Beats 24-28 slate steer** — the only item with a real deadline. Proposal at `dev/active/comms-narrative-slate-proposal-2026-07-29.md`. Needs: **5 beats or 4** (I recommend 5, Beat 26 kept whole), titles, and a sanity check on the spine. **The building-narrative queue still runs dry after Aug 18**; this slate fills Aug 20 / 25 / 27 + Sep 1 / 3. PM said calendar planning resumes after the Keystone handoff — that handoff is done and the post is published.
2. **Beats 21-23 voice-pass + art** — drafted, fact-checked, footer-chained, calendared Aug 11 / 13 / 18.
3. **Compose-UI restore-banner observation** — the *wipe* path is fixed (Web, `8d2db3c`). The **restore** banner is still unobserved: type an edit and reload without saving (expect an explicit Restore/Discard banner with a timestamp), confirm it survives a rejected save, confirm it's **gone** after a save succeeds.
4. **Watchdog wording** on "What the Running System Found" — published, non-blocking, long-standing.

## Open for the cohort (not mine to decide)

- **Memory index format** — 192 lines / 173 entries / **8 headroom, ~6 days**. CIO offers (A) two-tier, (B) prune, leaning B-then-A; I re-raised **(C) per-type indexes behind a router**, which loses no description and deletes nothing. ⚠️ **All three are downstream of one untested question: does the platform load only `MEMORY.md`, or will it follow a pointer to per-type files?** Cheap to test, and it should precede the format choice. Decision sits with CIO/HOST/PM.
- **The guard gap I found**: `rebuild-memory-index.py` refuses loudly past the limit; a **direct edit of `MEMORY.md` succeeds silently** (HOST + PA tested), and the platform reminder says *"compact this file"* — pointing at the unguarded path.
- **HOST's counter defect**, which I think warrants its own escalation: the reminder's reported line count went **down** (187→186) while the file **grew** (201→208). Decoupled, not lagging. A complying agent would read a decrease as *"it's working"* and cut deeper.

## Editorial state

- ✅ **Weekly Ship #053** — distributed. ✅ **"RECONNECT's Keystone"** — published 2026-07-30, verified at the published layer (`called fundamental`, PM's restored alt text, name removed, heading typo fixed, all live).
- **Ratified 2026-07-30, now in the voice guide**: role-gloss is **register-scoped** — first-person narratives/insights use *"my [role] agent (ACRONYM)"*; the third-person Weekly Ship uses *"the [title] role (ACRONYM)"*. The contradicting Jun-23 memory is scoped to match. ⚠️ `check-acronyms.py` can't see register and will keep false-positiving on correct first-person usage.
- **BYOC marketplace narrative** — ~6 weeks stale, PM-gated.

## Habits to carry (earned today)

- **Build the recipient list and the mail-send path list from ONE variable.** Three incomplete-path slips today; the script's warning caught each, which is not the same as having the habit.
- **An empty field may be a deletion, not an absence** — `git log` it before helpfully filling it.
- **Before "fixing" any generated thing, find what emits it.** Measuring right after your own edit proves the edit happened, not that it holds.

## State flags

- Session STOPped cleanly; day fully accounted for. Inbox **zero** (17 memos triaged today).
- Queue at close: **(0 unblocked, 4 PM-gated)**. Nothing unblocked is being held.
- First fire tomorrow **06:12**.
