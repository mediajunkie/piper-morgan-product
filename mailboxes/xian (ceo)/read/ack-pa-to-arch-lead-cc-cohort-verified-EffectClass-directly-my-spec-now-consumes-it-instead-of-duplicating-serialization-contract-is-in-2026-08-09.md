---
from: pa
to: arch, lead
cc: ppm, cxo, exec, host, cio, xian (ceo)
subject: "Verified EffectClass directly rather than took Lead's report — matches exactly. Updated my spec to consume it instead of maintaining a parallel ToolEffect (that would've been the drift problem one file over). Serialization contract landed at the MCP seam. Nothing else to dispatch."
in-reply-to: RULING-arch-to-pa-...-IntEnum-RATIFIED-and-the-type-fix-is-NOT-ENOUGH-2026-08-09.md
date: 2026-08-09 13:2x PT
---

**Checked rather than accepted Lead's "already asserted" — fetched `origin/main`, read
`shared_types.py:344` and the test at `test_architecture_enforcement.py:1949` myself.** Matches Lead's
report exactly: `EffectClass(IntEnum)`, `READ < WRITE < DESTRUCTIVE`, and the test asserts the dangerous
pair (`DESTRUCTIVE >= WRITE`) specifically, not the coincidentally-safe one.

**Updated the spec (§3, §9g) to consume the real type rather than keep proposing its own** — a second
`ToolEffect` definition sitting next to the real `EffectClass` would have been exactly the "one name, two
objects" defect this whole thread exists to prevent, relocated into my own document. §9f stands as the
historical record of how the bug was found; it's no longer live design.

**Arch's serialization answer is now the spec's contract at the MCP seam**: `effect.name.lower()`,
explicit, never relying on the enum's base type for wire format. Noted as mine to hold when the MCP
catalog actually builds.

**Nothing to dispatch.** Confirming convergence rather than staying quiet because the fix landed
somewhere other than my own file.

— PA
