---
last_updated: 2026-09-20
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-20 at the 22:17 STOP.

> ## 🔴 READ FIRST TOMORROW — every START re-verify this seat has run has found a real stale row
>
> **Three for three now.** 09-19's re-verify found the #1688 "OFF by a ruling" row was true of `main`
> and NOT of prod (flag absent, not off). 09-20's re-verify found **that same corrected row was
> ALSO wrong** — the flag has been ON in prod since 09-07 (PM overruled the hold), and separately
> found the T-axis "closing window" was false and had already reached PM as a deadline, and that
> #1807 sat marked time-critical after it had closed.
>
> 📌 **The generalisable finding, stated once rather than per-incident**: this seat's own error mode
> is trusting a prior tracker entry over the live source. **The START re-verify step is not
> ceremony — it has paid out every single time it's been run.** Run it before touching anything the
> tracker claims is settled.

> ## ⏱️ THE CRON OFFSET IS NOT A STABLE SINGLE VALUE — even on one unrotated job, across a day
>
> Job `23d4c124` (armed 09-19 22:2x STOP, expires ~09-26) produced, today: 06:59 (+12) ·
> 09:59:47 (+12) · 12:59:49 (+12:49) · 15:59:48 (+12:48) · **19:18:51 (+31:51)** ·
> **22:17:14 (+30)**. ⭐ **Yesterday's "five for five, exactly +30" and this morning's "two for two,
> exactly +12" were both real reads of real data — and neither one is the job's stable constant. A
> job's offset can shift mid-day with no rotation at all.**
>
> ✅ **This does NOT need re-litigating.** CIO found the operative answer already ships:
> `duty-cycle-freeze-check.sh`'s `FIRST_FIRE_GRACE_MIN` defaults to **45 minutes**, and every value
> above fits inside it with margin. **Leave `first_fire` at the nominal cron slot; do not tune a
> registry row to any observed offset — today is direct proof a tuned constant goes wrong same-day,
> not just at the next rotation.** Full thread: `finding-cxo-to-pard-web-cio-cc-exec-pm-…` (09-20) and
> the closing memo to Web/CIO/Pard the same day.

> ## ✅ #1818 and #1823 — CLOSED, full arc in the tracker (below), nothing open
>
> PM ruled (b): kind-matched acknowledgment + one shared explanation string, fixed text, no gate
> exemption. Copy delivered same day. Turn-2+ scope split confirmed with Arch at 22:1x tonight:
> **my short form covers repeated pleasantries only; #1823's gate string fires unchanged on any
> substantive request.** Nothing further owed by me on either issue.

> ## ✅ Acceptance contract → v1.1 — my own artifact had a real gap, found by PM's first live transcript
>
> §5b's two-case enumeration for a bare affirmative was INCOMPLETE — PM's #1837 dogfood session hit a
> third case (acceptance silently captured by an unrelated flow) within four turns. Amended as a dated
> box, not a silent edit. **If a future acceptance-adjacent finding shows up, check §5b's amendment
> box before assuming the two-case version is still current** — anyone citing this contract from
> memory rather than the file is citing the pre-09-20 version.

> ## 🔴 THE FILE'S OWN HEADER WAS INVERTED FOR SIX DAYS ONCE — the reason for the discipline below
>
> A prior version's `last_updated` sat stale for days while the body stayed current — the *opposite*
> of the failure the frontmatter warns about, and it produces the same wrong answer for a reader who
> trusts the field over the prose. **Touch the date whenever you touch the body — same edit, not a
> later one.** *(This entry stays compact rather than re-told in full each rewrite — the lesson is
> "touch the date with the body," and this file now does, every STOP.)*

## 🔴 THE QUEUE IS THREE SOURCES, NOT TWO (PM ruling, 2026-09-11)

📌 **PM**: the work queue = **carried work + mail + newly-observed GitHub issues meeting role-relevant
criteria**; *"an agent should really only go idle when there is nothing to work on at all."*

🔴 **My `(0,0)` idle reports covered mail + tracker — two of three.** ⭐ **m-44 applied to my own status
line: "(0,0)" and "(0,0) of the sources I check" are different claims and I filed the first.**

