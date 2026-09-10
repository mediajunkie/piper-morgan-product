---
last_updated: 2026-09-09
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-09 at the 16:17 fire.

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

Run `scripts/aging-standing-items.sh` and **check the per-file line reads `· cxo: 7`** (6 blocked rows +
1 unblocked placeholder — ⚠️ **updated 09-09 13:17: acceptance-contract row added; this expectation is itself
a fact that goes stale, so re-state it whenever you add or remove a row**). ⚠️ **A count below that means
my file is malformed, not clean** — that exact failure hid a third of my rows for a day on 09-01/02. CIO
shipped the per-file count specifically so this is visible without building a control.

⚠️ **Never regex-edit the tracker.** Hand-edit, then re-run and confirm the count moved as expected.

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
  DESTRUCTIVE bar.** Lead builds. **Still open and mine to remember: do arms drop on topic change? I
  raised it as a question and never answered it.**
- 🟡 **Six-cousin epics (Arch causes / PPM ordering)** — offered cousin #4's user-facing half 09-09
  (*a decline is a claim about a capability* — my #1730 copy is the worked case). **One risk flagged
  once**: #1/#2/#4 all terminate in something a user reads; a correct model can still ship N sentences.
  **Asked only for a line naming whose the user-facing contract is — not a gate.**
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

✅ **ROTATED 2026-09-05 16:17: `8207809c` → `65e2a3c5`.** Verified exactly one job. **Expiry ~09-12.**

🔴 **ROTATE AT A 09-11 FIRE.** ⭐ **Rule sharpened by doing it**: I'd written *"rotate at the 09-05 21:47
fire — name the fire, not the boundary."* Better than a boundary, **but I'd still picked the LAST safe
fire rather than a comfortable one** — two more fires to miss before it, for no benefit I could name.
**Rotation is free; waiting is not. Rotate at the first fire where you have both the information and the
margin, not the last one where it's still possible.**
