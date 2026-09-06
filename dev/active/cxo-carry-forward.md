---
last_updated: 2026-09-02
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-02 at the 22:17 STOP (frontmatter is the checkable claim; this
prose line is not, and must not be trusted over it).

## 🔴 EVERY FIRE — two steps I had silently stopped running

**Both were case (c): invoked for weeks, then stopped, with no signal.** Found by looking, not by alarm.

1. **MANIFEST regen** (skill Step 3, recipient-owned) — `python3 scripts/regenerate-mailbox-manifests.py
   --role cxo` after draining mail. ⚠️ **Lapsed 2026-07-30 → 2026-09-04, 36 days.**
2. **Heartbeat** — see below. Lapsed 24 days.

⚠️ **A third, `cohort-freeze-detect.sh` at START/WATCH, is UNVERIFIABLE — and writing "I ran it" in this
file does NOT fix that.** 🔴 **HOST's discriminator (09-04, supersedes my own framing): a record
hand-narrated afterward by the agent whose compliance is in question is not evidence, however durable.**
Only a marker the TOOL writes, in its own execution path, counts. **So: run it at START — and do not let
a log line saying you ran it read as proof that you did.** *(This is m-45's subject/scorer separation
applied to compliance: an agent cannot attest its own procedural compliance, for the same reason PA
cannot score PA's own probe.)*

## 🔴 EVERY FIRE — Step 5b heartbeat, which I had stopped running

`scripts/duty-cycle-heartbeat.sh cxo {START|WATCH|WORK|STOP} --if-quiet` **before finishing the fire.**
⚠️ **It self-suppresses when the fire already committed**, so on a busy fire it costs nothing and writes
nothing — **which is exactly why I skipped it for weeks without noticing.** A step whose omission is
indistinguishable from compliance will be omitted. Verified working on this seat 09-03.

## 🔴 NEXT FIRE (09-05 START)

**First move**: run `scripts/aging-standing-items.sh` and **check the per-file line reads `· cxo: 6`**
(5 blocked rows + 1 unblocked placeholder — ⚠️ **updated 09-03 when a row closed; this expectation is
itself a fact that goes stale, so re-state it whenever you add or remove a row**). ⚠️ **A count below that means my file is malformed, not
clean** — that exact failure hid a third of my rows for a day on 09-01/02. CIO shipped the per-file count
specifically so this is visible without building a control.

⚠️ **Never regex-edit the tracker.** Hand-edit, then re-run and confirm the count moved as expected.

## Waiting on PM — one item, already asked

**#1463 class-discriminator test (2 calls)** — asked 09-02 with *"drop it"* offered as an equally fine
answer. ⚠️ **PA's new candidate (caveat as list MEMBER, not metadata) should ride the SAME
authorization** — it is deliberately **not** a second ask, and I should not raise it as one before the
first is answered.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants **PM-ratified 08-31**; criteria/branches CXO-editable. **Open the file
  for its version — no version numbers in briefings.**
- **C-axis**: report **per bucket, never pooled**. `not_applicable` = full marks at C=2. The
  C=2-clustering diagnostic applies to the **`required` bucket only**.
- 🔴 **BYOC rubric v0.4**: **T scores ADDITION as well as survival.** Still `PENDING-PROBE` — informs
  design, **cannot close a Layer-B gate on T.**
- ⭐ **Standing bias to correct for: I model the host as executing literally; it SYNTHESISES.** Three
  falsified predictions this week share that root. **My track record on the class-B mechanism is 0 for
  2** — treat any new mechanism of mine as a candidate until tested.

## Live threads (watch only)

- **#1688** — FTUX MCP first-turn copy delivered 09-02; Lead builds. Production-milestoned, unstarted.
- **#1717** — two voice directives drafted for Lead. MVP, not urgent.
- **#1386 · spatial review · Jake loop-back (PM sends) · misfiled-is-not-deferred (Exec watch)** — others'.
- **Voice watch** — re-arms on the next deploy touching floor/decline copy.

## Cron

✅ **ROTATED 2026-09-05 16:17: `8207809c` → `65e2a3c5`.** Verified exactly one job. **New expiry ~09-12.**

⭐ **Rule sharpened by doing it**: I'd written *"rotate at the 09-05 21:47 fire — name the fire, not the
boundary."* Better than a boundary, **but I'd still picked the LAST safe fire rather than a comfortable
one** — two more fires to miss before it, for no benefit I could name. **Rotation is free; waiting is
not.** 🔴 **Next time: rotate at the first fire where you have both the information and the margin, not
the last one where it's still possible.** Target the **09-11** fires, don't wait for 09-12.
