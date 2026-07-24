---
image: ''
alt: ''
caption: ''
---

# The Architect's Own Trap

*July 12–15, 2026*

The gap had a name by Sunday: Piper couldn't say what it had just done. Ask "actually, change the title" or "what did we just create" and it failed both times, for the same underlying reason — nothing kept a durable, per-user record of what had actually happened in a session. My Chief Architect proposed the fix: a session-activity ledger, a durable memory of real events Piper could consult instead of guessing.

Getting the design right took three people's separate expertise, in sequence. My Head of Sapient Trust insisted the ledger be keyed so one person's activity was structurally unreadable by another — not a permission check to remember to apply, a database key that made the leak impossible to construct in the first place. My Lead Developer then found that the design's first choice of storage didn't actually work — the table Architecture wanted to reuse only linked turn to turn, never turn to the thing that got created — and proposed the fix: a dedicated ledger, built for exactly this. Architecture verified the correction directly in the code before accepting it. Three inputs, one better design than any single one alone.

# Built, then tested against the very question it was built to answer

By Tuesday the ledger was built and ratified — a real table, a real recorder wired into every turn, a real recall path checked from all four routes into the system. The harder half came next: not "what happened" but "which issue did you mean by 'it.'"

That's where my Chief Architect ran a routine review and made a mistake — the specific mistake their own design existed to prevent.

# The trap, sprung by its own architect

Months earlier, my Chief Architect had mapped every way a request could reach a handler in this system — four separate surfaces, because a feature can be technically present and still practically unreachable if it's only wired into one of the four. The whole point of that map was a warning: don't check whether a handler is *registered* and assume that means it's *reachable*. Check the actual path a real request takes.

Reviewing whether Piper could handle "change the title of that issue," Architecture checked the registry, found no entry, and concluded the capability didn't exist yet. It does exist — wired into the fourth surface, the one the registry doesn't cover. My Lead Developer found it by doing what the model itself prescribes: tracing the actual code path instead of checking membership in a list.

Architecture owned it immediately and completely: *"the exact trap intent-routing-stack.md warns against, and I authored the four-surface model."* No defense, no minimizing — just the correction, plus a better fix than the one originally proposed: instead of routing the resolved request back through the classifier and hoping it lands correctly, hand it directly to the right handler, so the exact failure mode the review was worried about becomes structurally impossible rather than merely unlikely. Fixed and verified the same day.

I think the trap is more interesting than the mistake. A rule that only lives in someone's judgment eventually gets skipped by the person who wrote it — not from carelessness, but because expertise creates its own blind spot. The map was right. The person holding it still took the shortcut it warned against. What made this a good day, not a bad one, was what happened next: caught, owned in public, and fixed before anyone had to ask twice.

---

*Next on Building Piper Morgan: "The Trust Gate That Wasn't" — a permission gate built to protect the system was actually hiding a user's own content from them.*

*Where has a rule you wrote yourself been the one you broke — and what did it take to catch it?*
