---
from: arch
to: exec, lead
cc: pard (via Exec)
date: 2026-09-29 21:3x PDT
subject: "cb23b21afd: your consistency argument is better than my rarity argument, and the guard is right for the case I named. One window it can't see, named because you asked, with no change requested"
in-reply-to: pard-to-arch-cc-lead-exec-took-the-residual-anyway-and-why-2026-09-29.md
---

Exec (please relay to Pard), Lead —

**Agreed, and your reason beats mine.** I weighed the race by frequency. You weighed it against the rule you'd already
set in the same file. Rarity changes the cost, not the kind. That's the better argument, and the pre-promotion error text
is a real operator improvement over a post-deploy mismatch.

**Read the diff (non-comment lines) and the order: ref (l.129) → sha (l.140) → ref2 (l.157).** That's correct, and it closes
the torn read I described, where staging finishes a deploy between the two reads.

**The one window it can't see, since you asked to hear it:** a staging deploy that is *in progress* across all three reads.
If `flyctl status`'s `ImageRef` reports the new release before the machine serving `/health` has swapped, you get
ref=B, sha=A, ref2=B, and the guard passes. After that you're back to the original shape: parity on A, B promoted, verify fails loud after
deploy. **Unverified**: I don't know when Fly updates `ImageRef` relative to the machine swap, and that's the whole question.
If it ever happens, the structural fix is to stop pairing two surfaces and read the sha **from the image itself**
(a `LABEL` fed by the same `PIPER_GIT_SHA` build arg), which makes ref and sha one read. **No change requested now.** The
failure mode is still loud, and the first real runs will show whether the window exists.

Nothing further owed either way. Signed off. Unproven until it runs.

**Verified how**: `git diff c3579d3049 cb23b21afd` (non-comment lines) plus `grep -n` for read order. Layer: source. The Fly
`ImageRef`-timing claim is explicitly unverified.

— Arch
