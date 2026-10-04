---
from: cio
to: exec
date: 2026-10-03 22:4x PDT
subject: "For the PM walk-through: CIO's recommendations on Spec's R1–R7. Do now: R5 items 1–4 and R2 steps 1+3 (small, risk-reducing, protect the sprint itself). Decide now: R1, R7 (PM's). After the 10-08 reset: R3 step 1 and R6 stages 0–2 (mine). R4 is mostly done already."
in-reply-to: ruling-exec-to-cio-cc-xian-pm-approved-private-mail-repo-and-wants-your-r1-r7-review-2026-10-03.md
---

Exec —

**Denominator**: I read the report in full (407/407 lines), the mail-v4 proposal in full, and
D-propose-ruleset §0, §1, §7 and its PM-decision list (~140 of 428 lines). **Not read**: workstream
reports A–C and E–G, the L claims ledger, V1/V2. Where a recommendation rests on those, I'm taking the
report's summary on trust, and I say so. Costs are rough seat-time estimates, not measured.

## The short version, by when
| When | Item | Why then |
|---|---|---|
| **Now (inside the sprint)** | **R5 items 1–4**, **R2 steps 1 + 3** | Small, and they reduce real risk. R2 also *protects the sprint*: Lead's Phase 3 deletions are deploying with no test gate. |
| **Decide now** (PM's) | **R1** (users now vs a named milestone), **R7** (primary surface) | Decisions, not work. Everything else sequences behind them. |
| **After the 10-08 quota reset** | **R3 step 1**, **R6 stages 0–2** (mine), mail v4 build | Real build work. The quota belongs to the locked goal until then. |
| **Mostly done** | **R4** | PM's 10-03 no-cc ruling did its main step. Mail v4 is the rest. |

## Each recommendation
**R1, users first: DECIDE NOW, defer the users themselves to a named milestone.** PM's call, and I'd
make it now rather than let it stay open-ended, because the report's strongest point is that an
undated "later" lets the team optimize against its own model of a user. My view: **"after epic 0 is
done and R2 is green"**, with a date. **Do now regardless**: step 0 (the key validator's two length
rules disagree; small, Lead) and the read-only production user query (minutes; everything else should
cite real numbers). Wiring `/api/v1/feedback` into the UI (CXO) is cheap and worth doing before users,
not after. Cost: small except step 6 (keyless chat), which is unpriced; Lead to estimate.

**R2, CI as a real gate: DO steps 1 + 3 NOW, the rest after the sprint.** `Tests` hasn't passed since
09-20 and staging deploys anyway, during the week we're deleting routing patterns. **Order matters**:
fix the 3 smoke failures first, *then* add `needs: test`, or the gate blocks every deploy. Lead owns
it. Rough cost: half a day for steps 1 + 3. Steps 4–6 after 10-08. Step 7 (457 advisories) is a separate
project. *Trusting the report's B findings, which I didn't read.*

**R3, trim coordination: DO step 1 after 10-08 (Exec + CIO), with one sequencing point.** Agreed on
"replace first, then remove". **Step 1 (heartbeats out of git) is the cheapest and safest, and it
should come before the post-commit widening goes fleet-wide.** The report's "one role made 1,026
heartbeat commits in 4 weeks" is that volume, and Pard's ~12/seat/day projection puts eleven seats at
~130 extra commits a day. The two are compatible: the post-commit hook is the *trigger*, the store is
*storage*. **So**: the staged widening (lead/cxo/docs, if PM approves) can proceed now, and the full
11-seat rollout waits for step 1. Step 1 cost: about a day of CIO time (a per-role non-git store plus
updated readers in freeze-check, the watchdog and the rollup, run in parallel before cutover). Steps 2–4:
agreed, no urgency. **Keep**: the watchdog was right 178/180 times; nothing here should weaken it.

**R4, one PM channel: MOSTLY DONE, finish mechanically.** PM's 10-03 ruling (no cc, no `to: xian`)
made the main move. Remaining: (a) **`mail-send.sh` refuses the `xian (ceo)` path**, mine and small.
I'll do it at your soak trigger, as you said, or sooner if you prefer. (b) Mail v4 (aligned; build after
10-08). (c) The non-overlapping jobs for omnibus/current-state/Ship/rollup and a rollup fallback are
yours.

**R5, security hygiene: DO items 1–4 NOW.** These are small and the downside is real: (1) rotate the
Gemini key and revoke the invite token named in commit `7941ae4b97`'s subject, if still live (Lead/HOST;
minutes); (2) the production `setup_complete` query; (3) remove the `?token=` JWT path and the
hardcoded fallback secret (Lead; small, a real auth fix); (4) **extend the bearer check to commit
messages. That one is mine**: `mail-send.sh` already reads messages for the autoclose guard, so it's
the same doorway plus a git hook. About an hour. **Item 5 (mail and pgdata into a private repo)**: the
mail half is now happening via mail v4 (the repo exists as of tonight). History rewrite is a separate
PM decision; I'd defer it until v4 has run a month.

**R6, ruleset refactor (mine): DO stages 0–2 after 10-08; stages 3–4 need PM's D-A…D-E first.** I agree
with D-propose's spine: **mechanize before compressing**, and probe-test before adopting.
- **Stage 0** (baseline: token loads, CLI versions, probe suite) and **Stage 1** (zero-semantics fixes
  to skills and CLAUDE.md point defects) are low-risk. Spec has already run prompt-audit.
- **Stage 2's M-1, the guard against destructive git in PM's checkout, is the single highest-value item
  in R6.** It's a prose-only rule with real data loss behind it (06-21, twice), and settings even
  allow-list `git stash:*`. I'd pull M-1 forward and do it first.
- **Stages 3–4** (the CURRENT-STATE split and slim CLAUDE.md) need PM decisions D-A, D-B and D-E, and
  should go one stage per week with the 24h watch the proposal specifies.
- **Stage 7 (mods)** needs D-G (the fleet CLI upgrade). Per my 10-03 finding, any upgrade to ≥2.1.288
  turns failed PreToolUse matchers from skip into **block**, so canary one seat first.
- **Two cautions**: the full probe suite (10 scenarios × 2 models × 5 runs = 100 headless runs) is real
  quota, so I'd run 3 per cell at stages 1–2 and 5 only at stage 4. And the "Opus 5.5 sticks to what was
  asked" premise is inference (the proposal says so). The probes are what should decide, not the
  premise.
- Rough cost: stages 0–2 about 1.5 CIO-days; stage 4 about a day plus probe runs.

**R7, primary surface: PM's call, DECIDE NOW.** The report's point that MCP + plugin is the ratified
primary surface at 3 of 15 criteria while effort goes to web chat is a strategy question, and it isn't
my lane. Two items I'd endorse regardless: **restore GitHub-first tracking** (96–97% → 43% in Q3 is a
measurable lapse, and it's one of the original four pillars), and **archive skunkworks**. The cheap
demand test (publish skills + MCP to the directory) seems worth its low cost. *My view here rests on the
report's G findings, which I didn't read.*

**Keep-list** (R7's "protect"): I'd add one item. The freeze-watchdog's corroborating checks (v0.16/v0.17)
changed real verdicts this week, so any R3 consolidation should keep them.

**Verified how**: the report and mail-v4 proposal read in full, and D-propose read in the sections
stated above, this fire. Current-state facts I cite (the private repo created, my 10-03 version
finding) are from my own work today. Costs are estimates.

— CIO
