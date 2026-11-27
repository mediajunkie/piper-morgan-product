# Project consult (2425) screen ×6 — 2425 consult on 705a7d5a30, stored projects: Harbor Pilot, Launch, Mobile Redesign

Run 2026-11-27 16:51Z · 6 sample(s) per phrase · ceiling 1.5 s · consult fact line: `STORED PROJECTS: "Harbor Pilot", "Launch", "Mobile Redesign"`

| phrase | main routes | consults fired | accepted | final routes | consult s min / median / max | timeouts |
|---|---|---|---|---|---|---|
| add a task to my Launch project: book the venue | `CLARIFY` ×3, `create_todo` ×3 | 3 | 3 | `create_todo` ×6 | 1.278 / 1.298 / 1.308 | 0 |
| add a task to the Launch project: book the venue | `CLARIFY` ×6 | 6 | 0 | `CLARIFY` ×6 | 1.242 / 1.311 / 1.375 | 0 |
| I need to remember to submit my timesheet | `create_todo` ×6 | 0 | 0 | `create_todo` ×6 | - | 0 |
| update project plan with new deadline | `CLARIFY` ×6 | 6 | 0 | `CLARIFY` ×6 | 1.056 / 1.072 / 1.092 | 0 |
| modify the status document | `update_document` ×6 | 0 | 0 | `update_document` ×6 | - | 0 |
| show me the todos in the Launch project | `CLARIFY` ×6 | 6 | 0 | `CLARIFY` ×6 | 1.093 / 1.175 / 1.318 | 0 |
| can you show me the tasks in the Launch project? | `CLARIFY` ×6 | 6 | 0 | `CLARIFY` ×6 | 1.071 / 1.085 / 1.116 | 0 |
| add a task: book the venue | `create_todo` ×6 | 0 | 0 | `create_todo` ×6 | - | 0 |
| create a github issue: book the venue | `create_issue` ×6 | 0 | 0 | `create_issue` ×6 | - | 0 |
| add renew passport to my personal list | `create_todo` ×6 | 0 | 0 | `create_todo` ×6 | - | 0 |
| add a task to my Apollo project: book the venue | `CLARIFY` ×6 | 6 | 0 | `CLARIFY` ×6 | 1.200 / 1.277 / 1.471 | 0 |

## Samples

