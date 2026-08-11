# Handoff — Comms — 2026-08-11 (Amber reboot, macOS 26.6)

**Role**: Communications · slug `comms`
**Worktree**: `~/Development/piper-morgan-worktrees/comms` · branch `claude/comms-cycle` · **Model A**
**Cron**: `f53ad8c5` · `12 6,9,12,15,18,21 * * *` · rotated 2026-08-10 STOP · **expires ~2026-08-17**
**Written**: 2026-08-11 ~06:25 PT, against Pard's stand-down notice.

**Written to be survivable on a COLD start** — i.e. assuming `--resume` fails for this seat specifically and someone picks up from files alone.

---

## 0. 🔴 CRON IS PARKED — READ THIS FIRST, IT IS THE THING THAT WON'T ANNOUNCE ITSELF

**I deliberately cancelled my duty-cycle schedule at 2026-08-11 ~06:5x PT, before the reboot, per Pard's second stand-down notice.** `CronList` verified: **"No scheduled jobs."**

**Mechanism**: session-scoped `CronCreate` — `CronList` labels it `[session-only]` and the tool contract says it dies with the session. **It leaves no trace on disk. Nothing will re-arm it automatically.**

⚠️ **After the reboot this seat is DARK until someone runs the command below.** A dead session-scoped cron is invisible: the fleet comes back looking healthy and this role simply never fires again.

### To restore — exact expression AND prompt, because the schedule alone is not enough

`CronCreate` requires a prompt. Re-arming with the cadence but the wrong prompt produces a cron that fires into nothing.

- **cron**: `12 6,9,12,15,18,21 * * *`  *(windowed, 6×/day; last fire of the day = 21:12 → STOP)*
- **recurring**: `true`
- **prompt** — verbatim:

```
DUTY CYCLE TICK — run the `duty-cycle-tick` skill.

ROLE: Communications · role-slug: comms
WORKTREE: /Users/xian/Development/piper-morgan-worktrees/comms (Model A — stable per-agent worktree on Amber, branch claude/comms-cycle)
CRON: 12 6,9,12,15,18,21 * * * (windowed, 6×/day; last fire of the day = 21:12 → STOP)
LAUNCH MODEL: Model A (Amber, stable worktree, reused every session)

End every fire with: scripts/duty-cycle-heartbeat.sh comms {START|WATCH|WORK|STOP} --if-quiet
```

**Prior job ids, for tracing**: `e37fa867` → `c635f4d1` (rotated 08-05) → **`f53ad8c5`** (rotated 08-10, **parked 08-11**).

⚠️ **On re-arm, use CREATE-THEN-DELETE if rotating** — a failed create leaves you silently dark; a failed delete leaves duplicates that Step 1 detects and heals. Here there is nothing to delete: **create only, then verify with `CronList` that exactly one job exists.**

**The watchdog registry row is parked to match** (`dev/active/duty-cycle-registry.tsv`). **Its clearing condition is falsifiable and deliberate: clear the parked note ONLY when `CronList` actually shows an armed job — not when someone intends to re-arm it.**

---

## 1. State at stand-down

**Clean.** Tree 0 uncommitted · **0 unpushed** · 0 behind `origin/main`. Yesterday closed properly (`<!-- DAY-CLOSED: 2026-08-10 -->`); today's log created. **Nothing was mid-flight when the notice arrived.**

---

## 2. 🔴 The one time-critical thing

**A post is scheduled to publish TODAY and is not ready.**

| | |
|---|---|
| **Post** | *The Write-Path Chase* (Beat 21) |
| **Slot** | **Tue Aug 11 — today** |
| **File** | `docs/public/comms/drafts/the-write-path-chase.md` |
| **State** | `drafted` · **550 words** · **no art** (`image`/`alt`/`caption` empty) · **PM voice pass not done** |

**PM said on 08-10 they would prep it that evening. It did not land** — last commit on the file is 2026-07-23.

**What it needs**: PM's voice pass + art. **Nothing from Comms.** It is pre-passed and clean.

⚠️ **550 words is CORRECT — do not pad it.** Measured: published narratives run **597–2,564** (median 1,403); *Almost Beta* shipped at 597. The `template-audit` word-count target of 800–1,300 describes only **2 of the last 14** published pieces and was recalibrated for this reason (v1.10).

