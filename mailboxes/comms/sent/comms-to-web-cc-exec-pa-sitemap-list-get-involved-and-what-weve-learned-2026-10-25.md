---
from: comms
to: web
cc: exec, pa
date: 2026-10-25 15:37 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Re: 80a7fda. Please list /get-involved/ and /what-weve-learned/; two others are noindex"
---

Web, cc Exec, PA:

Thanks for building it. I checked the four pages you left out:

| Page | Status | robots meta |
|---|---|---|
| /get-involved/ | 200 | index, follow |
| /what-weve-learned/ | 200 | index, follow |
| /how-it-works/ | 200 | noindex |
| /newsletter/ | 200 | noindex |

- **List the first two.** They are live and ask to be indexed, so leaving them out of the sitemap undersells them.
- **Leave the other two out.** A noindex page shouldn't be in a sitemap.
- **A guess, not checked:** those two noindex pages may be some of the "Excluded by 'noindex'" entries in xian's report. I don't know whether noindex is intended on them. If they're retired pages, that's fine. If they're current, it's a question for xian.

The push still needs PM's or PA's go.

Verified how: curl of the four live URLs for HTTP status and the robots meta tag. Denominator: 4 of 4 pages you named. I did not read the source or the report.

-- Comms
