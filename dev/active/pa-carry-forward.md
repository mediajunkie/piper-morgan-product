# PA carry-forward (ephemeral session state)
_Updated 2026-06-10 07:12 PDT (morning START fire — 6/9 closed, 6/10 log started)._

## Re-arm ritual — PILOT (Gap C partial mitigation, per CIO 6/7)
On **every turn the session gets** — session-start/resume, **each duty-cycle fire**, AND **sign-off** —
run `CronList`; if no PA duty cron, **re-arm it** (`CronCreate "42 6,9,12,15,18,21 * * *"` with the
duty-cycle-tick prompt — **WINDOWED expression, NOT the old `42 */3`**).

**⚠️ CRON EXPRESSION CHANGED 6/10 → windowed `42 6,9,12,15,18,21 * * *`** (live cron `56a2c4ee`).
PM-ratified (6/10): the deep-overnight dead zone ~midnight–4am has no fire at all — no overnight WATCH needed
"for us now" (a future all-night memo-sending agent isn't a thing yet). For the 3h cadence this drops exactly
the two midnight–4am no-op fires (old 00:42 + 03:42) at ZERO loss; keeps 06:42 START + 21:42 pre-hold check.
Came out of the cron-shape Day-7 memo to CIO (overnight fires = pure-cost no-ops). **Cohort-wide canonical
template change is CIO's lane** (PM+CIO doing the token-efficiency pass) — this is PA-lane adoption only. Agent-side re-arm only *reduces* the dark-window (it needs a live turn); the **Routines watchdog
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
- **Braintrust CONVERGED + CLOSED** (6/9–6/10). All 5 lenses + **Exec's cross-lens synthesis** captured into
  the thesis doc (§"CONVERGENCE CLOSE"); all 8 memos triaged → pa/read/. **Convergence: composition-not-
  greenfield at 3 altitudes; methodology is the MOST defensible thin-layer; HOST's three-party "guest" reframe
  = the load-bearing insight; M5→v1.1 is a moat-defensibility cut.** **PDR-006 RESOLVED → ADR-068 only** (PPM
  ruled, Arch withdrew PDR-006). Sequencing locked (M3 none / M4 ADR-068 drafts / M5 beta w/o colleague mode /
  v1.1 generalization). CIO catalog closed (m-34 extended; ship-routine-keep-loop = corollary, not minted).
  **3 OPEN PM QUESTIONS** (Exec→PM, cc braintrust — PA surfaces, doesn't decide): (1) loop-defensibility as an
  explicit M5 gate? (2) ratify ADR-068-only/no-PDR-006 → unblocks Arch's M4 drafting? (3) HOST "guest"
  one-liner as external narrative (Comms)? **PA posture: thesis fully converged; doc is the durable capture;
  next action is PM's; nothing for PA to push unprompted.**
- **BYO-key model DECIDED 6/9: multi-tenant, per-user keys** → **#1185** (beta build: wire LLM path to
  `user_api_keys` + per-user auth + Option A `/connect` captures the key). Alpha rides shared key meanwhile.
- **durable-cron**: CIO owns Routines watchdog ($70/mo PM-gated); PA pilots re-arm. **New 6/9 data**: cron
  store **non-deterministic across resumes — vanish AND reappear** (found a "dead" cron resurrected on
  resume + deduped). For next CIO touch.
- **Pending PM / awaiting**: the 3 braintrust open-questions above; rotate Rackspace creds (PM holding 6/9);
  Beatrice + a few NEW testers' feedback — **blocked till Wed-noon usage reset (TODAY)** (shared key hit usage
  limit; re-check / nudge after noon); file host-vs-Piper connector-gap insight?; fold OAuth-connector
  refinement when we discuss; **worktree stays modest-dhawan** until main-account migration (PM 6/9).
- **PM on other Anthropic account** until **Wed-noon usage reset (TODAY 6/10)** — testers unblock then.
- **Session-log discipline note (6/10)**: this continuous session ran 6/9 session-log-primary (no cycle log);
  the morning START self-healed 6/9's missing DAY-CLOSED (retroactive close: day-arc + memory-eval + sign-off
  + marker), then created the 6/10 log. Step-0 self-heal worked as designed.

## Cron
- `56a2c4ee` (**`42 6,9,12,15,18,21 * * *`** — WINDOWED, no midnight–4am fire; **session-only**, `durable:true`
  is a no-op in this env). Swapped from `78832b49`/`42 */3` at the 13:12 fire per PM's 6/10 ratification
  (overnight no-op-fire fix). Fires 06:42→21:42. Re-arm with the WINDOWED expr per the pilot ritual above.
