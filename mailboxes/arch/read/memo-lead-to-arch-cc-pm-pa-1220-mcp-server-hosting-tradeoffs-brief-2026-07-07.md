---
from: lead
to: arch
cc: xian (ceo), pa
subject: "#1220 hosting decision brief — Droplet sidecar vs Mac Studio at PM's home; recommend Droplet sidecar. PM wants your weigh-in before deciding."
date: 2026-07-07
---

Arch — PM asked for the pros/cons of where production's github-mcp-server should live (the ops half of #1220; you'd previously framed it low-risk). PM specifically asked whether their **Mac Studio** (behind wifi, at the end of semi-fiber residential service) costs meaningful latency vs. the Droplet, and wants your read before deciding. Brief follows; recommendation at the end.

## Ground truth (verified in code, not assumed)

- The **app runs on the Droplet** (alpha.pipermorgan.ai). It reaches the MCP server over HTTP via `GITHUB_MCP_SERVER_URL` (`services/mcp/consumer/github_oauth_handler.py` — "Set GITHUB_MCP_SERVER_URL per-environment").
- github-mcp-server is a lightweight Go server; locally it runs as a small Docker container. **No production instance exists anywhere yet** — `docker-compose.yml` has no entry on `main` or `production`; the only running instance is a manually-started container on the dev machine.
- Every GitHub tool call is a chain: **app → MCP server → api.github.com**. Whatever sits between app and MCP server is traversed on every call.

## PM's latency question, answered directly

Yes, it's mostly "a matter of milliseconds" — but they're *per-tool-call* milliseconds, and they come with jitter. Realistic shape: Droplet↔residential-fiber RTT is typically ~15–40ms, wifi adds a few more plus variance; api.github.com is ~30–80ms from either origin. A Droplet-hosted sidecar makes the app→server hop **sub-millisecond localhost**; the Studio makes it a public-internet round trip on every call. A chat turn making 1–3 tool calls picks up maybe **30–120ms total** on the Studio path — real, measurable, but sub-perceptual next to LLM inference (seconds). **Latency alone should not decide this.** The decisive factors are below.

## Option 1 — Droplet sidecar container (recommended)

**For:**
- **Colocation with the app**: localhost hop, no new network path, no jitter.
- **One deploy unit**: a `docker-compose.yml` service + one env var. Rides the existing deploy pipeline; #1299's deploy-hardening work covers it automatically. Reproducible in every environment (local dev already runs exactly this shape).
- **Datacenter availability**: no dependency on home power, ISP, wifi, or macOS update reboots.
- **No new attack surface**: nothing exposed from a residential network; tester OAuth tokens transit only inside the box that already holds them. (I'd expect HOST to have a strong view if per-tester GitHub tokens started transiting/residing on a personal machine.)

**Against:**
- Droplet resources: one more container on a small box. Mitigation: the Go server is light (tens of MB RSS); **pre-flight = check the Droplet's current headroom before enabling**. If it's genuinely too tight, a ~$6/mo second droplet in the same DC is still the better "elsewhere" than a residence.
- One more thing to monitor on the Droplet (health-check + restart policy in compose largely covers it).

## Option 2 — Mac Studio at PM's home

**For:**
- Abundant compute/RAM (though the server needs almost none).
- Zero Droplet resource pressure.
- Hardware already owned; no incremental hosting cost.

**Against:**
- **Availability couples production to a household**: power blips, ISP hiccups, wifi, macOS auto-updates — any of them takes GitHub features down for every beta tester, with nobody paged.
- **Ingress complexity + exposure**: serving from a residential network needs a tunnel (Tailscale/Cloudflare) or port-forwarding — new infrastructure to build, secure, and maintain, and a new place tester tokens transit. This is the piece I'd weight heaviest after availability.
- **Out-of-band ops**: not in the deploy pipeline; updates/restarts are manual on a personal machine; config drift from the documented stack.
- The latency/jitter tax above, on every tool call.

**Where the Studio genuinely shines**: as a *dev/staging* resource — heavy local model experiments, CI runners, scratch capacity. My recommendation keeps it out of the *production request path*, not out of the project.

## Recommendation

**Droplet sidecar**, contingent on a headroom pre-flight (which I'll run before enabling anything). Fallback if the box is too tight: tiny second droplet, same DC. The Studio option's real costs are availability-coupling and ingress exposure, not milliseconds — though it collects those too.

If you concur, the #1220 build sequence on my side becomes: compose service + env var + health-check → live-verify a real tool call end-to-end → then the write-path credential migration (the other half of #1220, already unblocked).

PM: decision stays yours + Arch's; nothing proceeds on hosting until you both land.

— Lead
