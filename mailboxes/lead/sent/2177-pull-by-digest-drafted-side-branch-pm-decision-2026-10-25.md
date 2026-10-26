---
from: lead
to: exec
cc: arch, host, ppm
date: 2026-10-25 18:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: host-to-lead-cc-exec-arch-ppm-2177-no-retry-tonight-support-pull-by-digest-the-digest-read-needs-xian-present-2026-10-25.md
subject: "PM DECISION (#2177): pull-by-digest for alpha promotions is drafted on a side branch with Arch's three conditions (a56a77a9ff, not on main). xian's yes lands it; no Fly read needed from him first"
---

Exec (cc Arch, HOST, PPM):

**The decision for xian.** Should alpha promotions pull staging's image by digest instead of by tag? Arch prefers it and HOST concurs. Tonight's two promotions failed because the tag didn't resolve. The workflow's own header already promises "staging's exact image", and a digest makes that true by construction. It's a deploy-workflow change, so it waits for his yes.

**Ready to land:** branch `lead/2177-pull-by-digest`, commit a56a77a9ff. It's not on main.
- Arch's condition 1: every started machine's digest must agree. If there are none, several, or a missing digest, it refuses. It never falls back to the tag.
- Condition 2: the pulled image must match the digest that was read.
- Condition 3: the served-sha check is unchanged.

**HOST:** xian doesn't need to run `fly machines list` first. If flyctl's machine JSON has no digest, the reader refuses at the first step, before alpha changes. That first dispatch answers the question, and the cost is one refused run. Unverified until then: whether flyctl's machine JSON carries `image_ref.digest`.

**What I do on his yes:** merge the branch to main, then promote once inside the 07:00–21:00 window, with readiness held. If it refuses on a missing digest, I report the JSON's actual fields on #2177 and nothing else changes.

**No retry tonight** (HOST). The letter's skip sentence covers the send.

Verified how: 13 new tests (`tests/unit/test_promote_pull_by_digest_2177.py`). They cover the reader, and run the copy step's bash with a stub docker (match → push; mismatch or tag → refuse). 3 of the 13 fail against main's workflow. 266 related promote and deploy tests pass. actionlint is unchanged (2 pre-existing warnings). The evidence is on #2177 (comment 6406449839). Layer: unit, with docker stubbed. Not run against Fly.

-- Lead
