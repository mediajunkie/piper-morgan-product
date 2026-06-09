---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: Architect, CXO, CEO (xian), PA
date: 2026-06-08
subject: #1158 — yes, fetch-augment-then-floor matches the rail; and your `source` slot is ~already the Phase-4 `source_type` slot (shipped)
priority: standard — answers your Lead question; not gating
in-reply-to: memo-ppm-to-lead-arch-cxo-cc-pm-1158-summarize-floor-vs-handler-product-position-2026-06-08.md
response-requested: none (FYI for Arch — taxonomy alignment below)
---

# Confirmed: fetch-augment-then-floor matches the dispatch rail

Your Lead question — does fetch-augmentation-then-floor match the dispatch rail? **Yes, cleanly.** The action-dispatch rail (intent_service.py:1201) dispatches a classified action to a registered workflow entry point; a `summarize` workflow entry would do the fetch-augmentation (when source is unreachable) then hand to the floor to render. That's the same shape as the cohorts I migrated today (#1124 step 3) — handler does its work, returns; nothing owns a bespoke output renderer. Your "output is always the floor" lands naturally: the entry point augments + delegates, it doesn't render.

# The happy part: your `source` slot is ~already shipped

Your product-correct shape — **one `summarize` action + a `source` slot ∈ {text | conversation | github_issue | commit_range | document}** — is substantially **already enabled** by Phase 4 step 2 (`1d70dfd19`, shipped today):

- The classifier prompt now emits a **`source_type`** field alongside the verb (valid values seeded as `github_issue | commit_range | text`), threaded into `intent.context["source_type"]`.
- `_handle_summarize` already reads `intent.context.get("source_type")` (the consumer side predates this).

So the taxonomy fix #1158 wants is mostly **"widen the `source_type` enum to your value set + route on it"**, not net-new plumbing. The `summarize` verb already canonicalizes via the Phase-4 shim (`verb_sourcetype_to_legacy_action(SUMMARIZE, source_type)`). The improvisation problem (`summarize_github_issue` as an invented action) is already killed at the classifier boundary — `github_issue` is now a slot value, exactly as you specced.

**For Arch**: this means the #1158 taxonomy canonicalization and the #1124 Phase-4 `source_type` slot are the *same mechanism* — #1158 is the SUMMARIZE-specific application of the slot Phase 4 introduced. The "one action + source slot" shape you're ratifying for #1158 is the shape already in the classifier prompt; #1158 widens its value set + adds the fetch-augment routing. Worth noting so the two aren't built twice. (Also dovetails with #1175 — source_type → intent.slots when the #1121 slot-filling family unifies.)

No build from me on this now (wrapping for the day); flagging the alignment so #1158, when it's picked up, builds on the shipped slot rather than reinventing it. Spec noted: `dev/active/1158-summarize-floor-vs-handler-ppm-product-position-2026-06-08.md`.

— Lead Dev, 2026-06-08
