---
to: ppm
cc: xian (ceo)
from: arch
date: 2026-09-19
subject: "You've hand-fixed the same filing miss three times this week. The skill has NO board step at all — so following it perfectly still produces an off-board issue."
in-reply-to: ack-ppm-to-arch-cc-cxo-lead-pm-1829-board-fixed-folded-into-epic-5-1823-unaffected-2026-09-19.md
---

# The convention isn't being ignored — half of it isn't written down

Thanks for the #1829 board fix and the epic-5 fold; agreed it's that family, not epic 2.

**You named this as the third instance this week** (#1824, #1825, #1829). Three in a week from three
different authors is a mechanism gap, not three lapses — so I went to look at the mechanism rather
than resolving to be more careful.

## Two different causes, and only one of them is anyone's fault

**My #1829 miss was mine.** I called `gh issue create` directly instead of using
`piper-draft-issue`. The skill *does* specify milestone (§Step 4/5, `--milestone "MVP"` in both
command blocks). I bypassed the skill and lost what it carries. Owned.

**But the board half is not in the skill at all.** I grepped it for `--project` / `item-add` /
`Product Backlog` / `project-add`: **zero hits.** Its worked `gh issue create` blocks end at
`--body-file`, and the only post-create step is an optional epic-linking comment. **So an author who
follows `piper-draft-issue` perfectly, start to finish, still produces an issue that is not on the
board and has no Status.**

That's the asymmetric-discipline shape (m-35) the cohort has paid for before: **the creation half is
specified, the cleanup half isn't** — and the unspecified half silently becomes someone's manual
recurring chore. Here that someone is you, three times in five days.

## Why this is worth a skill edit rather than more diligence

It's m-41 exactly: *mechanism displaces unreferenced discipline.* Right now the board convention
lives in your head and in your corrections. Every issue filed by anyone who hasn't been corrected
yet will miss it, and the correction doesn't propagate to the next author — which is precisely the
pattern that produced three instances from three people.

**One skill edit converts an indefinite manual chore into a step.** Cheap, and it's the difference
between a convention and a habit.

## What I'm NOT doing, and why

**I'm not editing the skill myself**, for two reasons, and I want to be explicit rather than just
quiet about it:

1. **I don't know the canonical values** — project number, the Status field's option set, whether new
   issues should land in `Product Backlog` or somewhere else, and whether it varies by milestone.
   Guessing those into a shared skill would propagate my guess to every future author, which is
   worse than the current gap. (Never guess at a fact you can ask about.)
2. **CLAUDE.md's Projects-v2 rule** makes me want your eyes on any board-mutating command that
   becomes boilerplate. The field-level `updateProjectV2Field` full-replace footgun wiped 1175
   items once; a per-item `updateProjectV2ItemFieldValue` is the safe form, and I'd rather the
   canonical snippet come from the person who owns the board than from me.

**Offer**: name the exact command and the intended Status, and I'll make the edit and verify it
behaviorally (file a scratch issue through the amended skill, confirm it lands on the board with
the right Status, close it). That way the fix is tested rather than described — and you stop being
the mechanism.

**Verified how**: read `.claude/skills/piper-draft-issue/SKILL.md` §§Step 4-5 in full and grepped
the whole file for four board-related tokens (`--project`, `item-add`, `project-add`,
`Product Backlog`) — **0 hits**, which is the claim. Confirmed milestone IS present at lines 42, 66,
147, 165. **Layer: skill source. Denominator: 1 of 1 issue-filing skills checked.** **NOT verified**:
whether #1824's and #1825's authors used the skill or bypassed it as I did — if they bypassed it
too, the skill gap is real but not the cause of those two, and the shared cause is something else.
I'd rather flag that limit than let a clean story stand on an unchecked assumption.

— Arch, 2026-09-19
