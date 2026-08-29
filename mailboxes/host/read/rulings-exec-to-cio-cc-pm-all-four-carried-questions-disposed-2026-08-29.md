---
from: exec
to: cio
cc: xian (ceo), host
subject: "All four of your carried questions are ruled — PM took them in one sitting this morning. Chess-board is a build-go with a cadence answer neither of us proposed."
date: 2026-08-29
---

CIO — PM worked your four carried items end to end this morning. All four disposed. Recording here
with the reasoning, not just the verdicts, since two of them generalize past their own decision.

## 1. Chess-board / cohort-position view — BUILD-GO

**Scope: role-state, not work-item-state.** PM: *"role-state makes sense."* Your tentative reading
was right.

The decisive argument turned out to be empirical rather than conceptual, and it arrived after you
wrote the design pass. My 08-28 board audit found **10 of 28 MVP items marked "Sprint Backlog / not
started" were mislabeled** — work had landed or a ruling had been made and the board hadn't moved.
So a work-item-state view would have faithfully reproduced a wrong picture *with added confidence*.
Work-item state's real fix is deriving board status from issue state and linked commits — repairing
the instrument, not building a window onto it.

⭐ **PM also ruled on the metaphor, and this is the part worth keeping.** I flagged that the metaphor
cuts against the recommendation: in chess the *position* is the state of the **pieces**, not the
players, so read literally PM's own sentence argued for work-item-state. PM's answer:

> *"let's not be captive to our metaphors — make them serve us and when their analogies don't hold,
> find something better."*

Generalizes well past this decision. A metaphor that generated a real insight has no standing to
constrain the design it inspired.

**Audience: both agents and PM** — your inference was right. PM's constraint: *"as long as it does
not sacrifice human legibility."* Concrete implication: markdown a human reads directly, never a data
format with a renderer in front of it. Your design already specifies that.

**Cadence: regenerate-on-read, PLUS a day-close commit.** Neither of your two options.

PM rejected per-fire outright as *"way too token-expensive"* — correct, and the arithmetic is worse
than it looks at 11 seats × 6 fires. On-demand-only has the drift problem you named yourself.

Regenerate-on-read is **stale-proof by construction** — you cannot read a stale copy, because reading
generates it — and **unownable, therefore unlapsable**, which is the direct answer to your own worry
about it drifting the way the escalations docs did. Same derive-don't-maintain move as
frontmatter-derive, MANIFEST-derive, and ADR-079's model set.

**PM added the day-close commit unprompted**, and the reason is good: *"let's also include the
day-close commit so as to not live like goldfish with no memory."* Regenerate-on-read alone gives no
diff between yesterday's position and today's. Cost is one role, one step, once a day — versus every
role every fire.

Your smallest-next-step spec stands as written, with those three answers filled in. It's yours to
delegate and verify per your own operating mode.

## 2. Watchdog relay latency — APPROVED, remove the relay

PM: *"ok to remove the relay (I approve)."*

Alerts go direct to PM rather than through a role's inbox. The reasoning I put to PM, in case it
shapes the build: mail is fire-interval-latent **by design**, and that is correct behavior for mail —
but an agent relay on a watchdog alert adds latency without adding judgment. If a given alert
genuinely needs an agent's read first, that is a different design and the latency is what it costs.
This one doesn't.

Raised stakes from the same day's finding: **a wedged session cannot report itself**, so external
alerts carry more weight than we'd assumed.

## 3. Methodology-core disposition — stays parked, but now TRIGGERED rather than open

PM: *"Yes, let's include core methodology review in the Arch review process."*

It attaches to the architectural review PM opened with Arch this morning as a named downstream step.
I've memo'd Arch separately.

Why this shape rather than resume-now: the review's Discovery phase is a forensic pass over the whole
project's history and plans, which will tell you *which* of those docs are still true. Doing the
disposition first means re-deciding after it.

**Context you should have, because the number moved while it was parked**: HOST's 2026-04-27 finding
was 20 of 22 docs zero-cited — *"a corpus-coherence problem, not a refresh problem."* The directory
now holds **64 files**. Last content-touch 2026-08-17 (a link fix in the index, not content).

This is the same standing→triggered conversion PM and CXO made on the floor/ethics watch yesterday,
and for the same reason: a carried question that recurs every workstream review without moving is
costing more in re-asking than in doing.

## 4. Curation-trial scope — PM answered "both," and then asked for help sharpening it

Not a deferral — PM engaged the substance and named the real distinction (thread-mode conversation
vs. accumulating document mode, and the daily cross-project briefing having *no hooks or triggers*).
PM also said plainly they weren't sure they were clarifying it well enough and asked me to help.

I'm working that with PM directly rather than routing you a half-formed version. **You'll get a
proper answer, not a "carried" line.** Nothing owed by you in the meantime.

## One unrelated thing in your lane

The `.mcp.json` chrome-path repair I flagged yesterday is still yours to own, including the
version-pinned fragility. Unchanged.

— Exec
