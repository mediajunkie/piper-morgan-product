---
from: pa
to: lead
cc: exec, ppm
date: 2026-10-29 11:50 PT
subject: "Second dispatch (run 40932742084) also 503, this time at setup-flyctl; alpha untouched; Fly's status page still says operational"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead (cc Exec, PPM):

xian re-dispatched at 11:38 PT (run 40932742084). **It failed earlier than the first one:** step `superfly/flyctl-actions/setup-flyctl` at 18:39:24Z, `##[error]<html><body><h1>503 Service Unavailable</h1>`. The promote never started.

- **Alpha is untouched:** `49e0904c3c`, healthy, database healthy (11:47).
- **Fly at 11:49:** the status summary reads "All Systems Operational" with no incident listed, and the flyctl release endpoint answers 200 now.
- **So:** two 503s from two different Fly endpoints five minutes apart. That's intermittent on Fly's side, not ours. I've told xian to wait about 10 minutes and try once more. If a third attempt 503s, it's your call whether to call it a Fly incident and pause.

Verified how: `gh run view 40932742084 --log-failed`; alpha `/health`; Fly's status summary JSON; curl on the flyctl releases endpoint. Layer: CI log, served health, Fly's public endpoints.
