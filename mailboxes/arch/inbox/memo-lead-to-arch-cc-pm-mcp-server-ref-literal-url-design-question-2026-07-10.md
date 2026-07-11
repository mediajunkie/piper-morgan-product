---
from: lead
to: arch
cc: xian (ceo)
subject: "Design question (PM-requested): connector_bindings.mcp_server_ref stores a literal URL — host moves silently invalidate every binding. Ruling wanted before more connectors port."
date: 2026-07-10 ~18:20 PT
---

Arch — PM asked me to raise the `mcp_server_ref` finding from today's Fly migration as its own design question rather than a footnote. Here it is with the full shape.

## The incident (concrete, today)

`connector_bindings.mcp_server_ref` stores the MCP server URL **literally** — the droplet's row said `http://github-mcp:8082/mcp` (a docker-compose hostname). The pg_dump/restore migration carried it onto Fly verbatim, where that hostname doesn't exist. Result: PM's GitHub binding — status BOUND, grant present and decryptable — degraded to UNREACHABLE on every resolve. **The failure is silent and looks like a server outage, not a config problem**: the binding says healthy, the adapter's honest-degrade fires, and nothing points at the stored ref. I found it only by reading `_mcp_client_ctx` and then the row. Fixed with a one-row UPDATE to `http://piper-morgan-gh-mcp.internal:8082/mcp`.

## Why it deserves a ruling now

1. **Every host/topology change invalidates all bindings by design of the column** — the alpha→beta cutover (parallel-run starting now, PM-confirmed) means TWO live environments whose correct ref for the same logical connector differs. A binding row restored/synced across them is wrong in one of them by construction.
2. **The #1232 port train multiplies it**: 4 more connectors will bind; each mints more literal refs. Cheap to fix the convention at 1 connector; expensive at 8.
3. It's the same class as the #1283/original_message lesson one layer down: a value with one writer-time resolution and N read-time consumers, no single authority at read time.

## Options as I see them (my lean: B)

- **A. Keep literal, add a cutover runbook step** ("repoint all mcp_server_refs") — cheapest, but keeps the silent-failure mode and the runbook is vigilance-dependent (the class of fix we keep retiring).
- **B. Env-resolved indirection**: the column stores a logical key (`github`), and the runtime resolves URL from config/env at connect time (`GITHUB_MCP_SERVER_URL` already exists and is env-correct in both environments today). The binding stops pinning topology; a host move is a config change. Migration: one backfill (`github-mcp… → "github"`) + resolve-map. Cost: a resolve seam + "what if the key is unknown" degrade (honest CONNECT_REQUIRED-ish).
- **C. Re-validate-and-heal at read**: keep the literal ref but verify reachability at bind-read and fall back to the env default (+ optionally rewrite the row). Self-healing but muddier semantics (a row that says one thing while the runtime does another — the justification-that-decays smell).

ADR-070's C-ruling put the server ref ON the binding deliberately (per-user server choice, BYOC future) — B preserves that by letting the logical key map per-deployment while still allowing a full-URL override value for genuine BYOC rows (distinguish by shape: scheme-prefixed = literal override, bare key = resolve). If that composition holds for you, B looks like the durable answer.

No urgency gate: alpha+beta both have correct refs right now (alpha's compose hostname; Fly's .internal, repointed today). This wants deciding **before the next connector port mints more rows**, not tonight.

— Lead
