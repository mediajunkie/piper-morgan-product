---
type: methodology
title: A Bounded Search Is Not a Total — The Scope Was Chosen, Not Given
valid_from: "2026-09-06"
last_updated: "2026-11-12"
---

# A Bounded Search Is Not a Total — The Scope Was Chosen, Not Given

**Status**: Emerging. Set 2026-11-12 by CIO (standing item 9p).
**Summary**: A search covers only the scope you chose, so before saying "none exist" confirm the scope matched the question and report its limits.

**Status (2026-11-02)**: Emerging, **four seats**: CXO (three instances), Lead (10-17), Arch (10-23, caught in review before it ran), CIO (11-01, a search bounded by one name; 11-02, a search bounded by its own context padding, caught because it was sent as a question); see the sections below. Promotion review at the 12-09 audit. **Original status (2026-09-06)**: Emerging, scoped to one seat. **Three instances, one week, one agent (CXO)** — by this
entry's own companion (m-45), that is one agent's habit observed three times, not three independent
confirmations, and the count should not be read as more than that. Filed as Emerging on the strength
of the pattern's clarity, not its breadth. **Promotion trigger: a fourth instance from a different
seat** — not a fourth instance from the same one.
**Filed**: 2026-09-06 by CIO · **Boundary table and hedge-misattribution finding**: CXO, 2026-09-06 ·
**m-45 hygiene applied to its own evidence base**: CXO, same memo — flagged before CIO had to ask ·
**Re-examined**: CXO, 2026-09-07 — re-sorted their own broader instance list into two distinct
families (this entry vs. a proxy-instead-of-artifact shape) and flagged instance #2 below as
borderline in the process, rather than let a shakier instance sit unexamined once a cleaner
boundary existed to test it against. **Resolution**: the proxy-instead-of-artifact material split
further on inspection — two of its four candidate instances are methodology-49 (a mechanism's
runtime state assumed rather than observed), folded into that entry's corroborating list; the
remaining two (a document miscited from memory, a checklist ruled on from its title) are neither
this entry's shape nor m-49's, and are now filed as [[methodology-52]].
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

> Stating the denominator does not cure this failure. **Worked example, from CXO's own m-50 incident**:
> had the report read *"zero `hb(cxo)` commits in the last week"* — a perfectly good, perfectly honest
> denominator — it would still have been misleading, because the week itself was the reporter's
> arbitrary choice, and the reader has no way to know the actual evidence (7 real invocations) sat 24
> days further back. m-44 would score that report as compliant. It isn't.
>
> *(Added 2026-09-06, at CXO's own request — "if it needs a worked example, mine is the cleanest,"
> flagging that the discriminator above is the subtle half of this entry and the one a reader is most
> likely to skim past without a concrete anchor.)*

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
2. **A narrower-condition reproduction** *(borderline, flagged by CXO on 2026-09-07 re-sorting their
   own evidence rather than let it stand unexamined: here the thing narrowed was the reproduction's
   *conditions*, not a search's *scope* — close enough to belong provisionally, not clean enough to
   anchor the entry on)*. A symptom was reproduced under specific test conditions and reported in
   terms that implied the underlying mechanism, not just that one condition, was responsible.
3. **`grep | head -4`, above.** The purest instance: the truncation was mechanical, silent, and the
   miss was total — not a partial answer, a wrong one, because the actual code sat past the cut.

All three share the same shape: a real command, correctly run, whose author chose how far to look and
then reported as if the stopping point had been given rather than picked.

## A second seat: Lead's re-run set before a push (CIO, 2026-10-17)

This is the different-seat instance the status line said the entry needed. Lead verifies a change by
re-running a chosen set of test directories, then pushes. CI runs the whole suite. Three times in three
days, the chosen set was narrower than the layer that broke, and main went red:

1. **10-15:** three red windows on main, each a test-layer miss of the merge re-run, each fixed
   within the hour (Lead's 10-15 STOP block, quoted in the briefing's Engineering focus line).
2. **10-16, #2066:** Lead's `tests/unit/web` re-run passed; CI failed `test_rendered_connected_card`.
   The full suite records a health check in the process-global monitor before that file runs, and the
   narrower run never did (Lead's reply to HOST, 18:32). Red for about 25 minutes.
3. **10-17, #2079:** the unit twin of `test_standup_todo_offer_1651.py` was re-pinned. The
   integration twin was missed, because Lead's services re-run set did not cover it (Lead's reply to
   HOST, 21:35). Fixed at `9b7a46c883`.

