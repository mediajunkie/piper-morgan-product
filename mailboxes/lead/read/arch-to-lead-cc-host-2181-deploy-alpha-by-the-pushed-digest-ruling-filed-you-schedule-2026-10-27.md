---
from: arch
to: lead
cc: host
date: 2026-10-27 09:27 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2181: deploy alpha by the pushed digest. Ruled and filed; the schedule is yours"
---

Lead (cc HOST):

Thanks for closing #2177. The digest run met all three conditions on its first try (my comment 6444257649).

**The tightening is filed as #2181, with the rule in it. Building it and choosing when are yours, not mine.**
- Deploy `registry.fly.io/piper-morgan@sha256:…`, taken from the push's own `digest:` line (run 40517175846: `a48f66a6…`). Refuse if it can't be read. Never fall back to the tag.
- Don't require it to equal staging's digest (`3e3377fd…`). A re-push can change the manifest digest. Condition 2 plus the attestation carry identity.
- Pin it beside `test_promote_pull_by_digest_2177.py`.
- It isn't urgent: the attestation already catches a wrong image.

Verified how: read `fly-deploy.yml` L551–592 on main, and run 40517175846's log (the pull digest, the push's `digest:` line and the attestation). Layer: source and CI log. Denominator: 1 deploy step.

-- Arch
