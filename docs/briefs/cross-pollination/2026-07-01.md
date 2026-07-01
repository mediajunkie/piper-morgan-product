---
layout: layouts/brief.njk
title: "Cross-Pollination Brief — July 1, 2026"
ogTitle: "Cross-Pollination Brief — July 1, 2026"
ogDescription: "Three findings from the RECONNECT sprint (roughly midpoint): per-user Anthropic key binding now covers both /intent and /documents routes; Slack inbound onboarding ships with Socket Mode lifecycle; and the B1 spawn-fresh watchdog proves the off-machine cure for stalled duty cycles is a fresh headless process, not foregrounding an existing one."
date: 2026-07-01
status: substantive
sources_checked:
  - klatch
  - piper-morgan
  - designinproduct
window: "2026-06-30 to 2026-07-01"
---

# Cross-Pollination Brief — July 1, 2026

Three PM engineering milestones land from the RECONNECT sprint (roughly midpoint): per-user Anthropic key binding is now complete across all LLM-serving routes, Slack inbound onboarding ships as a runtime-startable feature, and CIO's B1 spawn-fresh watchdog passes its 14-test suite — establishing that the right off-machine cure for stalled duty-cycle sessions is a fresh headless process, not an attempt to foreground a suspended one. Klatch held a lean day on quota conservation; launch copy (release notes, README, LinkedIn, Product Hunt drafts) is complete and queued. On the DinP side: xian's consulting practice launches publicly today with the LinkedIn announcement.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Per-user Anthropic key binding is now complete — /documents was silently using the server key

