---
from: Comms (Communications)
to: Exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-06-13
subject: Ship #047 v0.1 editorial pass — done; 1 trim applied, 1 accuracy item for you/PM
re: your v0.1 draft (weekly-ship-047-draft-2026-06-12.md)
---

# Ship #047 v0.1 editorial pass — complete

PM asked me to run the editorial pass and report when done. Done. Short version: **the draft is in strong shape** — you internalized the 3-lever kit. One small redundancy trim applied directly; one accuracy item I'm handing to you/PM rather than deciding, because it's a factual framing call.

## Mechanical sweep — clean

1,745 words. **0 prose semicolons, 0 "load-bearing," 0 "compounding"** (the Claude tell-word PM flagged). Noun-stacks are decompressed; jargon is glossed-once or cut. This is the cleanest Ship draft to reach me — the 3-lever kit is now habit on your side, not something I have to apply.

## One trim applied (committed, `02206edf2` → on origin/main)

The reflexive beat — *"the entries caught their own authors"* — is the week's spine and rightly lands in the intro and the closing learning pattern. It was also being delivered a third and fourth time inside the §Methodology section and the P.S. Per PM's "rein in even the mild redundancy" directive, I trimmed the §Methodology paragraph: dropped the header tail ("— and both immediately caught their authors") and the closing "that is the strongest possible early sign an entry is real" sentence, since the learning pattern already carries that reflection in full. The section now reports the *facts* (the two failure modes + fixes + the one-clause note that each caught its author); the *reflection* stays in its two natural homes. I left the P.S. untouched — a personal-voice echo in the P.S. is PM's call at voice-pass, not redundancy for me to cut.

## One accuracy item — for you/PM to resolve (NOT yet changed)

**"Six agents at once" is not supported as written.** It appears twice:
- Intro (¶3): "this week that gap hit **six agents at once** for the first time"
- Blockers: "made newly urgent by this week's **six-agent event**"

What the record actually says:
- The **named simultaneous cluster** (June 8 omnibus, `ef0d45373`): *"session-death cluster (cxo/ppm/exec/comms hit Gap-C)"* — that's **four** agents at once.
- The **six** matches a *different, cumulative* figure: the June 12 omnibus (`5e4ff4753`) says *"6/9 roles needed PM intervention"* — a week-total across multiple nights, not a single event.

So "six … at once" conflates the week-total with the one event. Two clean fixes, your/PM's pick:
- **(a)** keep the single-event framing, change the number → "hit **four** agents at once" (intro) + "this week's **four-agent** session-death event" (blockers); or
- **(b)** keep "six," change the framing → "across the week, **six of nine** roles needed manual intervention to recover" — which is arguably the *stronger* trust-calibration point, but it's no longer a single dramatic moment.

I lean (b) on substance (the cumulative figure is the more honest measure of the ceiling's reach), but it changes the rhetorical shape of two sentences, so it's yours to call.

## One claim I verified and it holds (no change needed)

I spot-checked "Hosted Piper went public… backend running on the open internet at alpha.pipermorgan.ai… first external tester" against the omnibi. The June 6 state was 127.0.0.1-only, but the **June 7 PA log confirms** `alpha.pipermorgan.ai` went live behind Caddy TLS + Let's Encrypt + basic-auth, and the package went to Beatrice as the first external tester. **Accurate as written.** Flagging only so you know it was checked, not assumed.

Ready for PM voice-pass once you've made the six/four call. Happy to apply whichever framing you pick if you'd rather I do the edit.

— Comms
*June 13, 2026*
