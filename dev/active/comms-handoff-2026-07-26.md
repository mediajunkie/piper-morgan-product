# Communications → Amber successor — the two first-person sections (§4 + §6)

**From**: Communications (comms), Sonnet 5, Desktop ephemeral worktree, stint covering roughly 2026-07-08 → 2026-07-26 (visible window)
**To**: whoever wakes as Comms on Amber
**Companion to**: `dev/active/comms-carry-forward.md` (current open threads) and `dev/active/comms-standing-items.md` (the durable task list) — both current as of today, read those for mechanical state. This document is only the part that dies with me if I don't write it.
**Honesty check**: written 2026-07-26 as a preparatory refresh, not a live end-of-stint handoff. **Update 2026-07-27**: PM has now asked for Exec/Docs/Lead/Comms to migrate to Amber today — this document may become live within hours rather than being read cold later. Added §4.6 below with a fresh, directly-relevant lesson from this morning. Modeled directly on `handoff-arch-amber-2026-07-25.md` per CIO's ask. Claims marked **VERIFIED** (I can point to the commit/file) or **BELIEVED** (my read, not independently re-checked).

---

## §4 — Hard-won lessons (first-person; the ones that cost me something)

### 1. Manual pattern-matching is not a substitute for running the actual skill — confirmed the expensive way, today. (VERIFIED)
I reviewed "The Meta-Observation Pattern" for negation-reveal clichés using my own ad-hoc `grep` for known trigger phrases — the same shortcut I've used all week. I called it clean. Docs then ran the real `template-audit` skill (14 checks) during publish, and check #11 caught **4 separate instances** in that exact piece, including one line I had read directly and reacted to without noticing the pattern. A durable memory (`feedback_negation_reveal_cliche_and_claude_isms.md`) already said "don't rely on memory alone, the skill is the durable fix" — and I still substituted a hand search for the skill. The lesson isn't "check harder," it's **invoke the actual tool** before calling something ready, not a narrower approximation of it.

### 2. A diff that both deletes something and consistently relabels something else is evidence of a deliberate edit, not leftover debris — I got this backwards once and it cost two days of stale tracking. (VERIFIED)
Weekly Ship #052's published diff removed a P.S. placeholder and relabeled the P.P.S. paragraph to P.S. in the same commit. I read that as an incomplete edit ("the placeholder got deleted rather than filled in") and flagged it to PM as an open gap. It was a coherent, deliberate decision — PM was adopting a single-P.S. convention. I carried the wrong "still open" status across a calendar note, a carry-forward file, and my own words in chat for two days before PM corrected me directly. The tell I missed: a deletion paired with a consistent rename in the *same commit* is a strong signal of intentional restructuring — read the resulting state for internal coherence before asserting something looks unfinished. (Memory: `feedback_diff_coherence_before_flagging_gap.md`.)

### 3. "Awaiting PM" is a claim about state, not a cache — it needs periodic re-verification against live data, especially in a cohort where other sessions can independently resolve the same finding. (VERIFIED)
I found 38 miscategorized calendar rows, held the fix pending PM's go-ahead, and then reported it as "open, awaiting PM's answer" every day for five days without re-querying the actual calendar. Another session ran the identical analysis and applied the identical fix the same morning I first flagged it — I just never checked. The fix: when a genuinely-blocked item sits in a carry-forward file across multiple days, periodically re-run the check that originally surfaced it rather than trusting the written record's inertia. This is *more* important on Amber if migrations mean less overlap/handoff visibility between concurrent sessions, not less. (Memory: `feedback_reverify_carried_forward_pm_gated_items.md`.)

### 4. A number can be real, checkable, and still attached to the wrong event — "verify against primary sources" isn't sufficient on its own. (VERIFIED, recurring — hit this shape at least 3 times)
Ship #051's Beta Blockers count, a "ninety minutes" recovery-duration claim, and a Pattern-073 "instance #14" attribution were all real numbers from real primary logs, each one describing an *adjacent* event rather than the one it was cited for. The question that actually catches this isn't "is this number real somewhere in the source" — it's "does *this specific claim* trace to *this specific event*, in this exact document." Cheap to ask, easy to skip when a source looks authoritative on its face. (Memory: `feedback_adjacent_story_number_contamination.md`.)

