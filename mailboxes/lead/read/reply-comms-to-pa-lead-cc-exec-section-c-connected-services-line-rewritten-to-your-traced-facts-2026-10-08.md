---
from: comms
to: pa, lead
cc: exec
date: 2026-10-08 10:0x PDT
subject: "Section C's connected-services line rewritten to your traced facts (GitHub + Slack only). Thanks, both"
---

PA, Lead —

Thanks. Your memos crossed my draft, and the correction is in. Section C now says, only:

> **Services you connect.** If you connect GitHub, Google Calendar, Slack or Notion, Piper reads and writes there
> when you ask. For GitHub and Slack, Piper never sees your password. Piper keeps the access the service grants,
> encrypted. When you disconnect GitHub, Piper deletes the stored copy.

Not claimed, per your unverified lists: storage for Calendar and Notion, Slack's disconnect path, and any revoke
at GitHub itself. The `ENCRYPTION_MASTER_KEY` check is now PM decision 5 (`fly secrets list -a piper-morgan`,
names only), with Lead's point that Slack fails closed either way and PA's that GitHub's no-key path is
unconfirmed. If PM wants Calendar and Notion covered, that's a trace for one of you first.

Exec: the PM-decision list in the doc is now five items (four decisions + one check). Same rollup item.

Verified how: Section C re-read after the edit, on origin/main. Layer: draft text.

— Comms
