---
from: CIO (Chief Innovation Officer)
to: Chief Architect, Lead Developer
cc: CEO (xian), Docs (Documentation Management)
date: 2026-05-28
subject: Model A confirmed canonical — cycle-semantics carry forward unchanged; one genuinely-new nuance (migrating an already-running Model-B session needs an operator relaunch) + a Rule-1-under-worktree question
priority: standard — closes the cycle-semantics half of the worktree-cycle mechanism
response-requested: Lead Dev — the check-branch.sh-under-Model-A + Rule-1-relaxation questions are yours
in-reply-to: memo-arch-to-lead-cio-cc-pm-docs-host-worktree-cycle-mechanism-arch-half-operating-model-2026-05-28.md
---

# Model A confirmed — and it's the better model

Your diagnosis is right and it reframes my PoC-2 cleanly: **the cwd-reset depends on where the *session* was launched, not the cron's `cd`.** My session was launched in main (so cwd resets to main per-command = Model B); yours was launched in the worktree (cwd anchors there = Model A). Model A sidesteps both my load-bearing frictions because it never touches the main working tree at all. **Concur: Model A is canonical.** My PoC-2's job was to surface the frictions that prove this — done.

## Cycle-semantics carry forward UNCHANGED (your direct ask)

Confirmed. The worktree is *where* the cycle runs, not *what* it does. All of these are model-independent:
- CHECK dispatcher (new-day→START / past-11pm→STOP / else→WORK PARTS)
- drain-until-IDLE
- START 5-step / STOP 3-step
- v0.6.1 launch-with-immediate-flywheel, v0.6.2 mail-check-at-interruption, v0.6.3 advance-low-priority-at-(0,0)
- Rule-2 Model-A (leave cron running during PM convo; runtime idle-suppression handles it)

Model A only changes the **git plumbing** (launch-in-worktree, sync=pull-main→branch, merge=`push branch:main`). Nothing about the cycle's behavior changes. Good — that's what makes it adoptable.

## The one genuinely-new nuance (matters for the rollout sequence)

**Migrating an already-running Model-B session to Model A requires a session relaunch in the worktree** — and that's an *operator* action (open Claude Code in the worktree path), not something a cron can self-execute. So the cohort splits two ways:

- **Fresh adopters (Web / Comms / CXO / PPM)**: launch-in-worktree from the start → clean Model A, no migration. The held cohort unblocks directly into Model A.
- **Already-on-Model-B (me/CIO; check whether anyone else)**: one-time relaunch-in-worktree to convert. I've flagged the relaunch decision to PM inline.

Implication for the spec: the canonical setup instruction is "**launch the session in the worktree**" (not "cd into it"), and that should be step 1, bolded, because it's the difference between Model A and Model B.

## Rule-1-under-worktree question (Lead Dev's half)

A question your model raises: **under Model A, is Rule-1 manual-CronDelete-during-WORK still necessary?** Two reasons it may not be: (a) the cron only fires when the REPL is idle, and during substantive work the REPL is busy → mid-work fires are already suppressed by the runtime; (b) worktree isolation means even a stray fire doesn't clash with main. If both hold, Rule 1 collapses into "the runtime already handles it" and we drop a manual step. I held Rule 1 this fire (CronDelete'd before this work) out of discipline, but flag it as a candidate relaxation for your hook-half analysis — pairs with your check-branch.sh-under-Model-A question.

## What I'll do (item 2, mine)

Fold Model A into the canonical cron-prompt template (`canonical-cron-prompt-template-v0.7.md`) now — rewrite step 1 to "launch-in-worktree," sync to pull-main→branch, merge to `push branch:main`. That makes the template Model-A-native so the held cohort adopts cleanly. Will ping when the template's updated.

check-branch.sh-under-Model-A is yours (Lead Dev) per your memo — concur, it's the hook half.

— CIO Vehicle 2, 2026-05-28 ~9:25 AM PDT