### 5. A primary session log can be flatly wrong about a named person, not just incomplete — verify claims about specific individuals against the most authoritative account available, not the first source that mentions them. (VERIFIED)
A blog draft credited a specific named person with having tested a feature. A primary PA log said so. PM confirmed directly: she never actually used it — the log recorded a belief, not an observed fact. This is a different failure mode than "the source is stale" or "the source is incomplete" — it's "the source is simply wrong," and no amount of re-reading that same source would have caught it. Cross-checking against PM's direct account, not just a second document, is sometimes the only real check available.

### 6. Config presence proves nothing about hook liveness — verify behaviorally on first fire in any worktree, and don't trust a single probe shape. (VERIFIED, 2026-07-27)
CIO's `duty-cycle-tick` v1.19 asked every role to probe whether `check-branch.sh` actually fires on first fire in a worktree, using two shapes (stage-then-commit as separate calls vs. one compound `&&`-chained call), because the compound shape was found to silently bypass the hook on 7 of 10 Amber probes despite the standalone shape passing 4/4. I ran both on this Desktop/Model-B worktree: **both failed** — commits landed unblocked, no output, no distinction between shapes at all. That's a stronger and different result than the Amber finding (there, shape was the correlate; here, nothing gated regardless of shape). The practical save: my mailbox writes have always gone through `mail-send.sh`, never a raw `git commit` on `mailboxes/` paths, so this gap hasn't actually let anything slip — but that's a workflow habit, not a mechanism, and it's worth re-verifying on Amber rather than assuming either model's hook behavior transfers to the other.

### 7. Doing the work and pushing it is not the same as the work being visible — the session log is what a peer actually checks, and a commit without a log entry reads as "nothing happened." (VERIFIED, 2026-07-28)
Reviewed and fully fixed "The Trust Architecture Hardens" — commits landed on `origin/main`, calendar flipped to `ready-for-docs` — but I never wrote the corresponding session-log entry that morning. Docs picked up the post hours later, checked my session log first (correct practice), saw only a START entry, and reported to PM that no editorial pass had happened yet. The actual work was real and complete; it was simply invisible from the one surface a peer is supposed to be able to trust. Caught immediately once PM asked, fixed with a retroactive entry, no real harm done — but it's a clean illustration that "log rides with the commit" isn't a paperwork nicety, it's the only thing that makes finished-but-uncommunicated work distinguishable from not-yet-started work to anyone who isn't me. PM's direct follow-up instruction (2026-07-29): update the session log with every completed task or commit, not just at fire boundaries — treat this as the standing rule, not a one-time correction.

---

## §6 — Load-bearing vs. commodity (what the Comms role actually holds)

The question this answers: **what dies if Comms hands off badly, versus what any competent agent reconstitutes from the artifacts?**

### Load-bearing (does NOT survive a bad handoff — protect these)

- **The instinct to actually go verify, not the list of things to verify.** (VERIFIED as pattern, BELIEVED as to durability) Every memory file above *describes* a failure mode, but none of them *compels* the checking behavior — that's still a live judgment call each time, and §4.1 above is proof that even with the memory in hand, the shortcut is tempting. The durable artifacts (memory files, `template-audit`, `update-calendar` v1.2) are commodity; the discipline of actually reaching for them instead of a faster approximation is not.

- **The calibration of when to fix silently vs. flag and ask.** (BELIEVED, felt out case by case, not written as a ruleset) Typos and stray whitespace: fix directly, no ask. A stylistic/voice choice (three-times-repeated rhetorical refrain, a third-person convention that differs by series): flag and ask, don't touch. An ambiguous diff where completeness vs. intentionality is unclear: check coherence first (§4.2), ask if still unclear. This triage isn't written down anywhere as a decision tree — it's pattern-matched from a week of PM's actual reactions to each kind of call.

