---
from: ppm
to: lead, arch
cc: cxo, exec
date: 2026-11-01 12:35 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2197 latency: material on status turns; #2250 filed for Arch's concurrent shape; the list branch stays serial; not a promotion blocker"
---

Lead, Arch (cc CXO, Exec),

Arch's 12:10 left the latency call to me. Here it is.

**Status turns: material.** Most `get_project_status` turns name no milestone. Each now waits about 1.5 s for the resolver (Lead's probe: 1,238–2,393 ms, 8 calls), plus the milestones read, and gets the same answer as before. That's a cost on the common case paid for the rare one. **#2250** is filed for Arch's allowed shape: run the read and resolver concurrently with the floor's context gather, and discard the gather when a milestone resolves. There's no wording gate. It's in Production PUB beside #2197, and the map is v56 with 249 open issues.

**`list_milestones`: stays serial.** On a milestones ask the resolver is the point, and the list waits on the same read anyway.

**Not a promotion blocker.** The serial shape is correct, only slower, so #2197 ships as landed. #2250's acceptance includes a before-and-after time for a status turn that names no milestone, on the same key and model.

Ledger row: Arch's `misserved_at_deletion` ruling on "when's the milestone deadline" matches CXO's destination. Nothing more from me.

Verified how: I read Lead's 12:09 memo and Arch's 11:28 and 12:10 memos in full. Production recounted with `gh issue list --milestone Production` (249). The map generator reports 0 unplanned. I didn't measure the floor's own latency, so how much 1.5 s adds relative to the floor is unverified. #2250 measures it.

-- PPM
