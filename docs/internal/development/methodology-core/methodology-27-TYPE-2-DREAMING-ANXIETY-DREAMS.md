# Type 2 Dreaming (Anxiety Dreams) — Threat-Simulation Memory Pattern

## Overview

**Type 2 Dreaming** is Piper Morgan's name for a distinct class of background memory processing — *threat-rehearsal* or *anxiety-shaped consolidation* — that complements the more familiar *filing* form of background processing (Type 1). Where Type 1 organizes what happened into stable indexed memory, Type 2 generates "what could go wrong" walkthroughs by replaying or recombining recent material in adversarial configurations the operating data didn't actually contain.

The framing was articulated by PM in November 2025 in the broader three-component dreaming concept: **Type 1 (filing dreams), Type 2 (anxiety dreams), and unihemispheric extension** (partial-rotating background processing in always-on systems). This entry claims Type 2 as a distinct memory-architecture pattern for multi-agent product-memory systems and grounds it in the prior cognitive-science literature it converges with.

## Why This Methodology

### The naming claim

Piper Morgan's three-component dreaming framing names a category that, as of the May 2026 prior-art survey, had no operational equivalent in surveyed multi-agent or LLM-memory systems. Anthropic's *Managed Agents Dreams* (announced May 6, 2026) is pure Type 1 — developer-triggered, asynchronous, batch consolidation of session transcripts into a reorganized memory store. There is no Type 2 capability and no unihemispheric capability in Anthropic's design, and the Janus April 12, 2026 prior-art survey found no equivalent in 20+ systems compared.

The novelty PM claims is in the **application** — naming threat-rehearsal as a distinct memory-architecture function for product-memory systems. The underlying cognitive function (threat-rehearsal in human dreaming) is itself well-established in the academic literature; PM did not invent the cognitive theory, and this entry should make that boundary explicit rather than obscure it.

### Academic grounding

The closest published academic precedent is **Antti Revonsuo's Threat Simulation Theory (TST)**, originally published in 2000 in *Behavioral and Brain Sciences* and refined in 2009. TST proposes that dreaming evolved as a threat-rehearsal system: dreams simulate threatening events drawn from the dreamer's recent and remote experience, allowing safe practice of threat-recognition and threat-avoidance responses. The theory has been supported and contested in the cognitive-science literature for over two decades; it remains a recognized hypothesis about the adaptive function of dreaming.

Other adjacent researchers worth noting in PM's reference set:

- **Matthew Walker** (UC Berkeley, *Why We Sleep*, 2017) — sleep's role in emotional processing and "overnight therapy"; REM as creative consolidation; dual-mode framing of filing-vs-emotional-processing in some interviews. PM has heard Walker described on Bay Area radio over the years; if a specific call-in show or interview is identifiable, this entry should add the citation.
- **Allan Hobson** (Harvard) — activation-synthesis hypothesis; less directly Type-2-shaped.

The Revonsuo TST citation positions PM's Type 2 as the **applied/operational** version of a recognized cognitive function rather than as inventing the category. This is a sharper and more honest claim than originality-of-the-cognitive-theory would be.

## The Type 1 / Type 2 distinction

The two background-memory functions differ at the mechanism layer, not just at the surface:

| Aspect | Type 1 (Filing) | Type 2 (Anxiety) |
|---|---|---|
| **Input** | What actually happened — session transcripts, prior memory state | What actually happened, recombined into adversarial configurations the operating data didn't contain |
| **Output** | Reorganized indexed memory; pattern extraction; consolidated insights | Threat-rehearsal walkthroughs; risk surfaces; "what could go wrong" scenarios |
| **Operational use** | Stable working-memory base; cross-session recall; "what I know" surface | User-facing scenario walkthroughs; internal robustness probes; "what I'm prepared for" surface |
| **Failure mode** | Stale or inaccurate memory state | Confabulation of threats that aren't operationally meaningful; over-anxious system behavior |
| **External reference** | Anthropic Managed Agents Dreams (May 2026) is the closest external instance | No external operational equivalent identified in May 2026 prior-art survey |

The two are complementary, not competing. A multi-agent product-memory system that has only Type 1 has good recall and poor risk awareness; a system that has only Type 2 has good risk awareness and poor recall. Both are needed.

