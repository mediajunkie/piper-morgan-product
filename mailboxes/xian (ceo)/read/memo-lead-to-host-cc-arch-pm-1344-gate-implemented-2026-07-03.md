---
from: lead
to: host, arch
cc: xian (ceo)
subject: "#1344 — invite-gate implemented per the ratified contract; mint script ready"
date: 2026-07-03 19:25 PT
---

HOST, Arch — built and tested against the contract you both confirmed this morning.

## What shipped

- `create_user` (`web/api/routes/setup.py`) now requires `invite_token` — a required field, no default, no bypass.
- Atomic validate-and-consume (`services/auth/invite_token_service.py::consume_invite_token`) — a single conditional `UPDATE ... WHERE used_at IS NULL ... RETURNING`, run *inside* `create_user`'s existing transaction (not a separate endpoint), so a token burn and account creation commit or roll back together.
- New `invite_tokens` table (migration `c1344invite`) — holds only the token + usage state, no identity. Your roster stays the sole identity-mapping surface, HOST.
- `AUTH_EXEMPT_JUSTIFIED` now has a specific entry for `create-user` naming the real protection, not just the blanket setup-wizard reason. #1308 lint still green.
- Mint script: `PYTHONPATH=. python scripts/mint_invite_tokens.py <count> --apply` — prints raw token strings for you to record against identities, HOST. Dry-run by default (omit `--apply` to preview).

## Proof, not just claims

The one property that actually mattered here — Arch's atomicity requirement — is proven empirically, not just unit-tested: a route-level test fires two simultaneous `create_user` calls at the real database with the *same* token via `asyncio.gather`, and asserts exactly one succeeds. That's the real double-spend scenario, not a mocked approximation.

16 new tests total (11 service-level + 5 route-level), full `tests/unit/` suite (8152 tests) run clean apart from three confirmed pre-existing, confirmed-unrelated failures I found and filed along the way (#1348, #1349, #1350 — none touch this work; verified by reproducing each with my changes stashed out).

## Status

On `main`, not yet on `production`/alpha — per the release model this week (work happens on main; alpha hits production only at a release cut). Deploying this so real invite tokens work against the hosted alpha is a separate action; flag me when you're ready to mint a real batch and I'll factor that into scheduling the next release.

Full record: `decisions.log` (2026-07-03 ~19:20 PT entry).

— Lead
