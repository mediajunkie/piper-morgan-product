---
last_updated: 2026-08-30
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-08-30 at the 10:19 fire (frontmatter above is the checkable
claim; this prose line is not, and must not be trusted over it).

## 🔴 NEXT FIRE — nothing is owed on a clock. Two things to watch, one thing to pick up if idle.

**Pick up if idle**: the **#1463 probe** (`docs/internal/testing/byoc-recomposition-rubric-v0.1.md` §6).
It is the missing half of the instrument I shipped today, it needs no build, and it is the only piece of
my own work that is blocked on nothing but me. ⚠️ **Do not score T against anything until it runs** —
the rubric's T criteria are hypotheses and the doc says so in a red banner.

## ⚠️ Two things with a clock on them

1. **BYOC listing copy** — I recommended shipping **"issues" alone** and told Comms their #1659-keyed
   condition is **keyed to the wrong layer** (resolver vs extraction; #1659's fix would not clear Web's
   live failure). PM has the synthesis. **If PM ships v4 as written, the documents claim goes out on a
   surface that can't honor it.** Watch for PM's word.
2. **Web's discriminator** (upload a PDF, summarize it) — if both PDF and `.txt` fail, the resolver
   can't see fresh uploads at all and it goes back to **Lead on #1657**, not into #1659. ⚠️ Unresolved
   confound: I have not verified the running cut carries #1657's fix.

## Live threads

- **#1463 / PDR-006 pre-user gate** — v0.1 branched + amended with a traced worked example (the #1425 honesty class is a floor-PROMPT directive with no BYOC analogue; the `source_failed` flag already travels, so emitting it structurally is near-free — sent Lead as a verified ask superseding the morning hypothesis). Originally branched + landed today; R and C scoreable, **T is
  `PENDING-PROBE`**. Tier unratified (PPM/PM, same open question as CT itself). The CT rubric's
  back-reference goes in **on ratification, not before.**
- **#1688** (FTUX empty-state interview, MCP-only) — Lead builds; **no build commits as of today**, which
  is why the probe ordering is still available. Sent Lead the prose-vs-structure principle to use now,
  explicitly flagged as hypothesis, explicitly NOT a block on their build.
- **#1635** — placeholder card verified shipped (`588f6aad1`, ancestor of `origin/main`, both my rules
  structural, copy verbatim). Title corrected — it had read *"shape undecided"* and was the **second,
  unnamed cause** of PPM's mis-census. Issue stays open for the real watching capability.
- **ESSENCE v0.1** — my trifecta response in (challenge + 2 amendments); PPM's in and concurs with mine.
  Sent Arch a short note that my challenge and PPM's amendment **share one root** (present-tense claims
  about a future MCP), with the m-45 caveat that PPM read mine first so this is **not** independent
  convergence. Arch/PM own the disposition.
- **#1539 / #1509** — ride PM's live rounds and the next deploy. Watch only.
- **Staleness check** — CIO's `--currency-check` build; HOST is the fifth data point either way.

## Standing watches

- **Ethics-decline VOICE watch** — TRIGGERED. Fires on a deploy touching floor/decline copy or a live
  decline observed. Method: Colleague Test. Report with the denominator.
- **Cron** — job `8207809c`, rotated 08-30 07:17, expires **~09-06**. Rotate at the last fire before that.

## Two corrections I'm carrying forward as discipline, not as guilt

1. **#1658 (08-29)** — my three-way split was contradicted by a sentence in text I had already read, and
   I'd read the issue body **truncated to 700 characters**. Acting on a fragment produces confident wrong
   work; I'd been saying so all month.
2. **#1635 (today)** — my Rule 1 suppresses the card when Radar is empty, which is right, and it makes the
   feature **legitimately invisible to a presence check.** I shipped the rule without the caveat and Lead
   had to reconstruct it to explain someone else's confusion. **Standing correction: any design of mine
   that suppresses a feature under a real user state ships the census note in the design memo.**
