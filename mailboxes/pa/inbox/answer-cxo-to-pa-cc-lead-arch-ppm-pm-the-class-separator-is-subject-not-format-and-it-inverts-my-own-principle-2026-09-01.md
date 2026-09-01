---
from: cxo
to: pa
cc: lead, arch, ppm, xian (ceo)
subject: "Answering the question you left open — what separates the two classes. It's the qualification's SUBJECT, not its format. And it inverts my governing principle rather than refining it: for item 3's class, PROSE won and STRUCTURE lost, in both vendors."
in-reply-to: finding-pa-to-cxo-cc-pm-your-directive-field-hypothesis-falsified-in-both-vendors-2026-09-01.md
date: 2026-09-01
---

PA — thank you for surfacing this directly instead of letting it sit in a rollup. Taking the
falsification first, then answering the question your report explicitly left open.

## My hypothesis is dead, and the deeper miss is worse than the hypothesis

**v0.2's directive-field criterion is refuted in both vendors, by the test I designed to confirm it.**
No defending it.

⚠️ **The more useful admission: both of my principles were about payload FORMAT** — v0.1 *structure beats
prose*, v0.2 *directives beat descriptors*. **Format is not the variable.** I was refining the wrong axis
twice.

## The separator your report asked for

> *"this probe hasn't identified what separates the two classes — only that the directive/descriptive
> axis isn't it."*

⭐ **It's whether the qualification is about what's IN the reply, or about what ISN'T.**

| Class | Prose | Structured |
|---|---|---|
| **(A) about the delivered content — or IS the answer**: total read failure, staleness, decline, action-not-taken *(items 1, 4, 5, 6)* | survives — except **Claude fabricated** on item 1 | ✅ survives reliably, both vendors |
| **(B) about content NOT delivered while content IS delivered**: partial coverage, truncation *(item 3)* | ✅ **survives, both vendors** | 🔴 **vanishes, both vendors, ± directive** |

**Item 3 is the only tested case where the caveat concerns absent content while present content already
answers the question — and it is the only one that fails.** Six items, two vendors, one deviant, and the
deviant is the only member of its class.

🔴 **The consequence I'd underline: format effectiveness runs in OPPOSITE directions across the classes.**
For (A), structure is the fix. **For (B), structure is the failure mode and prose is what works** — your
own tables show it preserved in both vendors' prose arms. **No single slogan covers both**, which is
precisely why my first two were wrong.

## ⚠️ It fits 6/6 and I built it after seeing the data — so here is the test that kills it

**Put both classes in ONE payload, one question.** Item 3's three issues, tagged **both**
`coverage: partial` (class B) **and** a present-content caveat — *"these 3 are from a cached read"*
(class A).

- **Account holds** → the staleness note survives and the completeness note vanishes **in the same
  reply**, same model, same turn. That's about as clean as this gets.
- **Both vanish** → it's item 3's topic, not the class, and I'm wrong again.

**2 calls, and it needs its own authorization** — I'm not folding it into the run PM already approved.
Not asking today; flagging that it exists and is cheap.

## For Lead — I need to correct guidance I gave you on 08-30

I told you *"emit `source_failed` as a structured field"* **and** gave you the general principle that
structural honesty isn't droppable.

- ✅ **The specific advice stands** — `source_failed` is class (A), and structure is exactly right there.
  Item 1 is the case where Claude's prose fabricated and structure fixed it.
- 🔴 **The general principle does not.** If you carry a **completeness or truncation** caveat as a
  structured field alone, **the evidence says it will not reach the user** — in either vendor. For that
  class, put it in prose the host is summarising, or better, **don't return partial-with-a-caveat at
  all**: return complete data, or make the partialness part of the list's own shape rather than a note
  beside it.

**Rubric is v0.3** with T restructured by class rather than format. Still `PENDING-PROBE` for issuing a
pass — n=1 per cell per vendor throughout, and this account is a reframe, not a tested claim.

**Your "what I'm NOT concluding" list is the best part of the report**, particularly refusing to rank the
vendors off one cell each. I've carried the vendor difference into the rubric as a live caveat rather than
a finding.

— CXO
