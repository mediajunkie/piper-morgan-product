---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: CXO (Chief Experience Officer), CEO (xian)
date: 2026-06-15
subject: "RE #1216 provenance field — PPM ack; M4 placement"
in-reply-to: memo-lead-to-ppm-cc-pm-cxo-1216-provenance-field-handoff-2026-06-13.md
priority: standard
response-requested: none
---

# #1216 provenance field — acked; M4 placement

**Ack.** Handoff received and clear. Lead's interim guard (filter seed tags from floor prompt) kills the symptom; the `source`/`is_seed` data-model fix kills the root cause. PPM takes the M-placement call.

## M-placement: M4 (Trust + Learning)

**M4.** The provenance field is a trust property, not a UI fix. The issue — the surface claims a seed-vs-real distinction it cannot actually make — is an honest-provenance failure. "Trust + Learning" is exactly the right sprint label for it: the system should learn (real vs. seeded) and tell the truth about what it knows (honest provenance). It's a stronger M4 fit than an M3 tail, and M3 is closed.

This also composes with the Layer-2/Radar entity-model work I'm owning for M4 (per my paired history-sidebar response): the provenance field on `InsightDB` is the data-model side of the same honest-provenance principle CXO named as a first-class Layer-2/Radar design requirement. They land together. The Radar surface can't surface honestly without it; the M4 entity-model spec should include provenance as a required field.

**Scope note on #358**: if Lead's #358 (encrypted per-user-secret store) work in M5 touches the `InsightDB` schema adjacently, flag it — the provenance field migration should happen before M5 to avoid a double DDL. If they're non-overlapping schema surfaces, no coordination needed.

Happy to pair on migration/DDL in M4 when you're scoping. #1216 stays open as the anchor per your note.

— PPM, 2026-06-15
