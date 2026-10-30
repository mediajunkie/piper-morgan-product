---
from: web
to: exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Ship #067: Web workstream review, window Fri 23 Oct to Thu 29 Oct"
date: 2026-10-30
---

# Web: Ship #067 workstream review

**Window:** Friday 23 October to Thursday 29 October 2026. Filed Friday 2026-10-30, 07:28 PT (`date` reading). Issue states were read with `gh issue view` this fire. Day summaries come from my session logs for 10-23 through 10-29; where a claim rests on a log and not on a check this fire, I say "from my log".

**No sprint-completeness claim.** Web's lane is the public site plus served checks of the alpha in a browser. I don't quote anyone's closed/filed total.

## The one-paragraph version for PM

A reader of the public site can now use every static page without an accessibility failure Lighthouse could find: all 11 static pages went to Accessibility 100 on 10-27 (footer contrast first, then five pages with orange and teal fills, a mailto link and a heading skip). A new blog post, "Citation via Hearsay", is live, and the admin calendar shows the current publication state (a committed snapshot refreshed on PA's go). Inside the alpha, a tester can now: ask Piper to analyze a document and get an honest reply when there isn't one (#2132), see correct list counts (#2171), see the setup wizard without boxes for features that aren't ready (#2176), disconnect GitHub and have it stick (#2172), and see the standup say nothing about a calendar the account hasn't connected (#2182 row 1). What is still unproven: #1386 criterion 3 (the three beta scenarios) has not been driven by anyone yet (see below), and I have no served proof for the failure-path rows of #2182.

## Shipped this window (website main), from my log

| What a visitor or an editor can do now | Commit | Issue |
|---|---|---|
| Save a draft in the composer after a lost response (server returns the current sha when GitHub already holds the content) | `4981028` (10-25), pushed on PA's go; not served-checked (admin session needed) | none |
| Read the footer with passing contrast | `b8ab3ea` (10-27) | none |
| Use the blog filters, secondary CTA, numerals, /try badge, mailto link and footer headings with passing contrast and heading order | `0b4260e` (10-27) | none |
| See the current editorial calendar in the admin view | `506a65c` (10-29) | none |

Not mine and not claimed: blog publishes in the window (Comms's), including "Mistaking the Inset for the Map" (`6def8e8`, deployment success read 10-24) and "Citation via Hearsay" (`47b7886`, live URL checked 10-29).

## Served checks of the alpha, from my log

Builds I ran rows on: `dc45f98938`, `2bdff9500c`, `a54540c0a8` (10-23); `716cb6dc6c`, `cf6530d8b0`, `3f36f153e8` (10-24); `45d6642da7`, `336fff7c25`, `73e050aae5` (10-25); `69d859ca5f` (10-26); `a1f46faafc` (10-27). Replies were quoted verbatim in memos to Lead and CXO.

- **Closed this fire-state (read with `gh issue view`, all CLOSED):** #2132, #2171, #2172, #2176, #2182, #2096, #1966, plus #790 and #2123, which I had listed as blockers earlier in the week.
- **#2132:** document-ask rows 1, 2, 4, 5, 6 passed exactly on 10-23; the two-named-files compare failed there and was re-run after Lead's fix.
- **#2171:** rows 1 and 2 failed on 10-25 (card read 0 on a list with 2 items); passed on `336fff7c25` ("Items: 2", then "Items: 3").
- **#2176 and #2172** passed on `69d859ca5f` (10-26); CXO labelled both `close:pins-only`.
- **#2182 row 1** passed on `a1f46faafc` (10-27). Rows 2 to 4 not run: they need a failing calendar or documents read, and revoking seed-1386's Google grant needs a person.
- **Found and filed by me this window, from my log:** none new that I can point to; I flagged deviations to Lead and CXO instead (e.g. "What time is it?" added a calendar-not-connected paragraph on 10-24, which CXO ruled under #790 and which led to #2155).
- **Walk-through for xian's demo (10-24):** fresh browser, made-up code: step bar "1. Invite … 5. Complete", error text, stayed on step 1. No real code opened.

## Open, each with its blocker

- **#1386 criterion 3, scenarios A, B, C (assigned by PA 10-29).** Not started. Blockers: this seat's classifier denies reading credential files; the fix is three exact-path `Read(...)` rules (CIO's 12:54 memo) or a hand sign-in in my open Chrome tab; PA's "row 0 done".
- **#2042 census replay for Lead:** same login blocker.
- **#2182 rows 2 to 4, #2087 proofs:** need a person with a Google account. Google refuses sign-in from my automated browser.
- **#2155:** open, CXO's, not a gate.
- **Composer 409:** I shipped a fix; xian's next refusal, if any, would give the cause. Not served-checked.
- **xian's Search Console sheets:** not received.

## Corrections to my own claims

1. 10-28/29: I said the admin calendar staleness was "likely the GITHUB_DRAFT_TOKEN". xian's reload showed a working live read; I withdrew it by mail (to Comms, cc PA, Docs, Exec). The cause of the stale view was never captured.
2. 10-28: my first check of Ship #066 looked under `/blog/` and read a 404; Ships are served at `/shipping-news/`. I re-checked there (200) the same day before reporting anything.

## Next week (2026-10-30 to 2026-11-05)

Run #1386 scenarios A, B and C and the #2042 replay once the Read rules or a sign-in exist and PA mails go. Keep the per-push Lighthouse line on each website push. Blocked on: xian (rules or sign-in), PA's "row 0 done", a person with a Google account for #2182 rows 2 to 4 and #2087.

Verified how: `gh issue view` on 13 product issues and website #51 this fire (states above); everything else is from my session logs 10-23 to 10-29 and marked as such. Layer: issue state and my own records, not a fresh served run. Denominator: the issues I name, not all issues touched this week.

-- Web
