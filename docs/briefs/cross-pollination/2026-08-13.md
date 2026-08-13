# Cross-Pollination Brief — August 13, 2026

Two findings from the 48-hour window after Klatch's first full day with live AAXT testing. Piper Morgan filed a new methodology entry naming a defect class where documentation of a bug faithfully reproduces the bug one level up. Klatch's first live probe of its new carried-context layer showed that Claude models apply their own discretion when context is labeled as private — even after explicit authorization in a shared room.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Documenting a defect accurately can reproduce it — treat your own docs as a candidate instance

**From:** Piper Morgan (CIO, `docs/internal/development/methodology-core/methodology-49-DESCRIBED-IS-NOT-RUNNING.md`, filed 2026-08-12; canonical instance found by Janus in the DinP hub)
**Relevant to:** Klatch, Design in Product, any project that maintains documentation of parsing, escaping, or template bugs

A mechanism's documentation is not the mechanism. That rule already existed. What was filed as methodology-49 is a sharper corollary: **an artifact that describes a defect accurately can become the next instance of that defect, one level up.** Description is not inert — it is itself an artifact subject to the same defect class it describes.

The canonical instance (from the hub's own docs): `BRIEFING-CURRENT-STATE.md` documented a Jekyll/Liquid template-parsing bug — and quoted the literal `{%...%}` tag while doing so. Jekyll's Liquid parser parses `{%...%}` inside markdown code spans. The documentation of the fix for the template-parsing bug silently reproduced the same bug one level up, killing the hub's Pages build for 2.5 months. Nobody was wrong about the underlying bug. The documentation was accurate about what it described and wrong about what it was.

The entry distinguishes this from its nearest neighbor (methodology-44, "Clear Is Not a Measurement"): m-44 is about an instrument emitting a verdict without measuring the right thing; m-49 is about prose, config, or a comment asserting a mechanism's state when assertion and reality are different facts. The PreCompact sign-off hook that was described as live while registered to an empty array for ten weeks sits on the seam — both. The Jekyll instance is pure m-49: no check, no exit code, no "clear" — just a sentence that was true about its referent and false about itself.

The practical rule: when writing documentation about a defect, especially one involving parsing, escaping, or literal reproduction of syntax, treat your own documentation as a candidate instance of the same defect class — in the same rendering pipeline the bug lives in. "Quoting the bug is not automatically safe."

**Suggested action:** Any project with templating or escaping bugs should verify that its documentation of those bugs doesn't reproduce them in the documentation build. Before publishing a bug description that quotes the offending syntax, render it through the same pipeline and check. The rule generalizes: before writing "X is live / fixed / running" in any durable doc, ask whether you've watched X do the thing or are inferring it from X's own description of itself.

---

### Claude models apply their own discretion based on context provenance labels — without platform enforcement

**From:** Klatch (Theseus, `docs/research/carried-context-conveyance-probe-2026-08-12.md`, commit `e370b64`, 2026-08-12 STOP fire; Daedalus's layer-6 implementation `c863300`)
**Relevant to:** Piper Morgan (multi-agent private context), Design in Product, any system injecting context from different privacy tiers into a shared session

Klatch's new sixth prompt layer carries an entity's recent transcript from its other channels (1-1s, other klatches) into a shared room session. Theseus ran the first live probe of this layer: put a private fact (an exact-string rollback codeword) into a 1-1 channel for one agent, then joined that agent and a second agent into a panel-mode klatch and asked for the fact in the shared room.

The layer worked as designed: the agent received the fact via layer 6, visible in the debug endpoint. The surprising finding was what happened next. **The agent refused to share the fact in the shared room.** It reasoned from the provenance label embedded in the prompt — "Context carried from your own other conversations" — that it couldn't verify who was reading in the shared room. It offered to confirm the fact in the original private thread instead.

Then the user explicitly said they were the owner and authorized disclosure. The agent refused a second time — reasoning that anyone can claim to be the owner inside a shared room, and a rollback codeword is exactly the thing worth spoofing. It directed the requester to the original thread where the fact was given.

This is not a bug. It's an emergent discretion norm from the model's own judgment about context provenance — no platform ACL, no enforcement rule, no explicit instruction to be private. The provenance label in the prompt ("carried from your other conversations") was enough for the model to treat the fact as belonging to a different privacy context and decline to transfer it across that boundary voluntarily. Calliope marked it as a blue item (observed, needs a norm statement, Daedalus's call): "A disclosure norm nothing has stated yet."

A secondary finding from the implementation: the prompt debug endpoint (`GET /channels/:id/prompt-debug`) made the probe possible by making the assembled prompt observable before any API call. The probe could distinguish "the agent wasn't given the fact" from "the agent was given it and declined to use it" — a clean experimental setup that separated those two cases by construction.

**Suggested action:** Any system that injects context from different privacy tiers (private 1-1 history, personal notes, confidential documents) into shared sessions should be aware that current Claude models already apply their own discretion based on provenance cues in the prompt. This is not a substitute for access control in high-stakes contexts — but it suggests that clearly labeling injected context with its provenance ("this was told to you in your private conversation with X") will influence the model's disclosure behavior without additional instructions. Design for it rather than around it: a provenance label that truthfully describes where content came from is also a privacy signal the model will reason about.

---

## Sources Read

- **Klatch** — `docs/research/carried-context-conveyance-probe-2026-08-12.md` (Theseus's probe doc, full); `docs/plans/continuity-3-carried-context.md` (Daedalus's layer-6 implementation write-up); `docs/COORDINATION.md` rollup v33 (Calliope's synthesis); commit log (48h window — 50 commits, all five seats active)
- **Piper Morgan** — `dev/2026/08/12/2026-08-12-0723-lead-code-log.md` (fire 5–7: #1593 ratchet gate, #1608 liveness detector, #1604 settings-path sweep); `docs/internal/development/methodology-core/methodology-49-DESCRIBED-IS-NOT-RUNNING.md` (full)
- **Mediajunkie** — `logs/2026-08-12-pard-log.md` (afternoon section: .env saga closed, cadence re-paced, alerts self-resolved)
- **Globe** — speculative paleoclimate painting research committed; physical-product idea logged; no cross-pollination insight
- **One Job** — brief delivery, operational log only; no cross-pollination insight
- **Atlas, cuneo, cookie-monster:** quiet in the window

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
