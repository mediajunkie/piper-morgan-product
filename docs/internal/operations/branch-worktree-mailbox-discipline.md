# Branch, Worktree, and Mailbox Discipline

**Status**: v1.0 (PA-hosted synthesis, published 2026-04-29 after cohort concurrence)
**Owner**: Docs (publication); PA (synthesis-of-record)
**Source inputs**: CXO original proposal (2026-04-26), with replies from Lead Dev, PPM, Exec, Docs, HOST + PM concurrence walks (Apr 26–28)
**Supersedes**: nothing (first canonical statement); CLAUDE.md "Mailbox Discipline" section is summary-and-pointer to this doc

---

## What this doc is

The canonical operating norms for how agents working on Piper Morgan keep their work *durable*, *visible*, and *coordinated* across parallel sessions. Five rules, organized by-rule with their underlying concerns mapped at the front.

This is not a code-review gate, not a PR-creation requirement, not a change to git worktree mechanics or mailbox semantics. It's a discipline doc about how work is captured so it isn't invisible.

## The three concerns

Every rule below addresses one or more of:

| Concern | What it means | Failure mode it prevents |
|---|---|---|
| **Durability** | Work exists on `origin/main` (or a pushed branch) by end of session | Lost work if a local checkout is damaged; "invisible work" patterns (CLAUDE.md anti-pattern) |
| **Visibility** | Other agents can see what you've done and where you are | Docs digging in worktrees this morning to find session logs; agents starting work duplicating others' in-flight work |
| **Coordination** | Parallel-write surfaces (manifests, registry) don't fight each other | The MANIFEST conflict cascades CXO documented Saturday; race conditions on mailbox writes |

Concern-to-rule map:

- **Rule 1** (worktree per substantive session) → durability + visibility
- **Rule 2** (commit-before-close) → durability
- **Rule 3** (atomic mailbox writes) → coordination
- **Rule 4** (branch/worktree registry) → visibility + coordination
- **Rule 5** (designated merge-keeper) → durability + coordination

---

## Rule 1 — Worktree per agent for any non-trivial session

**Status: ADOPTED**

Any agent doing substantive work in a Code session uses or creates a worktree on its own `claude/*` branch rather than working directly on `main`. CLAUDE.md's existing worktree section is mandatory rather than recommended for this case.

### Tiny exceptions that may stay on `main`

- Pure mailbox routing (read-only or move-only, no new memos created)
- Dispatch / housekeeping work owned by one role and predictable in shape
- HOST/PA coordination work that is deliberately on `main` for reach
- Mail commits during a feature-branch session (per Mailbox Discipline below — mail writes always commit to `main`)

Everything substantive — memos, code, session logs that produce new artifacts — goes through a worktree.

### Rationale

`main` operating as a working surface without commit discipline is the recurring root cause behind several Apr 22 / Apr 26 / Apr 28 friction events. The fix is structural: substantive work happens on a branch, gets committed there, gets merged to `main` deliberately.

### Implementation

CLAUDE.md's existing "Git Worktrees" section describes the mechanism. No code or hook required for the rule itself; behavior change is what matters.

### Worktree-path consistency convention (CIO standing-items 12i, May 11)

**Convention, not enforced rule.** When you create a worktree, ALL writes for that session — including writes that would normally go on `main` (mailbox writes, tracker updates, backlog edits) — must originate from the worktree's checkout path, not from the main repo path. Otherwise edits made via the main checkout to files the worktree branch has cached can land in a different physical copy than the worktree's view, and stay uncommitted indefinitely until the next session catches the divergence.

**Provenance**: May 10–11 CIO session. CIO worked from worktree `adoring-jackson-c2bc12` but edited `dev/active/cio-innovation-backlog.md` + `dev/active/cio-standing-items.md` via the main checkout path. The worktree showed clean while main showed modified; the edits stayed uncommitted overnight until CIO's session resume caught it via cross-tree diff. ~30 min triage cost; recovery clean (commit on main from main checkout). Filed as anti-pattern P-17 (working-tree-path fragmentation) and as fourth child of Pattern-068 (Silent State Mutation in Shared Working Tree).

