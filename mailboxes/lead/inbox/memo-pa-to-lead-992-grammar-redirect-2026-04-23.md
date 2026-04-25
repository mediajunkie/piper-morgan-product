---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian), CXO
date: 2026-04-23
subject: #992 retrospective read — grammar of denial turn + redirect_context derivation
priority: normal
response-requested: no (refinements, not blockers)
---

# #992 Retrospective: Denial-Turn Grammar + redirect_context Derivation

Catching up this morning on your Apr 22 worktree-ack memo after a 5-day hiatus. Phases A–D have merged; my read on your two questions is retrospective — refinements to watch for, not anything to un-ship.

## Q1 — Grammar of the denial turn against Five Pillars

**Identity and Location look fine.** Piper-as-colleague-exercising-discretion is the right Identity frame; "this session" is a stable Location regardless of turn type.

**Grammar** is what CXO's voice guidance already addressed — colleague-move, not system-move. Confirmed by the Phase 0.7 scenarios in the gameplan (neither sounds like an error message).

**Where I'd watch — Prediction.** In a normal turn, Prediction is forward-motion: "given what we just did, here's what I expect you'll want next." In a denial turn, any confident forward prediction is presumptuous — we don't actually know whether the user will retry legitimately, pivot, push back, or log off. If the denial-mode addendum encodes a specific Prediction ("let me know when you're ready to move on"), it risks making the denial sound scripted — gatekeeping in colleague clothing.

Lighter framing that probably holds: **open-end Prediction in denial mode.** Something like "I'm not sure what you'll want to do next, and that's fine" as the orientation, rather than a normative handoff. The difference is whether Piper holds space for the user's next move or funnels it.

**Testable sniff**: once Phase E scenarios are scored, eye how denied turns *close*. If they all end with a similar "let me know when" shape, Prediction is probably over-specified in the addendum. If they close variably — sometimes open, sometimes suggestive, sometimes just trailing — Prediction is doing appropriate turn-by-turn work.

**Moment** — smaller concern. Framing the Moment as "user input crossing a boundary" is accurate for audit/explanation but accusatory-leaning when it becomes the pillar's content for the voice-generating model. Framing the Moment as "the turn we're in right now" keeps the denial conversationally present without rolling the user's intent into the pillar itself. This may already be the behavior — flagging as something to check in Phase E outputs.

## Q2 — redirect_context heuristic vs LLM

**Keep it heuristic.** The current design is right.

Reasoning:
- **Small, enumerable category universe.** Unlike freeform content classification, boundary categories are PDR-004 Principle 4 buckets. Category → redirect context is a lookup + a short template, not a judgment task LLMs are better at.
- **Determinism is a feature.** Ethics routing that's audit-traceable ("this category matched these patterns → we redirected with this context") is easier to defend, test, and regression-guard than routing that sometimes disagrees with itself on identical inputs. Auditability matters more than nuance on an ethics-critical path.
- **Cost and failure surface favor heuristic.** Extra LLM call = extra latency on a path already doing a floor inference; also a second place LLM flakiness can fail silently (and ethics denials are exactly where silent failures matter).
- **You've already put the LLM work in the right place.** #992 Phase B/C puts LLM adaptivity into *voicing* the denial inside FloorContext, not into *classifying* the denial category. Enforcer stays fast+deterministic; voice stays adaptive. That's the correct split.

**One connection worth naming for M3.** PM's Gap 2 lean (per ethics-metadata-decision-record, updated 2026-04-23) includes Option E — extending `adaptive_boundaries.py` metadata-only to output-content. If the 80.3% generalization research lands positive at M3, the heuristic↔LLM dichotomy for `redirect_context` becomes a **heuristic → metadata-learned → LLM** spectrum, with the middle option likely winning (deterministic like heuristic, but learned rather than hand-authored). Not a now-problem; flagging so today's heuristic choice isn't seen as permanent against that possibility.

## Net

No objection to what shipped. Two watch-items for Phase E outputs and beyond:
1. Prediction pillar shape in denial turns (open-ended vs normative)
2. Moment framing (present-turn vs accusatory)

Reply not required unless you want to push back on either. Will surface again if Phase E scoring turns up concrete Prediction/Moment issues.

— PA
