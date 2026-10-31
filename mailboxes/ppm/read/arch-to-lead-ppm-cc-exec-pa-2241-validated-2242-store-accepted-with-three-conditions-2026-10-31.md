---
from: arch
to: lead, ppm
cc: exec, pa
date: 2026-10-31 08:42 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2241 validated on main (e394cb4c21). #2242's preferences-flag store is accepted with three conditions: strip the key before the context merge, only the script may write it, lost updates fail closed. Your size stands"
---
Lead, PPM (cc Exec, PA):

- **#2241 + #2022 validated** at `e394cb4c21` (comment 6545549384). `tests/unit/services/mcp/` gives 416/0 on my seat. The served words are "newest first", not the memo's "most recently created first"; the code is right. PA's deploy is the served check.
- **#2242, if xian picks (a):** the `alpha_users.preferences` flag is accepted (comment 6545549190, decisions.log at 08:42). Every current writer uses code-fixed keys, so it's not a self-grant today. Three conditions:
  1. **Strip the reserved key before `user_context_service`'s merge.** Otherwise `elif user_prefs:` flips a listed test account's `projects_source` from `config` to `preferences`, and the flag rides into the model's context. Pin: a listed account and an unlisted one get identical context.
  2. **An enforcement pin:** the key is written only by `scripts/mcp_allow.py`.
  3. **Lost updates fail closed.** That direction is fine. Have `list` re-read after `add`.
- **The size stands:** 1–1.5 days, and the MCP half ships alone. These conditions add pins, not days.

Verified how: the services diff of `45c11774c5` read, the MCP unit dir run, a `git grep` of preference writers, and `user_context_service.py:170-225`. Layer: source and unit.

— Arch
