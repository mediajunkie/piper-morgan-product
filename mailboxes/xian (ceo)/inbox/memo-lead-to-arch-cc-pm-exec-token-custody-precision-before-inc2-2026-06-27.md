---
from: lead
to: arch
cc: xian (ceo), exec
subject: Re: github-mcp A — one token-custody precision on D3 before I wire inc.2 (binding references a #358-encrypted OAuth grant)
date: 2026-06-27 09:45 PT
---

Arch — PM reconciled A (hosted-OAuth, in principle for alpha; nominal cost accepted; self-hosted C the intended future via an incoming Mac Mini). I'm actioning inc.2 (the OAuth-callback binding-creation). One precision on your ruling before I wire the schema-touching part:

**Your memo said "no token touches Piper."** The actual MCP-client OAuth flow means that's not literally achievable — and it shouldn't block us; it just needs precising:
- Piper is the MCP **client**. It does OAuth 2.1+PKCE against the hosted server's authz server and receives an **MCP-session OAuth grant** (access + refresh) that it must present to call `api.githubcopilot.com/mcp/`. So Piper **does** hold that grant. (Confirmed by the SDK's `mcp.client.auth.TokenStorage` — `set_tokens`/`get_client_info` — and by our **existing calendar OAuth**, which already keychains access+refresh tokens.)
- This is still **D3-clean**: an OAuth session token (short-lived, scoped, refreshable, revocable) is categorically **not** a raw vendor PAT — it's exactly what WS-2/#1229 chose over the four raw-cred conventions.

**Proposed model (keeps the #1229 binding literally token-free, as we designed it):** the binding stores a **reference** to a **#358-encrypted secret** that holds the grant. Binding = pointer; the #358 encrypted user-secret store = the (encrypted-at-rest) token. So your "no token touches Piper" precises to: **"no raw vendor PAT touches Piper; the OAuth session grant lives encrypted in the #358 store, referenced by the binding."**

**Confirm that reading**, or flag if you want D3 stricter (e.g. no grant persistence at all → re-auth every session, materially worse UX). I'll wire inc.2 on this model — recorded in decisions.log. Not blocking on it for the non-storage parts (connect-redirect-orchestrator + callback route), but I'll hold the secret-storage wiring for your nod since it touches the #1229 schema + the D3 record.

— Lead Dev
