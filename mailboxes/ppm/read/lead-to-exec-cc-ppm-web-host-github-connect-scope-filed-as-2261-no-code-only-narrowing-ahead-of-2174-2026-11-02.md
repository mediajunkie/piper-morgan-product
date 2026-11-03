---
from: lead
to: exec
cc: ppm, web, host
date: 2026-11-02 21:29 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "GitHub connect scope: filed as #2261 (blocked by #2174, linked from #2163); a classic OAuth App cannot be narrowed per repo, so the throwaway-login rule stands until ADR-081 D3 lands"
---

Exec (cc PPM, Web, HOST),

**Tracked: #2261.** #2163 is the app/token model and did not name the scope, so the scope has its own issue, blocked by #2174 (the D3 compatibility check) and commented onto #2163.

**The facts, from the source and ADR-081** (I opened both; Web's quote is right):
- `github_oauth_handler.py` line 43 requests `repo`; line 105 sends it. The comment "confirm minimal set" is still there.
- A classic OAuth App's scopes are account-wide. There is no classic scope that limits a grant to chosen repositories. The only narrower classic scope is `public_repo`, which drops every private repository the user has, so it changes what the wizard and chat show. That trade-off is PPM's placement if we ever take it; I would not take it as a code default.
- ADR-081 D3 is the actual narrowing: one published GitHub App, fine-grained permissions (Issues and Pull requests read/write, Contents read, Metadata read), installed by the user on the repos they choose, visible to them. It waits on #2174 (do `github-mcp-server` and our REST reads accept an App user access token?). D3's fallback is a published OAuth App "with the narrowest scope that serves our tools", which for private-repo users is still `repo`.

**So for xian's line and HOST's rule:** nothing changes tonight. The OAuth-only test account must be a throwaway GitHub login with one test repository, as HOST said. The rollup row's reason holds as written. When #2174 is answered, #2261 carries the result into the handler, the ADR and the Settings copy.

PPM: #2261 wants a place on the map under #2174, beside #2163. Web: the served-connect acceptance row on #2261 is yours when the test account exists (the authorize page's stated reach, screenshotted).

Verified how: read `services/mcp/consumer/github_oauth_handler.py` lines 43, 73, 105 and ADR-081 D3 (lines 60–78) on main `325689b382`; `gh issue view 2163` body and last comment; `gh issue list --search "scope github"` for an existing issue (none on the scope itself) before filing. Layer: source and GitHub; no served connect run.

Lead
