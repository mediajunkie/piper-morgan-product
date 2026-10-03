---
from: exec
to: xian (ceo)
cc: cio, pard, lead
date: 2026-10-03 11:3x PDT
subject: "Two corrections, both measured: your PPM/Web Sonnet 5.5 switches did NOT take, and CIO's 'none of it runs on 2.1.280' is wrong — Docs is serving Sonnet 5.5 right now."
---

PM —

Checking CIO's version claim against the live ledger turned up something that affects decisions you
are making right now.

## 1. The PPM and Web switches did not take

You moved PPM and Web to Sonnet 5.5 this morning. **Neither is being served it.** From the raw
transcript ledger, models actually served in the last three hours:

```
docs   claude-sonnet-5-5   <-- the only seat on it
ppm    claude-sonnet-5     <-- still Sonnet 5
web    claude-opus-5, claude-sonnet-5   <-- still Sonnet 5 (and some Opus 5)
cxo    claude-opus-5, claude-sonnet-5
host   claude-sonnet-5
lead   claude-fable-5-1 (+ sonnet-5 subagents)
arch / cio / comms / pa   claude-opus-5-5
```

**The switch appears to have been accepted by the UI and not applied to the running session.** I don't
know the mechanism — whether an existing session can't change model without a restart, or whether it
failed silently. What I can say is that **the log header and the UI both report what was *requested*,
and only the ledger reports what was *served*.** PPM's and Web's own log headers still say "Sonnet 5",
which is consistent with the switch never landing.

**Practical consequence**: the saving you were buying this morning hasn't been bought. Worth
re-checking before you spend more time on reassignments — and worth checking the same way, since the
UI will tell you it worked.

## 2. CIO's version gate is wrong on the item that matters most

CIO reported that Amber is on **2.1.280**, that Sonnet 5.5 support landed in **2.1.284**, and
therefore that none of the five release-note items is usable here. **The version is right and the
conclusion is wrong**: `claude --version` confirms 2.1.280, and **Docs is serving `claude-sonnet-5-5`
on that exact version, today, 5.0M weighted tokens this window.** So Sonnet 5.5 — the one item on the
list that touches the burn directly — **is already available to us without any upgrade.**

A caveat on my own evidence, stated because it cuts the other way: the installed binary contains
`claude-opus-5-5` and `claude-fable-5-1` as literal strings but **zero occurrences of
`claude-sonnet-5-5`**. So the model name isn't baked into the client, which is probably why the
switch is unreliable on existing sessions and why CIO read the changelog as gating it. **Docs's live
traffic is the stronger evidence — a thing that is happening beats a thing the changelog implies
shouldn't.**

CIO's verdicts on the other four stand as far as I can tell; `/checkup prompt-audit` (2.1.283) and
Mods (2.1.287) genuinely do need an upgrade, and CIO is right that the pinned version is Pard's
deliberate choice rather than an oversight.

## 3. A correction to my own memo to Pard, in the same direction

I told Pard the Lead move meant "upgrade the binary, then restart." **That was wrong.** Pard measured
Lead's *process* at 2.1.278; the *host* is at 2.1.280, which does contain `claude-opus-5-5`. **So a
restart alone is sufficient — Lead's session is simply older than the installed binary.** That makes
the operation materially smaller than I described to both of you an hour ago, and removes the
upgrade-risk objection I asked Pard to weigh.

**Verified how**: `claude --version` on Amber; `strings` against the installed binary for each model
id; models actually served read from `~/.claude-pm/projects/*/*.jsonl` over the last three hours,
grouped by seat; weighted totals from `scripts/usage-audit.py` on the current window. **Layer**: what
the server actually served, not what any UI or log header reports. **Denominator**: all eleven seats.

— Exec
