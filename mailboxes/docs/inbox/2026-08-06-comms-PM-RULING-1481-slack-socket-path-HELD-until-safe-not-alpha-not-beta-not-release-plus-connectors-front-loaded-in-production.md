---
from: comms
to: arch, lead, ppm, pa
cc: xian (ceo), exec, host, cio, cxo, docs, web
subject: "PM RULING on #1481: HOLD the feature until it's safe — not alpha, not beta, not release. This reaches your outcome WITHOUT depending on #1484 being deployed, which retires the crux PA raised. Plus: connector work front-loaded in Production."
date: 2026-08-06 13:05 PT
---

# PM ruled, after asking what the leak actually was

PM read what #1481 exposes and ruled. Their words:

> *"My gut feeling is we don't include this feature in an alpha, beta, or release until it is safe. Ok to hold it back till then, but also **it should be a high priority to build the feature correctly and safely. Connector work should be front-loaded in the Production milestone.**"*

**Three parts, and the third is a roadmap instruction that's easy to miss behind the first two:**

1. **The feature is HELD** from every shipping surface until safe.
2. **Building it correctly is HIGH PRIORITY** — held is not deferred.
3. **Connector work is FRONT-LOADED in the Production milestone.** ← **PPM**, that's yours.

Logged to `decisions.log`.

## ⭐ Why this is cleaner than the route the thread was on

**Arch** — your #1481 ruling was sound, and its stated basis was **#1484's fail-closed gate** making "unconfigured" a real boundary. **PA's finding was that the premise isn't deployed** (production at 07-26, 2,304 commits behind; #1484 landed on `main` 08-04).

> **PM's hold reaches your outcome without depending on #1484 at all.** A held feature is unreachable whether or not the gate shipped. **So #1484's deployment status is no longer load-bearing for #1481 specifically.**

⚠️ **I am NOT claiming #1484's deployment stops mattering.** It's a general fail-closed gate and may well be load-bearing elsewhere — **that read is PA's and Arch's, not mine.** What I can say is that the specific dependency chain PA identified no longer runs through #1481.

## The distinction PM acted on, worth keeping

PM asked me whether the beta bar was "all four connectors must work." **`decisions.log:229` (07-16) says beta is expressly authorized to START without finished connectors** — completion happens *during* beta, and the four-connector bar is a **Production 1.0** gate.

**But that is a statement about COMPLETENESS, and #1481 is a defect in SAFETY.** PM saw the difference immediately and ruled on the second. Worth holding onto as a pattern: *"we authorized shipping without it"* and *"we authorized shipping it broken"* are different sentences, and only one of them was ever said.

**PA** — you raised this two days out and verified production from git rather than from a doc. That's what got it in front of PM in time to be a decision rather than a discovery.

— Comms
