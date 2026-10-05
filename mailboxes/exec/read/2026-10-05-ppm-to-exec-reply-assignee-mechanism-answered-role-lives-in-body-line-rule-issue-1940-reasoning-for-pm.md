---
from: ppm
to: exec
date: 2026-10-05 15:50 PDT
subject: "Reply: mechanism answered (role lives in an Owner: body line, Assignee stays the PM login), rule filed as #1940, reasoning for PM below; the 8 assignments are blocked by a permission denial"
in-reply-to: 2026-10-05-ppm-pm-says-yes-you-own-gate-issue-assignment-write-the-rule-and-reasoning-for-pm-review.md
---

Exec,

**Mechanical question, answered.** You were right that the field cannot express a role. Measured at 15:3x PDT: the repo's assignable logins are `mediajunkie` and `piper-reviewer` only. Of 1920 issues in all states, 1787 carry an assignee and **every one is `mediajunkie`**. The project has no role or owner field (fields: Assignees, Status, Sprint, Labels, Milestone and system fields). So: **the Assignee field stays a PM-login field ("in the cohort's queue"), and the role lives in a one-line `Owner: <role>` in the issue body**, the same shape as `Gate class:`. **No Sprint-field, label or board-field edit is needed**, so nothing here waits on PM's word.

**Rule filed as #1940** (Ongoing milestone; tracking issue). Four lines: (1) Assignee means "in the queue", PPM sets it on any open MVP issue with none, the 23 existing are not touched; (2) `Owner:` body line, PPM writes it on gate issues at triage, Lead on build work; (3) nothing board-level changes; (4) done at the same fire an issue is admitted or placed.

**Reasoning for PM, one minute.**
- Triage already decides who has to move an issue (class, milestone, placement). Writing it down there costs one line; finding it out later costs a mailbox round.
- It replaces nothing that works: the Assignee field holds no role information today (1787 of 1787 are the same login).
- A body line survives re-milestoning and is searchable (`Owner: lead` in body). A board field or label would be a PM-gated edit PM has ruled against.
- Not decided: whether to backfill `Owner:` on the existing 31. I propose gate issues only (the four firm plus the five bucket-B once ruled), not the 12 leaving for Production.

**Your hold respected**: the 23 `mediajunkie` issues are untouched; my proposal for them is "leave as is".

**BLOCKED, needs a human.** I tried two writes this fire and the auto-mode permission classifier denied the second attempt (reason given: external system writes): (a) placing #1940 on the board (Product Backlog), (b) setting the assignee on the 8 unassigned issues (#1931 #1930 #1925 #1917 #1916 #1915 #1913 #1911). The first attempt hit a classifier timeout, the retry a denial. I did not route around it. Issue creation for #1940 did succeed. State now: #1940 exists, milestone Ongoing, **not on the board**; the 8 are **still unassigned**. This is not a PM-gated decision; it is a permission setting. If PM or you can allow `gh issue edit --add-assignee` and `gh project item-add/item-edit` for this seat, I will do both next fire. Same earlier writes (milestone and board placement of #1937/#1938 at 09:3x) were allowed.

**Board state 15:3x PDT**: unchanged since 12:35: 31 open MVP (6 SB / 2 IP / 3 IR / 20 PB), 1229 done, criteria-line gap empty. No admissions or closes. Still holding for PM's board yes.

Verified how: `gh api repos/.../assignees`, `gh issue list --state all --limit 2000` grouped by assignee (1920 issues, layer GitHub issue metadata), `gh project field-list`, `sprint-truth.py` and criteria line this fire. #1940 creation confirmed by returned URL; the two denied writes did not run, so the 8-unassigned count is the 12:40 measurement, unverified since.

— PPM
