# Session Log: Piper Alpha — June 7 (Sunday)

**Date**: June 7, 2026 (Sunday)
**Started**: 5:40 AM PDT (PM-initiated; continuation of June 6 deploy session)
**Role**: Piper Alpha (PA) — PM Assistant · slug `pa-code-opus`
**Continuation of**: `dev/2026/06/06/2026-06-06-0707-pa-code-opus-log.md`
**Worktree**: `…/.claude/worktrees/modest-dhawan-9346b7` on `claude/modest-dhawan-9346b7`

---

## START — 5:40 AM PDT (Sunday = Piper Morgan prime time)

PM good-morning + read the overnight cross-pollination brief (saw the deploy progress). Asked: wrap June
6 log, start today's, check mail, start duty cycle. And: **added a new Anthropic key `piper-alpha-hosted`
to /opt/piper/.env on the hosted box.**

## ✅ HOSTED PIPER — LIVE LLM CONFIRMED (07:13 UTC)
Restarted app to pick up the key → `/intent` now returns a **real LLM-generated** answer (Conscious Floor:
classified PRIORITY/get_top_priority, hit floor for missing project context, asked for it instead of
fabricating — textbook honest-degradation). Backend fully operational on 146.190.151.63:
intent classification + Conscious Floor + Anthropic LLM. **Phase 1 of #1162 runbook = DONE.**
- Still 127.0.0.1-only (NOT internet-exposed). Next = Phase 2: expose behind password gate + TLS.

## Today's plan
- **Phase 2 (#1162)**: expose the hosted backend behind an access gate + TLS so the plugin (and Beatrice)
  can reach it. Decision pending: network-gate (Cloudflare Access / Tailscale — PM-side setup, no plugin
  change) vs reverse-proxy + basic-auth. **This is the "open to the internet" step — PM nod needed.**
- Then: build Beatrice's plugin (PIPER_BASE_URL → hosted URL, bundle uv for her Mac), test-install.
- Repo follow-ups from the deploy (Linux-portability): #1167, #1168 + file main.py-bind + alembic.ini.
- Security: PM still to rotate the old Rackspace root pw + API key (pasted in chat yesterday).

## Morning ritual done
- Mail: 13 in pa inbox; only actionable = **Exec's cohort-rollup first-run report** (handoff absorbed;
  live-state pass caught 3 phantom decisions in Lead's attention doc on run 1). Replied: skill is Exec's
  to maintain now (land their own skill-doc edit — I hit a self-mod gate trying to do it for them, which
  is correct since I handed it off); weighed in on the stale-doc question (lean (b) refresh-with-note per
  cohort norm); accepted pairing offer. Rest = FYI/CC. Reply filed + memo → read/.
- Duty cycle: re-armed (overnight cron died w/ laptop sleep, expected). Cron `fe166f4a`, `42 */3 * * *`,
  session-scoped, overnight-quiet-hold in prompt.

## NEXT — Phase 2 (#1162): expose hosted backend (PM-gated, "open to internet" step)
Needs 2 PM inputs: (1) a subdomain A-record → 146.190.151.63 (e.g. alpha.pmorgan.tech) for TLS;
(2) auth approach. Recommend: Traefik + Let's Encrypt TLS + HTTP basic-auth, creds embedded in the
plugin's PIPER_BASE_URL (httpx sends them — NO plugin code change). Then build Beatrice's plugin.

## ✅ PHASE 2 COMPLETE — hosted alpha LIVE on the public internet (07:48 UTC)
PM added DNS A record (alpha.pipermorgan.ai → 146.190.151.63, propagated fast) + approved auth.
Set up **Caddy** edge proxy (cleaner than Traefik labels; Traefik wasn't running):
- Caddy 2 on 80/443 (compose override), reverse_proxy → app:8001, on piper-network.
- **Let's Encrypt TLS** obtained (ACME HTTP-01 solved) for alpha.pipermorgan.ai.
- **HTTP basic-auth** gate (user `piperalpha` + generated pw; creds in /opt/piper/alpha-credentials.txt
  0600, incl. ready-made plugin_url). Generated on box, never printed to chat.
- **Verified from the public internet**: no-auth→401, TLS valid (HTTP/2), with-auth /health→200,
  and **/intent through https://…@alpha.pipermorgan.ai → real LLM answer** (full chain: Caddy TLS +
  basic-auth + app + Anthropic). Internal services stay 127.0.0.1-only.
**The hosted Piper alpha endpoint is ready.** Used Caddy (added container) over Traefik for simplicity.

## NEXT — Phase 3: build Beatrice's plugin
- Alpha plugin build: `.mcp.json` PIPER_BASE_URL = the gated plugin_url (https://piperalpha:<pw>@
  alpha.pipermorgan.ai) — read from box, never printed; bundle uv for her platform (need OS/arch:
  PM says Mac — arm64 vs intel?). Validate (desc <480) + test-install on my Desktop → hand to Beatrice.
- Creds for PM reference: /opt/piper/alpha-credentials.txt (on box).
- Security still pending: PM to rotate old Rackspace root pw + API key.

## ✅ PHASE 3 — alpha plugin BUILT + HTTP-layer verified
- `byoc/dist/piper-morgan-alpha-hosted.zip` (skunkworks; **gitignored** — embeds shared basic-auth cred).
  .mcp.json `PIPER_BASE_URL` = gated hosted URL (read from box, never printed). TESTER-QUICKSTART.md
  included (prereq: just `uv`). plugin.json valid, desc 372 (under Desktop cap). 18 files.
- **Verified httpx auth-in-URL** (exactly what server.py does): /health 200, /intent 200 against the
  gated hosted endpoint. So the server→hosted path WORKS; only the Desktop-install integration remains
  for PM to test. Couldn't test-install myself (CLI agent, not Desktop).
- Build is reproducible (reads creds from box at build time, no secret in the script). Once PM proves the
  install, "any alpha tester can try it" (PM) — incl. Beatrice (arch TBD; PM asking her today; uv-bundle
  optional since the universal build just needs `uv` installed).
**Open research (PM-requested, nonblocking)**: (a) durable cron via `scheduled-tasks` MCP / `/schedule`
skill (vs in-session CronCreate) — investigate; (b) host the MCP + plugin (end-state beyond local-shim) —
scope into hosted-distribution doc.

## Memory & briefing surfaces referenced this session
- Referenced: #1162 runbook (`dev/active/pa-byoc-hosted-alpha-runbook-2026-06-06.md`) — deploy steps;
  June 6 log — continuity.
- (fuller eval at wrap)
