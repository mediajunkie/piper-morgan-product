# Chokepoint vs. Bolt-On — Attach the Obligation to Something That Can't Be Skipped

**Status**: Proven-by-use, filed late. **This is not a new claim** — it has shaped at least four
shipped mechanisms this week (the role-health-check natural experiment that motivated it, the
NO-SESSION-LOG detector, the subagent-worktree cleanup fix, and the duty-cycle backlog-intake
amendment) plus the 7k synthesis sent to PM — entirely as oral tradition in `decisions.log` and
memo prose. HOST found the gap while independently reading the corpus for the flywheel
re-evaluation: **the word "chokepoint" appears nowhere in `methodology-core/`, not even
`INDEX.md`.** Filed now because a concept doing this much load-bearing work deserves a citable
home, not because the idea itself is new.
**Filed**: 2026-09-08 by CIO · **Origin**: CIO's design principle, first named in mechanism form
during the 2026-09 recurring-duty investigation · **Natural experiments supplying the strongest
evidence**: HOST, 2026-09-04 (role-health-check pre/post 2026-08-07); CXO, 2026-09-12 (five
independent lapses on one seat, sharper "success indistinguishable from skipping" phrasing,
corroborated by Exec's clean-seat contrast case) · **Gap found**: HOST, 2026-09-08, while answering
Q4 of the flywheel re-evaluation
**Related**: [[methodology-36]] (mechanisms over vigilance — this entry's closest ancestor; this is
the specific *test* for telling which mechanism-shape actually holds), [[methodology-50]]
(self-attestation is not verification — the complementary half: a chokepoint stops the skip, a
machine-written artifact stops the false belief that a skip didn't happen)

## The claim

**A recurring obligation survives if it is attached to something that already cannot be skipped
without visibly breaking a procedure in progress. It decays if it is attached beside that
procedure as an additional, independently-skippable step — regardless of how important the
obligation is, how well-documented it is, or how much anyone cares about it at filing time.**

The distinguishing test:

> **Can this step be skipped without visibly breaking the procedure you're already running?**

If yes, it's a bolt-on. It will decay — not from carelessness, but because a step with no attached
consequence is structurally indistinguishable from an optional one, and vigilance is not a
mechanism (methodology-36). If no — skipping it means not running the procedure at all, or
producing an output the procedure's own consumer will visibly reject — it's a chokepoint, and it
survives.

## The evidence — a controlled natural experiment, not a plausible theory

**Role-health-check, same duty, same owner, before and after one design change** (HOST,
2026-09-04):

- **Before 2026-08-07**: a GitHub Action files a `sapient-trust`-labeled issue on a schedule;
  picking it up depends on someone remembering to check for it. **Result: 54 days between
  consecutive closures on a 28-day filing cycle** — one full cycle missed. The habit of checking
  rotted; the actual unattended-artifact window (issue-open to issue-closed) was 4 days, not 54 —
  but the mechanism itself, "will anyone look," went dark for roughly two months.
- **After 2026-08-07**: the same check became Step 1a of `duty-cycle-tick` — run unconditionally,
  every fire, not optional. **Result: closed same-day, 28-day cycle, first full run under the new
  form.**

Nothing about the underlying duty changed. What changed is whether skipping it is *visible*.

**Four more instances since, all using the test above at design time rather than discovering it by
decay**:

- **NO-SESSION-LOG detection** (standing-item 7q). The fix for a PM-initiated day silently skipping
  session-log creation was keyed on "did a role-tagged commit happen" — the same signal the
  heartbeat's own `--if-quiet` already used — rather than a new reminder to remember to log.
- **Subagent worktree cleanup** (standing-item 7r). Rather than add a new "remember to delete your
  worktree" step, the fix extended CLAUDE.md's existing, already-mandatory "commit verification
  after subagent work" checklist — a step that already ran at the moment closure was claimed.
- **Duty-cycle backlog intake** (2026-09-08, this same day). PM found that "there is no work" and
  "28 open milestone items" were both true because the Task Loop's own definition of "drained"
  excluded the backlog — a role idling on an empty inbox was the procedure working exactly as
  specified. The fix redefines what "drained" means inside the loop's own already-mandatory exit
  check, rather than adding a fourth loop beside the existing three.
- **7k's own synthesis** (the joint recurring-duty document sent to PM 2026-09-07) used this test
  as its central diagnostic across every instance in its inventory, including a case where the
  *diagnosis itself* was correctly made and never routed — "the writing-down was not a chokepoint."

## A second independent natural experiment, and a sharper phrasing of the test (CXO, 2026-09-12)

CXO found five of their own steps had silently stopped running — `check-refresh-promises.py`
(never run, ever), the duty-cycle heartbeat (24 days), the MANIFEST regen (36 days), the
`DAY-CLOSED` marker (16 days), and (via Exec's parallel check on a second seat) the same marker
gap corroborated as real rather than seat-specific. CXO's first hypothesis for what the five
shared — *"the consumer isn't this fire"* — was wrong, and CXO found the counterexample themselves
before proposing it: `check-refresh-promises.py`'s consumer **is** the running fire, and it still
rotted. The corrected discriminator is sharper than this entry's original phrasing:

> **If running a step and skipping it produce the same visible output at the end of the fire, the
> step will rot. It needs an external consumer or a distinguishable output — never a firmer
> intention.**

This restates the test above (a chokepoint's absence breaks something visibly; a bolt-on's absence
doesn't) but locates the *mechanism* precisely: it isn't about who consumes the step, it's about
whether success and skipping are distinguishable **at all**, to anyone, including the agent who
just ran it. A heartbeat that self-suppresses on a quiet fire writes nothing either way. A MANIFEST
regen that finds nothing new writes nothing either way. The step can have a real external consumer
(a future freeze-check, another role's inbox) and still rot, because the *fire in which it either
ran or didn't* has no way to tell which happened.

**This is independent corroboration, not a restatement of the same instance**: HOST's original
natural experiment (role-health-check, one duty, before/after one design change) and CXO's five
instances (one seat, self-audited, cross-checked against Exec's clean 13-of-14 seat as the
contrast case establishing this isn't universal) are two different seats supplying the strongest
evidentiary shape this claim can take, independently. CXO explicitly declined to claim cohort
prevalence from their own evidence — correctly, since Exec's clean seat is the needed contrast
that shows the failure isn't structural to every role, only to roles where a step's completion
produces no distinguishing trace.

## Boundary — this is the test; methodology-36 is the general principle it operationalizes

m-36 (mechanisms over vigilance) says a hoped-for behavior needs a mechanism, not a reminder. This
entry supplies the specific test for whether a candidate mechanism is actually one: does removing
it produce a *visible* break in something already running, or merely an invisible gap beside it?
Two mechanisms can both look like "we built something" and differ completely on this axis — a
reminder inside a checklist nobody re-reads is still a bolt-on even though it's "in the docs now."

## Why this is an edge case of anti-instrument-sprawl, not an exception to it

A live question this week (Exec, on the backlog-intake amendment): does converting a bolt-on into
a chokepoint count as "adding a layer" under a refactor-not-add constraint? **No, when the
conversion redefines an existing mandatory step's own exit condition rather than adding a new
artifact, reminder, or tracking surface beside it.** The anti-sprawl principle protects against
proliferating new things to remember; a chokepoint conversion typically *removes* an idle/skip
state from an existing loop rather than adding new surface area. Test both independently before
assuming they conflict: "does this add a new artifact?" and "does this make an existing exit
condition more complete?" are different questions, and a change can answer no/yes at once.

## The rule

> **At design time, before shipping a new recurring obligation, ask: can this be skipped without
> visibly breaking the procedure it rides on? If yes, don't ship it as a reminder — find the
> already-mandatory step it can attach to instead, or accept that it will decay and needs a
> different design.**

Operational corollaries:

- **A "we added a check for this" report is not evidence of durability** — ask whether the check
  itself is skippable. A check nobody is forced to run is a bolt-on with extra steps.
- **Pair with methodology-50**: a chokepoint stops the skip; it does not stop a false belief that
  the chokepoint ran. If the step can be satisfied by self-report rather than a machine-written
  artifact, add that too — the two failures are independent and a fix for one does not cover the
  other.
- **The natural-experiment shape (same duty, same owner, one design change, before/after outcome)
  is the strongest evidence this class of claim can produce** — stronger than a plausible theory or
  a single instance, and worth deliberately looking for when evaluating whether a fix actually
  worked.

## How to apply

- When a duty has decayed, before writing a new reminder, ask what already-mandatory step it could
  attach to instead — a fire's own step sequence, an existing checklist, a loop's own exit
  condition.
- When designing a new obligation from scratch, run the chokepoint test before shipping, not after
  months of silent decay reveal the answer.
- When judging whether a design change is "adding a layer," check separately whether it adds a new
  artifact/reminder/surface and whether it completes an existing step's definition — these are not
  the same question and a change can pass one test while failing the other.
