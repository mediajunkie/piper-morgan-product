# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-25 ~09:40 PT. Sole lead. Session log: `dev/2026/06/25/2026-06-25-0635-lead-code-opus-log.md`

## ▶ STATE — alpha bundle readiness (current focus)
- **Alpha 0.8.9 LIVE + hardened** (`alpha.pipermorgan.ai`): firewall (DOCKER-USER DROP 5432/6379/8000, boot-persistent) + postgres password rotated + redis auth. All 5 containers healthy.
- **#1318 + #1319 DONE + PM-UAT'd ✅** (commit `a12223dca`, 2026-06-25): onboarding system-check now reads env-var service addresses (was hardcoded localhost); mobile welcome card top-aligns (was below-fold on iOS `100vh`). Deployed to alpha (container restart, code is volume-mounted) + PM confirmed on phone. Live `check-system` returns `all_required_ready:true`.
- **#358 encryption deploy VERIFIED** on live alpha (2026-06-25): `ENCRYPTION_MASTER_KEY` set (44-char Fernet), `FieldEncryptionService.from_env()` + `EncryptedString` TypeDecorator round-trip confirmed in-container. 4 encrypted cols empty (no chat yet). **#358 epic stays OPEN** for M5 (per-user-secret store = #1185 hosted floor + broader PII). Exec corrected (the "PM must set the key" item is moot).
- **#1310 FIXED** (commit `c66bc7d6e`, 2026-06-25): `mail-send.sh` now self-reconciles its push residue (no more manual rm/restore before merges). 16/16 test-mail-send.sh pass.

## ▶ NEXT — Lead queue
**Unblocked unilateral Lead-code is DRAINED.** Remainder is PM/Arch/CXO/CIO/product-gated:
- **#1287 Multi-Agent Coordinator removal — PAUSED, awaiting CIO boundary call.** CIO triaged (cluster dead in prod; deletion = Lead lane). Lead verify-before-delete found the boundary extends into the **`methodology/` tree** (orchestration_bridge / enhanced_orchestration_bridge / integration_runner import `multi_agent_coordinator.AgentType`) — both prior traces missed it (scoped to `services/`). Methodology files are test-only-reached (dead-but-present) but it's CIO's lane. Mailed CIO (cc PM, `cb8f9441e`): expand removal into methodology/, or relocate AgentType. **Nothing deleted.** Execute full pass once CIO sets the boundary. Finding on #1287.
- **#1320 onboarding auth-loop** — side-bug #1 (check-keychain) FIXED+deployed; the loop itself = #1162 Caddy-gate-removal (PM/Arch); side-bug #2 (settings setup-exempt) tracked.
- **MCPB clean-machine test** — PM + PA on a non-dev machine. **The one remaining pre-alpha-tester-email gate** (Droplet + onboarding side done + verified). Not Lead work.
- **PM UI smoke test (chat write path)** — PM to log in + send a chat message; exercises the encrypted write path (headless-unreachable for the full auth+LLM path; #358 mechanism already proven). Now unblocked since onboarding works.
- **#1312 (DB↔model drift, ~111 diffs)** — Arch RULED the multi-Base seam (2026-06-25): collapse `personality/models.py` orphan Base, repoint repository, reject multi-`target_metadata`. **Scoped collapse plan captured on #1312** (it's a multi-caller refactor, not a 2-liner: canonical `id` no PK-default; `user_id` UUID+FK vs orphan String; `get_default("default_user")` sentinel + str-typed trust/response-enhancer callers; owner_id #357). **Awaiting PM execution-sequencing** (slots after alpha-tester gate) + **Arch pairing on the user_id-contract call**. Bulk ~111-diff reconciliation still separate. owner_id re-add rides with #357.
- **#1286 Slice 2 (radar tiling)** — CXO-gated (memo `e6decb14f`, 3 options); Slice 1+3 shipped, pending CXO conformance + PM phone-UAT. Can't close #1286 until.
- **#1185 / connector ports (RECONNECT Phase-1)** — #1232 Arch-ratified; WS-9/WS-1/WS-2 foundation done. Ports are the next spine move but **gated on PM/Arch sequencing direction** (MCP-spine #1220 — sequencing doc `dev/2026/06/22/reconnect-remainder-sequencing-2026-06-22.md`). Don't unilaterally launch the large architectural piece without direction.

## ▶ PENDING PM / Arch
- **PM**: MCPB clean-machine test (gates alpha-tester email) · UI chat smoke test · sequence the RECONNECT remainder (#1220 MCP-spine) vs other priorities.
- **Arch**: #1312 reconciliation (multi-Base, schema-risky) · confirm Phase-1 ports build-order if/when RECONNECT resumes.
- **CXO**: #1286 Slice 2 radar tiling decision (3 options memo'd) + conformance on Slice 1/3.

## ▶ DONE this session (06-25)
- #1318 (system-check env-var addresses) + #1319 (mobile welcome card) — fixed, 16 tests, deployed, PM-UAT'd, closed.
- #358 encryption deploy verified live; #358 verification comment; Exec queue corrected.
- #1310 mail-send self-reconcile — fixed + T6 regression + CLAUDE.md note; closed.
- Lead inbox cleared (CIO loop-closed + Exec nudge → read/). Jun 24 log was already DAY-CLOSED.

## ▶ STATE / refs
- **alpha** 0.8.9 live + hardened. Deploy mechanism: Droplet builds from local files (no git there) — `scp` changed files to `/opt/piper/...` then `docker compose ... restart app` (code is volume-mounted `.:/app`, so restart picks it up without a full rebuild). `deploy.sh` does a full rebuild (slow — downloads CUDA wheels; use restart for code-only changes).
- **Mailbox** = `scripts/mail-send.sh` (push-to-ref) — **now self-reconciles (#1310)**, no manual post-send cleanup needed.
- **Encryption**: key on Droplet; `services/security/field_encryption.py` (`from_env()`) + `encrypted_types.py` (`EncryptedString`, `PMENC1:` marker). 4 content cols: artifacts.content, conversations.preview, conversation_turns.{user_message,assistant_response}.

## ▶ Methodology
- **Investigate-before-extending**: read whole #1318/#1319 issue bodies + setup.py before fixing; verified #358 key state on Droplet before assuming Exec's "must set key" was current; read #1310 + the whole mail-send.sh before changing shared infra.
- **Shared-infra caution**: #1310 touched cohort-wide mail tooling → defensive design (surgical paths, best-effort, never-fail-the-send) + throwaway-repo test harness before shipping.
- **Verify at the user's layer**: #1318/#1319 not "done" until live curl + PM phone-UAT; #358 not "deployed" until in-container round-trip on the real key.
