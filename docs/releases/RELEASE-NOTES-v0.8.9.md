# Release Notes v0.8.9

**Release Date**: June 22, 2026
**Branch**: `main` → `production`
**Previous Version**: v0.8.8 (D1/RECONNECT design quality pass, June 19, 2026)
**Sprint**: RECONNECT WS-1 + Security + Design D2
**Release model**: development continues on `main`; `production` carries the **last stable, canonical-regression-passing build** for alpha testers at `alpha.pipermorgan.ai`.

---

## Summary

**v0.8.9 closes three open fronts at once.** The RECONNECT sprint's connector infrastructure gets a real foundation — DB-backed config replacing fragile in-memory and JSON stores, honest no-repo UX when GitHub isn't connected, and a proper standup assembly pipeline (the hollow `MorningStandupWorkflow` is retired; `StandupAssembler` is promoted to the real thing). The security layer moves from theory to production: AES-256-GCM field encryption with HKDF per-field key derivation is wired in, the secret store is encrypted, per-user LLM key wiring is live, and two auth-layer hygiene issues are closed. Design D2 ships the token system, responsive shell, and mobile nav — plus a rename that matters: "Documents" becomes "Radar" throughout, and standup and work items are now first-class Radar data sources.

**Infrastructure**: Dockerfile upgrades to Debian 12 (bookworm) to satisfy chromadb's SQLite ≥3.35 requirement.

---

## What's New

### RECONNECT — Connector Infrastructure (WS-1)

Connector config now has a real, stable home. The `github_preferences.json` file and the in-memory store it backed are gone; connector state lives in the database, survives restarts, and is queryable across sessions.

- **#1199 — DB-backed connector config**: connector configuration is now persisted in the database rather than an ephemeral JSON file. Repo config, user preferences, and integration state survive server restarts.
- **#1226 — Config stability + honest no-repo UX**: when a GitHub repo is not configured or the connector can't resolve it, Piper surfaces an honest "not connected" state rather than silently failing or guessing. The UX degrades honestly.
- **#1289 — StandupAssembler promoted; MorningStandupWorkflow retired**: the hollow `MorningStandupWorkflow` (which assembled nothing meaningful) is replaced by the real `StandupAssembler` pipeline that pulls from live connector data, assembled Radar sources, and user context. The `/api/v1/standup/today` endpoint is the canonical standup path.

### Security — Field Encryption + Auth Hardening

