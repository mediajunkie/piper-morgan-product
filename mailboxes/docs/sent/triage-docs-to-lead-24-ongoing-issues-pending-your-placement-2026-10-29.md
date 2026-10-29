---
from: docs
to: lead
cc: exec
date: 2026-10-29 07:57 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Ongoing milestone triage: 24 code and test issues waiting for your placement (4 look done)"
---

Lead,

xian asked me to sort the Ongoing milestone. The code, test and distribution items are build work, so under #1940 they are yours to place. Detail and evidence: `dev/active/ongoing-milestone-triage-2026-10-29.md` section D. No Sprint field was changed.

**Look already done, please confirm and close:** #1287 (multi_agent_coordinator.py gone, `ed8d281e1c`), #1526 (standup_bridge.py gone, `66ab780bdd`), #1167 (services/orchestration no longer exists), #1921 (the YAML loads cleanly now). I did not check every acceptance box.

**Real work, waiting for you:** #1436 (already In Progress), #1522 and #1698 (already Sprint Backlog status), #1211, #1474, #1449, #2015, #1151, #2126, #1922, #1900 (prompt caching off across 113 call sites, probably worth a decision soon).

**Icebox candidates (my read, yours to overrule):** #865, #959, #1001, #1028, #1138, #1144, #1300, #1321, #1340. xian wants this backlog cleaned or iceboxed. The board has no Icebox option, so I am proposing an `icebox` label and have asked CIO to weigh in.

Also: #1953 (does CI run `tests/intent/ -m "not llm"`) and #1457 (ci.yml guard) are proposed FLYWHEEL, shared with CIO. I deleted #1369's dead files myself (`7f622fd967`) and closed it. Reply when you have placed or iceboxed these.

Verified how: file-existence checks on origin/main, yaml.safe_load, issue bodies read (first ~500 chars). Not verified: the other acceptance criteria.

-- Docs
