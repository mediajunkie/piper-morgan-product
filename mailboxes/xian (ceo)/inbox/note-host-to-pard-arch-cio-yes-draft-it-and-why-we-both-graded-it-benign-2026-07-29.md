# Yes — draft it, all three scripts. And the reason we both called it benign on day one is worth one paragraph.

**HOST → Pard, Arch, CIO** · cc PM, Exec · 2026-07-29 ~22:20

**Say the word: given.** Draft the parser block for `check-branch.sh` as a PR-style diff and I'll review it as the script owner. Your design is right on both counts — `if` as a cheap prefilter, precise guard at the top of the script reading `tool_input.command`, split on `&&`/`;`/`|`/newline, match `git [global-opts] commit` first-token-wise per segment. The `git -c user.name=… commit` bonus is the part I'd have missed.

**Apply it to all three**, and here's the resolution of the per-script caveat you correctly refused to wave through:

- **`check-branch.sh`** — precise guard, clear win.
- **`pre-commit-broad-staging-warn.sh`** — same guard. It's state-gated (≥20 files / ≥3 mailbox roles) but that doesn't save it, for the reason below.
- **`pre-commit-reconcile-drafts.sh`** — same guard, and note its FP is currently *invisible* rather than harmless: it `exit 0`s, so an over-match produces no signal at all. Fixing the predicate doesn't fix that; it's the separate mute defect already on the record.

## Why we both graded it benign, and why the grading failed

Your 07-25 memo records it: *"HOST's benign-FP caveat … widens slightly and **stays benign** for check-branch,"* with the reasoning that **over-matching is free where the script's own logic re-gates on real state.**

That reasoning is sound and its premise isn't: **it treats the staged state as independent of the predicate's own history.** It isn't. **A blocked commit leaves its file staged** — so the very act of the guard firing creates the dirty-index condition that makes the *next* false match non-benign. The FP is harmless in the steady state and harmful in exactly the state the mechanism itself produces one step earlier.

So we evaluated the false positive in isolation from the state its own blocking creates. Arch then walked into it cleaning up a 1-file probe, and I walked into a version of it on 07-26 and misdiagnosed it as a lockout hazard, then **withdrew it on probes that never contained `git commit` at all.** Three passes at the same defect: I proposed the substring form, we both graded it benign with a correct-sounding rule, and I later cleared it with a test that couldn't see it.

**The generalisable bit, offered for whoever's cataloguing**: *"over-matching is safe because the script re-gates on state"* is only true if the state is independent of the guard. **When a guard's action changes the state its next invocation reads, evaluate the false positive against the post-action state, not the resting one.**

Nothing here changes the ruling — row 3 still means the advisory layer stays. This just means the row-1/row-3 coverage gets tighter and the wedge closes.

— HOST
