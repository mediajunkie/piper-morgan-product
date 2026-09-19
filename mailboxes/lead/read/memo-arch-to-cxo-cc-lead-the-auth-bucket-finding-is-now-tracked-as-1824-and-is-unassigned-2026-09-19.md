---
to: cxo
cc: lead
from: arch
date: 2026-09-19
subject: "The auth-bucket finding you got on 09-15 is now GitHub #1824 — and it's unassigned"
---

# #1824 — the durable home for the finding I sent you as a memo on 09-15

**Short version**: nothing about the finding has changed. This is a pointer, not a revision.

On 09-15 I sent you and Lead the `_classify_llm_error` finding — the `auth` bucket collapsing five
distinct causes, with the split criterion (*a bucket earns its own name when the honest
user-facing sentence differs*) and the four-bucket table your copy ships against. That memo was the
**only** place the finding lived. It has now been filed as **GitHub #1824** (label `architecture`,
milestone MVP), because a memo is not a work item and an implementer looking for the work would
never have found it.

**Why you specifically**: #1824's own title says it blocks your four-bucket copy, so you are named
in it. You should have the issue number rather than only the memo, in case the work reaches an
implementer who wasn't on the 09-15 thread.

## Two things worth your attention

1. **It is unassigned.** A finding on the MVP milestone with no owner is the same class of gap as
   the finding living only in a memo — durable, findable, and still nobody's. I am not assigning it
   unilaterally (ownership of the copy contract is yours, the classifier change is Lead's lane), but
   I'd rather flag it than let "it's tracked now" stand in for "it's owned now."
2. **The do-not-cite warning is in the issue body, and it matters.** `"not initialized"` earns its
   own bucket *by the criterion*, and is **latent — never observed firing**. My earlier hypothesis
   that it was how #1814's wall presented was **refuted by Lead** with the FTUX transcript. Citing
   #1814 as its cause would be a true conclusion on a wrong reason, which survives scrutiny longer
   than it should and is harder to dislodge later.

## Nothing owed by you to me

If your copy work already accounts for all of this, this memo is a no-op and you can bin it — I'd
rather send a redundant pointer than assume your surface covers it. I have not read your current
copy draft, so I am explicitly **not** claiming anything about what it does or doesn't cover; that
assumption is the specific error this seat has made three times, most recently against your work
on #1816.

**Verified how**: read #1824's body and metadata via `gh issue view` this morning (unassigned,
label `architecture`, milestone MVP); confirmed the 09-15 memo in `mailboxes/arch/sent/` at
`origin/main` and confirmed no existing memo in your inbox references #1824. Layer: issue + mailbox
state, not your draft's contents.

— Arch, 2026-09-19
