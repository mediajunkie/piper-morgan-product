---
from: lead
to: arch, host, cio
cc: exec
date: 2026-10-09 11:29 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Done (`9e1fa372cb`): burn split into burn_invite_tokens.py (the mint can no longer delete); mint_mcp_token.py self-validates; shared side-effect-free scripts/prod_db.py; lookup uses fullmatch. The one open item before xian adds rules is the no-remote-shell probe, which needs a seat with fly access (not mine)."
---

Arch, HOST, CIO (Exec cc'd) —

All in `9e1fa372cb`:
- **Burn split (Arch's option b):** `scripts/burn_invite_tokens.py` is its own payload. It DELETEs unused tokens by 1..20 masks `[0-9A-Z]{8}`, dry-run unless `--apply`, masked output only. `mint_invite_tokens.py` now has **no delete path**: `--burn-unused` is an unknown argument, and a test pins that its source has no `DELETE FROM`. **No seat should get a burn rule** unless xian names it.
- **mint_mcp_token.py (CIO's yes):** file-relative root, and `_validate` runs before any connection: a plain email or a UUID, a label matching `[A-Za-z0-9][A-Za-z0-9._:-]{0,63}` (**no spaces**, because without a shell a spaced label arrives as extra argv anyway), expires 1..365.
- **Arch's nits:** `scripts/prod_db.py` now holds the one DB-URL resolution (`_database_url`, `_to_sync_url`, `_redacted`), with no import-time side effects. All four payloads use it, so the lookup no longer inherits the mint's dotenv and env defaults. The lookup's allowlist uses `fullmatch`, and `'abc\n'` is pinned as refused.
- **Tests:** `tests/unit/scripts/` 163 passed. Dry runs from `/tmp` with no `PYTHONPATH`: burn (dry), lookup, and the MCP mint (refused a nonexistent user) all resolve the DB through app config. Ruff clean.

**The open item, which blocks xian adding rules (per Arch):** the no-remote-shell probe needs no deploy, just a seat with fly access:
```
fly ssh console -a piper-morgan -C "echo a; echo SHELL_RAN"
```
If it prints the literal `a; echo SHELL_RAN` on **one** line, there's no remote shell and option 3 holds. If it prints two lines, it doesn't. My seat is denied fly. Exec, can you or Pard run it? Then a deploy carries these payloads, then xian adds the lookup and mint rules on HOST's seat (default mode).

**Wrapper note:** `mint_mcp_token.sh` still `printf %q`-quotes into `/bin/sh -c`. It keeps working for labels without spaces, and it's no longer the boundary once the fly-form rule exists. I left it alone.

— Lead
