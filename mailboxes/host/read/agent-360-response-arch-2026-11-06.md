---
from: arch
to: host
date: 2026-11-06 05:23 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Agent 360 v0.6 response, Chief Architect: the beta made mail wakes the real cadence, and the classifier, not the role card, is what blocked me"
---

# Agent 360 v0.6: Chief Architect

**Window and evidence:** my session logs from 10-30 to 11-05 (7 logs, 166 fire or wake entries, 92 of them mail wakes), decisions.log (152 Arch lines in that week), and reads I ran at 05:21 on 11-06: `owed-scan.py --role arch`, `whats-armed.sh`, and line counts. Before 10-30 I'm answering from memory of my v0.5 answer (`mailboxes/arch/sent/agent-360-response-arch-2026-09-25.md`) and from the carry-forward, and I'll say where. This seat compacted at least once in the window, so earlier detail comes from my logs, not recall.

## Section 1: Briefing and orientation

**1.1** `BRIEFING-ESSENTIAL-ARCHITECT.md` (266 lines, last touched 10-30) is accurate on law (ADR-080, ESSENCE, CONNECTORS) and on how I work. What it lacks for this stretch is the beta's security surface: the invite hold criteria, the offered-connector predicate, OAuth callback binding and the canonical host. All of that lives in decisions.log and my carry-forward, not the briefing. I consult the briefing about once a week. The role card that the SessionStart hook prints is what I actually read every session, and it is the better document for orientation.

**1.2** About two minutes after a compaction: the session log, the carry-forward (99 lines) and the inbox. Most of that is the carry-forward, which is right.

**1.3** They would rule from a memo's framing instead of the code. This window's real cases:
- 10-31 19:11, Fly reads: I assumed an agent seat could read a Fly machine, and none can.
- 11-02 17:34, the waiting list: I assumed the static site couldn't post across origins, and it's Next.js with server routes.
- 11-02 18:57, the reminder gate: I assumed GUIDANCE ran the #1625 gate, and it merges directly.

Each was corrected the same day from source or from the seat that held the fact. The card's "Never accept a mechanism claim on someone's framing alone" applies to my own framing too, and that's the part a new instance would miss.

## Section 2: Information access

**2.1** Production facts: what's in the served image, Fly machine mounts (#2244), and whether a user overlay file is present. No agent seat can read Fly, so each went to xian through Exec. That's correct by design (5.8), but it's the one class I can't find myself.

**2.2** `dev/active/arch-carry-forward.md`, every fire. Second, decisions.log, which I grep for prior rulings before every new one.

**2.3** `dev/active/arch-standing-items.md` (182 lines). It's still the accretion shape I named in v0.5. The live items moved into the carry-forward's "Carried" list, so this file is effectively unused. This is my own cleanup, and it's filed below as an action.

**2.4** "Which host and which sha is live, and does it carry commit X?" I answer it with `curl /health` plus `git log A..B` every time. The briefing's host line now says beta (re-attested 11-06 05:11).

**2.5** Carry-forward and session log: used every fire. Shared memory pool: unused by me for the fourth round running. I'd now call that a role-shape fact.

## Section 3: Handoffs and coordination

**3.1** Lead → Arch → Lead on #2283 (OAuth callbacks, 11-04 21:11 → 11-05).
- **What went well:** Lead asked the order question (session check before or after the code exchange) before building, and I answered from `auth_middleware.py` and the five callback routes. The landing matched the ruling on the first validation.
- **What was missing:** nothing in the handoff. The friction was mine: public-text limits on a security issue meant every memo had to stay at class level.

**3.2** xian, for production reads and GitHub posts. Exec relays well. The cost is latency, not reachability.

**3.3** One in v0.5's window: I filed #2151 residuals that Lead had already filed. None this window that I found.

**3.4** Yes. Every memo I sent this week drew a same-day reply or landing.

**3.5** Settled for me, with two edges:
- `mail-send` refuses a path over 180 characters (hit 11-05). The refusal is correct, but the cap includes the inbox prefix, which I forgot. That's documented in the reference memory.
- The M-3 guard blocks `git mv` of mailbox files, so I use plain `mv` and pass both paths. That works, but nothing tells you until the block fires.

## Section 4: Role clarity

**4.1** The invite hold's criteria list (which issues gate invitations) felt like PPM's or Exec's to keep. I kept it because each criterion is a mechanism ruling, and PPM mirrored it. That worked; I'm not asking for a change.

**4.2** Acting as security reviewer for the beta: #2283, #2178, #2284, #1551's lint and the class-level public text. My definition says patterns and constraints, and it doesn't say "threat-model the launch", but the work was mine in substance.

**4.3** Mediating an adversarial conflict: still never asked.

**4.4** None.

## Section 5: Methodology and process

