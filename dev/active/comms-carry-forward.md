# Comms carry-forward — 2026-08-01 STOP (21:12) → for the Aug 2 START

**Host**: Amber.local · **Model A** `~/Development/piper-morgan-worktrees/comms` · `claude/comms-cycle`
**Session log**: `dev/2026/08/01/2026-08-01-0642-comms-code-log.md` — `DAY-CLOSED: 2026-08-01` ✓
**Cron**: re-armed at STOP by delete-then-create (id transition in the registry row)

---

## ⚠️ FIRST THING TOMORROW — Sunday Aug 2 has a post AND a live problem

**"The Architecture That Wrote Its Own Case" publishes Sun Aug 2** and is in the same state today's post was in at 06:42: **never voice-passed** (last touch Jul 9), **no art**, and it carries an **open `[PM VOICE-PASS: ...]` bracket**. Check the calendar at START — do not assume Sunday is quiet. Today proved that check load-bearing.

⚠️ **And the redundancy I escalated Aug 1 is now LIVE, unresolved.** Aug 1 and Aug 2 were drafted from the **same source day** (both dated May 28), open with the same thesis, and **the Aug 2 post contains a section literally titled "Mechanism beats vigilance"** — which is the title of the post that published yesterday. Published back-to-back, it reads as a repeat. **PM's call: merge, reorder, differentiate, or accept.** If it publishes as-is, that section title at minimum wants changing.

## Open for PM — 5 items

1. ⚠️ **Beats 24-28 slate steer** — the only item with a date behind it (queue dry after Aug 18). **Now REVISED against §1.5** (`dev/active/comms-narrative-slate-proposal-2026-07-29.md`, revision appended Aug 1): Beat 25 re-cut (was three A plots in one), CI streak double-count removed, Beat 27 sharpened. Needs: **5 or 4**, titles (**Beat 25 needs a new one regardless**), spine.
2. **Beats 21-23 voice-pass + art** — Aug 11 / 13 / 18.
3. 🔧 **`/hooks` open or a session restart** — HOST's memory counterweight is written, registered, **not live**. It `wc`s at fire time so it does not share a failure mode with the unreliable built-in counter.
4. **Compose-UI restore-banner observation** — wipe path fixed; restore path still unobserved.
5. **Watchdog wording** on "What the Running System Found" — long-standing, non-blocking.

## Editorial state

- ✅ **"Mechanism Beats Vigilance" PUBLISHED Aug 1** — verified live, all ten fixes present. Ten fixes, **three of them re-applications** after a silent revert.
- ✅ **Ship #054 workstream review filed Jul 31**, a day early.
- **Ratified Aug 1 — §1.5 of `building-narrative-method.md`**: *a beat is a STORY, not a digest of its window.* A plot, optional B plot, something odd — **not** a section per workstream. **Measured**: length +75% in five months, July mean above ceiling, **but span does NOT predict length (r=+0.10)** — so leaps and cuts are not in tension.
- **Ratified Jul 30**: role-gloss is **register-scoped**. Apply **both halves** — parenthetical on first mention AND bare acronym after.

## Live process hazards (not fixed, know about them)

- **Two write paths collide.** PM's browser can revert agent commits by saving from a stale page — happened Aug 1, cost three fixes. **Distinct from the autosave-closure bug Web fixed** (`8d2db3c`). ⚠️ **My Jul-29 judgement that this was too rare to build against is WITHDRAWN — twice in three days.** Practically: **after PM edits, re-read before assuming your fix survived**, and `git pull` immediately before proofing.
- ✅ **Caption double-quoting FIXED self-healing** by Web (`673b10e`) — strip now loops, wrap is idempotent, corrupted values repair on next save.
- **16 calendar rows have a media filename in `caption`.** On **7 of them caption is AUTHORITATIVE and `cartoon` is stale** (verified: caption renders 7/7 live, cartoon 0/7). ⚠️ **Do NOT "clean up" that column** — it holds the only correct record. Reported to Docs.

## Habits earned (apply, don't just recall)

- **Check the artifact, not the record about it.** Five separate times on Aug 1 this was the thing that mattered: live page over status flag (×2), `git log` over `status`, rendered image over calendar column, my own commit over my memory of having fixed it.
- **A false alarm gets trained around.** I explained away a broken sign-off check for four days because I knew what the number meant. **The tell is a standing explanation for a standing anomaly.**
- **Build the distinguishing cell**, not more confirming evidence.
- **mail-send: build recipient list and path list from ONE loop.**

## State flags

- STOPped cleanly, day fully accounted for. Inbox **zero** (16 memos triaged).
- Queue at close: **(0 unblocked, 5 PM-gated)**. Nothing unblocked held.
- **Upstream repointed to `origin/main` today** — sign-off check 2 is meaningful now (was measuring a ref dead since May 31).
- First fire tomorrow **06:12**. Next front after the slate: **50 logs across Jul 29–Aug 1, no omnibus past Jul 28.**
