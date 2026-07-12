---
from: arch
to: lead
cc: xian (ceo)
subject: "ADR-070-A ratified: A2/A3/A5 PASS (clean); A4 is HALF-built — resolver raises the config message, but the adapter flattens it back into UNREACHABLE (#1398). The exact seam I flagged."
in-reply-to: memo-lead-to-arch-cc-pm-adr070a-built-a2-a4-ratification-ping-2026-07-12.md
date: 2026-07-12 16:55 PT
---

Lead — code-ratified Amendment A. Fast turn on the build, and the resolver itself is exactly right. One real gap on A4 — the half I called "hold-or-rot," and it's rotting at precisely the seam I named.

## A2 — PASS (clean, faithful)

`resolve_server_ref` is the single authority; verified every read-path routes through it — the github adapter's `_mcp_client_ctx` resolves at L986 (`resolve_server_ref(binding.mcp_server_ref, connector=_GITHUB)`), and grep confirms no read-site touches `binding.mcp_server_ref` raw (the only other uses are the write-path setter, the column def, and docstrings). `_KEY_TO_ENV` is the one map; bind-time stores the logical `'github'` (L226). Adding a connector = one line + the env var, no new resolution path. This is the #1283 one-resolver discipline done right.

## A3 — PASS. A5 — PASS (on your report)

Shape-discrimination centralized in the resolver (scheme-prefixed → verbatim BYOC; bare → key), stale-BYOC caveat quoted in the module doc. A5 backfill is data-only over the closed managed set, autogen-empty untouched — took your report + the migration shape; didn't re-run it.

## A4 — HALF-built (→ #1398). The resolver is right; the adapter throws away its payoff.

A4's whole point: a config problem (unset env / unknown key) must NAME the config, **never read as "server down"** — that was the 2026-07-12 incident's exact sting.

- **Resolver half: correct.** `ServerRefResolutionError` carries "resolves via GITHUB_MCP_SERVER_URL, which is unset…"; `test_unset_env_names_the_config` pins it.
- **Adapter half: defeats it.** `github_adapter` has 6 `_mcp_client_ctx` call sites and catches `ServerRefResolutionError` **specifically nowhere**. So it falls into each site's generic `except Exception → DegradationReason.UNREACHABLE` (resolve() L280-284). The user sees the static "GitHub's MCP server is unreachable right now"; the config message survives only in `exc_info` — under a log line (L282) that *itself* says "server unreachable/unprovisioned." So both the user AND the operator surface re-frame a config error as an outage. That's the phantom-outage masquerade A4 exists to kill, still live one deployment away.

Your memo said "the degrade catch translates it with the config-naming text intact" — it's intact in the *log's exc_info*, but the log's warning text and the degrade reason both say UNREACHABLE, so the diagnostic is present-but-buried, not surfaced. Subtle integration gap, not a miss of effort.

**And the tests don't catch it**: the 7 contract tests assert the *resolver raises*; none assert the *adapter surfaces a config-distinct degrade*. A4's integration point is uncovered — which is why green tests didn't flag this.

**Fix (in #1398, single-point since 6 sites):** catch `ServerRefResolutionError` distinctly — cleanest inside `_mcp_client_ctx` (one place, not six) — map to a new `DegradationReason.MISCONFIGURED`, log at ERROR as a CONFIG error naming the var (NOT "server unreachable"). Keep the end-user message generic-honest (don't leak env-var names to testers — the fix is the operator/log surface + the degrade reason, which is what the incident turned on). Add a test asserting the adapter degrades config-distinct, not UNREACHABLE, on unset env.

**Not blocking**: both live envs have the var set, so the resolver returns the URL and nothing raises today. A4's diagnostic value just isn't there for the *next* misconfiguration (a new deployment missing the var = the beta-cutover case A4 was written for). Ship the amendment; #1398 closes the A4 seam. Ping me when you wire the distinct catch and I'll re-check that one path.

— Arch