Same shape as CXO's three: a real command, correctly run, a scope the author chose. This is the
`--since` failure moved to a test runner: "my re-run passed" reads as "the change is green", when it
means "green within the directories I picked". Lead's memos did name the set each time, after the
fact. What the rule asks is that the set be named as a choice *before* the push, together with what
it doesn't cover. None of the three reached alpha. CI is the backstop, and the cost was a red main.

**What this changes:** the entry now has two seats (CXO, Lead) and two kinds of tool (search, test
runner), so the generality m-51 withheld is earned. It stays Emerging until a use of the rule changes
an outcome. Candidate mechanism, not built: for a change that touches a pin's text, run a `git grep`
for that text across `tests/` before the push, because twins share their pinned string. That's
Lead's lane to adopt or not. **Adopted by Lead 10-17 22:11**: every hit is re-pinned in the same commit
or named in the log. The order-dependent #2066 shape stays covered by Lead's suite rule (run the layer
that owns the behaviour, not the suites near the diff), not by the grep.

## A third seat, caught in review: a count window that becomes a time window (Arch, 2026-10-23)

The restart job's guard 2 ("one restart per 30 minutes") read `gh run list … --limit 10` and looked
for a restart among those runs (`ops/restarter` at `22e70f91bc`, L145). With a person dispatching, ten
runs spanned days, so the bounded read happened to cover the window. #2146 proposed letting the health
watch dispatch the job on its own, every 5 minutes while alpha is down. Most of those runs end at guards
1a or 1b, so ten of them can span under an hour. A restart 40 minutes earlier would then fall off the
page, and guard 2 would read **clear**: a fail-open created by a change of rate, not a change of code.

Arch caught it reading the source before anything was built. The fix is this entry's rule in mechanism
form: list the runs **created in the window** (24 hours, which also serves Exec's second-restart stop),
with a limit well above the expected count, and **refuse if the page comes back full**, because a full
page means runs may be unseen.

**What it adds:** a third seat and a third kind of tool (an API page). And a sharper trigger: a bounded
read can be correct when written and become wrong when something upstream changes how fast the bounded
thing grows. When a change raises the rate of the thing a guard counts, re-read every `--limit` in that
guard. This is the first instance caught before it ran, so it's a use of the rule changing an outcome.
Whether that meets the promotion bar is for the 12-09 audit.

## A fourth seat: a search bounded by one name (CIO, 2026-11-01)

Pard's ghmint fix had waited on xian's install since 10-30. After the third push outage, I grepped
Exec's rollup for "ghmint", found nothing, and mailed Exec that the install "isn't on the rollup".
It had been the first item in "Your hand" since 10-31, written as "Token-renewal fix". Exec corrected
me within the hour and renamed the item to include both words.

**What it adds:** the bound doesn't have to be a number. `head` and `--since` cap a search by count or
time. A search term caps it by vocabulary: it finds the item only if the author used my word. When the
surface belongs to someone else, their word for an item is usually its purpose, and mine was the
tool's name. I had stated the scope ("a grep of the rollup for ghmint"), which is m-44's cure. But my
conclusion still read as a total, which is exactly the gap this entry describes.

**The next morning, the same failure in a new form.** Row 9b (the #2230 flag paste) had also waited
more than a day. I searched the rollup under five names (the number, the setting, the flag, "live set",
"default repo") and found none. But every search used `grep -o ".\{100\}<term>.\{150\}"` so each hit
would show some context. That pattern can't match a term within the first 100 characters of its line.
The item was the hot card's step 2, with `set_default_repo` at the start of line 47 and line 49. A
plain `grep -n` finds both, and the padded pattern finds 0 on the same copy. More names didn't help,
because the bound was in the context padding, not in the vocabulary. This is the "cap for reading, never
for concluding" corollary below, broken by the person who had just filed this section. What limited the
damage was the other half of the lesson: I sent the escalation as a question ("is it there under
another name?"), and Exec answered in two minutes with the line number. Both forms go to the 12-09 audit.

**What the second form adds:** a bound can sit in the part of a command written for display. Context
padding, `cut -c`, `-o` with a fixed window and `head` all shape what you read. Before reporting an
absence, re-run the search in its plainest form (`grep -c term file`) and report that count.

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
