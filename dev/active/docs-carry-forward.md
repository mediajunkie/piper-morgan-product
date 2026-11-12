# Docs Carry-Forward

**Updated**: 2026-11-11 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-11 22:12)
- **Mail now goes on v4** (`python3 scripts/mail4.py send --to <roles> [--cc ...] --type fyi|task|reply --subject ... --body-file F`), CIO 11-11 22:08: v3 `mail-send.sh` only for PM-through-Exec, Spec, outside agents, or a v4 failure (until 11-23).
- **Ship #068 is `distributed`** (LinkedIn URL from xian 11-11). Main CI 12 of 12 at 22:12 (the 19:12 concept-link red cleared). Next START owes the **11-11 omnibus** (Sonnet subagent, scratchpad, 11-10 omnibus as model, then verify) and Step 1d on 11-11 logs.
- **Ship #068 PUBLISHED 11-11 16:10** (website f4e2914, row `published`, draft archived, done-memo sent, v4 ack done). **LinkedIn leg owed by xian** (Ship is LinkedIn-only): flip row to `distributed` + linkedinURL/liPubDate/canonicalSite when URL arrives. Step 1f resurfaces it each fire.
- Thu 11-12 "The Server Has No Key" row `planned`: needs Comms ready-for-docs memo, slug must follow new title. Keychain ruling (Exec 11:12) noted, Docs unaffected.
- **11-10 omnibus landed 11-11** (185 non-merge commits, 11 of 11 markers, Exec memo sent). Next START owes the 11-11 omnibus (same method: Sonnet subagent, scratchpad only, 11-10 omnibus as format model, then verify).
- **Done 11-10:** 11-09 omnibus landed, Fly red reported (transient), Never Green published 23:31 and distributed (Medium in, draft archived).
- **Tue 11-10 "Never Green in a Thousand Runs"** (building, row `planned`) PUBLISHED 23:31 11-10 (Comms memo 23:27). Medium leg DONE 11-10 (distributed, draft archived). Thu post: slug must follow the new title "The Server Has No Key" (draft file still has the old slug). Wed 11-11 Ship #068 (LinkedIn only, row `drafted`) and Thu 11-12 "The Server Has No Key" (building) each on a Comms memo only.
- **PRE-FLIGHT (xian 11-07):** slot must match weekday (Sat/Sun insight, Tue/Thu building, Wed ship, no Mon/Fri). If the dry-run shows stray mid-sentence breaks, join hard-wrapped draft lines (whitespace only) and tell Comms.
- **Mail:** every inbox check reads v3 (`check-mailbox`) and `python3 scripts/mail4.py inbox --role docs` (first v4 read each day runs my canary, the one "addressed to docs" it shows is that canary). `read ID`, `ack ID done`, `send --to <role> --type ... --subject ... --body-file ...`. v3 is the fallback to 11-23: say why in my log and tell CIO. Mail for PM goes to Exec. Outside agents use `mail-send-external.sh`.
- Triage v3 mail with plain `mv`, `regenerate-mailbox-manifests.py`, then `mail-send.sh` with mailbox paths only (in zsh pass paths as an array). Log heading times from `date`. Quoted heredocs when text has backticks.
- Main CI 12 of 12 green at 22:12. The 11-08 link-checker red (GitHub outage) cleared.
- **Nothing waiting on xian for Docs.** Next monthly Dec 7.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