✅ **My criteria line, proposed to CIO 09-11: `gh issue list --label UX --state open`.** Denominator
today **3** — #1166, #1174, #1108, all now in the tracker's UNBLOCKED column. ⚠️ **Stated blind spot: it
depends on the label being applied.** ⚠️ **And for a small label the useful form is "the open set is
non-empty," NOT "created since last fire"** — a last-seen marker would report clean forever on a standing
backlog.

> # 🔴🔴 THE ROOT CAUSE OF ALL OF THEM — found 2026-09-12, and I had already written the rule
>
> **Five steps of mine have silently stopped** (DAY-CLOSED 16d · MANIFEST regen 36d · heartbeat 24d ·
> `cohort-freeze-detect` unverifiable · **`check-refresh-promises.py` — never run once, in any log**).
> 📌 Exec's prompt: *"they share a single point of failure and it isn't any of them."*
>
> ⭐ **They share this: SUCCESS IS INDISTINGUISHABLE FROM SKIPPING.** Every one of them, run correctly,
> produces nothing I can see this fire — a green exit, a suppressed row, a file only tomorrow reads.
>
> ⚠️ **And I already wrote that rule, on 09-04, about the heartbeat**: *"a step whose omission is
> indistinguishable from compliance will be omitted."* 🔴 **I applied it to one step and never asked
> which others it covered.** **Fixed the instance, didn't sweep — the exact thing I criticised in
> someone else's work on 09-10.**
>
> **The test, applied to any step before adding it to this file:**
> > 🔴 **If running it and skipping it look the same to me at the end of the fire, it WILL rot.**
> > **Then it needs an external consumer or a visible output — never a firmer intention.**
>
> **The four that never rotted** (sync · mail drain · commit+push · tracker guards) **all fail
> immediately and visibly if skipped.** ⭐ **That's not virtue; it's feedback.**
>
> ✅ **Applied once already, same morning: I committed today's START entry BEFORE the mail loop** — my
> own proposed reorder, done on my seat rather than waiting for CIO's 7v pass. **The log's presence on
> `origin/main` is now the visible output the old ordering lacked.**
>
> 🔴 **PROMOTED 2026-09-13 — and finding out why is the sixth instance.** ⚠️ **This lesson was living
> ONLY here, in `dev/active/`, which is SPRINT-CLEANED.** ⭐ **My most transferable finding of the week
> was sitting in a file designed to be deleted.** 📄 **And my own 09-02 rule says it**: *the cycle log is
> ephemeral; nothing durable lives only there.* **I applied that to the cycle log and never swept it to
> this file.** ✅ **Now in `docs/briefing/CXO-SUCCESSOR-READ.md` §4, which is durable.**
> **Read that as the canonical home; this block is the working copy.**

## 🔴 EVERY DAY — the `DAY-CLOSED` marker. The FOURTH silently-stopped step, found 2026-09-11.

**At STOP, the session log MUST carry a literal `<!-- DAY-CLOSED: {YYYY-MM-DD} -->` line.** At **START**,
grep the *prior* day's log for it and **run the missed close if absent.**

🔴 **Measured 09-11: zero markers in my last 14 days. Last one was 2026-08-26 — a 16-day lapse**,
case (c) like the MANIFEST regen (36d) and the heartbeat (24d).

⚠️ **The self-heal failed for the same reason the step did.** Step 0's check *is* the prior-day grep — so
when I stopped closing days I also stopped checking, and ⭐ **the lapse and its detector stopped
together.** 🔴 **A self-heal that runs inside the same discipline it heals is not a net.**

⚠️ **And nothing external reports it**: `cycling_now()` reads the marker only to decide whether to
**skip** a role, so **a role that never closes its days just gets checked more — which reads as attentive,
not as a gap.**

✅ **09-10 closed retroactively (annotated idiom). 🔴 The other 15 days deliberately NOT retro-marked** —
that would manufacture a record of a discipline I didn't have.

## 🔴 EVERY FIRE — the invisible-success steps (all five now enumerated above)

**All case (c): invoked for a while, then stopped, with no signal.** Found by looking, not by alarm.

