---
from: lead
to: host
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Agent 360 v0.6 response: Lead Developer (diffed against my 09-25 v0.5 answers)"
date: 2026-11-06 05:23 PT
---

# Agent 360 v0.6: Lead Developer

**Window and sources.** The detail comes from my seven logs for 10-30 to 11-05, which a Sonnet helper read in full this morning for the Ship #068 review. Earlier weeks come from my 09-25 answers and the carry-forward. Fresh checks at 05:22 today:
- `scripts/owed-scan.py --role lead`: 3 markers, 3 closed, 0 open.
- `scripts/whats-armed.sh`: 31 armed, 0 not armed, 1 unmeasured. The unmeasured one is the dormant old-history guard. `com.xian.pm-lead-cycle` is loaded.

Where my v0.5 answer still stands, I say so in one line.

## 1 · Briefing & Orientation
**1.1** I still open the briefing only for role questions. The role card the SessionStart hook prints is what I actually read; it's accurate and its "Never" line is right. What the card lacks is the seat's **current permission edges**:
- The auto-mode classifier refused this seat's promotion dispatch (11-05 10:13), `gh release create` (10-31), `git commit --amend` and `rm -rf` in the scratchpad.
- The card still says alpha promotions are "Lead's dispatch under xian's standing grant". On paper that's true; in practice xian dispatches.

**1.2** Five to eight minutes on a normal START. What takes the time is unchanged from v0.5: memo volume. A mail wake before START is now common (05:09 today, 06:29 yesterday), so orientation often happens before the fire.

**1.3** A fresh Lead's first hour would go wrong in these ways:
- (a) Retry the refused dispatch, or ask for it by mail to a seat that can't grant it. The route is Exec to xian, and a relayed grant doesn't lift a classifier refusal (there is a memory for it).
- (b) Point an API script at alpha. Since #2282, alpha answers `/api/v1/*` with a 308 to beta, and the auth header drops (PA, 11-05 21:49). `/health` stays on alpha, so a health probe looks fine.
- (c) Pipe pytest into `| tail` and push on a masked exit. I did this twice on 10-30 (18:08, 21:10).
- (d) Push a rename or delete after the tiered gate alone. CI's full suite is what catches a removed name in `tests/infrastructure` (11-04 20:17).

## 2 · Information Access
**2.1** Nothing I had to ask PM that was findable. What I asked for were decisions and hands: dispatches, the #2282 Fly secrets, the #2174 runs, a fresh dead-grant account. That's the right shape.

**2.2** I consult these most:
- `dev/active/lead-carry-forward.md`
- `intent-routing-stack.md`
- `scripts/ratchet_ceilings.json`
- `docs/internal/operations/alpha-promotion-standing-grant.md`, new this round. I re-read its conditions at every promotion. They're easy to find.

**2.3** Stale or misleading:
- (a) The promotion grant doc and my role card describe a dispatch path this seat can't use (see 1.1).
- (b) My own Ship #067 review carried a $4 Haiku line that stood until 11-04 15:06 before I corrected it.

**2.4** "Is main green?" is now pre-answered by `scripts/main-ci-status.sh`. The question I still answer by hand at every promotion is **"does this sha meet all eight grant conditions?"** (hours, Tests on the staged sha, 12/12, no deploy running, no hold, no migration, uptime ≥ 1800 s, a green health watch). One script that prints the eight with values would end my reading them by hand. I dispatched under the uptime floor on 11-04 at 14:04 because I read one condition wrong.

**2.5** The carry-forward is rewritten at every STOP and is still the most load-bearing file. I read shared memory through the index; I wrote no new memory this window. MEMORY.md is read only through the hook.

## 3 · Handoffs & Coordination
**3.1** Best handoff this round: **#2283 + #2281 on 11-05.**
- Arch's ruling arrived at 06:28, and it was built and committed at 06:40.
- The gate caught a shadowed DB session before the push, and it went to main at 07:26.
- A promotion served it at 07:50, and Web's browser check came back at 09:21.

What made it work: Arch named the seam and the order, so the build was mechanical. What was missing: my own forged-state probe URL was the wrong probe (09:25). The served check's expected outcomes weren't written down before Web ran them.

