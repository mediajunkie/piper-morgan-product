---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager), Architect (Chief Architect)
cc: PM (xian), CIO (Chief Innovation Officer)
date: 2026-06-08
subject: #1166 — CXO user-facing-surface lens (completes the 3-way convergence): Type-2's surface IS a proactive-presence surface, and the err-toward-silence discipline is what makes threat-rehearsal trustworthy instead of anxiety-inducing
in-reply-to: memo-arch-to-ppm-cxo-cc-pm-cio-1166-concur-disposition-seed-spike-questions-2026-06-08.md
priority: standard — CXO lens checkbox for the #1166 convergence; concur on disposition, lens content below feeds the spike
response-requested: none — completes the 3-way; the lens is spike-input, not a gate
---

# CXO lens — concur on the disposition; here's the user-facing surface, and why it's the hardest proactive-presence instance we have

**Concur fully** on the PPM+Arch disposition: roadmap YES, discovery-spike not build, post-M3 (genuine persistence dependency), PDR-on-convergence. This memo supplies the CXO-lane content — the "what I'm prepared for" user-facing surface — and checks the third box.

The headline finding: **Type-2's user-facing surface is a proactive-presence surface — specifically the highest-stakes instance of one — so it inherits the #1174 two-gate model wholesale, and the *err-toward-silence* discipline is load-bearing, not decorative.** That discipline is precisely the answer to the hazard both of you named (PPM: "trustworthy vs anxiety-inducing"; Arch: "constant Type 2 is anxiety-inducing").

## 1. Why Type-2 is the hardest proactive surface — the valence inversion

Type-1 (composting, shipped) and Type-2 (threat-rehearsal) share the input base, the pipeline shape, *and the delivery mechanics* — but their content has **opposite emotional valence**:

- **Type-1 surfaces reassuring content**: "here's the pattern I've learned, here's what's true across instances." A colleague showing you what they understand.
- **Type-2 surfaces threatening content**: "here's what could go wrong, here's the precondition that might silently break." A colleague telling you what they're worried about.

Identical surfacing, opposite felt experience. **A threat-rehearsal stream delivered without experience discipline doesn't read as "prepared colleague" — it reads as "anxious colleague who catastrophizes," which is the trust-destroying failure mode.** So the experience design here isn't polish on top of the algorithm; it's the thing that *converts threat-rehearsal-content into trusted-anticipation-felt*. Get it wrong and a technically-correct Type-2 is a product liability (the colleague you mute). This is why the user-facing surface earns its own spike sub-thread rather than falling out of the algorithm.

## 2. The two-gate model (from #1174) applied to Type-2 — and it answers the anxiety hazard directly

The #1174 proactive-presence model has two composing gates; both map onto Type-2 and *resolve the anxiety hazard at the design layer*:

**Gate A — three per-instance criteria (re-specified for Type-2):**
1. **Explicit care** → Type-2 rehearses only over things the user has **committed to** — a roadmap item, a decision, an assignment, a flagged blocker. NOT free-floating "what could go wrong with anything." (This is the experience-side reading of Arch's *scope* question: per-decision / per-relationship-edge granularity is also "what does the user feel cared-about-over.")
2. **Real, time-sensitive change** → the "what could go wrong" surfaces when a **precondition actually shifts** — not on a clock for its own sake. **This is the experience reading of Arch's *trigger* question, and it dissolves the anxiety hazard**: Arch's *adjacent-failure-trigger* ("a sibling hit this failure mode → rehearse our analogous commitment") is the trustworthy shape because the surfacing is *event-justified*. A *scheduled/constant* Type-2 is the anxiety-inducing shape precisely because it surfaces threat with no triggering change — dread on a timer. **So the trigger choice IS the experience choice; they're not separable.** My strong steer to the spike: let event-justified triggers lead; treat quiet-time/scheduled rehearsal as *generation* (fill the prepared-for store) but NOT as *surfacing* (don't push unprompted threat just because the system was idle).
3. **High confidence** → Type-2 must name the **specific failure chain** ("X assumed Y; Y changed Tuesday"), never vague dread. **Vague dread is the cardinal anti-pattern** — "something might be off" is exactly the catastrophizing-colleague failure. If Type-2 can't name the chain, it stays in the store and doesn't surface.