0. 🔴 **`check-refresh-promises.py --state-files cxo`** — the START-side currency check for this file's own
   frontmatter (skill addition 2026-08-30; I adopted the frontmatter, so it applies). ⚠️ **NEVER RUN ONCE
   — not in a single September log.** Ran it 09-12: **2 verifiable claims, neither stale.** ⭐ **Its own
   output states its coverage boundary, which is more than most checks do.** **This is the fifth, and the
   only one I never started rather than stopped.**
1. **MANIFEST regen** (skill Step 3, recipient-owned) — `python3 scripts/regenerate-mailbox-manifests.py
   --role cxo` after draining mail. ⚠️ **Lapsed 2026-07-30 → 2026-09-04, 36 days.**
2. **Heartbeat** — `scripts/duty-cycle-heartbeat.sh cxo {START|WATCH|WORK|STOP} --if-quiet` **before
   finishing the fire.** Lapsed 24 days. ⚠️ **It self-suppresses when the fire already committed**, so on
   a busy fire it costs nothing and writes nothing — **which is exactly why I skipped it for weeks
   without noticing.** ⭐ **A step whose omission is indistinguishable from compliance will be omitted.**
   Verified working on this seat 09-03.
2b. ✅ **SELF-VERIFY — AFTER the heartbeat. The word "after" is load-bearing.** *(skill v1.34/v1.35, CIO;
   adopted 2026-09-12.)*
   🔴 **2026-09-14: I ran this inside my START check batch, BEFORE the heartbeat, and it reported
   `BELT-INVISIBLE cxo … the writer ran before, then stopped`.** ⚠️ **True of the moment and a FALSE
   POSITIVE** — the day's heartbeat row didn't exist yet. **Ran the heartbeat, re-ran it in position:
   clean.** ⭐ **On the first fire of any day a pre-heartbeat self-verify reports BELT-INVISIBLE BY
   CONSTRUCTION.** ⭐ **A check's POSITION IN THE SEQUENCE is part of the check.** ⚠️ **And the message
   used case-(c) language — the exact shape of my five lapses — so it was very nearly reported outward
   as a real finding. What stopped it was reading the skill's wording before believing my own alarm.**
   Run `scripts/duty-cycle-freeze-check.sh` and **grep its output for `cxo`.** A `BELT-INVISIBLE` or
   `NO-SESSION-LOG` line naming me is an **in-fire action item**, not something for a colleague to
   notice days later. ⭐ **This is the first of my invisible-success steps to get an external
   consumer** — it hangs on a script that reads `origin/main` and can't be satisfied by my intention.
   ⚠️ **Its success signal is "no output," which was the same shape** — so I flagged that an unmatched
   grep means nothing unless the script actually ran. ✅ **CIO shipped that as v1.35 (`82de12e0d`) the
   same fire: Step 5b now confirms `rows=N` is non-zero itself.**
   ⭐ **So this is now the SKILL's step, not my private addition — follow the skill and don't maintain a
   second copy here.** ⚠️ **A hand-kept duplicate of a shared procedure is the drift shape I keep finding
   in other people's work** (three copies of one flag list; two failure-reporting paths). **Deleting my
   copy rather than keeping it in sync is the whole point.**
   *(Verified once on this seat 09-12: `rows=11`, one real non-alarm line (exec), no `cxo` line.)*
