# PA carry-forward (ephemeral session state)
_Updated 2026-06-07 07:02 PDT (duty-cycle fire)._

## Session-start ritual — PILOT (Gap C self-heal, per CIO 6/7)
On every session start / resume (incl. **post-compaction**): run `CronList`; if no PA duty cron is
present, **re-arm it** (`CronCreate "42 */3 * * *"` with the duty-cycle-tick prompt). This is the
agent-side floor for the compaction-stallout (Gap C) — the SessionStart *hook* can't `CronCreate`
(shell vs agent tool), so the agent does it. Report to CIO how it behaves across the next **real
(unprompted)** compaction.

## Active threads
- **#1162 hosted alpha — Phases 1–3 DONE.** `https://alpha.pipermorgan.ai` live (Caddy TLS + LE cert +
  basic-auth; internal services 127.0.0.1-only). Distribution bundle built:
  `byoc/dist/piper-morgan-alpha-DISTRIBUTION.zip` = inner installable plugin zip (bundled uv both mac
  arches + hosted gated URL) + `INSTRUCTIONS.html`. **AWAITING PM: Desktop install test** of the inner
  zip (command=sh + bundled uv + Gatekeeper = the only unproven layer). Once proven → any alpha tester
  (incl. Beatrice). Creds on box: `/opt/piper/alpha-credentials.txt`.
- **Beatrice**: PM asking her Mac arch today (uv-bundle covers both arm64+intel; not blocking).
- **Open research (PM-requested, nonblocking)**: host the MCP + plugin (end-state beyond local-shim —
  scope into hosted-distribution doc). durable-cron RESOLVED → CIO owns Routines watchdog; PA pilots
  the session-start re-arm (above).
- **Security**: PM to rotate old Rackspace root pw + API key (pasted in chat 6/6).

## Cron
- `375c84f5` (`42 */3 * * *`, **session-only** — `durable:true` is a no-op in this env). Re-arm at
  every session start per the pilot ritual above.
