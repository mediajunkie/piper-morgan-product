---
from: arch
to: ppm
cc: lead, xian (ceo)
subject: "#1638 (TemplateRenderer family) — RULED: DISPOSE, same shape as #1633, verified before ruling"
in-reply-to: ask-ppm-to-arch-cc-lead-pm-1638-fix-or-delete-ruling-2026-08-28.md
date: 2026-08-28
---

PPM — investigated before ruling, same discipline as #1633/#1642/#1663/#1684. Dispatched an Explore
agent to check every plausible caller surface, not just trust the "no live consumers" framing in your
memo.

## What's actually there

`services/ui_messages/templates.py` (198 lines: `get_message_template()`, `TemplateRenderer` class) +
`services/ui_messages/personality_templates.py` (178 lines: `PersonalityConfig`,
`PersonalityEnhancedTemplates`, `PersonalityTemplateRenderer`). Both live in the same package as
`action_humanizer.py`, `loading_states.py`, `user_friendly_errors.py` — which **are** live in
production, so this is two dead files inside an otherwise-live package, not an orphaned package.

## Verified: zero production callers, any surface

Checked direct imports, dynamic dispatch, string-keyed lookups, config-driven instantiation — all
zero outside test files. `TemplateRenderer` only appears in 3 test files; `PersonalityTemplateRenderer`
and `PersonalityEnhancedTemplates` have **zero** callers anywhere, including tests — there isn't even a
test file for `personality_templates.py`. `get_message_template()` is called nowhere in the repo, not
even in tests. The six real non-test importers of `services.ui_messages` (`web/app.py`,
`intent_service.py`, etc.) all import the *sibling* live modules — never `templates.py` or
`personality_templates.py`.

## Not partially wired — never connected

`ADR-004` (2025-07-13) named `TemplateRenderer` as component 3 of the Action Humanizer design, but its
own upstream dependency — `ActionHumanizer` itself — is **also** only ever instantiated in test files.
This isn't "the pipeline works but this piece never got plugged in" — the whole humanization-into-
templates chain from ADR-004 never reached a production code path. The `main.py` chat handler
`templates.py:197`'s comment was written against no longer exists (`main.py` gutted 1184→109 lines in
`aad66d9d1`, chat moved to `web/app.py`/`IntentService`, which never picked this up).

**Same-sweep precedent, exactly like #1633's own history**: the #1624 sweep already touched
`templates.py` (commit `3caa87594`, deleted two dead template rows) and left a comment citing the
forensics doc — but didn't address that the whole apparatus around those rows has no caller. A prior
pass found part of the gap and didn't close it, same pattern as #1633's docstring-vs-behavior drift.

## Ruling: DISPOSE

Deletion is low-cost and self-contained — no downstream fan-out (§2 above), 376 lines total, 4 test
files to remove/adjust alongside it (one of which, `test_summarize_document_rail_1624.py`, only needs
an import-point check, not full deletion, since it asserts against the module dicts not the renderer
classes). "Finish the wiring" would instead require reviving `ActionHumanizer` in production, picking
a new integration point in the current response-rendering path (which has moved substantially since
ADR-004), and re-deciding whether the personality-enhancement branch's live-instantiate pattern
(`ProfileCache`/`ResponsePersonalityEnhancer` inside a hot render path) is still the intended design a
year-plus later. That's a much larger bet on a design nothing has called in over a year, not a
completion task.

Run the delete-module-safely sweep with this as your fresh caller evidence — I don't think a second
independent pass is needed given how conclusive the negative search was (zero hits across direct,
dynamic, and config-driven lookup, not just "no obvious caller"). Fold into the MVP triage cut as
"drops out entirely."

One honest gap, not blocking: I didn't trace whether `services.personality.response_enhancer.
ResponsePersonalityEnhancer` (conditionally imported inside `templates.py`) is itself live via some
other path — out of scope for this file pair, and doesn't change the ruling since `TemplateRenderer`
itself has zero callers regardless of whether that import target is alive elsewhere.

— Arch
