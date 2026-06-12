---
from: CXO (Chief Experience Officer)
to: PM (xian)
cc: Lead Developer, PPM (Principal Product Manager)
date: 2026-06-12
subject: Radar umbrella-vs-peer — CXO confirms A (umbrella), and "eventually A" is exactly right: ship the cards now, introduce the Radar framing as the ambient zone gains streams
in-reply-to: memo-lead-to-ppm-cxo-cc-pm-radar-umbrella-vs-peer-pm-leans-a-2026-06-12.md
priority: standard — your load-bearing start-screen IA decision
response-requested: none — CXO read; PPM weighs the taxonomy side
---

# CXO read: A (umbrella), and your "eventually" instinct is the sequencing, not a hedge

**Confirm A.** Three experience reasons, then the sequencing that makes "eventually A" precisely right.

## Why umbrella (the experience case)

1. **One mental model vs. N.** Umbrella gives the user a single idea — *"Radar = where Piper shows me what it's keeping an eye on for me."* Peer makes the user mentally group What-I'm-seeing + Recently + watch-fires themselves; the product should do that grouping, not outsource it.
2. **"Radar" becomes UVP vocabulary.** Umbrella turns Radar into a *word for the trusted-colleague-watching behavior* — a name the user (and we) can speak ("it's on my radar", "Piper put it on my radar"). Peer wastes that — it's just another card label. Naming the distinctive behavior is exactly the being-good/MUX move.
3. **The form-factor story only works under umbrella (my lane).** On a small screen, an umbrella **collapses to one summarized surface** — *"3 things on your radar"* — that expands on tap. Peer modules each compete for vertical space with no natural collapse. Umbrella has a clean responsive-collapse story (one surface, summarized→expanded); peer fragments and forces scrolling. Cross-form-factor composition is the reason to prefer A beyond aesthetics.

## Why "eventually A" is the sequencing (not a hedge)

Lead confirms A-vs-B is composition/naming, not a rebuild (both live modules already share the Card chrome). So the destination is A; the question is *when the umbrella label earns its keep.* With only **two** ambient modules today (Places, Recently), the umbrella is light. With **watch-fires (#1181) + prepared-for (#1166) + drift** it's load-bearing — that's when "Radar" names something with real internal variety. So:

- **Now**: keep the cards (built), but **group the two ambient cards under a light "Radar" zone heading** — *don't* leave them isolated. This forms the mental model early so users don't have to re-learn when watch-fires arrive. Cheap (a section label), and it's the seed of the umbrella.
- **As streams land** (#1181/#1166): the zone fills, "Radar" graduates from section-label to genuine umbrella surface with the responsive-collapse behavior.

So **A is the destination, the light-zone-heading is the now, and the transition is free** — your "eventually A" is the right read.

## One connection for your IA session

**#313 tagging's "three taxonomies" question (tags / projects / MUX-lifecycle) is the same organizing-model decision as this** — both are *"how is the user's stuff structured."* Recommend the start-screen IA session covers both together (the "Your stuff" IA): surfaces (Radar/ambient) + organizers (tags/projects) are one coherent model, not three. I've sent Lead my #313 disposition (freeform-with-emergent-promotion; tags + projects as the only two user-facing organizers, lifecycle invisible) — it's built to fold into this session.

— CXO, 2026-06-12
