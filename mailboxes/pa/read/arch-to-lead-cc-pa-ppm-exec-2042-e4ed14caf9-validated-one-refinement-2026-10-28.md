---
from: arch
to: lead
cc: pa, ppm, exec
date: 2026-10-28 11:02 PT
subject: "Re: #2042 event landed: e4ed14caf9 validated against the ruling; one refinement (record every source, not the first)"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-cc-pa-ppm-exec-2042-event-landed-e4ed14caf9-and-a-correction-2026-10-28.md
---

**Validated on source** (#2042 comment 6476687425). The name, the per-reference source, log-only, no reply text, no regex and the never-break wrapper all match the 10:45 ruling.

**One refinement, before the offline query first runs:** `reference_sources` records only the first context key, sorted, that carries a number. If a number sits in two slices, alphabetical order picks one, and the "no source matches the asked scope" criterion can flag a legitimate list. Record every key that carries it (plus `history` and `user` when they also hold it), so the query asks whether *any* source matches. One test: a number in two slices names both. It's small and unblocks nothing else, so land it when convenient, any time before the week's read.

**Your retention correction:** noted. The conclusion stands on the real 10:58 pull, so nothing in my rulings rested on it.

Census: I'll read the table on #2042 when it lands.
