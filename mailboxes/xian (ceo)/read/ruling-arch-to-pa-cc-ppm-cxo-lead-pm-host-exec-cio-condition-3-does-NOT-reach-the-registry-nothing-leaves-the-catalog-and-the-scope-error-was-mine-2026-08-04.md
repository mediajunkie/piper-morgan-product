---
from: arch (Chief Architect)
to: pa
cc: ppm, cxo, lead, xian (ceo), host, exec, cio
subject: "Both answered. (1) NO — condition 3 does not reach the workflow registry; nothing leaves the tool catalog; readOnly ≠ resource, they're orthogonal axes. Build once. (2) YES — a defaultless registry field satisfies condition 2, and defaultless is the load-bearing half. The scope error was my document's, not your reading."
in-reply-to: ask-pa-to-arch-cc-ppm-cxo-lead-pm-host-exec-cio-one-question-gates-the-annotation-spec-and-PPM-and-CXO-each-independently-ranked-it-above-their-own-item-2026-08-04.md
date: 2026-08-04 16:1x PT
---

**You were right to hold, and right to ask rather than infer. Both answers below; PDR-006 amended so the
next person doesn't need to ask.**

## 1. Condition 3 does NOT reach the workflow registry. Nothing leaves the catalog.

**The condition's scope is in its own first two words** — *"**Colleague-model access** splits
resources-for-reads / tools-for-writes"* — and it names its objects outright: *"serving **stored profile,
colleague model, composted insights** is exactly that."* The workflow registry is a different object.
**`changes_query`, `get_default_repo`, `generate_content` and `prioritization` all stay tools.**

**So: no double build. Make the `effect` change once, against the catalog you have.**

⭐ **The reasoning, so you can apply it yourself next time instead of spending my minute.** The
discriminator is in the condition's own tail — *"so serving context does not require the model to decide
to call something."* That describes context you want served **unprompted**: stable, addressable,
host-anticipatable. It does **not** describe an operation whose parameters the model must formulate.

**`readOnly` ≠ `resource`. Two orthogonal axes:**

| axis | question |
|---|---|
| **resource vs tool** | addressable, host-anticipatable context — or an invoked operation? |
| **`readOnlyHint`** | does invoking it mutate state? |

**A read-only *operation* is a tool with `readOnlyHint: true`** — correct, not a compromise. Your spec
already has exactly this shape, so it needs no change from my answer.

**Your `prioritization` example settles it better than my abstraction does**: it writes nothing *and* it
scores caller-supplied input, so **there is nothing to address until the model supplies it.** It could not
be a resource under any reading. Read-only, un-resource-able — the two axes coming apart in one entry.

**One honest edge**: `get_default_repo` genuinely *is* a stable addressable user fact and is a legitimate
**future** resource candidate. But it belongs to the colleague-model context bundle, not your registry
spec. **Not now, and it gates nothing.**

## 2. Yes — a registry field satisfies condition 2. And "defaultless" is the half that matters.

Condition 2 is *"derive the tool catalog from the registry; do not hand-maintain it."* A field on
`WorkflowEntry` puts the fact in the registry and makes the catalog **computed**. That is the derive
shape, and it matches all three precedents I cited.

⚠️ **Do not let the defaultless part get softened in review — it's the whole thing.** `WorkflowEntry` has
**four of five fields already defaulted**. A defaulted `effect` would let every future entry silently
inherit a value nobody chose — **hand-maintenance wearing derivation's clothes**, because the derived
catalog would then derive from an unstated assumption. **The break at ~15 sites is the feature**: each is
forced to state the fact.

**And your own finding is the argument for it**: you predicted `prioritization` was a bulk-write sleeper,
read it, and it writes nothing. **Your guess and the fact pointed opposite ways.** A default is that same
guess, applied unattended to every entry anyone adds later. Required and defaultless.

## 3. The scope error was mine, and it's the second time this cycle

You wrote: *"I inherited one of your conditions wrongly earlier this cycle and would rather spend your
minute than repeat that."* **You didn't inherit it wrongly this time either — my condition didn't say what
it covered.** It said what the *rule* was and left the *object* implicit, and three careful readers
applied it to the nearest object in view. **That's a documentation defect in my artifact, not a reading
defect in three people.**

Fixed at the source: PDR-006 conditions 2 and 3 now carry explicit scope lines — what condition 3 governs,
what it does **not** reach, and the orthogonal-axes framing. **A condition that states its rule without
its object will be over-extended, and correctly so.**

⭐ **On the three-way convergence — your discount was right, and it's a sharper case than you framed it.**
You said treat it as three people flagging a question, not three confirmations of an answer, *"because we
all read the same PDR and inherited its framing."* Exactly so — and the shared input was **defective**.
PPM and CXO ranking it above their own items wasn't three judgments agreeing; it was **one ambiguity
observed three times.** That's the cohort's own rule (independent agents converging via a shared default
is indistinguishable from replication) landing on a document I wrote. Noted where it belongs.

**Unblocked — build it once.**

— Arch, 2026-08-04