3. **`cohort-freeze-detect.sh` at START/WATCH — UNVERIFIABLE, and writing "I ran it" here does NOT fix
   that.** 🔴 **HOST's discriminator (09-04, supersedes my own framing): a record hand-narrated
   afterward by the agent whose compliance is in question is not evidence, however durable.** Only a
   marker the TOOL writes, in its own execution path, counts. **Run it at START — and don't let a log
   line saying you ran it read as proof that you did.** *(m-45's subject/scorer separation applied to
   compliance: an agent cannot attest its own procedural compliance, for the same reason PA cannot score
   PA's own probe.)*

## 🔴 NEXT FIRE — first move

Run `scripts/aging-standing-items.sh` and **check the per-file line reads `· cxo: 19`**
(⚠️ **updated 09-20 22:1x STOP: 18→19, one new #1837 row.** **Re-state this expectation every time you
add or remove a row** — the check only catches a count going DOWN, never a stale expectation going
up, and a stale expectation here has hidden a real gap before.). ⚠️ **A count below that means
my file is malformed, not clean** — that exact failure hid a third of my rows for a day on 09-01/02. CIO
shipped the per-file count specifically so this is visible without building a control.

🔴 **NEVER regex-edit the tracker — and the ROW COUNT IS NOT A VALIDATOR.** I broke it again on 09-10
(a scripted rewrite dropped a row's last two columns) and **the count read 8 both before and after**,
because the scanner counts lines. **Three scripted-edit incidents on that one file in ten days.**
✅ **Run BOTH checks after any edit** — `aging-standing-items.sh | grep '· cxo:'` **and**
`awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`). **Use `Edit`, not
`.replace()`.**

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

📌 **PM**: *"Fewer memos to Lead if they don't bear on current work or require their input… running
interference for a busy dev is part of the product role."* **It binds me, not just Exec.**

**Self-audit, 09-08→09-09: nine memos of mine reached Lead's inbox in two days.** Honest split — three
needed him (voice-watch review, which he acted on in 3h · the acceptance pass he *requested* · the FTUX
copy call). 🟡 One was a courtesy ack that could have been three lines. 🔴 **One was a clear miss: the
`mail-send.sh` false-positive. That's tooling, not his current work — it should have gone to CIO with
Lead cc'd.**

**The rule going forward**: *before addressing Lead, ask whether he is the one who must ACT.* If the
answer is "he wrote it" rather than "he must act on it," **cc, don't address** — and prefer CIO/PPM/Arch
as the primary. ⚠️ **Cc'ing is not free either** (four of the nine were cc's). **Do not write a memo
about writing fewer memos** — Exec owns the broadcast; this is a seat rule.

## 🔴 EVERY MEMO — filename budget, because MY habit turned CI red

**PPM found it while installing the mailbox invariant (09-10): my own memo's filename tripped the
pre-existing 180-char path lint and `Code Quality` was RED on `origin/main` until they baselined it.**

⚠️ **They baselined the artifact — the correct remedy for an already-merged file — and the habit that
produced it is mine to change.** ⭐ **That is yesterday's own lesson ("a cleanup that doesn't change the
behaviour is a rollback") landing on me the next morning.**

**Measured, not estimated** (09-11): longest inbox dir is `mailboxes/dispatch-dinp/inbox` = 29 chars,
so with the `/` the **basename budget is 150**. Of my 09-04→09-11 memos, **one was 161** (the red one)
and **three more sat at 142–150** — I run at the edge habitually, not occasionally.

🔴 **Working rule: keep the memo basename ≤ 130 characters.** That is ~20 of headroom against the real
limit, and it costs nothing — **the subject line carries the argument; the filename only has to be
findable.**

> ### 🔴 FOURTH scripted-edit incident on my own state files — 2026-09-11, this fire
>
> **I wrote *"Use `Edit`, not `.replace()`"* into this very file yesterday, then used `.replace()` on it
> this morning** and produced a garbled count sentence plus a dropped section heading. **Caught by
> reading the file back, not by any check.**
>
> ⭐ **The mechanical conclusion, since the prose rule has now failed four times: a rule I wrote, in a
> file only I read, does not change my behaviour.** **The only thing that has worked is the column
> check** — an external command whose output I can't rationalise. 🔴 **So: state-file edits go through
> `Edit`, full stop, and any `.replace()` on `dev/active/*` is treated as a defect regardless of whether
> it looks right afterward.**

## Waiting on others — nothing owed to PM

**Nothing is currently queued for PM from this seat.** T-axis tokens ("spend the tokens now") land on
PA's queue, not mine — my half was pre-registered scoring properties, owed to PA this cycle, not to
PM. #1824's classifier owner is Lead's open question, not mine.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants **PM-ratified 08-31**; criteria/branches CXO-editable. **Open the file
  for its version — no version numbers in briefings.**
- **C-axis**: report **per bucket, never pooled**. `not_applicable` = full marks at C=2. The
  C=2-clustering diagnostic applies to the **`required` bucket only**.
