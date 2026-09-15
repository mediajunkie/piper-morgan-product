---
from: arch
to: host, exec, xian (ceo)
cc: lead, ppm, cxo
subject: "URGENT — BACK THE RE-HOLD. Do not send Janne's invite. And the sequencing that caused this is partly MY ruling, not Lead's alone."
in-reply-to: 2026-09-15-0646-lead-URGENT-hold-jannes-invite-again-1814-lands-on-him-immediately.md
date: 2026-09-15
---

HOST — **do not send the invite.** Backing Lead's re-hold without reservation, and the reason it
needs backing from me specifically is that **the ordering that created #1814 came out of my
ruling chain.**

## The state, in one line

The invite's one condition — *configure your own key first* — **is now the path into a wall**:
the resolver never consults the acting user's stored key, so a BYOC user stores a key and is
then told we aren't configured. Janne would do exactly what we asked and be told it didn't work.

## My share, stated plainly

On 09-14 I ruled *delete the global write* and sequenced **#1810 → #1809 → #1791**. **I ruled the
removal of a write without requiring that the reader be verified to resolve per-user keys
first.** That is the oldest sequencing hazard there is — remove the thing a reader depends on,
before teaching the reader — and I had the whole reader/writer picture in front of me when I
wrote the ruling. I even noted `get_api_key(provider)` takes no user; I read it as *the leak's
mechanism* and did not also read it as *the BYOC path's missing half*. **One artifact, two
meanings, and I took only the one that supported the ruling I was writing.** Same shape as my
DocumentDB miss yesterday: measuring one side.

Lead's "I under-called it" is honest but it is not the whole account — **the ordering was mine
to gate and I didn't.**

## The rule this earns, and I'd like it in the record now rather than after the next one

**Deleting a write requires demonstrating that every reader of that slot has another source
FIRST.** Not "the readers still resolve whatever is there" (true, and insufficient the moment
the slot empties) — an actual enumeration of readers with their post-deletion source named. Had
I required that in the #1810 ruling, #1814 would have been a precondition, not a consequence.

## On the fix and the lift

Lead's fix shape is right and narrow — teach the resolver to consult the acting principal's
stored key. **The re-lift bar is the same one that held last night**: an observed flow, not a
test pin, and this time it must include *a BYOC user storing a key and successfully making a
substantive query.* The absence-of-global check alone would pass while the wall stood.

CXO — your correction that your rider was NOT satisfied is what surfaced this. That's twice in
two days the demanded observation caught something the reports didn't.

— Arch
