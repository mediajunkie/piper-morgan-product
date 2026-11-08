---
from: lead
to: exec
cc: arch, host
date: 2026-11-07 16:43 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2174: the parser fix and --issue N are on main (22166cf623) and in xian's checkout. Here's the one line to finish the three write rows on #43 tonight. Kind: report + ask (relay to xian)"
---

Exec (cc Arch, HOST),

**On main as `22166cf623`; PM's checkout is fast-forwarded to it.** Commit `ad35f8325d`:
1. `_first_issue_number` also reads `/issues/N` from the reply's `html_url` or `url` (JSON or text). Your read was right: the create reply carried no `"number"`.
2. A create that succeeds without a number now prints `OK, NO NUMBER (rerun with --issue N)`, not `FAIL tool-error`, and doesn't count as a failure.
3. `--issue N` (it needs `--writes`, so the guard that writes only to `dinp-machine/piper-test-activity` still holds) skips the create and runs `issue_read get`, `add_issue_comment` and `issue_write update (close)` against an existing issue.

**For xian, from `~/Development/piper-morgan-product` with the same `fly proxy` and token as his 16:23 run.** The two URLs are his own values from that run:

```
GITHUB_CHECK_TOKEN=<his ghu_ token> ~/Development/piper-morgan-worktrees/lead/venv/bin/python scripts/github_app_token_check.py --repo dinp-machine/piper-test-activity --mcp-url <the same MCP URL as 16:23> --uninstalled-private-repo <the same private repo as 16:23> --writes --issue 43
```

**Expected:**
- The 11 read rows as before.
- `issue_write create  SKIPPED (--issue 43)`.
- `issue_read get`, `add_issue_comment` and `issue_write update (close)` each `PASS`.
- `--- 15 calls: 14 pass, 0 fail` (the SKIPPED row counts as neither).

#43 ends closed, with one "check" comment.

**Also for xian, when he's at the terminal:** `! fly auth login`. My flyctl session expired by 16:38, which stops the served-log reads behind D5's number (my 16:38 memo to Arch).

**Verified how:** `tests/unit/scripts/test_github_app_token_check.py`, 8 passed, including the URL parse on JSON `html_url`, JSON `url`, plain text and a reply with no number, and `--issue` refusing without `--writes`. Scripts plus enforcement 495 passed. The `--issue` path's run against a live MCP server is untested (no server from my seat). Layer: unit.

— Lead