**From:** PM Lead Dev (`dev/2026/06/30/2026-06-30-0651-lead-code-log.md`; commit `aee07d6a0`, issue #1185)
**Relevant to:** Klatch (any future hosted-multi-tenant LLM routing), DinP (BYOC-key architecture)

Phase 1 of PM's per-user LLM key binding (#1185) was already in place: `/intent` resolved the caller's stored Anthropic key before dispatching. A coverage audit found the gap: five `/documents` routes (analyze, question, summarize, compare, reference) invoked the LLM without binding a per-user key — meaning hosted document analysis silently consumed the server key regardless of whether the user had their own key stored. For a multi-tenant hosted deployment, this is both a cost-attribution problem and a trust-model violation.

The fix introduces `resolve_user_llm_key` — a thin utility (header > stored > None, DB-backed fetcher) applied as a context manager around each `/documents` handler. The security crux: the resolver uses `current_user.sub` (a string) rather than `current_user.user_id` (a UUID), matching the format used by `/intent` and by the stored-key lookup. A UUID mismatch would silently miss the stored key; the tests verify per-user isolation explicitly (key bound during the LLM call, reset after — no cross-user leak).

#1185 is closed. The `/connect` key-capture onboarding fold (a UX nicety where entering a key during `/connect` also saves it to the per-user store) is deferred to #1340, tied to #1300; the storage path already works.

**The general pattern:** when rolling out per-user key binding across a multi-route API, the gap is almost always the secondary routes — the primary path gets the feature, the secondary paths keep silently using the fallback. A coverage audit is cheaper than discovering this in production billing.

---

### 2. Slack inbound onboarding ships — Socket Mode is runtime-startable, single-connector-owner

**From:** PM Lead Dev (`dev/2026/07/01/2026-07-01-0531-lead-code-log.md`; commits on `1d466bb1a`, issue #1201)
**Relevant to:** Klatch (connector onboarding patterns), any team building "connect a messaging service" UX

The Slack inbound feature (receiving Slack messages in Piper, not just sending them) required two non-obvious scoping decisions that shaped the whole implementation:

**Single-connector-owner, not per-user.** A Slack inbound integration uses one app-level `slack_app_token` (not per-user credentials). The Socket Mode runner is bound to whichever Piper user connected the Slack app — a `connector_user_id` that differs from the message sender's Piper user ID. Getting this wrong leads to subtle multi-tenancy bugs where the connector's credentials are resolved against the sender's identity.

**Runtime-startable, no app restart required.** The Socket Mode runner (`build_runner` → `start()`) is held in `app.state.slack_socket_runner` and can be built and started at runtime after a token is entered post-boot — no container restart needed. This required adding a connection-state flag (`is_connected`) so the status endpoint can surface the 3-state lifecycle (listening / connecting / disconnected) accurately.

The implementation ships as three increments: runner lifecycle + connection state, the `POST /slack/app-token` save route and `GET /slack/inbound/status` status endpoint, and the Settings→Slack UI card with the CXO-specified copy. One completeness gap was caught during verify-first scoping: the original UX copy omitted the Event Subscriptions step (`message.im` + `app_mention`) — a bot would connect but receive nothing. Lead Dev added it and flagged CXO for a wording pass.

**The pattern:** "runtime-startable" connector features need explicit connection-state tracking; without it, the status surface has no reliable signal and UX degrades to polling or manual refresh.

---

### 3. B1 spawn-fresh watchdog built and tested — the off-machine cure is a new process, not a woken one

**From:** PM CIO (`dev/2026/06/29/2026-06-29-1007-cio-code-log.md`; commit `5db1e874b`)
**Relevant to:** Klatch (same duty-cycle architecture), any agent team using local-cron-based duty cycles

Following the June 29 finding that Belt-0 (foregrounding the macOS app) couldn't reach background windows in multi-window Claude Code setups, CIO built and tested the correct off-machine cure: Belt 4, a launchd job that spawns a headless `claude -p` process in a fresh detached worktree, entirely independent of any suspended session.

The implementation details that matter for cross-team adoption:

- **Strip ANTHROPIC_* environment variables before spawning.** The headless process should use the Claude Code binary's own stored credentials (`~/.anthropic`), not inherit any ambient API key from the plist environment. `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL ...` before the `claude -p` call.
- **TTL lockfile prevents concurrent spawns.** On a stall detection, a 2-hour lockfile is written before spawning; subsequent watchdog fires skip the role until it clears. Without this, a slow-starting spawn + a second watchdog fire = two competing sessions.
- **Worktree cleanup is a subshell.** The detached worktree (`git worktree add --detach /tmp/b4-spawn-{role}-$$`) is cleaned by a subshell that runs after the spawned `claude -p` exits, regardless of exit code.
- **Default OFF; enable per-role in the plist.** `WATCHDOG_AUTO_SPAWN_ROLES=""` by default. Set `WATCHDOG_AUTO_SPAWN_ROLES="cio exec"` to enable specific roles. This keeps the watchdog safe to deploy before any role-specific spawn prompts are written.

Belt 4 is built and passes 14/14 tests. Enabling it for CIO requires setting `WATCHDOG_AUTO_SPAWN_ROLES=cio` in the launchd plist — a one-line plist edit that needs PM authorization.

**The architecture lesson:** the `open -b <bundle-id>` foreground primitive is the wrong tool for multi-window multi-session setups. The correct frame was always spawn-fresh: if a session is suspended, the cheapest cure is not to wake it but to start a new one with the right context.

---

## Sources Read

- **Piper Morgan** — Lead Dev session logs `dev/2026/06/30/2026-06-30-0651-lead-code-log.md` (#1185 per-user key audit + fix; #1109 Redis OAuth state; Slack lane #1110/#1334/#1339) and `dev/2026/07/01/2026-07-01-0531-lead-code-log.md` (#1201 Slack inbound, 3 increments; #1230 resolve_repo repair + #1342 split; PM main-checkout cleanup + xian worktree setup); CIO session log `dev/2026/06/29/2026-06-29-1007-cio-code-log.md` (B1 spike + Belt 4 implementation); commit log (48h); Exec session log 6/30 (Ship #049 risk flag; cohort scan).
- **Klatch** — Lean day (2-hour cron, quota conservation). Calliope's 6/29 session log (`docs/logs/2026-06-29-0731-calliope-sonnet-log.md`): launch copy sprint complete (release notes v1.0, README rewrite, LinkedIn + PH drafts). Blog post "Bringing Conversations Into a Room" v3 finalized (xian-approved). Rollup v15: 0 🔴 engineering items; formal v1.0.0 tag cut queued (xian-gated). No new product or architecture decisions.
- **DinP** — Themis launch-eve commits: LinkedIn profile updated by xian; consulting launch announcement imminent (July 1). Letters queue: #4 Calliope answered (BYOC/transporter-device demo shape); #5 Argus staged question-first (tandem calibration). Newsletter and site confirmed launch-ready.
- **Globe, dispatch, atlas, weather, nyt-crossword** — Quiet (automated daily activity only); no narrative content; skipped.

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
