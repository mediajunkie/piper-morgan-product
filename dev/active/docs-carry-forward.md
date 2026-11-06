# Docs Carry-Forward

**Updated**: 2026-11-05 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-05 22:12 STOP)
- **Next START Fri 11-06 04:12 owes the 11-05 omnibus** (Sonnet subagent draft, then I verify counts, markers, issue numbers and prose rules myself) plus Step 1d nudges for any 11-05 role log without DAY-CLOSED. Prog lane logs are unclosed by design. Mine closes in this STOP. The 11-05 day includes the Vercel 402 outage (site down between 12:18 and 15:18, back at 16:25 per Web and Exec (not 18:19, that was Comms' fire time)) and the hosting-split plan (#2291).
- **Done 11-05:** 11-04 omnibus (733 commits, memo to Exec). "Don't Overpromise" PUBLISHED and DISTRIBUTED (Medium URL from xian, building = Medium only). Ship #067 LinkedIn was already filled. Main CI 12 of 12 green again after the Documentation Link Checker cleared (the 263-versus-60 red was the outage, I left the ceiling and links alone).
- **Sat 11-07 "At Long Last, Beta"** (building, Comms owns, row `planned`, draftPath `drafts/at-long-last-beta.md`) and **Sun 11-08 "Fixed and Scores Higher Came Apart"** (insight, `planned`), Tue 11-10 "Never Green in a Thousand Runs" and Thu 11-12 "The Server Key Is Not a Real Concept" (building, `planned`): publish each only on a Comms ready-for-docs memo. Steps: `git log -1` the draft, open the image against its alt, dry-run from the website worktree, publish, archive draft and image, row `published`, then the crosspost (building: Medium only, insight: Medium and LinkedIn, ship: LinkedIn only).
- **OWED at the Sat 11-07 publish (Comms' ask, memo 11-05 22:xx):** it is the first publish under Web's Vercel ignore-build step. In my published-memo, confirm that GitHub's deployments API for the website repo shows the publish commit's sha as `success` (as I could see for the 11-05 post). Web's step skips only docs, dev, .github, assets-source, devel, .serena, root data and tests and root md. A post publish changes src/data and public/assets, so it should build. If it does not, tell Web and Comms at once.
- **Mon 11-09: mail v4 opens to my seat** (CIO memo 11-05, xian's yes). I read two inboxes: `python3 scripts/mail4.py inbox --role docs`, `read ID`, `ack ID done`. Send to in-repo seats with `mail4.py send --to <role> --type <fyi|task|decision-request|ruling-relay|reply> --subject ... --body-file ...` (a deadline in the subject needs `--due`). CIO sends me one v4 message on 11-09 as the path test. v3 (`mail-send.sh`) stays the fallback to 11-23: if v4 fails, send on v3, say why in my log, tell CIO. Mail for PM still goes to Exec, outside agents still use `mail-send-external.sh`. Ops doc `docs/internal/operations/mail-v4-pilot.md`.
- **Mon 11-09: weekly audit** (the pm-issues-status step is gone from the template). Next monthly Dec 7.
- **Hosting split (#2291, ongoing, no date):** if it is ever approved it changes my publish step (publish-post.js into the website repo, then a live check) and the calendar's blogURL paths, so I should be in the plan's review. Nothing to do now.
- **Nothing waiting on xian for Docs.**
- Triage mail with plain `mv` then `regenerate-mailbox-manifests.py` then `mail-send.sh` (M-3 refuses `git mv` on mailbox paths). Log headings take their time from `date`, never an estimate. Commit a file only after its last edit. Building posts go to Medium only (I got this wrong once on 11-04).
- Main CI 12 of 12 green at 22:12, site 200.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
