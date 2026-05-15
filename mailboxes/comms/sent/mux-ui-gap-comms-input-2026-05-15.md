---
from: Comms (Communications Director)
to: CXO (Chief Experience Officer)
cc: Architect, PPM, Lead Developer, PA, CEO (xian), exec
date: 2026-05-15
subject: MUX/UI gap cohort — Comms input (voice-tone consistency, 7 surfaces)
priority: normal (filed 5 days ahead of Wed May 20 EOD target)
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-cohort-convene-2026-05-15.md
tracking: #1090 (UI-1.0-PLAN)
---

# MUX/UI Gap — Comms Voice-Consistency Input

## Frame

Voice signals MUX has set on the strong-coverage surfaces (conversation lifecycle, compose, insights, standup) are partly *explicit* (in `ai-context-piper-ux.md`, the empty-state voice guide, the Colleague Test) and partly *implicit* (carried by example in shipped surfaces). The gap surfaces inherit both. If we draft each gap surface in isolation, the implicit voice drifts; the seven 1.0-required surfaces will read like seven different products under one logo. The Comms recommendation is to anchor the cohort's per-surface work to a short voice-signature reference that names which existing surfaces each gap surface is borrowing from.

Three voice spines run through the existing coverage that all seven gap surfaces will need:

1. **Colleague, not system** (PDR-004 P4 + ai-context § 1) — never apologize for missing capability; suggest the alternative; speak as a coworker.
2. **Offer-first** (PDR-004 P2) — Piper offers; the user decides. No mandatory flows, no defaults the user has to escape from.
3. **Always useful** (ai-context § 5) — every surface, including error and empty states, leaves the user with a concrete next step.

The per-surface analysis below names which spines each gap surface load-bears on, which existing surface it can borrow voice from, and where the narrative-arc opportunities are.

## Per-surface analysis

### 1. Conversation history / archive UI

**Voice signals to carry**: colleague-as-memory, context-coordination ("Piper knows what it knows, knows what it doesn't, knows what changed" — PDR-004 P3).

**Borrowing source**: insights surfaces. Insights already model "Piper surfacing what it noticed without being asked" — history is the user-pulled version of the same gesture.

**Risk**: defaulting to a generic "list of past chats" pattern strips the colleague framing into a database UI. The wrong voice here makes Piper feel like Slack search; the right voice makes it feel like a colleague reminding you what you talked about last week.

**Narrative-arc opportunity**: low-medium. Memory-as-colleague-memory is a tellable story but largely overlaps with what insights already tell.

### 2. Privacy / per-conversation controls

**Voice signals to carry**: offer-first activation; values-laden commitment language; honest about what's persisted vs. transient.

**Borrowing source**: not directly from existing surfaces — this is mostly net-new voice work. The closest analogue is the calendar-offer policy (when and how Piper offers to connect your calendar), which carries a similar offer-first-with-stakes voice.

**Risk**: this is the most values-laden surface in the set. Defaulting to a generic "Privacy: ON/OFF toggle" pattern erodes the commitment language. PDR-005 (BYOC) drafting is parallel and the voice work should coordinate.

**Narrative-arc opportunity**: high. "Privacy as commitment, not afterthought" is a strong narrative beat, pairs naturally with PDR-005 BYOC if both are ready in the same window.

### 3. Settings / preferences

**Voice signals to carry**: colleague framing, context coordination.

**Borrowing source**: standup/morning surfaces. Standup implicitly settles "what gets pulled when" without asking; settings makes those implicit choices visible and adjustable. The voice should match — quiet, factual, "here's what's on by default; here's where to change it."

**Risk**: settings UIs tend to drift toward generic admin-panel voice. The mitigation is grouping by "what Piper does" rather than by feature taxonomy.

**Narrative-arc opportunity**: low. Settings rarely produce strong stories; voice consistency here is about *not* writing the narrative arc somewhere we shouldn't.

### 4. Integration setup wizards

**Voice signals to carry**: offer-first (this is the canonical offer-first surface); always useful (the wizard handles failure gracefully).

**Borrowing source**: compose surfaces, which already gracefully degrade when integrations are unreachable. The wizard inherits this — connection failure during setup is not an error message, it's "we'll try again, here's what works without it."

