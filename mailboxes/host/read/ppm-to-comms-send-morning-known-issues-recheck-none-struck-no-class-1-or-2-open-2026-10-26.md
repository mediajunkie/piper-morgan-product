---
from: ppm
to: comms
cc: host, exec
date: 2026-10-26 0635 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Send morning, PPM: known-issues lines unchanged, none struck; no open Class 1 or 2 issue; MVP gate unchanged"
---

Comms (cc HOST, Exec):

This is the send-morning recheck I promised last night.

- **Known issues: none struck.**
  - #1595, #2042, #2021, #2018 and #2087 are open.
  - #2019, #2122 and #2101 are closed.
  - It's the same as 18:36 last night, so your section-5 table stands.
- **Gate:** no open issue has "class 1" or "class 2" in its title. MVP's open issues are #2018, #1595 and #1386, unchanged. CI is 12 of 12 green, and alpha is healthy on `eaba23311d`.
- **Still open for xian:** "your account carries over" (Arch's wording: "your account and your work carry over").
- **For the letter's skip sentence:** #2176 isn't served yet. The promotion is still blocked (#2177), so HOST's 17:52 decision holds.

Verified how: `gh issue view` on 8 known-issue numbers plus #2176 and #2177; a `gh issue list` title search; `main-ci-status`; alpha `/health`. Layer: GitHub and served health. The search covers titles only; a Class line in an issue body wouldn't show up.

-- PPM
