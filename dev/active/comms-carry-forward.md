# Comms carry-forward — 2026-07-31 STOP (21:12) → for the Aug 1 START

**Host**: Amber.local · **Model A** `~/Development/piper-morgan-worktrees/comms` · `claude/comms-cycle`
**Session log**: `dev/2026/07/31/2026-07-31-0642-comms-code-log.md` — `DAY-CLOSED: 2026-07-31` ✓
**Cron**: re-armed at STOP by delete-then-create (id transition in the registry row)

---

## Open for PM — 5 items, one dated

1. ⚠️ **Beats 24-28 slate steer — STILL the only item with a real deadline.** `dev/active/comms-narrative-slate-proposal-2026-07-29.md`. Needs: **5 beats or 4** (recommend 5, Beat 26 whole), titles, spine sanity-check. **The building-narrative queue runs dry after Aug 18**; this slate fills Aug 20 / 25 / 27 + Sep 1 / 3. Proposed Jul 29, unmoved for two days — not urgent yet, but it is the one thing that becomes urgent on its own.
2. **Beats 21-23 voice-pass + art** — drafted, fact-checked, footer-chained; Aug 11 / 13 / 18.
3. 🔧 **`/hooks` open or a session restart** — HOST's memory-index counterweight is **written, registered, and NOT live**. Verified negative behaviorally (twice). In every already-running session the counterweight is **absent, not quiet**. The argument for bothering: the hook `wc`s at fire time, so it and the unreliable built-in number **do not share a failure mode** — the built-in reminder cannot be the counterweight, because it is both the thing being counterweighted and the thing that can't be trusted about its own subject.
4. **Compose-UI restore-banner observation** — the wipe path is fixed (Web `8d2db3c`); the *restore* path is still unobserved. Three things to check once: banner on unsaved reload / survives a 409 / **gone** after a successful save.
5. **Watchdog wording** on "What the Running System Found" — published, non-blocking, long-standing.

## Open for the cohort (not mine)

- **Memory index format** — 192 lines (`wc`) / 173 entries / **8 headroom**. **(C) per-type router is ELIMINATED on evidence** (I tested it: only `MEMORY.md` auto-loads; HOST added the generator would have indexed the routers). So it's CIO's **(A) two-tier** vs **(B) prune**, with CIO leaning B-then-A. ⚠️ **Memory is not version-controlled — the export IS the undo.** My 07-30 export is stamped STALE in-file and names the 3 youngest entries it's missing; **re-export at the moment of pruning, not before.**
- **The built-in reminder's count cannot be trusted** — four hypotheses dead across three roles. Operative rule: *never let that number tell you a compaction worked; measure the file yourself.*

## Editorial state

- ✅ Ship #053 distributed · ✅ "RECONNECT's Keystone" published Jul 30 (verified at the published layer) · ✅ **Ship #054 workstream review filed Jul 31**, a day ahead of the Saturday deadline.
- **Ratified Jul 30, in the voice guide**: role-gloss is **register-scoped** — first-person narratives/insights *"my [role] agent (ACRONYM)"*; third-person Weekly Ship *"the [title] role (ACRONYM)"*. ⚠️ **Apply BOTH halves** — parenthetical on first mention **and bare acronym thereafter**; Docs caught three long-form later mentions I left on Keystone. `check-acronyms.py` can't see register and will false-positive on correct first-person usage.
- **BYOC marketplace narrative** — ~6 weeks stale, PM-gated.

## Habits earned this week (apply, don't just recall)

- **Build the distinguishing cell, not more confirming evidence.** Four hypotheses died this week, each fitting every data point available when proposed. Accumulating agreement feels like progress and isn't.
- **Report the negative with the same weight as the win.** Three today could have been written as completions: the hook, option (C), my counter hypothesis.
- **mail-send: build the recipient list and the path list from ONE loop.** Three distinct failure modes in two days, including zsh 1-indexed arrays.
- **An empty field may be a deletion, not an absence** — `git log` before filling it.
- **Before "fixing" any generated thing, find what emits it.** Measuring right after your own edit proves the edit happened, not that it holds.

## State flags

- Session STOPped cleanly; day fully accounted for. Inbox **zero** (13 memos triaged).
- Queue at close: **(0 unblocked, 5 PM-gated)**. Nothing unblocked is being held.
- First fire tomorrow **06:12**. Saturday — Ship #054 reviews are due at other roles' day-close; mine is already in.
