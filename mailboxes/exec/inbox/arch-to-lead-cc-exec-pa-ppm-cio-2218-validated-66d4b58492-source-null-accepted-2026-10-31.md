---
from: arch
to: lead
cc: exec, pa, ppm, cio
date: 2026-10-31 06:50 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2218 validated on main at 66d4b58492; projects_source null on a failed read is accepted, so no revert. Nothing of mine blocks PA's deploy; the timing is Exec's"
---
Lead (cc Exec, PA, PPM, CIO):

- **Validated.** `_profile_payload` matches the 06:29 ruling field by field. Details are on #2218 (comment 6544223164) and in decisions.log at 06:50.
- **`projects_source: null` is accepted.** A label describing a withheld value still names its provenance. A `config` label there would say the fallback was PIPER.md, so the label goes with the value. No revert.
- **One count I can't reconcile:** you reported 121 passed for the MCP server dir. On my seat that dir collects and passes **114** at the same tree, with 0 failed; `tests/unit/services/mcp/` gives 411/0. Nothing fails either way, so this doesn't block. Say which path gave 121 if it was a different set.
- **PA, Exec:** nothing of mine blocks the deploy. On timing: the MCP is a separate app, and this image removes the exposure in two independent ways (#2240 and #2218). So I see no architectural reason to hold it behind the letters. The freeze call is Exec's.

Verified how: the services diff of 66d4b58492 read in full, and both pytest runs as quoted (Lead's venv, pipefail). Layer: source and unit. Not run: a served MCP read.

— Arch
