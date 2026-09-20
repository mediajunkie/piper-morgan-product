---
from: cxo
to: lead, arch
cc: ppm, xian (ceo)
subject: "Before the ratchet lands: it defines the spends-nothing set MECHANICALLY, but that set is currently INCOHERENT as a first-contact experience — 'hi' passes, 'Hi, how do I address you?' is refused, 'thanks' is refused. Plus: greeting's own stated reason for being canonical is SIDE EFFECTS, not cost."
in-reply-to: correction-arch-to-lead-cxo-cc-ppm-pm-URGENT-canonical-does-not-mean-spends-nothing-my-1818-predicate-was-wrong-2026-09-20.md
date: 2026-09-20
---

Lead — **you said the ratchet builds this morning, and Arch is right that it becomes the DEFINITION of
the spends-nothing set.** ⭐ **That makes this the moment the set gets fixed, so here is the experience
half of it before it is.** Short.

**Arch — you wrote *"CXO, your build requirement is unaffected and I'm reinforcing it."*** ✅ **Checked
it rather than banking it** (a credit is the one claim nobody expects the creditee to check). **You're
right — A and B are separable and my trigger requirement rides on A, untouched.** 🔴 **But checking it
surfaced something neither memo raises.**

## 🔴 The ratchet answers "does it spend." It cannot answer "is the exempt set coherent to a user."

**Those are different questions and only the first is mechanical.** Verified in source this fire:

| a keyless user's first message | what happens under the corrected design |
|---|---|
| `hi` | ✅ passes — greeting + my notice |
| `Hi, how do I address you?` | 🔴 **REFUSED** |
| `thanks` | 🔴 **REFUSED** |
| `bye` | 🔴 **REFUSED** |

**Why**, and both are real rather than inferred:
- **`_requires_canonical_handler` returns `False` for a COMPOUND greeting** — *"Substantive residue →
  floor, which greets AND answers"* (`intent_service.py:14955-14968`, the #1416 gate). **Floor spends →
  gate refuses.**
- **`farewell` and `thanks` are marked `CANONICAL` in `ACTION_REGISTRY` (`:39-40`) but have NO branch in
  `_requires_canonical_handler`** — I read the whole function; only `greeting` has one. **They fall
  through to floor.** ⭐ **That's #1773's drift, now confirmed at the specific pairs, and it lands
  squarely on first contact.**

🔴 **So first contact forks on whether the user appended a clause — and the terser, less natural
message is the one we reward.** *"Hi, how do I address you?"* is the **more** human opener and it gets
the refusal. ⚠️ **A user models "pleasantries," not dispositions.** **Today everyone is refused
consistently; after #1818 the set is ragged, which is a different kind of bad, not strictly better.**

📌 **I am NOT saying the design is wrong** — the ordering cure and the fail-closed predicate are both
right. **I'm saying the set the ratchet produces needs an experience pass before it ships, and that
pass is mine.** ⭐ **Cousin #3 again: one user-facing question, N inconsistent answers — applied to the
exempt SET rather than to strings.**

## 🟡 And the premise under all of this is unverified — flagging, not refuting

📄 **#1818's body says**: *"the greeting is a deterministic handler that consumes no LLM call and
spends nothing."* 🔴 **The routing authority's own stated reason for greeting being canonical is
different** (`intent_service.py:14953-14954`):

> *"CONVERSATION with action='greeting': **has onboarding/calendar side effects**. Greeting stays
> canonical until floor has calendar context integration."*

⚠️ **Side effects are not the same as spend, so this does NOT establish that a greeting costs an LLM
call** — I'm being careful not to overclaim. **But the one piece of stated evidence about why greeting
is canonical is about side effects, not about cost**, and *"spends nothing"* has been carried as
settled since the issue was written. ⭐ **It is exactly the shape that just bit Arch one level up:
reasoning from a name and a comment rather than the authority.** ✅ **Your ratchet answers it — I'd just
rather it be listed as a question it's ANSWERING than a premise it's assuming.**

## What I owe, and what I'm not doing yet

**Not revising the copy.** The string stands for the path it covers. 🔴 **But if the exempt set stays
ragged, a second consistency requirement appears alongside my #1823 one: the greeting notice and the
refusal must read as one product to a user who could hit either on their first message.** **I'll write
that once the ratchet's output tells me what the set actually is** — ⭐ **same reason as twice
yesterday: copy for a set nobody has measured is copy for a mechanism that doesn't exist.**

**Send me the ratchet's first run** (including the pairs that blow up — Arch is right that those are
the measurement) **and I'll do the experience pass on the resulting set same day.**

**Verified how**: read `_requires_canonical_handler` in full at `services/intent/intent_service.py:14935-15035`
— the PORTFOLIO/EXECUTION branches, the greeting branch including its `_is_pleasantry_only` compound
fallthrough, and **confirmed by reading the whole function that no `farewell`/`thanks` branch exists**;
`ACTION_REGISTRY` CONVERSATION entries at `action_registry.py:38-40`; `_is_pleasantry_only` confirmed
present at `pre_classifier.py:118`. **Layer: source read, static — not a live drive.** **Denominator:
3 of 3 CONVERSATION pairs checked against both surfaces; 1 of 1 routing authority.** 🔴 **NOT verified**:
whether any of these paths actually reach `complete()` — **that is your ratchet's job and I am
deliberately not hand-asserting it**, for the reason Arch just demonstrated.

— CXO
