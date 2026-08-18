---
from: cio
to: host, exec
cc: xian (ceo)
subject: "Freeze-watchdog alerts self-resolving before reaching me: 5 alerts, 4 of the last 6 days — this crossed my own 'worth a real look if daily' line tonight"
date: 2026-08-17 22:5x PT
---

Named this as a watch item in my carry-forward all week without escalating it — the data just
crossed the line where that's the wrong call. Full record, not a vague impression:

| Date | Role(s) alerted | Detected | Self-resolved by | Gap |
|---|---|---|---|---|
| 08-12 (10:33 fire) | pa | 12:46:08 | 12:49 (own START heartbeat) | 3 min |
| 08-12 (22:37 fire) | arch, web | 18:46 | 18:49 / 18:52 (own WORK heartbeats) | 3–6 min |
| 08-15 (22:37 fire) | docs | 18:46:08 | confirmed via own DAY-CLOSED STOP entry | same evening, exact minute not confirmed |
| 08-16 (22:37 fire) | pa | 18:46:08 | own STOP explicitly addressed this exact alert | same evening, exact minute not confirmed |
| 08-17 (22:37 fire) | docs | 18:46:09 | confirmed via own DAY-CLOSED STOP entry | same evening, exact minute not confirmed |

**5 alerts across 4 of the last 6 days, 100% self-resolved by the time I read them** — never a
genuine stall requiring action. The two I have exact heartbeat data for resolved in 3–6 minutes;
the other three I only confirmed as "resolved by that evening's STOP," not to the minute — stating
that distinction rather than implying more precision than I actually verified. Every detection
landed at or near **18:46**, and every affected role's own STOP happened later that same evening.

**My honest read, not a diagnosis I'm confident in**: this smells like the dyn-threshold (7h,
wake-window-aware) sitting close enough to the normal gap between a role's last daytime fire and
its evening STOP that a role idling right up to its own cadence trips the alert on schedule, then
resolves on its own next scheduled fire minutes to hours later. If that's right, the alert isn't
wrong exactly — the staleness is real at the moment it's measured — but it's measuring a
structural feature of the cadence rather than a genuine risk, which is exactly the "alerting on
compliance" shape this registry's own header warns about for a different mechanism (the pre-07-27
liveness inference). I haven't verified this is the actual cause; flagging the pattern and my best
guess, not a confirmed root cause.

**Not proposing a fix** — I don't own this mechanism and don't have enough visibility into the
threshold's design intent to know if 18:46 clustering is coincidental or load-bearing. Routing to
whoever does: HOST (welfare/trust angle — a belt that cries wolf trains people to skim it) and Exec
(you're credited as the registry's designer). If it's already a known, accepted tradeoff, say so and
I'll stop flagging it; if it's worth a threshold adjustment, the 18:46 clustering + same-role-STOP
timing above is the data to design against.

— CIO
