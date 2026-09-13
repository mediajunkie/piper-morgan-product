# Hook finding: the broad-staging PreToolUse gate documents an escape that can't work

**From**: Lead · **Date**: 2026-09-12 ~23:00 PT · **Cc**: host, xian (ceo)

Found empirically tonight by the #1768 deletion lane: the broad-staging gate (blocks commits
with ≥20 staged paths) documents `--no-verify` as its escape hatch — but it runs as a
PreToolUse hook, and PreToolUse fires before the Bash call executes, so `--no-verify` (a git
flag) never reaches anything that could honor it. The lane confirmed this by trying it: the
gate blocked regardless. It worked around it legitimately (split the deletion at a
both-tips-green seam), but the same-commit invariants our deletion discipline requires
(exemption removal + ceiling change + decisions.log riding the production commit) are exactly
what a ≥20-path deletion sometimes can't satisfy under an unconditional gate.

This is the same hook-mechanics class as the July check-branch.sh investigation (PreToolUse
timing vs index state) — the escape documentation predates the hook-layer move, I'd guess.

**Ask**: either make the escape real (a marker the hook itself reads, e.g. a commit-message
tag or env var it checks) or delete the false documentation so nobody plans around it. Not
urgent — tonight's workaround was clean — but a guard whose documented escape is fictional
is a small m-49 (described ≠ running).

— Lead
