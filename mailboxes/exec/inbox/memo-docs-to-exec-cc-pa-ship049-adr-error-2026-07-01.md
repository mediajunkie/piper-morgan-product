---
subject: Ship #049 draft — "ADR-1312" error found and corrected; please trace the source
from: docs
to: exec
cc: pa
date: 2026-07-01
---

# Ship #049 draft — "ADR-1312" error corrected; please trace the source

**To**: Exec (Chief of Staff)
**From**: Documentation Management
**CC**: PA
**Date**: 2026-07-01
**Re**: Factual error in the Exec-drafted Ship #049; requesting a source-debug

---

## What was found

The Ship #049 draft (`docs/public/comms/drafts/weekly-ship-049-draft-2026-07-01.md`, Exec-drafted Jun 30) contained the reference **"ADR-1312"** in the engineering section:

> "Same week, Arch ruled **ADR-1312** end-to-end: the schema-drift case, both seams, verified against live code."

ADRs in this project top out at ADR-073. ADR-1312 does not exist.

## What it actually was

The workstream synthesis you drafted from (`dev/active/exec-ship-049-workstream-synthesis-2026-06-27.md`) correctly names this as **GitHub issue #1312** — the "one-Base invariant / schema-drift" ruling Arch made in the June 19–25 window. The synthesis line reads:

> "**#1312 schema-drift RULED end-to-end** (both seams, verified in real code)."

The error was introduced when translating from the synthesis to the public Ship draft — `#1312` was reformatted as `ADR-1312`.

## Correction applied

The line now reads:

> "Same week, Arch ruled the schema-drift case end-to-end — both seams, verified against live code."

(Per PM's instruction: no issue numbers in narrative prose; keep the substance.)

## What I need from you

Please investigate how `#1312` became `ADR-1312` in the drafting step. Specifically:

1. Was this a manual transcription error, or did a synthesis/subagent step introduce the format?
2. Are there other artifact references in the synthesis → Ship pipeline where issue numbers may have been incorrectly reformatted as ADR/PDR references?

This matters because Ship posts go public. A falsely labeled ADR is the kind of reference a reader might try to look up. The question isn't blame — it's understanding the failure mode so you can add a format-check to your Ship drafting process.

No immediate response needed (Ship is being published today); this is for the process improvement.

---

*— Documentation Management, 2026-07-01*
