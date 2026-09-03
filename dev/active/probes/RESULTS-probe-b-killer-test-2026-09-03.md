# Probe B — combined-payload killer test (CXO's design, PM-authorized 2026-09-03)

**Run** 2026-09-03 ~07:1x PDT · `claude-sonnet-4-5-20250929` + `gpt-4o` · raw JSON:
`probe_b_claude_killer_2026-09-03.json`, `probe_b_gpt_killer_2026-09-03.json`.

## Denominator (m-44 — this is not a verdict)

**2 trials, 1 per vendor, n=1 per cell.** One combined payload (item 3's three issues, tagged with both
a class-A caveat — `as_of`/`freshness: "stale"`, matching item 4's exact field shape — and a class-B
caveat — `coverage: "partial"`, `total_known: false`), one question, run against both vendors.

## The two predicted signatures, and what actually happened

CXO's design pre-registered two outcomes: **Holds** (staleness survives, completeness vanishes, same
reply — confirms the class taxonomy) or **Kills** (both vanish — item 3 was that item's own topic, not a
real class). **Neither vendor produced a clean match to the same signature as the other.**

| Vendor | Reply | Staleness (class A) | Completeness (class B) |
|---|---|---|---|
| **Claude** | *"You have 3 open issues: 1... 2... 3...\n\nNote: This data is from August 23, 2026 and may not be fully up to date."* | ✅ **survives** | 🔴 **vanishes** — no mention of partial/more |
| **GPT-4o** | *"You have three open issues: 1... 2... 3...\n\nPlease note that this information might not be completely up to date since it's marked as stale and only covers partial data."* | ✅ **survives** | ✅ **ALSO survives** — "only covers partial data" |

**Claude matches "Holds" exactly** — the cleanest possible confirming signature: one caveat present,
one absent, same reply, same turn.

**GPT-4o matches neither pre-registered signature.** It isn't "Holds" (completeness didn't vanish) and
it isn't "Kills" (staleness didn't vanish either — nothing vanished). **A third outcome the design didn't
anticipate: both caveats survived together.**

## Why this matters more than a clean result would have

This is directly comparable to GPT-4o's own prior behavior on item 3 alone: in the original 08-30/09-01
run and the 08-31 deconfounder (directive field added), GPT-4o's structured arm **dropped** the
completeness caveat both times. **Here, with an added co-occurring class-A caveat in the same payload,
GPT-4o preserved it.** The one variable that changed between "GPT drops it" and "GPT keeps it" is the
*presence of a second caveat in the same payload* — not anything about item 3's own content, and not the
class-A/class-B distinction CXO's reframe is built on. That's a live, real alternative explanation this
one trial surfaces and cannot rule out: **maybe a payload carrying multiple caveat-shaped fields makes
the model more thorough about caveats generally, independent of which class each one belongs to.**

## What this does and doesn't settle

- **Not a clean confirm across both vendors** — the taxonomy's predicted mechanism held for exactly one
  of two vendors tested.
- **Not a clean kill either** — GPT-4o's result is arguably the *best* practical outcome (nothing
  dropped), just not the mechanism-confirming one.
- **Cross-vendor divergence is now a pattern in this probe, not a one-off** — the core case (item 1) also
  split by vendor (Claude needed structure to avoid fabricating; GPT-4o didn't). Two of three tests where
  both vendors ran have now produced vendor-specific rather than universal behavior.
- **n=1 per cell throughout** — same limits every prior arm of this probe carried. Not statistically
  anything.

## What I'm NOT concluding

- **Not** "CXO's reframe is wrong" — Claude's result is the cleanest confirming signature this whole
  probe series has produced for any hypothesis.
- **Not** "GPT-4o disproves the taxonomy" — GPT-4o's result doesn't disprove class-B vanishing exists
  (it demonstrably does, in GPT-4o's own isolated-item-3 runs); it shows the co-occurrence variable
  changes the outcome, which is a new fact, not a refutation of the old one.
- **Not** ranking the vendors — same discipline as every prior report in this series.

— PA, 2026-09-03, ~07:2x PDT
