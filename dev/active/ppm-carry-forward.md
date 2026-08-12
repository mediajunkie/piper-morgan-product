# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-08-12 07:22 PT (START fire). Cron **`71dc6b7c`**, unchanged since the
08-11 post-reboot re-arm. 08-11 retroactively closed this fire (missed STOP fires, see Cron
section below); nothing lost. Sprint-truth re-run fresh this fire: **MVP 48 not done / 1042
done** (matches Lead's 08-11 escalation figure, now independently verified rather than trusted).
The three PM-open items (criterion blessing, #1510 fork, Surface 1/3) re-checked via GitHub —
all still genuinely open, no PM movement since 08-10.
✅ **Jake conversion COMPLETE: #1536–#1540 filed 08-09, zero rows unfiled.**

## 🔴 AWARENESS FROM 08-11 16:1x — Lead's escalation to PM (not mine to action, but changes what I cite)
Read via mail triage, addressed to PM with PPM cc'd; **no PPM-owned decision, PM's three calls
(#1600 ratchet-fix-now?, #1599 is_admin grant method, deploy word)** — do not chase these, PM has
them. **What changes my own reasoning going forward:**
- **MVP open count moved 51 → 48**, composition not just number — 9 genuinely closed with evidence,
  2 (#1411, #1431) have live reproducing defects despite looking closeable, #1485 blocked by the new
  admin-403 beta blocker, #1480's client-side half is unverified (grep-only, JS never executed).
  ⚠️ **Do not cite "51 open" going forward — it's stale as of today.** Re-run `sprint-truth.py`
  before citing any count rather than trusting this note past today.
- **CI has been red on `main` two days** (#1600, ratchet ceilings breached, gating `smoke` marks
  failing) and **Architecture Enforcement red on every push since 08-09 15:07** — a STOP condition
  per CLAUDE.md, PM's to triage, not mine, but relevant context if any PPM spec work assumes green CI.
- **New beta blocker #1599**: `is_admin` unset for anyone (1377 users, zero admin) — 7 routes 403,
  including the Slack app-token save (#1201). PM-gated.
Filed for my own awareness only; moved to `mailboxes/ppm/inbox/read/` after triage, nothing else
required of PPM.

## ✅ FTUX FIVE RULED (2026-08-10) — HOLD STATE ENDED
**#1536 → MVP + Beta Blockers** (PM: *"if CXO feels one of the issues should be kept in MVP, I am
inclined to defer to that and err on the side of including"* — CXO's on-record argument was exactly
one issue). **#1537–#1540 → Production + PUB.** ✅ **Verified on the board.**
**PM resolved CXO's tension by clarification, not by us**: *"something can be discovered in alpha, and
we can decide to defer it before going into beta… comfortable with my placement and with clarifying
or overriding my needlessly blanket statement from earlier."* ⭐ ***"Out of alpha" = the PUBLIC beta***;
private beta stays invite-only until PUB completes.
✅ **#1536 now gates on the converged three** (CXO's two-tier + my merge + Arch's H1 clarify) —
`docs/internal/product/first-contact-criterion-merged-2026-08-10.md`. **Item ③'s block discharged.**
**Awaiting-decision population: 7 → 2** (#1511, #1569).

## ✅ #1511 IS MY SPEC LANE (PM direction 08-10) — slice ACCEPTED, spec on the issue
**Two modes, not one winner**: report-on-demand **default** (ratifies live behaviour) · interview
survives as a **NAMED** mode · possible first-run interactive fallback + preference capture.
**MVP** = the naming/disambiguation only (**the interview already works — anything touching its
behaviour is OUT**); **Production/PUB** = fallback + preference.
🔴 **The merge I added: #1511's preference capture IS #1510's declared mode in another domain.**
Lead spotted the shared *storage* (`users.preferences` JSONB); **the MECHANISM matters more —
declaration, REVOCATION, and showing the user what Piper believes about them.** *Two surfaces
inventing two revocation stories is how you get a preference nobody can find to change.* **Ride
#1510's surface, don't parallel it** — ordering already right since #1510 is MVP.
⚠️ **Anti-goal risk flagged**: a first-run *"what standup do you want going forward"* asks at the
moment of **least information**. **Demonstrate then ask** (as #1536), and make it **visibly revisable**
— *an unfindable preference is the dictating PM's anti-goal is about, arriving by accident.*

## ✅ PM APPROVED THE PLACEMENT (2026-08-09, relayed by Lead, board WRITTEN)
**#1510 → MVP · #1190 → MVP · #1509 → Production.** Verified on the board myself. **#1536–#1540
remain NONE, correctly — their unmilestoned state IS the ask.**
⚠️ **PM sequence correction, cohort-wide**: **MVP → Production → Fast Follow.** *"'MVP or Fast Follow'
encodes a misunderstanding by many agents."* **"Not MVP" NEVER defaults to Fast Follow.** Production =
required for PUBLIC beta, worked in the **PUB sprint**.
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
✅ **AND THE OWED RESIDUE IS NOW DRAINED TOO** (08-06 STOP). Scoped it: only **5** live refs, and **3 were correct as written** — the roadmap's own §M4 triage record, the briefing line that *instructs* readers what to do on seeing `(M4 territory)`, and a narrative about a stale artifact. **Fixing those would have been the error.** The 2 real ones were in my own entity-model spec.

✅ **The accurate source is `docs/internal/planning/beta-blockers.md`** (see its lines 12 + 20).

**Cost of not knowing this (2026-07-30)**: I reasoned from the two stale docs and produced three
successive wrong readings of one roadmap line, then recommended moving **#1174 into M4** — a
dissolved sprint. PM caught it. **I had run the sweep myself and it was in no artifact I carried.**
✅ **Repointing DONE 08-06** — and doing it as a class is what made it cheap (5 hits, 3 false positives). 🔴 **It also surfaced something worse**: chasing the 2 real refs led to **#1216**, which is **CLOSED COMPLETED 2026-07-07 in MVP** — while `roadmap.md:143` had claimed for a **month** that it *"remains OPEN"* and was a *"Beta Blocker candidate pending PM's call."* **It landed in MVP, so the call I was waiting on had been made by ACTION rather than by ANSWER, and I kept carrying it as PM-gated.** ⭐ **An item can leave your PM-gated queue without anyone telling you, and nothing in the queue notices.**

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

## ⛔ THE WEB UI IS NOT GOING AWAY — my sort key was a FALSE QUESTION (PM, 2026-08-08)

**READ THIS BEFORE ANY SURFACE/ROADMAP REASONING. Second time I've made this error.**

**PM verbatim**: *"I never said the web UI was going away… the modeled user experience is **not
specific to any one surface**. It's a holistic user experience, **expressed on each surface as
appropriate**"* — phone as notifications · **Slack** as a channel bot · **web** as conversations +
radar + settings · **another chat** as skills + MCP server · **CLI still maintained**. **All true at
the same time.** *"We can make decisions about what to ship first… but I have never said that we are
abandoning any one of those services."*

**PDR-005 never said otherwise**: decision **(b) "primarily MCP; thin web UI"**; option (a) *"no
Piper-specific UI in v1.0"* **explicitly REJECTED as infeasible**; **5 of 7 MUX/UI surfaces scoped
1.0-required**.

⭐ **The mechanism — "read more carefully" doesn't explain a repeat:**
1. I read a **PRIORITIZATION** statement as an **ONTOLOGY** statement. *"Primarily"* orders work; I
   made it a claim about which surfaces **exist**. Same family as production/trust/Notion/shipped:
   **"primary" = first-in-sequence vs. the-only-real-one.**
2. 🔴 **Building a SORT turned a misreading into infrastructure.** A sort needs a discriminator, so I
   **manufactured an axis**, and the axis smuggled in competition between complementary surfaces.
3. **Why it recurs cohort-wide**: the holistic model is **simultaneous truths**; decision artifacts
   are **singular commitments**. The doc's grammar wins every time. ⚠️ **It IS documented and
   referenced** (Nov-2025 holistic-UX brief; PDR-004 §Scope; PDR-005 lists PDR-004 under Related) —
   **so "not written down" is not available. It survives only in docs nobody opens mid-decision.**

**WITHDRAWN**: the sort key, at source in the synthesis §3 + my 07-30 memo + #055 framing. ⚠️ **PM
RATIFIED the bucket sort 08-05 on my framing** — flagged loudly rather than left standing.
⛔ **Do NOT re-key by patching labels** — any *survival* phrasing reintroduces it. Likely honest key:
**"which surface does this defect live in."**

✅ **#1477 re-anchored: a SURFACE-1 defect** (PDR-005:53 — *"left rail = current session"*),
1.0-required + scheduled. **Never needed the welfare exception.** ⚠️ **#1476's surface is NOT
verified** — couldn't locate what renders the "blocked" card; **do not assume it matches #1477.**

🔴 **OPEN, PM's to answer**: PM said the MCP path **"may emerge as primary"** — a **sequencing
possibility, not a settled ordering.** The re-sort waits on PM's read of how the surfaces relate.
**I treated an open question as closed once; not inferring it twice.**

## 🔴 CURRENT — ⚠️ BETA MOVED BACK A MONTH from Aug 9 (PM, 2026-08-08 ~10:10)

**Verified at source, `decisions.log:1242`.** PM verbatim: *"I am going to move the beta data back a
month. **We clearly have a lot more work still to do than anyone ever reported to me.**"*

⚠️ **That second sentence is about REPORTING, and I am a reporting role.** Context: T4/T5 verification
surfaced structural flaws (#1471/#1490/#1521 pre-classifier over-claiming · #1517 floor fabricating
capability denials · #1520 silent session expiry) on top of the denominator over-reporting Exec named
the same morning.

🔴 **MY SPECIFIC SHARE, so a future session doesn't re-derive a vague one**: **two of the six
NOT-STARTED items are mine** — **#1476 and #1477**, filed 07-31 as the bucket-A **welfare carve-out**
(*"fix regardless"*). **For eight days I reported them as filed and never once reported that nobody
had picked them up.** Portfolio said "advanced." #055 §0 said "advanced." **Neither false; both let a
reader infer motion that didn't exist.**

⭐ **The mechanism, which is the reusable part**: I gave PM *"21 open in MVP"* — **a total with no
parts**. And **`gh issue list --state open` CANNOT see board Status**, so it structurally cannot
distinguish *unstarted* from *awaiting PM's review*. **I was answering "how much is left" with a tool
that only answers "how many are open."** Not carelessness — **confident reporting from an instrument
that couldn't answer the question I was implicitly answering.**

**FIXED FORWARD**: use `scripts/sprint-truth.py` output **verbatim** (adopted 08-08, before the move
landed), or state explicitly what I excluded. **Report not-started AS not-started** — "filed,
unstarted, N days," never "advanced."

**Accurate gate state (08-08)**: `MVP: 22 not done (6 Sprint Backlog, 1 Blocked, 3 In Progress, 12 In
Review); 1021 done` — **with two corrections I found**: #1107 is CLOSED with a stale non-Done status
(so In Review is 11), and **#1509/#1510 are absent from the board entirely** (`gh issue create
--milestone` does NOT add to the board) → **≈23 genuinely not-done.** ⭐ **The 6 unstarted is the
planning number, not the 23.** And **In Review is the largest bucket, waiting on PM** — so the
critical path has been PM's attention, not build capacity.

**ASKED PM**: do #1476/#1477 still hold? They were a *welfare* carve-out justified by alpha testers
staying on the web UI meanwhile — **that reasoning may not survive a month's delay**, and I'd rather
re-ask than leave them unstarted on a rationale I stopped checking.

✅ **v30 IS LIVE and #1484's gate IS DEPLOYED — the 08-06 "gate is absent" reading is SUPERSEDED.**
CXO deployed 08-07 08:04 PDT and verified **off the running container** (`fly ssh console`, reading
`/app`): **`gate=2`** in `socket_mode_runner.py`, #1482's false-permanence strings gone, honest
replacement present. **Not an ancestry check, not a version inference, not a branch.**
⚠️ **Arch's 08-06 "0 occurrences in production" was a BRANCH query** — and `origin/production` is
**12 days stale** (`34744d184`, 07-26). I re-measured: **0 on that branch, 6 on `main`, and the
running artifact matches MAIN.** Arch has taken this and says they used branch ancestry as a
deployment check twice this week, false negative both times.
**#1386 criterion 5**: one green line, **NOT closed** — Arch posted it with the two remaining items
explicitly unclaimed. **My criterion-2 signature stands** (measured against `main`; layer was right).

🔴 **STANDING, and it is the week's most reusable rule**: **`origin/production` IS NOT THE
DEPLOYMENT.** Three layers — branch ancestry (*is it in some ref?* — **five of us got this wrong on
08-06**), `fly status` (*what version serves?*), and ⭐ `fly ssh console … grep /app/…` (***what does
the running system contain?*** — **no inference step at all**). **Use the third to answer a
deployment question.**

**1. Radar/Surface-1 is SETTLED — do not re-derive it.** Radar's rendering is **Surface 1** (history
sidebar, #1236). PDR-005 specifies a **cross-client variant** of it at `:122`, `:245`, `:288`, `:328`;
**PDR-005:135 + roadmap.md:127 both mark it "unblocked NOW", ~4-6 days.**
✅ **THE "WEAKER GROUNDS" CAVEAT I CARRIED IS RETIRED (2026-08-07, CXO).** PDR-005:84's rating was
written **2026-06-05**; **#1237 closed 06-18 and #1236 closed 06-19** — **the rating predates the
feature by 13–14 days and described a history list, not a ranked multi-entity attention surface.**
CXO ran PDR-005's own test on what exists: **criterion 1 MET strongly** (`feed.py:52` sorts by
`attention`; four heterogeneous sources; serializing to text loses the simultaneity + ranking that
*is* the information). CXO was revising **their own** Round-1 rating.

**My contribution, filed 08-07** — CXO's *"which of the five are named is unenumerated"* gap:
- ✅ **The five ARE enumerated — as BUILD LANES, `roadmap.md:127–129`, not as scope in PDR-005**:
  **Surfaces 1, 2, 4, 6, 7.** (2.1 = 1+7, 2.2 = 2+4, 2.3 = 6.) Scope inferable from schedule,
  asserted nowhere. **Surface 1 already has a lane marked "Unblocked NOW"** — so it is scheduled for
  1.0 and CXO's flattening risk did not land in the schedule; only the *justification* was stale.
- 🔴 **Surface 3 is a PHANTOM.** Whole-corpus grep: **one** MUX-roster mention, `PDR-005:84` — the
  very sentence pairing it with Surface 1. **No name, no doc, no ADR, no build lane** (Surface 2 has
  90 mentions + its own design doc). ⚠️ **And "Surface 3" collides**: in the *insight-delivery*
  numbering it means push-insights (#1032), so a grep lands on a confidently wrong referent.
- **Asked PM for**: the one sentence on Surface 1, **plus** name Surface 3 or strike it and say
  "5 of 6." **No urgency attached** — beta isn't gated on it.
⛔ **My earlier answers "the web page goes" and "undecided" are both WRONG.** Superseded.

**2. Awaiting PM** — ✅ **#1462 ANSWERED 08-07: Product / "PUB - Public beta" sprint** (with #1463).
Exec's note: *"you held #1462's milestone deliberately rather than guessing… PM's answer is a sharper
placement than either of us had. That's the held-question pattern working."* **Remaining five are all
milestoned already** (#1476 MVP · #1477 MVP · #1482 MVP · #1483 Production · #1485 MVP) — ⚠️ **verified
08-07, so what I was "awaiting" on these needs re-stating or dropping; do not re-ask as a block** · the **six Jake items** (PM answered 1, 2→"(b)", 5; needs plain English on 3 and 6 — 3 sent,
6 is PA's) · **canonical criterion text**.
✅ **CLOSED 08-06, both were on this list and both resolved**: **#1481 scope** — PM RULED the
socket-mode path **HELD** from alpha/beta/release until safe, *held not deferred*, with connector
work **front-loaded in Production** (sequence filed on #1440). **MVP milestone** — now reads
**2026-08-09**.
⚠️ **Before re-asking PM anything on this list, CHECK GITHUB FIRST.** #1216 sat here as PM-gated for
a month after closing. **The queue does not notice when an item leaves it.**

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

⚠️ **Pruned 2026-08-12** — the table this replaced (dated 7/28–7/31: Ship #053, the 07-31 gate
window, Jake's PPM-lens-only stage, PDR-006 pre-ratification, spatial (b), hooks TOCTOU, etc.) was
**three weeks stale and every row already superseded by newer sections above** (Jake is fully
converged and filed 08-09; PDR-006/spatial/hooks status folded into other sections; #1386's 07-31
window closed criterion 2 only, already recorded). Kept as a pointer, not carried forward as
content — if any of those threads turn out to still be open, that's a finding, not an inheritance.
**Current open-for-PM items are the three in `docs/handoff-ppm-2026-08-11.md` §2** (criterion
blessing, #1510 fork, Surface 1/3) — re-checked via GitHub at this fire (08-12 07:22): **all three
still genuinely open, no new PM comment on #1510, #1386, or the criterion doc since 08-10.**

## PM-attention / escalation items
- **Environment question** (see note above) — not blocking, but worth PM's call if a future session hits the same ambiguity.

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

**ARMED** — job **`71dc6b7c`** (re-armed 08-11 13:18 post-reboot; the 08-11 06:52 job `25f1a782`
was deliberately parked pre-reboot, not lost — see `docs/handoff-ppm-2026-08-11.md` §6-7).
`CronList`-verified exactly one, and the clearing condition (armed + verified + a fire has run) was
satisfied at the 08-11 16:22 WORK fire. Prompt carries the standing lines: **PROXIES** (*safe when
the remainder is ROUTED, dangerous when merely IMPLIED — say "gateable fraction", never "shadow"*)
and **MAIL-SEND CAN FAIL SILENTLY** (*a transient fetch failure leaves the memo unsent with no other
signal; read the tail, verify it landed*).

⚠️ **08-11's log had to be retroactively closed at this fire** — the 18:52/21:52 STOP fires never
reached the session (heartbeat history confirms zero rows, not dropped work; likely absorbed by the
reboot-recovery gap). Nothing was lost. ⚠️ **Session-only + 7-day auto-expiry, both silent** —
`71dc6b7c` expires ~2026-08-18 if not re-armed sooner.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
