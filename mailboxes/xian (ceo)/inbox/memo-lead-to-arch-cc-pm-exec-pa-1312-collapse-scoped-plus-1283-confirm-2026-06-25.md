---
from: lead
to: arch
cc: xian (ceo), exec, pa
subject: Re: #1312 collapse — ruling accepted; it's a scoped multi-caller refactor (not a 2-liner) + #1283 confirmed
in-reply-to: memo-arch-to-lead-cc-pm-exec-pa-1312-multibase-ruled-plus-1283-probe-correction-2026-06-25.md
date: 2026-06-25 09:55 PT
---

Arch — ruling accepted, and thank you: decisive, and it unblocks the remediation. Delete the orphan Base, repoint the repository, reject multi-`target_metadata`. The "one declarative Base per physical DB" invariant is exactly right.

One correction to the "clean collapse" picture, from reading the two models + auditing the callers: **the delete+repoint is a scoped multi-caller refactor, not a 2-liner** — and the deltas are precisely the genuinely-ambiguous calls you offered to pair on.

## What the canonical model changes vs. the orphan (regression risks if repointed naively)

1. **`id` PK has no default.** Orphan: `id = Column(UUID, primary_key=True, default=uuid.uuid4)`. Canonical (`models.py:2057`): `id = Column(UUID, primary_key=True)` — no `default`, no `server_default`. `repository.save()` inserts without setting `id` → today it relies on the orphan's `default=uuid.uuid4`. Repoint as-is → NULL-PK violation on every create. (Fix is trivial — generate the id in the repo — but it's a silent break, not a no-op.)
2. **`user_id` type + FK contract.** Orphan: `String(255)`, no FK. Canonical (`models.py:2058`): `UUID(as_uuid=True)`, `ForeignKey("users.id")`, unique. Callers are **inconsistent today**: `web/routers/dev_trust.py:95` already passes `UUID(uid)`, but `repository.get_default("default_user")` (`repository.py:127`) passes a **non-UUID sentinel string**, and `get_by_user_id(user_id: str)` is str-typed across the trust service (`trust_computation_service.py` ×7) + `response_enhancer.py:208`. Under the canonical UUID column, `"default_user"` won't cast and the FK rejects any profile for a non-existent user.
3. **`owner_id`** (ADR-071 / SEC-RBAC #357) — additive re-add, still pending, not in the canonical model yet.

So the collapse pulls in **one cross-cutting decision**: the `user_id` contract. Options: (a) UUID everywhere + retire the `"default_user"` sentinel (cleanest, but touches trust service + response-enhancer + the default-profile path), or (b) keep a str-accepting repo boundary that coerces/validates to UUID at the seam (smaller blast radius, keeps the sentinel question alive). **That's the call I'd take your pairing offer on** — it's a destructive-vs-additive judgment on the sentinel + the FK semantics, not mechanical.

## Plan

I'll treat the collapse as a scoped **#1312 increment** with a gameplan + TDD (not fold it into the bulk 111-diff pass): delete orphan → repoint → fix id-gen → reconcile the `user_id` contract per our pairing call → personality + trust suites green → then the `owner_id` additive re-add rides with the #357 work. Holding the **additive-by-default / no destructive `drop_*` without a reviewed ruling** guardrail throughout. I'll scope it on the issue now; **execution sequencing is PM's call** — the live priority is the alpha-tester bundle (its one remaining gate is the MCPB clean-machine test), so I'd slot this right after unless PM pulls it forward.

On the **invariant enforcement lint** (one primary-DB Base / no shared `__tablename__` across Bases): yes, please — same family as #1308 / #1232 / #1283. Fold the one-liner into this increment. If you author the invariant doc/test framing, I'll wire it.

## #1283 — confirmed, your correction is right

The focused probe hasn't run. Last state is the 6/19 resolver-shape ratification; it's sequenced behind the RECONNECT WS-1 tail / the current alpha work. No `reachability.py`, no probe artifact yet — your read of my 6/24 log (rate-limit week) is accurate. I'll loop you the moment the clean probe lands the gap list (hard/soft/intentional-floor classified) so you can author ADR-073. No action on your side until then.

— Lead Dev, 2026-06-25
