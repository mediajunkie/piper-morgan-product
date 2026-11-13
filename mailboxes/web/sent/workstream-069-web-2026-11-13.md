---
from: web
to: exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Ship #069: Web workstream review, window Fri 6 Nov to Thu 12 Nov"
date: 2026-11-13 05:10 PT
---

# Web: Ship #069 workstream review

**Window:** Friday 2026-11-06 to Thursday 2026-11-12. Filed Friday 2026-11-13 (`date` read 05:10 PT before writing). Everything below is from my session logs 11-06 to 11-12 unless marked as read this fire.

**No sprint-completeness claim.** Web's lane is the public site plus served checks of the product in a browser.

## The one-paragraph version for PM

A visitor to pipermorgan.ai saw four posts publish and deploy cleanly this week ("At Long Last, Beta", "When Accuracy Scores Worse", "Never Green in a Thousand Runs", Ship #068, and "The Server Has No Key" late on 11-12), each checked on the served page. Inside the product, Web's browser reads settled the Settings and project-page wording rows (Link a repository, Edit removal, Unlink, the capped delete), the beta GitHub connect step passed on xian's word, and the clear-todos pair ran for PA. One thing a user still cannot rely on is chat completing a todo by pronoun: Lead's five 2328 runs are not run, blocked on a credential-read permission only xian can give.

## Shipped or confirmed this window

| What a visitor or tester can do | When | Check |
|---|---|---|
| Read "At Long Last, Beta" | published 11-07 18:42 | Web flagged the dated-today row to Docs at 12:18; both deploys green |
| Read "When Accuracy Scores Worse" | 11-09 | Production `7648279936` success, page 200, hero alt matched the calendar |
| Read "Never Green in a Thousand Runs" | 11-10 | Production `7704429697` success, page 200, alt present, listed on `/blog` |
| Read Ship #068 | 11-11 16:12 | Production `7724516778` success, page and art 200, listings link it |
| Read "The Server Has No Key" | 11-12 late | Production `7758628398` success, page 200, alt and caption match Comms' memo, listed on `/blog` |

## Served checks of the product, from my log

- **11-06:** served reads on beta and alpha for the Settings groups, project-page "Link a repository" words and Edit removal; CXO closed #2273 and #2271. Check 5 (capped delete) passed and surfaced a "reminder" noun defect that Lead fixed. Pressed Unlink on a test project (#2272 PASS on my quote). I built the non-admin "Advanced" last group (`a1fd1f0ea2`).
- **11-07:** #2282 step 4 passed on beta (Connect from beta landed connected, no revoke), on xian's word to sign a test account in. Ran the #2318 clear pair for PA on `310ab2ed79`. Answered Lead's #2322 account question; the stored-done run waits for #2325 or Q8 after PPM withdrew the go on the web-pat-test account.
- **11-10:** Lead asked five served 2328 runs (a pronoun-only completion target asks which one). Not run: the harness denied reading the one test account's credential file, and I did not retry. Mailed Lead, cc CXO and Exec; options are with xian, or PA's scripted check runs them.
- **Also this week:** traced the multiple `<h1>` per post to `publish-post.js` mapping `#` to h1 by design (fix is visual and waits on CXO and PM). Found the Beta post's "Building in Public" badge is a site-wide default tag. Main's Code Quality went red on the bearer-credential gate on 11-11 (a fake test token quoted in prose in four files); mailed Lead, cc Arch and Exec, and the owners fixed it. 11-12: replied on the 2342 App callback (agree with listing both callbacks) and accepted #2344 row 2.

## Open, each with its blocker

- **2328 five runs:** xian's word on the credential read, or PA's rerun.
- **Served rows on 2342:** none open until xian's GitHub App sitting.
- **#2344 row 2** (Buttondown confirmation headers): a mailbox xian names, via Exec.
- **h1 change:** a CXO and PM go.
- **#2322 stored-done run:** #2325 reset or Q8 account.
- **#2267:** a username account. **Consent-page row:** a revoke xian said no to.
- **#2286 note:** an unconnected account.

## Corrections to my own claims

1. 11-12 22:16: I logged that the Server Has No Key page returned 404. It was a 308 to the trailing-slash URL, which I read wrongly; with redirects followed it returned 200. Corrected in the log the same night.

## Next week (2026-11-13 to 2026-11-19)

Run the 2328 runs and any 2342 served rows as soon as their blockers clear. Do #2344 row 2 when a mailbox arrives. Deploy-check each post as it publishes. Blocked on: xian (credential-read word, mailbox, GitHub App sitting), CXO and PM (h1), the #2325 reset.

Verified how: session logs 11-06 to 11-12 read this fire; deploy states and page checks are from each day's own check (not re-run now). Layer: my own records plus deploy and served-HTML checks; not a fresh served run. Denominator: the items named, not everything touched in the window.

-- Web
