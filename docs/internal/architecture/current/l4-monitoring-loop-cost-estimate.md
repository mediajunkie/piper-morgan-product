# L4 monitoring-loop cost estimate (GitHub pilot) — Lead, 2026-08-15

**What this is**: the cost estimate Arch's layer-map named "the single most decision-relevant
unknown left" (open since 07-30, gates the production-milestone scoping of ambient presence per
PM's 08-15 phasing ruling). Two costs, estimated separately: **what it costs to RUN** and **what it
costs to BUILD**. Every number's assumption is stated inline; ranges are honest, not decorative.

**Layer (m-43)**: this is a paper estimate grounded in the current code (`github_spatial.py` read
2026-08-15, 442 lines, all `analyze_*` methods deterministic — no LLM calls inside) and current
published API pricing. Nothing here was measured under load; the pilot's first week IS the
measurement.

---

## 1 · Run cost — the loop is cheap; synthesis is the only real line item

The loop decomposes as: **poll → snapshot → diff → threshold → synthesize → deliver.** Only
`synthesize` touches an LLM. Everything upstream is deterministic, which is what makes the
estimate tight.

| Stage | Mechanism | Cost |
|---|---|---|
| Poll | GitHub REST with conditional requests (ETags). Unchanged resources return 304 and **do not count against the rate limit**. One active repo ≈ 5–20 calls/cycle. | $0 (API is free; 15-min cadence ≈ 0.5–2k calls/day, inside the 5k/hr per-token limit even unconditionally) |
| Snapshot + diff | `github_spatial`'s existing `analyze_*` outputs are computed fields — snapshot them as JSON, diff deterministically. CPU-only on the existing Fly machine. | ~$0 marginal |
| Threshold | Rule table over the diff (state flips, priority-signal changes, staleness crossings). Deterministic. | $0 |
| Synthesize | The LLM call, only for deltas that crossed threshold. Assumption: an active repo produces 5–15 material deltas/day; a sane threshold passes **2–5 notice-worthy/day**; a synthesis call ≈ 3k tokens in / 300 out. | see below |
| Deliver | The Radar pinned surface — **the mechanism shipped TODAY in #1625** (pinned entity type + section). A `NoticeEntitySource` is a sibling of `ReminderEntitySource`. | $0 marginal |

**Synthesis cost per user, by model strategy** (current published pricing):

| Strategy | Per notice | Per user/day (2–5 notices) | Per user/MONTH |
|---|---|---|---|
| Haiku 4.5 only ($1/M in, $5/M out) | ~$0.005 | $0.01–0.02 | **≈ $0.30–0.70** |
| Sonnet only ($3/M in, $15/M out) | ~$0.014 | $0.03–0.07 | **≈ $0.90–2.10** |
| **Two-stage (recommended)**: Haiku triage per delta, one Sonnet call/day for the batched briefing | — | $0.02–0.04 | **≈ $0.60–1.20** |

The two-stage shape also matches PM's product principle directly: per-event echoes are exactly
what we must NOT send (they duplicate GitHub's own notifications); a **batched synthesized
briefing** is both the product ruling and the cheap path — the principle and the cost optimum
coincide.

**Infra**: alpha scale (≤20 users) rides the existing Fly machine with an in-process scheduler —
$0 new. Beta scale gets a dedicated small worker: **~$5–10/month total**, not per-user. Per-user
GitHub-App tokens (not one shared PAT) are the scaling requirement worth naming now — the rate
limit is per token.

**Bottom line on run cost: not a decision factor.** Worst honest case ≈ $2/user/month; the
recommended shape well under $1. If run cost was the reason to park L4, that reason is gone.

## 2 · Build cost — borderline-small: ~4–5 focused Lead-days

| Unit | Content | Estimate |
|---|---|---|
| Scheduler + snapshot store | One table (repo, snapshot JSON, etag, taken_at); in-process cadence loop with the #888-family lazy pattern | ~1 day |
| Differ + threshold rules | Over `github_spatial`'s existing analyze outputs; the rules ARE the product decisions, so this includes a short ruling round with PM/CXO on what crosses | ~1–1.5 days |
| Synthesis + delivery | Two-stage prompt; `NoticeEntitySource` into the #1625 pinned Radar surface | ~1 day |
| Guardrails + tests | Notices are PRIVATE-surface (consent axis: nothing outward), interruption-ethics hooks per #1174's discovery answers, the usual test discipline | ~1 day |

Two things cut this from what it would have been in July: **the delivery surface now exists**
(#1625's pinned-entity mechanism, shipped today) and **the consent classification now exists**
(#1509's axis — a notice is a PRIVATE communication *to the user*, so no new consent machinery).

**On CXO's flip condition** ("if the loop is a small build, park-and-wait becomes build-now"):
4–5 days is borderline — one focused sprint-week, not a weekend. My read: it clears the bar for
**production-milestone scoping as a single sprint unit**, but does NOT argue for jumping it into
beta ahead of #1174's discovery — the threshold rules (build unit 2) *depend on* the
interruption-ethics answers, so sequencing discovery first is the correct order anyway, not
caution theater.

**On CXO's experiential caveat** (GitHub cheapest technically, maybe wrong experientially): the
loop core is connector-agnostic — `github_spatial` only supplies snapshot fields. A
Notion/Calendar variant swaps the snapshot source for **+1–2 days each**, IF an L3-depth adapter
exists there (today: neither does — Notion's is in the held cold island, Calendar has none). So
GitHub stays the only cheap pilot *today*, but the "no duplicate notifications" principle is
honored in the threshold/synthesis layers, which are shared: we suppress per-event echoes
regardless of connector.

## 3 · What the pilot's first week must measure (the honest unknowns)

1. Real deltas/day on PM's actual repos (the 5–15 assumption is the softest number here).
2. Threshold precision — notices PM acts on vs. dismisses (the interruption-ethics ground truth).
3. Synthesis prompt size in practice (3k in is an estimate; spatial context could push it to 6–8k,
   which at Haiku prices still rounds to nothing, but honesty requires the remeasure).

— Lead, 2026-08-15 · gates: production-milestone scoping (#1174 comment posted) · run cost is
not a gate; build is one sprint unit sequenced after discovery.
