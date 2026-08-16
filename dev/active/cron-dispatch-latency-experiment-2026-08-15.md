# Dispatch-latency experiment — 2026-08-15

**Purpose**: decompose the duty cycle's ~30-min dispatch latency below the documented 15-min
jitter floor (PM-approved 2026-08-15, carried across three workstream reviews before this).
Three one-shot crons scheduled at short intervals; each logs scheduled-vs-actual arrival time.

**Design**: 3 one-shot fires at 22:47 / 22:52 / 22:57 PT, 2026-08-15. Separate from the LEAN
duty-cycle cron (`ba1e4618`) — does not touch or interrupt it.

## Readings

<!-- each fire appends one line below in the form:
scheduled=HH:MM actual=HH:MM:SS offset=+Xm Ys
-->
scheduled=22:47 actual=22:47:03 PDT offset=+0m 3s
