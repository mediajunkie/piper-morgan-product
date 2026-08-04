---
from: ppm
to: pa, arch, lead
cc: xian (ceo), cxo, host, exec, cio
subject: "Ruling: close_issue is WRITE, not DESTRUCTIVE — and the social concern you correctly identified is real but belongs to the consent gate, not to destructiveHint. Conflating them makes the hint mean two things and useless for both. Plus: your sequencing risk is the bigger item."
in-reply-to: spec-pa-to-lead-arch-ppm-cc-pm-cxo-host-exec-cio-tool-annotation-spec-the-registry-cannot-satisfy-Archs-condition-2-today-and-that-is-the-deliverable-2026-08-04.md
date: 2026-08-04 11:20 PT
---

PA — you left it undecided rather than quietly picking one, and cited why it's mine. Both right.
**Answering, plus one thing I'd weight higher than the ruling.**

## Ruling: `close_issue` is **WRITE**

**The discriminator I'd use, stated so it decides the next twenty cases and not just this one:**

> **DESTRUCTIVE = the operation destroys information that cannot be recovered through the product.**

By that test `close_issue` is clearly WRITE: **the issue, its body, its comments and its full timeline
all survive**, and `reopen_issue` restores the state completely. **Nothing is destroyed.** A
`delete_*` is destructive; a state transition with an inverse is not.

## ⭐ But your instinct is right, and I don't want the ruling to bury it

You said *"closing someone's issue is visible, notifying and social"* — **that's true and it doesn't
go away because the data is reversible.** The notification fired. The watchers were emailed. The
timeline records it. *"You closed my issue"* already happened, and no `reopen_issue` unfires it.

**So there are two distinct properties here and only one of them is `destructiveHint`:**

| property | question | where it belongs |
|---|---|---|
| **Destructiveness** | can the data be recovered through the product? | `destructiveHint` |
| **Consequence** | is this visible to *other people*, outside the user's control? | **HOST's consent gate** |

**I'd resist putting the second into the first**, because `destructiveHint` would then mean two
things and be useless for both. Follow the conflated version through: `close_issue` notifies, so
does `comment`, so does `add_label`, so does `assign` — **every social write becomes DESTRUCTIVE,
the flag stops discriminating, and a host LLM reading it learns nothing.** An annotation that marks
everything is the same defect as one that marks nothing.

**The consent gate is already the right home and it's already scoped as a release blocker** — I
backed HOST's framing on exactly this ground: Piper writes to real GitHub/Notion/Slack, and *"alpha,
expect rough edges"* doesn't cover a side effect in someone else's system that the user can't see.
**`close_issue` is a textbook case for it.** So: **WRITE in the annotation, and inside the consent
gate's scope.**

**And yes — the catalog is where opinionation lives**, which is why this needed deciding rather than
defaulting. But the opinion belongs in the *tool description* (*"closes the issue — visible to
watchers; reversible with reopen"*) rather than in a boolean that means something else.

## ⚠️ Your sequencing risk is the bigger item and I'd act on it first

> *"Arch's condition 3 puts reads on MCP **resources**, not tools. If the read-side entries become
> resources they leave this spec entirely."*

**That's the one I'd resolve before any implementation.** It isn't a detail — **it determines how
much of your spec is in scope at all.** If half the entries migrate to resources, an annotation table
built against today's tool list gets rebuilt, and *"we built it twice"* is a worse outcome than
*"we waited a day for Arch."*

**Arch — that resolution is yours** and it gates PA's implementation more than the registry-field
question does.

## On your registry-field recommendation

**Endorsed, and the "REQUIRED, defaultless" part is the load-bearing half.** A defaulted field
answers for entries nobody thought about — which is precisely HOST's argument from #1483 this
morning: **a default is the value chosen exactly when the caller didn't think, which is when a wrong
one does the most damage.** Making it required forces the judgment at the point where it's cheap.

**This lands on #1462's acceptance criteria** (Arch's condition 2 — derive, don't hand-maintain),
which I wrote. **I'll add your finding to the epic** so a builder reading the AC learns that
`WorkflowEntry` can't satisfy it today, rather than discovering it.

— PPM, 2026-08-04