⚠️ **A flag on this post was WITHDRAWN 08-10 — do not re-raise it.** I had flagged *"five stacked point releases"* vs three problems named. **The primary Lead log (`dev/2026/07/09/…-lead-code-log.md`, "Full chain") lists exactly FIVE.** The count is correct; the draft narrates three of the *problems*, and releases ≠ problems. Withdrawal is recorded on the calendar row.

**When PM clears it**: run `template-audit` (v1.10) **after** their pass, then **send the publish-ready memo to Docs FROM COMMS.** ⚠️ **Send it even if PM says they will tell Docs** — that assumption cost the Aug 6 slot; run-of-show step 3 now says so explicitly.

---

## 3. Open items, by owner

### PM
- ⭐ **Beats steer — the only item with a real date.** Eight candidates for seven slots; **narrative queue runs dry after Aug 18.** Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html` (current, safe to steer from). Needs: five beats or four · titles for **25 and 28** (28 collides with Ship #054) · Beat 24's A-plot restated (its *"more than half"* claim is refuted) · **and PM's call on whether they appear in Beat 25**, since primary logs put them in the chain.
- **Today's post**: voice pass + art (§2).

### PM + CXO
- **CXO's §3 entity-model line** (*"knows your work as things"*) in `docs/internal/design/experience-across-surfaces.md` is marked **✏️ pending PM**. **Flagged three times; still unratified.** The marketplace listing copy rests on it.

### Dispatch (filed at `~/Development/dispatch/mail/` — NOT on the `mailboxes/` system)
- **3 genuinely unsyndicated posts**: *The Package and the First Bite* (Jul 9), ***Drained on Paper* (Aug 7)**, *Verify at the User Path* (Aug 8) — no Medium, no LinkedIn.
- **1 partial**: *The Team Catches the Cycle* — Medium only.
- ✅ Two others were **bookkeeping only** and I already corrected them to `distributed`.

### Comms (me) — next moves
1. **BYOC listing copy v4.** Task force is live and moving. **v3 sent 08-10**; open question routed to **PPM**: does *"answers from that model"* hold against **#1440's contract** for connectors live at listing time?
2. ⚠️ **`scripts/scan-inbox.py` has MORE variants outstanding.** I fixed variants 1–3 on 08-10. **HOST then found a real memo in a fourth, plus a fifth; PA confirmed and fixed the fifth.** 3 unread memos in `mailboxes/comms/inbox/` carry the detail. **Deliberately not actioned during stand-down.**

---

## 4. Things a cold start would get wrong

- **`scripts/scan-inbox.py`** is the inbox scanner — **use it, not a `grep '^from:'`**, which is blind to ~19% of memos. ⚠️ Its `unparsed` count was **structurally incapable of reporting non-zero** until 08-10; **a historical "unparsed: 0" means nothing.**
- **Registry edits** (`dev/active/duty-cycle-registry.tsv`): **edit as PLAIN TEXT.** `csv.writer` re-quotes `#` comment lines containing quotes — it corrupted 7 of them on 08-05.
- **Cron rotation**: **create-then-delete**, not the skill's documented delete-then-create. A failed create leaves you silently dark; a failed delete leaves duplicates Step 1 heals.
- **Publication checks**: read the calendar's **`blogURL`**, never build the URL from the draft filename — PM retitles change slugs. And **assert content presence before checking absence**; the site was a soft 404 until Web fixed it 08-04.
- **Beta moved back a month** (08-08). Ship #054 published carrying *"new target: Aug 8"* — **PM ruled no retroactive edit and no correction notice**; the honest form is a future Ship saying it moved. **Exec has been told #055 must carry it.**

---

## 5. Continuity files

| file | holds |
|---|---|
| `dev/active/comms-carry-forward.md` | current cron, dated items, open questions |
| `dev/2026/08/11/2026-08-11-0621-comms-code-log.md` | today |
| `docs/internal/planning/comms/editorial-calendar.csv` | **the schedule — source of truth**; per-row notes carry pre-pass findings |
| `docs/internal/planning/comms/upcoming-beats-plan.html` | the beats slate awaiting PM |
| `.claude/skills/template-audit/SKILL.md` | v1.10; read the Ship-calibration table and check #12 before trusting a word count |

— Comms
