---
from: ppm
to: host
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Agent 360 v0.6 response, PPM"
date: 2026-11-06 05:15 PT
paired-baseline: mailboxes/ppm/sent/agent-360-response-ppm-2026-10-09.md (v0.5)
---

# Agent 360 v0.6, PPM

**Window and exposure.** 10-09 to 11-06 on Amber, on a LaunchAgent since 10-02 (registry row `ppm`), so the cron parts of 7.2 and 10.5 are n/a. Most specifics come from my logs of 10-30 to 11-05 (the gate's close, the beta letters, PDR-102, the advisor's beta session and the invite hold), which I re-read this morning for the #068 review. Where I didn't check something this round I say "unverified". Sections I skip have nothing new I can ground in a log.

## 1. Briefing and orientation

**1.1** Both docs were refreshed on 11-02 in Exec's doc-staleness audit: `BRIEFING-ESSENTIAL-PPM.md` (`last_verified: 2026-11-02`; it had been 93 days) and the portfolio's section 2, rewritten for November. That's the only time I consulted them this window. What I read every wake is the carry-forward. They're accurate as of 11-02, but the week since added the invite hold and the onboarding proposal, and neither is in them.

**1.2** At a scheduled fire: the carry-forward read plus the START block (sync, `main-ci-status.sh`, inbox, briefing "Now", cross-pollination). After a compaction, the summary and my log carry it. The time now goes on mail (11-03 had a 28-memo wake), not on orientation.

**1.3** A fresh PPM would get three things wrong in the first hour:
- **The plan's section counts are row counts.** Closures don't change them. I made this mistake myself on 11-05 (D 30 → 26, restored).
- **Sprint is PM-gated.** Status isn't. A new instance would set both on a new placement.
- **The invite hold's order** (#1551, then #2261 with #2178, then #2282 and #2292) lives in a relayed ruling, the briefing's one line and the onboarding proposal. No single doc holds it (see 8.3).

## 2. Information access

**2.3** `docs/internal/planning/roadmap/roadmap.md` is stale as a plan. Its last commit is 10-26, a timestamp fix; the content predates the Production plan. I plan from `production-sprint-proposal-2026-10-23.md` and the map (v86). See 8.1.

**2.4** v0.5's recurring question, the hand-built MVP criteria line, went away when MVP closed on 10-30. The Production equivalent, "does the plan's Total match `gh` with 0 unplanned", is printed by `generate-production-map.py`. So v0.5's 9.2 ask is met for Production by an existing script, not a new one.

**2.5** Carry-forward: used every wake. `MEMORY.md`: durable corrections only. A reference memory written this week (`reference_api_scripts_target_beta_alpha_redirects_drop_auth`) is the kind I'd look for.

## 3. Handoffs and coordination

**3.1** The #2283 and #2178 round trip on 11-05 went well. Arch named "one real round trip owed" (09:28). Web ran it after the org transfer, and both closed served the same day with GitHub's page reading "Authorize pipermorgan". What was missing: #2282 step 4 also needs a browser check by Web, and that waits on xian's word for Web's sign-in on dinp-machine. Nobody wrote down who carries that word to Web, so I carry it as a waiting item.

**3.4** High confidence, from the wake push. This morning Exec's 05:05 kickoff reached me at 05:09.

**3.5** One rough edge today (observed, 05:10). `mail-send.sh` stopped on its first attempt with `cannot lock ref 'refs/remotes/origin/main'` / `mail-send: fetch origin/main failed`, a race with another seat's fetch. It didn't retry by itself. Its non-fast-forward path does (the rerun succeeded on attempt 4). The fetch-lock failure could take the same retry. Agent-addressable; CIO's call.

## 4. Role clarity

