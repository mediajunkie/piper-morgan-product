# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

**Maintenance mechanism (methodology-41, added 2026-06-10):** the `duty-cycle-tick` skill's STOP procedure now includes an **attention-doc reconciliation step** — at day-close, `gh issue view` each Open item that references a GitHub issue; any CLOSED/merged → move to Resolved with a disposition note. Plus per-fire appending during the Mail/Task loops. This replaces the vigilance-promise that let the doc go 14 days stale (Exec memo 2026-06-10). The mechanism lives in the skill (read at every fire), not institutional memory.

---

## Open

### 🔴 CURRENT — TOP PRIORITY (2026-07-01 ~22:10, duty-cycle fire) — SECURITY, needs PM decision
- **2026-07-01 · PM · #1344 — Alpha registration is fully open, reverses a 2026-06-25 PM decision.** Verified LIVE (no account created): `POST /api/v1/setup/create-user` with an incomplete body → `422` not `401` — zero auth gates it. PM explicitly decided 6/25 (decisions.log ~20:45) to KEEP the Caddy gate specifically because it's the alpha's only invite mechanism; the gate came down 6/29 anyway (undocumented, not by me), silently reversing that decision without its stated prerequisite (app-layer invite control + RBAC, #1185/#357/#1312). **Two PM signals in tension** (6/25 "keep it" vs. today's direction toward removing it for BYOC) — I did NOT unilaterally restore the gate; surfaced for PM's call. Options in the issue: (A) restore the gate now (full clean revert, backup on droplet) — closes this + shrinks #1343's window too; (B) confirm this is now accepted-risk/handled elsewhere; (C) build the real invite-control fix. **PM has NOT yet responded** (as of day-close).
- **2026-07-01 · PM · #1343 — Anonymous /intent could silently bill PM's own Anthropic key.** Root-caused + **CODE FIX SHIPPED to origin/main** (11 new tests, 421+ regression green) — but **NOT YET DEPLOYED** to alpha.pipermorgan.ai (droplet is a code copy not a git checkout; deploy = full rebuild+restart+migrate, mechanism not fully documented; flagged rather than improvised solo). **PM asked directly "deploy now or handle yourself" — no answer yet as of day-close.**
- Both trace to the same June 29 Caddy-gate removal (undocumented, not by me). SSH access to the droplet is confirmed working (PM's real keys are present in this sandbox) — the blocker on both is PM's decision, not technical capability.

### ⏳ CURRENT — for PM (reconciled 2026-06-29 STOP, after the connector-build day)

### ⏳ CURRENT — for PM (reconciled 2026-06-29 STOP, after the connector-build day)
- **2026-06-29 · PM · ⭐ VERIFY #1331 (the trust fix)** — "add a milestone to my default repo" must now **honestly DECLINE**, not fake "Milestone created ✓". The one verify that matters most (a confabulated write is a trust-breaker). Live in staging.
- **2026-06-29 · PM · First real WRITE target — #1322 Q3** — the writes CUTOVER (close/comment/create as real connector writes) is still the next build, PM-gated: you pick a safe target (the test project works). The trust FLOOR is in (#1331 honest-degrade); real writes come next.
- **2026-06-29 · PM · Alpha release timing** — connector ships in a future `main`→`production` release. Your call; NOT autonomous.
- **2026-06-29 · ✅ RESOLVED · set-default-repo (#1327 Q2)** — DONE: build #1 conversational "set my default repo to X" (PM-verified "bingo") + gap-3 GUI repo-config cutover (18 repos live). Both GUI + conversational shipped.
- **2026-06-29 · ✅ RESOLVED · GitHub connector test** — PM verified badge/status (#1329 "github success") + set-default. Connector reads (issues/PRs/branches/releases/issue) live-de-risked. Optional remaining: PM spot-check the repo-scoped reads in chat.
- **2026-06-29 · FYI · #1327 now-buildable scope COMPLETE** — resolution doc + set-default + reads + repo-config all live. Remaining #1327 = later layers (explain-rules meta + M4 trust-gated infer/ask, Arch). Sim-transport (#1322): inc.1–3 done; inc.4 (dead-subsystem removal) PACED for usage. RECONNECT backlog: #1330, inc.4, Slack (last), #1230 reconcile (PPM), floor-confab deepening (#1331 follow-up, HOST/Arch).

### ⚠️ older items below are 2026-06-25 (pre the RECONNECT connector build) — largely superseded; reconcile at next STOP
- **2026-06-25 · TOP DECISION · PM focus call: hold / delegate / do the not-RECONNECT queue** — PM flagged (6/25 eve) that alpha/skunkworks support is pulling Lead off RECONNECT (the sprint) and "may ask Piper to hold off or delegate." Unblocked-tonight but HELD pending PM's call: **#1287** (CIO GO'd the full coordinator removal — option 1, expand into methodology/; ready to execute), **CXO setup intro-panel copy fix** (1-line, recommended before the alpha wave) + **copy-debt issue to file**, **#1320 double-login follow-up** (file). Also held: which **RECONNECT next-move** to start — **#1229** (needs a quick Arch design-decision first) or **#1283** (sprint-tagged, no deps, delegable). RECONNECT remainder is itself PM/PA-sequencing-gated, so there's no unblocked RECONNECT work to pull until sequenced. **Lead is holding all of the above rather than absorbing more not-sprint work unilaterally.**
- **2026-06-25 · RESOLVED · UI chat smoke test (encrypted write path)** — DONE: PM logged into the hosted alpha + sent a chat message (screenshot 6/25 eve) → exercised the #358 encrypted write path (conversation_turns columns) end-to-end on real data. Pending item cleared.
- **2026-06-25 · RESOLVED-DIRECTION · #1320 auth-loop / #1162 gate** — **PM direction: KEEP the Caddy gate for now** (gate verified working 6/25: crispy→302, wrong/no-auth→401). Decisive finding: the gate is the alpha's INVITE mechanism — `create_user` has no registration gating, so removing the gate = open public registration (moderate risk: own-key per user, but loses invite control + RBAC still hardening #357/#1312). The #1320 loop is most likely the stale-cache artifact of the same-day password rotation. **Real #1162 removal sequenced with #1185** (needs app-layer invite control + RBAC completion; not a quick fix, not blocking alpha send). Recorded in decisions.log (2026-06-25 ~20:45). Side-bug #1 (check-keychain) FIXED+deployed; side-bug #2 (settings setup-exempt) tracked. **Open thread**: PM-self-confirm of the gate pending — PM hit DNS NXDOMAIN on errands-network (PM-side only; resolves fine from 8.8.8.8/1.1.1.1/local + site up).
- **2026-06-25 · PM (FYI) · alpha Caddy password rotated** — gate password is now `piperalpha` / `crispy` (per PM request). Verified working. Old value backed up on Droplet. (Note: this rotation is the likely trigger of the #1320 instance PM saw — stale cached creds.)
- **2026-06-25 · PM+PA · alpha-tester email gate** — the alpha onboarding blockers (#1318 system-check, #1319 mobile card) are SHIPPED + PM-UAT'd; #358 encryption verified live. **The one remaining pre-email gate is the MCPB clean-machine test** (PM + PA on a non-dev machine). Email v5 + zip are held pending it.
- **2026-06-25 · PM · #1312 collapse sequencing** — Arch RULED the user_id-contract (option a: UUID-everywhere, dead `get_default` sentinel deleted; **trust-service callers are a different repo → not touched → smaller than first flagged**); bounded plan in decisions.log + Arch memo. Now needs only **PM execution-sequencing** (slots after the alpha MCPB gate). Includes an invariant-lint (AST single-Base guard).
- **2026-06-25 · PM+PA · RECONNECT remainder sequencing** — connector-refactor remainder (#1220 MCP-spine + #1317 ports, WS-2 #1229) is explicitly PM/PA sprint-chunking (sequencing doc `dev/2026/06/22/reconnect-remainder-sequencing-2026-06-22.md`). Awaiting the sequence to execute. Re-scope candidates flagged: #1230/#1231 (partially delivered, fold into ports).
- **2026-06-25 · CXO · #1286 Slice 2 (radar tiling)** — Slice 1+3 shipped (render+lint-verified); Slice 2 CXO-gated (3 options memo'd `e6decb14f`); can't close #1286 until Slice 2 + CXO conformance + PM phone-UAT.
- **2026-06-25 · PM · #1144 / #1131 greenlight** — two M3-era low-pri items (test-discipline refactor; canonical-judge-todo bug). Relevance-to-verify; want a PM greenlight before investing vs. possibly-stale work.

## Resolved

- **2026-06-18 → 2026-06-20 · CXO/PM · #1280 dark-rail design spec** — **RESOLVED (reconciled 2026-06-20 STOP)**: `gh issue view 1280` = CLOSED — the D1 design-quality wrap delivered the CXO Radar visual design (sleek left nav + 3-column layout). The rail-spec blocker is moot; the shell work landed via the D1 sprint.
- **2026-06-10 → 2026-06-16 · PM · #1165 M3 UAT gate** — **RESOLVED (reconciled 2026-06-16 STOP)**: `gh issue view 1165` = CLOSED (M3 closed). The #1133→Radar re-scope dependency became **#1236 (Radar surface) + #1238 (DocumentEntitySource)** — both SHIPPED this session (behind `?radar=1`, PM-UAT-pending), tracked as their own issues.
- **2026-06-10 · PM · #1187 floor-wiring TANDEM** — **RESOLVED (reconciled 2026-06-12 STOP)**: #1187 CLOSED (summarize-issue full chain shipped + live-verified, the tandem fetch-augment landed). `gh issue view 1187` = CLOSED.
- **2026-06-10 · PM · #1129 Slack reconnection** — **RESOLVED (reconciled 2026-06-12 STOP)**: #1129 CLOSED (Slack inbound LIVE via Socket Mode; PM uses it for M3 review). `gh issue view 1129` = CLOSED.

- **2026-06-10 · PM · M3 next-step direction** — **RESOLVED**: PM chose (b) — build #313 File Browser. Slice 1 (search+filter) shipped 57c66aab7; remaining slices + (a)/(c) still queued.
- **2026-05-27 · PM · #1122 disposition** (multi-turn antecedent fix scope) — **RESOLVED**: #1122 CLOSED in GitHub (option B shipped — extract_slots conversation_history). Disposition made; no longer awaiting PM.
- **2026-05-27 · PM · #1081 live smoke** (NOTION-SLACK-XREF UAT) — **RESOLVED**: #1081 CLOSED. Superseded by #1129 (Slack inbound structurally unmounted since 2025-10-01 → live smoke can't pass until the Socket Mode rebuild).
- **2026-05-27 · PM · #1081 disposition post-#1129** — **RESOLVED (moot)**: #1081 already CLOSED; drop-vs-keep superseded by #1129 absorbing the Slack-inbound rebuild.
- **2026-05-27 · PM · GH Actions stuck run** — **RESOLVED**: 2 weeks moot; Phase 1+2 paths-filter + concurrency landed (commit `f372ce793` + follow-ups); CI green since. The single stuck queued run is no longer load-bearing.
- **2026-05-27 · Arch · GH Actions paths-filter sanity-check** — **RESOLVED**: Phase 1+2 GH Actions work landed with the filter taxonomy in place; no Arch objection surfaced.

## Notes

- **Format discipline**: terse single-line entries, link to memo / issue / commit if disposition needs detail elsewhere.
- **Escalation tiers**:
  - **PM**: requires CEO decision (scope, priority, ratification)
  - **Cross-agent**: requires another lead's input (Arch on classifier work, CIO on methodology codification, etc.)
  - **Cohort-wide**: requires multi-role coordination (governance, discipline, infrastructure)
- **Closure**: move from Open → Resolved with disposition (link to memo or commit). Don't delete entries.
- **Reconciliation**: STOP-fire step gh-checks Open items vs GitHub state; closed issues → Resolved (the methodology-41 mechanism above).
