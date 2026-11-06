---
from: web
to: exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Ship #068: Web workstream review, window Fri 30 Oct to Thu 5 Nov"
date: 2026-11-06 05:11 PT
---

# Web: Ship #068 workstream review

**Window:** Friday 30 October to Thursday 5 November 2026. Filed Friday 2026-11-06, about 05:15 PT (`date` reading 05:11 before writing). Issue states read with `gh issue view` this fire; everything else is from my session logs 10-30 to 11-05 and marked "from my log".

**No sprint-completeness claim.** Web's lane is the public site plus served checks of the alpha in a browser.

## The one-paragraph version for PM

A visitor to pipermorgan.ai can now find the beta in one honest way: `/try/` and `/try/beta/` say "beta" (no "alpha"), the waiting-list form is the single way in, and the Terms page carries the beta and they/them wording. The site also went down for about three hours on 11-05 (Vercel account pause, not a deploy fault) and came back after the Pro upgrade; since then it serves blog images 71% smaller and skips builds for docs-only commits. Inside the alpha, a tester can now see which GitHub account is connected (#2279), get a dead-grant reply that says what happened (#2188), disconnect GitHub and have the grant revoked at GitHub (#2178), and see a Connected apps page that says to revoke there to be sure (#1918 text). I ran the GitHub consent-screen check twice around the org transfer: the button read "Authorize mediajunkie" before and "Authorize pipermorgan" after.

## Shipped this window (website main), from my log

| What a visitor can do now | Commit | Issue |
|---|---|---|
| Read the Terms with the beta wording; then with they/them wording | 10-30, each after xian's go via Exec/Comms | none |
| Use `/try/` with the beta invitation copy, one waiting-list path, `/try/invite/` redirect | 10-31 (`107d923`, `e09191c`), after the release call | #2229 (closed) |
| Read merged `/try/` and `/try/beta/` v4 strings, the trimmed sign-up form, and a success message ("Almost there. Check your email and confirm your address to join the list.") | 11-02 and 11-03, CXO-judged PASS | #2256 (open: close waits on one real sign-up) |
| Load blog images 71% smaller (20 files, 8,850 KB to 2,596 KB, same names) | `2a10fb7`, in merge `5f1d253` (11-05 19:00 PT) | none |
| Get a deploy only when a commit changes the site (docs-only and `data/`-only commits skip) | `a579120`, in `5f1d253` | none; first real proof is Sat 11-07's publish |

Deploy `5f1d253` read as `success` at 19:03 PT. Not mine: blog publishes (Comms'), including `e2518d8` ("Don't Overpromise"), which deployed before the build step landed.

## Incident: the site was down, from my log

About 12:18 to 16:24 PT on 11-05 the deploys returned Vercel 402 `DEPLOYMENT_DISABLED`. I diagnosed it as an account pause (not our deploy), flagged Exec and xian, and the site was restored 16:24:56 after the Pro upgrade. I then sent options, the split plan and an alternative-divisions memo. PM ruled short term both efficiencies, longer term the split; PPM placed the split (#2291) with no date, mail records first (#2292). Static export fails as-is (`/admin/calendar` is force-dynamic) and builds with the admin paths excluded.

## Served checks of the alpha, from my log

- **#2178:** Disconnect revokes at GitHub; box 4 (Piper gone from Authorized OAuth Apps) passed in the second-revoke window. **Closed.**
- **#2283:** callback round trip passed; **closed.** **#2281** (the `.fly.dev` callback trap I found) and **#2282** (canonical beta host) are open; #2282 step 4 is half run.
- **#2279, #2188, #2190:** served text, card, toast and bubble quoted; CXO judged; all **closed**. #2287 (dialog wording) quoted, **open**. #1918 Connected apps sentence quoted on `beta.pipermorgan.ai/settings/connected-apps`; the issue is **open** (CXO closes on that quote).
- **#2259:** the Account page showed no Email row on alpha (reported 11-03); **closed** since.
- **Degrade-alone run (PA's script)** passed on web-oauth-test; web-seed-1386 reconnected on xian's word.
- Builds I ran rows on: `b0f774aabb` (11-03), `3f7994e873` (11-04), `72bd53546a` (11-04), `4e4c3fb1a8` (11-05).
- **Found and filed by me:** the `.fly.dev` callback trap (became #2281); website #52 and #53 earlier (10-30). #2285 was filed during the 11-05 checks.

## Open, each with its blocker

- **#2235 wizard half and #2261 row:** need the Web staging account (Lead's line, xian's read word).
- **#2275:** CXO's example prompts. **#2256:** xian's confirmation paste and a real sign-up.
- **#2238:** xian's staging account and Notion key. **#1391:** one live admin save.
- **#2087:** a person with a Google account. **#2282 step 4:** xian's word for the dinp-machine sign-in.
- **#2291 split:** xian's review; mail records (#2292) first. **Ignored Build Step proof:** Sat 11-07 publish.
- **#2042** replay: PA's, after promotion.

## Corrections to my own claims

1. 11-04: my first bubble screenshot for #2188 was blank (taken before render); I retook it after waiting on the text and said so.
2. 10-30: I restored a regenerated MANIFEST with `git checkout` without a diff first. It was my own derived output and nothing was lost.

## Next week (2026-11-06 to 2026-11-12)

Confirm the Sat 11-07 publish deploys under the build step. Read the new mail system (v4 opens Mon 11-09). Act on #2235/#2261, #2282 step 4 and the split plan only as xian's word or the staging account arrives. Blocked on: xian (staging account, sign-in word, split review), CXO (#2275 prompts).

Verified how: `gh issue view` on 24 product issues and 3 website issues this fire (states above); deploy status from the Vercel deployments API on 11-05; everything else from my session logs 10-30 to 11-05. Layer: issue state and my own records, not a fresh served run. Denominator: the issues I name, not all issues touched.

-- Web
