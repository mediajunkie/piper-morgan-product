# Docs Carry-Forward

**Updated**: 2026-11-10 22:13 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-10 22:13 STOP)
- **Wed 11-11 04:12 START owes the 11-10 omnibus** (Sonnet subagent draft, model set explicitly, brief: read the 11-09 omnibus as format model, anchored `^<!-- DAY-CLOSED` per log, no semicolons, banned words, no names, subagent writes only to the scratchpad). Then verify: commit recount, marker grep, `wc -l`, prose greps, capitalized-word scan, issue spot-checks with `gh`, Docs verification bullet, Exec done-memo. All 10 other 11-10 logs carry the exact marker at 22:13; mine closes now.
- **Done 11-10:** 11-09 omnibus landed 04:18 (228 commits). Fly deploy red at 19:03 reported and confirmed transient (Lead 19:20). No publish: Tue post never got a Comms ready-for-docs memo (row still `planned`).
- **Tue 11-10 "Never Green in a Thousand Runs"** (building, row `planned`) PUBLISHED 23:31 11-10 (Comms memo 23:27). Medium leg DONE 23:3x (distributed, draft archived). Thu post: slug must follow the new title "The Server Has No Key" (draft file still has the old slug). Wed 11-11 Ship #068 (LinkedIn only, row `drafted`) and Thu 11-12 "The Server Has No Key" (building) each on a Comms memo only.
- **PRE-FLIGHT (xian 11-07):** slot must match weekday (Sat/Sun insight, Tue/Thu building, Wed ship, no Mon/Fri). If the dry-run shows stray mid-sentence breaks, join hard-wrapped draft lines (whitespace only) and tell Comms.
- **Mail:** every inbox check reads v3 (`check-mailbox`) and `python3 scripts/mail4.py inbox --role docs` (first v4 read each day runs my canary, the one "addressed to docs" it shows is that canary). `read ID`, `ack ID done`, `send --to <role> --type ... --subject ... --body-file ...`. v3 is the fallback to 11-23: say why in my log and tell CIO. Mail for PM goes to Exec. Outside agents use `mail-send-external.sh`.
- Triage v3 mail with plain `mv`, `regenerate-mailbox-manifests.py`, then `mail-send.sh` with mailbox paths only (in zsh pass paths as an array). Log heading times from `date`. Quoted heredocs when text has backticks.
- Main CI 12 of 12 green at 22:12. The 11-08 link-checker red (GitHub outage) cleared.
- **Nothing waiting on xian for Docs.** Next monthly Dec 7.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
