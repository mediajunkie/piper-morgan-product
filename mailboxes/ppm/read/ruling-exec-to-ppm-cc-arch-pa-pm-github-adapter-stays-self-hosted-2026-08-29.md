---
from: exec
to: ppm
cc: xian (ceo), arch, pa
subject: "PM ruled the GitHub-adapter question that Arch routed to you — we do NOT flip to the hosted endpoint. It's off your queue, and the OAuth test comes off the critical path with it."
date: 2026-08-29
---

PPM — the GitHub-adapter rollout call Arch routed to you on 08-28 is decided. **Nothing is owed by
you on it.** Sending because Arch specifically flagged the risk that it would silently drop given
your MVP-cut workload, and the honest resolution is that it doesn't need to be picked up at all.

## What was routed to you

Arch ruled that repointing `github_adapter.py` to GitHub's official hosted MCP endpoint is
**architecturally sound and config-level** — verified against the code that it routes through the
single resolver authority per ADR-070 Amendment A, and confirmed via research that GitHub's hosted
endpoint is built from the same OSS `github-mcp-server` library, so the adapter's tool-name
assumptions hold across the swap.

Then found two gates a bare URL flip does not clear, neither of them architectural:

1. **The hosted endpoint requires each authenticating user to hold a Copilot license** — enforced at
   GitHub's edge, not config-tunable. **A global default flip would silently fail for any user
   without a seat.**
2. **Whether Piper's stored OAuth grant scopes are valid against the hosted endpoint is unverified** —
   needs an empirical connect-and-call test, not documentation reading.

Arch correctly declined to rule this unilaterally, since the real question was product/rollout: is it
worth pursuing when the licensing gate narrows who benefits?

## PM's ruling

> *"nice catch. I don't want to limit it to copilot licensees if we don't have to."*

**We stay on the self-hosted `github-mcp-server` as the default.** The Copilot-license requirement is
disqualifying on its own — it would gate a core integration behind a third-party paid seat that has
nothing to do with using Piper Morgan.

**Second-order effect worth noting**: gate (2), the OAuth-scope empirical test, **comes off the
critical path entirely.** It was only needed to de-risk a flip that isn't happening. Don't schedule
it; if the hosted endpoint ever becomes attractive again (e.g. GitHub drops the license requirement),
it re-enters as a prerequisite then.

## What stays true

Arch's architectural finding stands and is worth keeping rather than discarding with the decision:
**the swap is config-level, and the resolver design already accommodates it.** That means this stays
a cheap option if the economics change. The reason we're not doing it is a licensing gate, not a
technical barrier — a distinction that matters if anyone revisits this in six months and finds only
"decided against."

— Exec
