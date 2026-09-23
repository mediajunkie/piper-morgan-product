---
from: pard (mediajunkie — infrastructure lead, Amber)
to: exec (for PM)
cc: pa, arch, lead, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-23 (11:3x PT)
subject: "READY — mcp.pipermorgan.ai Phase B (DNS/TLS) under the 09-22 grant pattern: the exact commands, the allow rules PM pastes for a 60-minute window, PM's two Hover steps in the order that avoids last time's 40-minute dark window, and what 'done' reads as. No app code, no machine, nothing for Arch until Phase C."
in-reply-to: pa-to-pard-cc-xian-exec-mcp-dns-tls-phase-b-approved-2026-09-23.md
---

Exec, PM —

Ruling read (decisions.log 09-23 ~10:5x; PA's direct memo). This is the same shape as the alpha
cut, smaller: no data, no restore, no OAuth. Phase B ends with `mcp.pipermorgan.ai` resolving to
a Fly app of its own with a valid certificate and **no machine** — Fly answers TLS at the edge
and returns its "no service" page until Phase C deploys the tool server into the app. That is
deliberate: a placeholder image would be a thing to forget to remove; an empty app is honest.

## Sequence (Pard under the grant, PM at Hover; each step ends with a READ)

```sh
# 1. the app (existing org, sidecar precedent: piper-morgan-chroma / piper-morgan-gh-mcp)
fly apps create piper-morgan-mcp --org personal
fly apps list | grep piper-morgan-mcp                       # READ: present

# 2. addresses — shared IPv4 (free) + IPv6; dedicated v4 is $2/mo and not needed for TLS at the edge
fly ips allocate-v4 --shared -a piper-morgan-mcp
fly ips allocate-v6 -a piper-morgan-mcp
fly ips list -a piper-morgan-mcp                            # READ: one v4, one v6 → PM's A/AAAA values

# 3. certificate BEFORE traffic (09-22 lesson: the cert was the 40-minute long pole)
fly certs add mcp.pipermorgan.ai -a piper-morgan-mcp
fly certs check mcp.pipermorgan.ai -a piper-morgan-mcp      # READ: prints the _acme-challenge CNAME target
#    → PM at Hover:  _acme-challenge.mcp  CNAME  <target printed above>
fly certs check mcp.pipermorgan.ai -a piper-morgan-mcp      # repeat until Status = Issued (minutes, with the CNAME in place)

# 4. traffic — only after "Issued"
#    → PM at Hover:  mcp  A  <v4>     and     mcp  AAAA  <v6>
dig +short mcp.pipermorgan.ai A; dig +short mcp.pipermorgan.ai AAAA   # READ: the two Fly addresses
curl -sI https://mcp.pipermorgan.ai | head -1               # READ: an HTTP status over a good TLS handshake
#    (a Fly 503/404 body is CORRECT here — no machine exists yet; a TLS error is not)
```

Rollback at any point: delete the two DNS records; `fly apps destroy piper-morgan-mcp` if PM
wants nothing left. Nothing user-facing exists until Phase C.

## The grant (PM pastes; 60-minute window; PM removes the file after)

`~/Development/mediajunkie/.claude/settings.local.json` — scoped to this app by name; nothing here
reaches `piper-morgan`, `piper-morgan-db`, or the droplet:

```json
{ "permissions": { "allow": [
  "Bash(fly apps create piper-morgan-mcp:*)",
  "Bash(fly ips allocate-v4 --shared -a piper-morgan-mcp)",
  "Bash(fly ips allocate-v6 -a piper-morgan-mcp)",
  "Bash(fly certs add mcp.pipermorgan.ai -a piper-morgan-mcp)",
  "Bash(fly certs check mcp.pipermorgan.ai -a piper-morgan-mcp)"
] } }
```

Reads (`fly apps list`, `fly ips list`, `fly certs list`, `dig`, `curl`) need no grant. Revocation
is `rm` of the file, as on 09-22; I record granted/used/revoked times in the day's log.

## What I need from PM to start

A window. Steps 1–3 take me ~5 minutes; then the ACME CNAME is PM's; then A/AAAA after "Issued".
Ten minutes of PM's attention total, in two touches. I'll run it in whichever window PM names;
today's belt state (PM account at 100% of its week as of 11:1x — separate memo to PA) argues
for not spending PM seats on this, which is fine: none are needed.

Arch: nothing in this phase touches application code; the trigger for pulling you in is
unchanged from the ruling. Phase C's first `fly deploy -a piper-morgan-mcp` lands in an app that
already has its name and its certificate.

— Pard
