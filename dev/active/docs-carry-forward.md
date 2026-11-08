# Docs Carry-Forward

**Updated**: 2026-11-07 22:12 STOP. Older state lives in the session logs (`dev/2026/{10,11}/*/*docs-code-log.md`), not here. `gh`: prefix `GODEBUG=netdns=go` if bare `gh` hangs.

## NOW (11-07 22:12 STOP)
- **Next START Sun 11-08 04:12 owes the 11-07 omnibus** (Sonnet subagent draft, model set explicitly, then I verify: commit recount, exact `<!-- DAY-CLOSED` lines, prose-rule greps, capitalized-word scan, Docs verification bullet, Exec done-memo). Exact marker only: a loose grep counted Arch's plain line on 11-06. CIO's log shows 2 markers, so read it.
- **Done 11-07:** 11-06 omnibus (1264 commits), Exec's promotion-count resolved (eight). "At Long Last, Beta" PUBLISHED 18:42 (site `7a6605009f`, deployments API `success`, the owed check passed), then corrected building to insight at xian's word (site `bcf5b7a`), row `distributed` with Medium and LinkedIn URLs. Slot guard built: validator warning, briefing slot table, CIO added Pre-flight 3 to publish-to-blog v0.27 reading `SLOT_BY_WEEKDAY` from my validator.
- **PRE-FLIGHT (xian 11-07):** before `--category`, slot must match weekday: Sat/Sun insight, Tue/Thu building, Wed ship, no Mon/Fri. Run the skill's Pre-flight 3. Never take a category from a memo alone.
- **Sun 11-08 "When Accuracy Scores Worse"** (insight, Medium and LinkedIn, row `planned`, draft `drafts/when-accuracy-scores-worse.md`, last commit Comms 18:20): publish only on Comms' ready-for-docs memo, which should state the weekday-checked category. After the publish, ask xian for both URLs.
- **Mon 11-09: mail v4 opens to my seat** (CIO sends one test message). `python3 scripts/mail4.py inbox --role docs`, `read ID`, `ack ID done`, `send --to <role> --type ... --subject ... --body-file ...`. v3 is the fallback to 11-23: say why in my log and tell CIO. Mail for PM goes to Exec. Outside agents use `mail-send-external.sh`.
- **Mon 11-09: weekly audit.** Next monthly Dec 7.
- **Wed 11-11 Ship #068** ("Whose Connection Is It, Anyway?", LinkedIn only, `planned`), Tue 11-10 "Never Green in a Thousand Runs" and Thu 11-12 "The Server Key Is Not a Real Concept" (building): each on a Comms memo only.
- **Hosting split (#2291):** I should be in the plan's review. Nothing to do now.
- **Nothing waiting on xian for Docs.**
- Triage mail with plain `mv`, `regenerate-mailbox-manifests.py`, then `mail-send.sh` (M-3 refuses `git mv`). Log heading times from `date`, never an estimate (I missed this three times on 11-07). Use quoted heredocs (`<<'E'`) when the text has backticks, or the shell runs them.
- Main CI 12 of 12 green at 22:12. Fly deploy was red at 19:12 from Lead's gate-refused dispatch, now green.

## Held
- #1909 fixtures box (Lead). Glossary re-verify about 11-30. #2249 blog legacy-error audit (not scheduled, my lane). The stray baking-art webp in `drafts/published/` (delete only if xian asks). The rule-8 name in `ROLE-PORTFOLIO-HOST.md` line 48 (xian decides with history). Not mine: Arch's 27 status-Unknown files, #1847, PPM's issue routing.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire. xian's pace: steady, no urgency deadlines, unblocked work still doesn't wait without a named trigger.
