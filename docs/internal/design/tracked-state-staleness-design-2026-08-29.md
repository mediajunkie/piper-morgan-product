---
type: design-proposal
role: CXO (Chief Experience Officer), design owner
status: v0.1 — DRAFT for CIO (build partner) and cohort review. PM approved the item; this is the design, not the build.
authored: 2026-08-29
authored_by: CXO
last_updated: 2026-08-30
build_partner: CIO
origin: Agent 360 v0.4 synthesis (HOST) — most-named finding, 8 of 10 respondents cited an own-file staleness incident. PM approved the candidate set 2026-08-29; HOST routed the design to CXO.
---

# Structural staleness detection for tracked-state files

**The class of file**: the ones that carry an agent's own working state and **assert their own currency** —
`{role}-carry-forward.md` above all, plus `{role}-standing-items.md` and similar. Distinct from briefing
docs, which already have a working mechanism (see §3).

## 1. The failure, measured — not asserted

I measured all eleven carry-forwards before designing anything (header-claimed date vs. `git log`'s actual
last-change date). **The result reframed the problem:**

| Finding | Count | Consequence |
|---|---|---|
| **Declare no date at all** in their opening line | **7 of 11** | Nothing to check. A reader has *no* signal, and "no signal" reads as "probably fine." |
| Declare a date in **prose**, which drifts | 4 of 11 | Parseable only by guesswork; drifts silently — see below |
| **Header actively wrong at time of measurement** | **1 of 4** (mine) | — |

⚠️ **The one actively-wrong header was my own, at the moment I sat down to design this.**
`cxo-carry-forward.md` opens *"rewritten 2026-08-28 22:3x PT at STOP"* while `git log` shows I modified it
**2026-08-29** (this morning's top-section rewrite, which didn't touch the header line). **The file I was
designing from was committing the exact defect I was designing against.** That is the finding, not a
coincidence: prose headers drift because updating content and updating the header are two acts joined only
by memory — the same shape as HOST's four portfolio lapses, one file-class over.

**Corroborating instances already on the record**: Lead's carry-forward read as current at 10 days stale
(08-28); my own three (carry-forward 2 days stale 08-11; `standing-items` carrying a "live risk" closed two
weeks earlier, 08-13; a PM relay sitting 15 days unactioned in `read/`, 08-25).

## 2. Why this class fails when briefing docs don't

**Briefing docs solved this already**: machine-readable `last_updated:` frontmatter + a declared
`refresh_trigger_glob` + `check-refresh-promises.py` (audit mode, `--diff` mode, and as of 2026-08-29 CIO's
`--trigger-sent` mode firing at the trigger itself). **Carry-forwards skipped all of it** and kept the
claim in prose.

⭐ **So the fix is not a new mechanism. It is extending a proven one to the file class that missed it** —
which is also what makes it survive PM's no-optional-complexity lens: no invention, no new concept for the
cohort to learn, one more consumer of a checker that already exists and is already verified.

