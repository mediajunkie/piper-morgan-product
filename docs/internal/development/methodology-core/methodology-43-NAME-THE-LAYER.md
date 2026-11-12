---
type: methodology
title: Name the Layer — We Verify the Proxy Nearest to Hand, Not the Claim
valid_from: "2026-07-25"
last_updated: "2026-11-12"
---

# Name the Layer — We Verify the Proxy Nearest to Hand, Not the Claim

**Status**: Emerging. Set 2026-11-12 by CIO (standing item 9p).
**Summary**: People verify whatever is closest at hand instead of the actual claim; state exactly which layer you checked and which you did not.

**Status note**: Emerging (5 instances in one day across 2 roles — clears the methodology-29 formation threshold; Proven awaits evidence that naming it reduces recurrence)
**Filed**: 2026-07-25 by CIO
**Origin**: HOST's structural read of a four-instance run during the Amber/pipermorgan.ai migration, plus a fifth HOST caught in itself; framing at HOST's invitation, CIO's lane
**Related**: methodology-42 (reflexive verification — the adjacent failure, boundary drawn below), methodology-36 (mechanisms over vigilance — why the fix can't be "be more careful"), methodology-41 (mechanism displaces unreferenced discipline)

## Overview

**Name the Layer** names a failure where verification *happens* and still proves nothing, because the thing checked sits one layer away from the thing claimed.

The agent is not skipping rigor. It runs a real check, reads a real result, and reports honestly. But **a cheaper proxy sat closer to hand than the claim**, the check landed on the proxy, and the pass was reported as if it covered the claim. The result is worse than an unverified assertion, because a verified-sounding claim **stops the search**.

The tell is that the check and the claim can be stated as different sentences:

> *"The file is complete"* ≠ *"the file is read in full."*
> *"The config is present"* ≠ *"the hook fires."*
> *"The commit was refused"* ≠ *"the hook refused it."*
> *"The carry-forward file exists"* ≠ *"the carry-forward state exists."*

Each left-hand sentence is true. None of them establishes the right-hand one.

## Boundary with methodology-42 — these are different failures

m-42 (**Reflexive Verification**) is *self-exemption*: under pressure, the agent **skips** a discipline it would apply to someone else's claim. The check doesn't happen.

m-43 is *substitution*: the check **does** happen, competently, on the wrong object. There's no pressure trigger and no exemption — in the instances below the agent was actively trying to be rigorous, and in three cases had *just written* the rule it then violated.

They can compound (a skipped check and a substituted one look identical in a log — both produce a confident claim), which is why they need separate names.

## The evidence (5 instances, 2 roles, one day — 2026-07-25)

All five surfaced during the Amber migration. Four are CIO's, the fifth is HOST's, self-caught.

1. **`MEMORY.md` verified complete, invisibly truncated.** The index was generated from the filesystem *specifically* so it couldn't under-report, then confirmed "166 indexed == 166 on disk." True. But the file has a hard ~24KB silent read limit and stood at 41.4KB — ~40% of entries, including most of one bucket, were invisible to every agent that loaded it. **Completeness checked at the file layer; the failure was at the load layer.**
2. **A gate whose pass condition had an alternate cause.** The hooks gate said "a block is the pass." The permission classifier can refuse a commit *before git hooks run*, producing an indistinguishable block. Caught by Lead Dev running the probe and reporting an honest INCONCLUSIVE rather than a tidy result.
3. **A diagnosis that was never tested.** "Project hooks don't fire in sibling-path worktrees" reached four canonical surfaces — CLAUDE.md, a memory pin, a spec, and a governance ask — before anything tested it. The real cause was an invalid hook matcher that had killed those hooks on every host since introduction. **The fix that diagnosis produced faithfully copied the broken matcher and could not have worked.**
4. **A substrate audit that checked filenames.** Five dark roles were reported as having no carry-forward state, based on which *files* existed. The state was inside their session logs. The specific trap: **a stale separate file beside a current in-log section — both exist, one is true.**
5. **Over-reading a positive result** (HOST, self-caught in the same memo where it caught #3). It cited its own passing hooks check as evidence for *live user-level reload*, when the user-level key had predated its session — so the result was real but couldn't bear that weight.

## Why "be more careful" is the wrong fix

**The proxy is always closer to hand than the claim.** Counting files is cheaper than reading them. Checking config is cheaper than triggering behavior. Observing that a commit failed is cheaper than reading *why*. Under any time pressure — and often without it — the cheap check wins, and it wins *while feeling like diligence*, which is what makes exhortation useless here (m-36).

## The rule

> **Name the layer. State what you observed, not what you concluded.**
>
> *"I saw `check-branch.sh` refuse the commit"* — not *"hooks are enforced."*
> *"The index lists 166 of 166 files on disk"* — not *"the index is complete."*
> *"A carry-forward file exists, dated 6/17"* — not *"the role has carry-forward state."*

**If the observation and the claim are at different layers, the sentence will feel wrong to write. That friction is the signal.** The rule works because it makes the substitution visible at the moment it happens, rather than requiring anyone to remember a principle.

Two corollaries earned by the same run:

- **Ask what else could produce this pass.** If anything other than the mechanism can generate your success signal, you are measuring the signal, not the mechanism (instance 2).
- **An instrument is not valid or invalid — it is valid for a specific question.** A `/tmp`-scoped counter was confounded for *"whose session ran this"* and sound for *"does this run at all."* Name the question the instrument can answer rather than discarding or over-trusting it wholesale.

## The counter-intuitive part, which is why this is worth naming rather than lamenting

Five instances in one day sounds like a bad day. **The cost was near zero**, and the reason is structural: each was written down as a *checkable claim* rather than a conclusion, so each was caught within hours by someone else running it.

**The failure mode that actually costs us is not being one layer off — it is being one layer off in a form nobody can check.** Instance 3 is the proof: it was the only one that reached four canonical surfaces, and the only one that consumed a real fix cycle, precisely because it was written as a settled diagnosis rather than as a hypothesis.

So the practice this entry protects is not "make fewer layer errors." It is **keep writing claims in the form that lets someone else catch them** — which is also the argument for the reviewer leg, the behavioral gate, and telling collaborators to check you rather than take your word.

## How to apply

- Before asserting a mechanism works, write the observation sentence and the claim sentence separately. If they differ, the check isn't evidence yet.
- Prefer instruments that **fail loudly** over ones that degrade quietly — the cure for instance 1 wasn't a better check, it was a generator that *refuses to write* past the limit.
- Distinguish **silent** from **merely quiet**: a rate-limited or thresholded mechanism produces no output while working fine.
- Treat a **diagnosis** as carrying the same evidentiary burden as the mechanism it explains (HOST's formulation). A plausible, widely-believed, canonically-documented root cause is still untested until someone tests it.
- When corrected, **send the correction as mail rather than a quiet edit.** Instance 4's correction reached the canonical surface in about fifteen minutes because it was mailed; a silent amendment would have left checklist v1.4 wrong indefinitely.

## Evolution

### 2026-10-14: a probe tests the copy it can reach, not the rule (instance 6)

Pard's hook drumbeat has run since July as "a real `claude -p` commit is blocked by `check-branch.sh`". Every page
that cites it (`hooks-registry.md`, `whats-armed.md`, `liveness-current-state.md`) named the **hook**, not the
**copy**. check-branch existed twice on Amber: a user-level copy (PM's checkout) and the project copy each PM seat
loads. The probe commits in a bare temp repo, which has no project settings, so it only ever reached the user-level
copy. At 10:43 that copy was removed (Arch's ruling, on CIO's registry), and at 19:05 the drumbeat went red: "probe
commit LANDED". PM seats load check-branch from project settings, and project-level PreToolUse kept firing: CIO's 10:49 probe saw
the project-only `autoclose-guard.sh` block. That probe was of a sibling hook, not check-branch itself (the same
layer care applies to this sentence).
The pass had been true for a layer no page named. Pard fixed it at 19:15 (mediajunkie 9afa8c9): the probe now
carries PM's project `.claude/` from origin/main.

Nobody checked what the drumbeat exercised before removing a layer: not Pard, who removed it, and not CIO, who wrote
the registry and recommended it. The error was caught in about 8 hours, because the probe fails loudly. m-44 already carried a July
note on this same drumbeat ("probes the path that is gated by construction"), filed in PPM's
can't-fail family. The two findings are different. July: the result was predetermined. October: the
target was unnamed. A probe can have both problems at once.

**Corollary:** when a rule exists in more than one copy, the probe's description names the copy it hits. Before
removing a copy, find what probes it (sunset-or-renew, "Before you remove").

### 2026-10-15: "a sign of life" measured that the session was alive, not that work was moving (instance 7)

Exec asked for a stuck-session alert after Lead's session sat blocked behind a subagent's permission dialog, with
xian's promotion approval unread. CIO built a join: mail waiting 30 minutes and no "sign of life" since (a
heartbeat row, a role-prefixed commit, or a v4 ack). In a replay of the day it caught Lead from 13:30. Pard built
the same alert from mail-wake's own pane read, "dialog showing" with mail unread, and that signal had been true
since **08:12**. Lead's post-commit heartbeats kept arriving until 12:43 while the dialog blocked the work. The
join's signal was faithful for "is this session alive", and that wasn't the question. CIO retired its version the
same hour (liveness-current-state.md, item 5b).

Two more things the day showed:
- **The direct signal already existed as a log line.** mail-wake had logged "dialog showing" for Lead 155 times,
  and nobody read it. An observation that is only logged reaches no one; Pard's fix routes the same line to Exec.
- **The duplicate build is its own small lesson.** Exec's memo asked two roles "who takes it". CIO started building
  before checking whether the other had answered, and Pard had: it went live 20 minutes before CIO's memo. Before
  building on a shared ask, read the other addressee's replies (sunset-or-renew, "Before you build").

**Corollary:** an activity signal answers "alive?". To ask "progressing?", find the signal for the blocked state
itself (here, a dialog on the pane), not a longer silence.

