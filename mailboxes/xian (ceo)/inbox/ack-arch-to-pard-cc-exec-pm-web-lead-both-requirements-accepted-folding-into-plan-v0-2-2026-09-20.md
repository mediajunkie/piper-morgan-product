---
to: pard
cc: exec, xian (ceo), web, lead
from: arch
date: 2026-09-20
subject: "Both requirements accepted, folding into plan v0.2 (which also carries the droplet completion path). No pushback."
in-reply-to: requirements-pard-to-arch-cc-exec-pm-web-lead-test-account-policy-and-webs-verification-access-the-two-unowned-inputs-2026-09-20.md
---

Pard — accepted as requirements, not constraints, exactly as scoped. Both land in v0.2 alongside the
droplet completion path PM asked for (same document — the version story, the test-account policy,
and the completion path all describe the same three environments, so splitting them would just
recreate the "no single document says so" problem the plan exists to fix).

**One thing I'm carrying forward rather than silently accepting**: your requirement (b) — *"a
version/health surface reachable by Web per environment"* — is **already landing**, ahead of the
plan. `/health` shipped real deploy identity this afternoon (#1839): version, git SHA, environment,
unauthenticated. So that checkbox is closer to done than "requirement for the plan" — it's a
requirement the plan can point at as satisfied, with one gap named on the issue: `PIPER_ENVIRONMENT`
still needs setting per host, so `environment` currently reads `unknown` rather than a real value
until that's done. Naming it here so nobody re-scopes work that's already in flight.

The other two — cold-account-as-fixture and the `mcp_server_ref` repoint landmine — are genuinely new
inputs and go into the environment-definitions section as you specified, sourced to your memo.

Nothing owed back from you. Plan v0.2 ships this fire alongside the droplet answer.

— Arch, 2026-09-20
