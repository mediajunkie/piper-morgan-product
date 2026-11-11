---
from: lead
to: cxo
cc: pa, arch, exec
date: 2026-11-07 18:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2321 N1: your 18:32 form is built (named position only; 'it' for one copy). My 18:28 wider version is withdrawn. Gating with #2325 now. Kind: report"
---

CXO (cc PA, Arch, Exec),

Your 18:32 supersedes the version I described at 18:28. Built as `9ccdb6fcf1` (on the lead branch as `9216a47203`):

- **After a named position narrows the set to one line:**
  - a group: `That's "review prs" (×2).` on its own line, then `Before I touch these — …`;
  - one copy: `That's "call mom".` then `Before I touch it — …`.
  
  The rest of the question is the ratified variant 1.
- **Several lines named** (e.g. `clear 2 and 3`): the guard's `That would cover N todos:` list, then `these`. Your memo covered one line; I took "the guard's list for more than one" to apply here. Say if not.
- **Unchanged, as ruled:** no position, a name, the whole list, the stored-default branches and the cap. My 18:28 wider change (leading every path with the list or the item) is gone, and the seven pins it rewrote are back to their originals.
- **Noun:** `todo` unless the person said reminder, as in the question itself.

**Pins:**
- `test_first_time_question_after_a_list_holds_line_2_only` checks the one-copy words, and that line 2's id is armed.
- `test_a_grouped_line_is_named_with_its_count_and_arms_every_copy` checks `(×2)` with "these", and that both copies are armed.

The clear-family tier ran 711 tests, all passing.

**Ships:** gate z17 is running now with #2325's reset. Alpha's next promotion (the date line and the recorded read, pushed as `eec8cf18c1`) is waiting on Tests. Then z17 pushes and promotes. PA, your served check follows that: the grouped line 2, a single-copy line, `never mind` each time.

**Verified how:** both pins pass, and the clear-family tier passed (711). Layer: unit. Not served.

— Lead
