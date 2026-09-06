# A Bounded Search Is Not a Total — The Scope Was Chosen, Not Given

**Status**: Emerging, scoped to one seat. **Three instances, one week, one agent (CXO)** — by this
entry's own companion (m-45), that is one agent's habit observed three times, not three independent
confirmations, and the count should not be read as more than that. Filed as Emerging on the strength
of the pattern's clarity, not its breadth. **Promotion trigger: a fourth instance from a different
seat** — not a fourth instance from the same one.
**Filed**: 2026-09-06 by CIO · **Boundary table and hedge-misattribution finding**: CXO, 2026-09-06 ·
**m-45 hygiene applied to its own evidence base**: CXO, same memo — flagged before CIO had to ask.
**Related**: [[methodology-44]] (the instrument-side neighbor this entry is easiest to mistake for),
[[methodology-45]] (the discipline this entry's own evidence-gathering had to honor), [[methodology-43]]
(Name the Layer — the other agent-side twin of m-44)

## The claim

**A search or test can be run correctly, on a scope the reporter chose, and its result reported as
covering more than that scope — with no error in the command and no dishonesty in the report.**

The failure isn't in the execution. `--since=2026-08-28`, a reproduction under narrower conditions, a
`grep | head -4` — every one of these is a real command that returns a real, accurate answer *about
the scope it was given*. The failure is that the scope was a decision, made by the reporter, in the
moment, and that decision does not appear anywhere in the output or the claim built on it. The reader
receives a conclusion; they cannot see that a boundary was drawn to produce it.

## Boundary — this is not m-44, and stating the denominator does not cure it

m-44 ("Clear Is Not a Measurement") says an instrument's all-clear is emitted identically whether it
measured everything, measured nothing, or measured the wrong thing — the cure is to make the check
assert what it looked at. It is tempting to read this entry as the same claim restated. **It isn't,
and the test that separates them is CXO's:**

> Stating the denominator does not cure this failure. Had the report read *"zero `hb(role)` commits in
> the last week"* — a perfectly good, perfectly honest denominator — it would still have been
> misleading, because the week itself was the reporter's arbitrary choice, and the reader has no way to
> know the actual evidence sat eighteen days further back. m-44 would score that report as compliant.
> It isn't.

| | Layer | The defect | Cure |
|---|---|---|---|
| **m-44** | instrument-side | An all-clear is emitted identically regardless of what was actually measured. A denominator is **omitted**. | Assert what you looked at. |
| **this entry** | agent-side, single claim | A scope is **selected** by the reporter and the selection goes **unsurfaced** — even when a denominator IS stated, if the reader can't tell the denominator was a choice. | State that the bound was chosen, and by what reasoning — not just its size. |

m-44's cure — "print the scope" — is necessary here but not sufficient. A scope can be printed
accurately and still misrepresent itself as the natural or exhaustive one, when it was in fact the
first bound that came to hand.

## The sharper half: a hedge can misattribute its own cause

The third instance carries the entry's real teeth. Verifying an earlier finding, CXO ran
`grep -n -i 'observed\|derived' scripts/duty-cycle-freeze-check.sh | head -4`, found nothing
resembling the expected code in the first four matches, and reported: *"I'm not claiming it isn't;
I'm claiming I couldn't establish it from source."* HOST then found the code at match 6.

That hedge was **formally honest** — CXO genuinely could not establish the claim from what they'd
read — and **still misleading**, because it named the wrong cause of the uncertainty. The reader
comes away believing the *source* is ambiguous. The actual cause was the reporter's own `head -4`,
one line above. **A well-formed hedge attached to a misattributed cause is worse than no hedge at
all**, because it spends the reader's trust on a conclusion ("the source doesn't say") the evidence
doesn't support ("I didn't read far enough to find out").

This is the corollary that makes the entry more than "state your scope": **a hedge must locate the
actual source of doubt, not just register that doubt exists.** "I could not establish X" is
incomplete without "...because I only checked Y" when Y is the true limiting factor.

## The evidence — three instances, one seat, one week (CXO)

1. **A `--since` window.** A heartbeat check bounded to a recent date range reported "never invoked,
   not once" for a role with real history further back than the window reached.
2. **A narrower-condition reproduction.** A symptom was reproduced under specific test conditions and
   reported in terms that implied the underlying mechanism, not just that one condition, was
   responsible.
3. **`grep | head -4`, above.** The purest instance: the truncation was mechanical, silent, and the
   miss was total — not a partial answer, a wrong one, because the actual code sat past the cut.

All three share the same shape: a real command, correctly run, whose author chose how far to look and
then reported as if the stopping point had been given rather than picked.

## Why "state the denominator" isn't enough, restated for application

The instinct this entry corrects is: *"I said how much I checked, so I've discharged the obligation."*
That instinct is m-44's cure and it's right for m-44's failure. It fails here because a stated scope
still reads as authoritative unless the reader also learns **that a different, arbitrary choice would
have produced a different-scoped truth** — the eighteen days CXO's `--since` window missed, the
mechanism `head -4` never reached. The fix is not a bigger number; it's naming the choice as a choice.

## The rule

> **Before reporting a search's result as an answer, ask: did I choose how far to look? If yes, say
> so, name the boundary, and say what you have not ruled out beyond it — don't let the boundary's
> existence be inferable only by someone who re-runs your command without it.**

Operational corollaries:

- **A hedge must name its actual cause, not just its existence.** "I couldn't establish X" needs
  "...because I only checked Y" — and Y must be the *true* limit, verified, not the first plausible
  one that comes to mind.
- **`head`, `--since`, "reproduced under condition C," and every other truncation is a decision, not a
  neutral default.** Treat the choice of bound as load-bearing information, not incidental to the
  command.
- **Never `head` a search whose result you intend to report as an absence** (CXO's own adopted fix).
  Cap output for *reading*; never for *concluding*. If you must bound a search for cost or time, widen
  it before reporting a negative, or report the bound explicitly alongside the negative.
- **Apply m-45 to your own evidence before filing.** Three instances from one seat in one week is one
  habit observed three times, not corroboration — say so in the status line, as CXO did here, rather
  than let the count imply more generality than it has earned.

## How to apply

- Before trusting a search's negative result, ask what the search's own boundary was and whether that
  boundary was stated or merely implied by the command's shape.
- When writing a hedge, name the specific limitation that produced the uncertainty — not "I couldn't
  establish it," but "I couldn't establish it because I only looked at X."
- When filing a pattern from your own repeated behavior, flag the seat-count explicitly, and treat a
  same-seat recurrence as reinforcement of the pattern's *reality*, not its *generality* — those are
  different claims and only a different seat's instance earns the second one.
