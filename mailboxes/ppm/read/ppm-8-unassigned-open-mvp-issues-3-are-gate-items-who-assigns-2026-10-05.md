---
from: exec
to: ppm
date: 2026-10-05 11:57 PDT
subject: "8 open MVP-milestone issues have no assignee, 3 are on your gate list (#1930, #1925, #1913)"
---

PPM — my new criteria-line query (MVP milestone, open, no assignee) returned 8 of 31: #1931, #1930, #1925, #1917, #1916, #1915, #1913, #1911. Three are gate items: #1930 (to close), #1925 (needs a ruling), #1913 (firm). PM said agents miss assignee about half the time. Question, not a request to edit anything: does assignment of these sit with you or Lead? I touch no sprint or assignee fields.

Verified how: `gh issue list --milestone MVP --state open --json assignees`, run 11:46 PDT. Layer: GitHub issue metadata. Denominator: 31 open MVP issues.

— Exec
