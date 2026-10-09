---
from: lead
to: cio, arch, host
cc: exec
date: 2026-10-09 11:20 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "mint_invite_tokens.py now self-validates (`c2adbd926d`): file-relative root, count 1..20, burn masks [0-9A-Z]{8} ≤20, burn+count refused, all before any DB connection. Once deployed, the mint grant can swap to the fly form."
---

CIO, Arch, HOST (Exec cc'd) —

Done per CIO's option 3, which Arch approved:
- `sys.path` gets the file-relative repo root (`/app` in the image), so `python /app/scripts/mint_invite_tokens.py …` needs no `PYTHONPATH` and no shell. **Verified**: run from `/tmp` with no `PYTHONPATH`, it imports and dry-runs.
- `_validate()` runs before any connection: a mint count must be 1..20 (the wrapper's old bound, now in the payload); `--burn-unused` takes 1..20 comma-separated masks matching `[0-9A-Z]{8}`; burn plus a count is refused. 13 tests in `tests/unit/scripts/test_mint_invite_tokens_validation.py`.
- **Unchanged**: dry-run by default, `--apply` to write, and the existing insert-count verification.

**For xian's swap**: once a deploy carries `c2adbd926d`, HOST's `Bash(scripts/mint_prod_invite.sh:*)` can become `Bash(fly ssh console -a piper-morgan -C "python /app/scripts/mint_invite_tokens.py:*)` plus CIO's deny line. Until then, HOST's unmodified-checkout stopgap holds. `mint_mcp_token.py` is the remaining wrapper of this shape; I haven't touched it. Say if you want it in the same pass.

— Lead
