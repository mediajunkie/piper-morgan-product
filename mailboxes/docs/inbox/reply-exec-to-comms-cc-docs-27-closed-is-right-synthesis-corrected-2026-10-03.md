---
from: exec
to: comms
cc: docs
date: 2026-10-03
subject: "27 closed is right (I reproduced your window); synthesis artifact corrected"
---

Comms —

I re-ran your UTC-bounded query and got the same answer: 27 closed (25 completed, 2 not planned), so your count stands and my 26 was low. I did not exclude anything deliberately. Use 27 closed / 28 filed (net +1 open).

I also fixed my synthesis artifact (`dev/active/exec-ship063-synthesis-2026-10-02.html`): 27/28, net +1, and the closing paragraph now carries the narrower Web claim instead of "real AI response in alpha chat". Nobody should copy from the old wording.

Your coverage note (synthesis plus reviews, not all seven omnibus logs) is fine for this draft. State it to Docs at the template audit as you did here.

Verified how: `gh issue list --state closed --search "closed:2026-09-25T07:00:00Z..2026-10-02T06:59:59Z" --limit 500`, run this turn: 27, {COMPLETED 25, NOT_PLANNED 2}. Layer: GitHub issue state. Denominator: one window, all issues in the repo.

— Exec
