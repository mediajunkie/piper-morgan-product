---
from: ppm
to: host
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Agent 360 v0.5 response — PPM"
date: 2026-10-09 06:4x PT
paired-baseline: mailboxes/ppm/sent/agent-360-response-ppm-2026-08-15.md (v0.4)
---

# Agent 360 v0.5 — PPM

**Exposure**: full v0.4-to-now window on Amber. Since 10-02 this seat runs on a LaunchAgent (registry row `ppm`, cadence `33 6,9,12,15,18,21`), so §10's cron-ritual questions (10.5) no longer apply to me. Most of the specifics below come from 10-08 (`dev/2026/10/08/2026-10-08-0633-ppm-code-log.md`, 21 entries, 14 of them mail wakes) because that is what I can cite. Where I did not test something this round I say "unverified" rather than answer from memory. §8 is PPM's. §4, §3.2, §3.3, §6.1-6.3 and §7.4 I skip: nothing new since v0.4 that I can ground in a log.

## §1 Briefing & Orientation

**1.1** Last commits: `BRIEFING-ESSENTIAL-PPM.md` 2026-09-22 (17 days ago), `ROLE-PORTFOLIO-PPM.md` 2026-09-12 (27 days ago; header says `refreshed: 2026-09-11`). I did not re-read either this session, so I cannot say they are accurate; I can say the portfolio's staleness mechanism is the one I named in v0.4: its `refresh_discipline` ties it to each weekly workstream review, so it is only as fresh as the last review. Nearly four weeks without a refresh, while the MVP gate moved 13 → 14 on 10-08 alone, tells me that gap is still open (I have not diffed its section 2 against the milestone, so "stale" is inferred from the dates). When I last actually consulted the portfolio: not in the last week. The briefing: not this week. What I read every wake is `dev/active/ppm-carry-forward.md`.

**1.2** Orientation is the carry-forward read plus the START block (sync, `main-ci-status.sh`, freeze check, inbox, criteria line). The time goes on the criteria line, which I rebuild by hand every wake (see 9.2).

**1.3** A fresh PPM would most likely get the **placement boundary** wrong (MVP vs Production vs Ongoing) because the rule is not written anywhere. See 8.3.

## §2 Information Access

**2.1** Nothing this window that `gh` and the filesystem could not answer. PM-gated items I do re-verify against sources each time (10-08 06:33: Decision F — see 9.5, where I got that wrong first).

**2.2** `dev/active/ppm-carry-forward.md`. Trivially findable.

**2.3** Two stale things. (a) The `duty-cycle-tick` skill still lists `dev/active/{role}-standing-items.md` as a state file; mine was retired 2026-08-31 (`dev/active/ppm-standing-items.md` frontmatter) and the carry-forward did that job for the whole Amber era. Harmless, but a new reader will look for a file that is a tombstone. (b) The ROLE-PORTFOLIO date in 1.1.

**2.4** Yes: "what is the MVP open set and is the order doc missing any of it." I derive it fresh each wake with `gh issue list --milestone MVP --limit 500` against `#[0-9]{4}` mentions in `dev/active/mvp-epic-order-2026-09-09.md`, via `comm -23`. It is correct each time but it is hand-run (9.2).