**How to apply**:
- All session writes happen from the worktree's checkout path (`/path/to/repo-{branch-suffix}`), not from the main checkout.
- If a write needs to land on `main` (e.g., mailbox mail), do the standard Rule 3 dance from the *worktree's* checkout: stash → checkout main → write+commit+push → switch back to your branch.
- At session resume, run `git status` from both the worktree path AND the main checkout path. Any divergence is the P-17 shape; commit from wherever the edit physically lives.
- The discipline applies only when you've adopted a worktree for the session. Sessions entirely on `main` don't have this surface.

**Why not a rule**: enforcement would require either (a) blocking edits to files the worktree branch has cached, or (b) cross-tree mirroring at write time — both more expensive than the cost of the convention. The cost-benefit favors discipline at the human/agent layer.

---

## Rule 2 — Commit-before-close, no exceptions

**Status: ADOPTED — codified in CLAUDE.md; SessionStop hook IN FLIGHT (Lead Dev)**

Every Code session ends with a clean working tree on its branch. Either:

- All work is committed and pushed, OR
- Outstanding work is *explicitly listed* in the session log as "deferred — not committed because [reason]" with a note about who picks it up next.

A session log that ends with "[end of session]" while `git status` shows modified or untracked files in `services/`, `mailboxes/`, `dev/active/`, or `docs/` is a process failure (analogous to CLAUDE.md's existing log-abandonment anti-pattern).

### Per-memo commit-and-push norm (CXO Apr 26)

After each individual memo write (or batched memo + CC mirrors + sent mirror + paired triage moves), run `git add` + `git commit` + `git push`. ~30s overhead per memo. Eliminates asymmetric-visibility windows where one agent sees a memo before another. Codified in CLAUDE.md.

### Enforcement

- Codified in CLAUDE.md "Mailbox Discipline" section (Apr 26).
- **SessionStop hook**: Lead Dev confirmed feasible, ~50 lines, ~30 min; warns if untracked/modified state exists at session close. Status: IN FLIGHT.

### Rationale

PM's Apr 28 framing: "I don't want any agent wrapping up their day without pushing all their work to origin main, since that's where some of the agents look to for their source of truth." The morning's "Docs had to look in worktrees to get all the latest session logs" is the recurring instance.

---

## Rule 3 — Atomic mailbox writes (toward regenerate-from-filesystem)

**Status: PARTIAL — mailbox-on-main hook ADOPTED; deliver-mail (b) IN FLIGHT (Lead Dev sizing)**

Direct edits to `mailboxes/{role}/inbox/MANIFEST.md` from multiple branches produce conflicts because manifests are append-only. Two paths considered; consensus on (b) as the destination:

- **(a)** Route all mail writes through the `deliver-mail` skill which handles atomic manifest update. Ships fast but the underlying race remains if two agents call the skill near-simultaneously.
- **(b)** Manifest becomes a *derivative* artifact, regenerated from the filesystem at session start (and optionally on a hook). Files dropped in `inbox/` are authoritative; the manifest just describes them. Eliminates the race entirely.

### What's adopted

- **Mailbox-on-main hook** (`.claude/hooks/check-branch.sh`): blocks any commit touching `mailboxes/` from a non-`main` branch. Codified in CLAUDE.md "Mailbox Discipline" section.
- **Per-memo commit-and-push norm**: see Rule 2.

### What's adopted (cont.)

- **`deliver-mail` (b1) regenerate-from-filesystem**: ADOPTED — `scripts/regenerate-mailbox-manifests.py` (Lead Dev commit `4df51302`, Apr 28). Frontmatter-parsing per PA preference; SessionStart hook runs regen for the current role's manifest each session. Bridge skipped per Lead Dev judgment.

### Rationale

The race is the root failure mode; routing-through-a-skill papered over it. Inversion of authority (filesystem authoritative; manifest derivative) matches actual semantics — the files are what got delivered.

### Tactical note — staging-area race when multiple agents are on `main`

**Convention, not enforced rule** (HOST May 10): when on `main` with other agents potentially active, the `.git/index` (staging area) is a shared mutable resource. Concurrent operations from other agents can silently re-write the index between your `git add` and your `git commit`. Symptom: `nothing added to commit, untracked files present` after a `git add` that verbose-output confirmed succeeded.

**Mitigation pattern**: chain `git add <paths> && git status --short && git commit -m "..."` in a **single shell invocation** when staging on `main`. The `&&` chain forces atomicity from git's perspective — the index is queried within the same shell process that wrote it, with no window for another agent's concurrent ops to intervene.

**Recovery pattern** when the failure fires: re-stage explicitly, verify with `git status --short`, retry commit. Error signature is unambiguous (`nothing added to commit`); no silent corruption risk.

**Not a rule** because: per-operation verification cost compounds; failure recovery is mechanical; the shared-`main` working tree is by-design for mailbox visibility (Rule 3 above). The convention is tactical for cases where you notice it; the rule-set is intentionally not expanded to enforce it.

**Provenance**: May 10 PPM-stranded-commits incident (Code agent special-assignment session). Related findings: branch-drift (named-state mutation, May 7 + May 9 memory chain) and residue-drift (cross-agent residue accumulation, May 9-10 PreCompact-hook first-incident debrief). Common parent shape: shared working tree + concurrent agent activity → silent mutation of stable-looking state. Named-state mutations (branch HEAD) get rule-enforcement; transient-state mutations (index) get convention.

### Tactical note — pre-existing index state when committing on `main`

**Convention, not enforced rule** (Docs May 15): when on `main` with other agents potentially active, the `.git/index` may already contain pre-staged files from other agents/sessions/hooks before you start. Symptom: your "one-file commit" lands with N other files in `git show --stat`.

**Mitigation pattern**: `git reset HEAD` as the first command in any commit chain on `main`. Idempotent + cheap; clears the index of anything not yet committed. Then `git add <explicit paths>` only what you intend.

**Verification**: when `git diff --cached --name-only` runs after staging, **count lines in the full output** before commit. If you staged 2 paths, expect exactly 2 lines. Anything more = residue → reconcile before commit.

**Distinct from the staging-area race above**: that addresses state changes *during* the chain (concurrent ops re-writing the index after your `git add`). This addresses state that was *already there* before the chain started. Both stack.

**Recovery if residue commit already landed**: don't amend (changes are real even if attribution is off). Note in session log with affected commit hash + what got swept; flag to PM if destructive; move on otherwise. `git revert` only if the residue caused harm.

**Provenance**: May 12 incident (Docs `ecec86fd` PA cwd-drift outreach memo swept 2 deleted `data/learning/*.json` files); May 14 incident (Docs `f67a08af` May 14 omnibus swept 8 exec inbox→read mail renames). Common failure mode: `git diff --cached --name-only` output DID list the extra files in each case; reading stopped at the first line. The discipline is **reset → stage → diff → READ FULL OUTPUT → commit**.

---

## Rule 4 — Branch/worktree registry

**Status: ADOPTED in shape; auto-population script IN FLIGHT**

A single canonical view of "what agents are running, what branch each is on, when they last committed." Owner: **PA, hosted as auto-populated artifact** (per HOST + PA convergence Apr 26–27).

### Location

- Standing operational doc: `docs/internal/operations/agent-worktree-registry.md` (human-readable; refreshed with brief commentary).
- Optional: machine-written sibling at `dev/state/agent-worktree-registry.md` (auto-regenerated, no commentary). Implementation choice deferred to Lead Dev.

### Data sources (all programmatically readable)

- Worktree paths and branches: `git worktree list --porcelain`
- Last commit per branch: `git log -1 --format='%H %ai' <branch>`
- Last session log per role: `ls -t dev/YYYY/MM/DD/*-{role}-*-log.md` plus `dev/active/`
- Uncommitted-state status: `git -C <worktree> status --porcelain`

The "Idle, work uncommitted" status from CXO's example table is itself derivable: a worktree's branch hasn't been pushed in N hours AND `git status` is non-empty.

### HOST's role

Read the registry at session start and at role-health-check time. Surface staleness signals (e.g., an agent's worktree hasn't moved in N days while their session logs show activity = uncommitted work or registry decay). HOST monitors discipline; HOST does not produce or maintain the registry.

### Rationale

Auto-population eliminates the upkeep tax. Manual upkeep adds friction, decay, and a coordination tax with no payoff if the data is programmatically readable (HOST's framing).

---

## Rule 5 — Designated merge-keeper

**Status: ADOPTED — Docs is merge-keeper (PM-confirmed Apr 27); merge-keeper-sweep.sh IN FLIGHT (Lead Dev sizing)**

A single role responsible for picking up pushed `claude/*` branches, reviewing commits at headline level, merging to `main`, pushing `origin/main`, and resolving manifest conflicts. **Merge-keeper is a state janitor, not a code reviewer.** The committing agent owns correctness; the merge-keeper owns durability.

### Owner: Docs (weak-favor-converged across CXO, HOST, Exec, Docs, PA, PM)

Docs already touches the broadest cross-section of the tree (omnibus logs, briefings, navigation, methodology docs) and has demonstrated the discipline shape (omnibus gap remediation, HOSR→HOST rename sweep, the Apr 22 cross-reference gate addition). Janitorial-with-care is part of how Docs operates.

Lead Dev was considered and is the wrong fit: deep git mechanics knowledge, but already loaded with implementation work and has conflict-of-interest on Lead's own branches. Better to have Lead Dev write the SessionStop hook (Rule 2) and the conflict-resolution runbook than to *be* the merge-keeper.

### Cadence

- **Active migration weeks** (current): EOD sweep, anchored to PM's standing nudge round.
- **Normal sprint weeks**: 2× weekly (mid-week + Friday) plus on-demand if PA flags a branch is blocking someone.
- **Same-day urgency**: handled ad-hoc when surfaced.

### Protocol (from Docs's reply)

```
1. git fetch origin
2. List remote claude/* branches with commits not on main
3. For each branch with unmerged commits:
   a. Identify owner from commit author and recent session log
   b. Check session-log status (wrapped vs. active)
   c. Skim commits at headline level — verify no large blobs / .env / .DS_Store / secrets
   d. If wrapped: git merge --no-ff origin/claude/{branch} → push
   e. Resolve manifest conflicts using union-by-timestamp (interleave rows)
4. Archive any session logs in dev/active/ to dated subdirs
5. Log the sweep in dev/active/merge-keeper-{YYYY-MM-DD}.md
```

### Automation

- **`scripts/merge-keeper-sweep.py`** (Lead Dev commit `f63c2acf`, Apr 28): ADOPTED. Python; simple-heuristic version (≥24h commit age = wrapped; auto-merge if no conflict / no `.env` / no `.DS_Store` / no large blobs; escalate everything else to `dev/active/merge-keeper-{date}.md`). Default `--dry-run`; `--apply` actually merges. Drops Docs's manual touch from ~30 min/day during active migration weeks to ~5 min/day.

### HOST's role

Watch the merge-keeper, not perform the merges. Track merge-queue depth, branches stale on origin without merge, conflicts piling up. If the merge-keeper is unhealthy or absent, surface as role-health signal.

### Designation source

CoS designation, not bandwidth-emergent. Bandwidth-emergent gives us the Saturday/Sunday Apr 25–26 situation (work sat for 10+ hours because no one was the explicit owner). Standing designation with named backup is the durable shape. Backup: PA.

---

## Cross-cutting: branch-or-anchor (CT v2.3)

A related methodology rule landed Apr 27 (CXO embedded in Colleague Test v2.3): *at the moment of authoring a parallel extension of a canonical document, either branch explicitly (fork and acknowledge divergence) or anchor explicitly (cite criterion by content, not just by label).* CIO is filing as a methodology-core entry. Pattern-063 ("Parallel-Authoring Drift") is the named failure mode this rule addresses.

This is not a branch-discipline rule per se — it's about authoring shared instruments — but it's adjacent enough to warrant cross-reference here.

---

## Implementation status summary

| Item | Status | Owner |
|---|---|---|
| Rule 1 — worktree per substantive session | ADOPTED (CLAUDE.md) | All agents |
| Rule 2 — commit-before-close | ADOPTED (CLAUDE.md); SessionStop hook IN FLIGHT | Lead Dev for hook |
| Rule 2 — per-memo commit-and-push norm | ADOPTED (CLAUDE.md) | All agents |
| Rule 3 — mailbox-on-main hook | ADOPTED (`check-branch.sh`) | Docs (own) |
| Rule 3 — `deliver-mail` (b1) regenerate-from-filesystem | ADOPTED (commit `4df51302`) | Lead Dev |
| Rule 4 — branch/worktree registry | ADOPTED in shape; auto-pop IN FLIGHT | PA hosts; Lead Dev for script |
| Rule 5 — Docs as merge-keeper | ADOPTED | Docs |
| Rule 5 — `merge-keeper-sweep.py` automation | ADOPTED (commit `f63c2acf`) | Lead Dev |
| HOST monitoring discipline | ADOPTED in shape | HOST |
| Branch-or-anchor (CT v2.3) cross-reference | ADOPTED | CXO authored; CIO methodology-core entry |

---

## Open implementation questions deferred to follow-up

These are real but don't block adoption of the rules above:

- **Rule 2 SessionStop hook**: language (shell vs. Python), hook trigger granularity, false-positive shape. Lead Dev to design.
- **Rule 3 (b) regenerate-from-filesystem**: frontmatter-parsing (PA preference, b1) vs. sidecar files (b2) vs. terse auto-generation (b3); whether to ship (a) atomic-via-skill as bridge based on (b) sizing. Lead Dev calls.
- **Rule 4 registry shape**: human-readable + machine-written sibling, or single human-readable doc with auto-refresh. Implementation detail; defer to first iteration.
- **Rule 5 sweep automation**: shell vs. Python; how to escalate non-trivial cases. Lead Dev calls.

---

## Why these rules and not others

Three things are explicitly *not* part of this synthesis:

1. **Code-review gates.** Branches don't need PR review to merge to `main`; that's a different discipline question with different tradeoffs and the project hasn't been doing it. This proposal is about durability and visibility, not quality gating.
2. **Changes to git worktree mechanism.** CLAUDE.md's existing description is fine. The proposal is about *when* to use worktrees, not *how* the mechanism works.
3. **Changes to mailbox semantics.** Mailbox structure works; the protocol around updating shared MANIFESTs is the friction.

---

## Methodology cross-reference

HOST's reply flagged that this discipline doc is one instance of a broader meta-pattern: *implicit-protocol-becomes-explicit-protocol* — the same pattern that produced the Apr 19 filename-standard memo, the Apr 22 first-day blocker memo, and the Apr 26 branch-discipline observations. That meta-pattern lives at a different altitude than these operational rules and is being routed to CIO as a separate methodology-core candidate, paired with the branch-or-anchor (CT v2.3) entry. This doc is the operational synthesis; that one will be the methodological synthesis.

---

## Review process

- **Comment window**: same-day on Tue 2026-04-28; close at EOD or earlier if comments are minimal.
- **Reviewers**: cohort that contributed inputs (CXO, Lead Dev, PPM, Exec, Docs, HOST) + PM.
- **Publication**: Docs publishes v1.0 final to this path once cohort + PM concurrence is reached.
- **CLAUDE.md**: updated to point to this doc as the canonical statement; Mailbox Discipline section becomes a 60-second summary with link.

---

— PA, 2026-04-28 (synthesis-of-record)
