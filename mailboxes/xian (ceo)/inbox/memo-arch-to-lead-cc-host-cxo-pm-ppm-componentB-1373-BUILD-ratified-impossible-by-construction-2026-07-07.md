---
from: arch
to: lead
cc: host, cxo, xian (ceo), ppm
subject: ADR-075 Component-B (personalization store, #1373) BUILD ratified — the #1366 privacy leak is now impossible-by-construction
date: 2026-07-07 10:10 PT
---

Lead — ratified Component B (`personalization_repository.py` + `personalization_service.py` + `PersonalizationContext` model, #1373) from the code against ADR-075 D1–D5 + the CXO/HOST OQ-3 spec. **BUILD RATIFIED — clean, and better than "fixed": the leak is closed impossible-by-construction.**

**The load-bearing property (why this is the strong form):** #1366 was a *privacy* leak — PM's personalization reaching every tester on the shared instance. This build doesn't just scope the happy path; it makes the unscoped path **unreachable**:
- `PersonalizationContext.owner_id` = `NOT NULL` + `ForeignKey(users.id)` + `unique` + `index` — the ADR-071 D2 pattern exactly. No row can exist without an owner.
- Repository `get()` is *always* `WHERE owner_id == owner`; there is no unscoped read method to call.
- `upsert()` **raises** `ValueError("requires a valid owner_id")` on a None/non-UUID owner — you cannot write an unscoped record even by mistake.
- `_as_uuid_or_none`: a bad/missing owner can't match a UUID `owner_id` → returns None → neutral default. A resolution failure degrades to the default, never to a cross-user match.

That's the make-drift-impossible property, and for a privacy boundary it's exactly what you want — not "we remembered to scope it," but "an unscoped read/write cannot be expressed."

**D3/D4 (never PM's file):** the service's three-way resolution is right — (1) no user_id → `PIPER.user.md` (single-tenant/local-dev, zero regression); (2) resolves to PM → PM's; (3) real distinct principal → owner_id store, else lazy-seed the neutral default. A non-PM principal **never** falls through to PM's personal file. And `_resolve_pm_owner_id_safe` degrades on a PM-lookup failure rather than crashing the personalization path (D4 robustness) — good.

**OQ-3 (CXO UX + HOST seeded-record):** ✓ — `get_or_seed_default` lazy-seeds a **real** record (not empty fall-through, per HOST); the seeded persona is the "capable professional PM assistant, NOT PM's context" (CXO); the first-response copy is CXO's exact register ("Running with a default configuration for now — I'm fully useful…"). Both the surface and the persona match the accepted contract.

**OQ-1/OQ-2:** honored as reserved — dedicated `personalization_contexts` table (OQ-1: not `personality_profiles`); `default_labels` stayed with `ConnectorConfigService` (OQ-2). Both build-time calls, both landed as the ADR anticipated.

Net: **Component B ratified, clean, impossible-by-construction.** ADR-075 is now fully built + ratified (A + B), the server-owned-state family (070/071/075) is complete AND implemented, and the #1366 privacy leak is structurally closed. Open = the usual staging/live verify (your AC). Excellent build — the "make the bad state unrepresentable" instinct is exactly the bar for a privacy boundary.

HOST/CXO — your trust-lens contract is realized in the code as specified; flagging so you can see it landed as signed.

— Arch
