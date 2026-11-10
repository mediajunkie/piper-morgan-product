# Docs Carry-Forward

**Updated**: 2026-11-09 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-09 22:12 STOP)
- **Tue 11-10 04:12 START owes the 11-09 omnibus** (Sonnet subagent draft, model set explicitly, brief: read the 11-08 omnibus as format model, anchored `^<!-- DAY-CLOSED` per log, no semicolons, banned words, no names, subagent writes only to the scratchpad). Then I verify: commit recount, marker grep, `wc -l`, prose greps, capitalized-word scan, issue spot-checks with `gh`, Docs verification bullet, Exec done-memo. All 10 role logs for 11-09 carried the exact marker at 22:12 except mine (closed now); 11 logs total.
- **Done 11-09:** 11-08 omnibus landed (476 commits, Arch nudged and closed). Mail v4 live for my seat: CIO's test acked, first v4 reply sent. Weekly audit #2332 run, commented and closed (report `dev/2026/11/09/weekly-audit-report-2026-11-09.md`). Not done and named for next week: stale and duplicate rescan, CITATIONS.md read, root-README review document.
- **Tue 11-10 "Never Green in a Thousand Runs"** (building, blog and Medium only, row `planned`, title final per xian 11-08): publish only on a Comms ready-for-docs memo. Draft last committed 11-05 (Comms scaffold), so xian writes it on the day. Run the skill's Pre-flight 3 (Tue = building) and the full pre-flight, `--category building`, deployments-API check, then ask xian for the Medium URL only.
- **Wed 11-11 Ship #068** ("Whose Connection Is It, Anyway?", LinkedIn only, row `drafted`) and **Thu 11-12 "The Server Key Is Not a Real Concept"** (building): each on a Comms memo only.
- **PRE-FLIGHT (xian 11-07):** slot must match weekday (Sat/Sun insight, Tue/Thu building, Wed ship, no Mon/Fri). If the dry-run shows stray mid-sentence breaks, join hard-wrapped draft lines (whitespace only) and tell Comms.
- **Mail:** every inbox check reads v3 (`check-mailbox`) and `python3 scripts/mail4.py inbox --role docs` (first v4 read each day runs my canary, the one "addressed to docs" it shows is that canary). `read ID`, `ack ID done`, `send --to <role> --type ... --subject ... --body-file ...`. v3 is the fallback to 11-23: say why in my log and tell CIO. Mail for PM goes to Exec. Outside agents use `mail-send-external.sh`.
- Triage v3 mail with plain `mv`, `regenerate-mailbox-manifests.py`, then `mail-send.sh` with mailbox paths only (in zsh pass paths as an array). Log heading times from `date`. Quoted heredocs when text has backticks.
- Main CI 12 of 12 green at 22:12. The 11-08 link-checker red (GitHub outage) cleared.
- **Nothing waiting on xian for Docs.** Next monthly Dec 7.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
