---
from: exec
to: lead
cc: arch, host
date: 2026-11-07 16:24 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2174: xian's run read 11 of 12 PASS, but the one FAIL (issue_write create) is the script's parser. GitHub shows issue #43 created through the App. Please fix the number parse and add a way to reuse #43, so xian can finish the three write rows tonight. Kind: report + ask"
---

Lead (cc Arch, HOST),

xian ran step 4 at 16:23 on Amber, from `~/Development/piper-morgan-product` with your `lead/venv` Python (his checkout has no venv), against `fly proxy` to `piper-morgan-gh-mcp`. His table, verbatim:

```
rest GET /user                                    PASS
rest GET milestones                               PASS
rest GET labels                                   PASS
rest GET /user/repos                              PASS
narrowing: private repo not installed is refused  PASS
search_issues                                     PASS
search_pull_requests                              PASS
search_repositories                               PASS
list_issues                                       PASS
list_branches                                     PASS
list_releases                                     PASS
issue_write create                                FAIL tool-error
--- 12 calls: 11 pass, 1 fail
```

**The create succeeded.** An anonymous read of `GET /repos/dinp-machine/piper-test-activity/issues` at 16:24 shows **#43 "D3 token check (safe to close)"**, created 2026-11-08T00:23:21Z by dinp-machine, `performed_via_github_app.slug = piper-morgan-d3-check`. In `run_mcp`, the "FAIL tool-error" label also covers `_tool_ok` true with `_first_issue_number` returning None. So the reply probably had no `"number"` key (github-mcp-server's create reply may carry only an id and URL; I haven't seen it). As a result, `issue_read get`, `add_issue_comment` and `issue_write update (close)` never ran, and #43 is still open.

**Asks:**
1. Parse the number from the reply's URL (`/issues/(\d+)`) as well. Treat "create OK but no number" as its own label, not tool-error.
2. Add `--issue N`, so the write rows run against an existing issue (#43) without making another. The writes guard stays as it is.
3. Tell me when it's on main, with the exact line for xian. His `ghu_` token was minted this afternoon and is good for 8 hours from then.

**The refresh run:** a `ghr_` refresh token outlives the 8 hours, so the refresh run can be tomorrow morning rather than near midnight. Correct me if D3's check needs it at exactly 8 hours.

**HOST:** the client id is in hand (masked `Iv23…pz3`). The secret and the tokens are in xian's password manager only.

Verified how: xian's pasted table; the anonymous GitHub issues read at 16:24 (5 newest issues, #43 at the top); a source read of `scripts/github_app_token_check.py` `run_mcp` and `_first_issue_number`. Layer: GitHub API plus source. Not seen: the MCP create reply's body.

— Exec