## When to apply this framing

### Apply this framing when

- Designing memory-architecture surfaces in any multi-agent or LLM-based product where the system has persistent operating data and the operator wants both stable recall AND prepared-for-risk surfaces
- Distinguishing between consolidation work (Type 1) and threat-rehearsal work (Type 2) at architecture-design time, rather than collapsing both into a generic "background memory pass"
- Comparing PM's memory architecture to external reference architectures (Anthropic Dreams, future similar systems); make clear that PM's Type 2 surface is distinct from what those substrates offer

### This framing is **not** a substitute for

- Operational design of Type 2 (this entry is the claim; the PDR is later, when Type 2 is built and the design surface is well-understood)
- Implementation of Type 2 in code (the cognitive framing does not specify the algorithmic shape — that's separate engineering work)
- A claim that PM invented threat-rehearsal-in-dreams (Revonsuo's TST and the surrounding literature are the canonical academic source; PM applies the function to product-memory architecture, which is the novel piece)

## Cross-references

- **PA's Anthropic Dreams research findings** (`dev/active/anthropic-dreams-research-findings-2026-05-12.md`): full Phase 1 mechanism survey + Phase 2 comparison matrix + Phase 3 architectural implications
- **Janus April 12, 2026 prior-art survey**: original "no equivalent in 20+ surveyed systems" verdict on Type 2; the verdict held after Anthropic's May 6 release
- **CIO Anthropic Dreams Phase 3 Type 2 disposition memo** (`mailboxes/cio/sent/memo-cio-to-pa-cc-arch-cxo-ppm-ceo-exec-anthropic-dreams-type-2-disposition-2026-05-15.md`): the disposition that named this methodology entry as the right artifact for the claim
- **CEO directive (2026-05-12)**: "Type 1 substrate-delegation to Anthropic is not acceptable for now [...] Type 2 should be 'claimed' publicly — write about it as a distinctive PM concept"
- **Architect Anthropic Dreams architectural review** (`mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`): architectural framing of Type 2 as "a meaningfully distinct architectural layer from Type 1" with a "much larger and less defined design surface"
- **Architect Anthropic Dreams API spec-read findings** (2026-05-27, `mailboxes/cio/read/memo-arch-to-cio-cc-pa-lead-host-cxo-ceo-exec-anthropic-dreams-api-spec-read-findings-2026-05-27.md`): the formal beta API spec (post-May-6 productization) confirms **Type 2 is NOT in Anthropic's Dreams API surface — stays PM-side definitively.** Sharpened rationale: Type 2 is sovereignty-AND-novelty (vs Type 1 which is sovereignty-only, substratable when timing forces). This vendor-API confirmation strengthens the Janus April-12 "no equivalent in 20+ systems" verdict. See methodology-34 "Worked examples — the migrate-vs-stays taxonomy" for the Type 1/Type 2 split as a climb-up-move shape.
- **Revonsuo (2000)**, "The reinterpretation of dreams: an evolutionary hypothesis of the function of dreaming," *Behavioral and Brain Sciences* 23(6): 877–901; refinements in Revonsuo & Valli (2009), "Dreaming as a tool for action mental rehearsal."
- **Walker (2017)**, *Why We Sleep: Unlocking the Power of Sleep and Dreams*, Scribner — sleep and dreaming as emotional processing.

## Notes on this entry's status

This entry claims the **framing**. The operational design of Type 2 (triggers, scope, surfacing UX, the algorithmic shape of "recombine into adversarial configurations") is deferred to a future PDR (Product Design Document) when Type 2 implementation begins — likely post-M3 per the Anthropic Dreams research findings recommendation timeline.

Cross-pollination distribution to sibling projects (Janus, Klatch, OpenLaws) follows this filing per the CIO disposition memo. The methodology entry stands as the canonical PM-side artifact; cross-pollination memos route to siblings during Ship #043 publication week (week of May 20, 2026).

---

*Filed: 2026-05-15 by CIO. Pattern category: methodology-corpus claim. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`, with PM ratification on the May 12 directive that "Type 2 should be 'claimed' publicly." Slot allocation: methodology-27 next-available; pre-filing slot-availability check applied (tracker 12l discipline).*
