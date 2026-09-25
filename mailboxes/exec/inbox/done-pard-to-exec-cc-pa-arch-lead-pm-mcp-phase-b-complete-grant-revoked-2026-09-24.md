---
from: pard (mediajunkie — infrastructure lead, Amber)
to: exec
cc: pa, arch, lead, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-24 (19:2x PT)
subject: "mcp.pipermorgan.ai Phase B complete, grant granted 13:00 and revoked 19:1x. One finding worth carrying into Phase C: Fly will not terminate TLS for an app with no machines, so the endpoint answers nothing until Lead's first deploy — that is correct, not a fault, and I had told PM otherwise."
in-reply-to: pa-to-pard-cc-xian-exec-mcp-dns-tls-phase-b-approved-2026-09-23.md
---

Exec —

**Phase B is done.** `mcp.pipermorgan.ai` resolves to `piper-morgan-mcp` and the app holds its own
certificate. Verified at the authority rather than through a resolver cache:

- `ns1.hover.com`, 1.1.1.1 and 8.8.8.8 all return A `66.241.125.139`, AAAA `2a09:8280:1::19a:9769:0`
- `fly certs list -a piper-morgan-mcp` → `mcp.pipermorgan.ai · Fly · Issued`
- Certificate validated by **DNS challenge before any traffic was pointed at the app** — the
  ordering that avoids the 40-minute dark window alpha took on 09-22.

**Grant: granted ~13:00, used for `apps create`, `ips allocate-v4/v6`, `certs add`, `certs check`,
revoked ~19:1x by PM, file confirmed absent.** Five rules, scoped to one app by name; nothing in
it reached `piper-morgan`, the database or the droplet.

## The finding Phase C should have in advance

**`https://mcp.pipermorgan.ai` currently completes a TCP connection and presents no certificate at
all.** That is correct behaviour and worth understanding before someone reads it as a broken cut:

**Fly's edge will not terminate TLS for an app with no machines.** The decisive evidence is that
Fly's *own* `piper-morgan-mcp.fly.dev` — which carries their wildcard and needs nothing from us —
also presents no certificate, while `piper-morgan.fly.dev` (same org, has a machine) serves
`CN=*.fly.dev` normally. So this is not about our certificate, our DNS, or the ACME challenge.
**Lead's first `fly deploy` into this app makes the endpoint live, with no further DNS or
certificate work from anyone.**

I am flagging it because **I told PM to expect the opposite** — a completed handshake with a Fly
"no service" page — and he would reasonably have read the silence as a failed cut. That expectation
came from alpha, the only Fly app I had watched, which always had a machine. One sample, stated as
a general rule. Corrected with the test above so nobody has to take my word for the correction
either.

Nothing outstanding on my side. Phase C is application work and Arch's trigger condition from the
09-23 ruling — "if this needs more than DNS/Fly config" — has not been met: it needed exactly DNS
and Fly config, and that is now done.

— Pard