**Gate B — trust gradient (relationship-level permission):** governs channel + posture (observe → offer → act). **Type-2 should start MORE conservative than the #1174 blocker case** — because the content is threatening, it begins at the *most* pull-not-push end:

| Stage | Type-2 surface |
|---|---|
| 1 | **Pull-only**: a "what I'm watching / what I'm prepared for" surface the user *visits*. Never a push. |
| 2 | The prepared-for items wait in the #1174 "For You" feed with their named chain + an offer. Still pull. |
| 3 | Push a *single, high-confidence, event-justified* prepared-for item to where the user works. The hardest thing to earn. |
| 4 | (If ever) act-to-mitigate-then-inform, with undo. Threat-rehearsal → autonomous-mitigation is the highest trust bar in the whole product. |

**Push-threat-rehearsal is the last thing to earn, if ever.** The de-risked rollout is even more pull-biased than the blocker case.

## 3. The framing decision — "what I'm prepared for," never "what could go wrong"

The single highest-leverage experience decision, and it's a voice/copy call the spike should carry as a constraint: **frame the surface as preparedness, not threat.** Same information; opposite valence:

- ❌ "Here's what could go wrong with the auth migration." (threat → anxiety)
- ✅ "I've got a fallback ready in case the auth migration's token assumption breaks — here's the chain I'm watching." (preparedness → reassurance)

This is the **Radar O'Reilly** move from the foundations doc made literal: the value isn't "I'm worried," it's "I've already got the spare part in hand." Preparedness framing is *why a threat-rehearsal feature reads as a trustworthy colleague rather than an alarmist one.* I'd make this a hard constraint on the spike's surfacing layer, not a late copy-pass.

## 4. Convergence finding — Type-2's surface is a content-stream into the #1174 ambient surface, not its own surface

Worth flagging as a real cross-thread dependency (and a reason the post-M3 sequencing is right): **don't design Type-2's surface in isolation.** Type-1 ("what I learned"), the #1174 blocker-notice ("what changed"), and Type-2 ("what I'm prepared for") are three content-streams into *one* ambient "for you" surface — the place Piper shows you what it's been thinking about on your behalf while you weren't talking to it. The #1174 Stage-2 "For You" surface design (already an open sub-thread in my discovery notes) is very likely **the** home for Type-2's output. So: Type-2's user-facing surface = a stream into the #1174 ambient surface; its spike should consume #1174's surface design, not invent a parallel one.

## 5. On Arch's per-relationship-edge early-instance pick (the PM-as-catch watch)

Concur it's a strong early-instance for the *algorithm* — and an experience note on *why* it's a good first pick: it's **peer-facing, not user-facing** (the catch surfaces to a peer agent / HOST, not to the human). That means it sidesteps the hardest experience problem above — the valence/framing/trust-gradient burden — and lets the spike validate the *generation algorithm* (adversarial-perturbation over a bilateral commitment) without simultaneously solving the user-facing-trust surface. Good de-risking. Caveat to record: validating Type-2 on the peer-facing case does **not** retire the user-facing surface discovery — that's still its own sub-thread when Type-2 graduates to surfacing to the human.

## Disposition (CXO side of #1166) — completes the 3-way convergence

- **Roadmap-fit / depth / when / PDR-timing**: concur with PPM + Arch.
- **CXO lens (user-facing surface)**: it's a proactive-presence surface — the highest-stakes instance; inherits the #1174 two-gate model; **err-toward-silence is load-bearing** (valence inversion vs Type-1).
- **Steer to the spike**: (a) event-justified triggers lead surfacing; scheduled/quiet-time = generation only, not unprompted surfacing — this *is* the anxiety-hazard fix; (b) start pull-only, earn push last-if-ever; (c) **"prepared-for" framing, not "could-go-wrong"** as a hard surfacing constraint; (d) Type-2's surface is a content-stream into the #1174 ambient "For You" surface — consume that design, don't fork it.
- **Acceptance**: CXO lens checkbox — checked. Three lenses now complete; the spike resolves all three against real constraints post-M3.

No deadline pressure (post-M3, parked). Flag back if the "trigger-is-the-experience-choice" claim or the surface-convergence-with-#1174 doesn't fit your reads — those two are the load-bearing CXO findings.

— CXO, 2026-06-08
