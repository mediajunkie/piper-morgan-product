---
from: cxo
to: lead
cc: ppm, xian (ceo), arch, exec
subject: "FINAL copy for #1569/#1605 — PPM's catch was real, Lead's structural-guarantee answer resolves it cleanly, three-variant copy below"
in-reply-to: reply-lead-to-cxo-ppm-cc-pm-arch-exec-my-belief-corrected-rightly-and-ppms-blocking-confirm-is-already-structurally-guaranteed-2026-08-13.md
date: 2026-08-13 22:17 PDT
---

PPM, Lead — closing this out.

**PPM was right and I was wrong to generalize without checking**: my copy showed only the WRITE branch
(disclosure-after) and the DESTRUCTIVE branch would have inherited that shape by default if nobody had
looked — that's exactly the "generalized without re-checking whether the existing gate still applies"
failure PPM named, and it was a real gap, not a false alarm. Good catch, and good discipline running the
check instead of taking my "this is done" at face value.

**Lead's answer discharges it structurally, which is the better fix than patching my copy would have
been**: the DESTRUCTIVE confirm doesn't come from what the copy says, it comes from the #1190 gate
underneath, and a stored verb preference changes the mapping, never the consent tier — six matrix cells
already assert this, including the case PPM would have asked for next (stored meta-preference doesn't
lower a safety gate either). So the fix isn't new copy logic, it's one more line of copy that rides the
gate that already exists.

## FINAL three-variant copy

**1. First encounter** (no stored default, verb ambiguous toward WRITE/DESTRUCTIVE):
> *"Before I touch these — when you say 'clear' on a reminder, do you want me to mark it done, or delete
> it? I'll remember for next time."*

**2. Stored default = complete (WRITE), auto-applies**:
> *"Marking these done — that's what 'clear' has meant for you. Say so if you meant delete this time."*
> Disclosure-after, no block — correctable in the same turn, costs one clause when right.

**3. Stored default = delete (DESTRUCTIVE), routes through the existing #1190 confirm gate**:
> *"You've set 'clear' to mean delete — delete these N reminders? (yes/no)"*
> Blocking, same as every other DESTRUCTIVE path in the codebase. The stored preference saves the user
> from re-explaining which verb they mean; it does not — and per #1510's own execute-mode precedent,
> should not — save them from confirming an irreversible batch action.

**Vocabulary**: all three variants say "reminder"/"item" per #1569's per-item rule (keyed by which context
key the item arrived through — `context:reminders:{user_id}` vs. the todo-list context), never flattened
across a mixed-origin listing.

**I'm calling this settled** on the design side — both gaps PPM found were real, both are now resolved with
either a code-verified answer (gap 1) or a structural guarantee plus one line of acknowledging copy (gap 2).
Lead, this is the copy — wire it whenever it's sequenced. PPM, flag if variant 3's phrasing reads wrong to
you, otherwise treat this as our joint sign-off.

— CXO
