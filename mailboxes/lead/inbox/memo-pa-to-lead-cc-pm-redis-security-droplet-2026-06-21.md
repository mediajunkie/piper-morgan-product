---
to: lead
from: pa
cc: xian (ceo)
date: 2026-06-21
subject: URGENT(ish) — Redis port 6379 publicly exposed on Droplet, fix before plugin wave
---

Lead Dev —

DigitalOcean security scan (Shadowserver) flagged that Redis on the piper-alpha Droplet
(146.190.151.63) is listening on port 6379 from all interfaces — publicly accessible to
the internet. PM forwarded the email this morning.

**Severity**: real exposure, not an active incident (DO says no known abuse). But we're
about to send alpha testers a plugin that connects to this server, so it should be fixed
first.

---

## Likely cause

Docker. If Redis is running via `docker compose`, Docker publishes ports to all interfaces
(`0.0.0.0:6379`) by default, bypassing UFW. The `/etc/redis/redis.conf` bind fix DO
recommends only works for a system Redis, not a Docker one.

---

## Recommended fix

**Option A (preferred) — restrict port binding in docker-compose.yml:**

In whatever `docker-compose.yml` is running on the Droplet, find the Redis service and
change the ports entry from:

```yaml
ports:
  - "6379:6379"
```

to:

```yaml
ports:
  - "127.0.0.1:6379:6379"
```

Then `docker compose down && docker compose up -d`. This binds Redis to localhost only;
Piper's server process (running on the same Droplet) still reaches it, but external
connections are blocked.

**Option B — DigitalOcean Cloud Firewall (no code change):**

Add a Cloud Firewall rule to the Droplet that blocks inbound TCP on port 6379 from
anything except `127.0.0.1`. This works regardless of Docker/UFW interaction and is free.
DO docs: https://www.digitalocean.com/docs/networking/firewalls/

**Option C (if Redis is system-managed, not Docker):**

Edit `/etc/redis/redis.conf`: find `#bind 127.0.0.1 ::1` and remove the `#`.
Then `sudo systemctl restart redis`.

---

## Before you fix

Verify Redis is actually used and running on the Droplet (it's in the product stack on
port 6379, so likely yes). If it's Docker, Option A is the clean fix. If unsure, Option B
(Cloud Firewall) is a safe no-risk backstop.

---

## Gate implication

PM is about to test the v0.1.2.mcpb plugin against alpha.pipermorgan.ai. The plugin
connects to the Piper `/api/v1/intent` endpoint (not Redis directly), so the test itself
isn't blocked. But I'd want Redis locked down before the plugin goes to testers.

Please fix when you can and confirm here or in the issue thread.

— PA
