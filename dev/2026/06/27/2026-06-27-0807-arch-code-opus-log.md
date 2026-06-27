# Session log — Architect (Chief Architect) — 2026-06-27

**Role**: Chief Architect (arch)
**Tool**: Claude Code — Opus 4.8 (`claude-opus-4-8`)
**Account**: DinP (xian@designinproduct.com)
**Worktree**: `.claude/worktrees/charming-borg-8957a7` (Option B ephemeral; continuous session from June 17)
**Branch**: `claude/charming-borg-8957a7` → `origin/main` via `git push origin HEAD:main`
**Mailbox method**: `scripts/mail-send.sh` (push-to-ref, #1259) — NOT the deprecated bridge dance.

---

## Saturday June 27 — START at 08:07 PT (PM-resumed; busy-signal stalls)

<!-- GAP-SINCE-LAST-FIRE: ~25h (June 26 fully stalled) -->

**Gap = June 26 fully stalled.** June 26 07:27 PM-resumed me to close June 25 + start June 26; I re-armed the cron + appended the June 25 close, then a **busy signal stalled the session before the START completed**. PM re-resumed 20:51 (June 25 close confirmed on origin) — stalled again before creating the June 26 log. Net: **June 26 had no completed START, no arch log, no cron fires** — a fully-stalled day. PM resumed again **June 27 08:07** ("get caught up"). This is the persistent liveness problem (CIO's model: re-arm fixes mode-1a, nothing local fixes mode-1b/the restart-kills-session-only-cron loop; off-machine trigger is the structural cure).

**Step-0 self-heal**: June 25 **CLOSED** ✓ (`DAY-CLOSED: 2026-06-25` on origin/main — #1312 fully ruled; retroactively closed June 26 morning). **June 26 = no log** (fully stalled, zero substantive arch work — not backfilled; documented here, consistent with the June 23/24 no-log stalled days).

**Cron**: `ff1df50a` (`27 6,9,12,15,18,21`) **survived in CronList** — no re-arm needed this START (it persisted across the busy-signal pause; note it's still session-only).

**Queue — caught up from the delta (41 commits behind):**
- **#1312 (personality-Base collapse) — RULED (both seams) + PM-APPROVED TIMING.** Exec relayed PM's approval: proceeds in its agreed slot **after the alpha bundle** (MCPB clean-machine + #1320/#1162), not a pull-forward. Fully specced (my (a)/UUID ruling + 6-step plan + invariant-lint skeleton). Lead won't touch until alpha clears. **Done my side.**
- **#1283 (routing-integrity / ADR-073) → M5 (PM call).** Deferred — ADR-073 is no longer imminent; I author it when #1283 activates at M5 + the probe lands. Standing, not active.
- **🟢 #1220 (real MCP transport) — Lead's Shape-B decision FLAGGED FOR PM/ARCH → my top catch-up action.** Lead found the official MCP SDK (`mcp==1.26.0`) is already a dep; chose **Shape B** (new SDK-based `MCPClient`, don't retrofit the live hand-rolled sim stack; legacy cutover = separate #1322). Explicitly surfaced for architectural weigh-in (transport-mechanism + legacy-cutover sequencing). **My action: read the gameplan → ratify/refine.**
- **WS-2 (#1229) CLOSED** by Lead 6/26 (`ConnectorBinding` storage foundation) — the "Arch WS-2 Q" Lead had planned resolved/closed on his side; nothing pending to me.
- **#1320/#1162 Caddy-gate = PM+Arch** (Lead's "gated, don't touch") — check whether a decision is pending from me.
- **CIO liveness-model memo** (consolidated my + Exec's datums into `duty-cycle-liveness-model-2026-06-25.md`) — ack pending.

**Plan this START**: ratify/refine #1220 Shape-B (the live arch deliverable) → ack CIO liveness → check the Caddy-gate → carry-forward refresh (#1283→M5, #1312 timing-approved, #1220 added). Draining.

---

### START drain (08:07–08:45) — #1220 Shape-B RATIFIED + CIO ack + caught up

Drained the catch-up in one wake:

**#1220 (real MCP transport) — Shape-B RATIFIED** (the live deliverable Lead flagged for Arch). Read the gameplan + grounded in the code (Verify-First). **Shape B is correct — clean GO, no Arch gate** (Lead's right that ADR-070 D5 already rules the protocol; conformant implementation): SDK-not-hand-roll (`mcp==1.26.0` present), textbook **m-40** (new MCPClient beside the live sim stack → migrate consumers → retire), zero-regression pure-addition, cutover tracked (#1322). **Arch altitude add** (the cutover sequencing Lead flagged): verified `query_router.py:60 enable_mcp_federation=True` + `MCPConsumerCore.simulation_mode` HARDCODED `True` (`client.py:93`, stale "replace with real MCP" POC comment) → **the MCP-federated query path serves simulated data today → #1322 is value-realizing, not optional polish** (it's what makes query routing real; a Pattern-073 deferred-replacement-comment). Ruled the sequencing (ports on real client now; #1322 = deliberate query_router cutover + sim-stack deletion gated on canonical-retest behavioral coverage) + named the **end-state invariant** (one transport; `simulation_mode` test-only + guarded-from-prod — make-drift-impossible family w/ #1312 single-Base + #1283 reachability). → memo to Lead cc PM/Exec/PA (`a182e9596`) + decisions.log (`b75cdf1dc`).

**CIO liveness ack** — concurred the resume-loop framing + **2 new datums**: (1) mode-1 has two flavors — 1a cron-object-dies-from-CronList (6/26+6/27; re-arm fixes) vs 1b survives-but-doesn't-fire-backgrounded (6/25; nothing-local fixes); (2) `CronCreate durable:true` still reports **session-only** → every restart kills the cron, re-arm only buys until the next restart → strongest evidence the waker must live *outside* the session. → memo to CIO cc PM (`5a70eca87`).

**Caught up**: #1283→M5 (PM call; ADR-073 M5-deferred); #1312 timing PM-approved (after-alpha; done my side); WS-2/#1229 closed by Lead; #1320/#1162 Caddy-gate = my 6/20 read stands, awaiting PM go (nothing pending from me). Carry-forward refreshed (`a097c0f58`). Both inbox memos → read/.

Cron `ff1df50a` armed (survived the pause). Light hold — queue awaiting Lead's RECONNECT ports (#1317) + the alpha bundle. Available; next fire 09:27 (if it fires).

---

### Fire — autonomous (08:17 tick) — github-mcp provisioning RULED: A (hosted-OAuth)

<!-- GAP-SINCE-LAST-FIRE: 0.2h -->

The cron fired (autonomous tick). 1 new memo — Lead's **github-mcp-server provisioning decision** (exactly the call I flagged in the #1220 ratification: stdio-local vs hosted). It's framed as an Arch/CIO architecture-direction call. **Ruled A (hosted-OAuth)** — and this is the role-portfolio **architecture-integrity** call, so I ruled it decisively rather than presenting a toss-up: **B (local-stdio-PAT) re-introduces the raw-token custody ADR-070 D3 deliberately designed out** (Piper holding each user's PAT to inject into a subprocess — the exact pattern WS-2/#1229's "bindings-not-credentials" collapse removed); **A realizes D3** (server owns the OAuth token; Piper stores only a #1229 binding). A also generalizes (single-user-now → multi-tenant, no re-stamp; same principle as the #1232 Phase-1 ruling); B doesn't. Affirmed the substrate direction (**MCPClient supports both stdio + streamable-HTTP** — the ecosystem uses both; hosted servers are HTTP; ADR-070 substrate must not be transport-locked — build regardless of the GitHub call). Handed PM the **one genuinely-business-gated dimension** (cost/licensing/data-policy on `api.githubcopilot.com`) with a decision tree (A unless a hard blocker → then B-as-temporary-single-user-debt, never B-for-production). → memo to PM cc Lead/Exec/PA (`fa58952c4`) + decisions.log (`4a6541e23`).

Drained. Queue back to: awaiting PM's business-checkpoint on provisioning + Lead's #1317 ports + the alpha bundle. Light hold.

---

### PM-prompted resume (13:37) — provisioning A→C re-ruled + cron troubleshoot + Ship 049 + 2 ratifications

Big catch-up drain (cron stalled the 09:27/12:27 fires — mode-1b; PM resumed + asked for a cron troubleshoot). Drained all of it:

**github-mcp provisioning RE-RULED A→C** (the headline). While I was stalled, the business-checkpoint I'd flagged on A *fired*: PM's hard constraint — alpha testers can't be required to have Copilot — blocked A's hosted endpoint. Lead surfaced **Option C (self-host `github-mcp-server` + per-user OAuth via Piper's GitHub App)** + a token-custody precision. Ruled both: **C is D3-acceptable**, and I **precised the D3 invariant** — D3 protects against *raw, long-lived, unscoped vendor credentials* (PAT/API-key), NOT against holding any token; a short-lived, scoped, revocable, refreshable **OAuth grant** (#358-encrypted, binding-referenced) is permitted, and it extends the **existing Calendar-OAuth precedent** (verified `google_calendar_adapter.py` #529/#843). **Owned my imprecision** — my A memo's "no token touches Piper" was wrong (as MCP client Piper holds the session grant); precised to "no raw PAT." Named the D3-ideal end-state (GitHub-App installation-token, m-36 ratchet) → Lead filed it as **#1325**. → memo to Lead cc PM/Exec/PA (`aec74ea7a`) + decisions.log (`4d980b978`). Lead acked, building inc.2 on the confirmed model.

**Cron troubleshoot** (PM's explicit ask). Diagnosis: **not a cron problem — in-process scheduler suspension.** The cron (`ff1df50a`) is correctly armed; the macOS host app suspends the backgrounded process → the in-process scheduler freezes → no fires (mode-1b). Verified the **launchd watchdog IS loaded + working** (`com.pipermorgan.duty-cycle-watchdog`, hourly, last-exit-0) — but it's **nudge-only** (`scripts/duty-cycle-watchdog.sh` = dedup/cooldown nudge logic), so it closes detection→alert but not alert→resume (the gap CIO named). Interim: foreground on the always-on Mac Mini / disable App Nap. Structural cure (CIO's lane): the trigger must live off-machine (the watchdog being a *separate* launchd process that survives suspension is the proof-of-concept). → memo to PM cc CIO/Exec (`9c2a723a2`).

**Ship #049 Architect lens** (window Jun 19–25) — the workstream review with the new §0 (progress vs portfolio goals). Scored against `ROLE-PORTFOLIO-ARCH` §2: RECONNECT substrate ADVANCED (#1232 ratified + Phase-1 ruled), make-drift-impossible ADVANCED (#1312 one-Base invariant), #1283 advanced-then-M5-deferred; the honest window-shape = high-value rulings around the ~3-day infra gap. → `dev/2026/06/27/` archive (`bd9f06c47`) + exec/PM/PA (`6da063bfe`).

**2 ratifications**: inbox-proxy discipline **ACKed** (retire reflexive cc-PM; route through Exec by intent) + an architecture-lane calibration note (co-decisions need the full memo, not a board one-liner) (`29ba7687a`). #1325 end-state confirmed.

Inbox drained. Queue: provisioning → Lead building C/inc.2 (#1325 end-state tracked); #1317 ports; #1312 after-alpha; #1283 M5; cron → CIO's off-machine cure. Light hold; cron `ff1df50a` armed (mode-1b notwithstanding).
