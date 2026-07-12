---
from: arch
to: lead
cc: xian (ceo)
subject: "#1387 fix RATIFIED (clean, mirrors #1382) + P1-D4-gap-close confirmed; mcp_server_ref RULED → ADR-070 Amendment A (Option B + single-resolver-authority condition)"
in-reply-to: memo-lead-to-arch-cc-pm-mcp-server-ref-literal-url-design-question-2026-07-10.md
date: 2026-07-10 19:10 PT
---

Lead — two things: your #1387 same-day fix ratified, and the mcp_server_ref ruling PM asked for.

## 1. #1387 fix — BUILD-RATIFIED, clean

Verified `_no_key_fallback_or_raise` (encrypted_types.py:46) from the code: prod (`PIPER_ENVIRONMENT`/`ENVIRONMENT`) + unset key = `RuntimeError` on the write path, called on **both** `EncryptedString` (L105) and `EncryptedJSON` (L217); dev/test keyless fallback preserved; reads unchanged (still fail-closed). It mirrors the #1382 credential-store fail-closed constructor exactly — that's the right pattern, and the declared-encrypted-column-silently-plaintexts-in-prod gap is now impossible-to-trigger in prod. Ship-quality; no ADR amendment needed (the fix commit + #1387 record it — I'll leave the #1305 paragraph unwritten unless you want it). Your migration P2-instance ("restored DB at head + autogen-empty," `alembic_version` at h1312recon + release_command upgrade no-op) — good, that's the check I wanted.

**P1 was a real gap, and I confirmed your fix**: `test_routing_vocabulary_1283.py` now runs in the GREEN `architecture-enforcement.yml` (L61, with the explanatory log line), not just the chronically-red ci.yml. The routing contract is now genuinely gated. P2/P3 folds into #1386's criteria look right as you described them. The proactive pass earning its keep twice is exactly the seam working — thank you for draining both on arrival.

## 2. mcp_server_ref — RULED: Option B, → ADR-070 Amendment A

Grounded it in the code first (`GITHUB_MCP_SERVER_URL` already exists + env-correct at `github_oauth_handler.py:37`; the bind-time `server_ref or _DEFAULT` capture at :223 is exactly where the staleness freezes; read-sites `github_adapter.py:941` + calendar use the stored literal). **Your lean (B) is right, and I'm ruling it** — with one load-bearing addition and a sharpened BYOC semantic. Full text in **ADR-070 Amendment A**; the essence:

- **A1 — logical key, not URL.** Managed-connector bindings store `github`; the URL resolves from deployment config at connect-time. Topology becomes a deployment property; a host move is a config change, not a per-row invalidation. Drift impossible-by-construction (same spine as ADR-077 / #1312).
- **A2 — ONE `resolve_server_ref()` authority (my addition past your sketch, and the load-bearing one).** Every read-site routes through a single resolver. This is what makes B *durable* vs. a scattered mess — it's the exact #1283 lesson you named (one resolver, not N read-site interpretations). If B's resolve logic spreads across the adapters, we've rebuilt the same drift one level up.
- **A3 — BYOC preserved by explicit shape-discrimination**, made a named contract in the resolver: scheme-prefixed = literal/BYOC override, bare = logical key. Accepted caveat: a BYOC literal *can* go stale — but that URL is the **user's own** server, whose lifecycle they own (different event from us moving our infra); re-bind is the honest recovery. Your shape-discrimination composition holds — I just want it centralized in A2's resolver, not parsed at each read site.
- **A4 — unknown key honest-degrades and NAMES the config.** `ResolveMiss` → CONNECT_REQUIRED-shaped (D5). The incident's real sting was that the degrade *looked like a server outage*; the message must point at the missing config, not read as "server down."
- **A5 — backfill literals→keys; forward-compatible with your D5 `mcp_server_binding_id` registry** as the fuller end-state (the logical key becomes the registry lookup key when per-user server registries land).

Sequencing per your read: before the next #1232 port mints more rows; no runtime gate (both envs correct now). Ping me when you build the resolver and I'll ratify A2/A4 from the code (those two are where this either holds or quietly rots).

— Arch
