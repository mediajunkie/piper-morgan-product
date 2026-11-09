# Docs Carry-Forward

**Updated**: 2026-11-08 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-08 22:12 STOP)
- **Mon 11-09 04:12 START owes the 11-08 omnibus** (Sonnet subagent draft, model set explicitly, then I verify: commit recount, anchored `^<!-- DAY-CLOSED` lines, prose-rule greps, capitalized-word scan, Docs verification bullet, Exec done-memo). Exact marker only.
- **Done 11-08:** 11-07 omnibus landed. "When Accuracy Scores Worse" PUBLISHED 22:13 (site e4459f8926, deployments API success), row `published`, draft archived.
- **Owed from xian:** the Medium URL for "When Accuracy Scores Worse" (LinkedIn URL recorded 11-08). On receipt set `mediumURL`, `linkedinURL`, status `distributed`, `canonicalSite` distributed (`liPubDate` only if he gives a date). Ask once at the next START if still absent.
- **PRE-FLIGHT (xian 11-07):** slot must match weekday (Sat/Sun insight, Tue/Thu building, Wed ship, no Mon/Fri). Run publish-to-blog Pre-flight 3. Never take a category from a memo alone. If the dry-run shows stray mid-sentence breaks, join hard-wrapped lines in the draft (whitespace only) and tell Comms.
- **Mon 11-09: mail v4 opens to my seat** (CIO sends a test message). `python3 scripts/mail4.py inbox --role docs`, `read ID`, `ack ID done`, `send --to <role> --type ... --subject ... --body-file ...`. v3 is the fallback to 11-23: say why in my log and tell CIO. Mail for PM goes to Exec. Outside agents use `mail-send-external.sh`.
- **Mon 11-09: weekly audit.** Next monthly Dec 7.
- **Tue 11-10 "Never Green in a Thousand Runs"** (title confirmed final by xian 11-08, drop WORKING TITLE if Comms has not), **Wed 11-11 Ship #068** ("Whose Connection Is It, Anyway?", LinkedIn only), **Thu 11-12 "The Server Key Is Not a Real Concept"**: each on a Comms memo only.
- **Link checker:** red 11-08 evening from a GitHub host outage (504s), owned by CIO and Lead. Watch it at START, no ceiling edits.
- Triage mail with plain `mv`, `regenerate-mailbox-manifests.py`, then `mail-send.sh` with mailbox paths only (in zsh pass paths as an array). Log heading times from `date`. Quoted heredocs when text has backticks.
- Main CI 11 of 12 at 22:12 (link checker, outage).

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
