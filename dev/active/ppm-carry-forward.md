# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-08-06 Fire 2 (~10:30 PT) — after correcting a two-orders-of-magnitude
error I had told PM I'd verified independently
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Environment note — CURRENT as of 2026-07-30

**This role is on Amber, Model A**: `~/Development/piper-morgan-worktrees/ppm`, branch
`claude/ppm-cycle`, 0 behind `origin/main`. **Cron is ARMED and firing.**

*(Superseded: the prior note here described a 7/28 session running from the old pre-Amber worktree
`pensive-kepler-02a0f6`. That was accurate then and is not now. Rewritten rather than left to be
inherited — this file has already caused one four-session error by being read as current state.)*

**PPM went dark twice** (7/20-25, 7/27-28) and was resumed by PM both times; a third interruption
(overload error, 7/29-30) was also PM-resumed. In all three the carry-forward + mail were the only
continuity — never a clean STOP. **The environment question the 7/28 session raised is now answered
by fact rather than by ruling: PPM runs on Amber.**

## ⚠️ SPRINT STRUCTURE — READ BEFORE ANY MILESTONE/SPRINT REASONING

**M4 and M5 DO NOT EXIST as sprints.** They were **swept 2026-07-04/05 — PPM's own work** — along
with M3-Quality/M3-Health/M3-Security/RECONNECT. Contents went either into the **Beta Blockers**
sprint or to the **Production** milestone.

- **Beta Blockers = the final pre-beta sprint.** The **MVP milestone IS the beta gate**: beta ships
  when every issue on `docs/internal/planning/beta-blockers.md` closes — not on a date.
- **Disposition rule**: anything in MVP that didn't meet the hard-gate bar → **Production**, to be
  addressed *during* beta. So **an issue sitting in Production is the rule working, not a defect.**

✅ **BOTH DOCS ARE NOW FIXED — verified 2026-08-06, and this line used to say they weren't.**
- `sprint-board-structure.md:77` carries a SUPERSEDED banner; `:88`/`:91` mark M4 triage-closed and M5 swept.
- `roadmap.md:68` annotates differentiator #4 with the sweep + #1174's move to Production.

⚠️ **Note what just happened, because it is the whole lesson in one line.** This warning existed
*because* those two docs burned me — and it outlived them. **I re-read my own warning today and had
to go check whether it was still true.** A warning about staleness is not exempt from staleness;
it is *more* exposed, because it gets written at peak conviction and reread as settled fact.
**Owed and still open**: the remaining `(M4 …)`/`(M5 …)` refs elsewhere, as a class.

✅ **The accurate source is `docs/internal/planning/beta-blockers.md`** (see its lines 12 + 20).

**Cost of not knowing this (2026-07-30)**: I reasoned from the two stale docs and produced three
successive wrong readings of one roadmap line, then recommended moving **#1174 into M4** — a
dissolved sprint. PM caught it. **I had run the sweep myself and it was in no artifact I carried.**
Repointing the stale `(M4 …)`/`(M5 …)` references is owed work — do it as a class, not line-by-line.

## ⚠️ HEARTBEAT — WAKE EMISSION, EVERY FIRE, AT THE START (adopted 2026-08-05)

**Run `scripts/duty-cycle-heartbeat.sh ppm <FIRE> ` at the START of every fire, before any commit.**
NOT as Step 5b at the end. **On 2026-08-05 I skipped Step 5b entirely on a busy fire** — nine other
roles emitted, ppm didn't — and PA's pre-registered falsifier fired on my seat as a result.
**Step 5b sits where a fire that found real work drops procedure**, which is exactly when the
liveness claim is most often made and least examined.

⚠️ **Do NOT repeat my claim that "~30 fires produced zero heartbeats" as evidence about the
mechanism.** On fires where I ran it, `--if-quiet` suppressed as documented; on at least one I never
ran it. Those two populations are not separable retroactively. **The clean claim is narrow.**

## ⚠️ BRANCH ≠ DEPLOYED ARTIFACT — and "I verified it independently" needs a DIFFERENT METHOD

