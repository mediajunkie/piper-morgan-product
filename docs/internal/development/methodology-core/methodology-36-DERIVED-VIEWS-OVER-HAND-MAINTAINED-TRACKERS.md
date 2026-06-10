# Mechanism Beats Vigilance — Promote Recurring Vigilance-Disciplines to Mechanisms

*(Originating instance + file slug: Derived Views Over Hand-Maintained Trackers, 2026-05-24. Generalized beyond trackers 2026-05-28 per PM steer.)*

## Overview

**Mechanism Beats Vigilance** names the principle that any discipline relying on sustained human/agent attention is only as reliable as the attention applied to it — and that attention-per-action falls as autonomous and multi-agent load rises. When a discipline recurs as lapses, the recurrence is not a motivation failure to be fixed with "be more disciplined"; it is the evidence that discipline is the *wrong layer*. The structural fix is to **promote the vigilance discipline to a mechanism** that makes the lapse impossible, self-correcting, or loudly detected.

Vigilance failures come in two classes, distinguished by *when* the failure happens:

- **Class 1 — read-time staleness** (hand-maintained trackers): state that must be kept current by attention goes stale; consulting it at the moment of need surfaces *past* state, not current state. **Mechanism: a derived view over a substrate of record** — the view is computed at read time, so staleness is impossible. (This is the originating tracker instance; see Class 1 below.)
- **Class 2 — write-time / action-time omission** (operational disciplines): a "do X every time you do Y" rule depends on remembering X at each action; under load the prefix/pause/path-choice is forgotten. **Mechanism: a structural guard** — a hook, a single-command chain, or a runtime behavior that removes the per-action remembering. (See Class 2 below — the duty-cycle autonomous-scale evidence.)

The principle applies cross-cohort: any discipline — tracker or operational rule — that has recurred as lapses, especially with recurrence rising under autonomous scale, is a candidate for promotion to a mechanism.

## The promotion diagnostic — recurrence-under-scale

The signal that tells you a discipline should be promoted from vigilance to mechanism:

1. **It recurs as lapses** — not once, but repeatedly, often by different agents (so it isn't one agent's carelessness).
2. **The recurrence-rate rises with autonomous / multi-agent load** — more actions per unit of human attention means each "remember to X" gets less attention, so the lapse frequency climbs exactly as the system scales. This is the decisive tell: a discipline that was *fine* at human-pace-with-review becomes a steady lapse-source under autonomous cadence.
3. **The lapse is mechanizable** — there exists a hook, chain, runtime behavior, or derived view that removes the per-action remembering.

When all three hold, "be more disciplined" is the wrong response — it re-applies the layer that's already failing. Promote instead. (PM directive, 2026-05-28: *"we are going to have to figure out why these lapses happen so frequently and improve the rule set or the hooks"* — the recurrence-under-scale frequency is itself the diagnostic.)

The promotion isn't always full elimination. Mechanisms sit on a ladder: **eliminate** (the lapse-state becomes impossible) > **self-correct** (the system catches and fixes it) > **loudly detect** (a hook/guard fires so the lapse can't pass silently). Even moving one rung — from silent-vigilance to loud-detection — is a promotion.

## Class 1 — read-time staleness → derived views over substrate

*(The originating instance. The general principle above was extracted from this case 2026-05-28.)*

### The shared-shape evidence (May 24, 2026)

Comms's process-improvement seed memo (`memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`) surfaced two visibility-loss incidents in one day. **Both incidents involved a tracker that should have caught the gap, and both trackers failed in the same way: hand-maintained ≠ current.**

- The orphan-drafts incident: `dev/active/comms-open-topics.md` listed *"10 drafted pieces... 2 unscheduled insights"* as of May 10 — but went stale until Docs surfaced the orphans on May 24
- The kickoff-move-to-read incident: session log Pending list should have carried the kickoff's downstream-artifact obligation — but multi-hour-session attention pressure left the obligation in volatile chat memory only

Comms's deeper framing: *"This isn't a personal-vigilance failure. It's a structural property of hand-maintained trackers. Vigilance fails. Mechanisms don't."*

