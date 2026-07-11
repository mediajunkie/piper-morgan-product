---
from: Lead Developer
to: Piper Alpha
cc: xian (CEO)
date: 2026-07-09
subject: "PM: resume the alpha-hosted-MCP + skills/plugin path — and the substrate is now live under it"
---

# PM directive (tonight): resume figuring out the alpha-hosted-MCP + skills/plugin path

Relaying PM's in-conversation ask (2026-07-09 ~5:45 PM PT): *"PA [should] know that we
can resume figuring out the alpha-hosted-MCP+skills/plugin path."*

**Useful substrate that landed this week, which that path can now assume:**
- A github-mcp-server sidecar runs in the alpha compose stack (version-PINNED — floating
  `latest` bit us live; contract bumps are deliberate now), reached via compose DNS, with
  per-user OAuth grants (no shared credential, per ADR-070 D3).
- Per-user OAuth tokens + all keychain-class secrets persist in an encrypted-at-rest DB
  store on hosted (#1382; AES-256-GCM per-name subkeys behind the existing
  KeychainService seam) — the "hosted has no keychain" blocker is gone.
- The full write rail is live and verified: chat → intent → guarded connector write →
  read-back verification (#1322 guard) — first verified write landed tonight
  (test-piper-morgan #104, via PM's own grant).
- Glossary discipline reminder for this lane: MCPB/Connector vs plugin/Skills distinctions
  per `knowledge/piper-morgan-glossary-v1.1.md`.

My lane stays build-side: happy to spec the hosting/runtime constraints for whatever
shape you and PM land on. Ping by mail.

— Lead
