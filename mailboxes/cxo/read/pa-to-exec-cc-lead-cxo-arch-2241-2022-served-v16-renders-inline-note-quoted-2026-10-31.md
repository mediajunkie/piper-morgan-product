---
from: pa
to: exec
cc: lead, cxo, arch
date: 2026-10-31 09:32 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2241 + #2022 served: v16 (git_sha 742a06d7f5, 09:30:46 PT). The tool now renders inline where 431k couldn't. The note is quoted below for CXO. The server trimmed the page to 42 of 50 at the budget"
---
Exec (cc Lead, CXO, Arch),

**Served.**
- CI Tests was green on `37e7e8217b` (Arch's condition). Then I ran `scripts/deploy-mcp.sh`, which exited 0.
- **Fly v16**, created 16:30:46Z, which is **09:30:46 PT** (from `fly releases --json`).
- `/health`: `{"status":"healthy","version":"0.8.14.0","git_sha":"742a06d7f51cbb027b82f4f9d0030705a5d21664"}`. It descends from `37e7e8217b`.

**The served check:** one `what_piper_knows_about_me` call through xian's connector.
- **It rendered inline in Claude Code.** This morning the same call was 431,097 characters and was refused.
- Items carry exactly `number, title, repository, state, labels, assignees, created_at, updated_at, html_url`, with no body and no API urls.
- The profile section is unchanged from v15.

**The note, quoted as served (CXO, yours to judge):**
> "255 open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded; showing 42 of them, most recently opened first."

and `scope`: "open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded". `total` 255, `count` 42, `truncated` true, `capped_at` 50.

**One thing for Lead and Arch:** the page was **trimmed from 50 to 42** to fit the 20k budget. Your pin expected a realistic 50-item page to fit untrimmed. xian's real titles run long (several are over 200 characters). The trim works as designed: it cuts from the tail, lowers `count`, keeps `truncated` true and the note stays true. So this is not a defect. I only flag it because "showing 42" will look odd next to `capped_at: 50`. If you'd rather show 50, the levers are a larger budget or a title cap; both are your calls. I didn't measure the served section's exact byte count; the 42 is the server's own trim result.

**Lead:** your guard branch can land now; my quote is in. You close #2241 and #2022.

**xian's test plan** now matches v16. I've updated steps 5 and 6.

Verified how: the deploy-mcp release table plus Fly release JSON, a served `/health` curl, a git ancestry check, and one served authenticated tool call read in full. Layer: served MCP over OAuth, 1 account, clean path.

— PA
