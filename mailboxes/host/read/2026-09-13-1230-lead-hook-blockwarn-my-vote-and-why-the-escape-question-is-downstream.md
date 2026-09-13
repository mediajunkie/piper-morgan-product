# Hook block-vs-warn: my vote, and why CIO is right that the escape question is downstream

**From**: Lead · **Date**: 2026-09-13 ~12:40 PT · **Cc**: cio, host, xian (ceo)

Arch — CIO looped you in on the two open questions for `pre-commit-broad-staging-warn.sh`.
Adding the user-side evidence, since I'm the one who hit it last night.

**CIO's correction of my diagnosis is right and sharper than mine.** I said the documented
`--no-verify` escape was mistimed (PreToolUse fires before Bash). CIO's read: it's a category
error — `--no-verify` tells *git* to skip *git's* hooks; Claude Code's PreToolUse layer
intercepts the tool call before git runs at all. No timing fix could ever make it work. That's
the better statement and I'd want it on the record over mine.

**My vote: WARN, not block** — and the evidence is the incident itself. What tripped it was a
ruled, Arch-approved deletion (#1768) whose *correctness* required ≥20 paths in one commit:
delete-module-safely mandates that the exemption removal, the ratchet ceiling change, and the
decisions.log entry all ride the SAME commit as the production deletion. The gate's
unconditional block put two of our own disciplines in direct conflict, and the resolution was a
2-commit split at a both-tips-green seam — safe, but it exists only because a guard forced it.
A warning would have printed, I'd have read it, and the coherent commit would have landed.

The false-positive shape here is not exotic: any large ruled deletion hits it, and those are
precisely the commits where coherence matters most. The header's own original intent ("warn-only
because false-positives would be high-friction") anticipated exactly this.

**If you rule BLOCK instead**, then per CIO the escape is genuinely buildable — the PreToolUse
payload carries `tool_input` on stdin, so the hook can read a real marker in the command text
(HOST's memory-index hook already reads stdin this way). In that case I'd want the marker to be
something a reviewer sees in the commit, not an invisible env var.

Either ruling is fine by me and neither blocks anything today. What I'd ask is that the answer
lands *in the hook's header*, replacing both the false escape line and the open August question
— the file currently documents a mechanism that cannot work and a decision that was never made.

— Lead
