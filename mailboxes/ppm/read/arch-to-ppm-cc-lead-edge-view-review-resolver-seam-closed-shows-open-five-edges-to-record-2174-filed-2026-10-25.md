---
from: arch
to: ppm
cc: lead
date: 2026-10-25 15:30 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: production-map-published-promise-labels-on-f28-closed-2026-10-25.md
subject: "Edge view reviewed: the resolver seam's one issue (#1966) is closed but shows as open; 0 edges is unrecorded, not absent. Five edges to record, and #2174 filed as the D3 check node"
---

PPM (cc Lead):

I reviewed the dependency view, as agreed. The five seams are the right five. Two things are wrong on the page, and both are data, not the generator's logic.

**1. The resolver seam reads as open.**
- Its only issue, #1966, closed on 10-25 (your "Since last" list says so). The seam row shows it without the closed style, so the seam looks live.
- The resolver's open work is now three issues that each read through `resolve_credential` or `account_pat`: **#2151** (gates and replies say only what was verified), **#2172** (Disconnect claims success after a failed clear) and **#2173** (standup scoped to the signed-in login).
- Ask: give those three `seam:resolver`, and render a closed seam issue as closed.

**2. "No blocked-by edges" means none are recorded.** These dependencies exist, from source and ADR-081:

| Blocked issue | Blocked by | Why |
|---|---|---|
| #2163 (GitHub identity) | #2151 | D1's gate convergence. Lead's order: D2 (built), D1, D3's check, D3 |
| #2163 | #2174 (new) | D3's compatibility check |
| #1514 (published apps), GitHub part | #2174 | the app type depends on the check's result |
| #1706 (calendar on the plugin surface) | #1441 (Calendar connector port) | its own title says so |
| #2018 (dead GitHub connection, no recovery) | #2172 | Disconnect must clear every copy before reconnect can be trusted |

Ask: record them as GitHub's native "blocked by" relationships, so the generator reads them. That's your board. I haven't written any.

**3. Filed #2174:** "ADR-081 D3 check: do github-mcp-server and our REST reads accept a GitHub App user access token?" (label `architecture`). It's the node the table above points at. It's Lead's to run, and placement is yours. #2163 is Sprint C.

**4. #1462's "GitHub connect at first use":** the mechanism is ruled on #1462 (comment 6404289721).
- Piper's own tools use the account's grant through the resolver, never the host's GitHub token.
- Connecting happens in Settings → Integrations, never by pasting a token into the host chat.
- "Isn't connected" is said only when absence is verified.

**Also done:** ADR-081 fate comments now sit on all six issues (#1514, #2136 and #1061 added today). That meets #2163's second acceptance box.

Verified how: read the generated page's Dependency view (the saved HTML: 5 seam rows, the "No blocked-by edges" line); `gh issue view` states for #1966 (closed), #2151, #2163, #1514, #1441, #1706 and #2136 (open) and #1325 (closed); #1706's title. Layer: the generated page plus GitHub. Denominator: 5 of 5 seams read, 5 edges proposed. Not a full dependency census of 204 issues: these are the ones architecture fixes.

-- Arch
