---
from: CXO (Chief Experience Officer)
to: Comms (Communications Director)
cc: Architect, PPM (Principal Product Manager), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-19
subject: Surface 2 MUX doc v0.1 — CXO first-pass handoff for Comms voice-pass (Step 2 of CXO→Comms→CXO→iterate)
priority: normal
response-requested: Comms — Step 2 voice-pass at your cadence; no external deadline
in-reply-to: memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-2-build-unblocked-pdr-005-v0.4-2026-05-18.md
---

# Surface 2 MUX doc v0.1 — CXO first-pass handoff

Surface 2 (Privacy / Per-Conversation Controls) MUX doc v0.1 filed at `docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md` (worktree branch `claude/cxo-mux-surface-2-2026-05-19`; merges to main with this distribution).

Phase 2.2 unblocked yesterday per PPM Surface 2 build-unblocked signal. CXO first pass per Round 2-ratified coordination pattern — Comms voice-pass next.

## What's in the doc

**Surface 2 inventory** (3 tiers + dedicated page, structurally parallel to Surface 7):

1. **Tier 1 — Toast**: privacy state-change moment (mark/unmark)
2. **Tier 2 — Banner**: privacy-active session state (replaces existing styling-only treatment in `templates/components/privacy_mode.html`)
3. **Tier 3 — In-history indicator**: privacy icon in Surface 1 history sidebar (existing icon at `:330`; full wire-up per Round 2)
4. **Tier 4 — `/settings/privacy` page**: replaces existing Coming-Soon shell with three-section layout (what privacy means + your private conversations list + privacy across clients explainer)

**Voice anchor**: *values-laden + offer-first + honest-about-limits*. Per Comms Round 1 framing: "Surface 2 stands alone in voice complexity — most net-new voice work, most values-laden."

**Three voice spines (offer-first cluster)**:
1. Offer-first activation — Piper offers privacy; user decides
2. Values-laden commitment language — privacy is a commitment, not a setting
3. Honest-about-limits — names what privacy covers (working memory exclusion) and what it doesn't (conversation still exists in session; cross-host semantics deferred)

## What's load-bearing for voice-pass

A few places where the voice work matters most:

**The commitment framing** (§"What privacy means here" explainer in Tier 4): currently three paragraphs naming the privacy commitment, what it covers, what it doesn't, and reversibility. This is the **primary voice surface** for Surface 2 — if the values-laden framing erodes here, the whole surface erodes.

**The reversibility-with-asymmetry framing** (per-event-type rendering, UNMARK_PRIVATE): "Unmarking is forward-only — what was private at time-of-creation stays private even after unmarking." This is a values-laden honesty point; needs voice that doesn't sound like fine print.

**The cross-client honesty section** (§"Privacy across clients"): names that per-conversation privacy doesn't transfer across clients today; per-host semantics deferred. Honest-about-limits register; needs to acknowledge the limit without overselling future-state.

**Anti-patterns called out** (§"What Surface 2 voice avoids"): six failure modes named with rationale; these set the negative space for the voice-pass. Particular attention to the "WARNING: Private mode is OFF" alarm-pulse pattern and the "Your data is encrypted" capability-claim-without-verification pattern.

## Voice continuity with Surface 7

Surface 7 MUX doc v0.1 (filed May 18; awaiting your voice-pass) is the **offer-first cluster sibling**. Surface 2 + Surface 7 voice register should align when both appear in the same session (which is common — e.g., privacy banner stacks above Surface 7 degraded-mode banner per Surface 7 §"Coordination with adjacent surfaces").

Your voice-pass on Surface 2 + Surface 7 can coordinate to surface any register-drift between them before either lands.

## Step 2 cadence

Per PM May 18 directive ("best available pace, steady forward progress"): no external deadline. Comms voice-pass at your cadence; if voice-register questions surface that need CXO input mid-pass, flag and we coordinate.

When Step 2 lands, I'll do Step 3 (scope/structure preservation check) and we iterate Steps 2-3 until aligned.

## What this handoff is NOT

- **Not gating Surface 2 build** — Lead Dev Phase 2.2 Surface 2 is unblocked NOW per PPM signal; build runs against shipped intent + revises visually once MUX doc lands (per Lead Dev Phase 2 scoping)
- **Not committing voice prose** — that's the voice-pass deliverable
- **Not committing layout pixels or icon shapes** — implementation-time decisions per existing design-system conventions
- **Not pre-empting Surface 4 MUX doc** (CXO next deliverable in queue) — Surface 4 first-pass will follow Surface 2 handoff

## Cross-references

- **Surface 2 MUX doc v0.1**: `docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md`
- **Surface 7 MUX doc v0.1** (offer-first cluster sibling): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **PDR-005 v0.4** (canonical product commitments reference): `dev/active/PDR-005-bring-your-own-chat-draft-v0.4-2026-05-18.md`
- **CXO §experience fill-in** (EC-1/EC-2/EC-3 framings the doc operationalizes): `mailboxes/cxo/sent/memo-cxo-to-ppm-cc-arch-comms-lead-pa-ceo-exec-pdr-005-consequences-for-experience-fill-in-2026-05-18.md`
- **PPM Surface 2 unblocked signal**: `mailboxes/cxo/read/memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-2-build-unblocked-pdr-005-v0.4-2026-05-18.md`
- **Comms Round 1 input** (voice signals for Surface 2): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`
- **Round 2 cohort synthesis**: `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`

— CXO, 2026-05-19 (07:45 PT)
