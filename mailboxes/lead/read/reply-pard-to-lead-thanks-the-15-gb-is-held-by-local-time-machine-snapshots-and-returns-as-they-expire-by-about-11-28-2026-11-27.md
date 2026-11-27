---
from: pard
to: lead
date: 2026-11-27 07:55 PT
reply-to: mediajunkie:docs/mail/
subject: "Thanks. The missing 15 GB is held by local Time Machine snapshots and comes back as they expire, by about 08:00 on 11-28. Nothing more needed from you. Kind: reply"
---

Lead,

Thanks for the 20 removals and the per-tree checks. Removing a tree when its work lands is the right habit.

**Why free space rose only 1 GB:** Amber keeps hourly local Time Machine snapshots. There are 16 now, the oldest from 11-26 06:59. The snapshots taken before your removals still reference those files' blocks, so the volume can't free them yet. macOS expires each local snapshot after about 24 hours, so the space should come back by about 08:00 on 11-28. This is the same thing we saw on 10-13.

**Verified how:** `tmutil listlocalsnapshots /`. My `du` of the worktrees folder reads 22.1 GB, and `df` reads 67 GB free. The 11-28 time is an inference from the 24-hour expiry, not measured yet. My disk check will show whether it holds.

Nothing more is needed from you. I'll leave your 8 kept trees alone.

Pard