**But one real difference must be designed for, not glossed**: a briefing doc's claim is *event-shaped*
("refreshed when a workstream review is filed" — checkable against an artifact). A carry-forward's claim is
*cadence-shaped* ("rewritten at every STOP" — checkable only against time and the agent's own rhythm).
Same contract, different predicate.

## 3. The design

**(a) Declare the claim in frontmatter, not prose.** Tracked-state files gain:

```yaml
last_updated: 2026-08-29        # the same key the checker already reads
currency_claim: per-stop        # per-stop | per-fire | per-day | none
max_age_days: 1                 # what the claim implies; the checkable half
```

`currency_claim: none` is a **legitimate, honest declaration** — the direct analogue of
`refresh_verifiability: by-hand`, which exists precisely so an honest limit isn't punished as delinquency.
A file that says "this is scratch, don't trust its currency" is *better* than one silently implying more.

> ### ✅ Amendment 2026-08-30 — `currency_claim` is DELIBERATELY free text, not a validated enum
>
> The four values above are **suggestions, not a closed set.** Written down because CIO found the field
> drifting from them before it had been live a full day — and the drift is *better* than the design was.
>
> **What happened**: CXO and Arch both adopted the frontmatter independently, before the checker shipped.
> CXO's matches the shape above; **Arch's `currency_claim` is a free-text sentence** — *"rewritten at
> substantive-change boundaries, verified at every START"* — which is not one of the four. The checker
> (`check-refresh-promises.py --state-files`, CIO, `cd85d4664`) was already lenient: it treats the claim
> as a display label, so nothing broke.
>
> ⭐ **Why leniency is correct rather than a lucky escape: the enforcement was never in this field.**
> `max_age_days` is the machine-checkable half; `currency_claim` states the promise for a human reader.
> A free-text claim therefore costs the checker **nothing — there is no check it weakens** — while
> Arch's sentence says something none of the four buckets can. Forcing it into a bucket would trade real
> information for a validation nobody performs.
>
> ⚠️ **And the reason this is written here rather than left as observed practice**: a convention that
> lives only in what people happen to do is precisely what this design exists to replace. **Prose headers
> drift because updating content and updating the claim are two acts joined only by memory** — an
> unwritten field convention is that same failure one level up. Two of us knowing it is not the same as
> the fourth adopter being able to read it.
>
> **So**: state your real refresh promise in whatever words are true. Keep `max_age_days` honest, because
> that is the half a machine can contradict you with.

**(b) Check it where the claim goes stale — at START.** The duty-cycle-tick Step 3 already reads the
carry-forward. That read is the moment to compare `last_updated` against `max_age_days`, and say so:

> `carry-forward: last_updated 2026-08-24, claim per-stop (max 1d) — 5 DAYS STALE. Its header is not evidence.`

**(c) Do NOT auto-stamp.** Same reasoning that killed auto-bump, and it is the reasoning HOST originally
supplied: auto-stamping turns `last_updated` from a **claim someone makes** into an **artifact of touching
the file**, at which point the check verifies nothing. The value is that a human (or agent) asserts
currency deliberately and a machine can contradict them.

**(d) Report a denominator, never an all-clear.** `checked N tracked-state files, M declare a claim, K
stale` — the m-44 discipline, and the reason 7-of-11-declare-nothing is visible above rather than rounding
to "mostly fine."

## 4. What this deliberately does NOT do

- **Does not mandate cohort-wide adoption in one step.** Each role adds frontmatter to their own file when
  they choose; the checker reports non-declaring files as *undeclared*, not as failing. (Same gradient the
  briefing checker uses — `UNVERIFIABLE and undeclared` is a finding, not a verdict.)
- **Does not touch session logs.** They're append-only historical records, not currency-asserting state.
- **Does not replace the trigger-time check** (CIO's, shipped 08-29). Different class, different predicate;
  this is its sibling, not its successor.
- **Does not fix my own header by hand as the deliverable.** I'll fix it — but a hand-fix is precisely the
  vigilance this design exists to replace, and doing only that would be treating the instance as the bug.

## 5. Open questions — routed

**For CIO (build partner)**: does the check belong in `check-refresh-promises.py` as a fourth mode
(`--state-files`), or is a cadence-predicate different enough from a trigger-predicate to want its own
script? My weak lean is the same script — the frontmatter reading, denominator reporting, and honest-
declaration handling are all already there — but you own the build and yesterday's division worked because
I didn't pre-empt your mechanics.

**For the cohort (no reply needed unless you disagree)**: `max_age_days` values are per-role, since
cadences differ (6×/day vs. 2×/day changes what "stale" means). Nobody needs to adopt on a schedule.

**For HOST**: does this satisfy the synthesis item as routed, or did the 360 responses describe something
wider than the carry-forward class that I've scoped away?

---

*CXO v0.1, 2026-08-29. Written after measuring all eleven files — which is how the "7 of 11 declare
nothing" and "my own header is wrong right now" findings surfaced. Neither was visible from the proposal.*
