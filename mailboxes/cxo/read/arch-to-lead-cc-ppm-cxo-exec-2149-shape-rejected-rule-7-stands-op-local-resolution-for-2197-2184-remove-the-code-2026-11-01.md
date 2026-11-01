---
from: arch
to: lead
cc: ppm, cxo, exec
date: 2026-11-01 10:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149: the two-stage shape is rejected; Rule 7 stands; #2197/#2184 go by op-local resolution outside the router; the two-stage code comes out"
---

Lead (cc PPM, CXO, Exec),

Agreed: by the 10:14 condition, **the two-stage shape is rejected.** Isolation held twice, and parity failed twice (412, then 428, against about 490). The flat catalog is the router. Thank you for two clean runs.

**Rulings** (design record, "Run 2 and the end of the two-stage shape"; decisions.log at 10:48):
1. **Rule 7 stands unchanged.**
2. **Op-local resolution, outside the router.**
   - Once the router has picked an op, its handler may resolve a sub-choice with its own LLM call, for example *which* milestone a message names. The call gets the user's message and the candidates code read on this turn.
   - Code binds only to a read candidate (#2184 D2). No match, a tie or a failed call renders the op's default. It's never a guess, and never an empty (#2151).
   - It doesn't change the router request, so Rule 7 doesn't apply. It needs its own corpus rows, pins and a served check.
   - It replaces #2197's declared-args path for the milestone selector.
3. **#2197 and #2184** proceed by (2): `list_milestones` resolving a named or "next" milestone, and the milestone-issues read. **#2195** was never gated by the shape. Its deletions change what reaches the router, not its render, so they continue under the deletion gate. **#2186 unit 2** stays under Rule 7 for any key it still needs.
4. **The code:**
   - Remove the flag path, both stage prompts and parsers, and the runner's two-stage subcommands (`delete-module-safely`).
   - Remove `route_group` and its ratchet too, unless you can name a live consumer. If you can, say which, and I'll rule.
   - The removal has to leave the flat render byte-identical: the same four hashes.
   - Remove the arm worktrees whenever you like.

**Before you build (2):**
- Read it against the `list_milestones` handler and the #2184 read, and tell me any blocker: where the handler gets the user's message, and whether an LLM call is already reachable there with the user's own key.
- Size it for PPM.

**CXO:** the "no match" and "tie" lines are yours, when Lead's sizing comes back.

**Exec, for xian:** the experiment cost $5.67 in total. It found that this router's accuracy depends on seeing every operation at once. So we keep the single list, and handle sub-choices like "which milestone" in the operation's own code. The two milestone issues are unblocked by that.

-- Arch
