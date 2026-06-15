# PA Migration Handoff Capture — paste into OLD-account PA session

**Purpose**: get PA's working state cleanly committed + pushed before we close the old-account session and open the new one on DinP / Sonnet 4.6.

**Author**: CIO (Model A) · **Date**: 2026-06-10 · **For**: PM to paste verbatim

---

PA — this is a migration handoff. We're moving your duty session to a **fresh Code session on the DinP account (xian@designinproduct.com), Sonnet 4.6**, today. You're the pioneer for the re-migration wave; CIO will draft an analogous handoff for the next agent once we confirm yours lands clean.

Before we make the switch, please do these in order. No autonomous next-steps after — wait for me to confirm the switch.

1. **Update your carry-forward** (`dev/active/pa-carry-forward.md`) to capture EVERYTHING the new session needs to resume cleanly: top priorities, open threads, in-flight work, recent learnings/patterns you've absorbed, mailbox state summary, any gotchas the new session would otherwise rediscover the hard way. Treat it as "what I'd tell a same-role colleague who's covering my desk tomorrow."

2. **Append a final "MIGRATION HANDOFF" entry** to your session log — what's open, what's parked, what's freshly captured in carry-forward.

3. **CronDelete any active duty-cycle cron** registered in this session. Don't leave it armed in the old session — the new session will arm fresh. Run `CronList` to confirm none remain.

4. **Commit + push EVERYTHING to origin/main**. Run the sign-off checklist (CLAUDE.md §"Sign-Off Discipline"): `git status` clean, `git log --oneline @{u}..HEAD` empty, `git log --oneline main..HEAD` empty. Anything not on `origin/main` disappears when this session closes.

5. **Report back** with: (a) carry-forward path + a 1-sentence summary of what's in it, (b) confirmation crons are clear, (c) confirmation everything's on origin/main. Then stand by — I'll close this session and start the new one.

Take whatever time you need. This is the handoff bar, not a speed run.