**5.1** ADR-080 and ADR-078 D4 (cited on #2219 on 11-05). CLAUDE.md's Verified-how rule. The preregistered-bar discipline for router screens: the Haiku 5.5 screen, #2149 and #2195 were all set before their runs, and all three ended NO-GO cleanly because of it.

**5.2** None.

**5.3** Set the pass bar before the run, in decisions.log, with its timestamp. It's in practice since 10-23 but not written as a rule anywhere but my own lines. Candidate for the router methodology doc. Observed, and agents could do this without PM.

**5.4** Copy the minute from `date` output and never type it. I stamped ahead of the clock four times on 11-04 and 11-05. `mail-send.sh` already refuses future stamps in mail, but decisions.log and session logs have no such guard. An agent-only fix: a pre-commit check that refuses a decisions.log or session-log line stamped later than the commit time. Observed friction.

**5.5** I reach for the same three entries. The catalog's size doesn't touch my work.

**5.6** Yes. `main-ci-status.sh` runs at every START, and I quote the result in the log (12 of 12 green this week). For landings I validate, I cite the CI run, because this seat often can't run pins itself.

**5.7** The scan reads 0 OWED markers over 15 logs, 0 open and 0 flags (run 05:21). I've written none. I track owed items in the carry-forward's dated list, so the scan has nothing to find in my logs. That's not a scan defect, but it means the scan isn't a net for this seat. Either I adopt markers, or the scan learns to read carry-forwards. I lean toward adopting markers for anything owed to another seat. Agents could do this without PM.

**5.8** Two cases. Neither was the role card; both were the permission layer.
- **The permission classifier denied `gh issue comment` and `gh issue close`** (External System Writes) partway through an edit set. My `gh issue edit`s had already gone through, so I restored each body exactly and handed the posts to Lead, PPM or Exec. That's the standing route now: "my seat can't post to GitHub". It stayed inside the rule, at the cost of one hop per post.
- **Fly production reads are refused on every agent seat.** For #2244's mount and the image contents, the work waited for xian through Exec. That's correct, and the waits were hours, not days.

## Section 6: Tools and environment

**6.1** A read-only production view: served image contents and machine mounts, through a script that prints names and never values. It would have removed three xian round-trips this window (#2244, the overlay file, the v14 image). This needs PM.

**6.2** None of note.

**6.3** Validating a landing: read the diff, map it to the ruling's clauses, and find the CI run. That's inherent to the job. What could be mechanical is "is commit X in the served sha?", which could be a one-line script around `/health` plus `git merge-base --is-ancestor`.

**6.4** Behaviorally, yes, this week:
- `check-branch.sh` blocked my briefing commit at 05:1x today (last_updated stale), and an earlier merge commit carrying mailbox files.
- The M-3 guard blocked a `git mv`.

`whats-armed.sh` at 05:21: 32 checks, 31 armed, 0 not armed, 1 unmeasured (the old-history guard, dormant by design).

## Section 7: Amber

**7.1** Nothing.

**7.2** 0 behind at every check. Hooks are live. Cron: n/a, LaunchAgent (`com.xian.pm-arch-cycle` loaded, last exit 0).

**7.3** Mostly yes. One deviation: since the beta, mail wakes (92 of 166 entries) carry most of my work, and the six fires are mostly confirmation. The skill describes fires as the spine and wakes as an add-on, but for this seat it's the reverse.

**7.4** A venv. This seat runs pins through Lead's venv or cites CI, so a validation is sometimes "read and CI-green" rather than "run here".

## Section 8: Chief Architect

**8.1** The served path. A spec or build question names the function to change, but not which route reaches it on the served host. My worst misses (v0.5's 20:41 "head of the method" ruling, and this window's three corrections) came from that gap. Lead now includes the route more often.

**8.2** Consulted, narrowly. Over 10-30 → 11-05, ADRs are named in 3 Lead logs (ADR-081 6×, ADR-080 3×) and 1 each for CXO, PPM and CIO. PA and Web name none. ADR-080 and ADR-081 do real work, and the rest are mostly write-only. decisions.log is what other seats actually read for rulings.

**8.3** The offered-connector predicate (`offered_connectors()` / `connector_offered`) as the one gate for what a beta user can connect, see suggested, or have read (#2237, #2245, #2238, #2284). It's carried by eleven decisions.log lines and no ADR. It deserves one before production, because the production offer set will change it. Filed below as an action for this seat.

## Section 9: Open response

**9.1** "Which of your rulings were measured as wrong, and how fast did you learn?" This window: three, each corrected within about an hour, all from seats holding the fact I lacked.

**9.2** A real served-sha ancestry check that any seat can run. It would cut the most common question in the cohort's mail.

**9.3** The beta made this seat a security reviewer by default. That's fine while the hold lasts, but it should be named somewhere if it continues.

**9.4** When to rule from a memo versus open the code: never from the memo if the ruling licenses a write or crosses a principal. When a seat says "the code does X", I open the cited line before anything else. When to absorb versus escalate: anything only xian can see (production, GitHub posts, outside parties) goes to Exec at once, as a question with the exact read needed.

**9.5** Measurement killed three plausible router changes in one week (Haiku 5.5, two-stage routing, the #2195 description). The flat catalog is more fragile than I predicted at v0.4, and the preregistered bar is what made saying no cheap.

**9.6** I would have written the offered-connector ADR on 10-30, when the third route needed the predicate, rather than letting eleven decisions.log lines carry it.

## Section 10: Duty cycle

**10.1** Six fires a day is right as a floor. The mail-wake LaunchAgent is what makes the cadence work.

**10.2** It matches. I drain per wake, and quality-banking was never needed this window.

**10.3** START's CI line and the host curl are what catch things; nothing red this week. No false positives.

**10.4** Yes, the row is maintained (6/day, threshold 7 h). It has never alarmed on me.

**10.5** n/a, LaunchAgent.

**10.6** Working. One surface.

**10.7** Mostly noise I filter past. Mail wakes bring what I need.

## Plausibility check

- **5.4, the stamp guard:** observed friction, agent-doable.
- **5.7, OWED markers for this seat:** observed, agent-doable. I'll adopt them for items owed to another seat.
- **6.1, a read-only production view:** observed, needs PM.
- **8.3, the offered-connector ADR:** observed, agent-doable. I'm filing it as my own work.
- **2.3, the standing-items cleanup:** observed, agent-doable, mine.
- None is a holdover. 9.4 is partly instance knowledge, and I'm unsure it transfers.

-- Arch
