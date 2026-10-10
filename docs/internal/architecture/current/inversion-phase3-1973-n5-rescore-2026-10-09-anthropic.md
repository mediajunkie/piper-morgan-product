# #1973 — N=5 fresh router scores for the 9 past-deletion rows (served model, 2026-10-09)

Arch's #1973 ruling: (a) router credit needs N=5 fresh served scores, all five the expected op at or above
0.8 (the dispatch threshold); else (b) surface-2 credit under rules 3 and 4; else (c) restore. Served model:
anthropic:claude-haiku-4-5 (resolved post-fallback, #1620), one `--phrase` call per sample, 45 calls.
The asserted table records each row's LOWEST of the 5 scores, so the gate reads the conservative value.

**Result:** 5 of 9 pass (a). 4 fail (a) and go to surface-2 (b):
`inversion-phase3-surface2-floor-probe-2026-10-09-n5-anthropic-1973.md`.

## All samples

| phrase | 5 samples (op@conf) | (a) all five >= 0.8 on the expected op |
|---|---|---|
| pull up my schedule | meeting_time@0.72, meeting_time@0.72, meeting_time@0.72, meeting_time@0.72, meeting_time@0.72 | no |
| walk me through my appointments | week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85 | yes |
| show all appointments | week_calendar@0.75, week_calendar@0.75, week_calendar@0.75, week_calendar@0.72, week_calendar@0.75 | no |
| what are the upcoming events | week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85 | yes |
| when am i free | week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85 | yes |
| when do I have free time | week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85 | yes |
| what are my open slots | week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85, week_calendar@0.85 | yes |
| I'd like a risk assessment for this project | analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72 | no |
| please identify the risks in this plan | analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72, analyze_blockers@0.72 | no |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| pull up my schedule | TEMPORAL | action:week_calendar | `meeting_time` @0.72 | MISMATCH | N=5 min; (a) FAILS (sub-threshold or other op) -> surface-2 probe |
| walk me through my appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH | N=5 min; (a) router credit: 5/5 >= 0.8 |
| show all appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH | N=5 min; (a) FAILS (sub-threshold or other op) -> surface-2 probe |
| what are the upcoming events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH | N=5 min; (a) router credit: 5/5 >= 0.8 |
| when am i free | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH | N=5 min; (a) router credit: 5/5 >= 0.8 |
| when do I have free time | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH | N=5 min; (a) router credit: 5/5 >= 0.8 |
| what are my open slots | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH | N=5 min; (a) router credit: 5/5 >= 0.8 |
| I'd like a risk assessment for this project | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.72 | MATCH | N=5 min; (a) FAILS (sub-threshold or other op) -> surface-2 probe |
| please identify the risks in this plan | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.72 | MATCH | N=5 min; (a) FAILS (sub-threshold or other op) -> surface-2 probe |
