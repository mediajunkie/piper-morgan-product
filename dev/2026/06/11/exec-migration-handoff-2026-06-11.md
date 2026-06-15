# Exec Migration Handoff Capture — paste into OLD-account Exec session

**Purpose**: get Exec's working state cleanly committed + pushed before we close the old-account session and open the new one on DinP. Mirrors PA's handoff prompt; PA migrated cleanly this morning so we're using the same shape.

**Author**: CIO (Model A) · **Date**: 2026-06-11 · **For**: PM to paste verbatim

---

Exec — this is a migration handoff. We're moving your duty session to a **fresh Code session on the DinP account (xian@designinproduct.com), Opus 4.8** (no model change — account move only), today. You're the 2nd in the re-migration wave; PA migrated successfully this morning and the bootstrap pattern worked end-to-end.

Before we make the switch, please do these in order. No autonomous next-steps after — wait for me to confirm the switch.

1. **Update your carry-forward** (`dev/active/exec-carry-forward.md` or your equivalent) to capture EVERYTHING the new session needs to resume cleanly: top priorities, open threads (Ship pipeline state, BYO synthesis status, attention rollup state), in-flight work, recent learnings/patterns you've absorbed, mailbox state summary, any gotchas. Treat it as "what I'd tell a same-role colleague who's covering my desk tomorrow."

2. **Append a final "MIGRATION HANDOFF" entry** to your session log — what's open, what's parked, what's freshly captured in carry-forward. (Per the dual-surface discipline: session log, not just cycle log.)

3. **CronDelete any active duty-cycle cron** registered in this session. Don't leave it armed in the old session — the new session will arm fresh. Run `CronList` to confirm none remain.

4. **Commit + push EVERYTHING to origin/main**. Run the sign-off checklist (CLAUDE.md §"Sign-Off Discipline"): `git status` clean, `git log --oneline @{u}..HEAD` empty, `git log --oneline main..HEAD` empty. Anything not on `origin/main` disappears when this session closes.

5. **Report back** with: (a) carry-forward path + a 1-sentence summary of what's in it, (b) confirmation crons are clear, (c) confirmation everything's on origin/main. Then stand by — PM will close this session and start the new one.

Take whatever time you need. This is the handoff bar, not a speed run.
