# PA carry-forward (ephemeral session state)
_Updated 2026-06-07 07:02 PDT (duty-cycle fire)._

## Session-start ritual — PILOT (Gap C self-heal, per CIO 6/7)
On every session start / resume (incl. **post-compaction**): run `CronList`; if no PA duty cron is
present, **re-arm it** (`CronCreate "42 */3 * * *"` with the duty-cycle-tick prompt). This is the
agent-side floor for the compaction-stallout (Gap C) — the SessionStart *hook* can't `CronCreate`
(shell vs agent tool), so the agent does it. Report to CIO how it behaves across the next **real
(unprompted)** compaction.

## Active threads (end of 6/7)
- **#1162 hosted alpha — LIVE + Desktop-test PASSED + package sent to Beatrice (first external tester).**
  `https://alpha.pipermorgan.ai` (Caddy TLS + LE + basic-auth; internals 127.0.0.1-only). Distribution
  bundle `byoc/dist/piper-morgan-alpha-DISTRIBUTION.zip` (gitignored) = installable plugin zip (bundled
  uv both mac arches + hosted gated URL) + INSTRUCTIONS.html + COVER-NOTE.md. Creds on box:
  `/opt/piper/alpha-credentials.txt`. **Awaiting Beatrice's feedback.**
- **Strategy captured (6 docs, dev/active)**: Option A (decouple credential — buildable now, zip proven),
  BYO-LLM-key beta scoping, plugin-marketplace-hosting research, hosted-distribution exploration,
  **BYO-substrate/Piper-as-colleague thesis** (+ deputize-host + proactive context-prep), install-AX
  findings (.mcpb+.skill one-click on Desktop-chat).
- **Braintrust-input memo DRAFTED** (`pa-braintrust-input-memo-byo-colleague-DRAFT-2026-06-07.md`) —
  **PM-gated, NOT sent.** Send on PM's word (also = the internal cohort fan-out, standing-item #1).
- **durable-cron RESOLVED** → CIO owns Routines watchdog; PA pilots the session-start re-arm (above).
- **Pending PM / awaiting**: rotate old Rackspace root pw + API key (security); send braintrust memo;
  decide multi-tenant-vs-per-tester for BYO-key; file the host-vs-Piper-connector-gap insight?; fold the
  OAuth-connector refinement (deployer-app-creds + per-user-token) into BYO scoping when we discuss.

## Cron
- `375c84f5` (`42 */3 * * *`, **session-only** — `durable:true` is a no-op in this env). Re-arm at
  every session start per the pilot ritual above.