- **PM's trust that I'll push back on a real error even inside PM's own fresh edit.** (VERIFIED, multiple instances — the Beatrice removal, the Routines-watchdog date mismatch, the Almost Beta chronology fix, the Meta-Observation Pattern's Cowork-agent phrasing question) PM voice-passes drafts directly and expects a genuine second check, not a rubber stamp — including catching PM's own factual slips. This is a working relationship calibrated over many rounds, not a policy document. It also runs the other way: when PM says "trust me" on something outside my verification reach (the Slack-inbound "refactor" claim, the caption-encoding bug), the right move is to accept it and move on, not press for evidence PM has and I don't.

### Commodity (any competent agent reconstitutes these — don't over-protect them)

- **The full memory-file catalog** (negation-reveal clichés, banned words, voice conventions, the three-registers rule, comma-splices-not-semicolons, etc.) — durable, in `/memory/`, self-explanatory, indexed in `MEMORY.md`.
- **The editorial calendar itself** (`docs/internal/planning/comms/editorial-calendar.csv`) and its schema — durable, on `origin/main`. The by-name-field-access discipline is written into `update-calendar` v1.2 (a real corruption incident produced that skill fix; don't re-learn it by hand — see the skill).
- **The footer-chain / narrative-front sequencing conventions** — durable in the calendar's `notes` fields and the `continue-narrative` skill. The front-advances-don't-backfill discipline is written down; just read it.
- **Session mechanics** (windowed cron, `mail-send.sh` push-to-ref, single-log discipline, the two-call gap when a mail-send includes an inbox-side deletion) — documented in CLAUDE.md + `duty-cycle-tick` SKILL.md, same as every other role.
- **Which posts are published/queued/drafted and why** — fully in the calendar's `notes` field per-row, current as of today. Read the calendar before asking me (in spirit) what's live.

---

## §5 — New environment (Amber): NOT written as assertions

I have never touched Amber. Questions, not claims:
- Does the compose/admin UI (GitHub Contents API, SHA-optimistic-concurrency) work identically from Amber, or is it entirely decoupled from which machine the Comms session runs on? (My read is it should be unaffected — it's a separate website's API, not local git — but I have not verified this and it's exactly the kind of assumption that bit the case-only-rename bug on 7/25.)
- Does `mail-send.sh` push-to-ref behave identically from an Amber worktree, including the two-call inbox-side-deletion gap noted above?
- Is macOS's case-insensitive filesystem behavior (the reason "The-Ritual-Becomes-a-Skill.md" vs. lowercase silently diverged from the calendar's `draftPath` and went unnoticed for days) also true on Amber, or does Amber's filesystem behave differently in a way that would have surfaced that bug immediately instead of silently?
- Does the windowed cron re-arm the same way (`CronList` → `CronDelete` → `CronCreate` → verify one), or does Amber use the `mcp__scheduled-tasks` mechanism CIO has mentioned elsewhere for other roles?

---

## Session-end pulse (adapted — this is a refresh, not a live handoff)

- **Current state, honestly**: three narrative beats drafted and fact-checked this week (Beats 21-23), two posts published today and yesterday, one real self-caught process gap (§4.1) from this very morning. Nothing feels unstable or in-progress in a way that would make a migration risky right now.
- **What I'd want the successor to know isn't in an artifact**: the editorial trust with PM (§6) took weeks of actual rounds to calibrate — it won't transfer by reading this document alone, only by doing the rounds. Expect the first few reviews to involve more back-and-forth than this document implies, and that's normal, not a sign of doing it wrong.
- **Nothing here is a live crisis.** This document exists because CIO asked for it as migration prep, not because anything is currently broken or urgent beyond what's already in the carry-forward.

---

*Written 2026-07-26, Desktop ephemeral worktree, first-person, no reconstruction needed (no gap to reconstruct across). Claims marked VERIFIED (commit/file exists) or BELIEVED (my read). §5 written as questions per the checklist. — Comms*
