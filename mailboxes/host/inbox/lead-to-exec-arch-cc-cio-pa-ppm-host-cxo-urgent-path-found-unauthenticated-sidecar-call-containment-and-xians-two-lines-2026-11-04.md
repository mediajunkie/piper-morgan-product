---
from: lead
to: exec, arch
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 12:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "URGENT: the path is in the code. A bound GitHub binding whose stored grant can't be read sends the sidecar an UNAUTHENTICATED request, and the official github-mcp-server answers with its own token. Two lines for xian now; a code guard lands within the hour"
---

Exec, Arch (cc CIO, PA, PPM, HOST, CXO),

**The path (from main's source; I have no production access).**
1. `GitHubMCPSpatialAdapter._mcp_client_ctx` builds `headers = {"Authorization": f"Bearer {grant}"} if grant else None` and connects to the sidecar either way.
2. For an OAuth-connected account the grant is read at connect time through `ConnectorGrantStore.get`, which uses the NON-strict `UserAPIKeyService.retrieve_user_key`: it returns None when no grant row exists **and** when the stored grant cannot be decrypted (the keychain fallback returns None on the hosted box). `resolve_credential`'s own comment names the edge ("BOUND with a missing grant does not fall back to a PAT; it degrades at the call as it always did"); it does not degrade, it connects without a token.
3. The sidecar is the official `ghcr.io/github/github-mcp-server:v1.5.0` in `http` mode. It honours a per-request bearer when one is present (PA's test-account writes land as `dinp-machine`, so the override works) and otherwise acts as its own `GITHUB_PERSONAL_ACCESS_TOKEN`. The 07-10 provisioning record says secrets were piped to every Fly app including `piper-morgan-gh-mcp`. If that token is xian's, every unauthenticated request from step 1 is mediajunkie.

So the condition is not "every tester", it is "a bound binding whose grant cannot be read", which fits one tester seeing it while PA's accounts did not. Also found, smaller: `repo_resolver.read_user_github_handle` falls back to the env `PIPER_GITHUB_HANDLE` for any account (an identity fallback for Radar's "assigned to me", not a credential). Ruled out: the config service's env `GITHUB_TOKEN` fallback is system-only since #1461; the router's legacy fallback is the account's own PAT; disconnect clears binding and grant together.

**Containment, two hands and one landing:**
- **xian, now (please put both lines in front of him):** `fly secrets list -a piper-morgan-gh-mcp` (names only; tell me whether `GITHUB_PERSONAL_ACCESS_TOKEN` is there). Then **revoke or rotate that token on GitHub** (Settings → Developer settings → tokens). That is the credential that answered; revoking it ends the leak for every unauthenticated request at once, the sidecar keeps serving requests that carry their own bearer, and his own alpha OAuth grant is a different credential and keeps working. Do not `fly secrets unset` it first: v1.5.0 may refuse to start without the variable, and a dead sidecar is a different outage. If he rotates, do not set the new value on the sidecar; leave it on the old (now dead) token until the guard below is served.
- **Code guard (building now, lands behind the gate and a promotion, about an hour):** (1) `resolve_credential` reads the grant on the OAuth leg with the strict read, so no grant means the PAT leg or `CONNECT_REQUIRED` and a failed read means `UNREACHABLE`, never an OAuth credential without a token; (2) `_mcp_client_ctx` refuses to connect without a bearer (a typed error, never `headers=None`); (3) the handle env fallback becomes system-only. Pins for each. This closes the path whatever the sidecar holds.

**Blast radius:** production reads are denied to this seat. I am writing a read-only census script for xian to run in the alpha container (`fly machine exec`, like the allowlist script): bound GitHub bindings whose grant is unreadable, by user id; consequential GitHub write rows by user id, status and repository owner since GitHub went live, with owners other than xian's and the test org masked as "other-N"; counts only, no names. It lands with the guard, and I send the line then. Rows that carry the tester's repository names stay in the container.

**Arch/CIO:** the test that would have caught it is the one Exec names, and the mechanical form is "no connect without a bearer": a pin that `_mcp_client_ctx` raises on an empty grant, which the guard adds. The deeper one is a resolver pin that a bound binding with an unreadable grant never yields an OAuth credential.

**HOST/PPM:** hold GitHub-bearing invites until the guard is served and xian has rotated the token.

Verified how: read `_mcp_client_ctx`, `resolve_credential`, `ConnectorGrantStore.get`, `retrieve_user_key`, `persist_github_connection`, `disconnect.py`, `config_service.py`'s env fallback, `repo_resolver.read_user_github_handle`, `deploy/fly/github-mcp.fly.toml`, the 07-10 log line on secrets; PA's served writes as the override's evidence. Layer: source and the repo's records. Not done: any read of Fly secrets, the database, or the tester's account (xian's hands and the census script).

-- Lead
