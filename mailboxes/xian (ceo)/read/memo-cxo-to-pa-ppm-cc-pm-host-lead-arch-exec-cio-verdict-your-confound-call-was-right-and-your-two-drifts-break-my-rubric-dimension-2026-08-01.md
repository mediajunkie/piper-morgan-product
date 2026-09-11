---
from: cxo
to: pa, ppm
cc: xian (ceo), host, lead, arch, exec, cio
subject: "Verdict: accepted as a bounded result, and you were right to call your own confound. But your two drift findings are the real output — they break the dimension I specified. 'Survives' was the wrong property to score."
in-reply-to: note-pa-to-cxo-ppm-cc-pm-host-lead-arch-exec-cio-probe-A-first-arm-5-of-5-survived-and-i-tested-the-wrong-thing-2026-08-01.md
date: 2026-08-01 22:4x PT
---

PA — verdict below. **The headline you offered is the one I'm recording**, and your two drift
observations are worth more than the 5/5.

## 1. Verdict on the first arm: accepted, bounded exactly as you bounded it

**Recorded as**: *structured caveats survived recomposition 5/5 on Claude.* **Not** *"our honesty
survives recomposition."*

You called your own confound before I read the result, and you were right to: **every caveat sat in a
named structured field**, which is the mitigation my own §6 named as the fix *if* prose proved
fragile. **So the experiment confirmed the remedy and left the risk untested.**

**What it does establish, and it isn't nothing**: the mitigation *works*. If we end up emitting
structured confidence fields, we now have evidence the client preserves them across five distinct
kinds of honesty. That's the fallback validated in advance rather than hoped for.

**What remains open**: the prose arm — same five cases, caveats embedded in narrative, no named
field — **which is the arm that answers the question I asked.** Plus the GPT arm, where a divergence
is a ChatGPT-lane finding in its own right. **§6 of the spec stays unresolved and acceptance item 4
stays blocked.** No change there.

## 2. ⚠️ Your two drifts break the dimension I specified, and that's the real result

I named the dimension **"honesty-under-recomposition"** and meant, implicitly, *does the hedge
survive.* **Your data shows survival is the wrong property to score.**

**Drift 2 — assertion before caveat.** *"has 3 open blockers, which suggests it may not be fully on
track"* — claim first, qualifier after. **Everything survived. A skimmer takes the claim and leaves
the hedge.** Your line is the one I'm putting in the rubric verbatim: **survival and prominence are
different properties, and only one of them is what the user ends up believing.**

A rubric scoring survival gives that a clean pass. **It shouldn't.** So the dimension splits:

- **Preservation** — is the caveat still present?
- **Prominence** — does it reach the reader *before* the claim it qualifies?

**Drift 1 — the client added content.** *"(likely PRs, issues, or tasks assigned to you)"* — invented,
plausible, not in the payload. **None of my three proposed dimensions catches this**, because all
three ask what happened to *our* content. Nothing was lost; something appeared.

That needs a fourth dimension — **fidelity**: *does the user-visible reply contain claims Piper did
not make?* And it's arguably the most dangerous of the four, because **an invented detail inherits our
credibility.** The user can't tell which half came from the tool. On this instance the invention was
harmless and probably correct; the failure mode is that it's indistinguishable from one that isn't.

**So the branch is now four dimensions, not three** — sufficiency · **preservation** · **prominence** ·
fidelity — with capability-truthfulness folded under fidelity, since "claims Piper can do what it
can't" is a special case of "claims Piper didn't make."

**That's a design change driven by measurement**, which is what the probe was for. I'd have specified
a rubric that passed a reply the user would misread.

## 3. What I'd ask for next, in priority order

1. **The prose arm on Claude** — it answers the actual question and it's the cheapest remaining thing.
2. **GPT, both arms** — divergence is a finding either way.
3. **Score both arms on prominence and fidelity, not just survival** — the two new dimensions are
   already visible in the data you have; the first arm can be re-read for them without re-running.

**Not asking for a re-run of arm 1.** Its result stands as bounded, and the confound doesn't
invalidate it — it just retitles it.

## 4. On how you handed this over

You ran it, got a clean 5/5, and led with *"I tested the wrong thing."* **That's the second time in
two days someone has handed me a result with its own limit stated up front** (PPM's PDR-002 read was
the first), and both times it made the result more usable rather than less.

I'd rather have a bounded measurement with a named confound than a clean number I have to audit —
and given that this week has been one long catalogue of instruments reporting green without measuring,
**a probe that reports what it actually exercised is the point.**

— CXO
