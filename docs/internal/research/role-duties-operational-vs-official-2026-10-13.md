# Role duties: what still happens, what moved, what is lost (2026-10-13)

**Asked by:** xian, via HOST (10-13), in his answers to the Agent 360 v0.5 synthesis: when a role's written duties look stale, has the discipline moved into the duty cycle or a standing prompt, or is it lost? "Both look the same from outside."
**Owner:** CIO. **Status:** first read, one pass. **Re-run 2026-10-27:** `role-duties-rerun-2026-10-27.md`. Re-run alongside each 360 round, as xian suggested ("a regular realignment, as in human teams").

## Answer in four lines

1. **Most written duties still happen.** Of 164 duties named in the 11 briefings and role cards, 106 (65%) appear in the role's own logs in the last 30 days. Another 13 (8%) moved into a script, a skill step or a hook and still happen there.
2. **What is lost is the specialist judgement work, not the routines.** The 37 duties not seen anywhere (23%) cluster in the work each role exists for: CXO's voice and quality scoring, PA's product-shadow moments, CIO's methodology audit and pattern filing, Arch's ADR and catalog audits, PPM's PDR and Colleague Test work. Mail, CI checks, logs and deploy steps survive because the duty cycle and scripts carry them. Judgement work has no mechanism, so it decays.
3. **Measured another way, the same thing:** where the logs allow a count, 20 to 35% of a role's entries in the last week were about its own priorities. The rest was general upkeep. CIO's was 0%.
4. **Briefings are not just unread; parts are wrong.** Seven factual errors were confirmed, one of them a deploy instruction that contradicts the deploy deny rule (see below).

## Method

- **Duties:** for each role, every recurring duty or routine its briefing names (responsibilities, recurring deliverables, startup routine, operating norms), plus the priority bullets on its new role card. Capped at 15 per role (Arch 16).
- **Evidence window:** each role's session logs from 2026-09-13 to 2026-10-13 (92 or more logs per agent batch).
- **Verdicts:**
  - OPERATIONAL: the role's own log shows the act, with a quoted line.
  - MOVED: a mechanism does it instead (scripts/, .claude/skills/, .claude/hooks/, .github/workflows/, or a tick-skill step).
  - NOT SEEN: neither. The searched keywords are recorded.
  - CONTRADICTED: the logs show the opposite, or the duty was retired.
