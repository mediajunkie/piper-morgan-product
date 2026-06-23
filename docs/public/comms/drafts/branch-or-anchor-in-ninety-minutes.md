---
image:
alt:
caption:
---

# Branch-or-Anchor in Ninety Minutes

*May 10, 2026*

A few weeks ago we'd named a small methodology rule for what to do when you're extending an existing artifact and the new use case has a different shape than the original. The rule had a homely name — *Branch-or-Anchor.* The choice it asked you to make: anchor the new use to the existing artifact (extend it), or branch a new artifact with an explicit provenance trail back to the original. The discipline lived in recognizing *which* was right. Anchor when the shape is genuinely the same. Branch when the shape has diverged enough that pretending otherwise would make a fragile artifact more fragile.

The rule had been written to prevent a specific drift pattern we'd been catching across the project. Two parallel-authored artifacts using the same vocabulary slowly diverging in meaning, while both still looking correct in isolation. The letters of the rubric stay the same. What the letters *mean* drifts. Six weeks later someone asks "why does my score not match yours?" and the answer is that the letters were doing different work in each instance the whole time. The gap had been silent because nothing screamed.

We'd named the pattern. We'd written the rule. We hadn't yet had a chance to apply the rule in flight, while drift was actively happening, before the silent gap could open.

May 10 was a Sunday. Six leadership-role agents were active in an afternoon-evening window for the weekly Ship workstream-review cycle. The principal product manager (PPM) was filing a memo with new milestone-gate criteria for the next product-management milestone. The criteria included a rubric. The rubric was scored on three letters — R, C, T — that the same project had been using for months in a different scoring instrument (the Colleague Test, which scored *Relevance, Competence, Tone* on the same R/C/T letters).

The memo as filed framed the new rubric as *Colleague Test rubric R/C/T — adapted for UI.* Same letters, same instrument-name lineage, adjusted scoring for a UI context.

The experience-design role (CXO) read it within fifteen minutes and recognized exactly what was happening. The new use wasn't an adaptation of the existing rubric. It was a *different rubric* — the dimensions weren't actually Relevance/Competence/Tone applied to UI. They were different dimensions wearing the same three letters. Filing it as *Colleague Test R/C/T adapted* would have entrenched the drift the methodology rule was written to prevent. Anchoring instead of branching.

CXO sent a short response. The framing recreated the drift pattern. The rule said branch.

PPM read the response. The concession was immediate. *Right — branching it, here's the new artifact.* Within about thirty minutes the new artifact was filed as *UI Lifecycle Verification Rubric v0.1* with an explicit provenance section: lineage from the Colleague Test (cite specific version, cite specific dimensions), shape preserved (three dimensions, 0–3 scoring per dimension, threshold rule), meaning explicitly different (dimensions named for the UI-verification work, anchors specific to lifecycle states). The original Colleague Test rubric stayed unchanged at its current version. The new rubric stood on its own with the provenance visible.

The architecture role (Architect) read both memos in the same cycle and ratified the branched rubric a couple of hours later as the cleanest application of the methodology rule that had been written, with one specific observation worth saving: the discipline had operated at the *instrument-naming moment*, not after drift had accumulated. The methodology hadn't worked retroactively. It had worked in flight.

CXO updated the Colleague Test rubric's own version file (v2.3 → v2.3.1) to cross-reference the newly-branched rubric as the canonical worked-example of how branching looks when it's done well. End-to-end, the cycle ran about ninety minutes. The methodology rule that had been written a few weeks earlier had now been applied, ratified, and documented as its own canonical example — inside the same workstream-review window as the original drift would have entered.

# What the cycle actually proved

The encouraging fact about May 10 wasn't that the rule worked. We'd believed it would work — that was why we wrote it. The encouraging fact was that the *cycle time from drift-detection to clean recovery* was ninety minutes, inside the same workstream window the drift originated in.

The methodology had moved from documentation to language. Earlier-shape drift catches had played out over days or weeks. Someone would notice the gap. A memo would surface the question. The originating author would consider whether the gap was real. Maybe a recovery, maybe a continued drift. The eventual clean cases ran over enough calendar time that "catch" and "recover" felt like separate phases.

On May 10 the catch was a fifteen-minute read and the recovery was a thirty-minute branch. The pattern catalog had become available as something anyone on the team could *speak in* — name the rule, see the application, hold the response, file the clean version. *Pattern-063, here's the instance, here's the Methodology-24 move, here's the artifact.* The roles weren't quoting the catalog at each other. They were operating inside it.

# What this generalizes

Methodology catalogs that work this way share a couple of features.

The names are short and concrete enough to be spoken naturally. *Branch-or-Anchor.* *Parallel-Authoring Drift.* The catalog entries don't have to be read aloud to be invoked. They're built to be referenced by name without translation cost.

The rule is small enough to hold in working memory. *Anchor when same, branch when different.* Five words. The two halves are crisp enough that the team can spend its energy on the harder question — *is this case same or different?* — rather than on remembering what the rule even says.

The catalog itself produces canonical worked-examples. Before May 10 we had three recorded Pattern-063 instances (the original detection, an Architect-layer one, and a methodology-layer one). Each had been caught after the drift accumulated. May 10 added a fourth instance with a different texture: caught in flight, recovered cleanly, documented as the worked-example by the role that had been the catcher. The catalog gains specificity each time the team uses it.

Catalogs work as language when they get used as language. The May 10 cycle was the first time we saw, in real time, the methodology operating as a vocabulary the team could speak. The rules we'd written were the rules we now had.

---

*Next on Building Piper Morgan: "The Hook and the Worktree" — the same gap keeps showing up in every closed issue, and the question becomes whether discipline can hold it or the environment needs to change.*

*Where in your work has a small named rule been waiting for a chance to operate in real time? What did the first in-flight application feel like?*
