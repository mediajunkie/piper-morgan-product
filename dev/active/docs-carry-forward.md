# Docs Carry-Forward

**Updated**: 2026-10-17 (04:12 fire, see NOW below; older DONE lines below are history). DONE 10-12: 10-10 + 10-11 omnibuses, Weekly Audit #1994 closed, BRIEFING-CURRENT-STATE refreshed, How to Report edit pushed (xian approved), Ship #064 row set by Comms and view rebuilt. Known fault: bare `gh` hung on Amber after the 10-10 reboot (Pard); prefix `GODEBUG=netdns=go` until Pard confirms the fix. History in session logs (`dev/2026/10/{04..12}/*docs-code-log.md`), not here.

## NOW (10-27 04:19 fire)
- **PUBLISHED**: every post through "A Clean Result Needs a Version Number" (10-25, website 5706b37, row `published`). **DISTRIBUTED**: through "Mistaking the Inset for the Map" (10-24). Omnibuses 10-15 through 10-24 DONE.
- Clean Result DISTRIBUTED 10-25 (URLs from xian, liPubDate my assumption). Nothing owed from xian.
- Tue 10-27 DONE: 10-26 omnibus, "The Caveat That Kept Disappearing" published (website c1e2538, row `published`). OWED from xian: Medium URL only (building). Then set mediumURL, canonicalSite=distributed, status=distributed, validate, rebuild view. Next START Wed 10-28 owes the 10-27 omnibus. Weekly Ship #066 row is `planned` pubDate 10-28 (Comms/xian own it, publish only on a ready-for-docs memo). Citation via Hearsay (building, pubDate Thu 10-29) is `drafted`. Next weekly audit Mon 11-02 (also monthly housekeeping).
- Rule 8: xian ruled 10-25 14:09 the corpus-row person is a client, Lead swapped it (566ab3db1c, 0 of 18 outside dev/ per Lead). Open: dev/ logs and history (xian), company name (Exec asked xian). HOST 10-20 log outside first name (reported).
- Held: #1909 fixtures box (Lead after 10-30), glossary re-verify about 11-30. CIO concept-link inventory for my files: nothing owed (checked 10-26).

## OWED (PM's hand)
- Nothing for "It Doesn't Count if You Skip It": FULLY DISTRIBUTED 10-11 (LinkedIn + Medium URLs from PM, row `distributed`, `canonicalSite` `distributed`).
- `published` with an empty pubDate: "15 Sessions, Fast Recovery" (outside Step 1f's window, age unverified).

## Unclosed logs / awaiting
- HOST 10-09 log: no DAY-CLOSED (nudge sent). Spec's 10-08 log unclosed, no Spec 10-09 log, seat looks dormant. Re-check at the next START (Step 1d).
- Roadmap v19.0 fold LANDED (`aca130a366`). I re-audited it and **closed #1644** (05:3x). Reply to PPM filed (`114a882b5`). Enterprise milestone date (GitHub 2028-10-30 vs decisions.log 2027-10-30) is PM's via Exec, PPM routed it, nothing owed from Docs. Exec (cc, read 05:4x) will relay PM's 2027/2028 answer to PPM and Docs; no Docs edit unless asked.

## NEXT (named triggers)
- **Giving It Away**: PUBLISHED 10-13 (website `d1f39f2`). Medium crosspost DONE 10-13 (row `distributed`).
- **10-12 omnibus**: drafted by a Sonnet subagent 10-13, commit plus activity rows pending in the 04:12 fire log. Exec and CIO 10-12 logs unclosed (nudged).
- **Ship #064**: PUBLISHED 10-14 (website `6bca437`). LinkedIn crosspost DONE 10-14 (row `distributed`).
- **10-13 omnibus**: drafted by a Sonnet subagent 10-14, commit plus activity rows pending. Exec and Comms 10-13 logs unclosed (nudged).
- **Overzealous Cleanup Routine**: PUBLISHED 10-15 (website commit pushed, live 200). Medium crosspost DONE 10-15 (row `distributed`).
- **10-14 and 10-15 omnibuses**: DONE (10-15: 527 lines, 35 logs, 1091 commits, 11 rows). No addendum owed. All role logs closed. **Timestamps**: take every log heading time from a `date` call (10-15 estimates were corrected).
- ~~Sat 10-17 04:12 fire: PUBLISH~~ DONE. "Convergent Claims Aren't Independent Evidence" (`ready-for-docs`, pre-flight and dry-run done 10-15). `--draft docs/public/comms/drafts/convergent-claims-arent-independent-evidence.md --image .../convergent-claims-arent-independent-evidence-four-telescopes-all-still-capped.jpg --slug convergent-claims-arent-independent-evidence --category insight --work-date 2026-09-20`. Re-fetch first. Then archive, row `published`, Medium+LinkedIn reminder to Exec.
- **Mon 10-19**: next weekly audit. **~11-30**: glossary 60-day re-verify.

## Held
- **#1909**: one box left, the test-fixtures review, owner Lead after MVP closes 10-30. Hooks box ticked 10-16 on CIO's report (12 of 15 working). The two stray `dev/active` files were removed by Exec on main (xian's direct word).

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire.
