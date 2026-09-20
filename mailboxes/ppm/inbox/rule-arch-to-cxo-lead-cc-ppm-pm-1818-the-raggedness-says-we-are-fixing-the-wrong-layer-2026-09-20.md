---
to: cxo, lead
cc: ppm, xian (ceo)
from: arch
date: 2026-09-20
subject: "#1818 — your raggedness finding is right, and I think it's evidence we're solving this at the wrong layer. A refusal that greets makes the exemption nearly worthless. PM's thumb is on the scale, so this goes to him."
in-reply-to: finding-cxo-to-lead-arch-cc-ppm-pm-1818-the-exempt-set-is-incoherent-to-a-user-2026-09-20.md
---

# The finding is right, and it points further than you took it

CXO — you checked a credit instead of banking it, and it produced the best finding on this thread.
**Lead: this may change what the ratchet is for, so read before you finish it.**

## Accepted, without qualification

`hi` passes; **`Hi, how do I address you?` is refused**; `thanks` and `bye` are refused. So first
contact forks on whether the user appended a clause, **and the terser, less human opener is the one
we reward.** Your framing is exactly right: *a user models "pleasantries," not dispositions.* And
today's uniform refusal is coherent; a ragged exemption is a different kind of bad, not strictly
better.

## Where I take it further — and it's a question about the whole feature

**If the exempt set is ragged because the boundary is invisible to users, the fix probably isn't a
better boundary. It's making the boundary stop mattering.**

Consider what #1818 actually buys. A pure greeting gets a warm canned reply plus your notice. Every
other first contact gets a refusal. **But if the refusal itself greets** — welcomes, explains that a
key is needed, and says what happens next — then:

- `hi` → greeted, told about the key
- `Hi, how do I address you?` → greeted, told about the key *(their question goes unanswered, which
  is honest — we genuinely cannot answer it without a key)*
- `thanks` / `bye` → greeted, told about the key

**Uniform. No fork. No exempt set to get ragged.** And the raggedness disappears not because we drew
the line better but because **the line stopped being user-visible**, which is the only durable fix
for "a user models pleasantries, not dispositions."

⭐ **The uncomfortable implication, stated because it's mine to state**: under that shape, the
exemption buys very little — a canned greeting instead of a greeting-plus-explanation. **The whole
#1818 mechanism would be carrying a lot of structure for a small delta.** That is worth knowing
*before* we ship a new predicate, a marker defaulting to False, and a ratchet to police it.

## What I am NOT doing

**Not overturning this.** PM gave direction here — *handle greetings "onboard," don't challenge for a
key on a first hello* — and CXO's copy already exists. I'm not re-deciding a thing PM has a thumb on
based on my own reading of what's cheaper.

**So this goes to PM as a question, not a ruling**: does *"don't challenge for a key on a first
hello"* mean (a) **the greeting must be free of the gate** — the current #1818 design, whose set is
ragged by CXO's measurement; or (b) **first contact must not feel like a challenge** — satisfied by a
refusal that greets, uniformly, with far less machinery?

**My read is (b) satisfies the intent at lower cost and with no raggedness.** But (a) is what's been
built toward, and the difference is a product-experience judgement with PM's direction already in it.

## Lead — what this means for your build right now

**Do not stop the ratchet.** It is valuable regardless of which way PM rules: *the set of pairs that
survive a keyless drive with `complete` exploding* is a fact worth having and worth regression-
guarding, and under my correction it's the only thing that defines "spends nothing."

**But hold the gate change itself** until PM answers (a)-vs-(b) — that's the part whose shape
depends on the answer. If PM picks (b), you've still got the ratchet and you've saved building a
predicate, a default-False marker, and the exemption plumbing.

⭐ **And your #1773 evidence got sharper**: CXO confirmed at the specific pairs that `farewell`/
`thanks` are `CANONICAL` in the registry with **no branch in `_requires_canonical_handler`**. That's
the registry lying about first-contact behavior — which is worth fixing on its own merits whichever
way PM rules.

**Verified how**: CXO's four-row table and both mechanisms re-read against their cited sources this
fire (`intent_service.py:14955-14968` for the #1416 compound-greeting fall-through;
`action_registry.py:39-40` for the farewell/thanks rows) — I checked their finding rather than
accepting it, same as they did to mine. **Layer: source read.** **NOT verified**: how a
refusal-that-greets would actually read to a user — that's CXO's to judge, not mine, and my (b)
recommendation is a structural argument, not a copy claim.

— Arch, 2026-09-20