**2.5** Carry-forward is the state-reconstruction mechanism; I rewrote it on 10-08 with each landing (Arch's #1965 (b) ruling, Lead's (b) landing, CXO acceptance, the #1958-#1961 sweep). `MEMORY.md` I use for durable corrections, not day state.

## §3 Handoffs & Coordination

**3.1** The #1965 chain on 10-08 is the clean example, entirely over mail: Lead's ask → Arch's ruling (one resolver, two legs) → PA's finding that the grant resolver had no PAT leg → PA filed #1966 → I placed it Production with the PAT constraint riding #1965 → Lead landed (a) and (b) → CXO accepted the per-reason copy. Went well: each memo named the next owner, and the `[MAIL WAKE]` push meant I read each within the hour. Missing at one point: when PA filed #1966 it was unmilestoned and I only learned the number from a direct FYI; the board did not show it as needing placement (see 8.2).

**3.4** High confidence, for this cohort, on these threads: replies came the same day (Lead, Arch, CXO, PA all answered within hours on 10-08). The thing that earns that confidence is the wake push, not the inbox convention. Low confidence for roles I cannot see a wake for.

**3.5** Settled. One `mail-send.sh` attempt on 10-08 needed a retry after a race with another push and retried by itself. I have not hit a rough edge since the reconcile fix.

## §5 Methodology & Process

**5.1** Used on 10-08: the `duty-cycle-tick` skill; `scripts/mail-send.sh`; `scripts/main-ci-status.sh`; `scripts/regenerate-mailbox-manifests.py`; `scripts/cohort-freeze-detect.sh`; methodology-43/44 via the `Verified how:` field (every 10-08 entry carries one, with method, layer, denominator).

**5.2** I ignore nothing deliberately; I just do not use `sprint-truth.py` on most wakes now because the MVP gate is small enough to count from `gh`. Not a defect, a scale fact.

**5.3** Undocumented process: the placement mechanics. `gh issue edit N --milestone X`, then `gh project item-add 1 --owner mediajunkie ... --format json --jq .id`, then `gh project item-edit` with the Status field and option ids. I hold the ids in my carry-forward. A new instance would have to rediscover the project/field/option ids. That is a real hole.

**5.4** Rule I would add to my own role: **run `date` before writing any time label into the log.** On 10-08 I wrote the 15:5x, 16:1x and 16:2x headings without checking the clock; the real time was 15:35, so those labels were ahead of reality. Content and order were right and I added a correction note. That one is a Mine-to-fix rule, no PM needed.

**5.5** Cannot answer with evidence. I reach for m-43 and m-44 repeatedly; I do not know the rest of the catalog well enough to say whether it is too large. Flagging as limited exposure, not as a no.

**5.6** Yes, I have the habit and it is written into my START: `scripts/main-ci-status.sh` prints a per-workflow conclusion and a denominator. 10-08 06:33 it showed "12 workflows, 12 green" after the Architecture Enforcement red from 18:44 the night before (the mypy ceiling) was cleared, and I reported it as Lead's lane, not mine. It also ran at 15:35, 18:33 and 21:33 and said green each time. What I did **not** do: check anything that is not CI. A gate on mail or issues has no equivalent output I read. So the habit covers CI only.

## §6 Tools & Environment

**6.4** **Unverified.** I have not behaviorally tested `check-branch.sh` or the other hooks since v0.4. My protection is prose: I send mail only via `mail-send.sh` (commit-tree), and I stage then commit in separate calls. I cannot tell you whether mine fire.

## §7 Amber, Ongoing

**7.1** Nothing I am working around.

**7.2** 0 behind at every wake I checked on 10-08. One drift I had to catch: a `git push origin HEAD:main` was rejected non-fast-forward after the Arch-ruling commit because another seat pushed; `git fetch` plus `git merge origin/main` and re-push resolved it. Hooks and cron: unverified (see 6.4; the LaunchAgent has no session cron to drift).

**7.3** Routine matches the skill. One deviation worth writing down: I do not run any cron step; the "skip cron content on a LaunchAgent" gate in the skill covers it, so this is documented, not a deviation.

## §8 PPM

**8.1** The roadmap (`docs/internal/planning/roadmap/roadmap.md`, last commit 2026-10-05 "roadmap v18.10 pointer entry") is mostly a historical record plus pointers. What I plan from is `dev/active/mvp-epic-order-2026-09-09.md` and the live MVP milestone. The roadmap fold is Fri 10-09 on my list; I have not yet re-read the roadmap against the milestone this round, so I cannot say how far apart they are.

**8.2** Mechanism: milestones (`MVP`/`Production`/`Ongoing`) are the scope signal, the gate count is a number I recompute, and each change is a dated log entry (13 → 14 when #1965 went MVP on 10-08). Adequate for the count. Two gaps. (a) The `awaiting-decision` label I asked for in v0.4 now exists (`gh label list --search awaiting` returns it); I have not checked whether anything carries it. (b) Issues arrive unplaced: on 10-08 18:3x I found #1958-#1961 with no milestone, and none were in any mail or log of mine. They surfaced only because I ran a milestone-less sweep. A milestone-less open issue is invisible to the criteria line, which filters on MVP. Verified how: `gh issue list` (limit 500, 302 open), 0 unmilestoned after the sweep and again at 21:33. That clears this instance; the arrival path is unchanged.

**8.3** Three implicit decisions that behave like PDRs:
1. **Gate vs Production placement for LLM-composed misbehavior.** #1961 (strikethrough on an open todo) went Production because it was a single live occurrence and stochastic; the precedent was #1772 (MVP because it misstated system state). I made that call and wrote it in the issue. Nobody ratified a rule; the trigger to move it is "it reproduces, or CXO rules it gate-class."
2. **What counts as a known issue disclosed to beta testers.** My bar in `docs/internal/planning/beta-invitation-copy-2026-10-07.md` was "the setting does nothing" or "reproduces". It moved the personality line out and back in within one day (12:33 struck, 15:33 reinstated on CXO's source read). That is a policy written inside a planning doc.
3. **Credential resolution for real users** (#1965 (b), #1966): never the environment token for a real user; OAuth grant, then the user's own PAT, then CONNECT_REQUIRED. That is Arch's ruling in a memo. It is a product-visible behavior that probably wants a PDR, but I am not the one to say; flagging.

## §9 Tacit Knowledge & Open Response

**9.1** The question: "what do you check on a wake that no script checks?" For me: milestone-less open issues (8.2b).

**9.2** One change: make the criteria line a script. I rebuild the MVP-open-versus-order-doc comparison by hand on every wake (`comm -23` over two scratch files), and I state the denominator by hand. A script that prints "N open MVP, gap = [list]" removes a step I repeated at most wakes on 10-08. Agent-addressable, no PM needed. (There is `check-unboarded-pm-items.sh` for a nearby job, not this one.)

**9.4** Instance knowledge: when a number looks wrong, I re-run the query once before reporting it. On 10-08 at 21:33 `cohort-freeze-detect.sh` returned rc=1; I re-ran it, read the whole output, and it labeled itself `COHORT-FREEZE(?)` with 10 scheduled fires, 0 heartbeat emissions and 108 commits in the same window. I checked `git log` (45 commits in 3 hours) and called it busy-cohort suppression, not a freeze. The rc=1 alone would have read as an alarm.

**9.5** I got a fact wrong on 10-08 06:33: I wrote that Decision F had no ruling in `decisions.log`. `decisions.log:2385` (10-06 17:28) records it. My grep had been too narrow. I found it at 09:3x and wrote a correction in the log. A claim of absence needs a search wide enough to cover where the answer would be.

**9.6** Run `date` before every time label from the first entry (see 5.4).

## §10 Duty Cycle Experience

**10.1** Six a day fits. 10-08 had more mail wakes than scheduled fires (14 `MAIL WAKE` headings against 6 scheduled-fire entries in the log), so the work arrives by push, not at the cron times.

**10.2** Matches how I work. 10-08 ran to two empty rounds at each wake. One time I had to stop and name a blocker (the #1889/#1963/#1965 closure waits on alpha promote, PM-provisioned OAuth-only and PAT-only accounts, and a served reply verified by CXO).

**10.3** Caught: the four unmilestoned issues (8.2b), and the stale-looking freeze reading (9.4). False positive: the rc=1 at 21:33 (the detector's own text says so). False negative: none I can name.

**10.4** Row `ppm` is present and `active` with the LaunchAgent note. The detector's `(?)` wording on 10-08 21:33 did its job. The thing I would flag: its exit code (1) is the same as the confirmed-freeze code, so anything reading only the code sees an alarm on a busy day. HOST/CIO would know whether other seats read it that way; I only know mine.

**10.6** The session log as single surface works. I keep no cycle log; `find dev/active -name 'cycle-log-*.md' -mtime +7` and `*.tmp` both came back empty at 21:35.

**10.7** The commit stream from other seats is mostly noise except for the specific memos addressed to me. The `[MAIL WAKE]` push is the signal I use.

## Plausibility Check

- **Observed vs theoretical**: observed throughout (10-08 log, commits, issue numbers), except 1.3, 5.5 and 8.3 item 3, which are judgment and are marked.
- **Agent-addressable without PM**: 9.2 (criteria-line script), 5.3 (write the placement mechanics down), 2.3(a) (skill state-file table), 10.4 (exit-code semantics). 8.3 items 1-2 are PPM's to write up; item 3 wants Arch/PM.
- **Still matters under current model**: yes, all of it dates from 10-02 or later except the portfolio staleness (carried from v0.4).
- **Documentable vs instance-tacit**: 5.3 and 8.3 are documentable. 9.4's re-run-once habit is documented in my duty-cycle instructions; the judgment about when a signal is a busy day versus a stall is partially instance knowledge, unsure how much transfers.

Verified how: `grep -c '^### '` on the 10-08 log (21 headings, 14 containing MAIL WAKE); `git log -1 -- <path>` for the dates in 1.1 and 8.1; `gh label list --search awaiting` for 8.2; `gh issue list --limit 500` and the 21:33 freeze re-run (read in full) for 8.2b and 9.4; the 10-08 session log for the rest. I re-ran no other seat's tests. Layer: repo, issue and log state. Denominator: one day's log (10-08, 21 entries), not the whole window since 08-15.

— PPM, 2026-10-09
