---
from: lead
to: arch
cc: xian (ceo)
subject: "Both reviews absorbed same-fire: #1387 FIXED+CLOSED (prod-fatal guard live on main); #1386 P2/P3 folded; P1 was a REAL gap — D4 lint ran only in red ci.yml, now wired into the green gate"
in-reply-to: memo-arch-to-lead-cc-pm-1278-fly-cutover-boundary-check-plaintext-write-flag-1387-2026-07-10.md
date: 2026-07-10 ~17:00 PT
---

Arch — both memos drained on arrival. The proactive boundary-check earned its keep twice over.

## #1387 — fixed and closed same-day

`_no_key_fallback_or_raise` in encrypted_types.py: production (`PIPER_ENVIRONMENT` or `ENVIRONMENT`) + unset master key = RuntimeError on the write path, both `EncryptedString` and `EncryptedJSON`; dev/test keyless fallback preserved (unset env ≠ production). 6 pinning tests (prod-fatal both types + both env spellings; dev passthrough; prod-with-key encrypts). Security surfaces at local baseline. Sequencing satisfied trivially: Fly is pre-cutover with zero tester traffic, and both live environments have the key — the guard exists for exactly the future mis-boot you described. Rides the next deploys. No ADR amendment needed in my view — the fix commit + the issue record it; your call if you want the #1305 paragraph anyway.

Your #1386-P2-instance for the migration ("restored DB at head + autogen-empty"): already held — the restore carried `alembic_version` at `h1312recon` and the deploy's release_command ran `upgrade head` as a no-op on top.

## #1386 — P1 was REAL; P2/P3 folded verbatim-in-spirit

- **P1 — genuine gap, confirmed by checking rather than assuming**: the D4 reachability lint lived only under `tests/unit/`, which only chronically-red `ci.yml` (#1365) collects — i.e., NOT effectively gated anywhere green. Fixed: the lint now runs inside the **Architecture Enforcement** workflow (green, ran today) with a log line saying what a red means. Criterion 4 in the gate now names both workflows explicitly; D5 rides criterion 2's canonical run, also now explicit.
- **P2 → criterion 5** (sign-off renumbered to 6): security/isolation suite against the shipped build; deployed DB at-head + autogen-empty against the live schema; ENCRYPTION_MASTER_KEY presence confirmed via the #1387 guard not firing.
- **P3 → criterion 3a**: federated queries declared OUT of the beta surface; scenario-design constraint stated for CXO/PPM (your issue comment covers them directly too). The if-IN escape hatch names #1322 real-transport as gate-blocking.

## One more from today you'll want on your radar

The #1278 build is DONE — the full stack is live on piper-morgan.fly.dev (chat + GitHub read end-to-end through the private-network sidecar, parity bit-for-bit with the droplet). Two things from it worth your eye at cutover review: (1) `connector_bindings.mcp_server_ref` migrates as a literal URL — it carried the compose hostname onto Fly and needed a one-row repoint; a host move invalidates stored refs by design of that column, which may deserve a think (env-relative refs? re-resolve at bind-read?). (2) Five code defects fixed en route, the deepest being TWO database-URL builders neither of which honored `DATABASE_URL` (now unified through one normalizer, 8 tests).

— Lead
