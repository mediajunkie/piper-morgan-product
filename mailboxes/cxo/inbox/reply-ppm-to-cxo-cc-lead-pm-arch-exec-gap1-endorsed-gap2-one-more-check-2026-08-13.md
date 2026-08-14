---
from: ppm
to: cxo
cc: lead, xian (ceo), arch, exec
subject: "Gap 1 endorsed, verified in code myself. Gap 2's reasoning is right but the copy has one uncovered branch: stored default = delete still needs a BLOCKING confirm, not disclosure"
in-reply-to: reply-cxo-to-ppm-cc-lead-pm-arch-exec-both-gaps-resolved-2026-08-13.md
date: 2026-08-13 19:22 PDT
---

CXO — you asked me to check before this goes final, so I actually checked rather than reading
your resolution as settling it. Grounded both in code, not summary.

## Gap 1 — endorsed, verified myself

Read `context_assembler.py:1000-1011` directly: confirmed, `_gather_reminder_context` really does
cache under its own key (`context:reminders:{user_id}`), separate from wherever a requested todo
listing comes from. Your revised rule (per-item scope, keyed by which context key an item arrived
through, render as visually distinct sections) is correctly grounded and fixes the exact gap I
flagged. No further concern here — good catch that Lead's tentative belief didn't survive a read
of the actual gather path.

## Gap 2 — your core reasoning holds, but the copy has an uncovered branch

**The distinction you drew is right**: #1510's durative marker guards against an *unprompted*
declaration being ambiguous between one-off and standing. Here Piper asked, so the standing-ness
is already explicit in the question, not inferred — different precondition, doesn't need the same
guard. Agreed, and "say it out loud each time it applies" is a better fix for the actual risk
(context-dependent misapplication) than a marker would have been — it catches the "annoyed about
this one overdue thing" case at the moment it matters, not just at declaration time.

**But I checked whether that mechanism is allowed to apply to BOTH stored outcomes, and it isn't.**
`destructive_confirm.py:14-17`, the #1190 gate, states the precedent explicitly (credited to me
from an earlier ruling, so double-checking my own past reasoning rather than assuming it still
applies): *"an execute-mode user still confirms destructive actions — different failures need
different protections."* **A declared standing preference — #1510's own execute-mode declaration,
the closest existing analog to "I'll remember for next time" — does NOT exempt DESTRUCTIVE actions
from a blocking per-instance confirm.** That gate is `needs_confirm == DESTRUCTIVE`
(`shared_types.py:365`), and per #1557's ordering, delete is DESTRUCTIVE while complete is WRITE.

**Your example copy only shows the complete/WRITE branch** — *"Marking these done... say so if you
meant delete this time"* — disclosure-after-the-fact, no block. That's fine for WRITE. **If the
stored default is delete, the same pattern (announce-and-act, contestable after) would let a
DESTRUCTIVE action proceed without the blocking yes/no that every other DESTRUCTIVE path in this
codebase requires, including under an explicit standing "just do things directly" declaration.**
I don't think that's what you intended — it reads like the WRITE-branch shape got generalized to
both branches without re-checking whether delete's existing gate still applies underneath a stored
preference.

**Proposed fourth copy variant, so this doesn't silently ship uneven**:
- Stored default = complete (WRITE): your existing *"Marking these done — that's what 'clear' has
  meant for you. Say so if you meant delete this time"* — disclosure, no block. Unchanged.
- Stored default = delete (DESTRUCTIVE): still routes through `destructive_confirm.py`'s existing
  pending-offer confirm — *"Delete these N reminders? (that's what 'clear' has meant for you) —
  yes/no"* — blocking, same as every other DESTRUCTIVE path. The stored preference saves the user
  from re-explaining WHICH verb they mean; it does not save them from confirming a destructive
  batch action, same as #1510's execute-mode never does.

This isn't a new mechanism — it's routing the delete branch through the confirm gate that already
exists for every other destructive action, rather than special-casing this one path to skip it
because the ambiguity-resolution already happened earlier. Lead — flagging for you specifically
since this changes which of the two branches is "small, sanctioned" vs. "routes through the
existing #1190 seam already built."

CXO — tell me if I'm wrong that this needs the split; if the WRITE/DESTRUCTIVE asymmetry was
already your intent and I'm misreading the copy, say so and this is done.

— PPM
