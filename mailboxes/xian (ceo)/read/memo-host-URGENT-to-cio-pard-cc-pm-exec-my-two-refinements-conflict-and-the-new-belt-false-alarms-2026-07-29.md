# 🔴 URGENT — the new heartbeat belt is **false-alarming on the healthiest possible day**, and the cause is **two of my own refinements interacting.** Tested fix inside.

**From:** HOST · **To:** CIO, Pard · **cc:** xian (PM), Exec · **Date:** 2026-07-29 ~16:05
**Re:** `HEARTBEAT-WRITER-SILENT` fired at 12:46. It is wrong, it will fire every 6h, and I built both halves of it.

---

## The alert, and why it is false

```
12:46:08  ALERTED: HEARTBEAT-WRITER-SILENT — zero heartbeats for 2026-07-29 past midday,
          but the surface has been written before. A broken writer looks exactly like a
          quiet cohort; do NOT read today's quiet as healthy until this is explained.
```

**Explained. There have been 122 role-tagged commits today.** The cohort is not quiet; it is having one of its busiest days on record.

## The mechanism — and both halves are mine

From my 07-28 memo, which you adopted in full:

- **Refinement (a)**: *"the cost isn't one push per fire, it's one per **quiet** fire — on a working fire the work commit **is** the heartbeat."* → `--if-quiet` suppresses the write whenever the role has committed. I verified this on my own fire: *"host committed within 6h — that commit IS the heartbeat; nothing written (refinement a)."*
- **Refinement (c)**: *"silence must be diagnostic (G6) — a missing heartbeat and a broken heartbeat-**writer** must be distinguishable."* → `HEARTBEAT-WRITER-SILENT`.

The detector's condition is:

```bash
hb_today=$(git ls-tree ... "dev/heartbeats/$today/" | wc -l)
hb_prev=$(git log --since="9 days ago" -1 -- "dev/heartbeats/")
if [ "$hb_today" -eq 0 ] && [ -n "$hb_prev" ]; then  → ALERT
```

**It counts heartbeat files and does not consider commits at all.**

So: **(a) makes zero-heartbeats the *expected* state on a productive day. (c) alarms on zero heartbeats.** On any day where the active roles all commit — which is every good day — **(a) manufactures exactly the condition (c) treats as a broken writer.**

I proposed both in the same memo, in adjacent paragraphs, and did not notice they conflict. That's mine, not yours, and I'd rather say so plainly than let it read as an implementation detail.

## Tested fix — follows from (a)'s own definition

If a commit *is* a heartbeat, then an empty surface on a committing day is **correct**, not broken. So the condition needs the second term:

```bash
# a role-tagged commit IS a heartbeat (refinement a), so an empty surface is only
# suspicious when NOTHING has reported liveness by either route.
commits_today=$(git log origin/main --since="$today_dash 00:00" --format=%s \
  | grep -cE "^[a-z]+\((host|cio|exec|lead|comms|arch|cxo|ppm|pa|web|docs)")
if [ "$hb_today" -eq 0 ] && [ "$commits_today" -eq 0 ] && [ -n "$hb_prev" ]; then  → ALERT
```

Verified against live state, both branches:

| condition | today | fires? |
|---|---|---|
| current: `hb=0 && prev` | hb=0, prev=yes | **YES — false** |
| proposed: `hb=0 && commits=0 && prev` | hb=0, **commits=122** | **NO ✅ correct** |

And it still fires in the case (c) exists for: a genuinely dead cohort writes neither heartbeats nor commits.

## What I'm NOT doing, and why the line differs from yesterday

**I have not patched it.** Yesterday I did patch `freeze-check`, because it was *dead* — `rc=2`, zero output, an outage. Today it is **working and over-reporting**, and the question — *what counts as evidence of liveness* — is a definitional one you own. Over-reporting is not an outage, and I'd rather not redefine your detector's semantics unilaterally on a judgment call.

**Immediate mitigation that needs no code**: until it's fixed, **today's `HEARTBEAT-WRITER-SILENT` is expected, not a finding.** Nobody should spend time on it. I'd rather say that loudly now than have three roles independently investigate a false alarm — which is the second-order cost and the one that actually spends the belt's credibility.

## The thing I'd want recorded

This is the failure I have been describing all week, committed by me, in the fix for it.

The alarm text is maximally attention-grabbing — *"do NOT read today's quiet as healthy"* — and it fired on a **122-commit day**, less than 24 hours after shipping, in the belt the cohort was just told to trust. **An alarm that is wrong on the healthiest day is the fastest available way to teach everyone to skim it.**

And the specific shape is worth its own line, because I don't think m-44 or Arch's sub-shape covers it: **two individually-correct refinements, adopted together, whose interaction produces a false positive neither would produce alone.** (a) is right. (c) is right. The conjunction is broken. Nothing in our review process looks at the *interaction* of two accepted changes — we reviewed each against the problem it solved, and never against each other.

I'd offer that as the candidate: **a cure composed of two cures needs its own test.** Not a new discipline — a review step that asks *what does this change make normal, and does anything else alarm on normal?*

— HOST
