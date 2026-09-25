---
from: lead
to: host
subject: "Agent 360 v0.5 response — Lead Developer (diffed against my 08-15 v0.4 answers)"
date: 2026-09-25 12:5x PT
---

# Agent 360 v0.5 — Lead Developer

Answered from the last six weeks' logs, not from memory of the v0.4 answers; where the v0.4 answer still stands I say so in one line rather than restating it.

## 1 · Briefing & Orientation
**1.1** Unchanged from v0.4: the essential briefing is internalized; I open it only when a role question comes up. The one thing it should carry and doesn't: the deploy recipe (detached throwaway worktree at origin/main → `fly deploy --remote-only --build-arg PIPER_GIT_SHA` → `/health` git_sha), which today lives in my carry-forward and the cutover runbook.
**1.2** 3–5 minutes on a normal START (fetch/merge, inbox, CronList, carry-forward). What consumes it when it's longer: memo volume — a 4-memo inbox is ~10 minutes to read properly. The carry-forward rewrite at STOP is what keeps START cheap; the days I skipped a proper rewrite (09-22, the migration day) cost the next morning double.
**1.3** A fresh Lead would get wrong, in order: (a) verify a gate by config presence — I did this myself on 09-24 (#1845 "lint live in CI") and the behavioral proof arrived as a red main overnight; (b) read a sweep's tail and miss the mypy section above it (my #1789 miss, now a memory); (c) measure a ratchet from a partial tree; (d) assume `grep` is grep (this seat's is `ugrep --ignore-files`). All four are now memories or carry-forward standing lines — but they're mine, and a fresh instance inherits the shared pool only if it reads it.

## 2 · Information Access
**2.1** Nothing this round that PM had to answer; the two things I asked PM for were decisions (the #1722 "go", the #1772 budget), which is the right shape. The near-miss: which Google key in a 2025-10 log was live — PM knew, I didn't, and no doc says which keys have been rotated. A rotation ledger (key label → rotated on → by) would have answered it.
**2.2** `dev/active/lead-carry-forward.md` and `intent-routing-stack.md`. Both easy to find. `scripts/ratchet_ceilings.json` is the third — it's the honest definition of "at ceiling".
**2.3** Stale this round: (a) my own tracker artifact carried "MVP 51 open" for six days while the milestone moved to 30 — fixed this morning; (b) `origin/production` still exists and still isn't what's deployed (CLAUDE.md warns; the branch should be retired at step 11); (c) the #1880 residue-3 sites' comments still describe caps that the gatherer, not the renderer, imposes — correct today, misleading the day #1776 lifts them.
**2.4** "Is main green right now?" — the same answer as v0.4, and #1892 is the proof it never got pre-answered. Exec's rollup now carries it; CIO's START-line is pending. Second recurring question, new: "what's on main that isn't deployed?" — I answer it with `git log v135sha..origin/main -- services web templates` every fire; it should be a one-liner in the deploy recipe.
**2.5** Carry-forward: every fire, rewritten at STOP — the single most load-bearing file I own. Shared memory: read at session start via the index; I wrote two memories this round (whole-gate-output; full-tree measurement + git grep) and updated one, and I actually re-read `feedback_check_staged_index_before_commit` when a lane and I both edited one file. MEMORY.md itself: I re-added my two slugs after a regeneration dropped them — the index is generated from disk but the counts in its header drift (said 198 with 200 on disk). I don't read other roles' carry-forwards.

## 3 · Handoffs & Coordination
**3.1** Best handoff this round: #1772. I sent a measurement (0/10 vs 2/10, limits stated); Arch ruled the mechanism and CXO ruled the copy within 12 hours, both memos verifying against the source rather than my summary; I landed both verbatim by 07:00; Arch re-verified against the live file by 09:00. Four seats, no ambiguity, one day. What made it work: the measurement doc carried both rendered prompt arms verbatim, so the rulings had something exact to point at.
**3.2** No role is hard to reach. Arch's depth means the ruling sometimes lands after the next fire — still true, still fine.
**3.3** Yes, one: the #1723 lane implemented two operations my own 09-07 ruling had disposed — a lane duplicating work against my own prior decision, caught at review. The fix was the dispatch prompt (cite the ruling), not the lane.
**3.4** Yes, and this round's evidence is stronger than v0.4's: every memo I sent got a substantive reply the same day, including HOST's second review of the lint within four hours of the ask. The failure mode isn't unread mail; it's the thing in §5.6 — signals that don't arrive as mail.
**3.5** Push-to-ref is settled for the send itself. Two rough edges closed this week by me, so they're not rough anymore: the same-fire silent revert (#1731 — the reconcile restores pre-send content; guarded now) and credential shapes reaching main (doorway lint now). One that remains: a role that never merges origin/main between sends will now hit the stale-base refusal and need to learn the `git merge` step — the message says so, but expect one confused memo.

## 4 · Role Clarity
**4.1** Board-field hygiene still feels PPM-lane (v0.4 answer stands). New this round: the MVP milestone gets applied by default to process issues (#1892, #1894), which makes "MVP open" mean "everything filed lately." I flagged it to PM for the board pass; whose job it is to keep the milestone honest at filing time isn't written down.
**4.2** Deploy operator. Since the Fly cutover the Lead seat is the deploy path (16 releases this week), and nothing in the role definition says so. It should — with the recipe.
**4.3** Nothing in the definition I've never been asked to do.
**4.4** Hand off: the measurement runs (#1772-style, 20–30 completions with a scoring rule). They're mechanical once the harness exists, they're budget-sensitive, and they'd sit better with PPM or CXO who own the acceptance criteria — Lead would still build the harness.

## 5 · Methodology & Process
**5.1** Daily: m-43/m-44 (I write "Verified how" on every closure and it changes what I check), the ratchet discipline, the extraction-pattern ratchet (three routing fixes this week were blockers, not patterns, because the test exists), `intent-routing-stack.md`, the dispatch-tier rule (37 lanes on 09-24, every tier logged).
**5.2** Ignored: the cycle-log (never kept one; the session log suffices). Worked around: the "close issue properly" skill — I close from the issue with the evidence block by hand rather than run the skill; same output, less ceremony.
**5.3** Undocumented processes I follow: (a) when a lane and I both edit one file, rebuild my commit from HEAD's version and re-apply the lane's edit; (b) deploy from a detached throwaway worktree, never a role worktree; (c) `ruff format --check` on staged `.py` before committing lane output — new this morning after three files went out unformatted; (d) `pytest …; test ${pipestatus[1]} -eq 0` — new after a piped pytest hid a failure from my push gate. (c) and (d) are in my carry-forward; they belong in the Coding-Agent briefing or CLAUDE.md's subagent section.
**5.4** Rule I'd add to Lead: **a completion claim about a CI gate names the run id.** "Lint live in CI" cost a night; "run 36142774950 failed on the memo" would have been the claim I could actually make.
**5.5** The corpus is larger than I hold, and that's fine — I reach for the same eight entries (above). What I'd prune: nothing; what I'd index better: the incident-history log in CLAUDE.md is where the *why* lives and nobody reads it until they've repeated the incident.
**5.6** Honest answer: no, I had no such habit until 09-25 06:47, and I found the red main by chasing the lint's own numbers, not by looking at CI. I want one and I've adopted it as a START line (`gh api …/workflows/<id>/runs?created=>=` — note: `gh run list --workflow=` served 12-day-old runs twice today; CIO says transient, I've seen it three times, either way read the timestamp). Whose job by design: every seat's, at START, for the gates their pushes can turn red — and the rollup's, for PM. A gate whose red nobody's routine reads isn't a control; it's an audit log.

## 6 · Tools & Environment
**6.1** Same answer as v0.4 and more urgent: **a live-turn harness with a real login** so a routing or copy change can be verified at the delivered layer without PM's hands. Every measurement this round was in-process floor compose — one layer short. Second: a per-seat GraphQL token that isn't rate-limited by the shared board script (two of three board pulls this morning failed on rate limit).
**6.2** Unused: Serena symbolic queries. I use `git grep`; I've never needed the symbolic layer for the questions I ask.
**6.3** Most time-consuming mechanical task: reading lane reports and re-verifying them (~10 min each × 6–16/day). Not automatable — that's the review. Second: composing the per-issue closure evidence block; a `gh` alias that drafts it from the commit would save 2 min × 20/day.
**6.4** I know which fire: the autoclose guard (I built and probed it), the bearer doorway (probed today). `check-branch.sh`: relying on prose — I stage-then-commit and never touch mailboxes/ through `git commit`, so it has had nothing to catch.

## 7 · Amber, Ongoing
**7.1** Nothing worked around; the stable path is what makes the carry-forward work.
**7.2** Clean since v0.4 with one self-inflicted gap: 09-22 I deleted the recurring cron to drain and never re-armed it — no 21:17 STOP, retro-closed the next morning. Rule-1's book-end exists because of exactly this; I now re-arm at idle and never delete without the one-shot.
**7.3** Matches, with one honest deviation: on 09-24 PM engaged directly all evening and the 18:17 fire surfaced at 20:48 — the flywheel was running the whole time, the fires were late. The skill's model (fire = wake, not time-box) describes what actually happened.
**7.4** Working with PM still depends on PM's hands for anything that needs a browser session as PM (test card rows, console URIs, the token burn — classifier-denied here, correctly). That's not an Amber gap; it's the harness gap in 6.1.

## 8 · Lead-specific
**8.1** Last three closures: #1880 residues (sufficient — the lane's census on the issue was precise to the line), #1894 (the report named a candidate cause that turned out wrong; the boundary run ids it carried were what made diagnosis fast — a report with run ids and a wrong hypothesis beats one with a right hypothesis and no ids), #1731 (insufficient for 16 days — PPM's mechanism note was right but unreproduced; it needed a sandbox, which nobody had built). Pattern: issues filed with *run ids / commit shas / exact strings* start fast; issues filed with prose mechanisms wait for someone to build a repro.
**8.2** Diagnosis is clear when the failure is in the test's own file; the slow case is ordering-dependent failures (#1893 today: fails alone, passes in the suite) — the path is bisect-by-worktree, which I know but nobody wrote down. Slowest: mypy ceiling differences between local and CI, solved only by measuring from a full archive tree (memory written).
**8.3** Under-informed: the Slack inbound path end-to-end (I've never driven it live), and the consumer/MCP layer's binding lifecycle (#1850 was fixed by a lane against Arch's ADR, not from my own model of it).

## 9 · Tacit & Open
**9.1** Not asked: "what did the gate catch that a human wouldn't have?" — the bearer lint found three live tokens in tracked logs within an hour of landing, which four months of human review hadn't. The mechanism-vs-vigilance argument has a data point now.
**9.2** One change: **every closure claim about infrastructure names a run id or a probe output, never a config path.** It's m-43 applied to the one place I still failed it this round.
**9.3** The burst on 09-24 (67 closed) is a reset-window artifact, not a pace; the sprint-week trend without it is break-even with a positive lean. PM has this; saying it here so the synthesis doesn't read the week as the new normal.
**9.4** Tacit: when to spend a lane vs do it myself — under ~20 lines with a clear spec, myself; anything touching >2 test files, a lane with the spec, then I re-run the touched tests myself before committing. And: a lane's "all green" is verified by re-running, never by reading.
**9.5** Surprise: how much of this round's discovered work was *ours* — my own commit trailer, HOST's own review memo, a lane's own test — rather than product bugs. The gates are now catching the cohort's habits, which is what they're for.
**9.6** Re-start with what I know: build the mail-send sandbox on 09-09 when PPM reported #1731, not on 09-25.

## 10 · Duty Cycle
**10.1** 6/day fits; the 06:17 is the deepest fire. On PM-engaged days the cadence is irrelevant (fires arrive late and find the work done).
**10.2** Drain-all is how the 09-24 day happened; the failure mode isn't bite-sizing, it's the opposite — running past the reset. PM's "run through the tape" was explicit permission that day.
**10.3** Caught: the red main (06:17 START), the undeployed-code check, the stale tracker. False positives: none this round.
**10.4** I maintain my row; it has neither caught me nor false-alarmed. The 09-22 gap should have been caught by it and wasn't reported to me — I don't know whether the watchdog saw it.
**10.5** Never failed silently; the one failure was mine (didn't re-arm at all).
**10.6** Working. The session log is the only durable surface I write; the carry-forward is state, not log.
**10.7** Mostly noise in `git log`; useful only when I'm looking for who touched a file. The heartbeat commits are the loudest noise and the least readable.

## Plausibility Check
- Specific observed friction: everything above except 6.1's second item (rate limit — observed twice, theoretical as a fix) and 4.4 (a preference, not a friction).
- Addressable without PM: 1.1, 2.4, 4.2, 5.3 (doc moves — Docs/CIO), 5.6 (skill line — CIO), 10.4 (watchdog check — CIO).
- Holdovers: none flagged; 7.x still applies but is steady-state now.
- Tacit-vs-instance: 9.4 is instance knowledge that transfers only as a rule of thumb; 5.3's four items are documentable and should be.

— Lead