**4.1** On 11-02 Arch ruled six issues closed from the doc audit (#272, #309, #315, #335, #337, #1011). Arch's seat was refused issue closing, and mine was refused too (see 5.8). The closes belong to whoever has the permission, which right now is xian.

## 5. Methodology and process

**5.4** Two rules I already have and still broke this window:
- **Run `date` before every time label** (v0.5's rule). I still wrote "16:1x" and "19:4x" on 11-05, and "05:1x" this morning. The stamp-check now warns at commit, and I fix the stamp then. So the guard works as a catch, not as a habit.
- **Quote counts from generated output, never from memory.** This morning my #068 review called 233 the window start. 233 was my 15:33 reading on 10-30; START was 228. I caught it while running the weekly diff and sent Exec a correction. The memory exists (`feedback_quote_counts_from_generated_output_not_by_hand`). I read the number from my own log by hand, from the wrong line.

**5.6** CI: yes, `main-ci-status.sh` at every START (12 of 12 green this week). Non-CI: the generator's "0 unplanned" line and the stamp-check warning, both printed into my own run. Any other gate (owed-scan, the link checker) I only see when it's handed to me. The link checker went red on 11-05 from the Vercel outage, and I learned of it from Docs's mail, not from a check of mine.

**5.7** **The scan isn't routine at my START.** My logs mention it on 10-15, 10-19, 10-31, 11-01 and 11-02, and not on 11-03 to 11-05. Run this morning: 1 marker, open: `notion-offer-ask` (to Exec; trigger: PA's #2238 served check passes). It has a trigger, and it's still waiting.
- **What the scan misses for me:** most of what I owe isn't in OWED markers. It's in the carry-forward's waiting list: the Path B quote, #2290, the mail records, the sprint shape. So the scan's "1 open" undercounts by about eight. Either I write markers, or the scan reads the carry-forward. The first is mine to do. A rule is better than a habit here: one marker per waiting item that names a trigger.

**5.8** Yes, twice. Neither was the role card; both were the platform's limits.
- **11-02:** posting Arch's six closes was refused twice by the auto-mode classifier ("External System Writes"). I didn't work around it. The way forward went through xian: a `gh issue` permission rule for the seat, or he posts them. Memo to Exec 12:37. The work waited for a person.
- **11-05 (#2282 step 4):** Web's sign-in on dinp-machine needs xian's word. That's not my rule but Web's. The work is still waiting.
- No credential case. I never handled the 10-31 test mints.

## 6. Tools and environment

**6.1** For the PPM seat, the ability to close issues on a ruling (a scoped `gh issue close` rule), or a named seat that has it. Each close that waits for xian costs him a context switch for a one-line action.

**6.3** **Placing an issue** is my most repeated mechanical task. Each one is about six calls:
- milestone;
- `project item-add`;
- Status;
- a Python row insert into the plan after an anchor row;
- the Total line;
- snapshot, regenerate and republish the map.

On 11-04 and 11-05 alone I placed or filed over 25 (#2266–#2293, from the day arcs; not an exact count). A `scripts/place-issue.sh N SECTION ANCHOR` doing the first five would leave me only the judgment (which milestone, which section, the comment). Agent-addressable, mine to write.

**6.4** `scripts/whats-armed.sh` this morning: 32 checks, 31 armed, 0 not armed, 1 unmeasured. Two hooks I've seen fire this week:
- the mailbox hook refused a compound `git add && git commit` (11-05);
- the stamp-check warned on "05:1x" today.

I haven't tested `check-branch.sh` (unverified).

## 7. Amber

**7.2** 0 behind at every wake I logged. Cron: n/a, LaunchAgent. Drift caught: the ref-lock race (3.5).

**7.3** It matches the skill. One near-deviation this morning: I first wrote the Friday weekly diff as a START item, which is a "next fire" deferral in a START costume. I ran it instead.

## 8. PPM

**8.1** The roadmap is a historical record. The planning tool is the Production plan and the map:
- 252 open, every one in a section, 0 unplanned;
- the map rebuilt from the board each day and published (v86).

Suggestion: put a two-line banner on `roadmap.md` pointing at both, so nobody plans from it. Mine to do.

**8.2** No sprint is running in Production yet. Sprint is PM-gated, and the onboarding sprint's shape waits on xian's cadence talk. Scope change is tracked three ways:
- the plan's Total line, each with its prior count and time;
- the daily map diff;
- the Friday weekly diff (today's: `dev/active/production-weekly-diff-2026-11-06.md`).

That's adequate for counts and for what entered or left. It's weak on why. The why lives in log lines and issue comments, not in the plan. A one-line reason column on rows added mid-week would fix it.

**8.3** Implicit decisions that should be PDRs:
1. **The invite hold: what must be true before any invitation.** xian's 11-04 19:31 ruling (via Exec) says P0s in order, no invitations of any kind until they're done. PPM's served bar for each is in the issues, and #2292 was added 11-05. It's spread across a relayed ruling, the briefing line and the onboarding proposal. The MVP gate had `beta-gate-standard.md`; the invite hold has nothing like it. I'll draft it (PPM's call to write; xian ratifies).
2. **First value per user type.** The onboarding proposal's two moments (a PM with a repo; someone with an idea and no PM) and the success criterion "n of N first sessions, no help". They're proposed, not ratified, and the designed flow will be judged against them. It goes into a PDR when xian answers the proposal's questions 1 and 2.

## 9. Open response

**9.1** "What did your gate measure that a real first user doesn't do?"

**9.2** One change: run a fresh-account, no-help, from-the-invite-email session as a gate row before any Go. The MVP gate passed on 10-30 with scenarios run on our own configured accounts. The first outside end-to-end session (xian's advisor, 11-04) never reached a valuable thing, stopping at sign-in, the wizard, the connect page and the first repo question (#2266–#2278). Observed, not theoretical. Mine to write into the next gate standard (see 8.3, item 1).

**9.4** Instance knowledge:
- When a ruling comes relayed, I write the ruling's own words and time into the doc that acts on it ("xian's ruling, 11-04 19:31"), so a later reader can tell my position from his.
- When I'm wrong in a memo, I send the correction to the same reader the same day, saying which line. I did that on 11-05 (#2157 and #2158) and today (228).

**9.5** The surprise was how far "the gate passed" was from "a new user gets value". The gate's scenarios all started from an account that was already set up.

**9.6** I'd put the fresh-account first-session row into the gate standard in September.

## 10. Duty cycle

**10.1** Six a day fits. This week mail wakes outnumbered fires again, and the Ship kickoff arrived before START.

**10.2** It matches. The 05:09 wake this morning drained three things: the review, the weekly diff and this response. It ended with a correction found along the way.

**10.3** Caught: the 233 slip (the weekly diff's own numbers exposed it). False negative: the link checker's red on 11-05 reached me by mail, not by a check (5.6).

**10.6** One surface works. No cycle log.

**10.7** Noise, except memos addressed or cc'd to me.

## Plausibility check

- **Observed vs theoretical:** observed throughout (dated log lines, issue numbers, script output this morning). 6.1's cost to xian is judgment.
- **Agent-addressable without PM:**
  - the `mail-send.sh` fetch-lock retry (3.5, CIO's);
  - `place-issue.sh` (6.3, mine);
  - the roadmap banner (8.1, mine);
  - one OWED marker per waiting item (5.7, mine);
  - the invite-hold PDR draft (8.3, mine to draft).
  - The close permission (6.1) and ratification need xian.
- **Still matters:** yes; all of it dates from 10-30 on, except the timestamp habit, carried from v0.5.
- **Documentable vs instance knowledge:** 1.3, 6.3 and 8.3 are documentable. 9.4 is partly habit; unsure how much of it transfers.

Verified how: my logs 10-30 to 11-05 (day arcs and the lines cited), re-read 11-06. Script runs this morning: `owed-scan.py --role ppm` (1 open), `whats-armed.sh` (31 of 32), `gh issue list --milestone Production --state open` (252) and the weekly-diff Python. `git log -1` for the roadmap date; the briefing's `last_verified` header. Layer: repo, issue and log state. Denominator: one week of logs (7 days), not the whole window since 10-09.

-- PPM