**2026-08-06, my error, caught by Lead and PA and not by me.** I sent PM an URGENT saying
*"commits on main not in production → **2,282**"* and wrote *"verified the deployment claim
independently before building on it."*

**`origin/production` is the production BRANCH; the deployed ARTIFACT is a Fly release.** Branch
staleness is benign-by-mode; the 2,282 delta is overwhelmingly mailbox/log/doc traffic from ten
agents. **Measured against the artifact (Fly v29, 2026-08-02, `main@b619794af`): 984 commits total,
of which 15 touch `services/` or `web/`.** ~15 product commits, ~4 days. **Two orders of magnitude.**

**⭐ The transferable part is the verification, not the number.** I ran the SAME comparison PA ran,
so **agreement was guaranteed and my check could not have caught the error.** A second measurement
that shares the first's method is **not** independent verification — it is replication wearing the
word "independent." *This is the class I wrote up on 07-26 and then committed eleven days later.*

**And it skewed a decision I put to PM**: I framed "deploy main before beta" as high-risk *because*
2,282. ~15 product commits over four days is an **ordinary release**. **A wrong magnitude doesn't
just misinform — it can invert which option looks safe.**

**Rule earned**: before writing "verified independently," name **what would have made my check come
out differently from theirs.** If the answer is "nothing," it's a repeat, and say *that* instead.

## 🔴 CURRENT — beta target **Sunday 2026-08-09** (was "Sat 08-08" here; wrong on BOTH counts)

**PM 08-06, via Comms**: *"August 8th was actually just a misremembering… I really meant August
9th."* Also: the target is *"somewhat arbitrary,"* PM named **their own availability** (not team
pace) as the recent constraint, and asked for **no artificial panic**. ⚠️ **Not a loosening of the
bar** — a soft date is *more* reason not to ship unverified, since the reason to hurry shrank.
✅ **MVP milestone due date now reads 2026-08-09** — the field I flagged twice. Resolved; dropped.

**#1386 criterion 5 is OPEN and CHECKABLE (not blocked).** Arch verified in production:
`slack_inbound_enabled` → **0 occurrences**, all three #1484 commits non-ancestors, **leak path
fully present** — so #1484's gate is genuinely absent from the deployed artifact. **But** the leak
requires a `slack_bot` token **a tester cannot mint**, so the criterion is checkable this morning.
**My criterion-2 signature stands** — it was measured against `main`; the layer question was right.

**1. Radar/Surface-1 is SETTLED — do not re-derive it.** Radar's rendering is **Surface 1** (history
sidebar, #1236). PDR-005 specifies a **cross-client variant** of it at `:122`, `:245`, `:288`, `:328`;
**PDR-005:135 + roadmap.md:127 both mark it "unblocked NOW", ~4-6 days.** ⚠️ Caveat that stays:
PDR-005:84 puts **Surfaces 1/3 on "weaker forms"** of the criteria (2/4/6/7 meet them clearly) — so
Surface 1 is 1.0-required **on weaker grounds**. Scheduled, not unassailable.
⛔ **My earlier answers "the web page goes" and "undecided" are both WRONG.** Superseded.

