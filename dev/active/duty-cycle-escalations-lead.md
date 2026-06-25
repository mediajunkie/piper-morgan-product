# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

**Maintenance mechanism (methodology-41, added 2026-06-10):** the `duty-cycle-tick` skill's STOP procedure now includes an **attention-doc reconciliation step** — at day-close, `gh issue view` each Open item that references a GitHub issue; any CLOSED/merged → move to Resolved with a disposition note. Plus per-fire appending during the Mail/Task loops. This replaces the vigilance-promise that let the doc go 14 days stale (Exec memo 2026-06-10). The mechanism lives in the skill (read at every fire), not institutional memory.

---

## Open

- **2026-06-25 · PM+Arch · #1320 onboarding auth-loop → #1162 Caddy-gate-removal DECISION** — NEW, onboarding-breaking. Validating the LLM key dialog-loops on the hosted browser path (MCP unaffected). Root cause CONFIRMED via chrome-devtools repro: the two-layer auth (Caddy basic-auth gate + app JWT) makes the XHR-heavy pre-login setup flow block on the browser credential dialog whenever basic-auth creds aren't cleanly carried. **Two PM asks**: (1) confirm whether it still loops in a FRESH incognito window (vs. just stale cache from today's password rotation) — tells us severity; (2) the real fix is **removing the Caddy gate (#1162)** — PM/Arch security-posture decision (app has its own auth now). Filed #1320. Two harmless side-bugs found (check-keychain wrong path; settings-status not setup-exempt) — Lead fixing the clear one (check-keychain) unilaterally.
- **2026-06-25 · PM (FYI) · alpha Caddy password rotated** — gate password is now `piperalpha` / `crispy` (per PM request). Verified working. Old value backed up on Droplet. (Note: this rotation is the likely trigger of the #1320 instance PM saw — stale cached creds.)
- **2026-06-25 · PM+PA · alpha-tester email gate** — the alpha onboarding blockers (#1318 system-check, #1319 mobile card) are SHIPPED + PM-UAT'd; #358 encryption verified live. **The one remaining pre-email gate is the MCPB clean-machine test** (PM + PA on a non-dev machine). Email v5 + zip are held pending it.
- **2026-06-25 · PM · UI chat smoke test** — encrypted write path (send a chat message); now unblocked since onboarding works. Headless can't reach the full auth+LLM write path; needs a real PM login. #358 mechanism already proven in-container.
- **2026-06-25 · PM+Arch · #1312 collapse sequencing + user_id-contract pairing** — Arch ruled the personality orphan-Base collapse; Lead scoped it (multi-caller refactor, not a 2-liner — see #1312 comment). Needs PM execution-sequencing (slots after the alpha gate) + Arch pairing on the user_id-contract destructive-vs-additive call. owner_id re-add rides with #357.
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
