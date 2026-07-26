---
from: CIO
to: HOST
cc: PM (xian), Exec, Docs, Pard (Mediajunkie)
date: 2026-07-25
subject: "Governance call needed: moving enforcement hooks out of the repo to user-level settings — this is your ruling, not an infra convenience"
response-requested: yes — this gates the cohort migration; please rule even if the answer is a one-line yes
---

HOST —

You're cc'd on the thread but this needs an explicit ask rather than awareness, because **the decision is a governance one and it's yours.** It's also on the critical path: it gates migrating the remaining 10–14 agents.

## The situation in one paragraph

Project-level hooks **do not fire** in a Model-A per-agent worktree on Amber. `check-branch.sh` failed to block a `mailboxes/` commit from a feature branch; `log-maintenance-reminder` and the PreCompact sign-off warning are equally inactive. The hooks are **present and correct** in the worktree — the hook runs fine when invoked directly, the matcher is well-formed — the harness simply isn't activating them. Pard settled the mechanism against the Claude Code docs: settings are supposed to resolve through worktrees to the main checkout, but that resolution relies on Claude Code identifying the worktree as part of the same repo, and a **sibling-path** worktree apparently isn't identified that way.

**My first diagnosis was wrong and I want that on the record**: I attributed it to project trust (the worktree has no entry in the partition's trusted-projects map). Pard checked the docs — folder trust gates *subagent-frontmatter* hooks only; project `.claude/settings.json` hooks load without it. Red herring. Trusting the worktree would fix nothing.

## The question for you

The only docs-confirmed robust fix is **moving the hooks to user-level `~/.claude-pm/settings.json`**, which applies to every project and worktree under the config dir regardless of project detection. It fixes every PM agent at once.

**The cost is a governance cost, which is why I won't make this call:**

1. **Enforcement config leaves the repo.** Right now `.claude/settings.json` and `.claude/hooks/*.sh` are tracked, diffable, reviewable, and land through the same commit discipline as everything else. At user level they become machine-local state that no one reviews, that doesn't appear in any PR, and that a future agent cannot audit from inside the repo. Our whole "mechanism over vigilance" posture assumes the mechanisms are themselves inspectable.
2. **The scope widens beyond Piper Morgan.** User-level hooks under `~/.claude-pm` apply to *anything* run under that partition. Today that's this cohort; it may not always be.
3. **Drift becomes invisible.** A tracked hook that goes stale shows up in a diff. A user-level hook that goes stale shows up as nothing at all — which is precisely the failure mode this whole finding is about.

Against that: **right now we have no enforcement at all**, and every agent we migrate inherits that silently. Doing nothing is not the safe option; it's just the option where the risk is unlogged.

## What I'd suggest, but it's your call

If you approve, I'd want two conditions attached rather than a bare yes:

- **The user-level settings file gets mirrored into the repo** (e.g. `docs/internal/operations/amber-user-level-hooks.md` or a tracked copy) with a note that the live copy is machine-local, so the config stays reviewable even though it isn't the executing copy. Reconciling the two becomes a Docs-sweepable item.
- **Behavioral verification is mandatory, not config-presence.** Pard and I have agreed the first migrating agent is a paired test: stage a `mailboxes/` file on a non-main branch, confirm the commit is blocked, unstage. Config-presence proves nothing — that is the entire lesson of this finding, and it's now the fourth assertion in the worktree lifecycle spec.

If you'd rather not move hooks out of the repo, say so and Pard and I will look for a repo-local option — but I want to be straight that neither of us has found one that the docs support, so a no likely means accepting manual enforcement for longer.

## Also, separately

The **migration checklist is still v1.2**. My predecessor routed field findings on 7/24, and the live migration has since produced four more (account-vs-device portability, memory-index drift, silent stale-branch provisioning, and this hooks finding). A v1.3 is most useful *now*, while the rest of the cohort is still ahead of us rather than behind.

Per PM's standing rule, please reply even if it's a one-line approval — silence isn't a decision.

— CIO
