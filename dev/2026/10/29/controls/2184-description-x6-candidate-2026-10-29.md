# Router ×6 control — candidate

Run 2026-10-29 16:06Z · 6 sample(s) per phrase · 144 router calls · 0 ERROR · served: anthropic:claude-haiku-4-5 (144/144)

| phrase | routes (count) | confidence range |
|---|---|---|
| can you show me issues from just one milestone? | `list_milestones` ×6 | 0.95–0.95 |
| MVP | `CLARIFY` ×6 | 0.40–0.40 |
| show milestones | `list_milestones` ×6 | 0.95–0.95 |
| list the milestones for this quarter | `list_milestones` ×6 | 0.85–0.92 |
| what milestones do we have | `list_milestones` ×6 | 0.95–0.95 |
| milestones due this month | `list_milestones` ×6 | 0.92–0.92 |
| any upcoming milestones for this project | `list_milestones` ×6 | 0.85–0.85 |
| show my open issues | `list_issues` ×6 | 0.95–0.95 |
| show my last two new issues | `list_issues` ×6 | 0.92–0.92 |
| show my open issues in the MVP milestone | `list_issues` ×6 | 0.95–0.95 |
| open bugs labeled needs-triage | `list_issues` ×6 | 0.95–0.95 |
| what closed issues do I have | `list_issues` ×6 | 0.95–0.95 |
| what are my issues | `list_issues` ×6 | 0.95–0.95 |
| list the issues please | `list_issues` ×6 | 0.95–0.95 |
| show the issues | `list_issues` ×6 | 0.85–0.85 |
| what's the issue count | `list_issues` ×6 | 0.95–0.95 |
| which issues are assigned to engineering | `list_issues` ×6 | 0.85–0.85 |
| what issues are assigned to me? | `NONE` ×6 | 0.95–0.95 |
| let's analyze the risk here | `analyze_blockers` ×6 | 0.95–0.95 |
| add octocat/hello-world to the project | `CLARIFY` ×6 | 0.40–0.40 |
| what's the next milestone? | `list_milestones` ×6 | 0.92–0.95 |
| what's blocking the milestone? | `analyze_blockers` ×6 | 0.95–0.95 |
| any update on the next milestone | `list_milestones` ×6 | 0.85–0.85 |
| when's the milestone deadline | `list_milestones` ×4, `CLARIFY` ×2 | 0.40–0.85 |

## Samples

| phrase | # | route | conf | args | served | error |
|---|---|---|---|---|---|---|
| can you show me issues from just one milestone? | 1 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| can you show me issues from just one milestone? | 2 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| can you show me issues from just one milestone? | 3 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| can you show me issues from just one milestone? | 4 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| can you show me issues from just one milestone? | 5 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| can you show me issues from just one milestone? | 6 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 1 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 2 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 3 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 4 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 5 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| MVP | 6 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 1 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 2 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 3 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 4 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 5 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show milestones | 6 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 1 | `list_milestones` | 0.85 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 2 | `list_milestones` | 0.92 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 3 | `list_milestones` | 0.85 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 4 | `list_milestones` | 0.85 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 5 | `list_milestones` | 0.92 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| list the milestones for this quarter | 6 | `list_milestones` | 0.85 | timeframe=this quarter | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 1 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 2 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 3 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 4 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 5 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what milestones do we have | 6 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 1 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 2 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 3 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 4 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 5 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| milestones due this month | 6 | `list_milestones` | 0.92 | timeframe=this month | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 1 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 2 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 3 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 4 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 5 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any upcoming milestones for this project | 6 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show my open issues | 1 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues | 2 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues | 3 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues | 4 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues | 5 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues | 6 | `list_issues` | 0.95 | state=open | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 1 | `list_issues` | 0.92 | filter=recent; limit=2 | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 2 | `list_issues` | 0.92 | filter=recent; limit=2 | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 3 | `list_issues` | 0.92 | filter=new; limit=2; sort=recent | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 4 | `list_issues` | 0.92 | filter=recent; limit=2 | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 5 | `list_issues` | 0.92 | filter=new; limit=2; sort=recent | anthropic:claude-haiku-4-5 |  |
| show my last two new issues | 6 | `list_issues` | 0.92 | filter=recent; limit=2 | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 1 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 2 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 3 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 4 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 5 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| show my open issues in the MVP milestone | 6 | `list_issues` | 0.95 | milestone=MVP; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 1 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 2 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 3 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 4 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 5 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| open bugs labeled needs-triage | 6 | `list_issues` | 0.95 | label=needs-triage; state=open | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 1 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 2 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 3 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 4 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 5 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what closed issues do I have | 6 | `list_issues` | 0.95 | state=closed | anthropic:claude-haiku-4-5 |  |
| what are my issues | 1 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what are my issues | 2 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what are my issues | 3 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what are my issues | 4 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what are my issues | 5 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what are my issues | 6 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 1 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 2 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 3 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 4 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 5 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| list the issues please | 6 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 1 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 2 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 3 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 4 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 5 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| show the issues | 6 | `list_issues` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 1 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 2 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 3 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 4 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 5 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the issue count | 6 | `list_issues` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 1 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 2 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 3 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 4 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 5 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| which issues are assigned to engineering | 6 | `list_issues` | 0.85 | assignee=engineering | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 1 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 2 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 3 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 4 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 5 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what issues are assigned to me? | 6 | `NONE` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 1 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 2 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 3 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 4 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 5 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| let's analyze the risk here | 6 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 1 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 2 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 3 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 4 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 5 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| add octocat/hello-world to the project | 6 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 1 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 2 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 3 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 4 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 5 | `list_milestones` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's the next milestone? | 6 | `list_milestones` | 0.92 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 1 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 2 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 3 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 4 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 5 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| what's blocking the milestone? | 6 | `analyze_blockers` | 0.95 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 1 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 2 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 3 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 4 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 5 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| any update on the next milestone | 6 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 1 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 2 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 3 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 4 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 5 | `CLARIFY` | 0.4 | - | anthropic:claude-haiku-4-5 |  |
| when's the milestone deadline | 6 | `list_milestones` | 0.85 | - | anthropic:claude-haiku-4-5 |  |