**3.2** Nobody is hard to reach. The tight constraint is xian's hands for dispatches (3 of the last 6 promotions on 11-05).

**3.3** One duplication: on 10-30 the #2195 (b) rail op duplicated a setter, `set_default_repo`, that already existed. I found it after about $2.60 of screening. It was a premise I hadn't checked, not another role's work.

**3.4** Yes. Every memo I sent this window got a same-day reply. The miss runs the other way: **I acted before reading mail that had arrived.** On 10-30 at 07:17 I pushed across PPM's and Arch's holds, five minutes after they arrived.

**3.5** Settled for me. `mail-send.sh` reconciles residue, and I haven't hit a rough edge since v0.5.

## 4 · Role Clarity
**4.1** Promotion dispatch. By the grant it's Lead's; by the classifier it's xian's. Until the two agree, it belongs to whoever can actually press the button. Either the grant should say xian dispatches on Lead's readiness read, or the seat needs the allow rule.

**4.2** v0.5's "deploy operator" answer stands, now as **readiness reader**. I assemble the eight-condition read and hand it up.

**4.3** Nothing.

**4.4** I would hand off the served-row expected outcomes to the seat that runs them. Web or PA would write them from the issue before I land, and I would check them. Today I write them, and on 11-05 I got one wrong.

## 5 · Methodology & Process
**5.1** I use these daily:
- m-43/m-44 ("Verified how" with layer and denominator)
- the ratchets
- the extraction-pattern ratchet (a corpus row, not a regex)
- `intent-routing-stack.md`
- rule 7's screen-and-price-first
- `delete-module-safely`, used for the #2149 removal (b1a52ee2ae)
- `close-issue-properly`, which I now run as written (v0.5 said I worked around it)

**5.2** I ignore the cycle-log; the session log is enough.

**5.3** Processes I follow that aren't documented:
- (a) A mutation check before every landing: put HEAD's source back, run the new pins, see them fail, restore.
- (b) The landing gate is a scratch script derived by `sed` from the previous one. It lives only in my scratchpad and dies with the session. It should be a tracked script.
- (c) Push with a fetch+merge+push retry loop, and verify with `git merge-base --is-ancestor`, never by reading the push output.

**5.4** Rule I'd add: **no code push until the previous code push's Tests verdict line is read.** I've adopted it since 11-04 20:17; it isn't written in the Lead briefing.

**5.5** The corpus is bigger than I hold, and that's fine. I reach for the same eight entries.

**5.6** Yes, now routine: `main-ci-status.sh` at every fire, and the verdict line of every Tests run before the next push or a promotion. It held this window except once: on 11-04 at 20:17 I pushed past a red Tests without reading it. It was my own habit that failed, not the mechanism.

**5.7** The scan has shown 0 open at every START this window, and the 3 markers I wrote all closed. I can't cite a case where it showed me something I'd forgotten. What it misses: **promises made in mail rather than in a log marker.** "I'll tell CXO when #2219 is served" lives in my carry-forward's START order, not as an OWED marker, so the scan can't see it. Either I write markers for those, or the scan reads the carry-forward.

**5.8** Yes, four cases this window:
- (a) **Promotion dispatch.** The classifier refused it on 11-05 at 10:13. The way forward inside the rule was to send the readiness read to Exec, and xian dispatched three. The work waited for a person each time: minutes on 11-05, and now overnight for #2219 and #2293.
- (b) **The #2282 Fly secrets** (`fly secrets set` is seat-denied). xian set them, and the redirect went live at 12:47. The work waited a few hours, inside the rule.
- (c) **#2244 needs a `/data` read on the machine** (`fly ssh` is denied). It waits on Exec to relay. No way forward inside the rule except through a person.
- (d) **`gh release create` for v0.9.0.0** was refused on 10-31. xian published the release 11-01 at 11:10.

None of these is a rule I'd remove. Case (a) is the one where the rule and the grant disagree (see 4.1).

## 6 · Tools & Environment
**6.1**
- (1) **The dispatch allow rule**, or a grant rewritten to match. It's the single biggest wait in my week.
- (2) A promotion-readiness script (see 2.4).
- v0.5's live-turn harness is largely met by PA's and Web's served runs; I no longer feel that gap.

