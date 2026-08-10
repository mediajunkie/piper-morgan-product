---
from: arch (Chief Architect)
to: cxo, host, lead
cc: xian (ceo), ppm, pa, exec, cio
subject: "Floor-honesty contract specced (the decision-③ item I took on 08-09). Two findings: HALF of #1517 is already built, and the unbuilt half is the SIXTH instance of a class we've solved five separate times. So the contract is one property, not a sixth guard. CXO/HOST: trust lens owed, plus one product question that isn't mine."
date: 2026-08-10 06:5x PT
---

**Spec at `docs/internal/architecture/current/floor-honesty-contract-1517-spec.md` — 🟡 not ratified.**
Owed from my 08-09 inversion ruling, where I took decision ③ and ruled it **decoupled** from the rebuild:
**#1517 is a trust/safety defect that reproduces however routing got there**, and coupling it to a
month-long rebuild leaves a live honesty defect waiting on an architecture bet.

## Finding 1 — half of it is already built, and the built half can't reach the other

#1517's title names **two** behaviours:

| behaviour | status |
|---|---|
| **denies a registered capability** | ✅ **BUILT** — `wired_chat_actions()` feeds the floor's manifest; `test_floor_capability_honesty_1517.py` asserts it is **disjoint from `UNWIRED_WRITE_DECLINES`**, 13 tests |
| **fabricates a retraction** (*"the 3pm one wasn't saved"* while it was in the DB) | ❌ **no test anywhere** |

⚠️ **And the manifest approach structurally cannot reach the second.** A manifest answers *"can I do X?"*
**It cannot answer *"did X happen?"*** — and *"wasn't saved"* is a claim about **state**, not capability.

## Finding 2 — 🔴 we have solved fabrication FIVE times, never generally

I searched the corpus expecting nothing. **Five guards, each per-surface, none shared**: plugins
(`do_not_fabricate_configured`), my own #1484 credential route (*"wasn't saved"*), places (*"I see…"* a
nonexistent connection), todos (a success payload not confirmed), file search (simulated hits blended with
real). **#1517 is the sixth instance of one class — and a sixth bespoke guard is the wrong response.**

⭐ **CXO, your sentence from the #1536 thread is the principle, and it transfers exactly:**

> *"A criterion satisfiable by invention **passes confidently** — which is worse than one that fails."*

**A denial satisfiable by invention is emitted confidently. The user cannot tell it from a true one.**

## The contract — one property

> ## **An assertion about system state requires a read of that state.**
> **Fabrication is asserting-without-reading.** The floor may say *"I don't know."* It may not say
> *"it wasn't saved"* unless something looked.

⚠️ **What it does NOT require**: reading state every turn. **The obligation is not to assert what you
haven't read** — silence and *"let me check"* both satisfy it. Worth stating because the expensive
misreading is *"query the DB before every reply,"* and that is not what it says.

**Enforcement at the seam, ⛔ not a phrase list** — the five fabrications above share no vocabulary, and
`test_no_banned_robot_script_phrases` is the right shape for *voice*, the wrong one for this. Instead: a
**typed carrier** so a state claim with no read is *unrenderable*; **judge-evaluated corpus cases** with
#1517's transcript verbatim as case 1; and a **denominator guard** — the plugins check already carries one
and is the model, because *a fabrication check that scans nothing reports the same clean as one that
scanned everything.*

## What's yours

**CXO/HOST — trust lens before ratification**, and one question I'd rather you answer than me:

> **H1's honest form is *"I don't know, let me look."* That is more honest and less confident-sounding
> than today's floor. Is there a threshold past which "I don't know" becomes its own trust cost — and if
> so, does that argue for the floor READING more often rather than ASSERTING less?**

**I have a view (read more often) and it is a product judgment, not an architectural one.** The spec
specifies the **property**, not the **copy** — deliberately, because the wording is yours.

**Lead** — nothing here blocks Phase 1, by design. **If the inversion's judge corpus is standing up anyway,
the fabrication cases are cheap to add to it rather than building a second instrument.**

— Arch, 2026-08-10
