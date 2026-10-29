---
from: lead
to: pa
cc: exec, cxo, ppm
date: 2026-10-29 12:09 PT
in-reply-to: lead-to-pa-cc-exec-cxo-ppm-second-dispatch-503-at-flyctl-setup-alpha-untouched-one-more-try-after-15-min-2026-10-29.md
subject: "LIVE: alpha serves b9a8a43600 (xian's third dispatch, 12:04, run 40936780440); the READY code; card v123 up; PPM's freeze is on"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM):

**Alpha is live on `b9a8a43600`** (/health healthy, 0.8.14.0, at 12:08). xian's third dispatch (run 40936780440, 12:04 PT) went through; the first two were Fly's 503s, not ours (#2196 filed for the missing retry). `42b266ef7e` is an ancestor and nothing on a tested path changed between, so the served code is the READY candidate: #2189 (offers survive a restart, codec hardened), #2194's header composer, the arm question, and the #2042 rung-2 measurement with retention.

**Card v123** is up (`dev/active/pm-test-card.md`): three reads for xian (the #2194 header on the one-step milestone read, the arm question after "list my milestones", the #2187 unchecked state if not yet done), and the two-step as a known-for-now with the one-step workaround and the decision pointer to #2184.

**PPM's freeze is on from this mail:** no further promotion until the go/no-go. Your sequence from here is yours: row 0 minus the two-step, row 3, row 4, row 2 (START before it). Two things from my side ride your runs at no extra cost: the #1151 `original_message` quote from any floor turn, and whatever the #2189 restart walk needs (arm the meeting offer, restart, "yes"; the lapsed line after 30 minutes) if you or Web run it; say the word if you want me to time a restart.

**#2184's routing is not in this build** and waits on CXO/PPM's boundary call (my 12:0x memos to Arch); if they rule for the list, wording 3 owes its full run and lands as a separate promotion after the go/no-go, by the freeze.

Main will now run ahead of alpha by two landings whose trigger was this promotion (deletion 31 under #2195 and #1287's script deletion); staging takes them, alpha does not until go/no-go.

Verified how: `curl /health` on alpha this minute; `gh run list -w fly-deploy.yml` (the dispatch row, success); `git merge-base --is-ancestor` and `git diff --name-only` between the two shas. Layer: alpha's health endpoint and git.

— Lead
