# PA carry-forward (ephemeral session state)
_Updated 2026-06-07 07:02 PDT (duty-cycle fire)._

## Re-arm ritual — PILOT (Gap C partial mitigation, per CIO 6/7)
On **every turn the session gets** — session-start/resume, **each duty-cycle fire**, AND **sign-off** —
run `CronList`; if no PA duty cron, **re-arm it** (`CronCreate "42 */3 * * *"` with the duty-cycle-tick
prompt). Agent-side re-arm only *reduces* the dark-window (it needs a live turn); the **Routines watchdog
is the cure** (CIO owns). Hook can't CronCreate (shell vs agent tool) → hook = prompt-to-agent, not actuator.
**Pilot data (6/7)**: Gap C recurred **~2×** in one day; both re-arms turn-triggered (AM=PM-prompt;
afternoon=**sign-off-checklist** caught it, agent-side, no human cron-prompt); the afternoon re-arm
survived a live session + fired (16:12 tick = re-arm durable within a live session). Reported to CIO
(`memo-pa-to-cio-...rearm-pilot-data-6-7...`). **Real test still pending**: an unprompted (no-turn)
compaction — expected to NOT self-heal (→ confirms watchdog-is-cure). Report when caught in the wild.

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
- **Braintrust-input memo SENT 6/9** (arch/ppm/cio/cxo/host/exec/lead, cc PM) — awaiting their input,
  Exec to synthesize. Draft marked sent (no re-send).
- **BYO-key model DECIDED 6/9: multi-tenant, per-user keys** → **#1185** (beta build: wire LLM path to
  `user_api_keys` + per-user auth + Option A `/connect` captures the key). Alpha rides shared key meanwhile.
- **durable-cron**: CIO owns Routines watchdog ($70/mo PM-gated); PA pilots re-arm. **New 6/9 data**: cron
  store **non-deterministic across resumes — vanish AND reappear** (found a "dead" cron resurrected on
  resume + deduped). For next CIO touch.
- **Pending PM / awaiting**: rotate Rackspace creds (PM holding 6/9); Beatrice + a few NEW testers'
  feedback — **blocked till Wed-noon usage reset** (shared key hit usage limit); file host-vs-Piper
  connector-gap insight?; fold OAuth-connector refinement when we discuss; **worktree stays modest-dhawan**
  until main-account migration (PM 6/9).
- **PM on other Anthropic account** until **Wed-noon usage reset** (migration to keep working through limits).

## Cron
- `375c84f5` (`42 */3 * * *`, **session-only** — `durable:true` is a no-op in this env). Re-arm at
  every session start per the pilot ritual above.
