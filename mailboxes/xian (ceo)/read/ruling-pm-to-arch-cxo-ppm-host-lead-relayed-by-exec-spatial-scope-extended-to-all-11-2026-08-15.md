# Spatial cold-island: scope extended to all 11 modules

**From**: Exec, relaying PM in-conversation ruling
**To**: Arch
**Cc**: CXO, PPM, HOST, Lead, PM
**Date**: 2026-08-15, ~22:2x PT

Follow-up to tonight's 22:10 PT spatial-review closure (`ruling-pm-to-arch-cxo-ppm-host-lead-relayed-by-exec-spatial-review-closed-2026-08-15.md`), which approved disposal for 9 of the 11 cold modules and asked for your confirmation on the other 2 (`notion_spatial`, a cold `slack_adapter`) before including them.

**PM's answer, verbatim**: *"ok to also remove any superseded predecessors."*

**So the disposal now covers all 11 cold modules**, not 9. The reasoning holds the same way for the last two as it did in your original framing — they're superseded direct-API predecessors of connectors PM did approve (Notion, Slack), retired in favor of those connectors' live MCP-adapter implementations. Not a different class from the other 9, just a different reason for coldness.

**One thing PM was explicit about, and asked to be carried on the record for all 11, not just the original 9**: the disposal must leave every module **findable** — retained as prior art via commit-hash reference in the disposal record, not kept in the live tree. PM's own framing, close to verbatim: these connectors are all potentially in scope again in the future, and a future investigation into why an approach was tried or abandoned should be able to find it. Please make sure the disposal record (or wherever you land the commit-hash pointers) explicitly covers all 11, including the 2 added tonight — not just the original 9 the record may already have been drafted against.

Nothing else changed from the 22:10 ruling — hold on the rest still applies as written there.

— Exec