**2. Awaiting PM — unchanged for days**: six filings with **no milestone** (#1462 · #1476 · #1477 ·
#1482 · #1483 · #1485) · the **six Jake items** (PM answered 1, 2→"(b)", 5; needs plain English on 3
and 6 — 3 sent, 6 is PA's) · **canonical criterion text** · **#1481 scope confirm** · **MVP milestone
still 2026-08-01**.

**3. Watch, don't drive**: #1484 (gate + CXO client branch, one commit) · the funnel query (Lead) ·
#1468 judge calibration · PA's annotation spec (unblocked; `headersHelper` is condition 1's carrier).

⚠️ **Standing instruction from PM, keep applying it**: *"I do not want to approve something I will
later regret because I felt rushed by a made-up deadline. I am a Time Lord after all."* **No
manufactured urgency in anything sent to him.**

⚠️ **My own lesson from 08-05, worth not repeating**: I gave PM three successive answers to one
question and only the third was right. **What fixed it was CXO finding a FACT neither of us had (the
surface number), not better reasoning over the same material.** On a question about something PM has
defended repeatedly — **find the number before answering at all**, and **check whether a peer has
already answered before sending.**

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Ship #053** | ✅ Sent 2026-07-28 (window Jul 17-23), on time despite same-day kickoff | None |
| **Jul 19 log** | ✅ Retroactively closed 2026-07-28 (had no DAY-CLOSED marker, flagged by Exec's kickoff) | None |
| **#1386 gate run** | 🔴 **WINDOW LOCKED FRI 07-31** — Lead drives from ~06:17; CXO + PPM verify + sign off **on the issue** by noon. Closes criterion 2 + Scenario-B only, NOT the gate | See the FIRST THING FRIDAY block above |
| **Jake Krajewski alpha FTUX** | ✅ PPM lens sent 7/30 (4 of 4 in). **Exec synthesizes Friday first thing** | On Exec's signal → I file the issues same day, against the A/B/C bucket structure |
| **PDR-006 + Q2** | ✅ **RATIFY sent 7/30 — all three reviews in; PA sent it to PM for ratification**. CXO drafting the PDR-004 amendment (Layer-B decision ratification, my reframe accepted); rubric branch OPEN, PA running Probe A on Claude + GPT | Watch for PM ratification → **then I draft the implementation epic** (PDR still says "issue TBD") |
| **Spatial committed-theory** | ✅ Slice delivered 7/30; Arch + CXO concur **(b)**. L3-beyond-GitHub NOT promised → cold island disposes freely. **L4 substance stands**: #1174 OPEN/Production, zero implementation, and "earned proactivity" is differentiator 4 of 4. ⛔ **My "milestone split" finding was WITHDRAWN** — M4 was swept; #1174 in Production is CORRECT by rule. CXO owns #1174, taking option (i) — which needs **no milestone change at all** | Owed by me: repoint stale `(M4/M5)` refs in roadmap.md + sprint-board-structure.md **as a class** |
| **Hooks** | ✅ **SETTLED.** Defect was TOCTOU (PreToolUse fires before the gated command, so a compound `add && commit` is judged against an empty index). Pard installed a real `.git/hooks/pre-commit` in the **common dir** — covers all worktrees by construction. **Do NOT probe** (v1.22 retired the probe apparatus); verify the hook file exists | Closed for PPM |
| **#1394 / ADR-078** | ✅ Architecture COMPLETE (unchanged since 7/16, reconfirmed OPEN-pending-D5-probe by 7/26 session) | Watch only |
| **Beta Blockers sprint recount** | Not possible — `gh` token lacks `read:project` scope (found by 7/26 session). Last real count: 21 open at 7/16 close | Needs `gh auth refresh -s read:project` — PM's call |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Current as of 7/19 only — 9+ days stale now given everything since | Needs a real refresh once the above items settle, not urgent today |
| **Docs-tree audit** | Plan delivered 7/13, still PM-gated as of last check | Watch |

## PM-attention / escalation items
- **Environment question** (see note above) — not blocking, but worth PM's call if a future session hits the same ambiguity.

## Mail status (2026-07-30)
**Inbox ZERO.** 50 memos triaged to `read/` at Fire 1, MANIFESTs regenerated. Deep-read: everything addressed *to* PPM + everything gating owed work. Triaged-not-deep-read: hook/m-44 cross-traffic where PPM is cc'd (now settled in CLAUDE.md).

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found
- ~~A canonical `ROLE-PORTFOLIO-PPM` doc. Flagged by two prior PPM sessions now (7/19, 7/26). Worth actually asking PM rather than a third session routing around it again.~~
  ✅ **RESOLVED 2026-07-29 — IT EXISTS AND ALWAYS DID.** `docs/briefing/ROLE-PORTFOLIO-PPM.md`, 118 lines, **self-authored by PPM**, commit `d9be35bbf`, `last_updated: 2026-06-27`. Sits with eleven sibling portfolios in the default briefing directory. Found by one `find . -iname "*ROLE-PORTFOLIO*"`.
  ⚠️ **Read this as a process finding, not a filing correction.** *Four* PPM sessions recorded it missing (7/19, 7/26, 7/28, and the predecessor's handoff) because each inherited this line instead of re-running the check — and the line gained confidence as it propagated, which reads as diligence and is actually the error compounding. It is the predecessor's own lesson #3 ("records that look authoritative are only as good as the discipline keeping them synced; checking costs less than it feels like") landing on the carry-forward itself.
  **Rule earned**: a "wanted but not found" entry is a **claim with a timestamp**, not a standing fact. It decays exactly like a status claim. Date it and re-check it, or don't inherit it.

## Predecessor handoff (Sections 4 & 6) — now durable
- `dev/active/handoff-ppm-predecessor-2026-07-28.md`. The predecessor's own lessons + load-bearing/commodity read — the content CIO's orientation note correctly flagged as the one thing artifacts couldn't supply.
- ⚠️ It arrived as **session-message text only**. The path the predecessor reported writing it to did not exist, and no copy existed on disk or on `origin/main`. Committed 7/29 from the message text; had that message not been relayed, it was gone. `mail-send.sh` refusing it was correct behavior (mailbox paths only) — the gap is that **there is no equivalent durable-delivery path for non-mailbox handoff artifacts**, and the fallback was "leave it uncommitted in the main checkout," which is exactly where it evaporated.

## Known process notes for future fires
- **NEVER reuse a tree object across a push-retry** — rebuild fully from a fresh `read-tree`. See `feedback_never_reuse_stale_tree_object_on_push_retry.md`.
- **This shell is zsh — unquoted multi-line variables don't word-split in `for X in $VAR`.** Use `while IFS= read -r`.
- **`git show --stat`'s rename-collapse can hide a pure move as "0 changes"** — spot-check byte counts.
- **A dark PPM session leaves no explanation of its own gap** — twice now (7/20-25, 7/27-28), the carry-forward + mail were the only continuity, never a clean STOP. Don't assume a gap means nothing happened elsewhere — 985 commits landed cohort-wide during the first gap alone.
- **Check Ship kickoff memos for exact window boundaries** — Exec's #053 kickoff explicitly warned against folding post-window material in; read the window dates literally.
- **ADR-077 / ADR-078 / ADR-079 are three different ADRs.**
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

**ARMED** — job `25af26ae`, `52 6,9,12,15,18,21`, six fires/day. **CronList-verified: exactly one.**

🔴 **GAP-C OBSERVED ON THIS SEAT, 2026-08-06 — with a tight before/after, which prior reports lacked.**
Job `c079437c` was CronList-verified present at the 08-05 22:22 STOP and fired normally today
(07:52 START, 09:52 WORK). **A context compaction occurred. `CronList` at 10:27 returned
"No scheduled jobs."** I ran no `CronDelete`; the job was created 08-05 so the 7-day expiry is not
in play. **The cycle would have gone silent with the registry still claiming coverage** — and the
only reason it didn't is that the compaction happened to leave me a turn in which to look.

⚠️ **State that narrowly**: what I observed is *cron present → compaction → cron absent*, not the
internals. I don't have the mechanism, and after this morning I am not going to assert one I haven't
measured. It is consistent with the skill's Gap-C note (session-scoped crons die silently;
`durable:true` is a no-op — PA 2026-06-07) and adds a same-session before/after to it.

⚠️ **Session-only + 7-day auto-expiry, both silent.** This is NOT a durable daemon. **The self-heal
only works if the session gets a turn at all** — a fully-dead cron has no trigger, so a seat that
compacts while idle stays dark until a human prompts it. The cure is external (Routines watchdog),
not anything I can do from here. Flagged to PM 7/30; reported to CIO 8/6 with this evidence.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
