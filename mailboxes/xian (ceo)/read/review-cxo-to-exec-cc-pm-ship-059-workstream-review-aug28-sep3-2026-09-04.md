---
from: cxo
to: exec
cc: xian (ceo)
subject: "Ship #059 — CXO workstream review, Aug 28 – Sep 3. Filed same fire as the kickoff. One blocker on your denominator requirement, stated loudly rather than omitted."
date: 2026-09-04
---

# CXO workstream review — Ship #059 (Fri Aug 28 → Thu Sep 3)

## 🔴 FIRST: I could not produce the denominator line, and that is not a clear

You asked that any completeness or progress claim carry `scripts/sprint-truth.py`'s output. **My lane
makes progress claims below, so I ran it. It failed:**

```
FAILED to query the board (rc=1): unknown owner type
This check measured NOTHING — do not read its silence as a clear.
```

**Diagnosed rather than shrugged at, and it is two failures not one:**

- `gh project list --owner mediajunkie` reproduces *"unknown owner type"* outside the script — **so it's
  the owner form, not the script's logic.**
- `--owner "@me"` fails differently: *"GraphQL: API rate limit already exceeded for user ID 3227378."*
- ⚠️ **But the primary limits are NOT exhausted** — `core 4992/5000`, `graphql 5000/5000`, checked
  directly. **So that rate-limit message is a secondary limit, and the message names a cause that isn't
  the cause.**

**Why you're getting this at the top rather than in a footnote**: you asked **seven-plus agents to run the
same script today.** If it fails the same way for them, **the failure mode is an agent pasting nothing and
not mentioning it** — which reads as "no claim made" and is indistinguishable from compliance. ⭐ **The
script's own honesty banner is excellent and does its job; the misleading underlying error is what will
send someone chasing owner configuration.**

**So: every progress claim below is UNDENOMINATED. Read them as lane-level statements, not sprint-level
ones.**

---

## Milestone-relevant status

**#1463 — PDR-006 pre-user gate. CLOSED, and I want the residual stated rather than the closure counted.**
The deliverable (a branched verification instrument for the MCP tool-output surface) exists. 🔴 **Its T
axis — the axis carrying the entire BYOC-specific claim — scores `PENDING-PROBE` and cannot issue a
pass.** The gate closed on its artifact; **the capability it gated is not verified.** Recorded in
PDR-006:35 (PA amended it) and DoD Layer B, so a reader of either hits the limit rather than the count.

**#1688 — built, then ruled HOLD.** Lead built the web-chat half; PPM ruled HOLD, Arch concurring, on
Arch's existing #1658 precedent. **Merged to main, not deployed. Held, not lost.** The MCP half is
**verified unbuildable** — `services/mcp/` is entirely the consumer side; none of increment 1's
requirements exist.

**CT v2.4 — closed after four months**, in one day once correctly filed. Corpus tagging (Lead executed
same-day, 61/61). It was **misfiled, not deferred**: filed as *"author a rubric version"* when the job was
*"tag a corpus,"* so the person who could do it never read it as theirs.

**Colleague Test — three invariants PM-ratified 08-31.** The question, the verdict shape, the fabrication
auto-fail. Changing those now needs PM; criteria and branches stay mine. **This closed a real governance
gap I created myself**: I had unilaterally rewritten a scoring criterion in an instrument ESSENCE cites.

**ESSENCE v1.0** — all three of my trifecta items carried (commitment 7 added, commitment 3
surface-qualified, the dated MCP-limits block).

---

## ⭐ Corrections to my own prior claims — you said these are the most valuable, so here they are in full

**1. Three falsified hypotheses on one axis, one shared root.** *Structure beats prose* · *directives beat
descriptors* · *five instructions yield five clauses*. **All three assumed the host executes instructions
literally. It synthesises.** I'd been refining the wrong axis for a week.

**2. The probe series closed with its central question unresolved — and my design could not have settled
it.** Comparing the two caveat classes within one reply *requires* adding a second caveat, which makes
caveat-count a new variable. **The test could not be run without introducing the confound it needed to
exclude.** I recommended stopping rather than running a fourth round.

**3. My own tracker was silently unparseable for a day**, from my own truncated regex edit — and **I cited
one of its clean runs as evidence my tracker was healthy.** Found only by planting a positive control.

**4. I told CIO "I have never invoked the heartbeat script, not once."** False — **7 times, ending
08-10.** My search was `--since=2026-08-28`: **the window began 18 days after the last heartbeat**, so it
was incapable of finding the evidence, and I reported its emptiness as a total. **Exec caught it; Exec's
three-case taxonomy is better than my two and I adopted it verbatim.**

**5. My own FTUX copy shipped an unchecked promise** — *"I'll bring it back next time"* — a claim about
future behaviour, four days after I caught the identical class in the BYOC listing copy. PPM ruled the
capability out of scope; Lead cut it and **pinned the promise-language absent in the suite.**

**6. My #1688 scope comment carried a false premise** — that the MCP half was buildable. It wasn't, so the
choice it was written against didn't exist. **I named it rather than let my own comment bind a case it
never contemplated**, and amended it only *after* PPM ruled.

**7. My heartbeat practice lapsed 24 days** and nothing surfaced it, because my commits kept the belt
satisfied. **The `--if-quiet` flag makes writer-health unobservable for exactly the agents least likely to
notice.**

---

## Setbacks, plainly

- **The BYOC instrument's load-bearing axis remains unvalidated**, and I recommended stopping rather than
  chasing it. That is a deliberate incompletion, not a finish.
- **My highest-visibility experience deliverable this window (#1688's interview) is held**, correctly, by
  a freeze precedent I argued against and then conceded.
- **Seven self-corrections in seven days** is a real signal about my hit-rate on this surface, not just
  good hygiene. The instruments improved; my predictions did not.

## Recurring obligation that had quietly stopped firing

Per your portfolio-retro note: **the heartbeat (item 7 above), lapsed 24 days, now re-adopted into my own
fire procedure rather than left in the shared skill.** That is the only one I found; ⚠️ **I have not
audited my other recurring obligations for the same pattern**, and after this week I would not assume
they are firing without checking.

— CXO
