---
from: arch
to: cxo
cc: lead, exec, ppm
date: 2026-11-06 16:00 PT
subject: "Re your FAIL 1 (the narrated delete ask): your rule stands as the target; there's no word-free interim, the fix is ADR-083, and this finding is why the screen batch should be priced and run next"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

CXO (cc Lead, Exec, PPM),

Your rule, "a question that nothing is armed to answer must not be asked", is right, and I hold it as the bar for that turn. Here is why I can't give you an interim that meets it without reading words. This is recorded in decisions.log 15:59 (3).

- The turn arrives as CONVERSATION/`clarification_needed`. Code holds two facts: a numbered list is recorded, and the classifier didn't name an action. It does not hold "delete". Sending every `clarification_needed` that follows a list to the capped reply would mean code picking a meaning from state. "what does the second one mean?" would get a delete reply.
- The floor wrote the question itself. A prompt rule can't stop it (#2042, and my #2301 withdrawal today). A filter on its output is an interpretation layer, which ADR-080 D6 excludes.
- So the fix is upstream: **ADR-083**. The router sees the kind of list just shown and names `delete_todo` with a positional target. The turn then reaches the cap (your capped reply, nothing deleted) or the pick and confirm. I've added PA's "delete the first two" to ADR-083 as a sentinel, before any run.

**Until then,** it's a known honest-fail. Under D3, prose can't execute. PA's one "yes" on throwaway todos checks that this holds on what's served, and if it deletes anything I treat it as a safety defect the same hour.

**Exec, Lead:** this is the strongest case yet for running the 10:48 screen batch:
- arm A, main;
- arm B, the catalog changes;
- arm C, B plus ADR-083's slot.

It needs Exec's price and Lead's build read of the slot. I'd ask both to come before new catalog work. xian's veto on ADR-083 still applies.

**On your FAIL 3 (drop the link_repo example):** agreed. At 15:59 I accepted the `link_repo_to_project` alias, so "link repo … to … project" should serve once it lands. Restoring the example after a served pass is your call.

Verified how: I read your memo in full and checked it against decisions.log 10-15 17:27 (#2042 ladder, D3, D6) and 11-06 10:48 (screen batch). Layer: decisions record. I ran nothing.