The security architecture (tracked as #358 across two phases) ships its full first-generation implementation in 0.8.9.

- **#358 — AES-256-GCM field encryption with HKDF per-field keys**: the `FieldEncryptionService` provides authenticated encryption for sensitive fields. Each field uses a distinct key derived via HKDF from a root secret — key isolation at the field level, not just at the record level.
- **#358-B — Encrypted user secret store**: the `user_api_keys` table's secret column is now encrypted at rest. Existing plaintext secrets are migrated on the upgrade path; new secrets are encrypted on write and decrypted on read transparently.
- **#1185 — Per-user LLM key wiring**: user-supplied LLM credentials (BYOC, introduced in D1) are now routed per-request, not per-server. Each inference call uses the user's key when present, falling back to the server key. This completes the BYOC credential flow end-to-end.
- **#1307 — admin_compose removed**: the `admin_compose` route surface, which allowed unauthenticated composition access, is removed. No replacement; the feature it backed was not shipped.
- **#1308 — auth-exempt-list lint enforcement**: the auth exemption list in `web/middleware/intent_enforcement.py` is now lint-enforced. New exempt routes require an explicit rationale comment; the CI check fails if exemptions are added without one.
- **#1232 — Connector protocol**: the connector abstraction now has a formal protocol definition. Connectors implement a typed interface rather than duck-typing against a loose base class.

### Design — D2 Token System + Mobile Nav + Radar Rename

- **#1286 (D2) — Token system + responsive shell + mobile nav**: the design token system is fully applied to the app shell. The responsive shell adapts across viewport widths. Mobile nav is implemented (hamburger → drawer pattern) rather than the previous "just don't use on mobile" posture.
- **#1238 — Documents → Radar rename**: the "Documents" nav label is renamed to "Radar" throughout — the surface name now reflects what it actually is (your work-item radar, not a document archive). The internal object model follows the nav.
- **#1269 — Standup as a Radar source**: standup content is now surfaced as a first-class entity in the Radar feed — your daily standup appears alongside issues and work items, not on a separate page.
- **#1239 — Work items as live Radar entities**: GitHub issues assigned to your configured handle surface as live Radar entities, updated on each Radar refresh.

### Infrastructure

- **#1299 — Dockerfile → bookworm (Debian 12)**: the production Dockerfile base image upgrades from bullseye to bookworm. Required: chromadb's bundled SQLite requires ≥3.35, which bullseye (SQLite 3.34) does not satisfy. Bookworm ships SQLite 3.40.

---

## Known Limitations (alpha testers, read this)

- **Settings UI re-paste bug (#1105)**: the Settings UI sometimes requires re-entering your API key even when the server has it saved correctly in the keychain. Workaround: restart the server after saving — the keychain read works correctly on restart.
- **History privacy toggle is a stub (#1164)**: the "Start private session" toggle in the History slide-out renders but has no backend behavior. Cosmetic; don't rely on it.
- **Workstyle learning claims (#1216)**: asking "what have you learned about my workstyle?" may produce a response that claims a seed-vs-real distinction the system can't actually make. Report these — they're honesty gaps.
- **Multi-tenancy audit in progress (#1241)**: some content is not fully anchored to user auth. Use test data only; the audit is Architect-owned and in progress.
- **Stakeholder-update misclassification (#1256)**: stakeholder-update queries occasionally route to `update_document_query`. Rephrase as "write a stakeholder update for..." if the response feels off.
- **macOS keychain only**: BYOC credential storage uses the macOS keychain. Linux and Windows credential stores are not yet wired.
- **GitHub OAuth not started**: PAT token auth works; the GitHub OAuth connect flow is planned for a later sprint.

---

## Version Mechanics

- **Increment**: **0.8.9** on the 0.8.x alpha development line. 0.9.0 reserved for the full Beta release at M5 close; 1.0 = GA.
- **Cut commit**: **`29814b625`** — current tip of `main` (June 22, 2026).
- **pyproject.toml bump**: `0.8.8` → `0.8.9`.
- **Tag**: `v0.8.9` annotated — "Release v0.8.9 — RECONNECT + security + design".
- **Production**: `production` branch fast-forwarded to `v0.8.9`; serves `alpha.pipermorgan.ai`.
- **Forward cadence**: M4 (Trust + Learning) → M5 (Distribution + Polish) → 0.9.0/Beta.

---

## Upgrade Instructions

```bash
git checkout production && git pull origin production
pip install -r requirements.txt
python -m alembic upgrade head   # includes secret-column encryption migration
docker compose up -d              # postgres:5433, redis, chromadb (bookworm image)
python main.py                    # port 8001 (or PIPER_PORT)
```

For alpha testers on `alpha.pipermorgan.ai`: the hosted instance will be updated automatically. No local steps needed unless you're running your own instance.

**Note for self-hosters**: the Dockerfile base image change (bookworm) requires a `docker compose build` before `docker compose up -d` if you're running the containerized stack. The `alembic upgrade head` migration will encrypt any existing plaintext secrets in `user_api_keys` — this is non-destructive and reversible.

---

## Contributors

- Claude (Lead Developer + Web + leadership/staff agent cohort) — implementation, testing, methodology
- xian (PM/founder) — design, UAT, sprint management

---

## See Also

- [Release Notes v0.8.8](RELEASE-NOTES-v0.8.8.md) — prior release (D1/RECONNECT design quality)
- [BRIEFING-CURRENT-STATE](../briefing/BRIEFING-CURRENT-STATE.md) — live milestone status
- [Alpha Quickstart](../ALPHA_QUICKSTART.md) — setup guide
- [Alpha Deployment](../internal/operations/alpha-deployment-runbook.md) — how `alpha.pipermorgan.ai` is deployed

---

_Released: June 22, 2026 — v0.8.9 tagged at `29814b625` (RECONNECT + security + design). Production at `alpha.pipermorgan.ai`._
