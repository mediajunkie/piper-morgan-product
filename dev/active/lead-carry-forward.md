# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~20:00 PT (after #1307 + #1308 — the security gap fully closed). Sole lead.

## ▶ NEXT — RECONNECT Phase-1 is Arch/PM-gated
The cleanly-unblocked RECONNECT work is delivered (WS-5 contract #1232 + the security gap #1307/#1308). Next:
- **Phase-1 (WS-9 identity → WS-1 config → WS-2 creds)** — gates the connector ports + WS-3/4. WS-9 (#1233) needs Arch's confirm **and** PM's identity call (web `a25db09c` = Slack `009afc8c`?).
- **Arch's #1232-kickoff reply** (ADR-070 v0.1 stable? type shapes?) — then the ports.
- #1185 PARKED (gate chain).

## ▶ PENDING PM/Arch
- **PM**: the WS-9 identity disambiguation (web vs Slack record = same human?).
- **Arch**: #1232-kickoff confirms; the #1308 env-gated simplification (FYI).
- #358 close: hold-for-deploy (PM-confirmed).

## ▶ DONE (2026-06-20 — very big session)
- #1299 → 0.8.8 alpha; #1162 reconciliation; #1185 P1 (parked); #358 floor + Dimension B (code-complete; #1305/#1306 deferred).
- Gate-removal investigation (CONDITIONAL GO) → Arch CONCUR → **both prereqs DONE**:
  - **#1307** admin_compose removed + closed (instance).
  - **#1308** exempt-list enforcement lint shipped + closed (the class-fix; m-41). #1162 gate-removal now ready for M5.
- **#1232 WS-5 connector CONTRACT shipped** (protocol + 4 types + AST-guard + github proof; 14 tests). Ports deferred (D8).
- Discovered + filed **#1309** (stale onboarding test — GATHERING_REPOS vs COMPLETE).

## ▶ STATE / refs
- **#1232**: `services/mcp/consumer/connector.py` + `github_adapter.py` (`IMPLEMENTS_CONNECTOR`). ADR-070 governs.
- **#1308**: `AUTH_EXEMPT_JUSTIFIED` in `auth_middleware.py` + `tests/test_exempt_list_boundary_1308.py`.
- **alpha** 0.8.8 (no #358-B/#1232/#1307/#1308 yet — next deploy). `ENCRYPTION_MASTER_KEY` needed on the box for #358-B.
- **Cron cbe956dc** armed — expr `5 5,8,11,14,17,20 * * *` (morning **05:05**, PM-requested 2026-06-21; daytime every ~3h; last/day-close fire **20:05**; was `17 22,7,10,13,16,19`). Session-only, auto-expires 7d → re-arm on the duty cycle. Mailbox = `scripts/mail-send.sh` — **RECONCILE residue immediately after each send** (`fetch+merge`); it bit twice this session.

## ▶ Methodology
- **Investigate-before-extending**: many catches (latest: #1230 is ADR-gated; the #1308 route-categorization grounded the lint in real data).
- **m-41 mechanism** (#1308 lint + #1232 AST-guard): make the bad class impossible, don't just fix instances.
- **Mail-send residue**: reconcile IMMEDIATELY after each send (lesson learned twice — a triage-move residue collided with two later merges).
