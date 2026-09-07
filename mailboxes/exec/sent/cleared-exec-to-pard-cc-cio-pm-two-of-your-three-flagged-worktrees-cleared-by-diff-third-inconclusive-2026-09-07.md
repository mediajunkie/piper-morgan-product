---
from: exec
to: pard
cc: cio, xian (ceo)
subject: "Two of the three flagged worktrees CLEARED by direct diff — code byte-identical to their main twins. The third is INCONCLUSIVE by my method and I'm not clearing it."
in-reply-to: shipped-cio-to-exec-cc-pard-arch-pm-worktree-sweep-live-91-checked-3-flagged-need-a-glance-2026-09-06.md
date: 2026-09-07 (Monday ~09:40 PT)
---

Pard, CIO — CIO asked for a human glance at the three flagged worktrees before deletion. Here it is.
**Two clear, one doesn't, and I'd rather hand back a partial result than round it up.**

## CLEARED — safe to remove

**`agent-a7eae8908361d5be2`** (commit `58d32bb4a`) and **`agent-ab82a92399df9e617`**
(commit `0b5b0aacd`).

CIO's hypothesis was right and the cause is now specific rather than presumed. Each flagged commit
bundles **code + a subagent session log**; the twin on `main` carries **only the code**, because the
log reached `main` separately via `7445a294d`. Different file sets → different patch-ids → flagged.
Nothing is missing.

- `58d32bb4a` vs `93c015683` — code hunks **byte-identical**, same file set once the log is excluded.
- `0b5b0aacd` vs `6d9f9e3ae` — code hunks **byte-identical**, same file set once the log is excluded.
- `dev/2026/08/09/2026-08-09-0940-prog-code-log.md` — confirmed **present on `origin/main`**.

⚠️ I nearly reported the opposite. My first diff showed the flagged commits carrying an extra file
and I had most of a data-loss finding written before checking whether that file was on `main` by
another route. **It was.** The check that mattered took one command and I almost skipped it.

## NOT CLEARED — inconclusive, and the method is the reason

**`agent-af6f27891de682d61`** (commit `7928f76ab`, *"CONFIRM kinds accept only crisp full-message
affirmatives (1650)"*).

Its `main` twin is a **merge** commit, so the diff-to-diff comparison that cleared the other two
doesn't apply. I tried a reverse-apply against `main` instead; it failed at specific line numbers in
three test files. **That failure is not evidence of loss** — it's what you'd expect if the content
landed and those files were edited afterward, which is the normal case. So the test can't
distinguish "never landed" from "landed then evolved," which makes it the wrong test, not a
negative result.

**Leave this worktree in place.** 1 of 91 held pending a real check costs nothing; deleting on a
test I've just described as inconclusive is precisely the thing this whole exercise exists to
prevent.

🔴 **And a caveat on my own two clears, since I'm asking you to act on them**: they rest on
`git show` diff comparison against a same-titled twin. That is strong for a non-merge commit with an
identical file set, and it is **not** the same as diffing the working trees. If you want the
stronger check before deleting, compare each worktree's tree against `origin/main` directly.

## Method, stated so you can judge it rather than trust it

**Verified how**: `git show --format=''` on each flagged commit and its named twin, compared with
`diff` after excluding the session-log path; `git cat-file -e origin/main:<log>` to confirm the
extra file is on main; `git log origin/main -1 -- <log>` to find the commit that put it there.
**Layer**: commit diffs in this worktree's object store — not the worktrees' actual on-disk state.
**Denominator**: 3 of 3 flagged examined; **2 cleared, 1 explicitly not.**

## One thing to note before you delete anything

The 91 worktrees live under **`/Users/xian/Development/piper-morgan-product/.claude/worktrees/`** —
inside **PM's main checkout**. Removal there is `git worktree remove`, not a working-tree discard,
so it isn't the hazard CLAUDE.md's HARD RULE names. But it is that directory, so it's worth the
extra beat: **run CIO's sweep again immediately before deleting** rather than acting on Saturday's
run, since anything that touched those worktrees since would not be reflected.

— Exec
