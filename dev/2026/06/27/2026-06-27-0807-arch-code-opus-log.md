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

---

### WATCH (autonomous tick, ~13:51) — 1 informational memo triaged

<!-- GAP-SINCE-LAST-FIRE: 0.0h -->

The cron fired (autonomous tick, right after the 13:37 drain). 1 memo: **CIO — both my cron datums folded into the liveness-model spec** (Update 6/27, `73a5d5f5a`); the `durable:true`=session-only datum is "load-bearing" (reframes the off-machine cure from nice-upgrade to the-only-thing-that-survives-restart) + it **caught a latent gap in the shipped Iris cutover runbook** (its F2 fix leans on `durable:true`; CIO flagged Calliope to verify on Klatch). Informational/appreciative, no ask → triaged to read/ (no noise-reply, per the inbox-proxy discipline I just ratified). No other unblocked Arch work — provisioning/ports with Lead, cron-cure with CIO, #1312 after-alpha, #1283 M5. WATCH; cron armed.

---

### Fire — PM-prompted (15:23) — cron cure (a) architectural decomposition → CIO

<!-- GAP-SINCE-LAST-FIRE: 1.5h -->

PM "you have mail." 1 memo: **CIO concurred my cron diagnosis** + named a crux before committing to cure (a): *can launchd inject the duty-cycle prompt into a suspended session?* Contributed an architectural refinement (genuine unblocked work on an active thread where CIO invited the framing): **"inject into a suspended session" is a category error** — a suspended process can't receive input → **(a) decomposes into (1) un-suspend by foregrounding** (launchd CAN: `open -a` / AppleScript activate; App-Nap releases on foreground) **then (2) the un-frozen in-process cron fires on its own** (no injection API needed). So the feasibility question narrows from the hard "inject-into-suspended" (impossible) to the **testable** "does foregrounding un-freeze the scheduler + fire promptly?" — with a concrete cheap experiment (background → miss a tick → `open -a` from launchd → observe). If step 2 holds, (a) shrinks to "watchdog gains a `foreground`, the existing cron is the resume" ($0). Deferred the mechanism-scoping + experiment to CIO (their lane). → memo to CIO cc PM/Exec (`7fb422b63`).

Drained. Back to light hold — same queue (Lead's C/inc.2 + ports; CIO's cron-cure scoping; alpha bundle). Cron armed.

---

### WATCH (autonomous tick, ~15:57) — cure (a) SHIPPED (my decomposition built)

<!-- GAP-SINCE-LAST-FIRE: 0.5h -->

1 memo: **CIO BUILT cure (a)** (`dafc4904f`, watchdog "Belt 0") — converged exactly on my decomposition: launchd foregrounds via **`open -b com.anthropic.claude-code`** (smart improvement over my `open -a`/activate — activate self-deadlocks from-within + System Events is TCC-blocked; `open -b` is Launch-Services, clean exit) → the existing cron fires (no injection). My "concrete first test" became their self-validation (watchdog log shows `FOREGROUND` on first real stall). **Honest scope boundary**: Belt 0 cures **Mode 1b** (backgrounded) but not **1a** (cron-object-dead/session-ended — foregrounding can't resume a non-existent cron); 1a still needs re-arm or the off-machine trigger ((b)/(c)). Informational + the architectural contribution already landed *in the build* → triaged to read/, no noise-reply. The cron-cure thread (my lane's contribution) is effectively closed: diagnosis → decomposition → built, all today. 1a residue is CIO's to advance. WATCH; cron `ff1df50a` armed.

---

### Fire — autonomous (18:27 cron, ran 18:57) — ADR-071 EntitySources-promise boundary CONFIRMED SETTLED (PPM unblock)

<!-- GAP-SINCE-LAST-FIRE: 3.0h -->

The 18:27 cron **fired cleanly** (~3h interval) — a good cron datum (no stall this slot). 1 memo: **Exec relayed PM's ask to expedite ADR-071** — the #049 synthesis flagged it as the single highest-leverage unblock (gating PPM #1237 entity-model + CXO #1290 nav). Question: does ADR-071 already settle the EntitySources-promise boundary, or need an increment?

**Investigated before ruling (the payoff)**: traced the referent — **#1237 is CLOSED** (6/18; 3-of-4 sources shipped, built to the ADR-071 pattern + PM-UAT'd) and the PPM entity-model spec is **build-ready + already uses `owner_id`** (its OQ-1/2/3 are M4 product-scoping, not ADR-071 gates); the one open type (People/#1281) is gated on **source-population, not ADR-071**. So the "#1237 gated on ADR-071" framing was **stale** — the gate is discharged.

**Ruled: ADR-071 already settles the boundary; no increment.** The 4 types map cleanly (PM-domain = global-by-design+render-guard D1; Conversation/Document = owner-anchored; People/stakeholders = owner-anchored D6). **Drew a disambiguation** to prevent mis-routing: "anchor-first trust governs which sources can be promised" conflates two boundaries — (1) who-can-see = owner-scoping = ADR-071's lane (SETTLED) vs (2) which-provenance-is-surfaceable = the trust-gradient / PPM OQ-2 (ADR-072-D5-adjacent, a PPM/CXO M4 call, NOT an ADR-071 increment). If PPM's blocker is (1) they're clear now; if (2), it routes to the trust-gradient, not ADR-071. → unblock memo to PPM cc PM/Exec/PA (`76c0f704c`) + decisions.log (`e8d149a78`). Unblocks two parked lanes on a gate that was already discharged.

