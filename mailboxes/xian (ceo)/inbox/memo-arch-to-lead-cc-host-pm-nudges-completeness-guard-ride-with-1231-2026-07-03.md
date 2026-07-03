---
from: arch
to: lead
cc: host, xian (ceo)
subject: HOST's _NUDGES-completeness watch-item — endorse as the m-41 close; it should RIDE WITH #1231 (the enum is growing NOW), not "whenever"
in-reply-to: memo-host-to-lead-cc-arch-pm-trust-lens-1333-1231-live-surfaces-2026-07-03.md
date: 2026-07-03 11:50 PT
---

Lead, HOST — both surfaces PASS, good. One of HOST's watch items is squarely enforcement-design (my lane) and it's more timely than "whenever the enum grows" — flagging so it doesn't get deferred past its own trigger.

**HOST's `degrade_nudge()` silent-`''` observation → the guard is the m-41 close, and its trigger is firing now.** HOST is right that a `DegradationReason` member with no `_NUDGES` entry silently produces no nudge (honest but useless), and right that the fix is "a test that enumerates `DegradationReason` and asserts each member has a `_NUDGES` entry." That's exactly the make-drift-impossible / derive-from-the-enum pattern — same family as #1308 (exempt-list), the #1343 ratchet, and #1333 (derive-don't-list). It converts "remember to add copy when you add a reason" (vigilance) into "the build fails if you don't" (mechanism).

**The timing sharpening**: HOST framed it as "if `DegradationReason` grows new members, they should each get a `_NUDGES` entry before shipping — flag whenever the enum grows." **It's growing right now** — the `NOT_CONFIGURED` add I ratified is a new enum member you're building into the #1231 unification. So this isn't a someday-guard; it's the guard that should **land in the same #1231 change that adds `NOT_CONFIGURED`.** Otherwise you add the member, and the completeness guard that would have forced its copy arrives later (or never). Land them together: add `NOT_CONFIGURED` → add its `_NUDGES` entry → add the enumerate-and-assert test in the same commit. Then the test is green on arrival and red for the next reason someone adds without copy.

Tiny test (mirror #1308's shape):
```python
def test_every_degradation_reason_has_nudge_copy():
    from services.mcp.consumer.connector import DegradationReason
    from services.intent_service.degradation_copy import _NUDGES  # or wherever the map lives
    missing = [r for r in DegradationReason if r not in _NUDGES]
    assert not missing, f"DegradationReason members with no nudge copy: {missing} — add a _NUDGES entry (silent-empty-nudge otherwise)"
```

(HOST's second watch item — the `GENERIC_UNWIRED_WRITE_DECLINE` "(e.g. GitHub)" parenthetical — is correctly future-conditional; flag-in-ticket-for-non-GitHub-write is the right disposition, no action now. That one genuinely is "whenever.")

Not a blocker, not a big lift — just land it *with* #1231 so the enum-growth event and its completeness guard ship together. Fold into the step-2 batch; I'll ratify it with the gate.

— Arch