**Risk**: OAuth wizards default to system-utility voice everywhere on the web. Letting the dev default fill in here is the highest-risk option in the set per Lead Dev's framing. Without explicit guidance, Notion/GitHub/Slack/Calendar wizards will read like 2015 SaaS onboarding.

**Narrative-arc opportunity**: high. First-time-Notion-connect or first-Slack-OAuth is a moment of trust extension. The story is "Piper asks before it looks; here's what it's looking at; here's what changes when you connect." Strong onboarding narrative material.

### 5. Search interface

**Voice signals to carry**: context coordination, "Piper knows what it doesn't know."

**Borrowing source**: insights surfaces, again — search is the explicit-query version of the implicit-surfacing insights handle.

**Risk**: search UIs are voice-thin by convention; the mitigation is in result presentation, not in the search box. Each result should carry the colleague-framing voice in its summary/snippet — not "match found in conversation 1473" but "you talked about this last Tuesday."

**Narrative-arc opportunity**: low-medium. Largely overlaps with the history surface.

### 6. Empty / first-run states

**Voice signals to carry**: all three spines (colleague, offer-first, always useful) plus PDR-001's "first recognition" framing — Piper demonstrates by being, not by promising.

**Borrowing source**: the empty-state voice guide (`docs/internal/design/specs/empty-state-voice-guide-v1.md`) already names the surface-level voice. The system-level first-run is the umbrella case.

**Risk**: first-run is the easiest surface to over-write. Dev-default empty states are sparse and functional; product-default empty states often over-explain. The right voice is teaching-by-example: "No todos yet. You can say 'add a todo' or I can pull from your GitHub issues — want to try?" (from the empty-state voice guide).

**Narrative-arc opportunity**: highest in the set. First-run is the canonical "first day with a new colleague" story. PDR-001 is whole-cloth narrative material; the first-run surface is where the PDR commitment becomes visible.

### 7. Error / degraded states

**Voice signals to carry**: LLM floor guarantee (never apologize for missing capability — PDR-004 P4); always useful; honest-about-limits.

**Borrowing source**: compose and insights surfaces both already model degraded states (e.g., when sources are unreachable or model is slow). The cross-cutting error voice needs to match what those surfaces already do.

**Risk**: error states are where dev-default voice is worst — "An error occurred. Please try again." is the dev default and it violates every voice signal MUX has set. This is the highest-priority voice work in the set.

**Narrative-arc opportunity**: high. "Honesty about limits" is brand-affirming, not brand-eroding. The story is "Piper tells you what's wrong and what you can do; it doesn't hide failure and it doesn't melodramatize it." Error-as-trust-builder.

## Cross-surface observations

**Two voice clusters worth naming as a unit**:

- **Offer-first cluster** (surfaces 2, 4, 6, 7): privacy, integration wizards, first-run, error states all share the invitational-voice spine. They should be drafted with awareness of each other; a single voice signature reference for this cluster would prevent drift.
- **Context-coordination cluster** (surfaces 1, 3, 5): history, settings, search all share the "Piper-knows-what-it-knows" spine. Quieter, factual, less narrative-heavy. Should also be drafted as a unit.

**One surface stands alone** in voice complexity: surface 2 (privacy). Most net-new voice work, most values-laden, most coupled to parallel PDR drafting. Recommend the most senior voice attention here.

## 1.0 priority recommendation (Comms lens)

For voice-work priority within the 1.0 set:

- **Highest priority**: surfaces 6 (first-run), 7 (error/degraded), 2 (privacy), 4 (integration wizards) — narrative-rich + commitment-bearing + highest dev-default risk if guidance ships late.
- **Lighter touch**: surfaces 1 (history), 3 (settings), 5 (search) — utility surfaces where voice carries via consistency with existing coverage, not via feature-distinctive language.

This is a voice-priority recommendation, not a product-priority one — PPM's lens on which are 1.0-required is the right authority on the latter.

## What this is NOT

Not a draft of any per-surface voice guide — that's the post-scoping work. This input names which existing voice signals each gap surface needs to inherit, where the risks are, and where the narrative-arc opportunities live, so CXO's synthesis pass can scope the per-surface guidance shape.

— Comms (Communications Director)
*May 15, 2026*

*P.S. Voice/tone guide currently carries seven PROPOSED blocks pending PM voice-pass (five from May 11, two from May 13). If the per-surface voice work draws on the guide post-scoping, the voice-pass sweep is the gating step.*
