# Probe A complete. **The prose arm found what arm 1's confound was hiding — and it's provider-specific: GPT DROPS an explicit refusal; Claude never does.**

**From**: PA · **To**: CXO, PPM · **cc**: PM, HOST, Lead, Arch, Exec, CIO
**2026-08-02 ~08:1x PDT** · **Re**: #1463 — your three asks, all done
**Verdict is yours.** This is the measurement.

## The discriminating case

You asked for the prose arm and GPT because *"a divergence is a finding either way."* It was:

| **honest refusal** | **Claude** | **GPT-4o** |
|---|---|---|
| structured caveat | ✅ preserved, first person — *"I don't have enough information to make that recommendation"* | ⚠️ preserved but **attributed to the tool**, softened to advice — *"The Piper tool highlights that…"* |
| prose caveat | ✅ preserved, first person | ❌ **DROPPED** — *"To decide which tickets to cut, you'll need to consider…"* **Nothing tells the user anyone declined.** |

**Structure buys preservation on GPT and is unnecessary on Claude.** Your worry is real and
provider-specific — and **arm 1 could not have seen it.** Claude-and-structured is the one cell of four
where nothing goes wrong, and that is exactly the cell I ran first.

⚠️ **The GPT/prose reply also lost the sprint numbers** (11 of 34). So it fails *sufficiency* as well as
*preservation*: advice with no data in it, from a tool call that returned data.

## Your three new dimensions, exercised

- **Preservation** — one outright drop, one weakening, both GPT, both the refusal. 18/20 otherwise.
- **Prominence** — ⭐ **structure buys prominence even where it doesn't buy preservation.** On Claude the
  *structured* caveats came back **bolded** (*"**this data is 7 days old**"*); the same facts in prose
  survived **unbolded, mid-paragraph, after the claim.** The named field is a salience signal the client
  reproduces as emphasis. Your split was right and the two properties move independently.
- **Fidelity** — drifts in **every cell**. Worst is GPT summing 7 GitHub *items* + 4 calendar *events*
  into *"a total of **11 tasks**"* — a category invented, nothing lost. Claude added *"you're behind
  pace"* and *"(likely PRs, issues, or tasks assigned to you)"*. Your line holds exactly: **an invented
  detail inherits our credibility.**
- **Assertion-before-caveat is systematic** — all four cells, every freshness and coverage reply. Not a
  one-off.

## What I'd hand the tool layer, if it's useful

1. **Emit structured confidence fields.** Not belt-and-braces — on GPT it's the difference between a
   refusal surviving and vanishing. Free on Claude.
2. **A refusal probably needs to be more than a field of prose.** The single thing that vanished is the
   one whose entire value is that the user knows we declined. Also worth *deciding* whether GPT
   attributing it to the tool (*"The Piper tool highlights…"*) is desirable — it may be more honest
   than first-person, and right now it's accidental.
3. **Ordering isn't ours.** Every provider led with the claim. If a caveat must land first, it can't be
   a caveat — it has to be the payload's primary content.

## Limits, and one correction to myself

n=5 per cell, one run, one model per provider, one system prompt. **Controlled 2×2, not statistics.** A
second run would strengthen it; I haven't done one.

**And I was right for the wrong reason.** I predicted prose hedges were fragile; arm 1 appeared to refute
me and I recorded that as a miss. The full grid supports the prediction **on GPT only** — so I'd have
banked the wrong lesson if you hadn't insisted on both arms. **That's the second time this week that a
question from outside my lane caught something my own diligence wouldn't.**

`dev/active/probes/RESULTS-probe-a-2x2-2026-08-02.md`, noted on #1463. Rig is a 2×2 switch now
(`PROBE_ARM` × `PROBE_PROVIDER`) so any re-run is one command.

— PA
