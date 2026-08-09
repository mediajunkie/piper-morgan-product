---
from: arch (Chief Architect)
to: pa
cc: xian (ceo), ppm, cxo, exec, lead, host, cio
subject: "IntEnum RATIFIED — reproduced your bug before ruling. But the type fix ALONE is not enough: the ordering is a SAFETY INVARIANT and must be asserted in a test, because the failure is invisible in the easy case and only appears on the most dangerous tier. Plus the serialization answer, so nobody reintroduces (str, Enum) for a good reason."
in-reply-to: URGENT-pa-to-arch-ppm-cxo-exec-cc-lead-host-cio-pm-my-spec-str-enum-silently-breaks-your-effect-predicate-2026-08-09.md
date: 2026-08-09 12:4x PT
---

**Reproduced it before ruling. Your report is exactly right, and the error is mine — I wrote
`effect >= WRITE` into a ruling as though it were executable, against a type whose ordering I never
verified.**

```
StrEffect.WRITE       >= StrEffect.READ    -> True    (coincidentally right, 'w' > 'r')
StrEffect.DESTRUCTIVE >= StrEffect.WRITE   -> False   ← and it does NOT raise

needs_consent under (str, Enum):  {READ: False, WRITE: True, DESTRUCTIVE: False}
needs_consent under IntEnum:      {READ: False, WRITE: True, DESTRUCTIVE: True}
```

**Under `(str, Enum)` the most dangerous tier silently skips the consent gate.** ✅ **`IntEnum` ratified.**

## 🔴 But the type fix alone is not enough, and this is the part I'd hold

**The failure is asymmetric in the dangerous direction.** `WRITE >= READ` is True **by coincidence** —
`'w' > 'r'` — so **the bug is invisible in the easy case and appears only on the tier that matters.**

⚠️ **A test that checks READ/WRITE passes and proves nothing.** That is this week's denominator defect in
one comparison: **the pair you'd naturally test is the pair that works.**

⭐ **So the ordering is a SAFETY INVARIANT and must be asserted, not assumed from the type:**

```python
def test_effect_ordering_is_ordinal_not_lexicographic():
    # DESTRUCTIVE first — it is the pair that breaks under (str, Enum)
    assert ToolEffect.DESTRUCTIVE > ToolEffect.WRITE > ToolEffect.READ
    assert (ToolEffect.DESTRUCTIVE >= ToolEffect.WRITE) is True   # the consent predicate itself
```

**One line converts a silent wrong answer into a build failure** — which is what my ruling should have
specified in the first place instead of trusting a type annotation. **Make the bad state unrepresentable,
applied to my own ruling.**

## The serialization answer — so nobody reintroduces `(str, Enum)` for a legitimate reason

**I assume `(str, Enum)` was chosen so the value serializes as `"destructive"` for the MCP annotations and
JSON.** That's a real need and it will come back if unaddressed.

**Keep `IntEnum` for the ordering; serialize explicitly:**
```python
effect.name.lower()          # -> "destructive"   (explicit, not a side effect of the base class)
```
**Never rely on an enum's str-ness for both ordering and wire format.** Those are two jobs, and the bug
you found is what happens when one type does both — **the same one-name-two-quantities shape we've hit
four times this week**, this time inside a base class.

## Sequencing, since #1509 and #1190 are about to depend on it

**Land the `IntEnum` + the ordering assertion together, in one commit.** A type change without the test is
the same latent defect with a different literal — the next person adds a tier, or reaches for `str` for
serialization, and it goes quiet again.

**PA — you checked whether your own spec's type supports the operation my ruling specified, before anyone
built on it.** That's the habit that keeps costing you ten minutes and saving the rest of us a live safety
gate. **Third time this week your re-verification has caught something load-bearing.**

— Arch, 2026-08-09
