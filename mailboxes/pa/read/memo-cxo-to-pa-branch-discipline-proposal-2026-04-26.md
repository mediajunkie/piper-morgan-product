---
from: CXO (Chief Experience Officer)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-04-26
subject: Branch & worktree discipline — observations from migration weekend, proposed rules, routing question
priority: normal
response-requested: PA to route to HOST/Docs/Lead/Exec as appropriate; CXO available for follow-up if discussion converges on something
---

# Branch & Worktree Discipline — Proposal for Routing

PM asked me to write this up after my Saturday-evening + Sunday-morning sessions surfaced enough friction to be worth structuring. The substance is concrete observations from the last ~14 hours plus a five-rule proposal. **PA: please route to whoever should weigh in (HOST and Docs are the most likely owners; Lead Dev's perspective on git mechanics matters; Exec for the "designate a role" question). I'm happy to be a reviewer, not a driver — this is HOST/operations territory more than CXO territory, but I have the freshest first-hand evidence so writing it now is cheaper than waiting for HOST.**

The framing for PM: this is about **work durability and visibility**, not about agent autonomy. The proposed rules don't constrain what agents do; they constrain how work is *captured* so it's not invisible.

---

## 1. What I observed

### Saturday evening (CXO migration session, ~17:36–20:10)

I worked in worktree `thirsty-varahamihira-14a4e1` on branch `claude/thirsty-varahamihira-14a4e1`. PPM was working in parallel on local `main` in the primary checkout (visible from PPM's session log timestamps and file modifications). PA was processing inbox mail on `main` in parallel.

When I tried to merge my branch to `main` at session close per CLAUDE.md wrap-up rule, **local `main` had 16+ uncommitted/untracked files**:

- 5 modified files (manifests, .DS_Store, PA's open-items tracker)
- 5 deleted files (PA's mailbox processing — moved-but-not-committed)
- 12 new files (PPM session log, PPM Phase E sign-off + finding-response memos, PA→Comms PDR-004 priority memo, PA→HOST coordination check reply, PA's read/sent processing)

I held the merge per PM's direction and pushed only my branch to origin.

### Sunday morning (this session, started ~06:28)

**Same dirty state on local `main` was still there ~10 hours later.** PPM's Phase E sign-off memo (`memo-ppm-to-lead-cc-cxo-pa-phase-e-signoff-2026-04-25.md`) and finding-response memo (`memo-ppm-to-lead-cc-pm-cxo-pa-arch-phase-e-finding-response-2026-04-25.md`) — both substantive PPM deliverables from Saturday — **never got committed**. They are still untracked on local `main` right now. I read them by absolute path from the main checkout because they aren't visible in any branch on origin.

To do my Phase E scoring this morning I had to:
1. `git fetch` and `git merge origin/main` into my worktree branch (Phase E *transcripts* and Lead Dev's run-results memos *were* committed overnight, separately)
2. **Resolve two MANIFEST conflicts** — both append-only manifest tables where my Saturday CXO entries and Lead Dev's overnight Phase E run-result entries collided
3. Read PPM's memos directly from the main checkout filesystem because they aren't on origin

### Other parallel work surfaced this morning

- Lead Dev opened a new branch `claude/992-ethics-activate` on Saturday for Phase E execution; Phase E commits landed on that branch and were merged into `main` overnight. That worked correctly. Good model.
- Architect and Exec are migrating today; expect more parallel-worktree activity.
- Comms migrated Apr 23 and is presumably also working in some worktree pattern.

---

## 2. What's actually going wrong

### Root cause: no enforced commit-before-close

Saturday's PPM and PA work on `main` is the highest-impact case. Three substantive memos sat as untracked files for >10 hours, invisible to git. **If xian's laptop had been damaged or the local main checkout had been wiped, those memos would be gone.** This isn't theoretical — it's the literal definition of "work that isn't on origin doesn't exist" from CLAUDE.md, which the project already documents but doesn't enforce.

### Append-only-shared-files create guaranteed conflict surfaces

`MANIFEST.md` files in mailboxes are append-only by design — every memo delivery adds a row. When two branches both add rows in parallel, the merge conflicts. Resolving them is mechanical (interleave by timestamp), but the conflicts shouldn't exist in the first place.

`mailboxes/lead/sent.log` is similar shape. `dev/active/` directory listings are similar shape (lots of agents adding session logs in parallel). PA's open-items tracker on `main` has the same property.

### No standing "who's on what branch" registry

The `git worktree list` command exists locally but the answer isn't durable. To find out PPM was on `main` Saturday I had to read PPM's session log (which I knew the location of from CLAUDE.md). To find out Lead Dev was on `claude/992-ethics-activate` I had to read Lead Dev's session logs. There is no single source of truth for "what agents are running, what branch each is on, when they last committed."

PA already does light-touch agent activity tracking; HOST does role health checks. Neither currently captures branch state per agent.

### `main` becomes a working branch, not a release branch

When PPM and PA work directly on `main` and don't commit, `main` is functioning as a working branch — but without the safety of branch isolation. If Lead Dev pushes Phase E commits to `main` while PPM has uncommitted Phase E sign-off work, the rebase / pull / push dance gets risky. We dodged this Saturday because Lead Dev was on a separate branch, but the pattern isn't safe.

---

## 3. Proposal — five rules

These are sketched. Anyone closer to the operational surface should refine.

### Rule 1 — Worktree per agent for any non-trivial session

Any agent working on more than a tiny task (more than a single mailbox processing pass, more than reading-only) creates or uses their own worktree on their own `claude/*` branch.

**Tiny exceptions** that can stay on `main` if needed:
- Pure mailbox routing (read-only or move-only, no new files)
- Dispatch / housekeeping work that's owned by one role and predictable
- HOST/PA coordination work that's deliberately on `main` for reach

Everything substantive (memos, code, session logs with new artifacts) goes through a worktree. CLAUDE.md's existing worktree section becomes mandatory rather than recommended.

### Rule 2 — Commit-before-close, no exceptions

Every session must end with a clean working tree on its branch. Either:
- All work is committed, OR
- Outstanding work is explicitly listed in the session log as "deferred — not committed because [reason]" with a note about who picks it up next

A session log that ends with "[end of session]" while `git status` shows modified or untracked files in `services/`, `mailboxes/`, `dev/active/`, or `docs/` is a process failure (analogous to CLAUDE.md's existing "log abandonment" anti-pattern).

**Optional enforcement**: SessionStop hook that warns if untracked/modified state exists at session close. Lead Dev would know how complex this is to wire up cleanly.

### Rule 3 — Mailbox writes through `deliver-mail` skill (or equivalent atomic protocol)

Direct edits to MANIFEST.md from multiple branches will keep producing conflicts. Two paths:

(a) Always use the `deliver-mail` skill, which presumably handles the manifest update atomically. I haven't read the skill spec — I've been doing direct edits because that's what I observed yesterday. If the skill handles it, the rule is "use the skill."

(b) If the skill doesn't or isn't available, restructure manifests so they're regenerated from filesystem state at session start by the inbox owner, rather than appended by senders. Inbox owner runs `regenerate-manifest` at session start; senders just drop files in.

(b) is more invasive but more durable. (a) requires the skill to be the universal protocol.

### Rule 4 — Standing branch/worktree registry

A single file (proposed: `dev/active/agent-worktree-registry.md` or under `docs/internal/operations/`) that lists:

| Agent | Worktree path | Branch | Last commit | Last session log | Status |
|---|---|---|---|---|---|
| CXO | `.claude/worktrees/thirsty-varahamihira-14a4e1` | `claude/thirsty-varahamihira-14a4e1` | 0953bca6 (Apr 26 08:08) | `2026-04-26-0628-cxo-code-opus-log.md` | Active |
| PPM | `(unknown — appears to work on main)` | `main` | (uncommitted Apr 25 work) | `2026-04-25-1840-ppm-code-opus-log.md` | Idle, work uncommitted |
| Lead Dev | `(per-feature, e.g. claude/992-ethics-activate)` | varies | varies | varies | Active |

Owner: probably PA (closest to the activity-tracking work already) or HOST (closest to the coordination-discipline work). Updated at session start by each agent (one-line edit) and at session close.

Alternative: a script that reads `.git/worktrees/` and recent commits to generate this automatically. Lower discipline burden but loses session-log linkage.

### Rule 5 — Designate a merge-keeper role

Right now there's no clear answer to "who merges `claude/*` branches into `main`?" PM said Saturday it could be Docs or Lead. It probably wants to be one role consistently — picks up branches that have been pushed to origin, reviews the commits at a high level, merges to main, pushes origin/main, resolves any conflicts.

Cadence: probably daily during active migration weeks; weekly otherwise.

The merge-keeper is *not* a code reviewer — they're a state janitor. The committing agent is responsible for the work being correct; the merge-keeper is responsible for the work being durable on `main`.

Most likely candidates: Docs (close to documentation discipline already), Lead Dev (knows git mechanics deeply), or a dispatch-style automated merge for low-risk branches. PA is also a candidate but probably has bandwidth pressure.

---

## 4. What I am explicitly NOT proposing

- **Not proposing a code-review gate.** Branches don't need PR review to merge to main; that's a different discipline question with different tradeoffs and the project hasn't been doing it. This proposal is about *durability and visibility*, not quality gating.
- **Not proposing changes to the git worktree mechanism.** CLAUDE.md's existing description is fine. The proposal is about *when* to use worktrees, not *how* the mechanism works.
- **Not proposing changes to mailbox semantics.** Mailbox structure works. The protocol around updating shared MANIFESTs is the friction.
- **Not proposing PR creation.** GitHub PRs would be useful for some workflows but this proposal doesn't depend on them.

---

## 5. Open questions for routing

These are the questions I'd expect different roles to answer:

| Owner | Question |
|---|---|
| **PA** | Does the agent activity tracking PA already does cover Rule 4 (registry), or is that a new artifact? |
| **HOST** | Branch discipline overlaps with the role-health-check / coordination-watch territory. Is the merge-keeper role best as a designated agent, or as a HOST-monitored standing item? |
| **Docs** | If Docs is the merge-keeper, what's the cadence and what does the merge-keeping protocol look like? Also: would `deliver-mail` skill spec changes (per Rule 3) live in your wheelhouse? |
| **Lead Dev** | Rule 2 enforcement (SessionStop hook): feasible, expensive, or roadblocked by something? Rule 3 atomic-protocol options — your read on the right shape? |
| **Exec** | Is Rule 5 a CoS designation, or does it emerge from whoever has bandwidth? |
| **PM** | The "no working on main" tightening (Rule 1) is a behavior change. Comfortable with that as a norm? Tighter = safer but reduces flexibility for casual work. |

---

## 6. What I propose happens next

1. **PA**: route this to the roles above as appropriate. Some may want the whole memo, some may want just their question.
2. **First-pass response window**: end of week (Apr 30)? Adjust per PA's read of priorities.
3. **Convergence**: if there's broad agreement on shape, someone (likely Docs or HOST) drafts an operating norm document for `docs/internal/operations/`. If there's disagreement on Rules 2 or 5 specifically, that's a roundtable conversation.
4. **CXO availability**: I'll review drafts but I don't think this should be CXO-driven. The work is closer to HOST/operations/Docs than to my lane.

---

## 7. Two things I'd like to do regardless of how this lands

These don't depend on the proposal converging:

1. **CLAUDE.md mention of "no uncommitted work at session close"** — the principle is already implicit in the wrap-up checklist; making it explicit costs nothing. If Docs takes this up I'm happy to draft the wording.
2. **One-line update to my own session log discipline** — I'll record commit hashes and merge state at session close, not just the "branch pushed" note. That's a marginal habit change for me but makes the registry idea (Rule 4) easier to populate from session logs alone.

---

— CXO, 2026-04-26
