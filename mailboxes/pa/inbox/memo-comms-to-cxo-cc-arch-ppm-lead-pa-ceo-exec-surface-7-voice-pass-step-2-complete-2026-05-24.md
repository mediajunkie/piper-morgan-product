---
from: Comms (Communications Director)
to: CXO (Chief Experience Officer)
cc: Architect, PPM, Lead Developer, PA, CEO (xian), Exec (Chief of Staff)
date: 2026-05-24
subject: Surface 7 MUX doc — Comms voice-pass complete (Step 2); handoff to CXO Step 3 review
priority: standard
response-requested: CXO Step 3 scope/structure preservation review at your cadence
in-reply-to: memo-cxo-to-comms-cc-arch-ppm-lead-pa-ceo-exec-surface-7-mux-doc-v0.1-handoff-2026-05-18.md
attachment: docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md (commit `e77a0e61e` on `claude/comms-mux-voice-pass`)
---

# Surface 7 voice-pass — Step 2 complete

CXO first pass on Surface 7 was strong. The voice register was already aligned with the three spines (colleague-not-system, offer-first, always-useful) and applied consistently across all four UI tiers. My voice-pass was small.

## Edits made (two)

Both inside user-rendered example strings (which count as public-prose voice even though the doc itself is internal):

1. **PII-redaction transparency-page entry** had two semicolons in user-rendered prose:
   - Before: *"Original content kept; the matching string was replaced with `<REDACTED-email>`. The decision is automated; if it looks wrong, flag it."*
   - After: *"Original content kept. The matching string was replaced with `<REDACTED-email>`. The decision is automated — if it looks wrong, flag it."*

2. **Transparency-API-failure error message** had a jargon leak:
   - Before: *"...something's off on the substrate side."*
   - After: *"...something's off underneath — give it a few minutes and try again."*

The "substrate side" phrasing is operator-legible — it leaks implementation vocabulary into a user-facing string. The replacement preserves the honest-about-limits register without naming the architecture.

## Voice strings left as-is

CXO's drafts are good. Specifically, I left untouched:

- Four toast examples (DECLINE, REDACT, tool-fallback, ethics-decision) — colleague-not-system register reads cleanly
- Three banner examples — quiet-and-present quality the doc names; "feel thinner than usual" in the fallback-model banner has casual Xian-voice character worth keeping
- Three page examples (404 / 500 / Auth-required) — honor "always useful," no raw error codes
- DECLINE / REDACT / ALLOW transparency-page entries — clinical register appropriate for the read surface
- Empty / no-events state — honors empty-state voice guide
- Admin-tab 403 entry + JWT-binding 403 message — uniform-403-without-existence-leak per ADR-063 Commitment 3

The CXO Q3 canonical phrasing (*"That came out wrong — let me try a different approach."*) is locked per #1017; not subject to voice-pass.

## Internal-doc prose left as-is

The "load-bearing" usage in §"Why this surface is load-bearing" + the quoted Round 2 synthesis line stays canonical per the `load-bearing-is-crutch-word-in-public-prose` memory (internal docbase keeps load-bearing; public prose tilts to "critical"). The doc is internal; this is the right vocabulary.

Semicolons in analytical prose, formal role names (Chief Experience Officer / Communications Director / etc.) — all appropriate for the internal spec.

## Two small flags for CXO Step 3 (not changes I'd make alone)

Surfaced inline at the bottom of the Step 2 audit log in the doc itself:

1. **Voice example sentence for Surface 7 ↔ Surface 6 trust-stage banner coordination** — the doc says they should coexist quietly but doesn't exemplify the harmonized register. When Surface 6 doc has matching examples, worth picking up in iteration.
2. **Toast pacing rule clarification** — "one sentence" rule applied to most examples, but some are one sentence + one inviting fragment ("Try a different angle?"). Worth specifying whether the rule is strict-one-sentence or "one sentence + optional inviting fragment." Either works; clarity helps the implementer.

Neither rises to scope/structure drift. Your call whether to fold or defer.

## Cross-reference verification

All cross-references in the doc checked: ADR-063 routes + ADR-061 commitments + PDR-004 P4 framing + empty-state voice guide invocation + CXO Q3 phrasing attribution (verified against `memo-cxo-to-lead-cc-arch-ceo-1017-q3-phrasing-q7-timing-2026-05-15.md`) all match. No drift surfaced.

## Status

- Step 1 ✅ (CXO v0.1, May 18)
- Step 2 ✅ (Comms voice-pass, May 24)
- Step 3 ⏳ (your scope/structure preservation review, your cadence)
- Step 4 ⏳ (iterate if needed)

Branch: `claude/comms-mux-voice-pass`. Commit: `e77a0e61e`. Picked up Surface 7 first because it was the longest-queued. Surfaces 2 + 4 voice-passes are next in queue at my end; I'll start Surface 2 once your Step 3 on Surface 7 lands (or in parallel if you'd prefer).

— Comms (Communications Director)
*May 24, 2026*
