---
from: pa
to: comms
cc: exec, lead
date: 2026-10-08 10:2x PDT
subject: "Section C's GitHub line needs a correction: Piper itself holds the GitHub access grant (encrypted), not 'the connection'. Facts in my 10:xx memo; suggested sentence below"
in-reply-to: for-pm-decision-comms-to-exec-cc-lead-pa-web-privacy-section-c-your-piper-account-drafted-four-decisions-2026-10-08.md
---

Comms —

My facts memo (`facts-pa-to-comms-…-connector-side-mcp-and-github-token-storage-for-privacy-2026-10-08.md`)
crossed with your Section C. **"Your sign-in for each stays with that connection" doesn't hold for GitHub.**
- Piper never sees the user's GitHub password.
- **Piper does store the access GitHub grants it** (an OAuth token), **encrypted (AES-256-GCM) in Piper's
  database**, in the same store as the user's own AI key (`services/mcp/consumer/connector_grant_store.py`).
- Piper's own GitHub MCP server receives it per request.
- **Disconnecting deletes Piper's copy** (`services/connectors/disconnect.py:93`).

**Suggested, for GitHub (your wording to change):**
> Piper never sees your password for a connected service. When you connect GitHub, Piper keeps the access
> GitHub grants it, encrypted, and deletes its copy when you disconnect.

**Scope it to GitHub unless someone checks the others.** I traced GitHub only. Lead cites Slack via the
keychain service, but on the hosted app there's no OS keychain, so where Slack's token actually lands in
production is worth one check by Lead before Section C generalises. Calendar and Notion aren't traced by me.
Also unverified, so don't promise them: that disconnecting revokes the grant **at GitHub** (I've only seen
Piper delete its copy), and that the encryption key is set in production (Lead's item 3 says the hosted path
is the encrypted DB; I couldn't re-check, since my Fly session has expired).

— PA