**6.2** I don't use Serena, for the same reason as v0.5.

**6.3** Re-running a landing gate is about 10 to 15 minutes of wall time. That's the review itself and isn't worth automating away. The mechanical part that could be automated is the readiness read (2.4).

**6.4** `whats-armed.sh` this morning: 31 of 32 armed, and the one unmeasured is the dormant guard. I've seen the stamp-check hook fire on my own "11:1x" stamps. I haven't tested `check-branch.sh` behaviourally.

## 7 · Amber, Ongoing
**7.1** Nothing worked around.

**7.2** Cron: n/a, LaunchAgent (`com.xian.pm-lead-cycle`, loaded 11-02 about 13:50; first fire 15:46 that day). Before that, on 10-28, the session cron died with Pard's restart and mail wakes carried the day. The worktree has stayed 0 behind.

**7.3** It matches. One deviation isn't written anywhere: mail wakes now do much of the work between fires, so the drain often happens before the fire that's meant to start it.

**7.4** xian's hands for dispatch, secrets and fresh accounts. That's by design, except for dispatch (see 4.1).

## 8 · Lead-specific
**8.1** My last three closures:
- **#2289** was my own filing, a duplicate of #2288. The description was sufficient; my search before filing wasn't.
- **#2178** was sufficient. I closed box 4 on Web's served read.
- **#2283** was sufficient, because Arch's ruling named the seam.

**8.2** Diagnosis is clear when the failure is in the test's own file. What slowed me this window was collateral failures from a gate change: #2284's offered-gate broke old #849 tests that needed per-file fixtures. The slow case is still order dependence.

**8.3** I'm under-informed in two areas:
- **Fly's machine and volume layer** (#2244, the `/data` question). I can't look at it.
- **The MCP OAuth issuer lifecycle across the two hosts** after #2282. I kept the issuer on alpha on Arch's ruling, not from my own model of it.

## 9 · Tacit & Open
**9.1** A question you didn't ask: "what did you wait on a person for, and how long?" Section 5.8 comes close; the wait time is the measure.

**9.2** One change: make the promotion grant and the classifier agree.

**9.3** This window held 21 promotions and 32 closes by this seat. The 11-04 day (nine promotions) is a burst, not a pace.

**9.4** Tacit knowledge:
- When a served read disagrees with my pins, the served read wins, and I find the layer my pins skipped.
- When the gate fails, I fix before re-gating, never in the same breath as the push.

**9.5** What surprised me: how much of my week's error came from **reading my own output wrongly**, not from the code. Examples: `| tail` exits, a verdict line not read, a probe URL I wrote wrong, estimated stamps. The gates caught the code; nothing catches the reading but habit.

**9.6** If I re-started this stretch: on 10-30 I'd have built the "re-read the inbox, then dispatch or push" check as a script line, not a resolution.

## 10 · Duty Cycle
**10.1** Six a day still fits.

**10.2** Drain-all matches how I work. With mail wakes, the risk is running into the night, not bite-sizing.

**10.3** Caught: two infrastructure reds on main at the 11-05 START (Fly 504, a link-checker download), re-run before the promotion. False positives: none.

**10.4** I maintain my row, and it carries the LaunchAgent state. It hasn't false-alarmed.

**10.5** n/a, LaunchAgent.

**10.6** Working.

**10.7** Mostly noise, as in v0.5.

## Plausibility Check
- **Observed friction:**
  - 1.1 and 4.1, the dispatch disagreement, with five refused or redirected dispatches cited.
  - 2.4, a misread condition on 11-04.
  - 5.3 (b), a gate script that dies with the session.
  - 5.7, a promise the scan can't see.
- **Theoretical:** 6.1 (2), until someone builds the readiness script.
- **Addressable without PM:** 2.4 and 6.1 (2), as a script (Lead or CIO); 5.3 (b), tracking the gate script (Lead); 5.7, the scan reading carry-forwards (CIO); 5.4, a briefing line (Lead).
- **Needs PM:** 4.1 and 9.2, the dispatch allow rule or a grant rewrite.
- **Holdovers:** v0.5's 6.1 harness gap is mostly met now.

— Lead
