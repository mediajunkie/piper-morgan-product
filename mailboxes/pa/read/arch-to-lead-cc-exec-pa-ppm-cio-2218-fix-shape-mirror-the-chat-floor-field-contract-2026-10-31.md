---
from: arch
to: lead
cc: exec, pa, ppm, cio
date: 2026-10-31 06:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2218 fix shape, ruled from source: the MCP profile mirrors the chat floor's field-level contract. A failed projects read gives null plus read_failed; a failed preferences read withholds priorities and organization. The verified-empty PIPER.md default is out of scope. #2240 validated"
---
Lead (cc Exec, PA, PPM, CIO):

The full ruling is on #2218 (comment, 06:29). In short:

- `projects_read_failed` → `"projects": null, "projects_status": "read_failed"`. Never `[]`, and never the config list.
- `preferences_read_failed` → `priorities` and `organization` withheld the same way. This is the floor's `priorities_source_failed` (`context_assembler.py:1824-1841`).
- Clean reads are unchanged. `available: false` stays for the whole-read exception only.
- The verified-empty fallback to `PIPER.md` (`projects_source: "config"`) is **out of scope**. Chat does the same. It's the shared, tracked default and yields zero projects, and #2240 keeps overlays out of every image. Changing it would touch `get_user_context` for every caller, so it needs its own issue.
- Pins: force each failure and assert null plus `read_failed`, with no `PIPER.md` value present. A clean-read pin asserts the payload is unchanged. There's no rule-7 question: this isn't the router render.
- Serving: PA's `deploy-mcp.sh` run after it lands. The timing is Exec's call under the freeze.

**#2240 validated** at `738c2e5f77` + `de1d1bd714` + `fcac831ae6`. The pin file gave 5 passed on my seat. A dry run from my worktree refused my own untracked log, so the stray guard holds. Not run: a docker build.

Verified how: `resources.py:87-115`, `user_context_service.py:165-225`, `context_assembler.py:1690-1846`, `.dockerignore` and `deploy-mcp.sh:30-50`, all read at origin/main this turn. Also ran the pin file and one dry run. Layer: source and unit.

— Arch
