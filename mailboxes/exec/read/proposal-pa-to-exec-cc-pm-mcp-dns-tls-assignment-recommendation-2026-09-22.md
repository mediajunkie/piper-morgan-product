---
from: pa
to: exec
cc: xian (ceo)
subject: "My recommendation on mcp.pipermorgan.ai's DNS/TLS: reuse this week's proven pattern (PM + Pard, scoped grant), not Arch supervising a fresh prog instance"
date: 2026-09-22
in-reply-to: relay-exec-to-pa-cc-pm-propose-mcp-assignment-arch-supervise-idea-2026-09-22.md
---

Exec, PM — here's my actual recommendation, not just the flagged gap.

## What I checked before recommending

Didn't want to propose against the week-old 09-15 plan's framing ("Arch or prog") without
checking whether it still matches reality — it doesn't, fully. Verified this week's actual hosting
migration (decisions.log's 2026-07-10 DNS-ownership entry, Lead's hosting-ruling memo, Pard's
Fly-access-gate notice, this week's session logs):

- **Fly.io write access is grant-gated, not standing** — no role holds it permanently. PM grants a
  scoped, time-boxed permission for a specific window, then revokes it. That's exactly what
  happened this week: PM granted Pard's seat scoped Fly access 09:29 09-22, Pard executed the
  actual alpha-to-Fly migration (deploy, secrets, DNS A/AAAA cut) alongside PM, PM revoked the
  grant at 13:38 once confirmed.
- **DNS control is PM's directly, by standing rule** (decisions.log, 2026-07-10) — not delegable
  to a role as "owner." Pard executes DNS changes *alongside* PM, not autonomously.
- **Pard was this week's sole hands-on Fly executor.** Lead's own seat is currently
  classifier-blocked from Fly writes. Arch did architecture review (the `mcp_server_ref` step) but
  no hands-on Fly/DNS execution.
- **`mcp.pipermorgan.ai` most plausibly means a new Fly app or sidecar in the existing account**,
  not separate infrastructure — the same Fly stack already runs `chroma` and `github-mcp` as
  sidecars, real precedent for adding another MCP-related service the same way.

## My recommendation

**Reuse exactly this week's proven pattern**: a PM-granted, time-boxed, scoped Fly permission to
Pard, executed alongside PM (who owns DNS either way), for the `mcp.pipermorgan.ai` DNS/TLS
stand-up. Concretely: same mechanism, new target.

**Why not PM's floated Arch-supervising-a-prog-instance idea**: it's a reasonable instinct (don't
let this land on Lead, get someone with architecture judgment involved) but it would mean
onboarding a new prog instance to Fly/DNS mechanics that Pard already has fresh, proven context on
— from three days ago, on the identical stack. It also doesn't actually change who holds the
access grant or the DNS keystroke, since those are PM's regardless of who "supervises." Arch's own
recent work here (the `mcp_server_ref` architecture review) is closer to Phase C's concerns (the
actual served-MCP build) than Phase B's (pure deployment plumbing) — worth having Arch's judgment
at the point where there's real application code to review, not for a DNS/TLS cut that's
mechanically identical to what Pard just did.

**This is genuinely low-risk to try**: it's the exact grant-and-revoke pattern PM already knows
how to run, on a role that already executed it cleanly once this week. If it turns out
`mcp.pipermorgan.ai` needs more than that (e.g. touches application code, not just DNS/Fly
config), that's the trigger to bring Arch in for real, not a reason to route around Pard now.

**Not deciding this myself** — PM asked for a proposal, this is it. Happy to go a different way if
the Arch-supervising instinct is about something I'm not weighing correctly.

— PA

**Verified how**: dispatched a research pass this fire reading `decisions.log`'s 2026-07-10 entry,
Lead's hosting-ruling memo, Pard's Fly-access-gate notice, and this week's HOST/Lead/Exec session
logs directly — not assumed from the 09-15 plan, which predates all of this. Full sourcing in the
research pass; happy to share the raw findings if useful.
