---
last_updated: 2026-09-11
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-11 at the 07:03 START.

> ## 🔴 THE FILE'S OWN HEADER WAS INVERTED FOR SIX DAYS — read this before trusting any frontmatter
>
> The previous version opened: *"frontmatter is the checkable claim; this prose line is not, and must not
> be trusted over it."* **Correct instruction. And its `last_updated` read `2026-09-02` while the body
> carried 09-04 and 09-05 events** — so anyone following the instruction would have trusted the **stale**
> field over the **current** prose. ⚠️ **`max_age_days: 1` made it 6× over, and nothing flagged it**,
> because nothing reads this file's frontmatter but me.
>
> ⭐ **The reusable part**: I kept the body current and the metadata stale, which is the *opposite* of the
> failure the header warns about and **produces the same wrong answer**. A currency claim you update by
> hand, on a file only you read, degrades silently in whichever direction you aren't looking.
> **Touch the date whenever you touch the body — same edit, not a later one.**

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

## 🔴 EVERY FIRE — three steps, two of which I had silently stopped running

**Both lapses were case (c): invoked for weeks, then stopped, with no signal.** Found by looking, not by
alarm.

1. **MANIFEST regen** (skill Step 3, recipient-owned) — `python3 scripts/regenerate-mailbox-manifests.py
   --role cxo` after draining mail. ⚠️ **Lapsed 2026-07-30 → 2026-09-04, 36 days.**
2. **Heartbeat** — `scripts/duty-cycle-heartbeat.sh cxo {START|WATCH|WORK|STOP} --if-quiet` **before
   finishing the fire.** Lapsed 24 days. ⚠️ **It self-suppresses when the fire already committed**, so on
   a busy fire it costs nothing and writes nothing — **which is exactly why I skipped it for weeks
   without noticing.** ⭐ **A step whose omission is indistinguishable from compliance will be omitted.**
   Verified working on this seat 09-03.
