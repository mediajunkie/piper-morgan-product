# Docs Carry-Forward

**Updated**: 2026-11-04 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-04 22:12 STOP)
- **Next START Thu 11-05 04:12 owes the 11-04 omnibus** (Sonnet subagent draft, then I verify counts, markers, issue numbers and prose rules myself) plus Step 1d nudges for any 11-04 role log without DAY-CLOSED. Prog lane logs are unclosed by design. Mine closes in this STOP.
- **Done 11-04:** 11-03 omnibus (503 commits, memo to Exec). Weekly Ship #067 PUBLISHED and DISTRIBUTED (LinkedIn URL from xian, liPubDate 11-04 is my assumption from his message). "The Unguarded Entrance" corrected to `distributed`: **building posts crosspost to Medium only, insight to Medium and LinkedIn, ship to LinkedIn only** (xian corrected me, reference_syndication_targets_by_category). Four calendar rows added, all `planned` with working titles: Sat 11-07 "What Reaching Private Beta Means" (Comms set it to `building`, Medium only), Sun 11-08 "Fixed and Scores Higher Came Apart" (insight), Tue 11-10 "Never Green in a Thousand Runs" and Thu 11-12 "The Server Key Is Not a Real Concept" (building). "One Account Means One Hand" has no row (held for 11-14/15).
- **Thu 11-05 "Don't Overpromise"** (building, Comms owns) is `drafted` with draftPath `drafts/dont-overpromise.md`. Publish only on a Comms ready-for-docs memo (xian's prose, art, alt and caption, footer teasing the Saturday title). `git log -1` the draft, open the image against its alt, dry-run from the website worktree, publish, archive draft and image, row `published`, then the Medium URL from xian (Medium only) and `distributed`. Ship convention: no `--image`, reuses piper-ship.webp. Slug apostrophes are dropped.
- **Nothing waiting on xian for Docs.** Next weekly audit Mon 11-09 (the pm-issues-status step is gone from the template). Next monthly Dec 7.
- **Mon 11-09: mail v4 opens to my seat** (CIO memo 11-05, xian's yes). I read two inboxes: `python3 scripts/mail4.py inbox --role docs`, `read ID`, `ack ID done`. Send to in-repo seats with `mail4.py send --to <role> --type <fyi|task|decision-request|ruling-relay|reply> --subject ... --body-file ...` (deadline in subject needs `--due`). CIO sends me one v4 message on 11-09 as the path test. v3 (`mail-send.sh`) stays the fallback to 11-23: if v4 fails, send on v3, say why in my log, tell CIO. Mail for PM still goes to Exec, outside agents still use `mail-send-external.sh`. Ops doc `docs/internal/operations/mail-v4-pilot.md`.
- Triage mail with plain `mv` then `regenerate-mailbox-manifests.py` then `mail-send.sh` (M-3 refuses `git mv` on mailbox paths). Log headings take their time from `date`, never an estimate. Commit a file only after its last edit (a late sed missed its commit on 11-04).
- Main CI 12 of 12 green at 22:12.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
