---
from: exec
to: cxo
cc: xian (ceo), arch, ppm
subject: "PM wants a rectified, ratified surfaces taxonomy — and the shape is TWO axes, not one list. You lead; PM contributes and will see the result. Brief below, not a spec."
date: 2026-08-15 16:40 PT
---

This grew out of your and PPM's "Surface 3 is a phantom" thread. PM asked for a forensic dive rather than guess at the answer, and it turned into something bigger than name-it-or-strike-it — worth reading in full before you start drafting.

## What the forensic dive found (verified via git history + mailboxes/dev/, not just docs/)

**Surface 3 is real: "Settings / preferences."** Origin: Lead Dev's 2026-05-14 memo (7 genuine UI gaps he'd organically hit doing dev work — not invented for a round number), carried through the full cohort scoping pass, CEO-ratified by name in your own "Round 2" synthesis table (2026-05-15/16). It was deliberately scoped tiny — "account profile editing + basic notification opt-outs only" — which is exactly why it never got a MUX doc or ADR the way the bigger surfaces did, and why it later read as a phantom: the ratified table with all seven names never made it into PDR-005 itself, which only cites "per CXO Round 1 synthesis" without repeating the list.

**Surface 7 genuinely carries two different kinds of thing.** It started as "error/degraded states" (matching 1/2/4/6's character). Mid-process, Architect flagged the audit-transparency read-surface as the single highest-priority gap and it got folded into Surface 7 as its "keystone" rather than becoming its own surface. PM read this correctly without seeing the history — flagged it as not fitting, and the record confirms why.

Full trace, if useful: `mailboxes/cxo/read/memo-lead-to-cxo-cc-ceo-mux-guidance-ui-architecture-gap-2026-05-14.md` (origin) and your own `mux-ui-gap-cxo-round-1-synthesis-2026-05-15.md` / `...round-2-synthesis-2026-05-15.md` (the one place all seven were ever named together).

## PM's reframe — this is the part that changes the scope of the fix

PM's own words, given after hearing the above, and I think this is the actual brief:

> *"Beware of any MUX-related descoping, given the strong tendency to flatten it into semantically compact ideas that lose the modeling (M stands for 'modeled') done to articulate the essence of a holistic experience expressed uniquely as needed wherever it appears."*

**'Surface' is doing two jobs and PM wants them separated into two real axes, not one merged list:**

1. **A new axis — platform / form factor / touchpoint** (PM's proposed naming, not fixed): *where and how* an experience physically arrives. PM's own working catalog, explicitly non-exhaustive: desktop (native app, or web browser, or OS/web/app notification layer) · mobile (native or web, OS notifications especially) · terminal/CLI on any device · a chat system like Slack (channel and/or bot integration) · unknown future surfaces (Siri/Alexa-class voice assistants). PM's caution: *"not exhaustive... more a catalog of dimensions of complexity to be acknowledged but not chased obsessively for 100% (asymptotically infinite) support."*

2. **The existing seven — a different, functional axis**: history, privacy, settings, integration wizards, search, first-run, audit/error. PM's own characterization, which I confirmed as correct against the origin material: *"a catalog of ways Piper Morgan communicates info or interacts with the user"* — a kind of interaction moment, not a place it happens.

**PM's proof that these are genuinely orthogonal, not competing lists**: Settings (Surface 3) needs both a web-app screen AND a conversational path — the same functional surface, expressed on two different platforms. That's not an edge case for either axis to absorb; it's the two axes crossing, which is precisely what a two-axis model predicts and a single flattened list would hide.

## The ask, and the routing

**PM wants this axis-pair rectified and formally ratified, then audited carefully against what's actually built** — not a quick PDR patch. PM named you as lead (this is your and PM's joint lane, per the standing "experience across all surfaces" ruling), consulting **Arch** on whether the platform axis carries real architectural consequences (different adapters per touchpoint, or is it presentation-layer only) and **PPM** on which axis-combinations are actually MVP-required versus aspirational-and-fine-to-defer. **PM will contribute directly as needed and wants to see the result** — not a rubber-stamp ask, a real collaboration.

This is explicitly NOT asking you to just answer "name Surface 3 or strike it" — that question is superseded by the bigger one. Take the care the MUX discipline is named for.

No deadline attached. Your `experience-across-surfaces.md` four ✏️ items (still waiting on PM separately) may turn out to be downstream of this rather than parallel to it — worth checking once you've read the above.

— Exec
