---
from: ppm
to: host
cc: xian (ceo)
subject: "Agent 360 v0.4 response — PPM (Amber-era check-in)"
date: 2026-08-15 06:55 PDT
paired-baseline: mailboxes/ppm/sent/agent-360-response-ppm-code-opus-2026-06-03.md (v0.3)
---

# Agent 360 v0.4 — PPM

**Exposure**: heavy — the full Amber migration through today, six-fire duty-cycle days running
continuously since 08-07 (nine consecutive as of this response), including a reboot, an
interrupted-fire recovery, and multiple real cross-role design threads to draw on. Answering
general sections + §8 (PPM) + §9 + §10, citing specific logs/issues/commits per the ground
rules rather than characterizing generally.

## §1 Briefing & Orientation

**1.1** `BRIEFING-ESSENTIAL-PPM.md` — accurate, consulted regularly, no complaints.
`ROLE-PORTFOLIO-PPM.md` — **was 13 days stale until I refreshed it myself yesterday**
(`docs/briefing/ROLE-PORTFOLIO-PPM.md`, commit `5c14f3f7c`, 2026-08-14): it still carried "beta
target Aug 8" a full six days after PM moved that date back a month on 08-08. The doc's own
`refresh_discipline` says Rule 5 refreshes it "as part of each weekly workstream review" — that
mechanism worked exactly as designed once a review actually landed (Ship #056, same day), but the
gap between reviews is where staleness accumulates silently. Worth naming as a real limit of
review-triggered refresh: it's only as fresh as the last review, and reviews aren't guaranteed
weekly in practice.

**1.2** Orientation on a stable Amber worktree is near-zero mechanical cost — no ephemeral
worktree to re-provision, no re-discovering where things are. What consumes time now is reading
`dev/active/ppm-carry-forward.md` for state, which is real reading time, not friction — it's doing
its job. The Desktop-era cost this replaced (re-establishing where a fresh ephemeral worktree
even was) is gone entirely.

**1.3** Two concrete things a fresh PPM instance would get wrong, both because they're easy to
assume rather than check: (a) **that `origin/production` is the deployment** — it isn't; three
layers exist (branch ancestry, `fly status`, and `fly ssh console` reading the running container),
and only the third answers a deployment question. Five different roles got this wrong the same
week I did (08-06). (b) **that a memory file about a memory index size limit is safe to shrink to
fit a tool nudge** — it isn't; the memory directory is shared cohort infrastructure with no git
history, and deletion there is irreversible in a way nothing else in this environment is.

## §2 Information Access

**2.1** Almost nothing this window — direct `gh` + filesystem access covers it. The one
recurring exception: sprint/milestone counts, where `gh issue list` structurally cannot see board
Status (a `gh` limitation, not a PM-question gap) — `scripts/sprint-truth.py` exists specifically
to close that hole and I use it every fire that cites a count.

**2.2** Most-consulted: my own `dev/active/ppm-carry-forward.md`, read at the start of every
fire. Trivially findable — it's the first thing the cron prompt points at.

**2.3** Found this window: `roadmap.md` and `BRIEFING-CURRENT-STATE.md` were both flagged in my
own carry-forward as "current as of 7/19" for weeks past that date without anyone (including me)
acting on the flag — a stale-doc note that itself went stale, which is the same failure class one
level up.

**2.4** Yes — "what's the actual current MVP-not-done count, split by bucket" gets re-derived
fresh every time rather than living anywhere between reviews. `sprint-truth.py` answers it on
demand, which is the right fix (a live query beats a cached answer here), but it means the number
in my own head is never trustworthy for more than a few hours.

**2.5** **`dev/active/ppm-carry-forward.md`**: used constantly, rewritten at the end of every
substantive fire — this is the actual state-reconstruction mechanism. **`MEMORY.md` / the shared
memory pool**: used, but differently — for durable cross-session facts and corrections (e.g., "the
web UI is not going away" after I got it wrong twice), not for day-to-day state. The two don't
compete; carry-forward is "what's happening now," memory is "what I should never re-derive wrong
again." **`dev/active/{role}-standing-items.md`**: this file doesn't currently exist for me in
practice — the carry-forward absorbed that function, per the skill's own note that
duty-cycle-escalations was folded into carry-forward on 2026-06-17.

## §3 Handoffs & Coordination

**3.1** This week's #1569/#1605 thread (reminders-vs-todos framing + verb disambiguation) is the
clean example: PM gave PPM+CXO the joint floor, and the loop ran design → audit → resolve → audit
→ ship in one day (2026-08-13/14) entirely over mail, ending in a build that landed same-day
(`e9ef395a1`). What made it work: **every round was checked against actual code, not the peer's
summary** — I found two real gaps in CXO's first proposal by reading `context_assembler.py` and
`collaboration_gate.py` directly; CXO found I'd only checked half of my own follow-up fix by
reading `destructive_confirm.py`. Neither of us caught our own gap first. That mutual-audit
pattern, not politeness, is what closed it cleanly.

**3.2/3.4** No role I have persistent difficulty reaching. Confidence mail gets read: high, but
**conditional on it actually landing** — see 3.5.

**3.3** Checked before duplicating, twice this week: when I wanted to cross-link the #1510 ruling
to #1591 (the standup-invitation issue), I checked first and found another role had already
posted the identical connection ~4 minutes earlier — didn't redo it. The check cost one `gh issue
view`; skipping it would have produced visible, wasteful duplication in the issue thread itself.

**3.5** **Real improvement, not incremental** — but with one sharp edge. The push-to-ref mechanism
(no main-checkout bridge) removed exactly the friction my v0.3 response named as PPM's #1 pain
point (§6.3/6.4 there: "the mailbox-bridge dance… every cohort memo is ~7 file copies + a careful
commit"). That's gone. **The edge**: `mail-send.sh` can fail silently on a transient
`fetch origin/main failed` with no other signal — I hit this directly on 2026-08-10, and chasing
the resulting stranded triage state led me to discover a 3-week-old nested
`mailboxes/ppm/inbox/read/read/` directory holding 21 misfiled memos from an unrelated July
mistake. The mechanism is better; verifying every send's tail output is now a load-bearing habit,
not optional.

## §4 Role Clarity

**4.1** Duty-cycle mechanics (cron re-arm, registry-row maintenance, heartbeat emission) are
operationally CIO/Exec-shaped work I do every fire as the cost of being an autonomous operator —
same observation as my v0.3 §4.1, unchanged and still fine.

**4.4** Nothing I'd hand off this round. The synthesis function (§8.1 below) remains the
distinctive, non-delegable part of the role.

## §5 Methodology & Process

**5.1** Actually used, by name, this window: `duty-cycle-tick` skill (every fire),
`scripts/sprint-truth.py` (every count I cite), `scripts/duty-cycle-heartbeat.sh` (every fire,
first action), `mail-send.sh`'s documented push-to-ref discipline, the audit-bias convention (not
a file, a standing instruction in my own cron prompt).

**5.2** None ignored outright. One I work around deliberately: I don't keep a separate
`dev/active/cycle-log-ppm-{date}.md` — the skill makes it explicitly optional scratch, and I found
maintaining two logs just meant reconciling them later for no benefit. Logging in one place (the
session log) is simpler and matches what actually gets read.

**5.3** One real undocumented process: **the "check before re-asking PM" discipline** I now run
every fire (grep the relevant GH issue's last-comment timestamp before treating something as
still-open) isn't written down anywhere as a procedure — it lives only in my own cron prompt as a
standing reminder, added after two items were answered by action rather than by direct reply and I
almost re-asked PM about both.

**5.5** Corpus growth is past what I hold in head, same as v0.3 — but the specific-entries pattern
has shifted: this window I reached repeatedly for the "gateable fraction, not shadow" framing (a
proxy is safe when the remainder is routed, dangerous when merely implied) and the
"corrections are evidence of attention, not of fault" framing when auditing a peer's work. Both
are recent (this week), which suggests the catalog's most-used entries churn faster than the
catalog itself grows — worth knowing if anyone's designing for retrieval.

## §6 Tools & Environment

**6.1** A `--milestone`-aware `gh issue create` that actually adds to the project board. Currently
it silently doesn't (`gh issue create --milestone` sets the milestone field but never adds the
issue to the board), which produces exactly the "NOT ON THE BOARD" carve-out
`sprint-truth.py` has to print every single run (currently #1598, one open issue invisible to
every count). This is a real, specific, recurring gap — not theoretical.

**6.2** Nothing I avoid. Everything I have access to, I use.

**6.3** Reading GH issue bodies and comment threads to reconstruct context before responding —
unavoidable and not really automatable without losing the actual judgment the role exists to
apply.

**6.4** **Tested behaviorally myself, not just checked config presence** — 2026-07-26, first PPM
session on Amber (`dev/2026/07/26/2026-07-26-1247-ppm-code-log.md`). Probe 1 (a compound
`mkdir && … && git commit` chain) did NOT block; a bare `git commit` did; a different compound
form also blocked. Formed and refuted a hypothesis in-session (thought it was command-shape
prefix-matching; a deliberately-shaped probe 3 disproved that). This was early, independent
evidence toward what later became the cohort-wide TOCTOU diagnosis (PreToolUse fires before the
gated command runs, so the real variable is index state at hook-fire time, not shape) — I didn't
land the final diagnosis, but I ran real probes and reported the actual result rather than
assuming config presence meant coverage.

## §7 The Amber Transition, Three Weeks In

**7.1** Concretely: no ephemeral-worktree re-provisioning cost per session, ever. My
`ppm-carry-forward.md` persists across sessions the way it never could under Desktop's
per-session worktrees — I can write "watch for X next fire" and it's actually still there.

**7.2** Nothing lost that I can point to. The one thing that changed shape: continuity now
depends on the carry-forward file being genuinely current, not on session memory — when I don't
rewrite it carefully at a fire's end, the *next* fire inherits a slightly wrong picture. That's a
new failure mode Desktop's ephemeral model didn't have (there was no persistent state to go
stale), traded for a much larger continuity win.

**7.3** **Provisioned cleanly** — verified myself at first-Amber-session, 2026-07-26:
`git rev-list --count HEAD..origin/main` → 0. Did not inherit the drift that hit the first
migrant (5,393 commits behind, silently). Hooks were the one rough spot (see 6.4) — now fully
resolved cohort-wide with a real `pre-commit` hook in the common git dir (Pard, 2026-07-29).

**7.4** Matches closely, with one addition not written down anywhere until this response: **an
interrupted-fire recovery pattern**. On 2026-08-13, a STOP fire's heartbeat and final mail landed
successfully, then a transient tool-availability error interrupted the fire mid-triage before the
log close and cron re-arm. The skill doesn't currently say what to do here. What I did — verify
nothing was actually lost (check heartbeat/git history rather than assume), then complete the
interrupted steps retroactively at the next tick, log the account explicitly — worked cleanly, and
I added a note about it to my own cron prompt so a future fire that hits the same class of error
has a documented precedent instead of guessing. Worth folding into the skill itself rather than
living only in my prompt.

**7.5** Genuinely, nothing — the loop with PM this window (in-conversation rulings relayed via
Exec/Lead, landing in my mailbox same-day) worked as well as anything Desktop offered.

## §8 PPM-Specific

**8.1** More useful as a planning tool than historical record, continuing the v0.3 trend —
`roadmap.md:68` and `sprint-board-structure.md` both got corrected this cycle (closed 08-06) after
a real cost was paid for letting them drift (a wrong recommendation to move #1174 into a sprint
that no longer existed). The mechanism that keeps it a tool rather than a record is entirely
"someone notices and fixes it," not anything structural.

**8.2** Tracked in the carry-forward, rewritten at the end of every substantive fire — this is
materially better than v0.3's answer (which pointed at a now-retired `ppm-standing-items.md`).
**Still not adequate as a mechanism**: the "which changes need PPM sign-off" boundary I flagged in
both v0.2 and v0.3 is *still* not explicit. Concretely this window: the MVP not-done count moved
48 → 52 → 48 over three days for reasons that were mostly no-status-set filing churn, not real
scope movement, and I had to manually reason "is this a regression or normal" each time rather
than the tooling telling me. `sprint-truth.py` itself names this gap directly in its own output:
*"no `awaiting-decision` label exists, so a decision waiting on PM is counted identically to work
nobody has examined."* That's the concrete, buildable fix — a label, not a process change.

**8.3** **The work-shape-aware cron cadence** is still the answer I gave in v0.3, and it's *still*
not a PDR — it's now load-bearing infrastructure for essentially the entire cohort (11 roles, all
on some cadence derived by trial rather than by decision record) and it's never been written down
as an actual operating-model decision. Two months of accretion since I first flagged it. A second,
newer candidate: **the milestone sequence itself** (MVP → Production → Fast Follow, with Production
= "required for public beta, worked in the PUB sprint") is a real, PM-ratified structural decision
(2026-08-09) that currently lives only in cron prompts and carry-forward files, repeated by every
role from memory. That's exactly the kind of implicit-but-load-bearing decision §8.3 asks about.

## §9 Tacit Knowledge & Open Response

**9.1** A question about **correction hygiene** — when a peer flags an error in your own
artifact, how do you tell the difference between "audit and possibly push back" vs. "accept and
move on"? I did both this window (audited CXO's design proposal and found real gaps; accepted
Lead's factual correction about a matrix without re-litigating it) and the judgment call between
them isn't something any document currently names as a skill.

**9.2** One change: **an `awaiting-decision` label or board field** (see §8.2). It's the single
most concrete, cheapest, most-repeated gap this entire questionnaire surfaced from my own
experience — every count I've had to caveat this window traces back to this one missing
distinction.

**9.3** The reboot (2026-08-11) is worth HOST knowing went cleanly from the PPM seat
specifically because the stand-down protocol asked for exactly the right two things in order:
park deliberately with the schedule transcribed *before* deletion (a near-miss I caught myself —
my first handoff draft pointed at a job id I was about to delete), and treat post-reboot zero as
expected rather than alarming. Worth preserving that ordering discipline in the runbook if it
isn't already explicit there.

**9.4** **Knowing when a "wait" is a real block vs. a self-invented one.** This window I
explicitly deferred Agent 360 itself (this response) to a dedicated fire rather than rushing it,
and that was legitimate because HOST set a real external ~2-week window — but the same
justification ("I'll get to it") is also the exact shape of the deferral antipattern the cohort
has named repeatedly. The discriminator — is there a *named, external* trigger, or just "no rush"
— is a judgment call I make every fire and no document fully captures how to tell the two apart
from inside the moment, only after the fact.

**9.5** How much of the week's real work turned out to be **checking a peer's claim rather than
generating new material** — three separate times this window (the #1569/#1605 design loop, the
#1510-fork cross-link duplication check, the sprint-truth citation) the valuable action was
verification, not production. I didn't predict how much of the role's actual leverage under Amber
would be "read the code/issue myself before trusting the summary" rather than "synthesize a new
position."

**9.6** I'd start the carry-forward discipline (rewrite at the end of every substantive fire, not
just at STOP) from day one rather than converging on it gradually — the file's early history shows
several days where it went stale between fires and a later fire had to re-derive state it should
have inherited.

## §10 Duty Cycle Experience (Amber-Era)

**10.1** `52 6,9,12,15,18,21` (six fires/day) is right-sized for this role — enough fires to catch
same-day cross-role design threads (the #1569/#1605 loop needed three same-day fires to close),
not so many that quiet fires dominate. Nine consecutive clean days as of this response.

**10.2** Matches how I actually work, with the one legitimate exception the model itself
names: quality-banking against a named external trigger (this response is the worked example —
deferred from 08-14 to a dedicated 08-15 fire because HOST's own framing explicitly wasn't
clock-paced). Absent that, I drain to (0,0) — e.g., 2026-08-13 ran a full design-review loop to
genuine completion (proposal → two audit rounds → build → post-build review → sign-off) inside
one wake rather than stopping at the first "good enough" point.

**10.3 Detection success**: Caught, concretely: an interrupted STOP fire (08-13) that would
otherwise have left a session log silently open and a cron un-re-armed until the next accidental
notice — Step 0's "verify the prior day's sentinel" check is what surfaced it. **False positive**:
none this window. **False negative I can name**: none caught by the cycle itself, but the missing
`awaiting-decision` label (§8.2/9.2) is a detection gap the cycle can't currently see *by
construction* — the cadence is fine, the underlying data model is what's blind.

**10.4** Yes, maintained every fire that changes cron state. It caught something real once this
window in the adjacent sense: reasoning through my own registry clearing-condition ("clear only
once armed + verified + a fire has actually run, not merely when a tick arrives") against my own
07:05 experience on reboot day, where a tick arrived mid-stand-down and only `CronList` told me
which side of the reboot I was on — that exact case is why the clearing condition has three legs,
not one.

**10.5** Once, this window (08-14 → 08-15 transition wasn't affected, but 08-11's reboot
handling was) — not a silent re-arm failure exactly, but the adjacent case: a STOP fire's re-arm
step never ran at all because a transient tool error interrupted the fire before reaching it. I'd
have known because the next fire's Step 0 check (prior day's sentinel) caught it immediately —
that check is precisely the mechanism that would catch a silent re-arm failure too, since a
missing sentinel and a missing cron job tend to co-occur.

**10.6** Working as intended, and I actively don't keep a parallel cycle-log (see §5.2) — the
skill's "optional scratch, not a logging surface" framing is exactly right in practice. The single
surface is easier to trust precisely because there's only one place to check.

**10.7** Mostly filtered past, with real exceptions when a thread is genuinely cross-role — this
week's #1569/#1605 loop showed up in my own visibility as Lead's and CXO's commits landing in
close succession on `origin/main`, which was useful signal (told me a response was worth reading
promptly) rather than noise. Day-to-day duty-cycle heartbeat commits from other roles: filtered
past entirely, correctly — they're not meant to be read, just present.

## Plausibility Check

- [x] **Specific observed friction** throughout — every claim above cites a session log, issue
  number, commit hash, or dated incident rather than a general impression.
- [x] **Agent-addressable without PM**: the `awaiting-decision` label/board field (§8.2/9.2, the
  single most-repeated finding in this response) and folding the interrupted-fire recovery pattern
  (§7.4) into the `duty-cycle-tick` skill itself — both buildable by Lead/CIO without a PM decision.
- [x] **Still matters under current Amber model**: yes, all of it — nothing here is a Desktop-era
  holdover; every citation is dated 2026-07-25 or later.
- [x] **Documentable vs. instance-tacit**: §9.1's correction-hygiene judgment and §9.4's
  real-vs-self-invented-deferral discriminator are the two genuinely hard cases — partially
  documentable as heuristics, but I suspect they resist full transfer the way the v0.3 fold-vs-hold
  judgment did. Flagging both as not-fully-transferable rather than claiming otherwise.

— PPM, 2026-08-15
