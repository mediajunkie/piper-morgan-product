# Mail v4 audit, Exec's half of the 11-05 pilot review

**Auditor:** Exec. **Written:** 2026-11-05 06:03 PST. **Window:** v4 messages to or cc exec, sent after the 10-22 review (10-22 10:30) up to 11-05 06:00. **Source:** `piper-morgan-mail` origin/main, the message headers plus `acks/exec.log`, read by a script. Canaries are excluded.

## Result

**14 of 14 acted on or needing no action. 0 dropped.** All 14 are acked. The 10-22 review asked for a 20-message sample, and only 14 exist in the window. That shortfall is itself the main finding (below).

| # | Sent | From | Type | What it asked | Exec's ack | Acted? (verified how) |
|---|---|---|---|---|---|---|
| 1 | 10-23 10:08 | cio | decision-request, due 10:30 | Alpha DB down; run B4 now | read 10:10 | Yes: relayed to xian at 10:10, plus an urgent note to Janus (exec log 10-23, 10:10–10:16) |
| 2 | 10-28 10:08 | cio | task | v4 inbox unread, no canary | done 10:11 | Yes: ran inbox, canary PASS, changed habit (ack note) |
| 3 | 10-29 06:50 | lead | decision-request | Promotion dispatch permission | read 06:52 | Yes: on rollup v646 with lean (ack note) |
| 4 | 10-29 06:54 | cio | reply | (a)/(b) for the same | read 07:06 | No action needed |
| 5 | 10-29 06:54 | cio | decision-request | One exact allow, xian's hand | read 07:06 | Yes: rollup v647; xian said yes 11-03, relayed (msg 9) |
| 6 | 10-29 08:03 | lead | task | Call tested-path push hold | done 08:10 | Yes: hold sent to all seats 08:06 (ack note) |
| 7 | 10-29 08:20 | lead | fyi | Hold can lift | done 08:20 | Yes: lift broadcast (ack note) |
| 8 | 10-29 09:41 | lead | task | Call the hold again | done 09:42 | Yes: broadcast fcd58f0f2 (ack note) |
| 9 | 10-31 10:09 | cio | reply (escalation) | 9a allow waiting 2 days | done 11-03 17:37 | Yes, late: it waited on xian's answer, which came 11-03 17:30, and the relay went out the same hour |
| 10 | 11-01 10:15 | cio | decision-request | Concept-link --ratchet on? | read 11-01 19:09 | Answered by Lead at 10:18 (msg 11); Exec was cc and needed to do nothing. The ack came 9 h later |
| 11 | 11-01 10:18 | lead | reply | yes | read 19:09 | No action needed |
| 12 | 11-02 10:09 | cio | decision-request | #2230 flag paste waiting | read 10:12 | Yes: it was already on the rollup (step 2); replied. #2230 is CLOSED (`gh`) |
| 13 | 11-02 10:25 | cio | reply | My grep was wrong | read 10:25 | No action needed |
| 14 | 11-02 10:56 | cio | decision-request | May CIO edit check-branch.sh (#2251) | read 12:32 | Yes: xian's yes relayed 12:32. #2251 is CLOSED (`gh`) |

## Findings

1. **Volume collapsed.** There were 14 messages to Exec in 2 weeks, against 51 in the first 2 weeks. Nothing has been sent on v4 since 11-02, so 11-03 and 11-04 had zero v4 traffic, while v3 carried hundreds of exec memos. The cause is the pilot's own rule: any message with a non-pilot participant goes v3, and nearly every thread now includes PPM, HOST, Arch, CXO or Web. So v4 tests delivery well but hardly touches the routing bottleneck xian named (decisions.log 11-03 13:18). Whether to widen it is xian's call.
2. **Required-ack decision-requests with no `due` (msgs 10, 12, 14) default to 1 day.** All three were acted on within the day, but msg 10's ack came 9 h after Lead had already answered. It was an ack-hygiene lag, not a missed action.
3. **Canary:** today's ran at 06:02 (PASS). The rule from 10-28 (run `inbox` on the first wake) held on 11-04 and 11-05 per `acks/exec.log`.

Verified how: a script over the 14 message headers and `acks/exec.log` on origin/main; outcomes from my session logs 10-23, 10-29 and 11-02 (grepped) and `gh issue view` for #2230 and #2251. Layer: ack log plus action evidence. Denominator: 14 of 14 in the window.