| phrase | # | main | main s | fired | consult route | consult args | accepted | final | final args | consult s | ceiling hit | error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add a task to my Launch project: book the venue | 1 | `CLARIFY` | 1.466 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.278 | False |  |
| add a task to my Launch project: book the venue | 2 | `create_todo` | 1.326 | False | `-` | - | False | `create_todo` | project=Launch; text=book the venue | - | False |  |
| add a task to my Launch project: book the venue | 3 | `create_todo` | 1.367 | False | `-` | - | False | `create_todo` | project=Launch; text=book the venue | - | False |  |
| add a task to my Launch project: book the venue | 4 | `create_todo` | 1.427 | False | `-` | - | False | `create_todo` | project=Launch; text=book the venue | - | False |  |
| add a task to my Launch project: book the venue | 5 | `CLARIFY` | 1.188 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.298 | False |  |
| add a task to my Launch project: book the venue | 6 | `CLARIFY` | 1.280 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.308 | False |  |
| add a task to the Launch project: book the venue | 1 | `CLARIFY` | 1.217 | True | `NONE` | - | False | `CLARIFY` | - | 1.319 | False |  |
| add a task to the Launch project: book the venue | 2 | `CLARIFY` | 1.182 | True | `NONE` | - | False | `CLARIFY` | - | 1.335 | False |  |
| add a task to the Launch project: book the venue | 3 | `CLARIFY` | 1.254 | True | `NONE` | - | False | `CLARIFY` | - | 1.270 | False |  |
| add a task to the Launch project: book the venue | 4 | `CLARIFY` | 1.177 | True | `NONE` | - | False | `CLARIFY` | - | 1.375 | False |  |
| add a task to the Launch project: book the venue | 5 | `CLARIFY` | 1.198 | True | `NONE` | - | False | `CLARIFY` | - | 1.242 | False |  |
| add a task to the Launch project: book the venue | 6 | `CLARIFY` | 1.229 | True | `NONE` | - | False | `CLARIFY` | - | 1.303 | False |  |
| I need to remember to submit my timesheet | 1 | `create_todo` | 1.143 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| I need to remember to submit my timesheet | 2 | `create_todo` | 1.228 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| I need to remember to submit my timesheet | 3 | `create_todo` | 1.170 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| I need to remember to submit my timesheet | 4 | `create_todo` | 1.104 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| I need to remember to submit my timesheet | 5 | `create_todo` | 1.163 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| I need to remember to submit my timesheet | 6 | `create_todo` | 1.180 | False | `-` | - | False | `create_todo` | task=submit my timesheet | - | False |  |
| update project plan with new deadline | 1 | `CLARIFY` | 1.233 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.073 | False |  |
| update project plan with new deadline | 2 | `CLARIFY` | 1.152 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.070 | False |  |
| update project plan with new deadline | 3 | `CLARIFY` | 1.092 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.092 | False |  |
| update project plan with new deadline | 4 | `CLARIFY` | 1.105 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.080 | False |  |
| update project plan with new deadline | 5 | `CLARIFY` | 1.180 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.056 | False |  |
| update project plan with new deadline | 6 | `CLARIFY` | 1.119 | True | `CLARIFY` | - | False | `CLARIFY` | - | 1.065 | False |  |
| modify the status document | 1 | `update_document` | 1.238 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| modify the status document | 2 | `update_document` | 1.288 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| modify the status document | 3 | `update_document` | 1.257 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| modify the status document | 4 | `update_document` | 1.351 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| modify the status document | 5 | `update_document` | 1.271 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| modify the status document | 6 | `update_document` | 1.350 | False | `-` | - | False | `update_document` | document=status document | - | False |  |
| show me the todos in the Launch project | 1 | `CLARIFY` | 1.231 | True | `NONE` | - | False | `CLARIFY` | - | 1.178 | False |  |
| show me the todos in the Launch project | 2 | `CLARIFY` | 1.117 | True | `NONE` | - | False | `CLARIFY` | - | 1.296 | False |  |
| show me the todos in the Launch project | 3 | `CLARIFY` | 1.230 | True | `NONE` | - | False | `CLARIFY` | - | 1.318 | False |  |
| show me the todos in the Launch project | 4 | `CLARIFY` | 1.099 | True | `NONE` | - | False | `CLARIFY` | - | 1.093 | False |  |
| show me the todos in the Launch project | 5 | `CLARIFY` | 1.198 | True | `NONE` | - | False | `CLARIFY` | - | 1.150 | False |  |
| show me the todos in the Launch project | 6 | `CLARIFY` | 1.225 | True | `NONE` | - | False | `CLARIFY` | - | 1.173 | False |  |
| can you show me the tasks in the Launch project? | 1 | `CLARIFY` | 1.093 | True | `NONE` | - | False | `CLARIFY` | - | 1.101 | False |  |
| can you show me the tasks in the Launch project? | 2 | `CLARIFY` | 1.157 | True | `NONE` | - | False | `CLARIFY` | - | 1.082 | False |  |
| can you show me the tasks in the Launch project? | 3 | `CLARIFY` | 1.289 | True | `NONE` | - | False | `CLARIFY` | - | 1.116 | False |  |
| can you show me the tasks in the Launch project? | 4 | `CLARIFY` | 1.175 | True | `NONE` | - | False | `CLARIFY` | - | 1.081 | False |  |
| can you show me the tasks in the Launch project? | 5 | `CLARIFY` | 1.241 | True | `NONE` | - | False | `CLARIFY` | - | 1.071 | False |  |
| can you show me the tasks in the Launch project? | 6 | `CLARIFY` | 1.154 | True | `NONE` | - | False | `CLARIFY` | - | 1.089 | False |  |
| add a task: book the venue | 1 | `create_todo` | 1.045 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| add a task: book the venue | 2 | `create_todo` | 1.028 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| add a task: book the venue | 3 | `create_todo` | 1.038 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| add a task: book the venue | 4 | `create_todo` | 1.110 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| add a task: book the venue | 5 | `create_todo` | 1.047 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| add a task: book the venue | 6 | `create_todo` | 1.135 | False | `-` | - | False | `create_todo` | task=book the venue | - | False |  |
| create a github issue: book the venue | 1 | `create_issue` | 1.162 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| create a github issue: book the venue | 2 | `create_issue` | 1.188 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| create a github issue: book the venue | 3 | `create_issue` | 1.065 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| create a github issue: book the venue | 4 | `create_issue` | 1.080 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| create a github issue: book the venue | 5 | `create_issue` | 1.110 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| create a github issue: book the venue | 6 | `create_issue` | 1.054 | False | `-` | - | False | `create_issue` | title=book the venue | - | False |  |
| add renew passport to my personal list | 1 | `create_todo` | 1.143 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add renew passport to my personal list | 2 | `create_todo` | 1.175 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add renew passport to my personal list | 3 | `create_todo` | 1.129 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add renew passport to my personal list | 4 | `create_todo` | 1.320 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add renew passport to my personal list | 5 | `create_todo` | 1.219 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add renew passport to my personal list | 6 | `create_todo` | 1.374 | False | `-` | - | False | `create_todo` | list=personal; text=renew passport | - | False |  |
| add a task to my Apollo project: book the venue | 1 | `CLARIFY` | 1.201 | True | `NONE` | - | False | `CLARIFY` | - | 1.361 | False |  |
| add a task to my Apollo project: book the venue | 2 | `CLARIFY` | 1.240 | True | `NONE` | - | False | `CLARIFY` | - | 1.200 | False |  |
| add a task to my Apollo project: book the venue | 3 | `CLARIFY` | 1.285 | True | `NONE` | - | False | `CLARIFY` | - | 1.205 | False |  |
| add a task to my Apollo project: book the venue | 4 | `CLARIFY` | 1.174 | True | `NONE` | - | False | `CLARIFY` | - | 1.311 | False |  |
| add a task to my Apollo project: book the venue | 5 | `CLARIFY` | 1.215 | True | `NONE` | - | False | `CLARIFY` | - | 1.242 | False |  |
| add a task to my Apollo project: book the venue | 6 | `CLARIFY` | 1.152 | True | `NONE` | - | False | `CLARIFY` | - | 1.471 | False |  |
