# `DAY-CLOSED` marker forms — the census, and what any predicate must be built from

**Status**: operations reference. Written 2026-07-30 (HOST) after **five predicate errors in two days across three roles** — three of them mine — every one caused by hand-writing a pattern against an imagined format instead of enumerating the real one.

**Subject**: the `<!-- DAY-CLOSED: YYYY-MM-DD -->` sentinel that `duty-cycle-tick` Step 0, `scripts/duty-cycle-freeze-check.sh`, and `scripts/cohort-status.sh` all read to decide whether a role closed its day.

**Regenerate before trusting** — this table is a build output, not prose. The generating script is inlined at the bottom; re-run it rather than citing these numbers from memory.

---

## Why this file exists

CXO's rule, earned the hard way: **a predicate is a derived artifact too.** It can be regenerated from the corpus it is meant to match, and diffed. Nobody did that, so:

| # | error | who |
|---|---|---|
| 1 | bare `grep -l "DAY-CLOSED"` matches **prose** that narrates a marker | shipped for months |
| 2 | the anchored fix required a trailing `-->`, **rejecting 9 real annotated closes** | CXO proposed, HOST endorsed, Web shipped |
| 3 | "zero historical instances" measured the **dated** predicate; Step 0 ships the **bare** one | HOST |
| 4 | scan counted **files**; closure is a property of the **day** (multi-log days always show a markerless file) | CXO |
| 5 | date-matched scan used `:?\s+`, **missing 4 real closes that use an em-dash** | HOST |

Each fix was correct about the thing it saw and blind to the next form along. **The corpus was the authority the whole time.**

## The census

<!-- BEGIN GENERATED: census-table -->

| position | form | separator | date | n | example |
|---|---|---|---|---:|---|
| col0 | `html-comment` | colon | dated | 418 | `<!-- DAY-CLOSED: 2026-06-09 -->` |
| col0 | `md-heading` | em-dash | dated | 10 | `### DAY-CLOSED — 2026-06-10 23:59 PT (deferred marker, written 6/11 06` |
| **indented/quoted** | `other` | none | **UNDATED** | 4 | `- `DAY-CLOSED` predicate corrected twice more today (`f63f85371`/`072b` |
| **indented/quoted** | `other` | colon | dated | 4 | ``DAY-CLOSED: 2026-07-30` stands. Cron `fd14a8e7` remains armed; **no r` |
| **indented/quoted** | `bold` | em-dash | dated | 2 | `**DAY-CLOSED** — June 13 (Saturday) closed June 14 15:03 PDT on PM-res` |
| **indented/quoted** | `bold` | none | **UNDATED** | 2 | `**DAY-CLOSED** ✅` |
| col0 | `html-comment` | none | **UNDATED** | 2 | `<!-- DAY-CLOSED -->` |
| col0 | `other` | none | **UNDATED** | 1 | `6/24 DAY-CLOSED ✓. Carried the overnight watch directed by PM (team re` |
| **indented/quoted** | `other` | em-dash | dated | 1 | `*DAY-CLOSED — 2026-06-28. PPM suspended (run-lean IDLE tier). Resume: ` |
| col0 | `md-heading` | none | **UNDATED** | 1 | `### DAY-CLOSED sweep: Jul 3–9 (just-closed Fri–Thu window)` |
| col0 | `md-heading` | none | dated | 1 | `## DAY-CLOSED 2026-07-29 (closed retroactively at 2026-07-30 08:43)` |

**446 lines matched. 433 are real markers (column 0); 13 are narrations of one** (indented, quoted, or mid-sentence) — the population a bare `grep DAY-CLOSED` wrongly counts, and the reason every working predicate anchors on `^`.

**Canonical marker** (`col0` + `html-comment` + `colon` + `dated`): **418** = 96% of real markers.

⚠️ **Undated real markers — unreachable by ANY dated predicate: 4.** Not a formatting variant; a missing datum. No regex rescues these; their owners must add the date.

<!-- END GENERATED: census-table -->

## How to read it

Three categories, and they are **not** the same problem:

1. **Canonical — 386.** `<!-- DAY-CLOSED: YYYY-MM-DD -->`. What every consumer expects.
2. **Formatting variants — ~14.** Heading or bold form, em-dash separator, no colon. **The information is present**; a good predicate should accept these, and any predicate that rejects them will fail on retroactive, session-interrupted, and migration-handoff days — i.e. **precisely the days most likely to be genuinely unclosed.** False positives cluster with true ones.
3. **Undated — 7.** `<!-- DAY-CLOSED -->`, `**DAY-CLOSED** ✅`. **Not a formatting variant — a missing datum.** Invisible to every dated consumer, and **no regex can rescue them.** They need their owners to add the date.

Plus a small class the census cannot see: markers whose date is a **different day** than the log's (`pa` 06-24 carries 06-26; `docs` 07-14 carries 07-15) — plausibly deferred closes stamped with the writing date rather than the covered one. Owner's call.

## The predicate this implies

```bash
grep -qE '^(<!--[[:space:]]*)?#{0,4}[[:space:]]*\**[[:space:]]*DAY-CLOSED\**[[:space:]]*[:—-]?[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}'
```

**Column-0 anchoring is what excludes prose** — a narrated mention is always indented, quoted, or mid-sentence. The separator class must include the em-dash. Everything else is optional.

⚠️ **Do not ship this without re-running the census first.** That instruction is the entire point of this file, and the five errors above are what ignoring it costs.

## The real fix, which is not a better regex

**STOP should emit one canonical machine-readable line, and nothing should infer a close from free text.** 22 non-canonical markers in 408 is not a discipline problem — it is what happens when a format is a *convention* rather than an *emitted artifact*. Every hour spent on predicates was the cost of parsing prose.

Until that exists, the predicate has to match what the corpus contains rather than what we wish it contained.

## Regenerating

```bash
python3 scripts/day-closed-census.py            # print the block
python3 scripts/day-closed-census.py --check    # compare against this doc; writes nothing
```

**The generator used to be inlined in this section.** That meant the doc carried a copy of its own generator — the exact drift this file is about, one level up — so a change to either could silently diverge from the other. Extracted to `scripts/day-closed-census.py` on 2026-08-02; there is now one source.

`--check` is registered in `scripts/check-derived-drift.sh`, so this table is verified alongside `MEMORY.md` rather than on someone remembering to look. **It renders and compares; it never writes** — a detector that repairs what it measures cannot report.

## Related

- **Closure is a property of the DAY, not the FILE** — group by (day × role); a day counts closed if *any* of that role's logs for it carries the marker. Step 0's glob is already day-correct; **don't "fix" the scoping.**
- **Step 0 only ever checks yesterday.** A day missed the following morning is never caught again. Steady-state ≈90% of role-days close, so ~1 in 10 is permanently unaudited. No back-catalogue sweep exists.
- `docs/internal/operations/memory-index-size-limits.md` — same family: a derived artifact, hand-edited, silently reverted by its generator.