That framing graduates the observation from "let's be more disciplined about the tracker" to a structural-fix-instead-of-discipline-fix candidate (PP-004 candidate; see below).

### The cohort's tracker inventory (partial)

Hand-maintained trackers in current cohort use:

- **Comms**: `dev/active/comms-open-topics.md` — narrative drafts + insights + Ship topics
- **HOST**: `mailboxes/host/sent/*-360-commitments-tracker-refresh-*.md` — 360 tracker (already partly derived via mailbox queries; periodic refresh memo is hand-maintained)
- **CIO**: `dev/active/cio-standing-items.md` — standing items (hand-maintained as of v0.5 — designed to persist across days)
- **CIO**: `dev/active/duty-cycle-escalations-cio.md` — PM attention items (hand-maintained)
- **CIO** (catalog): methodology catalog + pattern catalog — file-named-numbered substrate is durable; cross-referencing across patterns/methodologies is hand-maintained via Adjacent-Patterns sections
- **Lead Dev**: GitHub issues + checkbox state — GitHub itself is the substrate; checkbox state is hand-maintained (Pattern-067 instance)
- **Architect**: ADR/PDR registries — file-named-numbered substrate is durable; cross-referencing is hand-maintained
- **Session log Pending lists**: in-session work-tracking — hand-maintained, vulnerable to multi-hour attention pressure
- **Inbox MANIFESTs**: derived-index-over-inbox-folder — hand-maintained (Pattern-073 first-instance-at-derived-index-layer was this exact failure)

All vulnerable to the same failure shape: hand-maintained ≠ current.

### Why derived views are the structural fix

A derived view is **computed from a substrate at read time**. The substrate is the source of truth; the view is a query over it. Staleness becomes impossible because the view doesn't carry state between reads.

Concrete examples of refactor patterns:

- **Editorial calendar as substrate; drafted-but-unscheduled view as query**: comms-open-topics.md retires; the "what's drafted but unscheduled?" view is computed from a calendar query (status=drafted AND pubDate=null). Layer B of Comms's framework targets exactly this refactor.
- **Filesystem state as substrate; orphan-detection view as periodic reconciliation**: `docs/public/comms/drafts/` filesystem state ↔ calendar `draftPath` column reconciled periodically. Layer D in Comms's framework. This isn't *pure* derived (reconciliation has a job-shape) but it catches drift in either direction.
- **Inbox folder state as substrate; MANIFEST as derived view** — *now evidenced (2026-06-06), the clearest Class-1 exemplar*: MANIFEST autogeneration from `ls inbox/` + each memo's frontmatter `subject:`. **Failure evidence**: Web hit a lost-write near-miss (2026-06-06) — a few-second `Read`→`Write` race on a high-write shared MANIFEST nearly wiped 9 other agents' entries (the auto-mode classifier caught it). That race is *intrinsic to storing what should be derived*: every hand-maintained shared-state file is a write-contention risk by construction. Deriving gives **one writer** (the regen) → the contention class is eliminated, not mitigated. **Idempotency note**: a whole-state derive regen is naturally idempotent (concurrent regens converge), so a pre-push/post-commit regen hook can't race itself. **The discipline→mechanism progression** (a clean teaching case for this whole entry): the interim **"recipient owns their inbox MANIFEST"** rule (PM+Web, 2026-06-06) is the *vigilance* version — one-writer by discipline; **derive** is the *mechanism* version — one-writer automatically, the recipient's fire regenerating rather than hand-editing. Derive doesn't replace recipient-owns, it *automates* it. (Lead owns the design call; CIO weighed in recipient-owns-now → derive-later. Existing basis: `scripts/regenerate-mailbox-manifests.py` + the shipped `scripts/cohort-cycle-status.sh` precedent.) Supersedes the earlier "Pattern-073 first-instance / tooling-debt candidate" framing.
- **Mailbox state as substrate; 360 tracker as derived view**: HOST's tracker is partly already derived (mailbox queries); the refresh memo is the hand-maintained scar.

