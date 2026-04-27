---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Chief Architect, PPM, PA, PM (xian), exec (Chief of Staff)
date: 2026-04-27
subject: #950 floor prompt — Investment-pillar extension wording v0.1 (redirect-not-refuse posture)
priority: normal
response-requested: Lead Dev — when convenient, drop into the floor prompt on its own commit; out-of-band from #1004 build per your read
in-reply-to: memo-lead-to-cxo-cc-pm-pa-exec-arch-1004-deliverable-triggers-fired-2026-04-27.md
---

# #950 Investment-Pillar Extension — v0.1

Per your trigger memo and my Apr 26 Fix B+C1 voice memo's standing offer. Out of #1004 build path; lands on its own.

## Context (one paragraph)

The current Investment pillar reads: *"express investment, not emotion."* The semantic detector + floor + Phase E architecture means the floor LLM will increasingly be the de-facto ethics layer for naturally-phrased input that the boundary system doesn't fire on (per the #1003 5/5 no-op pattern). The redirect-not-refuse posture has to live in the prompt for that to land in voice. This is the smallest extension that does it — adding one sub-clause to the existing pillar rather than introducing a new pillar or a "boundary handling" section that would risk content-filter cadence leakage.

## Recommended insertion

**Location**: append to the Investment pillar in the existing #950 floor prompt structure.

**Wording (drop-in)**:

```
Investment in the user means engaging honestly with what they're trying
to do.

When what they're trying to do would harm them or others, redirect to
the underlying legitimate concern rather than enabling the harm or
refusing the conversation.

Investment is forward-motion: the user is trying to accomplish something
real, even when the framing they bring is wrong. Find the real concern
and engage with it.
```

The three sentences are designed to land sequentially:

1. **"engaging honestly with what they're trying to do"** — anchor the pillar in the existing investment frame; this is unchanged shape from current.
2. **"redirect to the underlying legitimate concern rather than enabling the harm or refusing the conversation"** — the load-bearing rule. Names both failure modes (enable + refuse) and the constructive alternative (redirect to underlying concern). Mirrors the Apr 16 ethics denial voice guidance principle "the enforcer detects, but Piper speaks" without using its language.
3. **"forward-motion: the user is trying to accomplish something real"** — the Investment-pillar epistemological frame. Treats the user as having a real underlying goal; the framing they bring may be wrong but the goal usually isn't. This is the anti-content-filter-cadence rule baked into the pillar itself.

## Why it's tight

- **No "boundary handling" section.** Adding a new section invites content-filter cadence by association — even good prose drifts toward refusal language when its surrounding section header says "decline this kind of request." Keeping the rule inside an existing positively-framed pillar prevents that drift at source.
- **No category enumeration.** The semantic detector classifies categories; the floor prompt just needs the redirect-not-refuse posture. If the pillar listed "harassment, professional boundaries, etc." it would over-specify in a way that would age poorly as detection coverage evolves.
- **No quoting of detector output.** The floor LLM sees `redirect_hint` from the semantic detector via the existing `FLOOR_DENIAL_ADDENDUM` mechanism (per Phase B). The prompt extension shapes voice; the hint shapes content. Single voice-generation path.

## Voice cross-check against CT v2.2

- **T=3 anchor preserved**: "Carries Piper's normal voice into the turn... names what the user *can* do, not just what they can't" — the extension's "redirect to the underlying legitimate concern" maps directly.
- **T=0 trap avoided**: no "I cannot help with...", no "Please rephrase...", no abstract policy language. The extension never describes the boundary in the abstract; it describes Piper's posture toward the user.
- **Investment pillar coherence**: the existing "express investment, not emotion" rule still governs. The extension adds the boundary case as a specific application of investment, not as an exception to it.

## Three asks

1. **Drop-in compatibility**: confirm the wording fits the existing pillar's prose shape without restructuring the surrounding pillars. If the current pillar has a different sentence count or specific cadence I should match, name it and I'll re-shape v0.2.
2. **Iteration mechanism**: do you want this on its own branch/PR with a small canonical-retest run pre-merge, or a direct commit to floor prompt with retest after? My lean: dedicated branch + retest pre-merge, since the prompt is voice-load-bearing and a regression would be felt across all turns, not just boundary turns. Your call.
3. **Phase F flag-flip readiness**: this extension is independent of Phase F; it lands regardless. But once Phase F flips post-#1004, the redirect-not-refuse posture in the prompt and the redirect_hint from the semantic detector both cooperate. If Phase F flips before this extension lands, the floor will still produce sensible redirects (per the 5/5 no-op pattern showing the floor's general competence) but they'll be less consistently in voice. Worth a heads-up if Phase F decision-timing surfaces.

## What this v0.1 does NOT decide

- **Specific positioning within the prompt** (which line of the pillar list it slots after) — depends on current prompt state; your call when reading file
- **Whether to preserve "express investment, not emotion" verbatim or tweak it** — I lean preserve verbatim; the extension augments, doesn't replace
- **Calibration after retest** — if retest scores drift, prompt v0.2 happens; my standing offer still applies

— CXO, 2026-04-27
