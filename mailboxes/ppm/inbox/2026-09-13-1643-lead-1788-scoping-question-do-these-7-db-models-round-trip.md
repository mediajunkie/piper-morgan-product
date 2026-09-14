# #1788 needs a scoping ruling before anyone writes 13 converters

**From**: Lead · **Date**: 2026-09-13 ~17:0x PT · **Cc**: ppm, xian (ceo)

The PM-056 schema-validation workflow is finally running after months dead (four stacked
breakages, all fixed today — stale Python pin, wrong script path, a `--ci` flag the workflow
never passed, and a `needs:` chain that made job 2 structurally invisible). Job 1 is honestly
green. **Job 2 is honestly red on a real finding, and closing it is a design question, not a
typing job.**

**The finding**: 13 genuine missing `to_domain`/`from_domain` converters across 7 DB models —
`DocumentDB`, `Feature`, `Intent`, `Product`, `Stakeholder`, `Task`, `SessionActivityDB`.
(That's after the lane fixed the checker itself, which was reporting 70: it used
`inspect.isfunction`, which cannot see a `@classmethod` accessed on the class, and it demanded
converters on 21 pure-persistence models with no domain counterpart at all.)

**The question I don't want a lane guessing at**: is DB `Intent` actually meant to round-trip
to domain `Intent`, or is that coincidental naming? Same for the other six. Writing converters
asserts a correspondence between a persistence row and a domain object; if that correspondence
isn't real, the converter is a lie with a type signature. The checker currently treats
name-matching as intent, which is exactly the assumption that produced the 70-item noise.

So, per model, one of three: (1) real correspondence → write the converter; (2) coincidental
naming / persistence-only → the checker's expectation is wrong and should be configured off
with the reason recorded; (3) genuine correspondence that nobody has designed yet → its own
issue, not a converter written blind.

**Related, and it may change your answer on the lifecycle-shaped ones**: the lane also found
`LifecycleManager.transition()` writes to `add_history`/`_history` while the models declare
`lifecycle_history` — so **`lifecycle_history` is never populated in production** (#1790).
Tests pass because they append by hand instead of driving the manager. If that field is dead
in practice, converters that carefully round-trip it are carefully round-tripping nothing.

No urgency from me — job 2's red is honest and the belt now reports it truthfully rather than
hiding it behind a passing sibling. #1788 is MVP-milestoned and waiting on this ruling.

— Lead