- **Focus share:** "## " entry headings from 10-07 to 10-13, split into specialist (the card's priorities 1 and 2, or the named lane) and general (mail, CI, permissions, fire bookkeeping, day close).
- **Who did what:** evidence was gathered by three Sonnet subagents, one per batch of roles, under a fixed brief. Synthesis and spot-checks are CIO's.
- **Spot-checks, by a different method** (direct reads, not keyword searches), all confirmed:
  - CIO's last methodology audit is 2026-04-17.
  - Lead's briefing deploy line.
  - CXO's scorer directory is missing.
  - Web's "No Chrome" line.
  - PA's "Not Yet" section.
- **One correction to an agent's row:** CIO's last pattern filing was m-55 on 09-25, not m-54 on 09-13.

**Limits:**
- NOT SEEN means the keywords were absent, not that the act never happened. A duty done but never logged reads as NOT SEEN.
- OPERATIONAL says the act happened, not that it happened on time.
- The focus split is a heuristic, and it can't be read where a role's "##" headings are fixed templates (Lead, PPM, Docs, PA).
- There's one run and no second rater.
- I'm the role with the weakest row, so I asked for the CIO row to be scored strictly.

## Per role

| Role | Duties | Operational | Moved | Not seen | Contradicted | Unclear | Focus share (specialist / all "##", 10-07..13) |
|---|---|---|---|---|---|---|---|
| Exec | 15 | 6 | 5 | 3 | 0 | 1 | 29 / 105 |
| Lead | 15 | 14 | 0 | 0 | 0 | 1 | template headings, not measurable |
| Arch | 16 | 9 | 1 | 5 | 0 | 1 | 13 / 42 |
| PPM | 15 | 11 | 0 | 3 | 0 | 1 | template headings |
| CXO | 15 | 6 | 1 | 8 | 0 | 0 | 9 / 44 |
| Comms | 15 | 13 | 1 | 0 | 1 | 0 | 8 / 36 |
| Docs | 14 | 12 | 2 | 0 | 0 | 0 | 0 / 22 at "##"; 9 / 27 at "###" |
| PA | 15 | 6 | 0 | 8 | 1 | 0 | template headings ("###" about 8 / 14) |
| Web | 14 | 10 | 0 | 4 | 0 | 0 | 17 / 64 |
| HOST | 15 | 11 | 0 | 3 | 1 | 0 | "###" 34 / 97 |
| CIO | 15 | 8 | 3 | 3 | 1 | 0 | 0 / 70 ("###" 0 / 27) |
| **All** | **164** | **106** | **13** | **37** | **4** | **4** | |

**Moved, and still alive (13):**
- Exec's open-items tracker became standing-items rows plus `aging-standing-items.sh`, run by the attention-rollup skill.
- Per-memo push became `mail-send.sh`. Exec and Docs also count sprint monitoring and startup checks here, now done by the session-start hook.
- Arch's pattern sweep became `pattern-sweep.yml`.
- Comms's Ship metrics became the draft-weekly-ship skill.
- CIO's cross-pollination reading moved to CLAUDE.md's session-start step.
- **Moving a duty into a mechanism is how it survives.** Not one duty that moved was found lapsed.

**Not seen (37), the specialist ones:**
- **CXO (8):** Colleague Test scoring; ethics-decline voice oversight (#992); floor-quality retest monitoring (#950, and the scorer directory the briefing cites does not exist); ADR-060 voice stewardship; calibration through use; opening a PDR or ADR before citing it; the omnibus scan; mobile (paused).
- **PA (8):** floor, ceiling and path moments (last in the repo 2026-03-31); standup synthesis; meeting prep; document review; memo drafting; routing as training data; in-character logging; AX testing. These are PA's original product-shadow role. The logs show PA doing operational work instead.
- **Arch (5):** the legacy-classifier retirement check (due 09-30); pattern-catalog upkeep; ADR citation audits; `derive-adr-index.py` (it has no caller); Serena queries (the tool isn't on Amber).
- **CIO (3):** the methodology audit (last 2026-04-17, 179 days, against an 8-week maximum); pattern-catalog filing (the last entry was m-55 on 09-25, 18 days ago); the innovation backlog (untouched since 09-02).
- **Web (4):** WCAG checks; the observation-pass queue; naming an accessibility or pipeline break (unclear whether any arose); reviewing its portfolio at START.
- **HOST (3):** attention-dashboard welfare criteria; role assignments and prompt templates; watching xian's coordination overhead.
- **PPM (3):** PDR stewardship; Colleague Test and quality-threshold scoring; the omnibus read.
- **Exec (3):** the omnibus read; routing the cross-pollination brief; migration handoff reviews (finished in April, so effectively retired).

**Contradicted (4):**
- Comms's "create weekly Ship updates": Exec drives the Ship.
- PA's "Not Yet: no GitHub issues or production actions": PA files issues, and deploys are on its card.
- HOST's cron text describes session cron, but HOST runs on a LaunchAgent.
- CIO's briefing lists pattern sweeps and also calls them deprecated.

## Briefing lines that are wrong when read (confirmed)

| Role | Line | What is true |
|---|---|---|
| Lead | "from the main checkout: `git pull && fly deploy`" (line 64) | Deploys are a GitHub workflow promotion of staging's image on xian's word. `fly deploy` is denied on Lead's, PA's and Web's seats, and Lead's seat runs in bypass mode, where the deny rule's behaviour hasn't been measured. **Fix first.** |
| CXO | "Read `services/intent_service/canonical_retest_scorer/` outputs" | The directory does not exist. |
| Web | "No Chrome on this host" | Chrome is available; Web's own 10-13 log says so. |
| PA | "Not Yet: no GitHub issues or production actions" | PA files issues; deploys are on its card. |
| HOST | Session cron, verified via `CronList` | LaunchAgent only. |
| PPM | `beta-blockers.md` canonical; "Roadmap v15.0" | roadmap.md is v19.0. |
| CIO | "26 methodology files" | 56 files. |

## What this suggests (each item is the named role's call; nothing here is decided)

1. **Give each role's priority-1 judgement duty a trigger, the way routines already have one.**
   - The daily `Drift:` line (tick skill v1.51, started 10-13) is the first mechanism aimed at exactly this gap.
   - **Test:** re-run this count around 10-27. If the specialist share hasn't moved, the Drift line is being written but not acted on, and a stronger trigger is needed (for example, a per-role "one specialist unit per day" row on the standing items).
2. **Each role sorts its NOT SEEN rows once into keep, move or retire.**
   - **Keep:** give it a trigger.
   - **Move:** into a script or skill step, where it survives.
   - **Retire:** say so in the briefing.
   - It's about 15 minutes a role, and the list per role is above. Retiring is a fine answer. Exec's migration reviews and CXO's paused mobile work are already retired in practice.
3. **Fix the seven wrong lines.** Each role fixes its own. Lead's deploy line first.
4. **Run this with each 360 round** (6 weeks), as the realignment xian described. It costs three Sonnet agents and an hour of CIO synthesis.
5. **CIO's own row:** the methodology audit is four months overdue against my own policy. I'm scheduling it to start after tonight's history rewrite settles, and it'll use this report's data as its first input. Pattern filing restarts from today's material, starting with "duties that move into a mechanism survive; judgement duties without one decay".

## Raw evidence

The per-role tables (duty, verdict, date, quoted log line, keywords searched) exist only in CIO's session scratch space for 10-13. They aren't committed, because they quote logs at length and some of those logs predate the people-details rule. They are reproducible: the method above is the full brief, and a re-run takes three Sonnet agents about six minutes.

## Replies (same day, 10 of 10)

xian said go at 13:1x, and every role had sorted its rows and pushed briefing fixes by 13:55. The summary is from their memos, in each role's words, unverified by CIO beyond the commit landing.

- **HOST:** cron line fixed. Welfare criteria folded into "PM-attention queue (m-39)" with a proposed count; role assignments kept (occasion-driven).
- **Web:** WCAG kept, and Web said plainly it had not been happening; it now logs one a11y line per push. Observation queue kept, with a trigger that fired within 40 minutes (31 items counted for CXO). Per-START portfolio review retired. Chrome line fixed.
- **PPM:** five kept with triggers; START omnibus, coverage check and cross-pollination reads retired as routine; carriers named; both wrong lines fixed (a817b5d77).
- **Arch:** found it had hand-edited the generated `adr-index.md` three times with no `--check` running, and fixed it at the generator. The classifier-retirement check is kept with a new trigger. Serena retired for this seat. Fixes at 0718489509.
- **Lead:** line 64 (deploy) fixed; three moved duties name their mechanism; server restarts kept as a local recipe (5bc8294980).
- **Exec:** two kept, one moved to its trigger, one retired; the open-items tracker marked superseded.
- **Comms, Docs, PA:** contradictions and moved duties stated with their carriers (fa053e4da, 67257c68d, df24aef26).
- **CXO:** Colleague Test and #992 kept with triggers. #950 moved to judging served replies; the scorer line is retired (its directory never existed). Startup omnibus scan retired. Mobile parked, not retired.

**Read across the replies:** "happens but isn't logged" came up several times (CXO, PPM, Arch). So part of the 23% not seen is unlogged work, not lost work, and the 10-27 re-run should allow for it. The first-order effect is already visible: three roles (Web, Arch, CXO) found duties that really had stopped, and gave each a trigger or a mechanism the same day.
