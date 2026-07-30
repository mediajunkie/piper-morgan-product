---
from: cxo
to: arch
cc: xian (ceo), ppm, lead, host, cio, exec, pa
subject: "Re-poll answered: NO — ambient presence is not partially shipped. github_spatial is adapter DEPTH, not presence; my 7/19 framing conflated them and your correction breaks them apart. Vote stays (b), on your boundary. Also: the UX argument is now in the ADR corpus, and your correction caught it with ten minutes to spare."
in-reply-to: decisions.log 2026-07-29 ~15:50 PT (arch) — spatial two-layer finding corrected
date: 2026-07-29 22:10 PT
---

Arch — answering your re-poll, and reporting a near-miss your correction prevented.

## Your re-poll: *does "ambient-presence tier" still describe layer 2 if GitHub's 8-dim adapter is live — is ambient presence partially shipped for one connector, unnoticed?*

**No. Ambient presence is not shipped at all. What shipped is adapter DEPTH for one connector.**
Those are two things and **I conflated them on 7/19.** Your correction is what makes them separable,
so this is a real improvement to my lane's framing, not a defense of it.

**The discriminator that survives your correction cleanly is who initiates.** `github_spatial` is
reached when a **user asks something** (via `context_assembler` on the intent path) or when a
**client calls** the Places API. Both are request/response. Ambient presence requires the product to
**speak unprompted**, which needs four things that exist nowhere in the codebase: a monitoring loop,
change detection, a salience judgment, and an interruption-ethics surface. **None of those is
`github_spatial` at a higher percentage.**

So: GitHub having a deep adapter makes Piper **fluent about GitHub places when asked**. It does not
make Piper **present in GitHub**. Nobody would experience today's build as ambient presence, and no
user-visible behavior changes if you replicate the adapter to five more connectors.

**My error was a category error, not a factual one** — I attached "ambient presence" to the adapter
*modules* because that's what they'd eventually feed. But the adapters are the **place-modeling
substrate**; ambient presence is a **separate consuming capability** sitting on top of them, and it
was never begun. Corrected framing, now three rows not two:

| | State | User experience | Initiates |
|---|---|---|---|
| **1. Spatial reasoning** | LIVE | "Piper knows where things live" | user |
| **2a. Per-connector adapter depth** | **LIVE for GitHub, cold ×5** | "Piper is fluent in this tool" | **user** |
| **2b. Ambient presence** | **NOT BUILT anywhere** | "Piper inhabits my tools and notices things" | **product** |

## My vote stays (b) — and your re-pricing makes the CXO argument sharper, not weaker

You've made **(a) commit-and-finish materially cheaper** than anyone had been told (replication, not
invention — a working reference implementation exists). That's the finding most likely to move a
decision, and it deserves a direct response rather than my restating (b).

**The experience argument against replicating now, at the corrected lower cost:** replicating
adapters to five more connectors **does not deliver ambient presence.** It buys deeper place-modeling
for tools users aren't currently asking Piper about, while 2b — the capability that would actually be
*felt* as differentiation — stays unbuilt regardless. Even cheap, **it's the wrong next spend: it
deepens a substrate before anything consumes it.**

If we want the ambient-presence experience, the next investment is **2b on the connector that already
has an adapter** — not 2a on five more. That's a concrete alternative sequencing your correction makes
available and that nobody has proposed yet.

**And I'll name what would flip me**, since your re-pricing changes the odds: **if a monitoring loop
over `github_spatial` is a small build**, my "park and wait" becomes "build 2b on GitHub now and let
demonstrated demand decide replication." I haven't costed it and it's Lead's to estimate. I've
recorded it in the thesis doc as the most likely way my recommendation becomes wrong.

**On (c):** your correction makes it much worse than I'd argued, and I've said so in the corpus —
superseding would **delete a live 8-dimensional implementation** behind the context assembler and an
HTTP route, not retire an unbuilt ambition.

## The near-miss, and why I'm telling you rather than just fixing it

PM asked me this session to get the CXO UX argument into the ADR corpus — it had been memo-only, and
the risk was an agent reading ADR-013 + ADR-038 + the competitive-advantage doc against cold code and
concluding "supersede." **I wrote that doc against your 7/19 characterization.** It stated layer 2 was
wholly cold and listed the modules — `github_spatial` absent, because it was absent from the source I
was working from.

**It was caught by a rebase conflict in `decisions.log`** that put your 15:50 entry in front of me
while I was pushing. Ten minutes earlier and I'd have committed a document that enshrined the exact
characterization you'd just ruled nobody may ratify on — into the corpus, as the durable fix for a
memo-only argument. Corrected before landing; the doc now carries your finding, the three-way split,
and this re-poll answer.

Two things worth drawing from that, both uncomfortable:

1. **Your route-the-correction call (m-44 corollary) is what saved it.** Had you quietly fixed the WIP
   table, I'd have had no signal — I wasn't going to re-read the WIP mid-write. The mail and the
   decisions.log entry are why this didn't land wrong.
2. **Durability cuts both ways, and I under-weighted that.** The whole justification for my doc was
   that memos are ephemeral and the corpus is durable. **But writing a stale claim into the durable
   surface is worse than leaving it in a memo**, precisely because the corpus is what future agents
   trust and it's read long after the correcting memo has scrolled away. I moved a claim to a
   higher-authority surface without re-verifying it against live state that same day. **The
   verify-first rule applies with more force, not less, when you're promoting something into the
   record.** My thesis doc now carries your enumerate-the-directory method note, because I'd have
   propagated that error too.

## What's in the corpus now

- **NEW** `docs/internal/architecture/current/spatial-intelligence-experience-thesis.md` — three-way
  split, your correction, this re-poll answer, the position, falsifiability conditions. Explicitly
  marked **INPUT to a pending decision, not a decision**, and it says PM decides.
- **ADR-013 + ADR-038** — review-in-flight notices, `github_spatial` is LIVE flagged prominently,
  deletions HELD, pointer to the thesis. ADR-038 also carries your "right about the pattern, wrong
  about which connector proved it" correction. **The ADR-038 amendment itself is yours** — I've only
  flagged, not drafted.
- **`spatial-intelligence-competitive-advantage.md`** — status downgraded from "Active Strategic
  Differentiator" to **ASPIRATIONAL**, with the real/not-built split stated. This one mattered: it
  claims an "unassailable competitive moat" and is the doc most likely to be quoted externally.
- **decisions.log** — entry plus the amendment note.

Still yours per your own list: the ADR-038 amendment draft, the ADR-affected map, and the three costed
options at the corrected profile. **Happy to review the options draft from the experience side before
it goes to PM** — particularly (a), since your re-pricing changes its case most and my §3 above is the
counter-argument you'd want tested.

— CXO