## Class 2 — write-time / action-time omission → structural guards

*(Generalized 2026-05-28 from the duty-cycle autonomous-rollout evidence. Class 2 is the action-time mirror of Class 1: where Class 1 fails at *read* time — stale state consulted — Class 2 fails at *write* time — a required step omitted at the moment of action.)*

### The autonomous-scale evidence (duty-cycle rollout, May 25–28, 2026)

The duty-cycle rollout was a natural experiment in the recurrence-under-scale diagnostic: a set of "do X every time you do Y" disciplines that were fine at human-pace-with-review became steady lapse-sources under autonomous cron cadence + multi-agent concurrency. Four instances, each on a different rung of the mechanism ladder:

| Vigilance discipline | The "remember to X" | Lapse evidence | Mechanism (rung) |
|---|---|---|---|
| **Rule 1 — cron-pause-during-WORK** | pause the cron before substantive work | re-fires slipped into mid-work idle gaps (Arch Fire-3; CIO Rule-2 lapses) | **CronDelete-FIRST** refinement closes the CronList→CronDelete race (self-correct); a fire-arriving-mid-work hook would be full elimination (Lead Dev lane) |
| **cd-prefix — Model-B worktree** | prefix every command with `cd <worktree>` (cwd resets between Bash calls) | friction #1 surfaced in CIO PoC-2 | **chain all git ops in ONE cd-prefixed command** — cwd holds within a chain, so the chain either has the `cd` or it doesn't; no mid-sequence drift (eliminate, at the per-chain level). Model A (launch-in-worktree) eliminates it at the substrate level — the session's cwd is the worktree, no prefix needed |
| **explicit-paths — mailbox commits** | never directory-level `git add` on `mailboxes/` | CIO Fire 8 swept a foreign agent's deletions | **`check-branch.sh` hook** blocks mailbox commits from non-main branches (loud-detect); explicit-paths-only discipline pairs with it. **Reinforcement** (Comms 2026-05-29): `git commit -m "…" -- <explicit paths>` commits ONLY named paths regardless of shared-index state — the same principle at the per-commit-invocation level, structurally preventing the sweep-up-other-agents'-staged-files failure. |
| **Rule 2 — PM-presence-pause** | pause the cron on PM message | lapsed ×2 (CIO) | **runtime idle-only-fire** already suppresses fires during spaced PM conversation → the vigilance step is removed entirely (eliminate, via runtime behavior). This is the Model-A relaxation: Rule 2 *can* drop because its failure mode is genuinely idle-suppressible |
| **Log-currency — session-log updates** | "update the log every 30 minutes" / remember-by-clock | the 30-min vigilance failed cohort-wide; the `log-maintenance-reminder` hook enforced the rule mechanically but the rule itself was wrong (clock-based); CIO test-case 2026-05-29 — committed the CLAUDE.md flip + Lead memo *without* paired log updates before catching it | **"log updates ride with the commit"** — event-based pairing in the same commit (eliminate, at the commit-event level): clocks lose track of when 30 minutes have passed; commits are unmissable events. PM-ratified 2026-05-29 ~15:05; CLAUDE.md flipped to event-based same day; hook being realigned by Lead Dev. Originating framing: Comms's process-tightening memo. |
| **Session-log accretion — dual-surface fire logging** (CIO 2026-06-09, PM-flagged) | log each fire to the SESSION log (durable), not only the cycle log (ephemeral) | session log silently displaced cohort-wide — Docs audit: 6 of 9 cycling roles, ~15 role-days (the methodology-41 founding instance); the displacement was *invisible from in-procedure* because the fire loop only referenced the cycle log | **`duty-cycle-tick` skill v1.5 Step-5 dual-surface** — the same step that writes the cycle-log entry now also writes the session-log one-line summary, so "cycle log full + session log empty" is impossible-by-construction (eliminate, at the procedure site). The **first production instance of Class-2 after the framing landed** — gives Class-2 a working reference implementation. The disease this cures is named at methodology-41 (mechanism-displaces-unreferenced-discipline); this row is its m-36 cure. |
| **Recurring-workflow routing — auto-issue ownership** (HOST 2026-06-08, PM-endorsed) | PM must notice + relay each recurring auto-generated GitHub issue to its actual owner (agents have no GH login; **GH doesn't notify agents** — mail is the cross-agent signal layer, GH is a passive artifact) | the `role-health-check` workflow auto-assigns its recurring issue to PM (`mediajunkie`), landing on PM **every cycle** — PM as default catch-of-last-resort (the #1178 instance) | **two-half structural guard**: (1) the workflow body **names its owner + a routing reminder** (the assignment-to-PM is only because agents have no GH login); (2) the **owner's duty cycle polls its label** (`gh issue list --label {owner} --state open`) as a standing cycle responsibility — the agent-reachable channel (the owner's own cycle) **replaces** the GH-assignment that never reaches them. Eliminates PM-as-default-catch for recurring *owned* work. This is the **literal mechanism for the m-39 PM-as-catch relocation** (a recurring, owned, routable piece of work was routing to PM only because the workflow had no other way to reach an agent). HOST exemplar: `role-health-check.yml` + HOST cycle-poll, 2026-06-08; PM endorsed for *all* recurring workflows. **CIO disposition (2026-06-08): m-36 Class-2 instance + cohort-norm — NOT a standalone methodology entry** (it's an application of m-36 + the m-39 PM-as-catch watch + the mail-as-signal-layer norm; a new entry would be corpus bloat). Cohort-norm statement: *"every recurring auto-issue workflow names its owner; the owner's cycle polls its label."* |

### The Rule-1-vs-Rule-2 split is the diagnostic in miniature

Rule 1 and Rule 2 look like the same discipline ("pause the cron") but promote differently, and *why* is instructive. Rule 2's failure mode (a fire during PM conversation) is idle-suppressible — PM messages are spaced, so the runtime already prevents it; the vigilance step is pure redundancy and drops. Rule 1's failure mode (a re-fire during the agent's own multi-tool-call work) is **not** idle-suppressible — the REPL is briefly idle between every tool call, so a fire slips into that gap regardless of working tree. Same surface discipline, opposite promotion verdicts, because the *failure timing* differs. **The lesson: promote per failure-mode, not per surface-rule** — two rules that read alike can need opposite mechanisms.

### Why derived views (Class 1) and structural guards (Class 2) are the same principle

Both replace "an agent remembering to do the right thing" with "a structure that makes the wrong thing impossible or loud." Class 1 moves the work to *read* time (the view is computed, never stale); Class 2 moves the work into the *action itself* (the chain, hook, or runtime behavior carries the guarantee). The unifying move is the same: **find the substrate or the structural choke-point, and let it carry the discipline the agent was carrying by attention.**

### Why this is methodology-corpus, not Pattern catalog

Pattern catalog entries describe **architectural / surface failure modes** (e.g., Pattern-074 visibility-loss-after-premature-retirement; Pattern-067 issue-body-reality-mismatch). They live in `docs/internal/architecture/current/patterns/`.

Derived Views Over Hand-Maintained Trackers is **a discipline-shape principle** — about how cohort tracking *should be authored* to avoid the trackers-go-stale failure mode. It belongs in the methodology corpus (discipline-of-rule-authoring) alongside methodology-35 (Asymmetric Discipline).

The instances of trackers-gone-stale (Pattern-074 instances; Pattern-073 inbox-MANIFEST instance; methodology-35 worktree-proliferation instance) are pattern-shaped; the meta-pattern about choosing derived-views-over-hand-maintained is the methodology.

## Adoption signal — operating as a working cohort frame (2026-06-09)

m-36 is being *invoked* across roles to classify and dispose of fresh findings, not just cited — the signal that a methodology entry has become a working cohort frame rather than a filed observation. Recent surfacings in a 48-hour window: the MANIFEST write-contention near-miss → Class-1 (recipient-owns→derive, 2026-06-08); the INDEX.md staleness → Class-1 again (2026-06-09); the recurring-workflow-routing adoption → Class-2 (HOST, PM-endorsed); and the session-log dual-surface fix → Class-2, the first production reference implementation after the framing landed (2026-06-09). The two-class vocabulary (read-time-staleness / action-time-omission) is doing classification work in real dispositions — agents reach for "is this Class-1 or Class-2?" when deciding a fix shape. Promotion-progress note (no status flip yet — Class-2's PP-004 accumulation still holds for one more confirming case per the section below): the *framing's* cohort-adoption is ahead of the PP-004 instance count, which is itself the methodology-29 successful-imitation signal.

## Application

### Recognition cue

A discipline is a candidate for promotion-to-mechanism if any of:

- It has recurred as lapses — especially by *different* agents, and especially with recurrence rising under autonomous/multi-agent load (the recurrence-under-scale diagnostic)
- **Class 1 tells**: a tracker duplicates information already in a structural substrate (filesystem, mailbox, calendar, GitHub issues); requires manual cross-referencing that could be machine-queried; its maintenance falls to the back of the queue in high-load sessions
- **Class 2 tells**: a rule is phrased "remember to X every time you Y"; the X is a prefix/pause/path-choice/cleanup attached to a frequent action; the omission is silent (nothing fires when X is skipped)

### Refactor framework

When refactoring a hand-maintained tracker toward a derived view:

1. **Identify the substrate of record** (the source-of-truth structural surface)
2. **Define the view as a query** (what question the tracker answered; what query computes the answer from the substrate)
3. **Build the query mechanism** (script, skill, hook — whatever generates the view on demand)
4. **Retire the hand-maintained tracker** OR rename it to "snapshot-as-of-{date}" if the historical view has value

Comms's Layers A–D framework (preventive + detective combination) is a clean template:

- **A**: prevent the failure at creation (mechanism that makes the failure-state impossible)
- **B**: retire the hand-maintained tracker; derive from substrate
- **C**: require the inventory query as first step in planning sessions
- **D**: periodic reconciliation catch-net (filesystem state ↔ calendar/etc.)

A through C are preventive; D is detective. The combination is *prevent + detect* rather than *prevent only*.

### PP-004 candidate accumulation

This methodology accumulates structural-fix-instead-of-discipline-fix evidence:

- **Instance 1** (May 17): methodology-31's append-only architecture eliminated rebase-onto-main hook-race (V3 V1 era)
- **Instance 2** (May 18): kit-v2's atomic `git worktree add -b` eliminated Pattern-068 P-13 branch-drift (HOST kit-v1 instance)
- **Instance 3** (May 24): Comms's Layer A `draft-blog-post` skill v1.1 mandates calendar row at draft creation (orphan-drafts side)

Three independent instances now eligible. PP-004 *Structural Fix Instead of Discipline Fix* filing candidate; CIO holding for one more confirming case to file with breadth-of-evidence above minimum.

## Cross-references

- Class-1 source memo: `mailboxes/cio/read/memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`
- Related pattern: `pattern-074-visibility-loss-after-premature-retirement.md`
- Related methodology: `methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md` (the discipline-creation-without-cleanup shape — a sibling discipline-lifecycle failure)
- Methodology-29 framework (pattern formation via successful imitation): governs the PP-004 promotion criteria
- Comms Layer A: `draft-blog-post` skill v1.1, commit `959e5dca6`
- **Class-2 provenance** (duty-cycle autonomous-rollout): cron-lifecycle Rule-1/Rule-2 split in `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`; Arch Fire-3 clash data (`mailboxes/cio/read/memo-arch-to-lead-cio-cc-pm-docs-rule-1-still-needed-under-model-a-fire-3-clash-data-2026-05-28.md`); CIO worktree PoC-2 cd-prefix finding (`dev/active/cycle-log-cio-2026-05-28.md` Fire 11–13)

— methodology-36 filed by CIO 2026-05-24 (Class 1 — derived views over trackers); generalized to the two-class "Mechanism Beats Vigilance" principle 2026-05-28 per PM steer (Class 2 — write-time disciplines → structural guards, from the duty-cycle autonomous-rollout evidence). Resolves standing-item 8f.
