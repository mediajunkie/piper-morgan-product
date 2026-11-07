# ADR-083 screen batch — result (2026-11-06, Lead)

Preregistration: `dev/2026/11/06/controls/adr-083-batch-prereg-2026-11-06.md` (with Arch's 16:53 flip definition), committed before any render.

- Batch 1: `msgbatch_01768ZoVxidGDG4tCYAZ2EmJ`, 1,332/1,332 succeeded (A corpus 624 ×1, A sentinels 7 ×6, C corpus 624 ×1, C sentinels 7 ×6). Served model `claude-haiku-4-5-20251001` (42/42 sentinel replies).
- Batch 2 (the preregistered flip re-run): `msgbatch_01EGwjmGDtR61bX3oxCKirzv`, 540/540 succeeded (45 flipped rows ×6 on A and on C).
- Cost about $3.45 at batch prices (1,872 requests at ~$0.00185); Exec's ceiling $10.
- Arm C: the slot `LAST LIST SHOWN: 7 numbered todos` on every request (the worst case). A's 622 shared rows are byte-identical to main's render; A adds only the two #2269 3a rows.

## Verdict: FAIL. ADR-083 stays PROPOSED; the interim stands.

**Sentinels: C passes its bar.**
```
== A-sent
  'complete the second one': {'CLARIFY': 6} args=['{}']
  'delete the third one': {'CLARIFY': 6} args=['{}']
  'delete the second one': {'CLARIFY': 6} args=['{}']
  'mark the first one done': {'complete_todo': 6} args=['{"targets": ["1"]}']
  'remove the last one': {'CLARIFY': 6} args=['{}']
  'what is on my calendar today': {'meeting_time': 6} args=['{"day": "today"}']
  'delete the first two': {'CLARIFY': 6} args=['{}']
== C-sent
  'complete the second one': {'complete_todo': 6} args=['{"targets": ["2"]}']
  'delete the third one': {'delete_todo': 6} args=['{"targets": ["3"]}']
  'delete the second one': {'delete_todo': 6} args=['{"targets": ["2"]}']
  'mark the first one done': {'complete_todo': 6} args=['{"targets": ["1"]}']
  'remove the last one': {'delete_todo': 6} args=['{"targets": ["last"]}']
  'what is on my calendar today': {'meeting_time': 6} args=['{"day": "today"}']
  'delete the first two': {'delete_todo': 6} args=['{"targets": ["1", "2"]}']
```

**Corpus: C fails clauses 1 and 3.** 45 of 624 rows flipped at ×1; re-run ×6 on both arms, every flip held (0 of 45 was noise). Clause 1 (A ≥ 5/6 → C < 5/6): 14 rows. Clause 2: 1 row. Clause 3 (a label in ≥ 3/6 that A never produced): 37 rows. 38 rows violate at least one clause. Rows marked VIOL below; `exp` is the corpus expectation.
```
VIOL CL1 CL3:manage_portfolio | 'list my projects' exp=action:list_projects | A={'list_projects': 6} (6/6) | C={'manage_portfolio': 6} (0/6)
VIOL  CL3:get_top_priority | "what's my next todo?" exp=REVIEW | A={'list_todos_query': 6} (0/6) | C={'get_top_priority': 6} (0/6)
VIOL  CL3:list_milestones | 'status of the Fast Follow milestone' exp=action:get_project_status | A={'review_issue': 6} (0/6) | C={'list_milestones': 6} (0/6)
ok   | 'finish the second one' exp=REVIEW | A={'CLARIFY': 5, 'complete_todo': 1} (0/6) | C={'complete_todo': 6} (0/6)
ok   | 'update my project name to Atlas' exp=floor | A={'CLARIFY': 6} (6/6) | C={'CLARIFY': 5, 'update_document': 1} (5/6)
VIOL  CL3:CLARIFY | 'delete my reminders' exp=REVIEW | A={'delete_todo': 6} (0/6) | C={'CLARIFY': 6} (0/6)
VIOL  CL3:NONE | 'use the standup interview format by default from now on' exp=REVIEW | A={'get_contextual_guidance': 6} (0/6) | C={'NONE': 6} (0/6)
ok   | 'Create a doc from this conversation' exp=REVIEW | A={'NONE': 2, 'CLARIFY': 4} (0/6) | C={'NONE': 6} (0/6)
VIOL CL1 CL3:NONE | 'show me completed todos' exp=action:list_todos_query | A={'list_todos_query': 6} (6/6) | C={'NONE': 6} (0/6)
VIOL CL1 | 'I could use some guidance on this' exp=floor | A={'CLARIFY': 5, 'NONE': 1} (6/6) | C={'CLARIFY': 2, 'NONE': 2, 'get_contextual_guidance': 2} (4/6)
VIOL  CL3:get_contextual_guidance | 'advise me on this decision' exp=action:get_contextual_guidance | A={'CLARIFY': 6} (0/6) | C={'get_contextual_guidance': 6} (6/6)
VIOL  CL3:prioritize | 'this is the highest priority item' exp=action:get_top_priority | A={'NONE': 6} (0/6) | C={'prioritize': 6} (0/6)
VIOL  CL3:get_top_priority | 'show priorities for this sprint' exp=floor | A={'prioritize': 6} (0/6) | C={'get_top_priority': 6} (0/6)
VIOL CL1 CL3:meeting_time | 'what meetings are coming up' exp=action:week_calendar | A={'week_calendar': 6} (6/6) | C={'meeting_time': 6} (0/6)
VIOL CL1 CL3:week_calendar | 'how much time do I spend sitting in meetings' exp=action:meeting_time | A={'meeting_time': 6} (6/6) | C={'week_calendar': 6} (0/6)
VIOL CL1 CL3:create_reminder | 'find time for a 1:1 with sarah' exp=floor | A={'NONE': 6} (6/6) | C={'create_reminder': 6} (0/6)
VIOL CL1 CL3:meeting_time | 'what are the upcoming meetings' exp=action:week_calendar | A={'week_calendar': 6} (6/6) | C={'week_calendar': 2, 'meeting_time': 4} (2/6)
VIOL  CL3:CLARIFY | "this week's priorities, remind me" exp=plan | A={None: 6} (0/6) | C={'CLARIFY': 6} (0/6)
ok   | "this month's numbers, remind me" exp=plan | A={None: 6} (0/6) | C={None: 6} (0/6)
VIOL  CL3:get_top_priority | 'what is my most important work today' exp=action:get_top_priority | A={'attention_query': 6} (0/6) | C={'get_top_priority': 6} (6/6)
VIOL  CL3:list_milestones | 'any upcoming milestones for this project' exp=action:list_milestones | A={'CLARIFY': 6} (0/6) | C={'list_milestones': 6} (6/6)
VIOL  CL3:get_project_status | "what's my current project" exp=action:get_project_status | A={'NONE': 3, 'CLARIFY': 3} (0/6) | C={'get_project_status': 5, 'CLARIFY': 1} (5/6)
ok   | 'what are my active projects' exp=action:manage_portfolio | A={'list_projects': 5, 'manage_portfolio': 1} (1/6) | C={'list_projects': 4, 'manage_portfolio': 2} (2/6)
ok   | "what's the current status" exp=action:get_project_status | A={'get_project_status': 6} (6/6) | C={'get_project_status': 6} (6/6)
VIOL CL1 CL3:list_todos_query | "what's the task status" exp=action:get_project_status | A={'CLARIFY': 1, 'get_project_status': 5} (5/6) | C={'list_todos_query': 6} (0/6)
VIOL  CL3:NONE | 'I need help understanding something' exp=action:get_capabilities | A={'CLARIFY': 6} (0/6) | C={'NONE': 6} (0/6)
VIOL  CL3:analyze_blockers | "what's in the way of finishing this" exp=action:analyze_blockers | A={'CLARIFY': 6} (0/6) | C={'analyze_blockers': 6} (6/6)
VIOL  CL3:NONE | 'can you run an impact analysis on this change' exp=action:analyze_blockers | A={'CLARIFY': 6} (0/6) | C={'NONE': 6} (0/6)
VIOL CL1 CL3:NONE | 'how do you see our relationship evolving' exp=action:explain_trust | A={'explain_trust': 6} (6/6) | C={'NONE': 6} (0/6)
VIOL  CL3:NONE | 'search history for that conversation topic' exp=action:get_memory | A={'CLARIFY': 6} (0/6) | C={'NONE': 6} (0/6)
VIOL  CL3:link_repo | 'connect my repository to the project' exp=action:manage_repos | A={'CLARIFY': 6} (0/6) | C={'link_repo': 6} (0/6)
VIOL CL1 CL3:NONE | 'are we behind upstream at all' exp=action:local_git_status_query | A={'local_git_status_query': 6} (6/6) | C={'local_git_status_query': 3, 'NONE': 3} (3/6)
VIOL  CL3:generate_report | 'show me my productivity report' exp=action:productivity_query | A={'productivity': 6} (0/6) | C={'generate_report': 6} (0/6)
ok   | 'Where did you get that from?' exp=action:explain_suggestion | A={'CLARIFY': 6} (0/6) | C={'CLARIFY': 3, 'NONE': 2, 'explain_suggestion': 1} (1/6)
VIOL  CL3:explain_trust | 'How did you know about that?' exp=action:explain_suggestion | A={'CLARIFY': 6} (0/6) | C={'explain_trust': 6} (0/6)
VIOL  CL3:explain_suggestion | "What's that based on?" exp=action:explain_suggestion | A={'CLARIFY': 6} (0/6) | C={'explain_suggestion': 6} (6/6)
VIOL CL1 CL3:CLARIFY | 'hide the project Beta' exp=action:archive_project | A={'archive_project': 6} (6/6) | C={'CLARIFY': 5, 'NONE': 1} (0/6)
VIOL CL1 CL3:CLARIFY | 'put the old project away' exp=action:archive_project | A={'archive_project': 6} (6/6) | C={'CLARIFY': 6} (0/6)
VIOL  CL3:NONE | 'edit the meeting notes document' exp=action:update_document_query | A={'CLARIFY': 6} (0/6) | C={'NONE': 6} (0/6)
VIOL  CL3:update_document | 'update project plan with new deadline' exp=action:update_document_query | A={'CLARIFY': 6} (0/6) | C={'update_document': 6} (0/6)
VIOL  CL3:CLARIFY | 'modify the onboarding checklist with the new steps' exp=action:update_document_query | A={'update_document': 6} (0/6) | C={'CLARIFY': 6} (0/6)
VIOL  CL3:complete_todo | 'Can we just mark done here?' exp=action:complete_todo | A={'CLARIFY': 6} (0/6) | C={'complete_todo': 6} (6/6)
VIOL CL2 CL3:update_todo | "Actually, change the title to 'Implement full-text search across nav and global search bar'" exp=action:update_issue | A={'CLARIFY': 2, 'update_issue': 4} (4/6) | C={'update_todo': 6} (0/6)
VIOL CL1 CL3:create_reminder | 'Find time for a 1:1 with the team lead' exp=floor | A={'NONE': 6} (6/6) | C={'create_todo': 2, 'create_reminder': 4} (0/6)
VIOL CL1 CL3:CLARIFY | 'Summarize this file' exp=action:summarize_document | A={'summarize_document': 6} (6/6) | C={'CLARIFY': 6} (0/6)
violations: 38
```

## The four new rows on A (their own measurement)
```
  NEWROW link repo octocat/hello-world to Mobile Redesign {'A-corpus': 'link_repo', 'C-corpus': 'link_repo'}
  NEWROW unlink repo octocat/hello-world from Mobile Redesign {'A-corpus': 'unlink_repo', 'C-corpus': 'unlink_repo'}
  NEWROW link repo dinp-machine/piper-test-activity to zz share-hide project {'A-corpus': 'link_repo', 'C-corpus': 'link_repo'}
  NEWROW I want to add a repo to my zz share-hide project {'A-corpus': 'link_repo', 'C-corpus': 'link_repo'}
```
All four route as written on A (×1).
