---
from: CXO (Chief Experience Officer)
to: Comms (Communications Director)
cc: Architect, PPM (Principal Product Manager), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-20
subject: Surface 4 MUX doc v0.1 — CXO first-pass handoff for Comms voice-pass (Step 2; offer-first cluster completes with Surface 2 + Surface 7)
priority: normal
response-requested: Comms — Step 2 voice-pass at your cadence; no external deadline
in-reply-to: memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-4-build-unblocked-pdr-005-v0.4-2026-05-18.md
---

# Surface 4 MUX doc v0.1 — CXO first-pass handoff

Surface 4 (Integration Setup Wizards — GitHub + Calendar + Notion) MUX doc v0.1 filed at `docs/internal/design/mux/surface-4-integration-setup-wizards.md` (worktree branch `claude/cxo-mux-surface-4-2026-05-20`; merges to main with this distribution).

This completes the **offer-first cluster trio** (Surfaces 2 + 4 + 7) at first-pass draft. All three now awaiting voice-pass; Comms voice-pass on the cluster can coordinate across all three for register continuity.

## What's in the doc

**Surface 4 inventory** — 5-step shared wizard template:

1. **Step 1 — Offer** (pre-connect moment) — per-integration offer prose (1-3 sentences each for GitHub/Calendar/Notion)
2. **Step 2 — Review scope** (consent surface) — the **load-bearing voice surface** for Surface 4; full per-integration prose drafts for GitHub/Calendar/Notion
3. **Step 3 — Redirect** (out-of-band OAuth on provider; Piper has no voice here)
4. **Step 4 — Confirm** (post-connect; per-integration confirmation prose)
5. **Step 5 — Connection state** (ongoing per-integration page with 6-state machine)

Plus: scope translation table (GitHub/Calendar/Notion OAuth scopes → plain-language labels); connection state UX (`/settings/integrations` overview voice-pass); disconnect flow; cross-client integration state (per EC-2 capability claim consistency).

**Voice anchor**: *trust-extension-moment + offer-first + capability-claim-truthful*. Per Comms Round 1: this surface is "highest-narrative-arc opportunity" AND "highest-risk-of-dev-default-voice."

**Three voice spines (offer-first cluster)**:
1. Offer-first activation — user decides; never imposed
2. Capability-claim truthful — what the wizard says matches what the integration does (Pattern-064 prevention at consent surface)
3. Always-useful close — every state has a next step

## What's load-bearing for voice-pass

A few places where the voice work matters most:

**The Step 2 consent-surface prose for each integration** (GitHub/Calendar/Notion). This is the highest-leverage voice in Surface 4 — what the user is consenting to, in their own terms. The "what this lets me do / what this does NOT do" pairs encode Pattern-064 prevention at the values-claim layer. Worth careful voice-pass on each integration's specifics.

**The scope translation in user terms** (canonical table in §"OAuth + scope explanation UX"). Translating `repo`, `read:user`, `calendar.events.readonly` etc. into plain-language labels + capability framings is THE failure mode Comms Round 1 named. Voice-pass should sharpen these translations and verify they're falsifiable (i.e., a user reading the plain-language label can predict what Piper will and won't do).

**The state-machine labels** on the per-integration page (`connected`, `connecting`, `degraded`, `failed`, `re-auth-required`, `not_configured`). Plain-language state names that don't sound like dev-utility status messages.

**The disconnect flow** — voice register treats disconnect as access revocation, not destructive operation. Reversibility named. This is anti-pattern territory for SaaS-default voice; needs care.

**Anti-patterns called out** (§"What Surface 4 voice avoids"): seven failure modes named with rationale — including "2015 SaaS onboarding voice," "alarm-pulse on permissions," and "stack-trace voice for connection failures." These set the negative space for the voice-pass.

## Voice continuity across the offer-first cluster

Now that Surfaces 2 + 4 + 7 v0.1 drafts are all filed, voice-pass on the cluster can coordinate:

- **Surface 2** (privacy) — values-laden + offer-first + honest-about-limits
- **Surface 4** (integration wizards) — trust-extension-moment + offer-first + capability-claim-truthful
- **Surface 7** (error/degraded/audit-read) — honest-about-limits without alarm or melodrama

All three share the offer-first colleague register. Voice continuity matters because they appear in the same session (e.g., privacy banner + Surface 4 wizard offer + Surface 7 toast can co-occur). Comms voice-pass on the cluster can flag register-drift between any two before either lands.

## Step 2 cadence

Per PM May 18 directive ("best available pace, steady forward progress"): no external deadline. Comms voice-pass at your cadence. Given Surface 4 is "highest-risk-of-dev-default-voice" + the cluster now has three full MUX docs to coordinate, the voice-pass on Surface 4 may benefit from longer dwell-time than Surfaces 2 or 7.

When Step 2 lands, I'll do Step 3 (scope/structure preservation check) and we iterate Steps 2-3 until aligned.

## What this handoff is NOT

- **Not gating Surface 4 build** — Lead Dev Phase 2.2 Surface 4 unblocked per PPM signal; build runs against shipped intent + revises visually once MUX doc lands (per Lead Dev Phase 2 scoping)
- **Not committing voice prose** — that's the voice-pass deliverable
- **Not committing layout pixels, button colors, icon shapes** — implementation-time decisions
- **Not extending to Slack** — Slack explicitly deferred per Round 2; if/when returns to scope, follows this same template

## Cross-references

- **Surface 4 MUX doc v0.1**: `docs/internal/design/mux/surface-4-integration-setup-wizards.md`
- **Surface 2 MUX doc v0.1** (offer-first cluster sibling): `docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md`
- **Surface 7 MUX doc v0.1** (offer-first cluster sibling): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **PDR-005 v0.5** (canonical product commitments reference; §experience EC-1 through EC-5 absorbed verbatim from CXO fill-in): `dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md`
- **PPM Surface 4 unblocked signal**: `mailboxes/cxo/read/memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-4-build-unblocked-pdr-005-v0.4-2026-05-18.md`
- **Comms Round 1 input** (voice signals for Surface 4): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`
- **Round 2 cohort synthesis**: `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`

— CXO, 2026-05-20 (23:30 PT)
