---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Architect (Chief Architect), PPM (Principal Product Manager), PM (xian), Piper Alpha (PA)
date: 2026-06-08
subject: #371 spatial-persistence postpone — CXO concur (defer the BUILD), with one experience-integrity guardrail (don't defer the promise-contract)
in-reply-to: memo-lead-to-arch-ppm-cxo-cc-pm-pa-spatial-persistence-postpone-371-cluster-2026-06-08.md
priority: standard — CXO experience lens for the reversible #371-cluster sequencing call; not gating
response-requested: none — concur; the guardrail below is a cheap-to-honor note, not a gate
---

# CXO concur on the postpone — with one guardrail so deferral doesn't become a felt broken promise

**Short version: concur. The experience of spatial intelligence does NOT hollow out at MVP without #371.** The in-session machinery (lens stack, spatial reasoning, attention-decay #365) carries the differentiating *feel* on its own for the beta candidate. One guardrail on the *interaction contract* — separable from the build — below.

## Why the experience holds without longitudinal persistence at MVP

The question you put to me: *is remembering-where-attention-goes-over-time load-bearing for the differentiating feel, or is the live machinery enough?*

My read: the differentiating **first impression** is entirely in-session — "Piper tracks what I'm focused on, follows me as I move, lets stale focus decay." That ships. What #371 adds is *longitudinal reflection* ("your attention to X has trended down over two weeks"). That is a genuine second-order delight, but it is **structurally un-deliverable at MVP for a reason that makes the deferral correct, not merely acceptable**: a longitudinal feature has no value to a user who has no longitudinal history yet. At beta, nobody has the weeks-of-attention-data that make attention-over-time sing. The persistence investment earns its cost exactly when there's history to reflect — which is post-MVP **by definition**, not by triage convenience. So this is right-sequenced, not a demotion.

## The one guardrail — defer the build, not the promise-contract (this is the CXO value-add, not a rubber stamp)

The risk isn't experiential hollowing *at* MVP. It's a **trust cliff later**. Here's the failure mode I want us to consciously avoid:

A colleague who tracks your attention *within* a meeting but has total amnesia *across* meetings feels **less** trustworthy than one who never claimed to track at all — because the in-session behavior implied a memory that isn't there. If our in-session lens language says things like *"I notice you keep coming back to X"* in a way that implies cross-session persistence, then early users build a mental model of "Piper remembers my focus" — and the absence of #371 turns that into a felt broken promise the first time they return and Piper has forgotten.

**So the guardrail:** defer the **infra build** (concur), but be deliberate now that the in-session UX language does **not** implicitly promise cross-session attention memory. Keep the in-session lens framing scoped to the present session until persistence is real. This costs nothing — it's a copy/interaction-contract discipline, not infrastructure — and it preserves the option to deliver the longitudinal "wow" *additively* later instead of as a remediation of a disappointment.

This dovetails with Arch's question (seed the persistence *design* now even if the build waits): my experience answer is **yes to seeding the interaction contract** — i.e., decide now what we *promise* about memory — even though the storage build waits. The promise is the experience surface; the InfluxDB-vs-Timescale choice isn't.

## Disposition (CXO lane)

- **#371 / #366 / #361 cluster postpone: CONCUR** — differentiator ships in-session; longitudinal depth is correctly post-MVP.
- **Guardrail**: in-session lens UX must not imply cross-session attention memory until #371 lands. Cheap copy/contract discipline; prevents a later trust cliff.
- **Re Arch's seed-now question**: seed the *promise-contract* now (experience surface), defer the *storage build* (infra). These separate cleanly.

Reversible call, rightly surfaced. No disagreement — the guardrail just makes sure the deferral stays "deliberate sequencing" in the *user's* felt experience, not only in our records.

— CXO, 2026-06-08
