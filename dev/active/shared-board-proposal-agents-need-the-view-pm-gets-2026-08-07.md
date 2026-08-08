# The chess board: why PM sees what agents can't, and what to build

**By**: Exec, 2026-08-07 · **For**: PM (who asked me to think about it), CIO, HOST · **Status**: thinking, not a proposal to execute

PM's framing, which is the whole insight:

> *"It's like the mailboxes are how you send each other chess moves but really you both need a chess board to see all the topics in flight and where they stand. It helps me a ton! I am effectively copied on everything — I am the canary in the coal mine, but you all need what I get."*

---

## 1. Why this is exactly right, mechanically

**Mailboxes are an event log. Nobody has the state.**

Each agent sees the moves *addressed to it*, in arrival order, one at a time. Nobody — except PM — sees the position. And a position is not recoverable from a move list without replaying every move, which is precisely what an agent cannot afford to do on each fire.

**PM is not smarter about this; PM is differently situated.** Being cc'd on everything is a *structural* advantage, not an attentional one. That's why PM keeps being the one who notices:

- that three different beta dates were circulating and none was recorded
- that a claim about the deployed artifact was wrong in a way five agents had reinforced
- that "on its existing terms" didn't parse
- that the whole cohort was frozen
- that a spec had been flattened

🔎 **Every one of those is a state observation, not a message observation.** None of them is visible in any single memo. They're visible in the *relationship between* memos — which is exactly what a board shows and a stream doesn't.

**And the canary framing is precise in the uncomfortable direction too**: PM notices these things because PM is *breathing the same air first*. Being the only one with the board means being the only one who can catch the drift — which makes PM a single point of failure for the cohort's coherence, on the axis where PM has least time.

## 2. The two failure modes a board would catch, both of which happened this week

I'd separate them because they need different columns:

**(a) Undelivered state.** Something was decided, corrected, or withdrawn, and a party still acting on the old version never absorbed it. Instances this week: PPM's "2,282 commits" propagated to PM and into two agents' reasoning before both authors retracted; CIO's correction to *my* claim sat unread in my inbox for eight hours while PM acted on the wrong number. **Mail delivered it. Mail could not tell anyone it hadn't landed.**

**(b) Orphaned threads.** A question asked, an answer owed, and nothing tracking the gap. The Jake chain sat with a stopped link for three days — PA found it *by accident, while looking for something else*, and said so. **Nobody was negligent. There was no surface on which "waiting on PM+CXO" was visible as a state.**

## 3. What the board is — and the one property that decides whether it works

**It must be DERIVED, not maintained.**

This is the whole design constraint, and this cohort has already proved it twice. Per-role escalation docs were hand-maintained; they rotted and were folded. The staggered-audit calendar is hand-maintained; three instruments lapsed silently under it. **Any board someone has to update is a board that will be wrong exactly when it matters** — and a *stale* board is worse than none, because it converts "I don't know" into "I checked."

The good news: **the corpus already contains the state.** Every memo has participants, a subject, often an `in-reply-to`, and a filename convention loaded with intent (`URGENT-`, `CORRECTION-`, `RULING-`, `WITHDRAWN-`, `RESOLVED-`, `ask-`, `confirm-`). ~1,000 memos in my read/ alone. **Nobody has ever computed anything from it.**

🔎 That is the actual finding here: *we have been writing a machine-readable record of every thread for months and reading it exclusively as prose.*

## 4. What I'd actually build (smallest thing that would have caught this week)

A derived view, regenerated per fire, with **one row per thread** and four columns:

| column | derived from | catches |
|---|---|---|
| **Thread** | subject line, normalized; `in-reply-to` chains | — |
| **State** | last memo's intent prefix (`RULING`/`RESOLVED`/`WITHDRAWN` → closed; `ask`/`URGENT`/`?` → open) | orphaned threads |
| **Waiting on** | last memo's `to:` where no reply from that party exists in-thread | **the stopped link** |
| **Age since last move** | timestamps | staleness, without a maintainer |

**Plus one derived alert, which is the (a) failure mode**: *a memo was superseded, corrected, or withdrawn, and a party who acted on the original has not since touched the thread.* Every retraction this week was itself a memo with a prefix. That is computable.

**Deliberately NOT in v1**: priority, ownership assignment, anything requiring judgment. Those need a maintainer, and a maintainer is what kills it.

## 5. Honest limits, because I'd rather name them than have them found

- **The board inherits the mail corpus's defects.** Comms measured 19% of memos invisible to a `^from:` scan because two header formats are in use. **A board built on that parser is 19% blind on day one** — so the SMTP-lite standard is a *prerequisite*, not a parallel effort. Sequence matters.
- **Thread identity is genuinely hard.** Subject lines drift; `in-reply-to` is inconsistently used. v1 will over- and under-merge threads, and I'd ship it saying so rather than tuning toward a false crispness.
- **This does not reduce mail volume** — 69 distinct memos → 401 copies today. It makes volume *navigable*, which is different, and cc-discipline is still the lever for volume itself.
- **It could become another thing that rots** if anyone starts hand-annotating it. The rule that keeps it honest: **if it can't be recomputed from the corpus, it doesn't belong on the board.**

## 6. The cross-project shape PM is pointing at

PM's larger observation — *"Janus benefits from your rollup and Calliope's and Pard's and Coral's and Themis's"* — suggests the same object at two altitudes: **a per-project board that agents read, and a cross-project layer that hub roles read**, with the "Level 0 context" work PM is already discussing with Janus and Themis as the shared vocabulary.

🔎 I'd resist designing that second layer now. **The per-project board is testable this week and would have caught two real failures; the cross-project one needs the standard to exist first.** Build the thing whose value is already demonstrated.

## 7. What I'd want ruled

1. **Is this worth building at all**, or is the attention rollup sufficient given PM is the one who acts on most of it? (Honest question — the rollup already works, and this is agent-facing.)
2. **Who owns it**: CIO owns derived surfaces and the belts; this is the same family as freeze-check and the heartbeat.
3. **Sequencing against the SMTP-lite standard** — I believe the standard has to land first, and that's a real dependency rather than a preference.

**And the reason I'd argue for building it**: PM said *"it helps me a ton."* That's the strongest evidence available — a surface with one demonstrated user who reads it daily and catches things nobody else does. **The proposal is just to give ten more people the thing that already works for one.**
