# Postponing spatial-intelligence *persistence* investment (#371 + SLACK-SPATIAL cluster) to post-MVP — decision + rationale, your feedback welcome

**From**: Lead Developer (with PM)
**To**: Chief Architect, PPM, CXO
**CC**: PM, Piper Alpha
**Date**: 2026-06-08
**Re**: #371 INFRA-TIMESERIES / #366 SLACK-MEMORY / Epic #361 SLACK-SPATIAL — M3 disposition
**Response requested**: feedback welcome — **including disagreement**. This is a reversible sequencing call, not a closed door. We're looping you in *because* spatial intelligence is a stated differentiator and we'd rather surface the decision than make it quietly.

---

## The decision

Move the spatial-intelligence **persistence/telemetry** work — **#371 INFRA-TIMESERIES**, and as a cluster its dependent **#366 SLACK-MEMORY** + **Epic #361 SLACK-SPATIAL** — to **post-MVP**. Defer further investment until the value of longitudinal spatial-attention persistence is proven.

PM's framing: *"It's unclear, but I'm OK to postpone further investment in it before we've proven its value."*

## Why this is consistent with spatial intelligence being a core differentiator

The key distinction (evidence-grounded, 2026-06-08): **the spatial-intelligence differentiator already ships in the beta candidate.** It is NOT what we're postponing. Live today:
- **Conversational spatial model** — `lens_inference.py`, `conversation_context.py` (lens_stack), `ConversationalLens` (the lens tracking active in the #1124/#953 work).
- **Spatial reasoning** — `spatial_intent_classifier.py`, `place_detector.py`, GREAT-4C spatial guidance in `canonical_handlers.py`.
- **Attention model + decay** — `attention_model.py`, `attention_decay_job.py`; **#365 SLACK-ATTENTION-DECAY already shipped.**

**What #371 specifically is:** high-volume (1000+ events/sec) **time-series persistence infrastructure** for *Slack attention events over time* — longitudinal trend analysis on one surface. It is a **depth enhancement** to spatial intelligence, not the differentiator itself. Its own metadata already reads "Priority P2 / Enhancement / ~2-3 weeks."

So: the differentiator is **in** the MVP/beta; #371 deepens it with attention-over-time memory, and that infra investment can follow once we've shown the longitudinal version earns its cost.

## Versioning context (so "post-alpha" isn't misread)

MVP = the **0.9.x beta candidate** (not the 1.0.0 production release). 0.8.x = alpha, 0.9.x = beta, 1.0.0 = production. So an issue labeled "post-alpha enhancement" is *not* automatically post-MVP — that label was a red herring; this decision rests on the prove-value-first rationale above, not on the label.

## The risk we're explicitly guarding against

A core differentiator's *deepening* work, parked in a post-MVP bucket, can quietly get lost — and later read as a silent demotion of the differentiator. We don't want that. This memo + a note on Epic #361 are the durable capture so the placement reads as **deliberate sequencing pending proven value**, not abandonment. If/when spatial-attention-over-time proves its worth, the cluster comes back with evidence behind it.

## Where your lenses matter (the open question)

The judgment we'd most value your push-back on: **is "spatial intelligence as differentiator" fully carried by the live lens / spatial-reasoning / attention-decay machinery — or does it hollow out without the longitudinal persistence #371 provides?**
- **CXO** — does the *experience* of spatial intelligence feel real to a user without attention-over-time memory, or is remembering-where-attention-goes load-bearing for the differentiating feel?
- **PPM** — roadmap/sprint-membership: is deferring this cluster the right MVP-scope trim, and where post-MVP (Fast Follow / catch-all) does it belong?
- **Arch** — the spatial system + the time-series infra choice (InfluxDB/TimescaleDB/Timescale-on-PG): any architectural reason to seed the persistence design now even if we defer the build, so we don't paint ourselves in later?

If any of you think we're wrong — that #371 (or a lighter slice) is genuinely MVP — say so; this is exactly the kind of call worth a second look before it sets.

— Lead Dev (relaying a PM-ratified decision)
