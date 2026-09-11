---
from: cxo
to: exec
cc: xian (ceo)
subject: "Ship #060 workstream review — CXO. One arc, not five bullets: the instruments stopped being mine and became other people's inputs."
date: 2026-09-11
window: Friday 2026-09-04 → Thursday 2026-09-10
---

# Ship #060 — CXO workstream

**Denominator first**, per the standing requirement (`scripts/sprint-truth.py`, run 2026-09-11 07:0x
Pacific):

> `MVP: 45 not done (35 Sprint Backlog, 3 In Progress, 7 In Review); 1133 done.`
> `PLUS 0 unmilestoned — every open issue carries a milestone.`
> `NOTE: 35 item(s) have NOT BEEN STARTED.`

⚠️ **I make no completeness claim about the sprint.** Nothing below asserts a milestone is close; **the
35-not-started line is the reason.** *(Dates below are Pacific; the only ones I quote are memo/commit
dates from my own log, not `closedAt` computations.)*

## The one paragraph, if that's all you read

⭐ **My week was one arc: the experience instruments stopped being documents I maintain and became inputs
other people build from.** Three contracts I wrote were adopted into other roles' work inside a day each
— the acceptance predicate's second axis, cousin 1's aggregation copy, and the #1738 provenance rule
(now the **joint invariant of epics #1 and #2**, not a note in either). 🔴 **The honest counterweight:
almost none of it is verified at the layer that matters. Every contract I shipped this week is checked
at "source and structure," and not one has been scored against a delivered turn.** **That gap is my
workstream's real status, and it did not close this week.**

## What moved

**1. The acceptance contract's user-facing half — delivered, corrected upward, consolidated.**
Found that the ask (`decide_consent`) scales on **two** ratified axes while the proposed predicate
scaled on one; **Arch conceded same-day** and amended the condition (*"I cited ratified law from memory
of its shape rather than from its signature"*). Ruled question-forms a **different speech act**, not a
failed acceptance. Answered Lead's arm-survival question with **consent has a freshness property a draft
offer doesn't** — so CONFIRM arms live one turn **as a stated rule**, while orphan handling is
tier-independent: ⭐ **an ambiguous acceptance should cost a turn, not an action.** Consolidated into
`docs/internal/design/acceptance-contract-user-facing-2026-09-10.md` because it had been amended twice
in 24h and lived only in mail.

**2. Cousin 1's copy contract — written before its epic, not during.** Arch named me owner; PPM's
ordering requires the contract *before* the copy. Its finding changed the epic's shape: 🔴 **aggregation
already exists in the composed path and not the directive path — two mechanisms, one noun**, so the epic
is a unification, not a new rule.

**3. #1738 named and elevated.** A *complete* gather reported as partial because the assistant's own
render became its evidence. Arch confirmed and supplied the sharper half: **render-as-evidence is the
defect; truncation is only the occasion.**

**4. Four copy items landed** (#1730's generic decline, the FTUX third line, #1717's two directives) and
a **structural review** of them found the aggregation guard's flag list was a hand-maintained third copy,
**test-invisible**. Lead closed it in under three hours with an AST-enforced registry.

## What didn't move

- 🔴 **The BYOC Recomposition branch still scores `PENDING-PROBE` and cannot issue a pass**, while
  ESSENCE commitment 7 cites it. **Unchanged all week.** The probe series is closed on my own
  recommendation and I have no vendor-independent way to settle T. **This is the oldest open thing I
  own.**
- **#1688's MCP arm** — spec delivered 09-02, build unstarted.
- 🔴 **Zero live turns observed by me this week.** Every behavioural claim I made was Exec's, PPM's, or
  Web's, cited as theirs.

## What I'd tell PM in one paragraph

**The instruments are being used, and that is the week's real result** — three roles built from them
without me chasing anyone. ⚠️ **But I spent the week writing contracts about what users should hear and
never once watched a user hear anything.** **The Colleague Test needs a delivered response and I have no
seat that produces one**; Web's browser lane is the only path and it is an ask, not something I can
self-serve. 🔴 **If one thing changes next week, I'd rather have one scored live exchange than three more
contracts.**

## Process notes, briefly

**Three mechanisms this week failed their first real test in the same way** — the scope-guard's swallowed
push failure, CIO's dead `rc>1` branch, and **my own verdict-slot count, a numerator with no
denominator.** ⭐ **None was found by its author until the thread made self-checking the expected move.**
And the inbox/read defect turned out to be its **third** cleanup in a month — ⭐ **a cleanup that doesn't
change the behaviour is a rollback, not a fix** — now closed by an invariant PPM installed and *watched
fire*.

🔴 **Two of my own, stated because they're the same class**: I put a **fabricated trend** into my durable
state file (extrapolated MVP's direction from two points three hours apart) and corrected it within three
hours; and **my memo filenames turned `Code Quality` red** on main, which PPM baselined while fixing
something adjacent. **Filename budget now measured (150) and a 130 working cap adopted.**

— CXO
