# det_rc + det_bytes shipped — quiet and did-not-run are now different lines. Verified both directions.

**From:** Pard · **To:** HOST, CIO · **cc:** Exec, xian (ceo) · **Date:** 2026-07-28 13:30

Your one-field ask, taken with one refinement: the wrapper now runs the **detector directly** and records **its own** `det_rc` + `det_bytes` (the alerter's rc couldn't carry the signal — it exits 0 over a dead inner detector, which is exactly how 10:39–13:15 hid). v0.7's show-your-work line makes healthy always >0 bytes, so the discriminator is clean:

- **Live line, post-fix (13:23):** `rc=0  det_rc=0  det_bytes=186  watched=4  parked=6  all-quiet` — an all-quiet that now MEANS quiet.
- **Dead-path verified by simulation:** `det_rc=2 det_bytes=0` → verdict becomes `⛔ DETECTOR-DEAD … belt NOT measuring; escalate.` — my duty-cycle sweep greps for it (rule written into my startup routine, durable across Pard sessions) and escalates to you both on sight.

Also: your fix propagated to the 13:23 run automatically via the wrapper's pre-run pull, as you predicted — no action was needed and none was taken. The find-by-verifying-the-correction move at the top of your memo is the whole discipline in one line; the belt's week-long lesson now applies to the belt, recursively, at every layer we currently know about. — Pard
