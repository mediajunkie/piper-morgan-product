# Docs Carry-Forward

**Updated**: 2026-10-10 04:35 PDT (04:12 START fire, mid-drain). History of earlier states lives in the session logs (`dev/2026/10/{04..10}/*docs-code-log.md`), not here.

## Done this fire (04:12)
- 10-09 omnibus (`adba285845`, 540 lines, 15 logs, 1128 commits, 574 comparable) + 15 activity rows (`a0906091be`, 2865 to 2880). Nudged HOST (10-09 log lacks DAY-CLOSED, `8e927d29ef`).
- **"No Undo" PUBLISHED** (insight): website `d3246f3`, live at https://pipermorgan.ai/blog/no-undo/ (body phrase "sprint options" + image 200, verified after the deploy lag). Calendar row `published`, blogURL/blogPath set, `canonicalSite` empty, draft + jpg archived, validator 0 errors, 0 of 470 draftPaths unresolvable.
- Notice to Exec that the crosspost is owed (`afdcc5345`).

## OWED (PM's hand)
- **No Undo Medium + LinkedIn crosspost** (insight = both). Medium canonical `https://pipermorgan.ai/blog/no-undo/` (trailing slash). When PM gives URLs: mediumURL, liPubDate, linkedinURL, status `distributed`, `canonicalSite` `distributed` (update-calendar, by header name). Step 1f resurfaces each fire for 7 days.
- Also still `published` and unsyndicated by the Step 1f scan: "15 Sessions, Fast Recovery" (row has an empty pubDate, so Step 1f's 7-day window does not cover it, age unverified).

## Unclosed logs / awaiting
- HOST 10-09 log: no DAY-CLOSED (nudge sent). Spec's 10-08 log unclosed, no Spec 10-09 log, seat looks dormant. Re-check at the next START (Step 1d).
- Roadmap v19.0 fold LANDED (`aca130a366`). I re-audited it and **closed #1644** (05:3x). Reply to PPM filed (`114a882b5`). Enterprise milestone date (GitHub 2028-10-30 vs decisions.log 2027-10-30) is PM's via Exec, PPM routed it, nothing owed from Docs.

## NEXT (named triggers)
- **Sun 10-11 04:12**: "It Doesn't Count if You Skip It" has pubDate 10-11 but is `drafted`, not `ready-for-docs`. Publish only after Comms sets `ready-for-docs` and sends a publish-ready memo. START heartbeat first, full pre-flight (image vs alt, diff draft copies, 16-check audit, dry-run, `--work-date` from the dateline).
- **Mon 10-12**: Weekly Docs Audit. `roadmap.md` flag is CLEAR (fold landed 10-10, audited). Mention only the Enterprise date discrepancy as PM-pending.
- **~11-30**: glossary 60-day re-verify.

## Held on PM (via Exec)
- `git rm` of `dev/active/covapitchdeckv2.pptx` and `dev/active/Treatment`. #1909's two open boxes.

## Seat facts
- LaunchAgent-only (cron `12 4,7,10,13,16,19,22 * * *`), no session cron to re-arm. START opens every fire.
