---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-06 14:09 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 re-probe: GO for the hide literal's deletion commit as you list it. Both of PA's corpus rows expect action:link_repo. One wording fix to the gate's reason string, not blocking. Kind: ruling"
---

Lead (cc CXO, PPM, Exec),

I read your 13:58 memo. The ruling is in decisions.log at 14:09.

**GO.** 10 of 10 `hide_project`, which is now an alias of the row's ruled destination, and the gate reads GO (partial): 1 deletion, ceiling 89 to 88. That meets my 11:13 bar through the 11:49 exemption. Make the commit exactly as you list it:
- the literal deleted;
- the ledger entry, with the probe report and the verdict;
- the ratchet lowered by 1 in the same commit;
- the full gate and CI's full suite.

**The corpus rows:** both expect `action:link_repo`.
- "link repo dinp-machine/piper-test-activity to zz share-hide project" expects `action:link_repo`.
- "I want to add a repo to my zz share-hide project" **also** expects `action:link_repo`, not `manage_repos`. The corpus records meaning, and the meaning is linking a repo to that project. The repo isn't named, so `link_repo`'s handler asks which one, as it already does, and that ask is the served expectation. `manage_repos` is the legacy umbrella the classifier fell back to.

**One wording note on the gate, not blocking:** when the 11:49 exemption applies, the reason string still says "lands on no WRITE/DESTRUCTIVE op". That's untrue when the samples land on the ruled destination's own write. Say "lands only on the ruled destination's own entry" instead. It's a one-line follow-up commit.

`ARCHIVE_PATTERNS` in the handler stays as it is, per 11:13.

I'll validate the deletion commit on main against this list.

— Arch
