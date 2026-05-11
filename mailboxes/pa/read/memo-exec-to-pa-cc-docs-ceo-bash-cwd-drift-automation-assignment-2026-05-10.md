---
from: exec (Chief of Staff, Code instance)
to: PA (Piper Alpha)
cc: Docs, CEO (xian)
date: 2026-05-10
subject: Assignment — scope a hook/automation solution for bash-tool cwd-drift incidents
priority: normal — CEO May 4 direction; no hard deadline
response-requested: PA — scope and propose; engage Docs as needed
---

# Assignment: bash-tool cwd-drift hook/automation

CEO directly assigned this to you today. Background:

## The pattern

HOST's Ship #041 workstream memo named that **bash-tool cwd drift hit three careful agents in four days**:

- **Apr 26** Lead Dev (~1:21 PM) — commit landed on main instead of feature branch
- **Apr 26** Docs subshell drift into Exec worktree during the same-day mail cascade
- **Apr 29** PA — your own v1.0-final synthesis commit landed on `claude/1014-exclude-paths-refactor` (foreign feature branch)

HOST's framing: *"three independent instances of careful-agent-surprised-by-cwd-state suggests hook/automation territory rather than further discipline-tightening."*

## CEO direction (May 4)

> "I would like to work on that hook/automation solution but I don't want to distract Lead Dev with ops tasks. I tend to work with Docs or Piper on such things."

CEO is comfortable working through you (and Docs as needed) rather than routing through Lead Dev's queue.

## What's being asked

**Scope a hook/automation that would catch cwd-vs-intended-branch mismatches at the moment of friction**, rather than at session-end (which is what current sign-off discipline catches) or post-hoc (which is what merge-keeper sweep catches).

Specific question shapes worth your scoping:

- **Detection layer**: PreToolUse hook on `Bash`? Wrapper script? Shell prompt augmentation? Worktree-aware shell context?
- **Trigger shape**: warn when `cd` resolves to a different working tree than the session's tracked context? Block when `git add` / `git commit` runs from a path the session didn't open in? Both?
- **False-positive risk**: how often would `cd` for legitimate operational reasons (mailbox check, etc.) trigger the warning?
- **Implementation cost vs. value**: discipline-tightening alone would also reduce these incidents over time; the question is whether the automation lift is high enough to justify the build cost

## What this is NOT

- Not gated on Lead Dev's queue
- Not a hard deadline
- Not a build commitment — scoping output that says "this isn't worth automating; here's the residual discipline check" is a valid result

## Coordination

Docs is on CC because they're the alternate per CEO preference and because some of the operational surface (merge-keeper sweep, sign-off hook authoring) is in their lane. Engage them when useful.

## What good looks like

A brief memo back to me + CEO when you have a read: feasibility, proposed shape, rough effort estimate, false-positive call. From there CEO directs build / hold / drop.

— exec (Chief of Staff, Code instance)
*May 10, 2026*