- 🔴 **BYOC rubric (v0.7.2 as of 09-18)**: T axis still `PENDING-PROBE`. **Open the instrument itself
  before scoring anything** — it names FOUR blockers, and as of 09-20 only three are token-solvable
  (one vendor / n=1 / a design confound). **The fourth — "still our model, not the actual MCP
  surface" — is stated in the instrument's own §6c as sufficient on its own to hold `PENDING-PROBE`
  regardless of spend.** Proposed splitting the axis (T-own-surface vs T-MCP-surface) to PM/PPM; not
  ruled on as of this writing. **Owe PA pre-registered scoring properties before their round.**
- ⭐ **Standing bias to correct for: I model the host as executing literally; it SYNTHESISES.** My
  prediction record on this class is **0 for 3** as of 09-19 — pre-registration in writing, before
  seeing output, is the only mitigation that has worked. Treat any new mechanism claim of mine as a
  candidate until tested against real output.

## Live threads (watch only)

🔴 **PRUNED 2026-09-20 STOP — the prior version of this section was 09-08 through 09-10 content,
eleven days stale, sitting under a file whose own header claims per-stop currency.** Every item in it
was either closed, superseded by a later ruling, or already carried more currently in
`cxo-standing-items.md` (the durable tracker, which is where open items belong — this file is
ephemeral session state, not a running history). **Kept nothing rather than re-verify eleven days of
claims I'd need to re-check anyway; the tracker is the source of truth for what's actually open.**
Current open items: see `dev/active/cxo-standing-items.md`, 19 rows, both guards clean as of tonight.

## Cron

✅ **RE-ARMED at the 2026-09-20 STOP: `23d4c124` → new job** (delete-then-create; `CronList` singular
before signing off — id recorded in the sign-off section below). **Expiry ~7 days from tonight's
arm-time.**

⭐ **Rotate at the FIRST fire with both the information and the margin.** ⚠️ **A target DATE here quietly
outranks the RULE that produced it** — name the rule, not just the date.
🔴 **`CronList` proves a job OBJECT exists. The only proof a cron FIRES is a fire.**
🔴 **And per tonight's finding above: do NOT infer the new job's offset from today's data.** A job's
offset is not even stable within itself across a day — the 45-min grace absorbs it; don't tune
anything to a number from the outgoing job.

## ⚠️ AMBER COLD-START RESTART may land overnight

⚠️ **`docs/handoff-cxo-2026-09-18.md` is now TWO DAYS STALE** — verified stale in two places at
09-19 arrival (cron job id, tracker row count) and superseded further by everything above since. **No
seat change happened tonight, so no fresh handoff doc was written** — under an ordinary overnight gap,
**this carry-forward plus tonight's session log
(`dev/2026/09/20/2026-09-20-0659-cxo-code-log.md`) are the load-bearing artifacts.** If a genuine seat
change lands, write a fresh dated handoff before assuming the 09-18 one still applies — it doesn't.

## 🔴 WHAT NO CHECK OF MINE CATCHES — the 09-18 tally, kept because it is uncomfortable

**Five defects in my own record found in one day, every one by LOOKING, none by a mechanism:**
1. a registry claim that my 09-16 `CronDelete` was never executed *(it was)*
2. a wake memo expecting a 09-16 close *(already written)*
3. a word count I asserted without counting *(~474 against a ~400 ceiling)*
4. **my stated PRIMARY GOAL with no tracker row at all** — invisible to the aging check because it was
   never entered
5. **the carry-forward's own count expectation stale at 11 for six days**, read past every fire

✅ **The one a check DID catch**: `check-refresh-promises.py` flagging this file stale after the
standdown — ⭐ **the step I had never run until 09-12.**

> 🔴 **The aging check watches rows that EXIST. A missing row and a stale expectation are both invisible
> to it.** ⚠️ **That is a denominator problem inside the tool I use to catch denominator problems.**
> ⭐ **Until something better exists, the mitigation is the one that worked: re-read the expectation
> against the number you just ran, every fire, and treat a mismatch as a finding rather than a typo.**
