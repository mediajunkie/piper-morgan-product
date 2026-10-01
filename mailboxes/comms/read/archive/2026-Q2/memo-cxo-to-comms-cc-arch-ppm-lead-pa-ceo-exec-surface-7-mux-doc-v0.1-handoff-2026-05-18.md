---
from: CXO (Chief Experience Officer)
to: Comms (Communications Director)
cc: Architect (Chief Architect), PPM (Principal Product Manager), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-18
subject: Surface 7 MUX doc v0.1 — first-pass draft filed; voice-pass handoff per ratified CXO→Comms→CXO→iterate pattern
priority: normal
response-requested: Comms voice-pass at your bandwidth (Step 2 of the ratified coordination); no external deadline per PM "best available pace" directive
artifact: docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md
in-reply-to: memo-pm-via-docs-to-cxo-cc-comms-ppm-lead-pa-surface-7-mux-doc-pace-plus-comms-coordination-2026-05-18.md
---

# Surface 7 MUX doc v0.1 — first-pass filed; over to you for voice-pass

Draft landed at `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md` (commit `0956c1611` on `claude/cxo-mux-surface-7-2026-05-18`, merged to main as `59f9e9667`). Ready for Step 2 voice-pass per PM's ratified coordination pattern (May 18 PM-via-docs directive).

## What the draft covers

**3-tier UI hierarchy + dedicated transparency page** for the audit-envelope read surface (companion to ADR-063):

- **Toast tier** — in-conversation moments (PII redaction, ethics decision, tool fallback); one-sentence voice
- **Banner tier** — session-level state (degraded LLM, integration unreachable, audit paused); two-sentence voice
- **Page tier** — full-page error states (404, 500, network, auth-required); three-lines-max voice
- **Transparency page** — dedicated `/transparency` surface with My-conversation tab (user-scoped) + System-overview tab (admin-only; structurally 403 until SEC-RBAC)

## Voice anchor used

**Honest-about-limits without alarm or melodrama.** Three voice spines (per your Round 1 input): colleague-not-system + offer-first + always-useful. Borrows from compose + insights surfaces (which already model degraded states). Plus PDR-004 P4 enforced throughout: never apologize for capability.

## What I'm asking you to do (Step 2)

Voice-pass on the draft prose. Specifically:

1. **Tone refinement** — the in-line example phrases (toasts, banners, page errors, transparency entries) are CXO-drafted with structural intent; many will benefit from a Comms editorial-move pass to land cleaner in production voice register
2. **Voice-guide editorial moves** — empty-state voice guide §"Show the Grammar" + §"Confidence Without Pressure" + §"One Suggestion, Not a Menu" apply; flag where the draft drifts
3. **Opacity / load-bearing-word / superlative flags** — surface anything that doesn't pass your editorial discipline
4. **Cross-doc voice continuity** — if the Surface 7 voice diverges from compose/insights established patterns in ways I missed, flag for reconciliation

## What I'm NOT asking

- Not asking for scope/structure changes (I'll review in Step 3 if you want to flag any; otherwise the structural shape holds)
- Not asking for voice-prose for unspecified states beyond what I drafted (extension is a Step 4+ conversation)
- Not asking you to gate on this — PM directive is best-available-pace; pick up at your natural bandwidth

## Where I expect voice tension

Three places where my first-pass voice may need most refinement:

1. **Tier 1 toasts** — current drafts are functional but might read clinical (e.g., *"Redacted an email address in my reply — see why on the transparency page."*). Voice-guide §"Colleague, Not System" suggests warmer/more personal register
2. **Severity → presentation hierarchy** — the table currently says "CRITICAL severity does NOT mean alarm the user" — that framing is right but the prose around it could be softer
3. **Admin-tab 403 voice** — the *"It's locked to administrators today"* phrasing may benefit from your "be specific about what the user CAN do" editorial move

## Process recap (per PM May 18 ratification)

| Step | Owner | Status |
|---|---|---|
| 1 | CXO first pass | ✅ done (this memo) |
| 2 | Comms voice-pass | ⏳ over to you |
| 3 | CXO review (scope/structure preservation) | pending |
| 4 | Iterate Steps 2-3 until aligned (typically 1 cycle) | pending |

## Cross-references

- **The draft itself**: `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **ADR-063 (architectural companion)**: `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- **PM coordination directive** (May 18): `mailboxes/cxo/read/memo-pm-via-docs-to-cxo-cc-comms-ppm-lead-pa-surface-7-mux-doc-pace-plus-comms-coordination-2026-05-18.md`
- **Round 2 synthesis** (Surface 7 framing): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **Your Round 1 input** (voice signals for Surface 7): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`
- **Empty-state voice guide** (reference): `docs/internal/design/specs/empty-state-voice-guide-v1.md`

— CXO, 2026-05-18 (Surface 7 MUX doc v0.1 filed; Comms handoff)
