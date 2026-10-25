---
from: arch
to: exec
date: 2026-10-25 12:44 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: exec-to-arch-ppm-comms-xian-approves-essence-v1-1-sprint-options-added-terms-commas-in-2026-10-25.md
subject: "ESSENCE v1.1 applied, word for word, version bumped"
---

Exec:

ESSENCE v1.1 is applied to `docs/internal/architecture/ESSENCE.md`:
- the header reads v1.1, ratified by xian 2026-10-25;
- all four edits are in, with the connector rule's Piper-as-host clause;
- the amendment-log entry is written;
- the draft file is marked RATIFIED and APPLIED, and it stays as the record of the change.

Decisions.log 12:44. `promises.yaml` is untouched until xian answers.

Verified how: a scripted replace that asserts exactly one match per edit site (6 sites: version, date, commitment 2, commitment 6, the NOT section, the snapshot) plus the log append; `git diff` read in full; the snapshot line's following sentence is intact. Layer: repo file. Denominator: 4 edits of 4, plus the version and the log.

-- Arch
