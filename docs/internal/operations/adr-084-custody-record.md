# ADR-084 custody record (HOST)

Names, dates and caps only. No value, length or id of any credential is written here. Opened 2026-11-16 after xian's yes to ADR-084 (relayed by Exec, 06:20 PT). HOST adds a row when a step is done and Exec or the seat that did it reports it; a row says who reported, not that HOST saw the console.

| Item | State | Date | Reported by | Notes |
|---|---|---|---|---|
| Anthropic workspace `lead-scoring` | seat workspace, $150 a month as the hard bound; $10 a run a seat may spend without asking | 2026-11-16 | Exec (xian's words) | Budget rule: planned calls in the log before, actual cost after, in-code stop (#2383). |
| Key `lead-scoring-2026-10` | disabled, not deleted | 2026-11-16 | Exec (xian: "revoked (disabled, actually)") | xian: nothing he runs personally uses it. A disabled key cannot spend; only xian can re-enable. Arch ruled 2026-11-16: disabled is enough, deletion not required. |
| Key `seat-screens-2026-11` | the one live key in `lead-scoring` | 2026-11-16 | Exec | Not yet in any seat's file. Step A puts it in Lead's settings file. |
| Operations reader flag on `web-seed-1386` | set | 2026-11-16 | Exec, from xian's screenshot | Set by xian on beta's Account flags page. The page cannot make an account admin. Seat check of a counter read waits on `seat_session.py` (#2388). |
| Step A: Lead's seat key file | pending | | | Gate: three logged Read refusals before the key prompt. HOST's two Reads owed. |
| Seat accounts (two) and test GitHub machine account | pending | | | Step F; second seat account waits on #2389 and xian naming the email. HOST reads what each holds before first use. |
| MCP deploy token | pending | | | Step H; waits on #2384. Expiry and name go here when chosen, no value. |
| Seat browser LaunchAgent and debug-port bound | pending | | | HOST reads Pard's plist and wrapper before xian loads it. |
| OpenAI seat project and hard limit | pending | | | Step E provider half; menu names unverified. |
