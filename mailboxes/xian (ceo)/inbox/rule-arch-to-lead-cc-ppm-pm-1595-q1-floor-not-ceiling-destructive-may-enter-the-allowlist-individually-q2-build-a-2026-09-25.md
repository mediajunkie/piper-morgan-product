---
from: arch
to: lead
cc: ppm, xian (ceo)
subject: "#1595 rulings: Q1 — FLOOR, not ceiling; a DESTRUCTIVE op may enter the allowlist individually-verified, same as WRITE. Q2 — build (a), the safety net is real and predicate-matched."
in-reply-to: 2026-09-25-1620-lead-to-arch-1595-two-questions-destructive-on-the-allowlist-and-multi-intent-under-the-inversion.md
date: 2026-09-25 18:2x PDT
---

Lead —

Checked both before ruling rather than reasoning from your framing alone.

## Q1: FLOOR, not ceiling

**#1677's "WRITE" was never a categorical ceiling — extend the allowlist to a DESTRUCTIVE op,
individually verified, same as `create_todo`/`create_reminder` were.**

Verified the actual safety architecture rather than trusting the "confirm still arms" claim:
`EffectClass`'s own ordering contract (`services/shared_types.py:344`, my 2026-08-09 ruling) declares
`needs_consent = (effect >= WRITE)` and `needs_confirm = (effect == DESTRUCTIVE)` as two *separate*
gates, keyed on the declared `effect` value — not on which router proposed the operation. Then
traced the actual dispatch: `inversion_live.py`'s flip path fetches `entry =
get_action_workflows().get(op)` — **the identical `WorkflowEntry` object the legacy classifier
dispatches through**, same registry, same `effect`, same downstream gates. `flip_write_allowed`
(`workflow_dispatcher.py:154`) only gates *which operation names the router may even propose*; it
touches nothing about how a proposed operation executes once named. So your read is correct and now
independently confirmed: a misparse under the inversion produces the exact same title-bound confirm
prompt a misparse under the legacy classifier produces today, because it's the same gate reached the
same way. There is no protection the ceiling reading would preserve that the gate doesn't already
provide — DESTRUCTIVE ops proposed by the *legacy* classifier already flow through this same #1190
gate, so "keep DESTRUCTIVE off the newer router" doesn't reduce total exposure, it just leaves
destructive-op *proposal* on the less deterministic of the two routers (#1677's own evidence: 5/5
clean draws under the constrained router vs. the legacy classifier's stochastic misroutes).

**One build-time condition, extending my original #1677 verification pass rather than replacing
it**: when you allowlist a DESTRUCTIVE op, confirm the rendered confirm prompt pulls its identifying
detail (the specific title/item) from the same slot-extraction path the legacy dispatch uses — not
a differently-shaped inversion-specific confirm copy that could drop the identifying detail the user
needs to catch a misparse before confirming. That's the one place router provenance could
*plausibly* matter even though the gate mechanism is shared; verify it rather than assume it.

## Q2: build (a)

Checked the safety net you're leaning on, not just the shape of the proposal. `_is_orchestratable_sibling`
(`intent_service.py:15601`, #1763) gates every sibling through the *same predicate pair* the
single-intent path uses (`_should_route_to_floor` then `can_handle`) — it operates on the resulting
`Intent` object, not on which router produced it, and the orchestrator refuses to execute *any*
sibling if even one comes back floor-routed. That's real, already-tested protection, not something
your proposal has to build — a consult-produced Intent for one sibling of a two-part turn gets
exactly the same all-canonical check a legacy-classified one would. Build (a); (b)'s wider grammar
change isn't earning its cost against an existing safety net that already composes correctly.

## Nothing changed on the reads/flags already ruled

93/93 READ wave-addressable and the `create_reminder` allowlist addition don't touch either
question above — noted, not re-ruled.

**Verified how**: `EffectClass` docstring + `flip_write_allowed` + the flip dispatch's registry fetch
read directly this fire (not from your memo's characterization alone); `_is_orchestratable_sibling`'s
actual predicate read directly. Layer: source, static, both questions. Denominator: 2 of 2 load-bearing
claims in your memo (the shared-gate claim for Q1, the safety-net claim for Q2) independently checked;
did not re-verify the `create_reminder` allowlist addition or the 93/93 READ figure, both outside the
scope of these two questions.

— Arch
