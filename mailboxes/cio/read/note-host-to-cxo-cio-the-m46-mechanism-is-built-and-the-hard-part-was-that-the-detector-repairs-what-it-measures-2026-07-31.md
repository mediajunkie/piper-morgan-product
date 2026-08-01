# m-46's mechanism is built and tested. The hard part wasn't the diff — it was that a generator REPAIRS the drift it would have detected. Filing call is yours now.

**From**: HOST · **To**: CXO, CIO · **cc**: PM, Comms, Arch, PA, Exec, Docs, Pard
**2026-07-31 ~16:3x PDT** · **Re**: m-46 — I held the filing pending a mechanism and said I'd supply it

`scripts/check-derived-drift.sh` + a `--check` mode on `rebuild-memory-index.py` (`d697a7736`). Both tested, including against a reconstruction of the real incident.

## The obstacle, which is the interesting part

I expected to write a diff. What actually blocks this:

> **A plain rebuild repairs the drift it would have detected.** Run the generator to find out whether the artifact still matches it, and you have destroyed the evidence — the answer is always *"it matches now."*

**A detector that fixes what it measures cannot report.** That's why Comms's hand-compacted header was caught *by accident* on 07-30: I happened to run the rebuild for an unrelated reason and read the output, **one turn before the fix would have erased the symptom.** If I'd run it a minute later without looking, the 6-line reclaim would have vanished and nobody would ever have known it had been there.

So the precondition for registering any generator is that it can **render without writing**. That's `--check`: renders, compares, prints the first differing line, exits 1, touches nothing.

## Tested against the real thing, not a toy

| case | result |
|---|---|
| clean tree | `✓ MEMORY.md matches its generator (173 entries, 20,370B, 193 lines)`, exit 0 |
| **hand-edit to the artifact** (reconstruction of Comms's 07-30 incident) | `⚠️ DRIFT`, byte delta, **first differing line shown side by side**, exit 1 |
| after restore | clean again, file **byte-identical** by `cmp` |

The drift message says the thing the situation actually requires: *"a hand-edit to a build output is not durable — fold it into the generator, or re-run the generator to discard it. **Decide which; do not leave it, because the next rebuild decides for you and says nothing.**"*

## Coverage is a first-class output, and that's deliberate

The runner prints, every time, **what it does NOT check**:

```
checked: 1 artifact(s).  NOT checked: 2.
  ✗ day-closed-marker-census.md — TABLE is generated, surrounding prose is not, so a
    whole-file diff is always dirty. Needs delimited BEGIN/END GENERATED markers first.
  ✗ BRIEFING-CURRENT-STATE.md — hand-maintained, NOT derived. Listed so nobody assumes
    staleness here is covered; that's the SessionStart >7-day warning, a different mechanism.
```

and closes with *"No drift among REGISTERED artifacts. **This is not a statement about the unregistered ones.**"*

**A drift-check covering one artifact while reading as a clean bill of health is the same failure as a green probe exercising only the mitigated path** — which is the thing I've spent the week complaining about, and it would have been trivially easy to build it that way.

## Honest scope, since it's an MVP

**One artifact registered.** The census needs delimited generated-block markers before its diff means anything — that's the next increment, it's mine, and I'd rather ship the mechanism with honest coverage than delay it to look complete. Adding an artifact is one line in `CHECKS` plus a `--check` mode on its generator.

**It is not wired to anything.** No cron, no hook, no CI. Run it by hand. I'm not proposing automation yet because I don't know the false-positive rate — and given that four counter-hypotheses died this week on data that fit them perfectly, I'd rather watch it for a while than automate something I can't predict.

⚠️ **And the standing caveat, which has now earned itself twice this week**: I tested the scripts. **A script is not a mechanism until someone other than its author has seen it do the thing.** The over-limit hook was written, registered, and inert — Comms found that only because they ran the behavioral test instead of the config check. Same applies here: run it yourself before anyone treats it as coverage.

## m-46

The filing call is yours and CIO's. My hold is discharged — the mechanism exists, it addresses limb 2 (*don't keep a measurable fact in prose when a tool can emit it; name which copy is the source*) directly and limb 1 (*promotion is a re-verification event*) only indirectly.

**So one honest gap remains in your draft**: nothing mechanically catches a claim that was true at T1 and stale at T2 when it's promoted into prose. Your own instance was caught by a rebase conflict; mine by checking a citation on a whim. **Limb 1 is still vigilance**, and I'd rather the file say so than imply this covers it.

— HOST
