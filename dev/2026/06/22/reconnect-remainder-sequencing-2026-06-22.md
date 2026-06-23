# RECONNECT remainder — sequencing recommendation

**Author**: Lead Dev · **Date**: 2026-06-22 · **For**: PM + PA sprint chunking (per PM's "you can plan your own sprints" autonomy)
**Source of truth**: `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md` (the sprint umbrella) + the GH Projects **Sprint** field.

## Done (as of 2026-06-22)
- **Phase 0 (Design)**: ADR-070 ratified — MCP-consumer connector architecture.
- **WS-1 (config home)**: #1226 + #1199 **CLOSED** — DB-backed `connector_configs`, cwd-independent, honest-degrade.
- **WS-5 (contract)**: #1232 **CLOSED** — `Connector` protocol + sum-types + m-41 no-credential guard, Arch-ratified.
- **WS-9 (identity)**: #1233 **CLOSED** — single-identity collapse; multi-tenant deferred (ADR-070 OQ-3).
- Release **v0.8.9** cut to `production`; Droplet deploy (Phase B) pending PM's master key.

## The spine: the MCP migration reshapes WS-2/3/4 (key finding)
Per scope §0 + line 15, the MCP decision means **auth / config / resolution / degrade increasingly happen at the MCP layer**. That's not just WS-8 — it *reshapes* the middle workstreams, and two of them are **already partially delivered**:
- **WS-2 (#1229) credential model** may SHRINK to "store per-user MCP-server *bindings*, not raw creds" (scope §0). Decide the shape with Arch before building.
- **WS-3 (#1230) resolution correctness**: the github `resolve_repo` + dead-default-project halves are **DONE** (WS-1). Remaining = generalize resolution to **non-GitHub connectors** — per-connector, i.e. it folds into the **ports** (#1317).
- **WS-4 (#1231) honest-degrade contract**: the `degrade()` *contract* is **DONE** (#1232 `DegradationResponse`). Remaining = **apply degrade per connector** (≈ the ports, #1317) + the "connect-me" surfaces (partly #1226 Phase-3).

**→ Don't run #1230/#1231 as written.** Re-scope them (as we did #1226): their remainders are per-connector and belong with the MCP ports (#1317 / #1220), not as standalone pre-port workstreams. Re-scope-or-close is a PM/PA call.

## Recommended sequence
1. **WS-2 (#1229) — credential model.** First a quick Arch design-decision: does MCP-server-binding storage shrink this to a thin "store bindings" task? Foundation; decide before building.
2. **MCP-migration spine — #1220 (WS-8) + #1317 (WS-5 ports).** Port connectors onto the contract + MCP, folding in WS-3 non-GitHub resolution + WS-4 per-connector degrade as each ports. This is the bulk of the remaining refactor.
3. **First-run / connect UX — #1201 (WS-6) + #1314 (auto-default).** The connect-me surfaces + guaranteed-resolvable-or-prompt.
4. **Slack robustness — #1109 + #1110 (WS-7).** Redis-backed OAuth state + `user_id` propagation.
5. **#441 (auth phase-2), #865 (setup-wizard refactor).** Independent of the connector framework; schedule by priority.
6. **#1315 (populate project-links), #1316 (residual cleanup).** Roadmap / low-priority.

## Beta-gating (separate track from connector mechanics)
Per scope decision-a (PM 2026-06-20): the hosted-beta foundation is **#1185 (identity / BYO-key core)** + **#1300 (cred-decouple, SKUNK/M5)**. #1185's Phase-1 + #358 encrypt-at-rest floor shipped; its remaining gate is the **Caddy-gate-removal decision** (#1162, PM/Arch). That's the beta path — distinct from finishing the connector refactor, and it (plus M4/M5) is what gates the 0.9.0 beta version.

## Flagged for PM/PA
- **Re-scope candidates**: #1230 (WS-3) + #1231 (WS-4) — partially delivered by WS-1/WS-5; re-scope to the port work or close-with-fold-in.
- **Arch design-decision** needed before WS-2 (#1229): does MCP-binding storage shrink the credential model?
- This is a *recommendation*, not a unilateral plan — PA owns sprint chunking with PM; I'll execute whatever sequence you both land on.
