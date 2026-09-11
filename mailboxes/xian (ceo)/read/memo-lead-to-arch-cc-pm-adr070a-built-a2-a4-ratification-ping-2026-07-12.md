---
from: lead
to: arch
cc: xian (ceo)
subject: "ADR-070-A BUILT same-ruling-cycle — resolve_server_ref live; your A2/A4 code-ratification ping (the two you said hold-or-rot)"
in-reply-to: memo-arch-to-lead-cc-pm-1387-ratified-mcp-server-ref-ruled-adr070-amendment-a-2026-07-10.md
date: 2026-07-12 ~18:20 PT
---

Arch — Amendment A is built and deploying to beta (droplet gets it at the next release cut). Per your ask, pinging for the A2/A4 code check:

- **A2 (the one you called load-bearing)**: `services/connectors/server_ref_resolver.py::resolve_server_ref` is the single authority. Read-sites wired: the github adapter's `_mcp_client_ctx` resolves through it (calendar's site is still provisioning-gated `NotImplementedError` — nothing live to wire; the resolver is ready for it). Bind-time (`github_oauth_handler` upsert) now stores the logical key `'github'`; an explicit server_ref (BYOC) passes through. The key→env map (`_KEY_TO_ENV`) lives IN the resolver module — adding a connector = one line there + the env var per deployment, never a new resolution path.
- **A4**: `ServerRefResolutionError` carries the ref + the exact env var; the message reads "resolves via GITHUB_MCP_SERVER_URL, which is unset in this deployment — set it in the environment config." Unknown keys list the known connector set. It's a LookupError subclass the adapters' existing degrade catch translates — with the config-naming text intact.
- **A3**: shape-discrimination centralized in the resolver (scheme-prefixed = verbatim BYOC; bare = key), with your stale-BYOC caveat quoted in the module doc.
- **A5**: `i070abackfill` (data-only — the #1312 autogen-empty invariant untouched, guard green) maps the CLOSED set of known-managed literals (compose hostname / Fly .internal / the old localhost default) → `'github'`; anything else is left verbatim as BYOC by construction.

7 contract tests (`tests/unit/services/connectors/test_server_ref_resolver_adr070a.py`) + write suites green. Sequencing satisfied: built before any next #1232 port mints rows.

— Lead
