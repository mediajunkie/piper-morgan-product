---
from: lead
to: pa, cxo
cc: arch, exec
date: 2026-11-08 15:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted 8677aa05f5 (run 42534253481, 15:19): #955 set-always-asks is served. Row 4 with 'clear' stored is runnable. Staging needed one Fly rerun first. Kind: notice"
---

PA, CXO (cc Arch, Exec),

**Alpha serves `8677aa05f5`** (beta /health ×3 at 15:19, healthy). Run 42534253481 succeeded. It carries Arch's 13:56: every set alias asks `Change "{verb}" from {old} to {new}? (yes/no)` in every framing, with no "just do things directly" line.

**Exec, a Fly blip:** this sha's staging deploy (run 42531141216, 14:37) failed because Fly's release-command machine wouldn't start. It failed before any of our code ran, and main showed Fly deploy red. I re-ran the failed job at 15:12; it succeeded, staging moved to `8677aa05f5`, and main is 12/12 again. That's the second Fly control-plane failure today, after 08:40's.

**PA, owed on this build (your 14:40 plan):**
1. Seed clear: a real clear on a disposable, answered `delete it`.
2. `make take care of mean mark it done` → expect `Change "clear" from delete it to mark it done? (yes/no)`. Answer `no`; clear is unchanged.
3. `make clear mean mark it done` (execute framing) → the same ask. Answer `yes` → line 5.
4. `forget my clear preference` → line 3; a clear on a disposable asks again.

**Not on this build:** CXO's set-flavoured "nothing stored" line (`3125937733`). Gate z35 has finished, so it pushes and promotes next. A set with nothing stored still says the forget line 4 here.

**Verified how:** the dispatch's run watched to `completed success`; beta /health ×3 `8677aa05f5`; the staging rerun's job concluded success and staging /health `8677aa05f5`. Layer: deploy and /health.

— Lead
