# Project consult (2425) full-corpus run — 2425 full corpus at 11f0ca7d40, 2.0 s ceiling, six stored projects

Run 2026-11-27 17:27Z · ceiling 2.0 s · consult fact line: `STORED PROJECTS: "Harbor Pilot", "Launch", "Mobile Redesign", "Onboarding", "Test", "Website"`

| rows | main CLARIFY | consults fired | accepted | timeouts | errors | consult s min / median / max |
|---|---|---|---|---|---|---|
| 630 | 62 | 62 | 0 | 1 | 0 | 1.021 / 1.187 / 2.002 |

Moved rows (accepted): 0. `create_todo` with a stored project: 0. Anything else: 0 (0 by construction of the accept rule, which takes only create_todo naming one stored project; counted anyway).

## Rows where the consult fired (moved rows first)

| row | phrase | expected | main | consult route | consult args | accepted | final | final args | consult s |
|---|---|---|---|---|---|---|---|---|---|
| 28 | can you clarify what you meant? | REVIEW | `CLARIFY` | `explain_suggestion` | - | False | `CLARIFY` | - | 1.286 |
| 41 | add a repo to my portfolio | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.269 |
| 88 | look at this project/repository. Give me quick feedback and then help me to move forward. | action:get_project_status | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.508 |
| 92 | can you show me issues from just one milestone? | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.190 |
| 93 | MVP | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.213 |
| 101 | delete that reminder | action:delete_todo | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.096 |
| 102 | delete a reminder | action:delete_todo | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.299 |
| 110 | finish the second one | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.082 |
| 114 | update my project name to Atlas | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.091 |
| 119 | Yes please | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.180 |
| 138 | remind me | action:create_reminder | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.168 |
| 143 | use the interview from now on | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.094 |
| 150 | Create a doc from this conversation | REVIEW | `CLARIFY` | `NONE` | - | False | `CLARIFY` | - | 1.171 |
| 175 | I could use some guidance on this | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.208 |
| 176 | do you have a recommendation | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.232 |
| 177 | what's your advice here | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.300 |
| 181 | advise me on this decision | action:get_contextual_guidance | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.142 |
| 197 | mark this as priority one | action:prioritize | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.046 |
| 231 | not sure what to do about this | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.098 |
| 297 | schedule check for today | action:week_calendar | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.255 |
| 307 | show all events | action:week_calendar | `CLARIFY` | `NONE` | - | False | `CLARIFY` | - | 1.277 |
| 316 | when was the last time I worked on this | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.227 |
| 317 | how long have I been working on this | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.201 |
| 332 | close the completed issue | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.105 |
| 333 | please close this issue | action:close_issue_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.116 |
| 335 | reopen the old issue | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.203 |
| 336 | re-open the old issue | floor | `CLARIFY` | `-` | - | False | `CLARIFY` | - | 2.002 |
| 361 | when's the milestone deadline | action:list_milestones | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.099 |
| 391 | any upcoming milestones for this project | action:list_milestones | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.115 |
| 412 | what's the progress on this | action:get_project_status | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.130 |
| 424 | what's the task status | action:get_project_status | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.062 |
| 447 | I need help understanding something | action:get_capabilities | `CLARIFY` | `NONE` | - | False | `CLARIFY` | - | 1.117 |
| 451 | what's the main obstacle here | action:analyze_blockers | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.321 |
| 452 | what's in the way of finishing this | action:analyze_blockers | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.284 |
| 455 | can you run an impact analysis on this change | action:analyze_blockers | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.220 |
| 487 | search history for that conversation topic | action:get_memory | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.260 |
| 491 | link my repository to the project | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.244 |
| 492 | connect my repository to the project | action:manage_repos | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.086 |
| 494 | add octocat/hello-world to the project | action:link_repo | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.143 |
| 495 | please unlink my repository from this project | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.089 |
| 496 | please remove my repository from this project | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.146 |
| 499 | which repo connected to this project should i check | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.200 |
| 570 | Where did you get that from? | action:explain_suggestion | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.314 |
| 574 | Why is that on your list? | action:explain_suggestion | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.209 |
| 575 | Based on what? | action:explain_suggestion | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.211 |
| 576 | What's that based on? | action:explain_suggestion | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.223 |
| 584 | bring back my archived project | action:restore_project | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.027 |
| 586 | find project deadline | action:search_projects | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.183 |
| 594 | edit the meeting notes document | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.295 |
| 596 | change the spec doc | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.144 |
| 597 | add to the notes document new items | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.101 |
| 598 | append to the log doc | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.183 |
| 599 | update project plan with new deadline | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.304 |
| 600 | edit the report with corrections | action:update_document_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.172 |
| 601 | modify the onboarding checklist with the new steps | action:update_document_query | `CLARIFY` | `update_document` | action=modify with new steps; document=onboarding checklist | False | `CLARIFY` | - | 1.603 |
| 612 | Can we just mark done here? | action:complete_todo | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.181 |
| 617 | Actually, change the title to 'Implement full-text search across nav and global search bar' | action:update_issue | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.211 |
| 618 | Also we should call it out in the release notes | floor | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.021 |
| 621 | Show me that issue. | action:review_issue_query | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.212 |
| 625 | What does this document say? | action:analyze_document | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.104 |
| 628 | make clear mark them done | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.281 |
| 630 | make take care of mean mark it done | REVIEW | `CLARIFY` | `CLARIFY` | - | False | `CLARIFY` | - | 1.111 |
