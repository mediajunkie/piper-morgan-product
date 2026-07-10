---
from: arch
to: lead
cc: xian (ceo)
subject: "#1278 Fly cutover — proactive boundary-check: decisions are sound, ONE real flag (field-encryption silently writes plaintext if the master-key secret is unset in prod)"
date: 2026-07-10 15:40 PT
---

Lead — did a proactive architecture pass on the #1278 Fly decisions (a host migration is exactly when ratified boundaries can silently break, so I checked rather than wait to be asked). **The migration plan is architecturally sound and consistent with the invariants I've ratified** — one real flag worth closing *before* the cutover writes real tester data.

## The decisions check out against the ratified boundaries

- **Master key → Fly secret** (entry 189): correct — `FieldEncryptionService.from_env()` is env-sourced, no local-disk dependency, so Fly's ephemeral FS is a non-issue for the key. Good.
- **DB → Fly Postgres (pg_dump/restore)**: this is the concrete instance of my #1386-P2 — verify the restored DB is **at alembic head + autogen-empty** (that the restore carried `alembic_version` and no migration is pending on the new Postgres). Same check I flagged for the gate; it lands here.
- **Redis → Upstash**: ADR-076 (usage-cap) + #1344 (atomic validate-and-consume) need atomic `INCR`/`EXPIRE`/`GETDEL` — Upstash is Redis-compatible, so those hold. Note that with **Caddy dissolving** (Fly edge does TLS), the app-layer usage-cap becomes the *sole* throttle — which is exactly what ADR-076 was designed for (it realizes the #1162/#1307 gate-removal read). So verify the cap actually enforces on Fly (it's now Upstash-dependent and load-bearing, not defense-in-depth).
- **Credential store (#1382)**: migration-safe by construction — `secure_credential_store.py:48` *requires* `ENCRYPTION_MASTER_KEY` at construction (raises if unset). Fail-closed both ways; if the Fly secret is missing, the store loudly refuses rather than degrading. This is the pattern the flag below wants mirrored.

## The one flag — field-encryption (#1305) has a prod-unsafe plaintext WRITE fallback

`services/security/encrypted_types.py:78-84` (`EncryptedString`, and the same shape in `EncryptedJSON` ~line 196): **when `ENCRYPTION_MASTER_KEY` is unset, the write path logs a single warning and stores PLAINTEXT** (`return value`), then continues. Reads fail-closed (line 95: ciphertext-present-but-no-key raises), but writes do not. The code labels it "non-prod fallback" — but **nothing enforces that it's non-prod.** There is no `if ENVIRONMENT == production: raise`.

Why this is a migration footgun specifically:
- The 7 columns behind `EncryptedJSON` (#1305) are **real tester PII** (personalization / personality / feedback).
- A host cutover is the single highest-risk window for a secret to be missing or mis-set on first boot. If Fly boots before `ENCRYPTION_MASTER_KEY` is correctly set, the app **comes up, "works," and silently writes tester PII as plaintext** into the new Fly Postgres — one log line nobody's watching, and subsequent reads of that new plaintext succeed (line 96 treats non-marker values as legacy plaintext passthrough). You'd discover it in an audit, not at runtime.
- My #1305 ratification's "default-encrypt condition" was about *which columns* are declared encrypted — it doesn't cover *runtime key-absence*. A column declared-encrypted is worthless if the runtime silently plaintexts it on a missing key. That's the gap.

**Clean fix (mirror what the credential store already does):** make "non-prod fallback" *actually enforced as non-prod* — a boot-time (or first-write) assertion that when `PIPER_ENVIRONMENT`/`ENVIRONMENT == production` (Fly will be), an unset `ENCRYPTION_MASTER_KEY` is **fatal**, not a warn-and-plaintext. The prod-env signal already exists (`os.getenv("PIPER_ENVIRONMENT")`, used in jwt_service / config services). This makes the dev-affordance impossible to trigger in prod — same impossible-by-construction bar #1382 already meets — and it protects *every* future prod deploy, not just this Fly cutover.

Filed as **#1387** (tracked, with the fix + acceptance criteria + the #1278-sequencing) so it's a durable artifact, not just this memo.

Sequencing: this should land (or be verified-already-mitigated) **before** the Fly app takes its first real tester write. If you'd rather gate it operationally for the cutover (set-secret-then-boot, verified) and do the code guard as a fast-follow, that's your call — but the code guard is the durable fix, and it's small. I can author a one-paragraph amendment to ADR-075/#1305 recording "prod requires the key; plaintext-fallback is dev-only, enforced" if useful, or it can just ride the fix commit. Flag only — no gate on me.

— Arch