Drained. Light hold — same queue (Lead's C/inc.2 + ports; alpha bundle). Cron armed + firing.

---

### STOP (21:27 cron, ran 21:57) — day-close

<!-- GAP-SINCE-LAST-FIRE: 3.0h -->

2 memos, both informational → triaged: **PPM fully accepted my ADR-071 correction** (acknowledges the stale blocker-label, isolates People/#1281 to source-population, takes OQ-2 to CXO in M4, forward-carries my 2 impl notes to Lead, updating their standing-items + portfolio to drop the stale gate) + **Exec's People source-population one-pager ask** (PPM's lane; my impl note + the ADR-071 boundary already captured; I'm cc for awareness — may get looped if the connector-import option touches the ADR-070 substrate). No response needed; day-closing.

**Cron datum**: the daytime cron **fired cleanly at 18:27 + 21:27** (~3h intervals) — the afternoon's earlier stalls didn't recur this evening (Belt 0 helping and/or the app stayed foregrounded). Good close to a day that started in a stall.

## Day arc — June 27 summary (DinP day 11 / Saturday; dense architecture-ruling day + cron-cure landed)

Started recovering from the June-26-into-27 stall; turned into one of the highest-output ruling days — three architecture calls + the cron-cure collaboration + Ship 049 + 2 ratifications.

| Fire | Time PT | Gap | Deliverable |
|---|---|---|---|
| START | 08:07 | (June 26 stall) | June 25/26 close recovery; **#1220 Shape-B RATIFIED + #1322 cutover ruling** (found the hardcoded-sim → #1322 is value-realizing) |
| provisioning | 08:17 | 0.2h | github-mcp provisioning ruled **A** (hosted-OAuth, D3-aligned) + HTTP-transport direction |
| resume | 13:37 | (PM/stall) | provisioning **RE-RULED A→C** (D3 precised); **cron troubleshoot** (in-process suspension); **Ship #049 lens**; **inbox-proxy ratified** |
| WATCH | 13:51 | 0.0h | CIO datums folded (triaged) |
| cron-cure | 15:23 | (PM) | **cron cure (a) decomposition** → CIO (foreground-then-cron, not inject) |
| WATCH | 15:57 | 0.5h | CIO **built cure (a)/Belt 0** — my decomposition shipped |
| ADR-071 | 18:57 | 3.0h | **ADR-071 EntitySources boundary CONFIRMED SETTLED** (PPM unblock; the gate was already discharged) |
| STOP | 21:57 | 3.0h | PPM ack + Exec People one-pager triaged; day-close |

**Load-bearing of the day**: three architecture rulings — **provisioning A→C** (precised the D3 invariant: protects against raw PATs, not all tokens), **#1220 Shape-B** (+ the value-realizing #1322 finding), **ADR-071 boundary** (the investigate-before-extending payoff: the highest-leverage move was *verifying the blocker was real* — it wasn't, the gate was discharged, two lanes freed without writing anything). Plus the **cron-cure** went diagnosis→decomposition→Belt-0-built in one day (clean Arch↔CIO), Ship #049 shipped, and 2 ratifications (inbox-proxy + #1325 end-state).

## Memory & briefing surfaces referenced this session (per #974)

**Referenced**: ADR-070 D3/D6 (provisioning C) · ADR-071 D1/D6 + the Radar entity-source gates (the boundary ruling) · the **PPM entity-model spec** + GH #1237/#1281 (investigate-before-extending — traced the referent, found #1237 closed) · the Calendar-OAuth precedent (`google_calendar_adapter.py` #529/#843 — grounded the D3-grant-custody read) · `query_router.py` + `MCPConsumerCore` (the #1220 hardcoded-sim find) · the **launchd watchdog** (`com.pipermorgan.duty-cycle-watchdog` + `duty-cycle-watchdog.sh` — the cron troubleshoot) · `ROLE-PORTFOLIO-ARCH` §2 (Ship #049 §0) · m-40 (#1220 layer-then-migrate) · m-36 (end-state invariants: #1325, simulation-test-only, single-Base) · `[Investigate before extending]` + `[STOP on source gap]` + `[no flattened commands without referents]` (the #1237-stale-framing catch — the day's sharpest discipline win) · `[feedback_honor_durable_instructions_under_cross_pressure]` (used mail-send.sh, not the cron prompt's stale bridge-dance line).
**Loaded but not referenced**: xpoll brief; most of the cohort delta.
**Wanted but not found**: nothing notable — every artifact I needed (ADRs, the PPM spec, the issues, the code, the watchdog) was present + verifiable.

## Sign-off discipline

```bash
$ git log --oneline origin/main..HEAD   # 0 — all June 27 work on origin/main (verified per-fire)
$ git status --short                     # clean apart from this close
```

✓ All June 27 work on `origin/main` — verified by content per-fire (provisioning A→C + #1220 + ADR-071 rulings; decisions.log ×4; cron troubleshoot + cure-decomposition; Ship #049; inbox-proxy ack; all triage moves).
✓ Carry-forward current (provisioning C / #1325; #1220 + #1322; ADR-071 boundary settled; cron Belt-0; Ship #049 done).
✓ Cron `ff1df50a` armed — leave armed for tomorrow's 06:27. Fired cleanly at 18:27 + 21:27.

<!-- DAY-CLOSED: 2026-06-27 -->

— Architect (DinP / Opus 4.8), Saturday June 27 closed at 21:57 PT. Day 11 on DinP: three architecture rulings (provisioning A→C, #1220 Shape-B, ADR-071 boundary) + the cron-cure landed (Belt 0) + Ship #049. **Sunday**: Lead's C/inc.2 + #1317 ports to watch; the PPM People-source one-pager (may loop me on the connector-import ADR-070 touch-point); #1322 cutover when Lead scopes it.
