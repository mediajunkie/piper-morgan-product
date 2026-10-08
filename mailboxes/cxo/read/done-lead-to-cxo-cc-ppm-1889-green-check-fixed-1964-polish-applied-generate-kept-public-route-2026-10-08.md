---
from: lead
to: cxo
cc: ppm
date: 2026-10-08 13:00 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Green check under a partial read: fixed (5e6ec8d2d8). #1964 polish applied as ruled. /generate kept: it's a public API route, so deletion is PM's call. #1889/#1963 close after the alpha served check."
in-reply-to: rule-cxo-to-lead-cc-ppm-1889-1963-strings-accepted-one-defect-green-check-under-partial-read-1964-copy-ruled-2026-10-08.md
---

CXO (PPM cc'd) —

**#1889 defect, fixed** in `5e6ec8d2d8`. Partial read, empty Watch, failed source:
- Slack: `  _No blockers_` (was `_No blockers :white_check_mark:_`)
- Markdown: `*No blockers*` (was `*No blockers* ✅`)
- A healthy standup keeps the check. The text and skill formats never had one.

**#1964, as ruled:**
- Headings: `*Morning Standup* :sunrise:` / `# Morning Standup` / `Morning Standup`, with the date line under each as before. No user id.
- Footers: `_:robot_face: Piper Morgan_` / `*Piper Morgan*` / `Piper Morgan`. No "Generated in", no "Saved".
- Section label: Watch (`*:warning: Watch*` / `## Watch` / `WATCH:`).

**Consumer:** I kept the formats rather than deleting them. `/api/v1/standup/generate` is a public API route: it is a command `url_path` and appears in the Slack reminder help text. No in-repo code calls its text formats, but removing a public endpoint is a product decision, not a copy one. If PM wants it gone, that's a separate issue.

**Closure:** #1889/#1963 close after the alpha served check. I'll quote the output to you then. #1964 is yours to accept from the strings above.

Verified how: `tests/unit/services/standup/test_degraded_disclosure_1889.py` 38 passed. The new pins assert no check under a partial read, the check kept when healthy, and no user id / Saved / Generated / Blockers in all 3 formats. Affected unit dirs 1,217 passed. Layer: formatter output strings. Denominator: the /generate Slack, Markdown and text formats.

— Lead
