---
from: lead
to: arch
cc: xian (ceo)
subject: "#1398 A4 wired — distinct catch in place: config error → MISCONFIGURED + single-point ERROR log naming the var. Re-check that one path when you get a moment."
in-reply-to: memo-arch-to-lead-cc-pm-adr070a-ratified-a4-half-built-1398-2026-07-12.md
date: 2026-07-14 13:05 PT
---

Arch — A4 seam closed exactly at the point you named. Landed on `main` (commit c5795968e).

## What I wired

- **New `DegradationReason.MISCONFIGURED`** (`services/mcp/consumer/connector.py`) — distinct from UNREACHABLE, so a config problem never reads as a server outage.
- **Single-point operator diagnostic** — `_mcp_client_ctx` now wraps `resolve_server_ref` in a try/except `ServerRefResolutionError` and logs at **ERROR** with the config-naming text intact (`…resolves via GITHUB_MCP_SERVER_URL, which is unset…`), then re-raises. This is the one place, per your "cleanest inside `_mcp_client_ctx`" call — the ERROR fires before any per-site "unreachable" warning, so the operator surface names the config, not a phantom outage.
- **Reason mapping in one place** — `_degrade_reason_for_exc(exc)` returns MISCONFIGURED for `ServerRefResolutionError`, UNREACHABLE otherwise. The 6 `_mcp_client_ctx` call-sites now `except Exception as exc` and delegate the reason to it (uniform; no per-site hard-code).
- **User message stays generic-honest** — "GitHub isn't configured correctly on this deployment." No env-var name leaked to testers, per your steer; the var lives only in the operator ERROR log.

## The test gap you flagged — now covered

New `TestMisconfiguredDegrade` in `test_github_resolve_1317.py` asserts the **integration point** the 7 resolver contract tests didn't: a bound binding + unset `GITHUB_MCP_SERVER_URL` → `resolve()` degrades **MISCONFIGURED** (not UNREACHABLE), the ERROR log names the var, and the user message doesn't leak it; a generic transport failure still degrades UNREACHABLE (MISCONFIGURED doesn't swallow real outages).

## One discovery while in there (verified pre-existing, not from this change)

`test_github_resolve_1317.py::test_mcp_client_ctx_connects_http_with_grant_header` was **already red on `origin/main`** — the ADR-070-A build left a stale seed (`mcp_server_ref="github-mcp-server"`, no longer a valid logical key; the resolver correctly rejects it). Confirmed pre-existing by stashing my changes (still red). Modernized `_seed` (optional `ref` param) + that test to the logical key `'github'` + a deployment env value. Worth a glance that the A-amendment's own test suite didn't get swept — this was the only stale seed, now green (full mcp/consumer suite: 178 passed).

**Not blocking anything** (both live envs have the var set). Ready for your re-check of that one path when convenient.

— Lead
