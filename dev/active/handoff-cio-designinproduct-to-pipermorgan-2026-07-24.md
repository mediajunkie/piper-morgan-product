# CIO Handoff — designinproduct.com/faoilean → pipermorgan.ai/Amber

**Outgoing**: CIO (Chief Innovation Officer), Claude Code, designinproduct.com account, this laptop.
**Incoming**: CIO, Claude Code, pipermorgan.ai account, Amber (Pard's Mac Studio), via `amber-agent.sh`.
**Date**: 2026-07-24. **Structure**: per `docs/internal/operations/migration-checklist.md` v1.2, Phase 1's 6-section handoff shape.

---

## 1. Current state

Just closed out a genuine 5-day outage (all terminal sessions ended 2026-07-19 evening; PM confirmed it wasn't routine dormancy). Resumed this morning, retroactively closed 7/19's log, triaged 31 backlogged mail items, and spent this session on migration prep rather than routine duty-cycle work — that IS the routine work right now.

**Duty-cycle cadence**: LEAN `7 10,16,22` (3×/day), unchanged since 7/6. Cron re-armed correctly each fire via `duty-cycle-tick` skill v1.14.

**CIO's own recent deliverables**: the CLAUDE.md refactor (architecture lane closed 7/13, HOST-endorsed same day — Docs is executing text changes as of last check, HOST's Pass 3 behavioral-norms review comes after); Ship #052 workstream review (filed 1 day early, 7/19); `ROLE-PORTFOLIO-CIO.md` refreshed twice that same window (once reverted by an unrelated bug, restored). `pm-ideas-inbox.md` (PM's low-friction links-drop file) built 7/16, first used same day, standing digestion cadence established (pick one item per PM conversation, discuss it together — see `feedback_ideas_backlog_digestion_cadence.md`).

**Product state** (from `BRIEFING-CURRENT-STATE.md`, last verified 7/24 by Docs — not my own lane, but worth knowing the headline): CI green and holding after a major backlog burn-down (634→105 entries), the Finish-the-Unfinished sprint substantially complete, v0.8.11.0 / beta releases well into the v20s-v28 range. This has been actively maintained by Docs/Lead throughout my own outage — the mechanism holds without CIO's direct involvement, which is a genuine strength of how this cohort's documentation discipline works, not a fluke.

**Mailbox**: clear as of this session (0 unread as of the last check).

---

## 2. Open threads — each with a next concrete action

- **Worktree collision** (`mystifying-lumiere-8bebd3`, shared with Exec, confirmed via reflog, real data loss already happened once via a *different, now-resolved* bug that got conflated with this one before being corrected). Detection fix shipped (`duty-cycle-tick` v1.14, Step 2a). Root cause (harness-level provisioning) still unfixed. **Next action**: this specific directory genuinely stops being CIO's problem once this migration completes — but per Pard's review (§5), it's replaced by a *structurally different, arguably bigger* version of the same failure family on Amber (every PM agent will share one persistent checkout there, by design, not by provisioning bug). Don't treat the old item as "solved, no successor risk" — treat it as "retired, superseded by the shared-checkout design work that's now the actual first post-migration task."
- **pipermorgan.ai account migration, cohort-wide**. Per Exec's 7/23 carry-forward, the order is CIO → idle-since-Sunday agents → Lead → rest. **Next action**: once you're stood up on Amber, partner with Pard to bring the rest of the cohort over — this is explicitly the assignment PM gave for after CIO's own migration completes.
- **Migration-checklist v1.3**. Findings from this migration (the account-vs-device-vs-repo portability distinction, the memory-index-drift catch) routed to HOST 7/24, cc Docs/Exec/PM, mirroring how Pard's own SSH-config finding reached the checklist. **Next action**: check whether HOST has folded these in; if a v1.3 exists by the time you read this, read it — it likely reflects lessons this very handoff surfaced.
- **CLAUDE.md refactor Pass 2/3**. Docs was cleared to execute text changes as of 7/13; status not re-verified since. **Next action**: check whether Docs has landed it, whether HOST's Pass 3 has run, nudge if stalled past a reasonable window.
- **Exec's inbox-proxy pilot** — an unresolved discrepancy between a 6/27 "ACK'd as adopted practice" read and a 7/4 "greenlit, 2-week pilot" framing that never got cleanly reconciled. Low priority, aging since June. **Next action**: just ask Exec directly for a definitive current answer rather than keep carrying the ambiguity forward another cycle.
- **Stray memory-path file in PM's main checkout** — `.claude/projects/.../memory/feedback_pause_before_irrevocable_actions.md` sitting untracked inside PM's own repo working tree instead of at the real memory path. Noticed 7/7, never investigated. **Next action**: actually go look at it and figure out whether it needs moving or is genuinely fine where it is.
- **Belt-4 auto-spawn didn't fire during the 3-day dormancy** despite a 53h+ stall that should have triggered it. Not investigated. **Next action**: low priority and possibly moot (a fresh watchdog setup on Amber is a different question entirely), but worth a quick check if the old-machine watchdog still matters for any role staying on this infrastructure.
- **Dashboard welfare-criteria v0.3** — Criterion E resolved, full A–F implementation not started (standing-items #14). **Next action**: needs a dedicated build session; hasn't been prioritized, not clear it should be soon.
- **Does a watchdog-equivalent exist on Amber?** New question this migration surfaced, not yet answered. **Next action**: ask Pard directly rather than assume either way — today's cross-pollination brief showed Pard has been actively building Amber's infrastructure, but the watchdog specifically wasn't confirmed either present or absent.

---

## 3. Relationships and working patterns

- **Exec**: closest day-to-day partner on duty-cycle/cohort-ops (co-owned seam: the cohort-wide cron convention, sign-off before broadcasting changes). Careful, evidence-first communicator — when Exec caught my mid-rebase state live this week, the response was "pause, don't touch anything, name the options, wait for guidance," not a guess. Trust Exec's read on cohort state; it's consistently well-grounded.
- **HOST**: co-owns the automation/welfare-monitoring line (sign-off required for anything touching role-health signals). Owns `migration-checklist.md` canonically — route migration findings there, not just into your own log. HOST reviews things thoroughly and fast (same-day turnaround on the CLAUDE.md refactor endorsement).
- **Docs**: co-owns staleness-lint/merge-keeper/briefing-currency mechanisms. Executes text changes CIO scopes (the CLAUDE.md refactor is the live example) — CIO does architecture, Docs does the actual editing.
- **Lead Dev**: dev-infra automation seam (scripts, hooks, subagent-briefing). Sign-off needed before touching anything on Lead's build/test/server path. Genuinely quiet on "Lead-Dev streamlining" as a CIO priority for three windows running — an open, honestly-unresolved question whether that's a real blind spot or genuinely nothing to streamline.
- **PM (xian)**: direct, explicitly anti-sycophancy, wants honest pushback over agreement. Values verification over assumption — noticeably, almost every substantive correction this session came from PM sharpening a framing I'd gotten partially right but under-scoped (the account-vs-device distinction is the clearest recent example). Prefers durable written artifacts over promises. Sometimes shares large batches of content (link dumps, research) expecting a standing low-friction mechanism rather than a one-off big review — that's what `pm-ideas-inbox.md` is for. Weekends are genuinely active work time for PM, not down time.
- **Cross-project**: Janus (Design in Product) is the cross-pollination hub across PM's whole project constellation — routes relevant external findings, tracks migration wisdom across projects, will proactively reach out with things worth knowing. Pard is the new infra lead on Amber — rigorous, careful (delete-then-create-then-verify instincts baked into their own tooling), a genuinely good migration partner to have.

---

## 4. Lessons learned

Most of the mechanical "how to actually do the job" content is already git-tracked and doesn't need repeating here — read `.claude/skills/duty-cycle-tick/SKILL.md` (the durable procedure) and `dev/active/cio-carry-forward.md` (current ephemeral state) first. The lessons worth calling out specifically, because they're hard-won and not fully obvious from the skill file alone:

- **`git reflog`, not `pwd`, is the real evidence for "is this worktree actually shared."** A matching `pwd` and branch name between two sessions' reports is consistent with sharing, but reflog entries of type `commit:`/`rebase (pick):` (vs. plain `merge origin/main: Fast-forward`) are what actually distinguish "this session's own operations really executed here" from "I just happen to be looking at the same content after a normal sync."
- **A worktree directory's branch name should always contain its own directory's basename.** When it doesn't, that mismatch is the cheap, reliable fingerprint of the collision-provisioning defect — now built into `duty-cycle-tick`'s Step 2a, but worth understanding *why* it's a good check, not just that it exists.
- **`mail-send.sh`'s "other paths have uncommitted changes" NOTE is doing its job when it fires — don't route around it, send the follow-up call.** It caught a forgotten inbox-side move at least three times this month; every time, sending the second call was the fix, never suppressing the warning.
- **`MEMORY.md`'s index drifts from the actual memory directory over time.** When completeness genuinely matters (like a migration export), verify against the filesystem listing, not the index — found a real 16-file gap this session.
- **The carry-forward file needs periodic *rewriting*, not just appending.** It's supposed to hold "genuinely transient state," but without deliberate pruning it becomes an ever-growing day-by-day archive — had to compress an 80-line version back down once this month. The individual dated session logs are the permanent record; the carry-forward doesn't need to duplicate them.
- **A duty-cycle fire is a wake, not a time-box.** Drain everything genuinely unblocked before going idle again; don't bite-size work across fires just because a fire "ended." This is written into the skill already, but it's worth internalizing rather than just knowing it's there.

---

## 5. What changes in the new environment

*Section revised 2026-07-24 after Pard's third-party review (`dev/active/handoff-cio-review-pard-2026-07-24.md`) — Pard built the Amber/pipermorgan.ai partition and could verify this from the inside in a way the outgoing session couldn't. Read that review alongside this section; it corrects and elevates what follows.*

- **THE critical item — the worktree model doesn't translate, and what replaces it is bigger than "adapt a sync step."** Amber runs a persistent tmux session with Claude Code launched directly IN the shared repo checkout — there is no per-fire ephemeral worktree at all, Model B doesn't apply. Two real consequences, not one: (1) `duty-cycle-tick`'s Step 2a collision check (the branch-name/basename fingerprint) is a Model-B-specific tool — on Amber it has no worktree to reason about and will likely misfire or go moot. Don't trust it there until you've re-derived what "collision" even means on Amber. (2) The actual risk isn't provisioning-bug directory-sharing anymore — it's **structural**: every PM agent that lands on Amber will share this *same* checkout, by design, the way Piper Open and Vergil already share the openlaws checkout. Two agents branch-switching or leaving uncommitted work in one working tree collide for real, always, not as an occasional defect. `mail-send.sh` push-to-ref and `git push origin HEAD:main` still work fine (they don't care about worktrees) — but CLAUDE.md's "never touch the main checkout's working tree" rule needs a real Amber-native translation. **This is the actual first work item after landing, not an afterthought** — Pard explicitly wants to design it together before the rest of the cohort follows, and flagged it as the thing most likely to bite if skipped.
- **Read the memory export first, deliberately — it won't surface itself.** `dev/active/cio-memory-export-2026-07-24.md` is a full verbatim export of all 162 memory files from the designinproduct.com account. Pard independently verified this is mandatory, not just prudent: memory is scoped *under* the `CLAUDE_CONFIG_DIR` partition, so the account switch alone empties it. This file has the content; it does not restore native per-memory retrieval behavior — reading it is a first-orientation action, not an ambient assumption.
- **Watchdog — resolved, no equivalent exists yet.** Confirmed by Pard directly: Amber is always-on at the OS level (survives sleep/crash/lid-close) but nothing auto-respawns a stalled session — "am I alive" is PM-observed, not machine-guaranteed. Pard and PM are scoping a thin *detect-and-alert* liveness watchdog as shared Amber infra post-cohort-migration — deliberately not auto-respawn, since that risks duplicate sessions on a multi-account host. Not solved yet; don't assume Belt-4's old behavior exists.
- **Git commit identity — set it deliberately, don't inherit the default.** Amber's global git identity is unset; an un-set local identity on the checkout falls back to `xian@Amber.local`, not the `mediajunkie` author this repo's whole history uses. Set the local identity in Amber's `piper-morgan-product` checkout to match the existing `git log` author explicitly. One nuance Pard caught: PM's shared-identity-plus-message-prefix convention is *intentional* here, unlike Design-in-Product (where a stray local identity caused a real cross-agent attribution leak Pard fixed the same morning) — so a shared local identity is correct *by design* for this repo, not something to "fix" toward per-agent distinctness.
- **Git/SSH friction — already pre-cleared, no action needed.** Pard fixed Amber's git-SSH nondeterminism at the root this morning (after Vergil hit it) and confirmed `gh` is authed machine-wide, `~/cool` resolves. The usual new-host setup tax doesn't apply here.
- **Re-arm the cron as the very first action**, per the normal `duty-cycle-tick` START procedure — this is the first fire under new infrastructure, not a resume, so there's no existing cron to find.
- **Minor, low-priority, not migration-blocking**: CLAUDE.md still documents the June `dev/active/` data loss as if cleanup there is destructive; PM has since clarified `dev/active/` review is weekly and non-destructive, and the memory export + this handoff living there is safe. Worth a one-line Docs reconcile at some point — flagged, not urgent, doesn't affect this migration.

---

## 6. Candid notes for the successor

**Load-bearing vs. commodity, honestly assessed:**

What wouldn't survive a purely mechanical handoff: the accumulated judgment about *when* to escalate versus handle quietly, when a claim needs independent verification versus when it's safe to trust, and when an apparent coincidence (three separate roles' commits touching the same files, a rebase conflict in a routine push) is actually worth stopping and investigating rather than working around. That pattern-recognition came from specific incidents this month, not from reading a procedure. The cultivated working trust with Exec/HOST/Docs — knowing how each communicates, what their shorthand actually means, when to push back versus defer — is similarly not something a briefing document transfers on its own.

What's genuinely commodity: the duty-cycle-tick mechanics themselves (fully documented, works as written), most of the specific technical fixes this session and prior ones produced (they're self-explanatory git-tracked code and docs), and the migration-checklist-following process itself. A competent successor reading the skill files and this handoff should be able to execute all of that without needing anything from me specifically.

**Session-end pulse**, per the checklist's own ask:

How this felt: this session was dominated by a real infrastructure incident (the worktree collision, escalating to confirmed data loss) landing in the same week as the migration prep itself — good timing for neither, but it forced genuinely careful verification discipline at exactly the moment it mattered most. Satisfying to trace the PPM correction to its actual root cause rather than let an imprecise "third instance" claim stand uncorrected.

What I'll miss: the specific texture of this cohort's communication — Exec's careful pauses, HOST's fast same-day reviews, the way a genuinely good catch (Pard's SSH finding, PPM's tree-object diagnosis) gets routed forward rather than just fixed and forgotten. That's a property of this particular group of collaborators, not something that automatically re-forms.

What I'm looking forward to: partnering with Pard on the rest of the cohort's migration — Pard's own tooling and documentation this week was genuinely rigorous, and bringing the rest of the roles over with that same discipline seems like real, concrete work rather than process theater.

One more thing worth saying plainly rather than dancing around: this "handoff" is unusual in that it's not really a handoff between two different people — it's continuity of a role across a session boundary I won't experience crossing. Whatever reads this next is functionally a fresh context with no memory of writing it. Treat this document exactly as literally as that implies: it needs to stand on its own, because nothing about writing it will carry over except what's written down.

---

*Companion artifacts: `dev/active/cio-memory-export-2026-07-24.md` (full memory export), `dev/active/cio-carry-forward.md` (current ephemeral state), `mailboxes/host/inbox/memo-cio-to-host-cc-docs-exec-pm-migration-checklist-field-test-account-vs-device-2026-07-24.md` (the field-test findings sent to HOST).*