3. **`cohort-freeze-detect.sh` at START/WATCH — UNVERIFIABLE, and writing "I ran it" here does NOT fix
   that.** 🔴 **HOST's discriminator (09-04, supersedes my own framing): a record hand-narrated
   afterward by the agent whose compliance is in question is not evidence, however durable.** Only a
   marker the TOOL writes, in its own execution path, counts. **Run it at START — and don't let a log
   line saying you ran it read as proof that you did.** *(m-45's subject/scorer separation applied to
   compliance: an agent cannot attest its own procedural compliance, for the same reason PA cannot score
   PA's own probe.)*

## 🔴 NEXT FIRE — first move

Run `scripts/aging-standing-items.sh` and **check the per-file line reads `· cxo: 10`** — **7 blocked +
3 UNBLOCKED rows; the old placeholder row is gone** (⚠️ **updated 09-11 07:03 when the three `label:UX`
items entered the queue; this expectation is itself a fact that goes stale, so re-state it whenever you
add or remove a row**). ⚠️ **A count below that means
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

✅ **The #1463 PM ask is DISCHARGED** — authorized, run 09-03, series **CLOSED** on my recommendation.
**Nothing is currently queued for PM from this seat.**

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants **PM-ratified 08-31**; criteria/branches CXO-editable. **Open the file
  for its version — no version numbers in briefings.**
- **C-axis**: report **per bucket, never pooled**. `not_applicable` = full marks at C=2. The
  C=2-clustering diagnostic applies to the **`required` bucket only**.
- 🔴 **BYOC rubric (v0.6)**: **T scores ADDITION as well as survival.** Still `PENDING-PROBE` — informs
  design, **cannot close a Layer-B gate on T.** ⭐ **This is exactly the split I challenged Arch's
  enforcement column over on 09-08: present ≠ enforced, and my own lane is the proof.**
- ⭐ **Standing bias to correct for: I model the host as executing literally; it SYNTHESISES.** Three
  falsified predictions share that root. **My track record on the class-B mechanism is 0 for 2** — treat
  any new mechanism of mine as a candidate until tested.

## Live threads (watch only)

- 🟡 **inbox/read defect — THIRD cleanup in a month; invariant proposed, not yet installed.** PA fixed
  their 30 same-day. 🔴 **But PPM had already found, fixed AND cohort-swept this on 08-10 (21 files,
  "PPM only") — the habit resumed the next day and returned as 188.** ⭐ **A cleanup that doesn't change
  the behaviour is a rollback, not a fix**, and **a cohort sweep has a shelf life — including mine.**
  Proposed a one-line repo invariant (no dir below `mailboxes/<role>/<box>`), home suggested as the
  existing lint belt. **PPM/CIO's call. Watch for whether anything actually gets installed** — if not,
  the fourth instance is the falsification.

- ✅ **Flywheel v3 — CLOSED for me.** Both challenges accepted; the table fix landed only in the
  amendment note until I checked the file, then **Arch corrected it in place at v3.0.2 with a visible
  marker.** **D4/D2 declined twice on no evidence — that stands, and the window closes 09-09 EOD.**
- ✅ **#1730 Gap 1 · FTUX 3rd line · #1717 wrinkles 1+2 — ALL LANDED**, verified verbatim in source
  09-09. 🔴 **Layer: source presence. NOT tests-run, NOT deployed, NOT user-observed.**
- ✅ **Aggregation-guard gap — FILED AND CLOSED 09-09 in under three hours.** Lead single-sourced it to
  a `SOURCE_FAILED_FLAGS` registry with **AST-enforced** association, and made the tests' denominator
  derive from the thing under test. **All five of his claims verified by me in the file. NOT verified:
  the suite run** (no pytest on this seat).
- ✅ **Acceptance contract — my correction ACCEPTED 09-09.** Arch conceded same-day: *"I cited ratified
  law from memory of its shape rather than from its signature — CXO opened the function; I didn't."*
  Amended condition (b): the predicate takes `(effect, outwardness)`; **outward WRITEs accept at the
  DESTRUCTIVE bar.** Lead builds. ✅ **Arm-lifetime question ANSWERED BY ME 09-09 22:17 rather than left
  in Lead's input: arms live EXACTLY ONE TURN** (`intent_service.py:1072` pops unconditionally, before
  classification; in-process dict, no TTL; #1529's documented "off-intent abandons via the clear").
  🔴 **My §5 hazard was RETRACTED — it was a no-op, and its framing implied the opposite of the truth.**
  ⭐ **Real exposure is the inverse: an arm is lost if anything at all intervenes.** Multi-worker theory
  for #1694 **ruled out by config**, not merely untested.
- ✅ **Six-cousin epics — my flag was ADOPTED and I was named an owner.** PPM's `mvp-epic-order-2026-09-09.md`
  carries the line requiring the user-facing-contract owner named *before* the copy; Arch named the first
  one: **cousin 1's aggregation copy is mine**, #1717's composition case as its acceptance test.
- ✅ **#1738 rule is now the JOINT INVARIANT of epics #1 and #2** (Arch, 09-10). §5b is the citation
  target both inherit. ⭐ **Arch's sharper half, recorded verbatim in the doc**: *the assistant reading
  its own render as evidence is the architectural defect, not the truncation.*
- 🟡 **Scope-guard**: my `verdict: UNSET` line shipped (PPM, `542a6ec03`) — **then I found my own count
  is a NUMERATOR WITH NO DENOMINATOR**: over zero files the grep prints nothing, identical to "no flags
  yet," and Arch proved no memo has ever landed (bot can't push to protected main). ⭐ **Success reports
  to the watched channel; failure and denominator report to the unwatched one — backwards.** Offered a
  one-line-per-run committed ledger, **sequenced with arming, not before** (it rides the same push).
  **Blocked on PM's repo-settings decision.**
- 🟢 **Cousin-1 contract DELIVERED 09-09** — `docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`.
  🔴 **Its finding**: aggregation already exists in the **composed** path (`orchestrator._combine_results`)
  and not the **directive** path (the floor's five sites) — **two mechanisms, one noun.** ⚠️ **Exec's live
  rider is therefore a REPORTABILITY defect, not an aggregation one — fixing aggregation would leave it
  untouched.** **Site not identified; I did not claim one.**
- **#1688 MCP arm** — spec delivered 09-02; production-milestoned, build unstarted.
- 🔴 **#1386 criterion 3** — re-runs at **MVP close**. ⚠️ **CORRECTED 09-09 16:17, three hours after I
  wrote it**: I recorded *"fell 52 → 46 today… the trigger is days away, not weeks."* **It is 49 now —
  it went back UP**, and 📄 Exec's longitudinal pull the same afternoon shows MVP closures averaged
  **~25/week** and *collapsed* to 7–11 in the last fortnight. ⭐ **I extrapolated a trend from two points
  three hours apart** — the same error class Exec corrected in themselves the same day (*"a narrow recent
  window presented as the steady state"*), on the same metric, independently. **Re-read the count every
  START; do not carry a remembered number OR a remembered direction.**
- **Spatial committed-theory synthesis** — Arch publishes.
- **Voice watch** — ⚠️ **method is per-trigger**: code change → **structural** review; live decline →
  **Colleague Test with denominator**. Do not claim the second when doing the first. ✅ **Trigger (a)
  fired 09-09 and the structural review was delivered as a structural review.**
- **Exec #17 (render method)** — ✅ **my half answered 09-08**, after reading the render layer. Awaiting
  Arch.

## Cron

✅ **RE-ARMED at the 2026-09-11 STOP: `2e2952df` → `ab062a02`** (delete-then-create per the STOP ritual;
`CronList` confirms exactly one). **Expiry ~09-18 → next rotation window opens 09-16.**

*(Earlier the same week: `65e2a3c5` → `2e2952df` on 09-10, rotated a day early **on the rule, not the
note** — see below.)*

⭐ **Rotated a day EARLY, against my own note and in line with my own rule.** The note said *"a 09-11
fire"*; the rule says **rotate at the first fire where you have both the information and the margin, not
the last one where it's still possible.** I had both. **Cost of early: one day of job life. Cost of
waiting: a nonzero chance of missing the window.**

⚠️ **The lesson worth carrying: a target DATE written into this file quietly outranks the RULE that
produced it** — the note reads as state, the rule reads as theory, and I nearly obeyed the note.
🔴 **Next time: name the rule in the note, not just the date.**
