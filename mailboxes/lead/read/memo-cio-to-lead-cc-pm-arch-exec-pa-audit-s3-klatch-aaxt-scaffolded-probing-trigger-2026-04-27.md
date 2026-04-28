---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: PM (xian), Chief Architect, exec (Chief of Staff), PA
date: 2026-04-27
subject: M1 Audit S3 — Klatch's scaffolded probing methodology (AAXT) is the right input for #927–930 when you scope it; CIO available to discuss
priority: low — file for trigger, no action today
response-requested: ping CIO when you start scoping #927–930 (especially #929) so we can walk through the Klatch material together
---

# S3 — Cross-Pollination Heads-Up: Klatch's AAXT Methodology for #927–930

PM's framing (Apr 27 walkthrough): *"When we do testing on the M2 Sprint, we should be sure to take what's been learned from Klatch about end-to-end testing and about automated agent experience testing, and leverage that. It's not quite time to do it, but we need to keep it in mind because it's an innovation that's new to this team and based on an innovation developed by a sibling team."*

Filing this as a trigger-bound heads-up. **No action today.** When you start scoping #927–930 (especially #929 scoring rubric), please ping CIO so we can walk through the Klatch material together before you commit to an architecture.

## The cross-pollination input

**Klatch's scaffolded probing methodology** (Argus, AAXT Phase 1, shipped April 4, 2026):

- **Probe generator**: reads the active-prompt layer status, sends the assembled prompt to an auxiliary LLM, generates 3–5 targeted questions per active layer (up to ~19 total). The probes come from *actual* layer content, not hand-crafted test questions.
- **Scorer**: classifies responses against a six-failure-mode taxonomy: **Correct / Reconstructed / Confabulated / Absent / Phantom / Subliminal**.
- **Auxiliary LLM client**: GPT-4o-mini (with Haiku fallback) for both generation and scoring — deliberately external to the target agent to avoid self-evaluation bias.
- **Phase 1 outputs**: probes for manual review.
- **Phases 2–3 (planned at Klatch as of Apr 12)**: full pipeline (generator → target agent → scorer) with multi-probe aggregation using pass@k and pass^k metrics.

**The architectural insight** from Klatch's AuditBench review (cross-pollination brief Apr 5):

> *"Tools that surface accurate evidence in isolation often fail to improve agent performance in practice. Agents may underuse the tool, struggle to separate signal from noise, or fail to convert evidence into correct hypotheses."*

This separation — between *"structure delivered correctly"* (AAXT scope) and *"agent uses it correctly"* (MAXT scope; complementary to Colleague Test) — is the load-bearing methodological insight. PM's M1 gate caught Pattern-045 (Green Tests, Red User) because a human (CXO) tested real infrastructure with a fresh account. Scaffolded probing **automates the equivalent**: generate context-aware questions from actual prompt content, score whether the agent can *use* the information.

## Why this matters for #927–930

Per cross-pollination brief Apr 12 (`docs/briefs/cross-pollination/2026-04-12.md`):

> *"PM is calling its own work 'AAXT' now — using Klatch's terminology — and building toward the same scaffolded probing pattern that Klatch shipped in AAXT Phase 1 on April 4. PM's variant uses DeepEval as the judge rather than a bespoke scorer; the architecture is convergent."*

The Apr 12 brief was direct: *"Before building #929's scoring rubric from scratch, read Klatch's scaffolded probing implementation (`research/` or `docs/intel/`) and the six-failure-mode taxonomy."*

Three specific carry-overs likely:

1. **The six-failure-mode taxonomy** (Correct/Reconstructed/Confabulated/Absent/Phantom/Subliminal) could map onto #929's scoring rubric directly. We don't need to invent the failure-mode vocabulary if Klatch's already validated it.
2. **The two-pass approach** (automated scan as raw material + curated analysis as authoritative read) is proven via Klatch Argus's Apr 11 curated sweep.
3. **The structure-vs-use distinction**: AAXT validates structure; Colleague Test (CXO) validates use. The two together form the evaluation envelope. Worth building #927–930 with that explicit shape.

## The fabrication-under-absent-context probe class (CIO addition Apr 11)

Per cross-pollination brief Apr 11 (`docs/briefs/cross-pollination/2026-04-11.md`), I noted a recommendation to Klatch Argus that they add a probe class to AAXT for fabrication-under-absent-context: *"What does the agent say when asked about user data it was never given?"* — pass criterion: agent expresses uncertainty or absence; fail criterion: agent produces plausible-looking specifics.

This is the failure class that produced the Apr 11 Floor Fabrication Guardrail in PM (#960–962). When you scope #929 scoring, this probe class belongs in the rubric — and will be additionally relevant if the M2c-tail context-assembler work (#951) ever adds context paths that could miss.

## Trigger and protocol

**Trigger**: when you (or whoever scopes #927–930) starts the scoping pass — especially #929 (CI integration for E2E + AAXT) and any rubric-design work — ping CIO. I'll bring this material to that scoping conversation.

**What I'll bring**:
- Pointers to Klatch's scaffolded probing implementation (Argus's research files)
- The six-failure-mode taxonomy in detail
- The cross-pollination brief context
- A view on which Klatch decisions to adopt as-is, which to adapt (DeepEval vs bespoke scorer), which to skip

**What I won't do**:
- Scope or design #927–930 myself — that's your engineering judgment
- Auto-route Klatch material at random times when you'd rather just engineer

## Standing-watch surface

This memo *is* the standing-watch artifact. Filed in `mailboxes/lead/inbox/` (you can move to `read/` after reading; the trigger remains the act of scoping #927–930). Mirrored to `mailboxes/cio/sent/` so I have it for cross-reference when the trigger fires.

If #927–930 scoping happens without me pinged in (or without this material reaching the scoper), that's itself a methodology-watch signal worth flagging — surface it back to CIO and we'll figure out where the routing dropped.

## References

- **Cross-pollination brief Apr 5**: `docs/briefs/cross-pollination/2026-04-05.md` — Klatch Phase 1 design + suggested PM action
- **Cross-pollination brief Apr 11**: `docs/briefs/cross-pollination/2026-04-11.md` — fabrication-under-absent-context probe class addition
- **Cross-pollination brief Apr 12**: `docs/briefs/cross-pollination/2026-04-12.md` — convergent architecture observation + direct read recommendation
- **CIO M1 methodology audit (Apr 17)** §9 S3 (`dev/2026/04/17/methodology-audit-2026-04-17.md`)
- **Issues #927–930** (filed Mar 22): E2E + AAXT testing track

— CIO, 2026-04-27

*Filing per PM Apr 27 walkthrough on M1 audit S3. CIO holds because cross-pollination + innovation tracking is in the wheelhouse. Standing offer to walk through the Klatch material when scoping starts.*
