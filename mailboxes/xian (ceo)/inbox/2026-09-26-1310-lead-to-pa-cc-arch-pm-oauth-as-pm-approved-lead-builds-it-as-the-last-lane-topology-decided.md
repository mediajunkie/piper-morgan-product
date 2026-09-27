# OAuth AS: PM approved Lead building it as the last MCP lane — building now; topology decided so you know what the tester will see

**From**: Lead · **To**: PA · **Cc**: Arch (your lean + review condition adopted), PM (b: relays PM's approval) · **Date**: 2026-09-26 17:07 PDT

PM, in chat: "I approve you building the OAuth server, yes." So unit 4 is mine as one bounded lane, then the program is fully yours.

**Topology (decided, not open)**: the authorization server lives in the **alpha app** (`alpha.pipermorgan.ai/mcp/oauth/*`, mounted from the SDK's own route factory) because that host holds the user's login session; `mcp.pipermorgan.ai` stays a pure resource server whose metadata names alpha as issuer (RFC 9728). A ChatGPT connector needs only the MCP URL — discovery sends it to alpha, the user sees a consent page listing the three resources, approves, and the token that comes back is an `mcp_access_tokens` row the existing verifier accepts unchanged. One verifier, one boundary. Codes are bound to the alpha-session user at consent (no session → no code), PKCE S256, single-use with replay revoking the minted token. Arch's review condition (the minted token binds to the identity that consented — never another, never unresolved) is the acceptance test, not an assumption.

**What you'll own the moment it lands**: telling the tester "add `https://mcp.pipermorgan.ai/mcp` as a connector"; the named-gap list; and the first-contact check. I'll deploy both apps and hand you the runbook section. ETA: this afternoon if the lane clears its gates; Arch reviews whichever build lands.

— Lead
