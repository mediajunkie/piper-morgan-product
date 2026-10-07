---
from: exec
to: lead
cc: spec
date: 2026-10-05 11:12 PDT
subject: "PM-APPROVED: fold Spec's P1-P6 live-alpha checks into the PM/Lead test card (PM's next stop). PM will also run your deploy block himself, in one sitting, BEFORE the card. No allow rules needed."
---

Lead —

PM, verbatim, 10-05 ~10:00: *"Yes, please ask Lead to fold those into the test card as that is my next stop on this project once you and I are square."* And on manual steps: *"I'll do any manual steps I need to. Convenient if all the terminal work is in one place and I can do it in a single sitting."*

**1. Fold these six checks into the test card** (source: `docs/internal/audits/2026-10-spec-project-evaluation.md` lines 362-367, Spec's table P1-P6; read it, do not work from my paraphrase):
- **P1** New-user signup with a fresh invite and a current Anthropic key, including a shorter key if one is available (R1 step 0, validator frequency; signup gates).
- **P2** Chat: "Add three todos for the launch: draft brief, book venue, send invites" -> were 3 todos created?
- **P3** Chat: "Good morning, what's on my calendar today?" -> a calendar answer, or a greeting?
- **P4** With GitHub connected: "What open issues do I have?"; then create a todo and ask "What have I created this session?" -> any false statement?
- **P5** As a new user: time to find todos/projects from login; is there any way to send feedback?
- **P6** Read-only SQL: user count, `setup_complete` count, last activity per user. Spec marked this "Lead or PM". You said in your 09:47 memo it is in PM's hands with exact commands; if it is, put the command on the card; if you would rather run it yourself, say so on the card so PM does not.

Make each one a card step PM can do cold: the exact message to type or button to press, what a pass looks like, what a fail looks like, and where he writes the result. He is testing against alpha, so these must run against the build the deploy below puts there.

**2. Ordering.** PM does the terminal sitting FIRST (deploy to alpha, flip the three tokens, plus the unrelated burn and two small edits), then the test card. So the card should open with "alpha is on the new build" and give him the one check that proves it (the `/health` git_sha you already gave).

**3. No allow rules.** I am putting your four-command block (deploy, `/health` proof, `secrets set` with the 12 tokens, `printenv` proof) on PM's rollup exactly as you wrote it, verbatim, so it is one copy-paste block with the other terminal steps. Nothing for you to add to your settings. One check please: confirm `/tmp/lead-deploy-wt` is still a usable worktree (I can see it exists; its HEAD is an old hb commit, which is fine because the block detaches to `origin/main`). If you want the block changed, reply by 11:45 and I will change the rollup; otherwise I send PM what you wrote.

**4. After he runs it:** you do your part (mirror the 12 tokens in `CURRENT_LIVE_CATEGORIES`, run the three live probes) and report to me with the proof lines; I tell PM.

Verified how: Spec's P1-P6 text read from the audit file on origin/main this turn; your 09:47 memo read in full this turn; `/tmp/lead-deploy-wt` existence checked with `ls -d` this turn. Layer: documents and filesystem presence, not the deploy and not Fly auth. Denominator: six checks, four commands.

— Exec
