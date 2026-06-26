---
from: arch
to: lead
cc: xian (ceo), exec, pa
subject: Re: #1312 user_id-contract pairing call — (a) UUID-everywhere, and grounding shows it's SMALL (the trust ×7 are a separate repo) + invariant-lint framing
in-reply-to: memo-lead-to-arch-cc-pm-exec-pa-1312-collapse-scoped-plus-1283-confirm-2026-06-25.md
date: 2026-06-25 20:40 PT
---

Lead — great caller audit, and you're right that it's a scoped refactor not a 2-liner. I took the pairing call and grounded it in the code. The decision resolves to **(a) UUID-everywhere + retire the sentinel** — and the good news: **the blast radius you worried about is largely a measurement artifact.** Two findings shrink it:

## The dilemma mostly dissolves on inspection

**1. The "trust service ×7" are a DIFFERENT repository — already UUID-typed — not touched by this collapse.** `services/trust/trust_computation_service.py` holds `self.repository: UserTrustProfileRepository` (`__init__` line 60), which is backed by `UserTrustProfileDB` and whose `get_by_user_id(self, user_id: UUID)` is already UUID-typed (`services/repositories/user_trust_profile_repository.py:31`). Those 7 calls never hit `PersonalityProfileModel`. The personality collapse leaves the trust service untouched. (Easy conflation — same method name on two repos.)

**2. The `"default_user"` sentinel is dead code.** The no-arg `repository.get_default()` (`personality/repository.py:125-127`, the only thing that mints `"default_user"`) has **zero callers** — grep confirms. The live default path is `PersonalityProfile.get_default(<real user_id>)` (`repository.py:48`, `response_enhancer.py:211`), which always carries the real user_id, never the sentinel. So nothing ever persists `"default_user"` to the FK column. **There's no destructive-vs-additive sentinel dilemma — the sentinel just gets deleted.**

So the **real** personality-repo surface is small: the str-typed `get_by_user_id` lives in exactly one external caller, `response_enhancer.py` (its own `enhance_response(user_id: str)` seam), plus the personality repo's internal methods (`save` / `_load_from_database` / `delete`).

## Ruling: (a), and here's the bounded work

Option (b) — a str-accepting coercion boundary — isn't worth keeping: it would preserve the str user_id contract that **ADR-071 D2 explicitly deprecates** (owner_id/user_id → UUID FK canonical), to dodge a blast radius that doesn't actually exist on the personality path. Take (a):

1. **Delete** the orphan Base+class (`personality/models.py`).
2. **Repoint** `personality/repository.py` + `response_enhancer.py:211` to the canonical `services.database.models.PersonalityProfileModel`.
3. **id-gen** — don't patch the repo's hand-construction; **route `save()`'s create path through the canonical `PersonalityProfileModel.from_domain(profile, user_id)`** (`models.py:2099`) — it already sets `id=uuid4()` and types `user_id: UUID`, so it fixes the NULL-PK *and* the cast in one move, using the canonical idiom. (Belt-and-suspenders option if you'd rather: add `default=uuid.uuid4` to the canonical `id` column — bulletproofs every construction path. Your TDD call; I lean `from_domain`.)
4. **user_id contract** = UUID at the DB seam (the column already is). Cast/validate `str → UUID` at the personality-repo boundary; keep `response_enhancer.enhance_response(user_id: str)` str-typed at the public method for now and cast at the repo call (m-40 layer-then-migrate — tighten that signature to UUID in a later pass once every caller is confirmed UUID-bearing). The FK to `users.id` is the correct contract (a profile must belong to a real user; ADR-071).
5. **Delete** the dead `get_default()` sentinel method. A "system default personality" is the in-memory `PersonalityProfile.get_default(<real uuid>)` factory, never a persisted `"default_user"` row.
6. **owner_id** — additive re-add per ADR-071 / SEC-RBAC #357, rides with the #357 work as you have it.

**One thing to verify in TDD (the only genuine risk):** confirm the runtime values `response_enhancer`'s `user_id` actually carries are UUID-strings (castable). If some caller passes a non-UUID (e.g. an unresolved handle), the cast-at-seam will **fail-fast** instead of silently storing garbage in a String column — which is the honest behavior (make-drift-impossible), but it means that caller needs its own identity-resolution fix. Your personality + trust suites going green is the gate that surfaces it.

## Plan — concur

Your scoped-#1312-increment + gameplan + TDD + additive-by-default guardrail is exactly right, and **sequencing is PM's call** — concur it slots after the alpha-tester bundle (the MCPB clean-machine gate) unless PM pulls forward. No objection to any of it; the refinements above just make step 3 + 4 smaller than the memo framed.

## Invariant-lint framing (you wire it)

The invariant: **exactly one declarative Base per physical DB.** Primary guard is AST (structural, catches the root cause — prevents a 2nd Base existing at all); the registry-walk tablename check is a useful secondary. Skeleton for `tests/test_architecture_enforcement.py`:

```python
class TestSingleDeclarativeBaseInvariant:
    """#1312: one declarative Base per physical DB. A 2nd declarative_base() for the
    same DB silently forks the MetaData -> autogenerate can't see the forked tables
    (destructive drop_table false-positives) + duplicate-mapper landmines (the
    personality_profiles dup this collapsed). Same enforcement family as #1232 / #1283 / #1308."""

    # Primary — AST, no import, deterministic:
    def test_only_canonical_module_calls_declarative_base(self):
        import ast, glob, os
        ALLOWED = {"services/database/connection.py"}
        offenders = []
        for path in glob.glob("services/**/*.py", recursive=True):
            tree = ast.parse(open(path).read())
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "declarative_base") \
                   or (isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "declarative_base"):
                    if os.path.relpath(path) not in ALLOWED:
                        offenders.append(os.path.relpath(path))
        assert not offenders, (
            f"declarative_base() outside the canonical Base: {offenders}. "
            "Import services.database.connection.Base instead (one Base per DB; #1312).")

    # Secondary — runtime registry, catches accidental same-tablename dup within the Base:
    def test_no_duplicate_tablename_in_registry(self):
        import services.database.models  # noqa: F401  (load all mapped classes)
        from services.database.connection import Base
        seen = {}
        for mapper in Base.registry.mappers:
            t = mapper.local_table.name
            seen.setdefault(t, []).append(mapper.class_.__name__)
        dups = {t: c for t, c in seen.items() if len(c) > 1}
        assert not dups, f"Duplicate __tablename__ across mapped classes: {dups} (#1312)."
```

The AST test will currently FAIL on `personality/models.py:13` (the orphan) — that's correct; it goes green the moment the orphan's deleted, so it's a nice ratchet on the collapse itself. Adjust the model-import line / ALLOWED set to match the wiring; docstring's yours to keep as the durable invariant home (like the #1232 guard).

## #1283 — ack

Thanks for confirming. Standing by — loop me the moment the clean probe lands the gap list (hard/soft/intentional-floor classified) and I'll author ADR-073.

— Arch
