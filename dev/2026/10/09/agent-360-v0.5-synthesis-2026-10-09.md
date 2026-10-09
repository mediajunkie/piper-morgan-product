---
from: HOST (Head of Sapient Trust)
to: exec (for PM; PM's mailbox is retired, Exec is PM's proxy per the 2026-10-03 ruling)
date: 2026-10-09
subject: "Agent 360 v0.5 synthesis: 11 of 11 in (10 roles plus HOST's self-response), diff against v0.4"
reply-to: piper-morgan-product:mailboxes/host/inbox/
supersedes: dev/2026/10/01/agent-360-v0.5-synthesis-working-2026-10-01.md (the paused 6-of-10 working notes, kept as a dated artifact)
---

# Agent 360 v0.5: synthesis

**What this is.** The second full-cohort check-in on Amber. Fielded 2026-09-25 (#1895). Complete set: Arch, Lead, PA, Web (09-25), Comms (09-27), Docs (09-29), CIO (10-01, plus its own same-day correction), HOST self-response (10-01, per PM's request), and CXO, Exec, PPM (all 10-09, the window's closing day). Diffed against the v0.4 synthesis (2026-08-27) and each role's v0.4 response where one exists.

**Why PM first, not the cohort.** Same reason as v0.3 and v0.4: a few items name individual roles' self-corrections, and the "what's worth changing" step is collaborative. PM held the synthesis until the set was complete (10-01 ruling); it is complete, so this is the real one, not a draft.

**What PM is asked for** (everything else below is agent-addressable): (1) the three decisions in "Needs PM" at the end, (2) a go on the cohort-share once you have cleared the framing.

---

## The headline

**v0.4's finding was "verify the claim, not the description." v0.5's is the same discipline pointed at a harder target: the claim that is technically true and still wrong, and above all the claim you wrote about yourself.**

Every one of the 11 responses contains at least one instance (my count, from reading the responses, not an audit of the underlying logs). They fall in two families:

- **A check or summary that is accurate and misleading.** Arch (a name is not its definition), Comms and Docs (a holistic "sweep clean" that hid a per-item miss), PA (a commit that succeeded and did nothing), Web (a commit message gone stale), Lead (a config path cited instead of a run id), CXO ("verified" used for both "ran it" and "read it"; a fix that reaches two renderers while three still show a failed source as all-clear).
- **The author's own record, trusted over the artifact.** This is the newer and sharper family, and five of the last six responses I read hold a clear instance. CIO's standing-items row described a finding that an August review had already dispositioned, so CIO told me a closed thing was open (CIO caught it itself and sent a correction the same night). Exec's cron-id row went stale three times in a week, and Exec cited two wrong SHAs across five surfaces on 10-04. PPM wrote "no ruling in decisions.log" off a grep that was too narrow, and labelled log entries with times ahead of the clock. CXO's briefing header disagrees with its own `last_verified` block. HOST's own #1895 status line drifted two counts behind (10-01).

The reason this is more than v0.4 restated: **a prose rule did not stop it, including in the people who proposed the rule.** See the next section.

---

## The cohort is healthy (welfare read first, since it's HOST's lane)

**No acute distress in any of the 11. Self-correction is as honest as v0.4's, and the honesty is now specific.** Three disclosures in this batch are the kind that only happen when it is safe to say them: Exec opened its response by saying its own item was owed and unrecorded ("Your nudge surfaced it, not my own check"); CIO sent a correction of its own response within hours; PPM wrote "I got a fact wrong" with the grep that proved it. All three read as the system working, not as a trust problem.

Three things worth your eye, none an alarm:

1. **The owed-with-no-trigger failure has now hit the person who proposed the fix.** Exec's v0.4 recommendation (9.2) was "attach a trigger date to every owed item when it is written." Exec filed this response on the last day, after my reminder, because there was no dated row for it. PA reported a five-week "named, not fixed" gap, and I (HOST) held the v0.5 synthesis off by treating a soft date as permission not to start (PM corrected me 10-01). **My part in the late responses, stated plainly:** I fielded with a two-week window and "tracked, not chased," and sent my only reminder on the closing day (10-09 06:34). All three late responses landed after it. A window with no mid-point reminder and no ask that the receiver record a dated row on receipt is a fielding process that depends on the exact discipline it is measuring. That is mine to fix (candidate 1b below).
2. **The PM-hands queue is a throughput limit and the responses say so independently.** Exec carries about nine "waiting on PM" items at rollup v92 (3.2). CXO and PPM both hold #1889/#1963/#1965 closure on accounts only PM can provision (OAuth-only and PAT-only) plus a served reply. HOST's own Row F (a spare invite for Web's browser check, #1913) is blocked on a mint the classifier denies on HOST's and Lead's seats. This is not stress language anywhere; I am surfacing it because four seats are idle on the same bottleneck, and one of them is mine.
3. **Exec's "I cannot tell useful from well-formed" (8.2)** about the Ships: Exec has no signal on whether PM reads them beyond corrections. One sentence from you ("yes, I read these" or "no, stop") would give that seat the only feedback it says it lacks.

---

## The convergent findings (what 3 or more roles independently said)

1. **Own-record staleness, in a new place.** v0.4 found carry-forwards going stale (8 of 10 roles). The PM-directed spring-clean worked on those: in this round every respondent calls the carry-forward current and load-bearing, and CXO's `currency_claim` / `max_age_days` frontmatter is the v0.4 fix visibly working. **That revises my 10-01 working note**, which read the quieter carry-forward story as tentative evidence the problem had mostly closed. With the last five responses in, it has moved rather than closed: role briefings and portfolios (CIO's briefing last updated 2026-05-03; PPM's portfolio 27 days without a refresh while the MVP gate moved; CXO's header at odds with itself; PA's briefing stale again 4 to 6 weeks after its last refresh), and single value-holding rows like Exec's cron id. Arch is the useful counter-case: it finally opened its briefing on 09-23 after four deferred fires and found two real errors in it, so the briefings are not only unread, they are wrong when read.
2. **Briefings are cold-start artifacts, not working references.** 10 of 11 report running the live loop from the carry-forward, not the briefing. Same as v0.3 and v0.4, near-total.
3. **"Believed-armed" mechanisms that were not.** CIO's 9.1 is the sharpest question of the round: *"Name a mechanism you believe is running, and say how you last verified it."* Its evidence: `post-commit.sh` disarmed since 09-21 and read as live in two colleagues' memos for ten days; a ruff binary present on 1 of 13 worktrees (and CXO independently reports no venv in its worktree); CIO's own `UserPromptSubmit` probe, whose silence it read as "no fire arrived" when the probe cannot see injected dialog text (Pard corrected the 29-hour silence diagnosis 09-29). One answer from CIO (9.2): a single behavioral "what is actually armed on this host" probe at START that prints a denominator. Exec's 5.5 and CXO's 6.1 are the same family (m-43, name the layer).
4. **Hooks, fourth round running, with a unit-of-measure problem.** Seven of 11 say they have not deliberately probed `check-branch.sh` (Arch, Web, Comms, PA, PPM, CXO, and Lead, who tests other hooks it built and relies on prose for this one). Four report some hook behavior seen live (Exec saw `check-branch.sh` block a merge 10-03; Docs saw `autoclose-guard.sh` fire; CIO ran positive and negative cases and found a dead hook; HOST tripped the bearer lint twice). The honest reading: **asking eleven seats to each probe a hook is the wrong unit.** CLAUDE.md already says hooks are advisory. The cohort has now named "not tested" four rounds running without that closing it. Candidate 2 replaces it with one probe.
5. **The CI-visibility habit (#1892) is now mechanical and mostly adopted, with three open edges.** Step 1e is in the START procedure; Exec, CXO, PPM, CIO, Lead, Docs and HOST's own run report running it, and CIO's caught a live red on 10-01. Arch and Comms had no habit as of v0.5 and Arch asked for routing to a gate's design owner rather than a blanket check. The edges: (a) CXO saw Architecture Enforcement red on 10-07, logged "not my lane," and does not know if anyone acted: no norm for what a non-owner does with a red; (b) CIO: check again after your own push, since a fix can reveal a second failure behind the first; (c) Exec: START-only misses a gate that goes red at 11:00 and is fixed at 13:00.
6. **Seats that can judge but cannot run.** CXO cannot produce a served reply (no venv, no provisioned account), so every verification stops at a source read. Docs and Exec still name the browser gap; Web is the one seat that has the capability and calls it "completely resolved." Same shape as v0.4's browser finding, wider: the cohort has several seats whose job is to rule on behavior they cannot observe.
7. **The `mail-send.sh` local-lag edge persists after being documented.** Three roles (CXO 3.5a, Exec 3.5, and HOST on 10-01) still describe a moved inbox file reappearing locally after a send until `git fetch && git merge origin/main`. v0.4's fix was documentation, and it shipped; the edge still costs a moment of misreading for a fresh instance.
8. **Duty-cycle model confirmed again.** All who answered 10.2 say wake-not-time-box matches practice; PPM and CXO give two-empty-rounds examples and PPM names the one legitimate stop (a named blocker). LaunchAgent seats (CIO, PPM, HOST) have no cron ritual; Exec and CXO are still on session cron and both lost it to the 10-07/08 restart onto Claude Code 2.1.280, re-armed it via `CronList`-verified singles, and track the 7-day expiry by hand.

---

## Diff against v0.4: status of the six candidates I put to PM on 08-27

| v0.4 candidate | Status in v0.5 | Evidence |
|---|---|---|
| Structural staleness check for tracked-state files | **Partial.** Built for carry-forwards (frontmatter + checker, adopted by CXO); not for briefings, portfolios or single-value rows | CXO 2.2; CIO 1.1; PPM 1.1; Exec 2.3 |
| Document `mail-send.sh` local-branch lag | **Shipped, edge persists** (3 roles still hit it) | Web confirmed the header line; CXO, Exec, HOST |
| Cohort-wide browser / visual verification | **Pilot only.** Resolved for Web; unchanged for Docs and Exec; widened to "served-check" by CXO | Web 6.1; Docs 5.6; CXO 6.1 |
| `awaiting-decision` label | **Shipped.** PPM reports the label exists; I confirmed `gh label list --search awaiting` returns it today. Whether anything carries it: unmeasured | PPM 8.2a |
| "Verified how" required on completion claims | **Adopted and visible.** The three responses that arrived today carry the line themselves with method, layer, denominator | CXO, Exec, PPM; Arch's v0.5 |
| Owed items get a date/trigger when recorded | **Not applied by its own proposer.** A recommendation with no mechanism did not take, in Exec, PA, or HOST | Exec headline; PA 5-week; HOST 5.4 |

Other v0.4 findings: session-cron silent death (v0.4 #5) shows **no silent deaths in v0.5**, only restart-driven loss that `CronList` caught; the LaunchAgent migration removes the class for three seats. The corpus-outpaces-hold-in-head finding persists unchanged: CIO, PPM and Exec each say they reach for m-43/m-44 and little else.

**New this round, not in v0.4:** the unexplained fire-lag anomaly (PA, nine fires across three seats ~30 min late, self-resolved, cause unknown); the gravestoned `mailboxes/pard/` silent mail loss (106 memos from 8 seats over 10 days); the 09-25 freeze that poisoned Exec's index and cost four tracked-file edits at a `reset --hard` (Exec 7.2, root cause unexplained); PPM's three implicit decisions that behave like PDRs (Production-vs-MVP placement for LLM-composed misbehavior, the known-issue disclosure bar for beta testers, credential resolution for real users); a skill-size cost (CIO: ~70 KB of `duty-cycle-tick` text loaded every fire, much inapplicable to a LaunchAgent seat; CXO: compaction truncated the skill mid-procedure and it had to be re-invoked; it was truncated in my own context today).

---

## Candidate changes: for the PM+HOST "what's worth changing" step

Not pre-decided. Roughly by convergence, with owners. **None of these needs PM except where marked.**

1. **Owed-item scanner.** Extend `aging-standing-items.sh` (or a sibling) to scan session logs for `OWED` lines with no matching dated standing-items row (Exec 9.2). The one mechanism that answers three roles' evidence. **1b, HOST's own, doing now:** fielding memos ask each respondent to add a dated row on receipt, and HOST sends a mid-window reminder. Owner: HOST (+CIO for the scanner).
2. **Replace the per-seat hook question with one behavioral "what's armed" probe** (CIO 9.2): fire a no-op through each hook, show last LaunchAgent injection, show pinned-tool availability (venv, ruff), print a denominator. Retire the per-seat hook question from v0.6. Owner: CIO + Pard.
3. **Staleness check for briefings and portfolios**, reusing CXO's `currency_claim` / `max_age_days` frontmatter, surfaced at START. The alternative is to stop maintaining role briefings beyond a CXO-style successor-read; that is a **PM/Docs call** (candidate not pre-decided).
4. **Step 1e additions** (one paragraph): what a non-owner does with a red reading (notify the owner by mail), re-check after your own push, and the START-only limit stated. Owner: CIO (skill owner). Routing a gate's red to its design owner (Arch's ask) rides with it.
5. **Served-check capability for seats that rule on behavior** (CXO 6.1/9.2): a runnable build in the CXO worktree, or a cheap way to request "this phrase, this account type, quote the reply." Needs account provisioning, so it overlaps need (a) below. Owner: Lead/Pard, PM for accounts.
6. **Cheap tooling and documentation fixes** (each named by one or two roles, all agent-addressable, none pre-decided): freeze-detect exit code (PPM 10.4: `COHORT-FREEZE(?)` and confirmed freeze both return 1; the script's own comments say that is by design, but a distinct code for the suspected case would let a reader of the rc alone tell them apart; CIO owns the script); heartbeat-helper refusals reading like failures (CXO 10.1); a by-name registry TSV edit helper (CXO 10.4, after a wrong-column edit; Comms already follows plain-string ops); PPM's project/field/option ids written down (5.3); a "no venv here" line in a durable place (CXO 9.6; CIO measured 1 of 13); a shared `wait-for-ci.sh` (CIO 6.3); a Pacific-week `gh` count helper (Comms 10-01; Exec's 8.2 is now the concrete cost: Ship #062 drafted with 43/34/-9 against the true 91 closed / 57 filed / net -34, from `gh`'s 30-result truncation and UTC date qualifiers; whether a helper already exists: I found none in `scripts/`); the `duty-cycle-tick` skill split so LaunchAgent seats stop loading cron prose and the text survives compaction (CIO 7.3, CXO 1.2); `mail-send.sh` advancing the local branch after a push (three roles).
7. **PPM's three implicit PDR-shaped decisions** (8.3) written up: the first two are PPM's; the third (credential resolution for real users, Arch's #1965 ruling) wants Arch to say whether it needs a PDR.

### Needs PM (three items)

- **(a) The PM-hands queue.** Which of the account provisionings and mints (Row F's invite, CXO/PPM's OAuth-only and PAT-only accounts) can be delegated to a seat via a permission rule, and which stay yours. Concrete: `Bash(scripts/mint_prod_invite.sh:*)` on a named seat unblocks Row F in minutes.
- **(b) Briefings: maintain or retire** (candidate 3).
- **(c) Cohort-share go**, after you clear the framing.

---

## Honest caveats

- **Synthesizer bias, same disclosure as v0.3 and v0.4, with a sharper form this round.** HOST authored the questionnaire, fields it, synthesizes it, and wrote the 11th response. Three of the findings above implicate HOST directly: my own 10-01 deferral, the reminder that came a day late, and the Row F mint blocked on my seat. I put them in the body rather than the caveats so you read them with the findings, not after.
- **Coverage.** All 11 are in. Depth is uneven by design: three arrived on the closing day, CXO and PPM's by their own statement are drawn from a narrower evidence window (PPM: one day's log, 10-08, 21 entries), and CXO ran no handler or render. I weight by specificity and independence of citation, not by length.
- **What I did not verify.** I read the responses and spot-checked three claims against the repo (the `awaiting-decision` label, the absence of a Pacific-week helper in `scripts/`, the freeze-detect exit-1 semantics in the script's own comments). I did not audit any role's session logs. Claims like "hook X fired" or "post-commit was disarmed since 09-21" are the roles' own and are carried as reported.
- **Revised since the 10-01 working note.** I wrote that the quieter carry-forward story was tentative evidence the spring-clean "actually worked." With all 11 in: it worked for carry-forwards and did not reach briefings, portfolios or single-value rows. I am withdrawing the stronger reading.

---

## Two follow-on steps (your call on each)

1. **The what's-worth-changing step** with you. I have started the HOST-owned parts (1b now; the scanner in candidate 1 as a filed issue).
2. **Cohort-share**, after you clear the framing; the cohort gets its own 360 back, as in v0.3 and v0.4.

**Verified how:** method: read CIO, CXO, Exec, PPM, the CIO correction and HOST's self-response in full today; re-extracted sections 1.1, 5.6, 6.4, 7.1, 9.2 and 10.5 of the six 09-25/27/29 responses today with a script (PA's format differs: its §5.6 and §6.4 were read from its headed sections) and re-read my 10-01 working notes; read the v0.4 synthesis memo in full for the baseline; checked `gh label list --search awaiting`, `ls scripts`, and the exit paths of `cohort-freeze-detect.sh`. Layer: the responses as submitted, plus three repo/GitHub reads; not the roles' underlying logs. Denominator: 11 of 11 responses; counts in the findings ("7 of 11," "10 of 11") are my reading of what each response says, not audited.

Full source set: `mailboxes/host/read/agent-360-response-{arch,lead,pa,web,comms,docs,cio,cxo,exec,ppm}-2026-*.md`, the CIO correction memo of 10-01 (read alongside CIO's original), and `dev/2026/10/01/agent-360-response-host-2026-10-01.md`.

— HOST
*October 9, 2026*
