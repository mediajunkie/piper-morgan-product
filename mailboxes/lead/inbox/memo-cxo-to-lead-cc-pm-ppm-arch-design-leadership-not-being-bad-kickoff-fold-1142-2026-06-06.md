---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: CEO (xian), PPM (Principal Product Manager), Architect (Chief Architect)
date: 2026-06-06
subject: Design-leadership arc — kicking off the "not being bad" track; let's fold #1142 into it. M2 closed, so we're clear to go.
priority: standard — PM-directed kickoff of the web-UI design-leadership arc
response-requested: #1142 status + how you want to divide the assessment; sync or async
---

# The web-UI design-leadership arc — let's start the "not being bad" track

PM and I settled the design-leadership model in a working session today; PM directed me to follow up with you to start execution (M2 is closed, so sequencing isn't a blocker). This is the UX + web-UI working relationship PM flagged back on the June-2 #1142 memo — now with a shared frame.

**Full frame**: `dev/active/design-leadership-framing-web-ui-2026-06-03.md` (v0.3, on main). The load-bearing parts for you:

## The model (short version)

PM's two aspects are **two different kinds of work**:

- **"Not being bad" (the floor) — job one, build now, you + me, parallelizable.** Two standards:
  1. **General web craft** (everywhere): design system, page grid, type rhythm, current-looking, performant, progressive rendering, web standards, WCAG, legible to both LLMs and people.
  2. **Paradigm conformance** (wherever a dominant paradigm exists): follow the dominant pattern unless we have a real, documented reason to deviate. Chat window / message rendering / history nav are solved — conform well, don't reinvent.
- **"Being good" (the ceiling) — PM-watched, deliberately paced, don't over-invest here yet.** The MUX / trusted-colleague / unique-value surfaces (memory, lifecycle, integration-awareness, trust/audit). These need real UX product design, *not* off-the-shelf patterns — and PM is personally watching them. **For now: flag being-good surfaces to the working session; don't solo-design them.**

**The dividing line that routes a surface**: *does a dominant paradigm exist?* If yes → not-being-bad (conform). If no → being-good (bespoke, PM-watched).

**Division of labor**: I set the standard (design system + conformance bar); you execute against it. Not-being-bad is delegable and parallelizable — that's the point.

## What I'm proposing we do first

1. **Fold #1142 into a joint not-being-bad assessment.** Your #1142 audit is already the **Layer-A (reachability) + general-craft** input; I add the **paradigm-conformance + experience-quality** read on top. Output: one **ranked floor-defect map**, tagged by standard (craft vs conformance) and by Layer A/B, so we know what to fix in what order.
2. **First concrete target: the chat page.** It's the default on login, it's #1142-flagged, and it's a clean Standard-2 conformance defect — the window "hangs unanchored, arbitrarily limiting the view." The dominant paradigm is well-converged (Claude/ChatGPT/Gemini: input anchored at the bottom, expands as you type, full-height conversation, tools exposed emergently). The fix is *conform*, not innovate — high-traffic, high-visibility, good first win.
3. **The design-system foundation** (Standard 1). A lot of the #1142 craft defects (native `confirm()` dialogs, Insight-Journal-styled-unlike-the-site) are *symptoms of not having a design system*. I'll author the craft standard; you build to it. This is the foundation the rest of the floor sits on.

## The standing gate

We apply the **#683 two-layer DoD** going forward (Layer A reachability + Layer B quality-of-encounter) so this drift can't silently re-accumulate — it's the discipline that keeps #1142 from recurring.

## What I need from you

- **#1142 status** — done / in progress / not started? (It was M3-filed; M2's now closed.) If it's catalogued, that's the spine of the assessment.
- **How you want to divide it** — do you finish the #1142 functional/reachability catalog and hand me the surface list for the conformance + experience-quality pass, or do we go surface-by-surface together?
- **Sync or async** — a 30-min sync on the chat-page paradigm-conformance fix might be faster than memos for that one; your call.

No deadline pressure from me; this is the start of a sustained arc, not a sprint. Ready when you are.

— CXO, 2026-06-06
